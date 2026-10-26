"""Bounded source-aware checker for the fixed-state root-down effects.

This is not a CK3 interpreter. It parses only the frozen helper shape, binds
literal branch conditions to called variant names, and compares those branches
with an independent F-003 parent/child oracle.
"""
from pathlib import Path
import itertools
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "research/probes/my-dynasty-r016/mod/common/scripted_effects/dynmap_r016.txt"
SOURCE = SOURCE_PATH.read_text(encoding="utf-8-sig")
VIEWS = ("realms", "holdings", "my_realm")


def _block(text, start):
    """Return (opening brace, end-exclusive) for a bounded balanced block."""
    opening = text.find("{", start)
    if opening < 0:
        raise AssertionError("missing opening brace")
    depth = 0
    quoted = escaped = False
    for pos in range(opening, len(text)):
        char = text[pos]
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
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return opening, pos + 1
    raise AssertionError("unclosed source block")


def _effect(source, name):
    match = re.search(r"(?m)^" + re.escape(name) + r"\s*=\s*\{", source)
    if not match:
        raise AssertionError("missing production effect: " + name)
    opening, end = _block(source, match.start())
    return source[opening + 1:end - 1]


def _iter_block(body, token, start=0):
    pos = body.find(token, start)
    if pos < 0:
        raise AssertionError("missing " + token)
    opening, end = _block(body, pos)
    return body[opening + 1:end - 1], pos, end


def _own_match():
    return "trigger_if = { limit = { exists = dynasty } dynasty = scope:dynmap_r016_player_dynasty } trigger_else = { always = no }"


def _own_miss():
    return "OR = { NOT = { exists = dynasty } AND = { exists = dynasty NOT = { dynasty = scope:dynmap_r016_player_dynasty } } }"


def _paint(role):
    return {"primary": "dynmap_r016_paint_dark_effect = yes",
            "secondary": "dynmap_r016_paint_light_effect = yes",
            "neutral": "dynmap_r016_paint_grey_effect = yes"}[role]


def _role(view, root_d, ancestor_d, inside, own_d):
    if view == "realms":
        return "primary" if root_d else ("secondary" if ancestor_d or own_d else "neutral")
    if view == "holdings":
        return "primary" if own_d else ("secondary" if ancestor_d else "neutral")
    return "primary" if inside else ("secondary" if ancestor_d or own_d else "neutral")


def _child_dispatch(view, root_d, child_ancestor, inside):
    lines = []
    choices = ((1, 1, "if"), (1, 0, "else_if"), (0, 1, "else_if"), (0, 0, "else"))
    for own_d, is_player, keyword in choices:
        child_inside = int(bool(inside or is_player))
        target = f"dynmap_r016_rootdown_{view}_r{root_d}a{child_ancestor}i{child_inside}_effect = yes"
        if keyword == "else":
            lines.append(f"else = {{ {target} }}")
        else:
            identity = "this = scope:dynmap_r016_player_root" if is_player else "NOT = { this = scope:dynmap_r016_player_root }"
            dynasty = _own_match() if own_d else _own_miss()
            lines.append(f"{keyword} = {{ limit = {{ AND = {{ {dynasty} {identity} }} }} {target} }}")
    return lines


def _check_source(source):
    # Bind every role action to the node's own Dynasty branch and fixed F-003 tuple.
    for view, root_d, ancestor_d, inside in ((v, r, a, i) for v in VIEWS for r, a, i in itertools.product((0, 1), repeat=3)):
        name = f"dynmap_r016_rootdown_{view}_r{root_d}a{ancestor_d}i{inside}_effect"
        body = _effect(source, name)
        match_prefix = f"if = {{ limit = {{ {_own_match()} }}"
        miss_prefix = f"if = {{ limit = {{ {_own_miss()} }}"
        yes_block_start = body.find(match_prefix)
        no_block_start = body.find(miss_prefix)
        if yes_block_start < 0 or no_block_start < 0:
            raise AssertionError(name + " must guard both own-Dynasty branches")
        yes_open, yes_end = _block(body, yes_block_start)
        no_open, no_end = _block(body, no_block_start)
        yes_body = body[yes_open + 1:yes_end - 1]
        no_body = body[no_open + 1:no_end - 1]
        for branch_body, own_d in ((yes_body, 1), (no_body, 0)):
            if branch_body.count("every_held_title = {") != 1 or "tier = tier_county" not in branch_body:
                raise AssertionError(name + " must visit each matching held-county branch once")
            paints = [p for p in ("dynmap_r016_paint_dark_effect = yes", "dynmap_r016_paint_light_effect = yes", "dynmap_r016_paint_grey_effect = yes") if p in branch_body]
            expected = _paint(_role(view, root_d, ancestor_d, inside, own_d))
            if paints != [expected]:
                raise AssertionError(name + " own_D=" + str(own_d) + " paints " + repr(paints) + "; expected " + expected)

        # Parent own_D is tested OUTSIDE every_vassal, then becomes the child's
        # strict-ancestor input. Child Dynasty/player identity remain child tests.
        held_positions = [m.end() for m in re.finditer(r"every_held_title\s*=\s*\{", body)]
        if len(held_positions) != 2:
            raise AssertionError(name + " must have two exclusive held-title branches")
        start = held_positions[-1]
        parent_match_at = body.find(match_prefix, start)
        if parent_match_at < 0:
            raise AssertionError(name + " missing parent own_D transition")
        pm_open, pm_end = _block(body, parent_match_at)
        yes_vassals, _, _ = _iter_block(body[pm_open + 1:pm_end - 1], "every_vassal = {")
        child_a_yes = 1  # parent inclusive_D = strict ancestor OR parent's own_D
        if [line.strip() for line in yes_vassals.splitlines() if "rootdown_" in line] != _child_dispatch(view, root_d, child_a_yes, inside):
            raise AssertionError(name + " parent-own-D branch has wrong child conditions or targets")
        else_at = body.find("else = {", pm_end)
        if else_at < 0:
            raise AssertionError(name + " missing parent own_D false branch")
        en_open, en_end = _block(body, else_at)
        no_vassals, _, _ = _iter_block(body[en_open + 1:en_end - 1], "every_vassal = {")
        if [line.strip() for line in no_vassals.splitlines() if "rootdown_" in line] != _child_dispatch(view, root_d, ancestor_d, inside):
            raise AssertionError(name + " parent-no-D branch has wrong child conditions or targets")
        if "any_liege_or_above" in body or "top_liege" in body or "local_variable" in body or "variable_list" in body:
            raise AssertionError(name + " contains a forbidden senior walk or mutable state")

    # Root seeding includes the root itself and starts strict-ancestor false.
    for view in VIEWS:
        start_body = _effect(source, "dynmap_r016_rootdown_start_" + view + "_effect")
        root_body, _, _ = _iter_block(start_body, "every_independent_ruler = {")
        expected = []
        for root_d, is_player, keyword in ((1, 1, "if"), (1, 0, "else_if"), (0, 1, "else_if"), (0, 0, "else")):
            target = f"dynmap_r016_rootdown_{view}_r{root_d}a0i{int(bool(is_player))}_effect = yes"
            if keyword == "else":
                expected.append(f"else = {{ {target} }}")
            else:
                identity = "this = scope:dynmap_r016_player_root" if is_player else "NOT = { this = scope:dynmap_r016_player_root }"
                dynasty = _own_match() if root_d else _own_miss()
                expected.append(f"{keyword} = {{ limit = {{ AND = {{ {dynasty} {identity} }} }} {target} }}")
        actual = [line.strip() for line in root_body.splitlines() if "rootdown_" in line]
        if actual != expected:
            raise AssertionError(view + " root seed conditions/targets differ")
        if "every_county = { if = { limit = { NOT = { exists = holder } } dynmap_r016_paint_grey_effect = yes } }" not in start_body:
            raise AssertionError(view + " no-holder neutral accounting path missing")

        world = _effect(source, "dynmap_r016_world_" + view + "_effect")
        if not ("limit = { exists = dynasty }" in world and "dynmap_r016_paint_neutral_base_effect = yes" in world and f"dynmap_r016_rootdown_start_{view}_effect = yes" in world):
            raise AssertionError(view + " world guard/base/root entry missing")
        if any(f"dynmap_r016_{view}_county_effect = yes" in world for view in VIEWS):
            raise AssertionError(view + " world path invokes the old county classifier")
        if world.index("dynmap_r016_paint_neutral_base_effect") > world.index(f"dynmap_r016_rootdown_start_{view}_effect"):
            raise AssertionError(view + " base must precede traversal")

        for mode in ("summary", "samples"):
            wrapper = _effect(source, f"dynmap_r016_{mode}_{view}_effect")
            if f"dynmap_r016_world_{view}_effect = yes" not in wrapper:
                raise AssertionError(f"{mode}/{view} does not consume root-down production totals")
        audit = _effect(source, f"dynmap_r016_audit_{view}_selected_effect")
        if f"dynmap_r016_world_{view}_effect = yes" not in audit or "else = { debug_log = \"DYNMAP_R016 AUDIT V4 REJECT" not in audit:
            raise AssertionError("selected audit path or reject framing changed for " + view)

    # Base and projected writers preserve audit suppression; neutral held and
    # unheld diagnostic counters stay on the existing neutral paint helper.
    base = _effect(source, "dynmap_r016_paint_neutral_base_effect")
    if "NOT = { exists = scope:dynmap_r016_audit_armed }" not in base or base.count("set_title_color = { 65 70 80 }") != 1:
        raise AssertionError("neutral base audit/write invariant failed")
    for name in ("dynmap_r016_paint_dark_effect", "dynmap_r016_paint_light_effect"):
        if "exists = scope:dynmap_r016_audit_armed" not in _effect(source, name):
            raise AssertionError(name + " missing audit write suppression")
    grey = _effect(source, "dynmap_r016_paint_grey_effect")
    if "dynmap_r016_diagnostic_county_neutral_effect = yes" not in grey or "set_title_color" in grey:
        raise AssertionError("neutral diagnostics/write path changed")
    return True


def _production_model(nodes, player, dynasty):
    """Model the encoded tuple; the source checker above binds each transition."""
    result = {}
    roots = [n for n in nodes if n["parent"] is None]
    by_parent = {}
    by_id = {n["id"]: n for n in nodes}
    for n in nodes:
        by_parent.setdefault(n["parent"], []).append(n)

    def visit(node, root_d, ancestor_d, inherited_inside):
        own_d = node["dynasty"] is not None and node["dynasty"] == dynasty
        inside = inherited_inside or node["id"] == player
        inclusive = ancestor_d or own_d
        for idx in range(node["counties"]):
            result[f"{node['id']}:{idx}"] = {
                view: _role(view, root_d, ancestor_d, inside, own_d) for view in VIEWS
            }
        for child in by_parent.get(node["id"], []):
            visit(child, root_d, inclusive, inside)

    for root in roots:
        visit(root, root["dynasty"] is not None and root["dynasty"] == dynasty, False, False)
    for n in nodes:
        if n["unheld"]:
            for idx in range(n["unheld"]):
                result[f"{n['id']}:unheld:{idx}"] = {v: "neutral" for v in VIEWS}
    return result


def _f003_oracle(nodes, player, dynasty):
    by_parent = {}
    for n in nodes:
        by_parent.setdefault(n["parent"], []).append(n)
    out = {}

    def walk(node, ancestors, root):
        own = node["dynasty"] is not None and node["dynasty"] == dynasty
        chain = ancestors + [node]
        root_d = root["dynasty"] is not None and root["dynasty"] == dynasty
        strict_d = any(x["dynasty"] is not None and x["dynasty"] == dynasty for x in ancestors)
        inclusive_d = strict_d or own
        inside = any(x["id"] == player for x in chain)
        for idx in range(node["counties"]):
            out[f"{node['id']}:{idx}"] = {
                "realms": "primary" if root_d else ("secondary" if inclusive_d else "neutral"),
                "holdings": "primary" if own else ("secondary" if strict_d else "neutral"),
                "my_realm": "primary" if inside else ("secondary" if inclusive_d else "neutral"),
            }
        for child in by_parent.get(node["id"], []):
            walk(child, chain, root)

    for root in by_parent.get(None, []):
        walk(root, [], root)
    for n in nodes:
        for idx in range(n["unheld"]):
            out[f"{n['id']}:unheld:{idx}"] = {v: "neutral" for v in VIEWS}
    return out


def _fixtures():
    # Chain with multiple counties and a missing-Dynasty holder; star/shared
    # foreign senior; independent singleton; player-vassal sibling isolation.
    return [
        ([{"id":"r","parent":None,"dynasty":7,"counties":2,"unheld":1},
          {"id":"m","parent":"r","dynasty":None,"counties":1,"unheld":0},
          {"id":"h","parent":"m","dynasty":9,"counties":2,"unheld":0}], "h", 7),
        ([{"id":"r","parent":None,"dynasty":3,"counties":1,"unheld":0},
          {"id":"d","parent":"r","dynasty":7,"counties":1,"unheld":0},
          {"id":"f","parent":"r","dynasty":4,"counties":1,"unheld":0},
          {"id":"cadet","parent":"f","dynasty":7,"counties":1,"unheld":0}], "d", 7),
        ([{"id":"solo","parent":None,"dynasty":None,"counties":1,"unheld":2}], "solo", 7),
        ([{"id":"r","parent":None,"dynasty":4,"counties":1,"unheld":0},
          {"id":"p","parent":"r","dynasty":7,"counties":1,"unheld":0},
          {"id":"sib","parent":"r","dynasty":7,"counties":1,"unheld":0},
          {"id":"child","parent":"p","dynasty":None,"counties":1,"unheld":0}], "p", 7),
    ]


class RootDownTests(unittest.TestCase):
    def test_condition_aware_source_checker_accepts_production_graph(self):
        self.assertTrue(_check_source(SOURCE))

    def test_source_bound_model_matches_independent_f003_tree_oracle(self):
        _check_source(SOURCE)
        for nodes, player, dynasty in _fixtures():
            self.assertEqual(_production_model(nodes, player, dynasty), _f003_oracle(nodes, player, dynasty))
        # Fresh player/Dynasty inputs cannot inherit a prior traversal tuple.
        nodes, _, _ = _fixtures()[1]
        self.assertEqual(_production_model(nodes, "f", 3), _f003_oracle(nodes, "f", 3))

    def test_role_swap_mutation_is_rejected(self):
        name = "dynmap_r016_rootdown_holdings_r0a0i0_effect"
        block = _effect(SOURCE, name)
        old = "dynmap_r016_paint_grey_effect = yes"
        self.assertIn(old, block)
        mutated = SOURCE.replace(block, block.replace(old, "dynmap_r016_paint_dark_effect = yes", 1), 1)
        with self.assertRaises(AssertionError):
            _check_source(mutated)

    def test_parent_ancestor_and_sibling_mutations_are_rejected(self):
        name = "dynmap_r016_rootdown_holdings_r0a0i0_effect"
        block = _effect(SOURCE, name)
        expected = "dynmap_r016_rootdown_holdings_r0a1i0_effect = yes"
        self.assertIn(expected, block)
        wrong_ancestor = block.replace(expected, "dynmap_r016_rootdown_holdings_r0a0i0_effect = yes", 1)
        with self.assertRaises(AssertionError):
            _check_source(SOURCE.replace(block, wrong_ancestor, 1))
        wrong_sibling = block.replace("dynmap_r016_rootdown_holdings_r0a1i1_effect = yes", "dynmap_r016_rootdown_holdings_r0a1i0_effect = yes", 1)
        with self.assertRaises(AssertionError):
            _check_source(SOURCE.replace(block, wrong_sibling, 1))

    def test_skipped_root_duplicate_county_and_unheld_counter_mutations_are_rejected(self):
        start_name = "dynmap_r016_rootdown_start_realms_effect"
        start = _effect(SOURCE, start_name)
        skipped = start.replace("dynmap_r016_rootdown_realms_r1a0i0_effect = yes", "dynmap_r016_rootdown_realms_r0a0i0_effect = yes", 1)
        with self.assertRaises(AssertionError):
            _check_source(SOURCE.replace(start, skipped, 1))
        name = "dynmap_r016_rootdown_realms_r0a0i0_effect"
        block = _effect(SOURCE, name)
        duplicate = block.replace("every_held_title = { limit = { tier = tier_county } dynmap_r016_paint_grey_effect = yes }", "every_held_title = { limit = { tier = tier_county } dynmap_r016_paint_grey_effect = yes } every_held_title = { limit = { tier = tier_county } dynmap_r016_paint_grey_effect = yes }", 1)
        with self.assertRaises(AssertionError):
            _check_source(SOURCE.replace(block, duplicate, 1))
        start = _effect(SOURCE, "dynmap_r016_rootdown_start_holdings_effect")
        no_unheld = start.replace("dynmap_r016_paint_grey_effect = yes", "dynmap_r016_paint_light_effect = yes", 1)
        with self.assertRaises(AssertionError):
            _check_source(SOURCE.replace(start, no_unheld, 1))

    def test_audit_write_and_neutral_diagnostic_mutations_are_rejected(self):
        base = _effect(SOURCE, "dynmap_r016_paint_neutral_base_effect")
        no_guard = base.replace("NOT = { exists = scope:dynmap_r016_audit_armed }", "always = yes", 1)
        with self.assertRaises(AssertionError):
            _check_source(SOURCE.replace(base, no_guard, 1))
        grey = _effect(SOURCE, "dynmap_r016_paint_grey_effect")
        no_count = grey.replace("dynmap_r016_diagnostic_county_neutral_effect = yes", "", 1)
        with self.assertRaises(AssertionError):
            _check_source(SOURCE.replace(grey, no_count, 1))


if __name__ == "__main__":
    unittest.main()
