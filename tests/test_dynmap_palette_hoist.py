"""Production-linked checks for county-scoped literal palette dispatch."""

import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "research/probes/my-dynasty-r016/mod/common/scripted_effects/dynmap_r016.txt"
SOURCE = SOURCE_PATH.read_text(encoding="utf-8-sig")
PALETTE = json.loads((ROOT / "data/dynmap-r016-palette.json").read_text())


def block_at(source, opening):
    """Return the balanced brace block beginning at opening, ignoring quoted braces."""
    if opening < 0 or source[opening] != "{":
        raise AssertionError("expected opening brace")
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


def effect(name, source=SOURCE):
    match = re.search(r"(?m)^" + re.escape(name) + r"\s*=\s*\{", source)
    if not match:
        raise AssertionError("missing effect: " + name)
    return block_at(source, source.find("{", match.start()))[0]


def top_level_effect_occurrences(source):
    """Return ordered (name, exact body) pairs, preserving duplicate definitions."""
    declaration = re.compile(r"(?m)^([A-Za-z0-9_]+)\s*=\s*\{")
    occurrences = []
    depth = 0
    quoted = escaped = comment = False
    line_start = 0
    index = 0
    while index < len(source):
        char = source[index]
        if char == "\n":
            comment = False
            line_start = index + 1
            index += 1
            continue
        if comment:
            index += 1
            continue
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            index += 1
            continue
        if char == "#":
            comment = True
            index += 1
            continue
        if char == '"':
            quoted = True
            index += 1
            continue
        if depth == 0 and index == line_start:
            match = declaration.match(source, index)
            if match:
                name = match.group(1)
                opening = source.find("{", match.start(), match.end())
                start = opening + 1
                depth = 1
                cursor = start
                inner_quoted = inner_escaped = inner_comment = False
                while cursor < len(source) and depth:
                    current = source[cursor]
                    if current == "\n":
                        inner_comment = False
                    elif inner_comment:
                        pass
                    elif inner_quoted:
                        if inner_escaped:
                            inner_escaped = False
                        elif current == "\\":
                            inner_escaped = True
                        elif current == '"':
                            inner_quoted = False
                    elif current == "#":
                        inner_comment = True
                    elif current == '"':
                        inner_quoted = True
                    elif current == "{":
                        depth += 1
                    elif current == "}":
                        depth -= 1
                    cursor += 1
                if depth:
                    raise AssertionError("unclosed top-level effect: " + name)
                occurrences.append((name, source[start:cursor - 1]))
                index = cursor
                line_start = source.rfind("\n", 0, index) + 1
                depth = 0
                continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
        index += 1
    return occurrences


def assert_duplicate_realms_occurrences(source):
    occurrences = [body for name, body in top_level_effect_occurrences(source)
                   if name == "dynmap_r016_realms_county_effect"]
    if len(occurrences) != 2 or occurrences[0] != occurrences[1]:
        raise AssertionError("both identical top-level realms classifier occurrences must remain")
    return True


def replace_effect_body(source, name, transform):
    match = re.search(r"(?m)^" + re.escape(name) + r"\s*=\s*\{", source)
    if not match:
        raise AssertionError("missing effect: " + name)
    opening = source.find("{", match.start())
    body, end = block_at(source, opening)
    return source[:opening + 1] + transform(body) + source[end - 1:]


def replace_fallback_body(source, name, transform):
    def update(body):
        fallback = next((item for item in _blocks_at_indent(body, depth=1)
                         if item[0] == "else" and "every_in_de_jure_hierarchy" in item[2]), None)
        if fallback is None:
            raise AssertionError("missing fallback branch")
        _, start, _, end = fallback
        opening = body.find("{", start)
        fallback_body, _ = block_at(body, opening)
        return body[:opening + 1] + transform(fallback_body) + body[end - 1:]
    return replace_effect_body(source, name, update)


def _blocks_at_indent(text, indent="\t\t", depth=0):
    """Yield (kind, match start, body, end) at an exact indentation and brace depth."""
    pattern = re.compile(r"(?m)^" + re.escape(indent) + r"(if|else_if|else)\s*=\s*\{")
    result = []
    brace_depth = 0
    quoted = escaped = False
    line_depth = {}
    for pos, char in enumerate(text):
        if pos == 0 or text[pos - 1] == "\n":
            line_depth[pos] = brace_depth
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
        elif char == "{":
            brace_depth += 1
        elif char == "}":
            brace_depth -= 1
    for match in pattern.finditer(text):
        if line_depth.get(match.start(), -1) != depth:
            continue
        body, end = block_at(text, text.find("{", match.start()))
        result.append((match.group(1), match.start(), body, end))
    return result


def dispatch_branches(name, source=SOURCE):
    body = effect(name, source)
    branches = []
    for kind, start, contents, end in _blocks_at_indent(body, depth=1):
        condition = re.search(r"scope:dynmap_r016_palette_id\s*=\s*(\d+)", contents)
        if condition:
            branches.append((kind, int(condition.group(1)), contents, start, end))
    fallback = next((item for item in _blocks_at_indent(body, depth=1) if item[0] == "else" and "every_in_de_jure_hierarchy" in item[2]), None)
    if fallback:
        branches.append(("else", None, fallback[2], fallback[1], fallback[3]))
    return body, branches


def _hierarchy(branch):
    match = re.search(r"every_in_de_jure_hierarchy\s*=\s*\{", branch)
    if not match:
        raise AssertionError("palette branch must traverse the county hierarchy")
    return block_at(branch, branch.find("{", match.start()))[0]


def _guarded_increments(hierarchy, expected_count=1):
    county = "change_local_variable = { name = dynmap_r016_d_county_writes add = 1 }"
    attempted = "change_local_variable = { name = dynmap_r016_d_attempted_writes add = 1 }"
    if hierarchy.count(county) != expected_count or hierarchy.count(attempted) != expected_count:
        raise AssertionError("each barony write needs exactly one county and attempted counter increment")
    guards = []
    for kind, _, body, _ in _blocks_at_indent(hierarchy, "\t\t\t\t"):
        if "exists = scope:dynmap_r016_diagnostic_armed" in body:
            guards.append(body)
    if len(guards) != expected_count:
        raise AssertionError("each counter pair must be enclosed by one diagnostic guard")
    if sum(body.count(county) for body in guards) != expected_count or sum(body.count(attempted) for body in guards) != expected_count:
        raise AssertionError("counter increments escaped their diagnostic guard")


def assert_audit_never_writes(source):
    for name in ("dynmap_r016_audit_palette_primary_effect", "dynmap_r016_audit_palette_secondary_effect"):
        if "set_title_color" in effect(name, source):
            raise AssertionError(name + " must remain write-free")
    for name in ("dynmap_r016_paint_dark_effect", "dynmap_r016_paint_light_effect"):
        body, _ = dispatch_branches(name, source)
        audit_if = next((b for k, _, b, _ in _blocks_at_indent(body, "\t") if k == "if" and "dynmap_r016_audit_armed" in b), None)
        if audit_if is None or "set_title_color" in audit_if or "every_in_de_jure_hierarchy" in audit_if:
            raise AssertionError(name + " audit path must log only and never traverse or write")


def assert_source_invariants(source):
    rows = PALETTE["rows"]
    expected_ids = [row["pair_id"] for row in rows]
    role_info = (
        ("dynmap_r016_paint_dark_effect", "dark", "primary", [25, 105, 50]),
        ("dynmap_r016_paint_light_effect", "light", "secondary", [145, 220, 150]),
    )
    for name, data_key, role, fallback_rgb in role_info:
        body, branches = dispatch_branches(name, source)
        if len(branches) != len(rows) + 1:
            raise AssertionError(name + " must have all 76 literal branches and one fallback")
        if [pid for kind, pid, _, _, _ in branches if pid is not None] != expected_ids:
            raise AssertionError(name + " palette IDs or order differ from frozen data")

        audit_blocks = [b for k, _, b, _ in _blocks_at_indent(body, "\t") if k == "if" and "dynmap_r016_audit_armed" in b]
        if len(audit_blocks) != 1 or f"dynmap_r016_audit_palette_{role}_effect = yes" not in audit_blocks[0]:
            raise AssertionError(name + " audit role dispatch changed")
        if "set_title_color" in audit_blocks[0] or "every_in_de_jure_hierarchy" in audit_blocks[0]:
            raise AssertionError(name + " audit path may not paint")

        reset = re.search(r"(?m)^\t\tif\s*=\s*\{\s*limit\s*=\s*\{\s*exists\s*=\s*scope:dynmap_r016_diagnostic_armed\s*\}\s*set_local_variable\s*=\s*\{\s*name\s*=\s*dynmap_r016_d_county_writes\s+value\s*=\s*0\s*\}\s*\}", body)
        first_branch = min(start for _, _, _, start, _ in branches)
        if reset is None or reset.start() > first_branch or body.count("name = dynmap_r016_d_county_writes value = 0") != 1:
            raise AssertionError(name + " must reset county writes once before palette dispatch")

        for index, (kind, pid, _, _, _) in enumerate(branches[:-1]):
            row = rows[index]
            if pid != row["pair_id"] or kind != ("if" if index == 0 else "else_if"):
                raise AssertionError(name + " palette branch ID or ordering changed")

        fallback_kind, _, fallback_branch, _, fallback_end = branches[-1]
        if fallback_kind != "else":
            raise AssertionError(name + " final palette branch must be the fallback else")

        # Apply the same projection invariants to every numbered branch and fallback.
        all_branches = branches
        for index, (kind, pid, branch, _, _) in enumerate(all_branches):
            if index == len(rows):
                rgb = fallback_rgb
            else:
                rgb = rows[index][data_key]
            expected_literal = "set_title_color = { " + " ".join(map(str, rgb)) + " }"
            if branch.count("set_title_color = {") != 1 or expected_literal not in branch:
                raise AssertionError(name + " branch writer must be one correctly associated literal")
            hierarchy = _hierarchy(branch)
            if hierarchy.count("every_in_de_jure_hierarchy"):
                raise AssertionError("nested hierarchy traversal")
            if "continue = { always = yes }" not in hierarchy or "limit = { tier = tier_barony }" not in hierarchy:
                raise AssertionError(name + " hierarchy scope filters changed, including fallback")
            if "dynmap_r016_palette_id" in hierarchy:
                raise AssertionError("palette dispatch moved into the barony traversal, including fallback")
            if hierarchy.count("set_title_color = {") != 1:
                raise AssertionError("each selected traversal, including fallback, must write once per barony")
            _guarded_increments(hierarchy)
            for counter in ("dynmap_r016_d_county_writes", "dynmap_r016_d_attempted_writes"):
                marker = f"change_local_variable = {{ name = {counter} add = 1 }}"
                if branch.count(marker) != 1 or hierarchy.count(marker) != 1:
                    raise AssertionError(name + " fallback/branch counter is missing, duplicated or outside traversal")

        callback = f"dynmap_r016_diagnostic_county_{role}_effect = yes"
        if body.count("change_local_variable = { name = dynmap_r016_d_county_writes add = 1 }") != len(rows) + 1:
            raise AssertionError(name + " contains an extra or missing county counter increment")
        if body.count("change_local_variable = { name = dynmap_r016_d_attempted_writes add = 1 }") != len(rows) + 1:
            raise AssertionError(name + " contains an extra or missing attempted counter increment")
        callbacks = [(kind, start, block, end) for kind, start, block, end in _blocks_at_indent(body, depth=1)
                     if callback in block]
        if len(callbacks) != 1:
            raise AssertionError(name + " role diagnostic callback must be one direct sibling")
        callback_kind, callback_start, callback_block, callback_end = callbacks[0]
        if callback_kind != "if" or callback_start <= fallback_end:
            raise AssertionError(name + " callback must be a sibling after the complete fallback chain")
        if "limit = { exists = scope:dynmap_r016_diagnostic_armed }" not in callback_block:
            raise AssertionError(name + " role callback must remain diagnostic-guarded")
        if "every_in_de_jure_hierarchy" in callback_block or "set_title_color" in callback_block:
            raise AssertionError(name + " role callback sibling cannot traverse or write")
        if "dynmap_r016_paint_mixed_primary_effect = yes" in body or "dynmap_r016_paint_mixed_secondary_effect = yes" in body:
            raise AssertionError("old per-barony palette dispatch remains in production path")

    if re.search(r"(?m)^\s*dynmap_r016_paint_mixed_(?:primary|secondary)_effect\s*=\s*yes", source):
        raise AssertionError("production call site still invokes a per-barony palette writer")
    assert_audit_never_writes(source)
    return True


def _literal_map(name, data_key, source):
    _, branches = dispatch_branches(name, source)
    result = {}
    for _, pid, branch, _, _ in branches:
        if pid is not None:
            match = re.search(r"set_title_color\s*=\s*\{\s*(\d+)\s+(\d+)\s+(\d+)\s*\}", branch)
            result[pid] = tuple(map(int, match.groups()))
    fallback = next(branch for kind, _, branch, _, _ in branches if kind == "else")
    match = re.search(r"set_title_color\s*=\s*\{\s*(\d+)\s+(\d+)\s+(\d+)\s*\}", fallback)
    result[None] = tuple(map(int, match.groups()))
    return result


def project_from_source(source, counties, roles, prior_colors=None, *, valid=True, audit=False, diagnostic=True):
    """Small bounded model tied to validated production roles, literals and counter guards."""
    assert_source_invariants(source)
    colors = dict(prior_colors or {})
    attempted = county_writes = 0
    callbacks = []
    if not valid or audit:
        return colors, {"attempted": 0, "county_writes": 0, "callbacks": []}
    colors.update({barony: "neutral" for baronies in counties.values() for barony in baronies})
    if diagnostic:
        attempted += sum(map(len, counties.values()))
    maps = {
        "primary": (_literal_map("dynmap_r016_paint_dark_effect", "dark", source), (25, 105, 50)),
        "secondary": (_literal_map("dynmap_r016_paint_light_effect", "light", source), (145, 220, 150)),
    }
    for county, (role, palette_id) in roles.items():
        if role not in maps:
            continue
        county_writes = 0  # production reset: one reset per exceptional county invocation
        literals, fallback = maps[role]
        rgb = literals.get(palette_id, fallback)
        for barony in counties[county]:
            colors[barony] = rgb
            if diagnostic:
                county_writes += 1
                attempted += 1
        callbacks.append((county, role, county_writes))
    return colors, {"attempted": attempted, "county_writes": county_writes, "callbacks": callbacks}


class PaletteHoistTests(unittest.TestCase):
    def test_occurrence_guard_rejects_either_duplicate_deletion_and_ignores_nested_else(self):
        self.assertTrue(assert_duplicate_realms_occurrences(SOURCE))
        positions = [match.start() for match in re.finditer(
            r"(?m)^dynmap_r016_realms_county_effect\s*=\s*\{", SOURCE)]
        self.assertEqual(len(positions), 2)
        for position in positions:
            prefix = SOURCE[:position]
            opening = SOURCE.find("{", position)
            _, end = block_at(SOURCE, opening)
            candidate = prefix + SOURCE[end:]
            with self.assertRaises(AssertionError):
                assert_duplicate_realms_occurrences(candidate)
        nested = SOURCE.replace(
            "dynmap_r016_operation_cleanup_effect = yes",
            "dynmap_r016_operation_cleanup_effect = yes\n"
            "if = {\nelse = {\ndynmap_r016_realms_county_effect = { fake = yes }\n}\n}", 1)
        self.assertTrue(assert_duplicate_realms_occurrences(nested))

    def test_all_ordered_palette_literals_and_fallbacks_match_public_data(self):
        self.assertTrue(assert_source_invariants(SOURCE))

    def test_county_dispatch_structure_and_audit_are_enforced(self):
        self.assertTrue(assert_source_invariants(SOURCE))

    def test_production_validator_rejects_rgb_role_condition_and_dispatch_mutations(self):
        mutations = (
            SOURCE.replace("set_title_color = { 137 76 67 }", "set_title_color = { 137 76 68 }", 1),
            SOURCE.replace("limit = { scope:dynmap_r016_palette_id = 1 }", "limit = { scope:dynmap_r016_palette_id = 2 }", 1),
            SOURCE.replace("dynmap_r016_diagnostic_county_primary_effect = yes", "dynmap_r016_diagnostic_county_secondary_effect = yes", 1),
            SOURCE.replace("limit = { tier = tier_barony }", "limit = { tier = tier_barony scope:dynmap_r016_palette_id = 1 }", 1),
            SOURCE.replace('debug_log = "DYNMAP_R016 AUDIT V4 RESULT PRIMARY RGB 137 76 67 WRITES_SUPPRESSED"', "set_title_color = { 137 76 67 }", 1),
        )
        for candidate in mutations:
            self.assertNotEqual(candidate, SOURCE)
            with self.assertRaises(AssertionError):
                assert_source_invariants(candidate)

    def test_production_validator_rejects_missing_duplicate_and_guard_escape(self):
        attempted = "change_local_variable = { name = dynmap_r016_d_attempted_writes add = 1 }"
        county = "change_local_variable = { name = dynmap_r016_d_county_writes add = 1 }"
        guard = "if = {\n\t\t\t\t\tlimit = { exists = scope:dynmap_r016_diagnostic_armed }\n\t\t\t\t\t" + county + "\n\t\t\t\t\t" + attempted + "\n\t\t\t\t}"
        missing = SOURCE.replace(attempted, "", 1)
        duplicate = SOURCE.replace(attempted, attempted + "\n\t\t\t\t\t" + attempted, 1)
        escaped = SOURCE.replace(guard, "if = { limit = { exists = scope:dynmap_r016_diagnostic_armed } }\n\t\t\t\t\t" + county + "\n\t\t\t\t\t" + attempted, 1)
        for candidate in (missing, duplicate, escaped):
            self.assertNotEqual(candidate, SOURCE)
            with self.assertRaises(AssertionError):
                assert_source_invariants(candidate)

    def test_source_linked_projection_covers_multi_empty_roles_and_lifecycle(self):
        counties = {"primary": ["a", "b", "c"], "secondary": ["d"], "neutral": ["e"], "empty": []}
        roles = {"primary": ("primary", 1), "secondary": ("secondary", 2), "neutral": ("neutral", 1), "empty": ("primary", 88)}
        prior = {name: "old" for baronies in counties.values() for name in baronies}
        colors, counts = project_from_source(SOURCE, counties, roles, prior)
        base_writes = sum(map(len, counties.values()))
        override_writes = len(counties["primary"]) + len(counties["secondary"])
        self.assertEqual(counts["attempted"], base_writes + override_writes)
        self.assertEqual(counts["callbacks"], [("primary", "primary", 3), ("secondary", "secondary", 1), ("empty", "primary", 0)])
        self.assertEqual(colors["a"], (137, 76, 67))
        self.assertEqual(colors["d"], (176, 128, 108))
        self.assertEqual(colors["e"], "neutral")
        self.assertEqual(colors["old"] if "old" in colors else "absent", "absent")

        colors_off, counts_off = project_from_source(SOURCE, counties, roles, prior, diagnostic=False)
        self.assertEqual(counts_off, {"attempted": 0, "county_writes": 0, "callbacks": [("primary", "primary", 0), ("secondary", "secondary", 0), ("empty", "primary", 0)]})
        self.assertEqual(colors_off, colors)
        for kwargs in ({"audit": True}, {"valid": False}):
            unchanged, suppressed = project_from_source(SOURCE, counties, roles, prior, **kwargs)
            self.assertEqual(unchanged, prior)
            self.assertEqual(suppressed, {"attempted": 0, "county_writes": 0, "callbacks": []})

    def test_validator_rejects_reset_or_callback_moved_out_of_order(self):
        reset = "if = { limit = { exists = scope:dynmap_r016_diagnostic_armed } set_local_variable = { name = dynmap_r016_d_county_writes value = 0 } }"
        dark = effect("dynmap_r016_paint_dark_effect")
        # Move the exact reset block to after the dispatch chain but before callback.
        moved = SOURCE.replace(reset, "", 1)
        marker = "dynmap_r016_diagnostic_county_primary_effect = yes"
        moved = moved.replace(marker, reset + "\n\t\t" + marker, 1)
        with self.assertRaises(AssertionError):
            assert_source_invariants(moved)
        before = SOURCE.replace(marker, "", 1)
        first = "\t\tif = {\n\t\t\tlimit = { scope:dynmap_r016_palette_id = 1 }"
        before = before.replace(first, marker + "\n" + first, 1)
        with self.assertRaises(AssertionError):
            assert_source_invariants(before)

    def test_fallback_and_callback_mutations_are_rejected_by_validator_and_projection(self):
        dark_name = "dynmap_r016_paint_dark_effect"

        def move_callback(branch_body):
            callbacks = [(start, end) for kind, start, _, end in _blocks_at_indent(branch_body, depth=1)
                         if "dynmap_r016_diagnostic_county_primary_effect = yes" in branch_body[start:end]]
            self.assertEqual(len(callbacks), 1)
            cb_start, cb_end = callbacks[0]
            statement = branch_body[cb_start:cb_end]
            without = branch_body[:cb_start] + branch_body[cb_end:]
            fallback = next(item for item in _blocks_at_indent(without, depth=1)
                            if item[0] == "else" and "every_in_de_jure_hierarchy" in item[2])
            insert_at = fallback[3] - 1
            return without[:insert_at] + "\n" + statement + without[insert_at:]

        callback_in_fallback = replace_effect_body(SOURCE, dark_name, move_callback)
        fallback_filter_removed = replace_fallback_body(
            SOURCE, dark_name,
            lambda b: b.replace("limit = { tier = tier_barony }", "limit = { always = yes }", 1))
        fallback_write_outside_loop = replace_fallback_body(
            SOURCE, dark_name,
            lambda b: b.replace(
                "\t\t\t\tset_title_color = { 25 105 50 }\n", "", 1
            ).replace(
                "every_in_de_jure_hierarchy = {",
                "set_title_color = { 25 105 50 }\nevery_in_de_jure_hierarchy = {", 1
            ))
        fallback_dispatch_inside_loop = replace_fallback_body(
            SOURCE, dark_name,
            lambda b: b.replace(
                "limit = { tier = tier_barony }",
                "limit = { tier = tier_barony scope:dynmap_r016_palette_id = 1 }", 1
            ))

        for candidate in (callback_in_fallback, fallback_filter_removed,
                          fallback_write_outside_loop, fallback_dispatch_inside_loop):
            self.assertNotEqual(candidate, SOURCE)
            with self.assertRaises(AssertionError):
                assert_source_invariants(candidate)
            with self.assertRaises(AssertionError):
                project_from_source(candidate, {"x": ["a"]}, {"x": ("primary", 1)})


if __name__ == "__main__":
    unittest.main()
