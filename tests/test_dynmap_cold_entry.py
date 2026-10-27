"""Bounded source and projection checks for the cold-entry repaint path.

The fixtures model the declared algorithm only; they are not CK3 engine proof.
"""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "research/probes/my-dynasty-r016/mod/common/scripted_effects/dynmap_r016.txt").read_text(encoding="utf-8-sig")


def effect(name, source=SOURCE):
    match = re.search(r"(?ms)^" + re.escape(name) + r"\s*=\s*\{(.*?)^\}", source)
    if not match:
        raise AssertionError("missing effect: " + name)
    return match.group(1)


def balanced_body(source, opening):
    depth = 0
    quoted = escaped = False
    for end in range(opening, len(source)):
        char = source[end]
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return source[opening + 1:end], end + 1
    raise AssertionError("unclosed source block")


def direct_blocks(source, indent):
    pattern = re.compile(r"(?m)^" + re.escape(indent) + r"(if|else_if|else)\s*=\s*\{")
    for match in pattern.finditer(source):
        body, end = balanced_body(source, source.find("{", match.start()))
        yield match.group(1), match.start(), body, end


def assert_diagnostic_write_accounting(source):
    increment = "change_local_variable = { name = dynmap_r016_d_attempted_writes add = 1 }"
    base = effect("dynmap_r016_paint_neutral_base_effect", source)
    barony_match = re.search(r"every_barony\s*=\s*\{", base)
    if not barony_match:
        raise AssertionError("neutral base must contain a flat every_barony body")
    body, _ = balanced_body(base, base.find("{", barony_match.start()))
    if body.count("set_title_color = { 65 70 80 }") != 1:
        raise AssertionError("each base barony must receive exactly one neutral RGB write")
    if body.count(increment) != 1:
        raise AssertionError("each base barony write must be counted exactly once")
    base_guards = [b for k, _, b, _ in direct_blocks(body, "\t\t\t")
                   if k == "if" and "exists = scope:dynmap_r016_diagnostic_armed" in b]
    if len(base_guards) != 1 or base_guards[0].count(increment) != 1:
        raise AssertionError("base write counter must be enclosed by its diagnostic guard")
    # Palette branches now choose a literal at county scope, then traverse
    # baronies inside that branch. Each branch must retain one guarded count.
    for name in ("dark", "light"):
        paint = effect("dynmap_r016_paint_" + name + "_effect", source)
        branches = [b for _, _, b, _ in direct_blocks(paint, "\t\t") if "every_in_de_jure_hierarchy" in b]
        if len(branches) != 77:
            raise AssertionError(name + " must retain 76 palette branches and one fallback")
        if paint.count(increment) != 77 or paint.count("change_local_variable = { name = dynmap_r016_d_county_writes add = 1 }") != 77:
            raise AssertionError(name + " must contain only one counter pair per literal branch")
        for branch in branches:
            hierarchy_match = re.search(r"every_in_de_jure_hierarchy\s*=\s*\{", branch)
            if not hierarchy_match:
                raise AssertionError(name + " override must retain one attempted-write increment per branch")
            hierarchy, _ = balanced_body(branch, branch.find("{", hierarchy_match.start()))
            if hierarchy.count(increment) != 1:
                raise AssertionError(name + " override must retain one attempted-write increment per branch")
            county_increment = "change_local_variable = { name = dynmap_r016_d_county_writes add = 1 }"
            if hierarchy.count(county_increment) != 1:
                raise AssertionError(name + " override must count one county write per projected barony")
            guards = [b for k, _, b, _ in direct_blocks(hierarchy, "\t\t\t\t")
                      if k == "if" and "exists = scope:dynmap_r016_diagnostic_armed" in b]
            if len(guards) != 1 or guards[0].count(increment) != 1 or guards[0].count(county_increment) != 1:
                raise AssertionError(name + " override counters must both be inside one diagnostic guard")
            if branch.count(increment) != 1 or branch.count(county_increment) != 1:
                raise AssertionError(name + " override counters cannot appear outside its selected barony traversal")


def project(baronies_by_county, roles, prior_colors=None, *, valid=True, audit=False):
    """Synthetic single flat base followed by Primary/Secondary overrides."""
    colors = dict(prior_colors or {})
    writes = 0
    if not valid or audit:
        return colors, writes
    colors.update({barony: "neutral" for values in baronies_by_county.values() for barony in values})
    writes += sum(map(len, baronies_by_county.values()))
    for county, role in roles.items():
        if role in ("primary", "secondary"):
            for barony in baronies_by_county[county]:
                colors[barony] = role
                writes += 1
    return colors, writes


class ColdEntrySourceTests(unittest.TestCase):
    def test_each_valid_world_view_runs_one_neutral_base_before_rootdown(self):
        for view in ("realms", "holdings", "my_realm"):
            body = effect("dynmap_r016_world_" + view + "_effect")
            self.assertLess(body.index("dynmap_r016_paint_neutral_base_effect"), body.index("dynmap_r016_rootdown_start_" + view + "_effect"))
            self.assertIn("limit = { exists = dynasty }", body)

    def test_base_is_flat_and_audit_guarded(self):
        body = effect("dynmap_r016_paint_neutral_base_effect")
        self.assertIn("NOT = { exists = scope:dynmap_r016_audit_armed }", body)
        self.assertIn("every_barony = {", body)
        self.assertIn("set_title_color = { 65 70 80 }", body)
        self.assertNotIn("every_in_de_jure_hierarchy", body)

    def test_neutral_county_has_no_color_write_or_hierarchy_traversal(self):
        body = effect("dynmap_r016_paint_grey_effect")
        self.assertNotIn("set_title_color", body)
        self.assertNotIn("every_in_de_jure_hierarchy", body)
        self.assertIn("dynmap_r016_diagnostic_county_neutral_effect", body)

    def test_holdings_secondary_omits_only_proven_duplicate_holder_test(self):
        body = effect("dynmap_r016_holdings_county_effect")
        secondary = body.split("else_if =", 1)[1].split("dynmap_r016_paint_light_effect", 1)[0]
        self.assertEqual(secondary.count("dynasty = scope:dynmap_r016_player_dynasty"), 1)
        self.assertIn("any_liege_or_above", secondary)

    def test_realms_secondary_keeps_holder_dynasty_after_nonmatching_primary(self):
        body = effect("dynmap_r016_realms_county_effect")
        secondary = body.split("else_if =", 1)[1].split("dynmap_r016_paint_light_effect", 1)[0]
        self.assertIn("dynasty = scope:dynmap_r016_player_dynasty", secondary)

    def test_flat_base_resets_previous_view_exceptions_and_overrides_roles(self):
        counties = {"held": ["a", "b"], "unheld": ["c"]}
        old = {"a": "secondary", "b": "primary", "c": "primary"}
        colors, writes = project(counties, {"held": "primary", "unheld": "neutral"}, old)
        self.assertEqual(colors, {"a": "primary", "b": "primary", "c": "neutral"})
        self.assertEqual(writes, 3 + 2)

    def test_neutral_unheld_and_missing_holder_are_covered_by_base_without_override(self):
        counties = {"neutral": ["n1", "n2"], "unheld": ["u"]}
        colors, writes = project(counties, {"neutral": "neutral", "unheld": "neutral"})
        self.assertEqual(colors, {"n1": "neutral", "n2": "neutral", "u": "neutral"})
        self.assertEqual(writes, 3)

    def test_rejected_context_and_audit_do_not_reset_or_write(self):
        counties = {"x": ["barony"]}
        prior = {"barony": "primary"}
        self.assertEqual(project(counties, {"x": "neutral"}, prior, valid=False), (prior, 0))
        self.assertEqual(project(counties, {"x": "neutral"}, prior, audit=True), (prior, 0))

    def test_write_accounting_is_base_plus_exception_baronies(self):
        counties = {"primary": ["p1", "p2"], "secondary": ["s"], "neutral": ["n1", "n2"]}
        _, writes = project(counties, {"primary": "primary", "secondary": "secondary", "neutral": "neutral"})
        self.assertEqual(writes, 5 + 3)

    def test_production_source_links_base_and_overrides_to_attempted_write_counter(self):
        assert_diagnostic_write_accounting(SOURCE)

    def test_counter_omission_and_double_count_mutations_are_rejected(self):
        marker = "change_local_variable = { name = dynmap_r016_d_attempted_writes add = 1 }"
        base = effect("dynmap_r016_paint_neutral_base_effect")
        self.assertEqual(base.count(marker), 1)
        omitted = SOURCE.replace(marker, "", 1)
        with self.assertRaises(AssertionError):
            assert_diagnostic_write_accounting(omitted)
        doubled = SOURCE.replace(marker, marker + "\n\t\t\t" + marker, 1)
        with self.assertRaises(AssertionError):
            assert_diagnostic_write_accounting(doubled)

    def test_override_counter_guard_escape_mutation_is_rejected(self):
        county = "change_local_variable = { name = dynmap_r016_d_county_writes add = 1 }"
        attempted = "change_local_variable = { name = dynmap_r016_d_attempted_writes add = 1 }"
        guarded = (
            "if = {\n\t\t\t\t\tlimit = { exists = scope:dynmap_r016_diagnostic_armed }\n"
            f"\t\t\t\t\t{county}\n\t\t\t\t\t{attempted}\n\t\t\t\t}}"
        )
        escaped = SOURCE.replace(
            guarded,
            "if = { limit = { exists = scope:dynmap_r016_diagnostic_armed } }\n"
            f"\t\t\t\t{county}\n\t\t\t\t{attempted}", 1)
        self.assertNotEqual(escaped, SOURCE)
        with self.assertRaises(AssertionError):
            assert_diagnostic_write_accounting(escaped)


if __name__ == "__main__":
    unittest.main()
