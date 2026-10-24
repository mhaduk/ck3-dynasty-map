"""Small synthetic native-format audit fixtures; no CK3 captures/identities."""

import importlib.util
import json
from pathlib import Path
import re
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("classification", ROOT / "scripts/analyze_dynmap_classification.py")
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


def obj(typ, number, key=None, historical=None, label="Synthetic"):
    return {"type": typ, "runtime_id": str(number), "key": key,
            "historical_id": historical, "label": label}


def character(number, dynasty=10, parent=None, top=None):
    subject = obj("Character", number, historical=str(900000 + number))
    return {"subject": subject,
            "dynasty": obj("Dynasty", dynasty, key="synthetic_" + str(dynasty)) if dynasty is not None else None,
            "liege": obj("Character", parent, historical=str(900000 + parent)) if parent is not None else None,
            "top": obj("Character", top, historical=str(900000 + top)) if top is not None else subject,
            "no_liege": parent is None, "liege_self": parent == number,
            "top_self": top in (None, number), "independent": parent in (None, number)}


def marker(text):
    return ("[12:34:56][D][jomini_effect_impl.cpp:450]: file: "
            "common/scripted_effects/dynmap_r016.txt line: 700 (dynmap_r016_audit_actor_effect): "
            + audit.PREFIX + text + "\n")


def native(value):
    meta = ""
    if value["historical_id"] is not None:
        meta = " - Historical ID " + value["historical_id"]
    elif value["key"] is not None:
        meta = " - Internal Key: " + value["key"]
    return ("[12:34:56][D][effectimpl.cpp:642]: %s (Internal ID: %s%s) "
            "\x15weak (%s - %s)\x15!\n") % (
        value["label"], value["runtime_id"], meta, value["type"], value["runtime_id"])


def identified(field, value):
    return marker(field) + native(value)


def actor(role, value):
    text = marker("ACTOR_BEGIN " + role) + identified("SUBJECT", value["subject"])
    for field in ("DYNASTY", "LIEGE"):
        text += identified(field, value[field.lower()]) if value[field.lower()] else marker(field + "_NULL")
    for field in ("NO_LIEGE", "LIEGE_SELF"):
        text += marker(field + (" YES" if value[field.lower()] else " NO"))
    text += identified("TOP", value["top"]) if value["top"] else marker("TOP_NULL")
    for field in ("TOP_SELF", "INDEPENDENT"):
        text += marker(field + (" YES" if value[field.lower()] else " NO"))
    return text + marker("ACTOR_END")


def fixture(player=None, holder=None, seniors=(), roles=None, held=True, key="c_synthetic_alpha"):
    player = player or character(1)
    roles = roles or ("PRIMARY", "PRIMARY", "PRIMARY")
    county = obj("Landed_title", 500, key=key)
    text = marker(audit.BEGIN) + actor("PLAYER", player)
    text += marker("ROSTER_BEGIN") + identified("EXPECT_COUNTY", county) + marker("ROSTER_END")
    for view, role in zip(audit.VIEWS, roles):
        text += marker("VIEW_BEGIN " + view) + identified("COUNTY_BEGIN", county)
        text += actor("HOLDER", holder or player) if held else marker("HOLDER_NULL")
        text += marker("SENIORS_BEGIN")
        text += "".join(actor("SENIOR", s) for s in seniors)
        text += marker("SENIORS_END")
        text += marker("RESULT %s RGB %s WRITES_SUPPRESSED" % (role, " ".join(map(str, audit.RGB[role]))))
        text += marker("COUNTY_END") + marker("VIEW_END " + view)
    return text + marker("BATCH_END")


def marker_v2(text):
    return marker(text).replace(audit.PREFIX, "DYNMAP_R016 AUDIT V2 ")


def marker_v3(text):
    return marker(text).replace(audit.PREFIX, "DYNMAP_R016 AUDIT V3 ")


def marker_v4(text):
    return marker(text).replace(audit.PREFIX, "DYNMAP_R016 AUDIT V4 ")


def marker_diag_v3(text):
    return marker(text).replace(audit.PREFIX, "DYNMAP_R016 DIAG V3 ")


def native_dump(values, role=1):
    identity_text = native(character(role)["subject"]).split("]: ", 1)[1].strip()
    lines = [native(character(role)["subject"]).strip(), "Root: " + identity_text,
             "", "Saved event targets:"]
    lines.extend("%s: %s.00" % (key, value) for key, value in values.items())
    return "\n".join(lines) + "\n"


def fixture_v4(view="REALMS", **kwargs):
    """Wrap a selected V3 fixture with synthetic, native-shaped declarations."""
    v3 = fixture_v3(view, **kwargs)
    out = []
    for line in v3.splitlines(keepends=True):
        if "DYNMAP_R016 AUDIT V3 BATCH_BEGIN" in line:
            line = line.replace("AUDIT V3 BATCH_BEGIN SOURCE F001_FIX_12 TARGET 1.20.1.2",
                                "AUDIT V4 BATCH_BEGIN SOURCE F004_NATIVE_14 TARGET 1.20.1.2 BUILD 26046173")
        elif "DYNMAP_R016 AUDIT V3 ROSTER_COUNTS " in line:
            match = re.search(r"COUNT (\d+) ACTORS (\d+)", line)
            values = {"dynmap_r016_out_roster": int(match[1]), "dynmap_r016_out_actors": int(match[2])}
            out.append(marker_v4("COUNTERS_BEGIN PHASE ROSTER VIEW SELECTED"))
            out.append(native_dump(values))
            out.append(marker_v4("COUNTERS_END PHASE ROSTER VIEW SELECTED"))
            continue
        elif "DYNMAP_R016 AUDIT V3 COUNTS " in line:
            fields = re.findall(r"([A-Z_]+) (\d+)", line.split("DYNMAP_R016 AUDIT V3 COUNTS ", 1)[1])
            values = {"dynmap_r016_out_" + k.lower(): int(v) for k, v in fields}
            out.append(marker_v4("COUNTERS_BEGIN PHASE VIEW VIEW " + view))
            out.append(native_dump(values))
            out.append(marker_v4("COUNTERS_END PHASE VIEW VIEW " + view))
            continue
        else:
            line = line.replace("DYNMAP_R016 AUDIT V3 ", "DYNMAP_R016 AUDIT V4 ")
        out.append(line)
    return "".join(out)


def actor_v2(role, value):
    return actor(role, value).replace(audit.PREFIX, "DYNMAP_R016 AUDIT V2 ")


def identified_v2(field, value):
    return marker_v2(field) + native(value)


def fixture_v2(player=None, holder=None, seniors=(), roles=None, held=True, key="c_synthetic_alpha"):
    player = player or character(1)
    holder = (holder or player) if held else None
    roles = roles or ("PRIMARY", "PRIMARY", "PRIMARY")
    county = obj("Landed_title", 500, key=key)
    definitions = {audit.ref(player["subject"]): player}
    for value in ([holder] if holder else []) + list(seniors):
        definitions[audit.ref(value["subject"])] = value
    text = marker_v2(audit.BEGIN_V2) + actor_v2("PLAYER", player)
    text += marker_v2("ROSTER_BEGIN")
    text += "".join(actor_v2("DEF", v) for k, v in definitions.items() if k != audit.ref(player["subject"]))
    text += identified_v2("COUNTY_BEGIN", county)
    text += identified_v2("HOLDER", holder["subject"]) if holder else marker_v2("HOLDER_NULL")
    text += marker_v2("COUNTY_END")
    text += marker_v2("ROSTER_COUNTS COUNT 1 ACTORS " + str(len(definitions))) + marker_v2("ROSTER_END")
    for view, role in zip(audit.VIEWS, roles):
        text += marker_v2("VIEW_BEGIN " + view)
        text += identified_v2("RESULT %s RGB %s WRITES_SUPPRESSED" % (
            role, " ".join(map(str, audit.RGB[role]))), county)
        values = dict.fromkeys(audit.COUNTER_FIELDS, 0)
        values.update(total=1, held=int(held), unheld=int(not held))
        values[role.lower()] = 1
        if holder:
            # Fixtures supply a literal chain; no graph/oracle calls into production.
            chain = [holder] + list(seniors)
            d = audit.ref(player["dynasty"])
            values.update(holder_no_dynasty=int(holder["dynasty"] is None),
                          holder_match=int(d is not None and audit.ref(holder["dynasty"]) == d),
                          senior_match=int(d is not None and any(audit.ref(a["dynasty"]) == d for a in seniors)),
                          top_match=int(d is not None and audit.ref(chain[-1]["dynasty"]) == d),
                          subtree=int(any(audit.ref(a["subject"]) == audit.ref(player["subject"]) for a in chain)))
        text += marker_v2("COUNTS " + " ".join(k.upper() + " " + str(values[k]) for k in audit.COUNTER_FIELDS))
        text += marker_v2("VIEW_END " + view)
    return text + marker_v2("BATCH_END")


def fixture_v3(view="REALMS", **kwargs):
    """Selected V3 frame copied from one independent synthetic V2 view."""
    lines = fixture_v2(**kwargs).splitlines(keepends=True)
    kept, in_selected, found_header = [], False, False
    for line in lines:
        payload = line.split("DYNMAP_R016 AUDIT V2 ", 1)[-1].rstrip("\r\n")
        if payload.startswith("BATCH_BEGIN"):
            line = line.replace("DYNMAP_R016 AUDIT V2 ", "DYNMAP_R016 AUDIT V3 ")
            line = line.replace("SCOPE FULL", "SCOPE SELECTED VIEW " + view)
            kept.append(line)
        elif payload == "VIEW_BEGIN " + view:
            in_selected, found_header = True, True
            kept.append(line.replace("DYNMAP_R016 AUDIT V2 ", "DYNMAP_R016 AUDIT V3 "))
        elif payload == "VIEW_END " + view:
            kept.append(line.replace("DYNMAP_R016 AUDIT V2 ", "DYNMAP_R016 AUDIT V3 "))
            in_selected = False
        elif payload == "BATCH_END":
            kept.append(line.replace("DYNMAP_R016 AUDIT V2 ", "DYNMAP_R016 AUDIT V3 "))
        elif in_selected or not payload.startswith(("VIEW_BEGIN ", "RESULT ", "COUNTS ", "VIEW_END ")):
            kept.append(line.replace("DYNMAP_R016 AUDIT V2 ", "DYNMAP_R016 AUDIT V3 "))
    if not found_header:
        raise AssertionError("selected synthetic view missing")
    return "".join(kept)


def effect_source(name):
    source = (ROOT / "research/probes/my-dynasty-r016/mod/common/scripted_effects/dynmap_r016.txt").read_text(encoding="utf-8-sig")
    match = re.search(r"(?ms)^" + re.escape(name) + r" = \{\n(.*?)^\}", source)
    if not match:
        raise AssertionError("missing effect " + name)
    return match[1]


class ClassificationTests(unittest.TestCase):
    def analyze(self, text, **kwargs):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "synthetic.log"
            path.write_bytes(text.encode("utf-8"))
            return audit.analyze_paths([path], **kwargs)

    def assert_status(self, text, status):
        result = self.analyze(text)
        self.assertEqual(result["status"], status, audit.summary(result))
        return result

    def test_existing_positive_and_true_zero_role_controls(self):
        # Positive Primary and genuine zero Secondary/Neutral remain distinct
        # in a nonempty complete synthetic batch; no values are invented.
        report = self.assert_status(fixture_v2(roles=("PRIMARY", "PRIMARY", "PRIMARY")), "PASS")
        self.assertEqual(report["batches"][0]["view_counters"]["REALMS"]["primary"], 1)
        self.assertEqual(report["batches"][0]["view_counters"]["REALMS"]["secondary"], 0)
        self.assertEqual(report["batches"][0]["view_counters"]["REALMS"]["neutral"], 0)

    def test_v3_selected_view_positive_zero_and_independent_semantics(self):
        primary = (character(1), character(1), [])
        secondary = {
            "REALMS": (character(1), character(2, 10, 9, 9), [character(9, 20)]),
            "HOLDINGS": (character(1), character(2, 20, 9, 9), [character(9, 10)]),
            "MY_REALM": (character(1), character(2, 20, 9, 9), [character(9, 10)]),
        }
        neutral = {view: (character(1), character(2, 20, 9, 9), [character(9, 20)])
                   for view in audit.VIEWS}
        for view in audit.VIEWS:
            for role, case in (("PRIMARY", primary), ("SECONDARY", secondary[view]), ("NEUTRAL", neutral[view])):
                with self.subTest(view=view, role=role):
                    player, holder, seniors = case
                    roles = {name: "PRIMARY" for name in audit.VIEWS}
                    roles[view] = role
                    result = self.assert_status(fixture_v3(view, player=player, holder=holder,
                                                           seniors=seniors, roles=tuple(roles[n] for n in audit.VIEWS)), "PASS")
                    batch = result["batches"][0]
                    self.assertEqual(batch["schema"], 3)
                    self.assertEqual(batch["operation_scope"], "SELECTED")
                    self.assertEqual(batch["selected_view"], view)
                    self.assertEqual({row["view"] for row in batch["records"]}, {view})
                    self.assertEqual(len(batch["records"]), 1)
                    self.assertEqual(batch["records"][0]["expected_role"], role)
                    rendered = audit.summary(result)
                    self.assertIn("scope=SELECTED view=" + view, rendered)
                    self.assertIn("only its explicitly named view", rendered)
                    self.assertEqual(batch["view_counters"][view]["total"], 1)
                    self.assertEqual(batch["view_counters"][view]["primary"] +
                                     batch["view_counters"][view]["secondary"] +
                                     batch["view_counters"][view]["neutral"], 1)

    def test_v3_rejects_wrong_or_missing_selected_view_and_zero_declarations(self):
        text = fixture_v3("REALMS")
        self.assert_status(text.replace("SCOPE SELECTED VIEW REALMS", "SCOPE SELECTED VIEW HOLDINGS"), "INCOMPLETE")
        self.assert_status(text.replace(marker_v3("VIEW_BEGIN REALMS"), ""), "INCOMPLETE")
        self.assert_status(text.replace("COUNTS TOTAL 1", "COUNTS TOTAL 0", 1), "INCOMPLETE")
        self.assert_status(text.replace(marker_v3("BATCH_END"), marker_v3("VIEW_BEGIN HOLDINGS") + marker_v3("VIEW_END HOLDINGS") + marker_v3("BATCH_END")), "INCOMPLETE")

    def test_v3_rejects_duplicate_counties_actors_bad_role_and_bad_identity(self):
        text = fixture_v3("REALMS", holder=character(2, 10, 1, 1))
        lines = text.splitlines(keepends=True)
        record = []
        copying = False
        for line in lines:
            if "AUDIT V3 RESULT " in line:
                copying = True
            if copying:
                record.append(line)
            if copying and "AUDIT V3 COUNTS TOTAL" in line:
                record.pop()
                break
        self.assertTrue(record)
        counts_line = next(line for line in lines if "AUDIT V3 COUNTS TOTAL" in line)
        self.assert_status(text.replace("".join(record), "", 1), "INCOMPLETE")
        self.assert_status(text.replace(counts_line, "".join(record) + counts_line, 1), "INCOMPLETE")
        actor_block = []
        copying = False
        for line in lines:
            if "AUDIT V3 ACTOR_BEGIN DEF" in line:
                copying = True
            if copying:
                actor_block.append(line)
            if copying and "AUDIT V3 ACTOR_END" in line:
                break
        self.assertTrue(actor_block)
        roster_end = next(line for line in lines if "AUDIT V3 ROSTER_END" in line)
        self.assert_status(text.replace("".join(actor_block), "", 1), "INCOMPLETE")
        self.assert_status(text.replace(roster_end, "".join(actor_block) + roster_end, 1), "INCOMPLETE")
        self.assert_status(text.replace("RESULT PRIMARY RGB", "RESULT UNKNOWN RGB", 1), "INCOMPLETE")
        self.assert_status(text.replace("c_synthetic_alpha", "b_synthetic_alpha", 1), "INCOMPLETE")

    def test_v3_rejects_interrupted_partial_and_invalid_actor_graph(self):
        text = fixture_v3("MY_REALM")
        self.assert_status(text[:text.index(marker_v3("BATCH_END"))], "INCOMPLETE")
        self.assert_status(text.rstrip("\n"), "INCOMPLETE")
        broken = fixture_v3("REALMS", holder=character(2, 10, 7, 7))
        self.assert_status(broken, "INCOMPLETE")
        rejected = marker_v3("BATCH_BEGIN SOURCE F001_FIX_12 TARGET 1.20.1.2 SCOPE SELECTED VIEW REALMS") + marker_v3("REJECT PLAYER_DEAD_MISSING_OR_NO_DYNASTY") + marker_v3("BATCH_END")
        result = self.assert_status(rejected, "INCOMPLETE")
        self.assertEqual(result["batches"][0]["availability"], "UNAVAILABLE")

    def test_v4_native_counters_drive_selected_audit_without_row_synthesis(self):
        for view in audit.VIEWS:
            report = self.assert_status(fixture_v4(view), "PASS")
            batch = report["batches"][0]
            self.assertEqual(batch["schema"], 4)
            self.assertEqual(batch["counter_source"], "CK3 debug_log_scopes / Saved event targets")
            self.assertEqual(batch["view_counters"][view]["total"], 1)
            self.assertEqual(batch["view_counters"][view]["secondary"], 0)
        broken = fixture_v4("REALMS").replace("dynmap_r016_out_primary: 1.00", "dynmap_r016_out_primary: 0.00")
        self.assert_status(broken, "INCOMPLETE")
        for mutation in (
            lambda s: s.replace("dynmap_r016_out_primary: 1.00\n", "", 1),
            lambda s: s.replace("dynmap_r016_out_primary: 1.00", "dynmap_r016_out_primary: -1.00", 1),
            lambda s: s.replace("dynmap_r016_out_primary: 1.00", "dynmap_r016_out_primary: 1.50", 1),
            lambda s: s.replace("dynmap_r016_out_primary: 1.00", "dynmap_r016_out_primary: 1.00\ndynmap_r016_out_primary: 1.00", 1),
            lambda s: s.replace("BUILD 26046173", "BUILD 999", 1),
            lambda s: s.replace("SOURCE F004_NATIVE_14", "SOURCE F004_NATIVE_15", 1),
            lambda s: s.replace("COUNTERS_BEGIN PHASE VIEW VIEW REALMS", "COUNTERS_BEGIN PHASE VIEW VIEW HOLDINGS", 1),
            lambda s: s.replace("Saved event targets:", "Saved targets:", 1),
        ):
            self.assert_status(mutation(fixture_v4("REALMS")), "INCOMPLETE")
        injected = fixture_v4("REALMS").replace(marker_v4("BATCH_END"),
            "dynmap_r016_out_primary: 1.00\n" + marker_v4("BATCH_END"), 1)
        self.assert_status(injected, "INCOMPLETE")

    def test_v4_rejects_paired_wrong_view_legacy_header_and_spoofed_end(self):
        text = fixture_v4("REALMS")
        self.assert_status(text, "PASS")
        cases = {
            "paired-wrong-view": text.replace("PHASE VIEW VIEW REALMS", "PHASE VIEW VIEW HOLDINGS"),
            "legacy-no-build-header": text.replace(
                "BATCH_BEGIN SOURCE F004_NATIVE_14 TARGET 1.20.1.2 BUILD 26046173",
                "BATCH_BEGIN SOURCE F001_FIX_12 TARGET 1.20.1.2"),
            "spoofed-native-end": text.replace(
                marker_v4("COUNTERS_END PHASE VIEW VIEW REALMS"),
                "untrusted: DYNMAP_R016 AUDIT V4 COUNTERS_END PHASE VIEW VIEW REALMS\n"),
        }
        for name, changed in cases.items():
            with self.subTest(case=name):
                self.assertNotEqual(changed, text)
                self.assert_status(changed, "INCOMPLETE")

    def test_native_numeric_parser_accepts_zero_and_rejects_unknown_targets(self):
        expected = audit.SUMMARY_NATIVE_KEYS
        lines = [native(character(1)["subject"]).strip(),
                 "Root: " + native(character(1)["subject"]).split("]: ", 1)[1].strip(),
                 "", "Saved event targets:"]
        lines.extend(key + ": 0.00" for key in sorted(expected))
        values, _ = audit.parse_native_targets(lines, expected)
        self.assertEqual(values["total"], 0)
        with self.assertRaises(audit.Invalid):
            audit.parse_native_targets(lines + ["dynmap_r016_out_injected: 4.00"], expected)

    def test_diag_v3_complete_native_summary_keeps_diagnostic_scope_separate(self):
        for view in audit.VIEWS:
            values = dict.fromkeys(audit.COUNTER_FIELDS, 0)
            text = marker_diag_v3("BEGIN SOURCE F004_NATIVE_14 TARGET 1.20.1.2 BUILD 26046173 SCOPE SUMMARY VIEW " + view)
            text += marker_diag_v3("COUNTERS_BEGIN PHASE SUMMARY VIEW " + view)
            text += native_dump({"dynmap_r016_out_" + f: v for f, v in values.items()})
            text += marker_diag_v3("COUNTERS_END PHASE SUMMARY VIEW " + view)
            text += marker_diag_v3("END")
            report = self.analyze(text)
            operation = report["diagnostic_operations"][0]
            self.assertEqual(operation["framing"], "COMPLETE")
            self.assertEqual(operation["schema"], 3)
            self.assertEqual(operation["view"], view)
            self.assertEqual(operation["counter_source"], "CK3 debug_log_scopes / Saved event targets")
            self.assertEqual(operation["summary"]["total"], 0)

    def test_diag_v3_rejects_unclosed_or_duplicate_native_blocks(self):
        values = dict.fromkeys(audit.COUNTER_FIELDS, 0)
        base = marker_diag_v3("BEGIN SOURCE F004_NATIVE_14 TARGET 1.20.1.2 BUILD 26046173 SCOPE SUMMARY VIEW REALMS")
        start = marker_diag_v3("COUNTERS_BEGIN PHASE SUMMARY VIEW REALMS")
        dump = native_dump({"dynmap_r016_out_" + f: v for f, v in values.items()})
        end = marker_diag_v3("COUNTERS_END PHASE SUMMARY VIEW REALMS")
        done = marker_diag_v3("END")
        self.assertEqual(self.analyze(base + start + dump + done)["diagnostic_operations"], [])
        report = self.analyze(base + start + dump + end + start + dump + end + done)
        self.assertTrue(report["errors"])

    def test_diag_v3_samples_keep_bounds_and_native_declaration(self):
        values = dict.fromkeys(audit.COUNTER_FIELDS, 0)
        values.update(total=1, primary=1)
        text = marker_diag_v3("BEGIN SOURCE F004_NATIVE_14 TARGET 1.20.1.2 BUILD 26046173 SCOPE SAMPLES VIEW HOLDINGS")
        text += marker_diag_v3("SAMPLE ROLE primary") + marker_diag_v3("DETAIL ROLE neutral")
        text += marker_diag_v3("COUNTERS_BEGIN PHASE SAMPLES VIEW HOLDINGS")
        text += native_dump({"dynmap_r016_out_" + f: v for f, v in values.items()})
        text += marker_diag_v3("COUNTERS_END PHASE SAMPLES VIEW HOLDINGS") + marker_diag_v3("END")
        operation = self.analyze(text)["diagnostic_operations"][0]
        self.assertEqual(operation["samples"]["PRIMARY"], 1)
        self.assertEqual(operation["details"], 1)
        self.assertEqual(operation["native_counter_block"]["phase"], "SAMPLES")

    def test_native_dump_rejects_nested_marker_and_unclosed_wrapper(self):
        expected = audit.SUMMARY_NATIVE_KEYS
        lines = [native(character(1)["subject"]).strip(),
                 "Root: " + native(character(1)["subject"]).split("]: ", 1)[1].strip(),
                 "DYNMAP_R016 DIAG V3 COUNTERS_BEGIN", "Saved event targets:"]
        lines.extend(key + ": 0.00" for key in sorted(expected))
        with self.assertRaises(audit.Invalid):
            audit.parse_native_targets(lines, expected)

    def test_v1_v2_historical_scopes_remain_supported(self):
        self.assert_status(fixture(), "PASS")
        self.assert_status(fixture_v2(), "PASS")
        self.assertEqual(audit.analyze_paths([])["supported_capture_schemas"], [1, 2, 3, 4])

    def test_numeric_total_candidate_and_sample_role_grammar_are_narrow(self):
        loc = (ROOT / "research/probes/my-dynasty-r016/mod/localization/english/dynmap_r016_l_english.yml").read_text(encoding="utf-8-sig")
        effects = (ROOT / "research/probes/my-dynasty-r016/mod/common/scripted_effects/dynmap_r016.txt").read_text(encoding="utf-8-sig")
        total = re.search(r"dynmap_r016_audit_v3_counts:0 \"([^\"]+)\"", loc)[1]
        self.assertIn("TOTAL [SCOPE.GetValue('dynmap_r016_out_total')|0]", total)
        self.assertNotIn("IntToString(FixedPointToInt(SCOPE.GetValue('dynmap_r016_out_total')))", total)
        for role in ("primary", "secondary", "neutral"):
            self.assertIn('debug_log = "DYNMAP_R016 DIAG V3 SAMPLE ROLE ' + role + '"', effects)
            self.assertIn('debug_log = "DYNMAP_R016 DIAG V3 DETAIL ROLE ' + role + '"', effects)
        self.assertNotIn("ROLE $ROLE", effects)

    def test_receiver_experiment_is_retired_without_weakening_v2_unavailable(self):
        loc = (ROOT / "research/probes/my-dynasty-r016/mod/localization/english/dynmap_r016_l_english.yml").read_text(encoding="utf-8-sig")
        effects = (ROOT / "research/probes/my-dynasty-r016/mod/common/scripted_effects/dynmap_r016.txt").read_text(encoding="utf-8-sig")
        self.assertNotIn("dynmap_r016_receiver_nested", loc + effects)
        self.assertNotIn("dynmap_r016_receiver_root", loc + effects)
        self.assertNotIn("RECEIVER EXPERIMENT", loc + effects)
        self.assertIn('else = { debug_log = "DYNMAP_R016 DIAG V3 UNAVAILABLE" }', effects)

    def test_top_dynasty_routes_reuse_realms_modifier_operations(self):
        menu = (ROOT / "research/probes/my-dynasty-r016/mod/gui/zz_dynmap_r016_menu.gui").read_text(encoding="utf-8-sig")
        expected = {
            "dynmap_r016_dynasty_entry": ("dynmap_r016_compute_realms", True),
            "dynmap_r016_dynasty_entry_shift": ("dynmap_r016_summary_realms", True),
            "dynmap_r016_dynasty_entry_option": ("dynmap_r016_samples_realms", True),
            "dynmap_r016_dynasty_entry_audit": ("dynmap_r016_audit_realms", False),
        }
        for name, (operation, selects) in expected.items():
            match = re.search(r'name = "' + re.escape(name) + r'"(.*?)(?=\n        button_round = |\n        flowcontainer = )', menu, re.S)
            self.assertIsNotNone(match, name)
            block = match[1]
            self.assertIn("GetScriptedGui('" + operation + "').Execute(", block)
            self.assertEqual("onclick = \"[SetMapMode('dynmap_my_dynasty')]\"" in block, selects)

    def test_final_banner_restores_icon_order_and_uses_native_header_close(self):
        gui = (ROOT / "research/probes/my-dynasty-r016/mod/gui/zz_dynmap_r016_views.gui").read_text(encoding="utf-8-sig")
        row = gui.split('name = "dynmap_r016_active_subviews"', 1)[1].split('name = "dynmap_r016_custom_header"', 1)[0]
        names = re.findall(r'name = "(dynmap_r016_view_(?:realms|holdings|my_realm)(?:_audit)?)"', row)
        self.assertEqual(names, ["dynmap_r016_view_realms", "dynmap_r016_view_holdings", "dynmap_r016_view_my_realm", "dynmap_r016_view_realms_audit", "dynmap_r016_view_holdings_audit", "dynmap_r016_view_my_realm_audit"])
        self.assertNotIn("dynmap_r016_slot_", row)
        self.assertNotIn("dynmap_r016_legend_", gui)
        self.assertNotIn('text = "dynmap_r016_back"', gui)
        self.assertIn('text = "MAP_MODE_SHOWING_HEADER"', gui)
        self.assertIn("text_map_mode_header = { visible = \"[IsMapMode(\'dynmap_my_dynasty\')]\" text = \"dynmap_r016_realms\" }", gui)
        self.assertIn("onclick = \"[SetMapMode(\'realms\')]\"", gui)
        self.assertIn('shortcut = "close_window"', gui)
        self.assertIn('tooltip = "dynmap_r016_back"', gui)

    def test_hover_copy_has_full_categories_without_debug_or_modifier_hints(self):
        loc = (ROOT / "research/probes/my-dynasty-r016/mod/localization/english/dynmap_r016_l_english.yml").read_text(encoding="utf-8-sig")
        views = (ROOT / "research/probes/my-dynasty-r016/mod/gui/zz_dynmap_r016_views.gui").read_text(encoding="utf-8-sig")
        menu = (ROOT / "research/probes/my-dynasty-r016/mod/gui/zz_dynmap_r016_menu.gui").read_text(encoding="utf-8-sig")
        for key in ("dynmap_r016_realms_tt", "dynmap_r016_holdings_tt", "dynmap_r016_my_realm_tt"):
            line = next(line for line in loc.splitlines() if line.startswith(" " + key + ":"))
            for label in ("Dark:", "Light:", "Grey:"):
                self.assertIn(label, line)
            self.assertNotRegex(line.lower(), r"shift|option|alt|ctrl|debug|hold modifiers|audit")
        for label in ("Dark green:", "Light green:"):
            self.assertNotIn(label, loc)
        self.assertIn('dynmap_r016_dynasty_tt:0 "Open Dynasty Realms and refresh the map for your current Dynasty."', loc)
        self.assertNotRegex(next(line for line in loc.splitlines() if line.startswith(" dynmap_r016_dynasty_tt:")).lower(), r"shift|option|alt|ctrl|debug|hold modifiers|audit")
        self.assertEqual(views.count("using = tooltip_nw"), 6)
        self.assertEqual(menu.count("using = tooltip_nw"), 4)
        self.assertNotRegex(views.lower(), r"on_mouse|tooltip_delay|timer")
        self.assertNotIn("RECEIVER EXPERIMENT", loc)

    def test_hover_cards_have_native_title_paragraph_and_separate_bold_rows(self):
        loc = (ROOT / "research/probes/my-dynasty-r016/mod/localization/english/dynmap_r016_l_english.yml").read_text(encoding="utf-8-sig")
        expected = {
            "dynmap_r016_realms_tt": "Dynasty Realms",
            "dynmap_r016_holdings_tt": "Dynasty Holdings",
            "dynmap_r016_my_realm_tt": "My Realm & Dynasty",
        }
        for key, title in expected.items():
            line = next(line for line in loc.splitlines() if line.startswith(" " + key + ":"))
            value = line.split('"', 1)[1].rsplit('"', 1)[0]
            rows = value.split(r"\n")
            self.assertEqual(len(rows), 8, key)
            self.assertEqual(rows[0], "#T " + title + "#!")
            self.assertTrue(rows[1].strip(), key)
            self.assertEqual(rows[2], "")
            self.assertTrue(rows[3].startswith("#bold Dark:#! "), key)
            self.assertTrue(rows[4].startswith("#bold Light:#! "), key)
            self.assertTrue(rows[5].startswith("#bold Grey:#! "), key)
            self.assertEqual(rows[6], "")
            self.assertTrue(rows[7].strip(), key)

    def test_child_button_hit_frames_match_their_full_slots(self):
        views = (ROOT / "research/probes/my-dynasty-r016/mod/gui/zz_dynmap_r016_views.gui").read_text(encoding="utf-8-sig")
        row = views.split('name = "dynmap_r016_active_subviews"', 1)[1].split('name = "dynmap_r016_custom_header"', 1)[0]
        self.assertEqual(row.count("button_round = {"), 6)
        self.assertEqual(row.count("size = { 40 40 }"), 6)
        self.assertEqual(row.count("size = { 130 40 }"), 1)
        self.assertEqual(row.count("name = \"dynmap_r016_normal_row\""), 1)
        self.assertEqual(row.count("name = \"dynmap_r016_audit_row\""), 1)
        self.assertEqual(row.count("parentanchor = top|left"), 2)
        self.assertEqual(row.count("widgetanchor = top|left"), 2)
        self.assertEqual(row.count("spacing = 5"), 2)
        self.assertEqual(row.count("visible = \"[GetPlayer.IsValid]\""), 6)
        self.assertIn('visible = "[And(GetPlayer.IsValid, Not(And(IsAltDown, IsShiftDown)))]"', row)
        self.assertIn('visible = "[And(GetPlayer.IsValid, And(IsAltDown, IsShiftDown))]"', row)
        self.assertNotRegex(row, r'button_round\s*=\s*\{[^}]*parentanchor\s*=\s*hcenter')

    def test_scope_dump_is_singlely_inserted_at_realms_summary_boundary(self):
        effects = (ROOT / "research/probes/my-dynasty-r016/mod/common/scripted_effects/dynmap_r016.txt").read_text(encoding="utf-8-sig")
        summary = effects.split("dynmap_r016_summary_realms_effect = {", 1)[1].split("dynmap_r016_samples_realms_effect = {", 1)[0]
        self.assertEqual(summary.count("debug_log_scopes = yes"), 1)
        self.assertRegex(summary, r"dynmap_r016_counts_snapshot_effect = yes\n\s*debug_log = \"DYNMAP_R016 DIAG V3 COUNTERS_BEGIN PHASE SUMMARY VIEW REALMS\"\n\s*debug_log_scopes = yes\n\s*debug_log = \"DYNMAP_R016 DIAG V3 COUNTERS_END PHASE SUMMARY VIEW REALMS\"")
        self.assertNotIn('debug_log = "dynmap_r016_diag_counts"', effects)
        self.assertEqual(effects.count("debug_log_scopes = yes"), 10)

    def test_child_modifier_dispatch_keeps_single_view_semantics(self):
        gui = (ROOT / "research/probes/my-dynasty-r016/mod/gui/zz_dynmap_r016_views.gui").read_text(encoding="utf-8-sig")
        for view, mode in (("realms", "dynmap_my_dynasty"),
                           ("holdings", "dynmap_dynasty_holdings"),
                           ("my_realm", "dynmap_my_realm_dynasty")):
            ordinary_name = 'name = "dynmap_r016_view_' + view + '"'
            start = gui.rfind("button_round = {", 0, gui.index(ordinary_name))
            end = gui.find("\n                button_round = {", gui.index(ordinary_name))
            ordinary = gui[start:end]
            self.assertIn('visible = "[GetPlayer.IsValid]"', ordinary)
            self.assertIn("dynmap_r016_samples_" + view, ordinary)
            self.assertIn("dynmap_r016_summary_" + view, ordinary)
            self.assertIn("dynmap_r016_compute_" + view, ordinary)
            self.assertIn("onclick = \"[SetMapMode('" + mode + "')]\"", ordinary)
            self.assertIn("using = tooltip_nw", ordinary)

            audit_name = 'name = "dynmap_r016_view_' + view + '_audit"'
            start = gui.rfind("button_round = {", 0, gui.index(audit_name))
            end = gui.find("\n                button_round = {", gui.index(audit_name))
            if end < 0:
                end = gui.index('\n            flowcontainer = {\n                name = "dynmap_r016_custom_header"', gui.index(audit_name))
            audit_button = gui[start:end]
            self.assertIn('visible = "[GetPlayer.IsValid]"', audit_button)
            self.assertIn("dynmap_r016_audit_" + view, audit_button)
            self.assertNotIn("SetMapMode", audit_button)

    def test_f003_examples_across_all_three_views(self):
        # Nine examples from the fixed contract, using invented runtime identities.
        foreign_king = character(9, 20)
        player_king = character(1)
        player_duke = character(1, parent=9, top=9)
        cases = [
            (player_king, character(2, 20, 1, 1), [player_king], ("PRIMARY", "SECONDARY", "PRIMARY")),
            (player_king, character(2, 10, 1, 1), [player_king], ("PRIMARY", "PRIMARY", "PRIMARY")),
            (player_king, character(2, 10, 9, 9), [foreign_king], ("SECONDARY", "PRIMARY", "SECONDARY")),
            (player_king, character(2, 20, 3, 9), [foreign_king, character(3, 10, 9, 9)], ("SECONDARY", "SECONDARY", "SECONDARY")),
            (player_duke, character(2, 20, 1, 9), [foreign_king, player_duke], ("SECONDARY", "SECONDARY", "PRIMARY")),
            (player_duke, character(2, 20, 9, 9), [foreign_king], ("NEUTRAL", "NEUTRAL", "NEUTRAL")),
            (player_king, character(2, 20, 3, 3), [character(3)], ("PRIMARY", "SECONDARY", "SECONDARY")),
            (player_king, character(2), [], ("PRIMARY", "PRIMARY", "SECONDARY")),
            (player_king, character(2, 20, 9, 9), [foreign_king], ("NEUTRAL", "NEUTRAL", "NEUTRAL")),
        ]
        for player, holder, seniors, roles in cases:
            with self.subTest(roles=roles, holder=holder):
                result = self.assert_status(fixture(player, holder, seniors, roles), "PASS")
                self.assertEqual([r["expected_role"] for r in result["batches"][0]["records"]], list(roles))

    def test_primary_precedence_and_cadet_shared_dynasty_identity(self):
        player = character(1)
        holder = character(2, parent=1, top=1)
        holder["dynasty"]["label"] = "A different cadet label, same Dynasty identity"
        self.assert_status(fixture(player, holder, [player]), "PASS")

    def test_holder_no_dynasty_does_not_suppress_senior_checks(self):
        player = character(1)
        self.assert_status(fixture(player, character(2, None, 1, 1), [player],
                                   ("PRIMARY", "SECONDARY", "PRIMARY")), "PASS")

    def test_independent_holder_with_self_liege_and_no_liege_false(self):
        holder = character(2, parent=2, top=2)
        self.assert_status(fixture(holder=holder, roles=("PRIMARY", "PRIMARY", "SECONDARY")), "PASS")

    def test_regression_secondary_despite_same_dynasty_highest_ruler(self):
        player = character(1, parent=3, top=3)
        senior = character(3, parent=3, top=3)
        text = fixture(player, player, [senior], ("SECONDARY", "PRIMARY", "PRIMARY"))
        result = self.assert_status(text, "FAIL")
        row = result["batches"][0]["records"][0]
        self.assertEqual(row["expected_role"], "PRIMARY")
        self.assertEqual(row["classification_match"], "MISMATCH")
        self.assertEqual(result["exit_code"], 1)
        self.assertIn("c_synthetic_alpha", audit.summary(result))

    def test_vassal_player_own_and_sibling_subtrees(self):
        player = character(1, parent=9, top=9)
        king = character(9, 20)
        self.assert_status(fixture(player, player, [king], ("SECONDARY", "PRIMARY", "PRIMARY")), "PASS")
        self.assert_status(fixture(player, character(2, 10, 9, 9), [king],
                                   ("SECONDARY", "PRIMARY", "SECONDARY")), "PASS")

    def test_absent_holder_is_counted_neutral(self):
        result = self.assert_status(fixture(held=False, roles=("NEUTRAL",) * 3), "PASS")
        self.assertEqual(len(result["batches"][0]["records"]), 3)

    def test_invalid_player_rejection_and_missing_dynasty(self):
        for reason in ("PLAYER_DEAD_MISSING_OR_NO_DYNASTY", "INVALID_ROOT"):
            result = self.assert_status(marker(audit.BEGIN) + marker("REJECT " + reason) + marker("BATCH_END"), "INCOMPLETE")
            self.assertEqual(result["batches"][0]["availability"], "UNAVAILABLE")
        result = self.assert_status(fixture(player=character(1, None)), "INCOMPLETE")
        self.assertEqual(result["batches"][0]["availability"], "UNAVAILABLE")

    def test_missing_contradictory_and_cyclic_hierarchy(self):
        cases = [
            (character(2, 20, 3, 3), []),  # edge has no actor
            (character(2, 20, 3, 9), [character(3)]),  # top contradicts ordinary terminal
            (character(2, 20, 3, 3), [character(3, 10, 2, 3)]),  # cycle
            (character(2), [character(3)]),  # extra senior, no connecting edge
            (character(2, 20, 3, 3), [character(3), character(3)]),  # duplicate
        ]
        for holder, seniors in cases:
            with self.subTest(holder=holder, seniors=seniors):
                result = self.assert_status(fixture(holder=holder, seniors=seniors), "INCOMPLETE")
                self.assertTrue(all(r["classification_match"] == "UNVERIFIED" for r in result["batches"][0]["records"]))

    def test_null_top_is_unverified_not_arbitrary_highest(self):
        holder = character(2)
        holder.update(top=None, top_self=False)
        result = self.assert_status(fixture(holder=holder), "INCOMPLETE")
        self.assertIn("null top_liege", result["batches"][0]["records"][0]["expected_reason"])

    def test_independence_predicate_is_recorded_not_ordinary_chain_oracle(self):
        holder = character(2)
        holder["independent"] = False  # could encode a non-ordinary dependency
        self.assert_status(fixture(holder=holder, roles=("PRIMARY", "PRIMARY", "SECONDARY")), "PASS")

    def test_duplicate_county_and_roster(self):
        text = fixture()
        county = text[text.index(marker("COUNTY_BEGIN")):text.index(marker("VIEW_END REALMS"))]
        self.assert_status(text.replace(marker("VIEW_END REALMS"), county + marker("VIEW_END REALMS")), "INCOMPLETE")
        entry = identified("EXPECT_COUNTY", obj("Landed_title", 500, key="c_synthetic_alpha"))
        self.assert_status(text.replace(marker("ROSTER_END"), entry + marker("ROSTER_END")), "INCOMPLETE")

    def test_truncated_nested_missing_view_and_zero_records(self):
        text = fixture()
        self.assert_status(text[:text.index(marker("BATCH_END"))], "INCOMPLETE")
        self.assert_status(marker(audit.BEGIN) + text, "INCOMPLETE")
        start, end = text.index(marker("VIEW_BEGIN HOLDINGS")), text.index(marker("VIEW_END HOLDINGS")) + len(marker("VIEW_END HOLDINGS"))
        self.assert_status(text[:start] + text[end:], "INCOMPLETE")
        self.assert_status(marker(audit.BEGIN) + marker("BATCH_END"), "INCOMPLETE")
        empty = marker(audit.BEGIN) + actor("PLAYER", character(1)) + marker("ROSTER_BEGIN") + marker("ROSTER_END")
        for view in audit.VIEWS:
            empty += marker("VIEW_BEGIN " + view) + marker("VIEW_END " + view)
        self.assert_status(empty + marker("BATCH_END"), "INCOMPLETE")
        self.assert_status("ordinary non-audit log\n", "INCOMPLETE")

    def test_missing_county_and_missing_actor_field(self):
        text = fixture()
        start, end = text.index(marker("COUNTY_BEGIN")), text.index(marker("VIEW_END REALMS"))
        self.assert_status(text[:start] + text[end:], "INCOMPLETE")
        self.assert_status(text.replace(marker("TOP_SELF YES"), "", 1), "INCOMPLETE")

    def test_repeated_complete_batches_and_file_boundaries(self):
        result = self.assert_status(fixture() + fixture(key="c_synthetic_beta"), "PASS")
        self.assertEqual([b["sequence"] for b in result["batches"]], [1, 2])
        with tempfile.TemporaryDirectory() as temp:
            first, second = Path(temp) / "one.log", Path(temp) / "two.log"
            text = fixture()
            middle = text.index(marker("VIEW_BEGIN HOLDINGS"))
            first.write_text(text[:middle]); second.write_text(text[middle:])
            self.assertEqual(audit.analyze_paths([first, second])["status"], "INCOMPLETE")

    def test_intended_rgb_is_separate_from_semantic_match(self):
        result = self.assert_status(fixture().replace("RGB 25 105 50", "RGB 1 2 3", 1), "FAIL")
        batch = result["batches"][0]
        self.assertEqual(batch["classification_match"], "MATCH")
        self.assertEqual(batch["intended_rgb_mapping"], "MISMATCH")
        self.assertIn("UNVERIFIED", result["runtime_storage"])

    def test_identity_names_do_not_match_runtime_and_historical_namespaces(self):
        text = fixture()
        text = text.replace("Synthetic (Internal ID: 1 - Historical ID 900001)", "Other label (Internal ID: 1 - Historical ID 900001)")
        self.assert_status(text, "PASS")
        self.assert_status(fixture().replace("Character - 1", "Character - 900001", 1), "INCOMPLETE")
        self.assert_status(fixture().replace("Historical ID 900001", "Internal Key: 900001", 1), "INCOMPLETE")
        self.assert_status(fixture().replace("Historical ID 900001", "Historical ID 999999", 1), "INCOMPLETE")

    def test_generated_character_without_historical_identity(self):
        holder = character(2)
        holder["subject"]["historical_id"] = None
        self.assert_status(fixture(holder=holder, roles=("PRIMARY", "PRIMARY", "SECONDARY")), "PASS")

    def test_null_flags_wrong_types_and_inconsistent_county_identity(self):
        text = fixture()
        for modified in [text.replace("NO_LIEGE YES", "NO_LIEGE NO", 1),
                         text.replace("Landed_title - 500", "Dynasty - 500", 1),
                         text.replace("Internal Key: c_synthetic_alpha", "Internal Key: c_other", 1),
                         text.replace("TOP_SELF YES", "TOP_SELF NO", 1),
                         text.replace("RGB 25 105 50", "RGB 999 0 0", 1),
                         text.replace("RGB 25 105 50", "RGB " + "9" * 5000 + " 0 0", 1)]:
            self.assert_status(modified, "INCOMPLETE")

    def test_unsupported_ambiguous_missing_native_lines_and_versions(self):
        text = fixture()
        scope = native(character(1)["subject"])
        self.assert_status(text.replace(scope, "unrelated line\n" + scope, 1), "INCOMPLETE")
        self.assert_status(text.replace(scope, scope + scope, 1), "INCOMPLETE")
        self.assert_status(text.replace("AUDIT V1", "AUDIT V2", 1), "INCOMPLETE")
        self.assert_status(text.replace(marker("ACTOR_END"), marker("SUBJECT") + scope + marker("ACTOR_END"), 1), "INCOMPLETE")
        self.assert_status(text.rstrip("\n"), "INCOMPLETE")

    def test_byte_line_limits_and_input_error_never_pass(self):
        result = self.analyze(fixture(), max_bytes=100)
        self.assertEqual(result["status"], "INCOMPLETE")
        self.assertEqual(result["inputs"][0]["hash_scope"], "partial input only")
        self.assert_status("x" * (audit.MAX_LINE_BYTES + 1), "INCOMPLETE")
        result = audit.analyze_paths([ROOT / "tests/does-not-exist-synthetic.log"])
        self.assertEqual(result["exit_code"], 2)

    def test_source_emitted_grammar_uses_tested_native_shapes(self):
        # Historical V1/V2/V3 input remains covered above; active calls emit V4.
        source = (ROOT / "research/probes/my-dynasty-r016/mod/common/scripted_effects/dynmap_r016.txt").read_text(encoding="utf-8-sig")
        for view in ("REALMS", "HOLDINGS", "MY_REALM"):
            self.assertIn("SCOPE SELECTED VIEW " + view, source)
        self.assertNotIn("DYNMAP_R016 AUDIT V2", source)
        for field in ("SUBJECT", "DYNASTY", "LIEGE", "TOP", "COUNTY_BEGIN", "HOLDER"):
            self.assertRegex(source, r'debug_log = "DYNMAP_R016 AUDIT V4 ' + field + r'"\s+debug_log_scopes = no')
        self.assertEqual(source.count('debug_log = "DYNMAP_R016 AUDIT V4 COUNTERS_BEGIN PHASE VIEW VIEW '), 3)
        self.assertEqual(source.count('debug_log = "DYNMAP_R016 AUDIT V4 COUNTERS_BEGIN PHASE ROSTER VIEW SELECTED"'), 1)
        self.assertNotIn('debug_log = "dynmap_r016_audit_v3_counts"', source)
        roster_phase = source.split('dynmap_r016_audit_v3_roster_effect = {', 1)[1].split('\n}', 1)[0]
        self.assertLess(roster_phase.index('COUNTERS_END PHASE ROSTER'), roster_phase.index('clear_saved_scope = dynmap_r016_out_roster'))
        self.assertLess(roster_phase.index('clear_saved_scope = dynmap_r016_out_actors'), roster_phase.index('ROSTER_END'))
        loc = (ROOT / "research/probes/my-dynasty-r016/mod/localization/english/dynmap_r016_l_english.yml").read_text(encoding="utf-8-sig")
        for key in ("dynmap_r016_audit_v3_counts", "dynmap_r016_diag_counts", "dynmap_r016_audit_v3_roster_counts"):
            line = next(line for line in loc.splitlines() if line.startswith(" " + key + ":"))
            if key == "dynmap_r016_audit_v3_counts":
                self.assertIn("TOTAL [SCOPE.GetValue('dynmap_r016_out_total')|0]", line)
                self.assertNotIn("IntToString(FixedPointToInt(SCOPE.GetValue('dynmap_r016_out_total')))", line)
                self.assertEqual(line.count("SCOPE.GetValue("), line.count("IntToString(FixedPointToInt(" ) + 1)
            else:
                self.assertNotIn("|0", line)  # Other counters retain the historical machine grammar.
                self.assertEqual(line.count("SCOPE.GetValue("), line.count("IntToString(FixedPointToInt("))

    def test_runtime_only_dynasty_empty_and_missing_keys_v1_v2(self):
        for fixture_fn in (fixture, fixture_v2):
            text = fixture_fn(holder=character(2), roles=("PRIMARY", "PRIMARY", "SECONDARY"))
            for replacement in (" - Internal Key: ", ""):
                self.assert_status(text.replace(" - Internal Key: synthetic_10", replacement), "PASS")
            self.assert_status(text.replace(" - Internal Key: synthetic_10", "", 1), "INCOMPLETE")
            self.assert_status(text.replace("Dynasty - 10", "Dynasty - 11", 1), "INCOMPLETE")
            self.assert_status(text.replace(" - Internal Key: c_synthetic_alpha", ""), "INCOMPLETE")
            self.assert_status(text.replace(" - Internal Key: c_synthetic_alpha", " - Internal Key: "), "INCOMPLETE")
        generated = character(2, 30)
        generated["dynasty"]["key"] = None
        self.assert_status(fixture_v2(holder=generated, roles=("NEUTRAL",) * 3), "PASS")
        self.assert_status(fixture_v2(holder=character(2, None), roles=("NEUTRAL",) * 3), "PASS")
        # Runtime-only D is still a Dynasty, not a null Dynasty or name match.
        foreign = fixture(holder=character(2, 20), roles=("NEUTRAL",) * 3)
        self.assert_status(foreign.replace(" - Internal Key: synthetic_20", ""), "PASS")
        self.assert_status(foreign.replace(" - Internal Key: synthetic_20", " - Internal Key: synthetic_10"), "INCOMPLETE")
        self.assert_status(fixture().replace("Historical ID 900001", "Historical ID ", 1), "INCOMPLETE")

    def test_v2_complete_all_three_views_repeated_and_cross_schema_batches(self):
        result = self.assert_status(fixture_v2() + fixture_v2(key="c_synthetic_beta"), "PASS")
        self.assertEqual([b["schema"] for b in result["batches"]], [2, 2])
        self.assertEqual(result["batches"][0]["operation_scope"], "FULL")
        self.assertEqual(len(result["batches"][0]["actor_definitions"]), 1)
        self.assert_status(fixture() + fixture_v2(), "PASS")
        self.assert_status(fixture_v2() + fixture(), "PASS")

    def test_v2_self_liege_regression_foreign_top_and_unheld(self):
        player = character(1, parent=3, top=3)
        senior = character(3, parent=3, top=3)
        self.assert_status(fixture_v2(player, player, [senior]), "PASS")
        result = self.assert_status(fixture_v2(player, player, [senior],
                                  ("SECONDARY", "PRIMARY", "PRIMARY")), "FAIL")
        self.assertEqual(result["batches"][0]["records"][0]["expected_role"], "PRIMARY")
        king = character(9, 20)
        middle = character(3, 10, 9, 9)
        self.assert_status(fixture_v2(holder=character(2, 20, 3, 9), seniors=[middle, king],
                                     roles=("SECONDARY",) * 3), "PASS")
        self.assert_status(fixture_v2(holder=character(2, 20, 2, 2), roles=("NEUTRAL",) * 3), "PASS")
        self.assert_status(fixture_v2(held=False, roles=("NEUTRAL",) * 3), "PASS")
        self.assert_status(fixture_v2(holder=character(2, None, 1, 1), seniors=[character(1)],
                                     roles=("PRIMARY", "SECONDARY", "PRIMARY")), "PASS")

    def test_v2_vassal_player_subtree_and_sibling(self):
        king, player = character(9, 20), character(1, 10, 9, 9)
        self.assert_status(fixture_v2(player, player, [king], ("SECONDARY", "PRIMARY", "PRIMARY")), "PASS")
        self.assert_status(fixture_v2(player, character(2, 10, 9, 9), [king],
                                     ("SECONDARY", "PRIMARY", "SECONDARY")), "PASS")

    def test_v2_missing_duplicate_conflicting_actors_and_unsupported_references(self):
        text = fixture_v2(holder=character(2), roles=("PRIMARY", "PRIMARY", "SECONDARY"))
        definition = actor_v2("DEF", character(2))
        self.assert_status(text.replace(definition, ""), "INCOMPLETE")
        self.assert_status(text.replace(definition, definition * 2), "INCOMPLETE")
        conflicting = actor_v2("DEF", character(2, 20))
        self.assert_status(text.replace(definition, definition + conflicting), "INCOMPLETE")
        self.assert_status(text.replace(identified_v2("HOLDER", character(2)["subject"]),
                                        identified_v2("HOLDER", character(99)["subject"])), "INCOMPLETE")
        self.assert_status(text.replace("ROSTER_COUNTS COUNT 1 ACTORS 2", "ROSTER_COUNTS COUNT 1 ACTORS 3"), "INCOMPLETE")
        self.assert_status(text.replace("HOLDER\n", "HOLDER_REF unknown\n"), "INCOMPLETE")
        # Same runtime reference but contradictory historical metadata must not resolve.
        self.assert_status(text.replace(identified_v2("HOLDER", character(2)["subject"]),
                                        identified_v2("HOLDER", obj("Character", 2, historical="999999"))), "INCOMPLETE")

    def test_v2_missing_links_cycles_conflicting_tops_and_unused_bad_definition(self):
        self.assert_status(fixture_v2(holder=character(2, 10, 3, 3)), "INCOMPLETE")
        self.assert_status(fixture_v2(holder=character(2, 10, 3, 3), seniors=[character(3, 10, 2, 3)]), "INCOMPLETE")
        self.assert_status(fixture_v2(holder=character(2, 10, 3, 9), seniors=[character(3)]), "INCOMPLETE")
        bad = character(9); bad.update(top=None, top_self=False)
        self.assert_status(fixture_v2().replace(marker_v2("ROSTER_BEGIN"),
                marker_v2("ROSTER_BEGIN") + actor_v2("DEF", bad)).replace("COUNT 1 ACTORS 1", "COUNT 1 ACTORS 2"), "INCOMPLETE")

    def test_v2_missing_duplicate_county_views_endings_counters_zero_roster(self):
        text = fixture_v2()
        for field in ("COUNTY_END", "ROSTER_END", "VIEW_BEGIN HOLDINGS", "VIEW_END MY_REALM", "BATCH_END"):
            self.assert_status(text.replace(marker_v2(field), "", 1), "INCOMPLETE")
        self.assert_status(text.replace(marker_v2("VIEW_BEGIN REALMS"), marker_v2("VIEW_BEGIN REALMS") * 2), "INCOMPLETE")
        result_line = identified_v2("RESULT PRIMARY RGB 25 105 50 WRITES_SUPPRESSED", obj("Landed_title", 500, key="c_synthetic_alpha"))
        self.assert_status(text.replace(result_line, "", 1), "INCOMPLETE")
        self.assert_status(text.replace(result_line, result_line * 2, 1), "INCOMPLETE")
        roster = identified_v2("COUNTY_BEGIN", obj("Landed_title", 500, key="c_synthetic_alpha")) + identified_v2("HOLDER", character(1)["subject"]) + marker_v2("COUNTY_END")
        self.assert_status(text.replace(roster, roster * 2).replace("COUNT 1 ACTORS", "COUNT 2 ACTORS"), "INCOMPLETE")
        self.assert_status(text.replace("COUNTS TOTAL 1", "COUNTS TOTAL 2", 1), "INCOMPLETE")
        self.assert_status(text.replace("ATTEMPTED_WRITES 0", "ATTEMPTED_WRITES 1", 1), "INCOMPLETE")
        self.assert_status(text.replace("TOP_MATCH 1", "TOP_MATCH 0", 1), "INCOMPLETE")
        self.assert_status(text.replace("COUNTS TOTAL 1", "COUNTS TOTAL " + "9" * 5000, 1), "INCOMPLETE")
        self.assert_status(text.replace(roster, "").replace(result_line, "").replace("COUNT 1 ACTORS", "COUNT 0 ACTORS"), "INCOMPLETE")

    def test_v2_partial_modes_version_rgb_and_native_ambiguity(self):
        text = fixture_v2()
        for scope in ("SUMMARY", "SAMPLES", "PARTIAL"):
            self.assert_status(text.replace("SCOPE FULL", "SCOPE " + scope), "INCOMPLETE")
        for mode in ("SUMMARY", "SAMPLES"):
            diagnostic = marker_v2("BEGIN SOURCE F001_FIX_12 SCOPE " + mode + " VIEW REALMS").replace("AUDIT V2", "DIAG V2")
            self.assert_status(diagnostic, "INCOMPLETE")
        self.assert_status(text.replace("AUDIT V2", "AUDIT V3", 1), "INCOMPLETE")
        self.assert_status(text.replace("AUDIT V2", "AUDIT V1", 1), "INCOMPLETE")
        self.assert_status(text.replace("RGB 25 105 50", "RGB 999 0 0", 1), "INCOMPLETE")
        self.assert_status(text.replace("RGB 25 105 50", "RGB 1 2 3", 1), "FAIL")
        line = native(character(1)["subject"])
        self.assert_status(text.replace(line, line * 2, 1), "INCOMPLETE")
        self.assert_status(text.rstrip("\n"), "INCOMPLETE")

    def test_diagnostic_scope_framing_bounds_and_unavailable_never_full_pass(self):
        def dm(value):
            return marker_v2(value).replace("AUDIT V2", "DIAG V2")
        counters = "SUMMARY TOTAL 1 PRIMARY 1 SECONDARY 0 NEUTRAL 0 HELD 1 UNHELD 0 HOLDER_NO_DYNASTY 0 HOLDER_MATCH 1 SENIOR_MATCH 0 TOP_MATCH 1 SUBTREE 1 ATTEMPTED_WRITES 4"
        for mode in ("SUMMARY", "SAMPLES"):
            begin = dm("BEGIN SOURCE F001_FIX_12 SCOPE " + mode + " VIEW REALMS")
            text = begin + dm(counters) + dm("END")
            report = self.assert_status(text, "INCOMPLETE")
            self.assertEqual(report["diagnostic_operations"][0]["operation_scope"], mode)
            self.assertIn("PAINT_ATTEMPTS", report["diagnostic_operations"][0]["write_policy"])
            self.assertIn("full audits suppress writes", report["runtime_storage"])
            self.assert_status(fixture_v2() + text, "PASS")
            self.assert_status(fixture_v2() + text.rstrip("\n"), "INCOMPLETE")
            self.assert_status(fixture_v2() + begin, "INCOMPLETE")
            self.assert_status(fixture_v2() + begin + dm(counters) * 2 + dm("END"), "INCOMPLETE")
        begin = dm("BEGIN SOURCE F001_FIX_12 SCOPE SAMPLES VIEW REALMS")
        sample, detail = dm("SAMPLE ROLE primary"), dm("DETAIL ROLE neutral")
        at_bound = begin + sample * 10 + detail * 20 + dm(counters) + dm("END")
        self.assert_status(fixture_v2() + at_bound, "PASS")
        for records in (sample * 11, detail * 21):
            self.assert_status(fixture_v2() + begin + records + dm(counters) + dm("END"), "INCOMPLETE")
        self.assert_status(fixture_v2() + begin.replace("SCOPE SAMPLES", "SCOPE SUMMARY") + sample + dm(counters) + dm("END"), "INCOMPLETE")
        self.assert_status(fixture_v2() + begin + dm("UNAVAILABLE") + dm("END"), "PASS")
        self.assert_status(fixture_v2() + begin + dm("END"), "INCOMPLETE")
        self.assert_status(fixture_v2() + begin + dm(counters.replace("TOTAL 1", "TOTAL 2")) + dm("END"), "INCOMPLETE")
        self.assert_status(fixture_v2() + begin.replace("DIAG V2", "DIAG V3"), "INCOMPLETE")
        # Even a correctly framed zero roster/counter stream cannot pass.
        empty = marker_v2(audit.BEGIN_V2) + actor_v2("PLAYER", character(1))
        empty += marker_v2("ROSTER_BEGIN") + marker_v2("ROSTER_COUNTS COUNT 0 ACTORS 1") + marker_v2("ROSTER_END")
        for view in audit.VIEWS:
            empty += marker_v2("VIEW_BEGIN " + view)
            empty += marker_v2("COUNTS " + " ".join(f.upper() + " 0" for f in audit.COUNTER_FIELDS))
            empty += marker_v2("VIEW_END " + view)
        self.assert_status(empty + marker_v2("BATCH_END"), "INCOMPLETE")
        text = fixture_v2()
        line = next(line for line in text.splitlines(True) if "COUNTS TOTAL" in line)
        self.assert_status(text.replace(line, "", 1), "INCOMPLETE")

    def test_source_normal_paths_full_audit_and_bounded_cleanup_invariants(self):
        source = (ROOT / "research/probes/my-dynasty-r016/mod/common/scripted_effects/dynmap_r016.txt").read_text(encoding="utf-8-sig")
        sg = (ROOT / "research/probes/my-dynasty-r016/mod/common/scripted_guis/dynmap_r016.txt").read_text(encoding="utf-8-sig")
        for view in ("realms", "holdings", "my_realm"):
            world = effect_source("dynmap_r016_world_" + view + "_effect")
            self.assertNotIn("debug_log", world)
            self.assertNotIn("local_variable", world)
            self.assertIn("dynmap_r016_operation_cleanup_effect = yes dynmap_r016_world_" + view + "_effect", sg)
            for mode in ("summary", "samples"):
                body = effect_source("dynmap_r016_" + mode + "_" + view + "_effect")
                self.assertEqual(body.count("dynmap_r016_world_" + view + "_effect"), 1)
                self.assertEqual(body.count("dynmap_r016_operation_cleanup_effect = yes"), 2)
                self.assertEqual("save_scope_as = dynmap_r016_diagnostic_samples" in body, mode == "samples")
        for view in ("realms", "holdings", "my_realm"):
            batch = effect_source("dynmap_r016_audit_" + view + "_selected_effect")
            self.assertNotIn("diagnostic_samples", batch)
            self.assertNotIn("set_title_color", batch)
            self.assertEqual(batch.count("dynmap_r016_audit_v3_roster_effect = yes"), 1)
            self.assertEqual(batch.count("dynmap_r016_operation_cleanup_effect = yes"), 2)
            self.assertEqual(batch.count("dynmap_r016_world_" + view + "_effect"), 1)
            self.assertEqual(sum(batch.count("dynmap_r016_world_" + other + "_effect") for other in ("realms", "holdings", "my_realm")), 1)
        roster = effect_source("dynmap_r016_audit_v3_roster_effect")
        self.assertEqual(roster.count("every_county"), 1)
        self.assertEqual(roster.count("dynmap_r016_world_"), 0)
        for color in ("dark", "light", "grey"):
            writer = effect_source("dynmap_r016_paint_" + color + "_effect")
            audit_arm, paint_arm = writer.split("\n\telse = {", 1)
            self.assertNotIn("set_title_color", audit_arm)
            self.assertNotIn("every_in_de_jure_hierarchy", audit_arm)
            self.assertNotIn("diagnostic_county", audit_arm)
            self.assertIn("exists = scope:dynmap_r016_diagnostic_armed", paint_arm)
            self.assertEqual(paint_arm.count("set_title_color"), 1)
        for role in ("primary", "secondary", "neutral"):
            bounded = effect_source("dynmap_r016_diagnostic_county_" + role + "_effect")
            self.assertIn("dynmap_r016_d_sample_" + role + " < 10", bounded)
            self.assertIn("dynmap_r016_d_details < 20", bounded)
            self.assertIn("else_if", bounded)
            self.assertNotIn("random", bounded)
        initialized = set(re.findall(r"set_local_variable = \{ name = (dynmap_r016_d_\w+)", source))
        cleaned = set(re.findall(r"remove_local_variable = (dynmap_r016_d_\w+)", effect_source("dynmap_r016_diagnostic_cleanup_effect")))
        self.assertEqual(initialized, cleaned)
        realms = effect_source("dynmap_r016_realms_county_effect")
        self.assertEqual(realms.count("top_liege = this"), 2)
        self.assertNotRegex(realms, r"NOT = \{\s+exists = liege")
        # Evaluate stable-key source routing; engine delivery needs user testing.
        views = (ROOT / "research/probes/my-dynasty-r016/mod/gui/zz_dynmap_r016_views.gui").read_text()
        self.assertNotIn("onaltshift", views)
        self.assertNotRegex(views, r"\bonalt\s*=")

        def blocks(text, kind):
            # Bounded brace extraction ignores quoted expressions and comments.
            tokens = list(re.finditer(r'"[^"\n]*"|#[^\n]*|\b\w+\b|[{}=]', text))
            for i, token in enumerate(tokens[:-2]):
                if (token.group(), tokens[i + 1].group(), tokens[i + 2].group()) != (kind, "=", "{"):
                    continue
                depth = 1
                for end in tokens[i + 3:]:
                    depth += (end.group() == "{") - (end.group() == "}")
                    if depth == 0:
                        yield text[tokens[i + 2].end():end.start()]
                        break
                else:
                    self.fail("unclosed " + kind)

        menu = (ROOT / "research/probes/my-dynasty-r016/mod/gui/zz_dynmap_r016_menu.gui").read_text(encoding="utf-8-sig")
        native_instances = list(blocks(menu, "dynmap_r016_mode_button"))
        self.assertEqual(len(native_instances), 16)
        self.assertIsNotNone(re.search(r"type dynmap_r016_mode_button = icon_button_mapmode\s*\{.*?size\s*=\s*\{\s*32\s+32\s*\}", menu, re.S))
        for instance in native_instances:
            explicit_size = re.search(r"(?m)^ {16}size\s*=\s*\{\s*(\d+)\s+(\d+)\s*\}", instance)
            if explicit_size:
                self.assertEqual(explicit_size.groups(), ("32", "32"))
        top_buttons = list(blocks(menu, "button_round"))
        for name in ("dynmap_r016_dynasty_entry", "dynmap_r016_dynasty_entry_shift",
                     "dynmap_r016_dynasty_entry_option", "dynmap_r016_dynasty_entry_audit"):
            button = next(body for body in top_buttons if 'name = "' + name + '"' in body)
            self.assertRegex(button, r"size\s*=\s*\{\s*40\s+40\s*\}")
            self.assertIn("alwaystransparent = yes", button)

        def properties(text):
            # Only this container's fields; nested icons cannot add callbacks.
            depth, direct = 0, []
            for token in re.finditer(r'"[^"\n]*"|#[^\n]*|[{}]|[^{}"#]+', text):
                value = token.group()
                if value == "{":
                    depth += 1
                elif value == "}":
                    depth -= 1
                elif depth == 0 and not value.startswith("#"):
                    direct.append(value)
            return re.findall(r'(\w+)\s*=\s*"([^"\n]*)"', "".join(direct))

        def evaluate(expression, keys):
            # Only the authored boolean/string selector subset; unknown syntax fails.
            tokens = re.findall(r"'[^']*'|[\w.]+|[(),]|\S", expression.strip("[]"))
            def value():
                token = tokens.pop(0)
                if token.startswith("'"):
                    return token[1:-1]
                if token in keys:
                    return keys[token]
                arity = {"Not": 1, "And": 2, "Or": 2, "Select_CString": 3}
                self.assertIn(token, arity)
                self.assertEqual(tokens.pop(0), "(")
                args = []
                for index in range(arity[token]):
                    if index:
                        self.assertEqual(tokens.pop(0), ",")
                    args.append(value())
                self.assertEqual(tokens.pop(0), ")")
                if token == "Select_CString":
                    return args[1] if args[0] else args[2]
                return {"Not": lambda: not args[0], "And": lambda: all(args),
                        "Or": lambda: any(args)}[token]()
            result = value()
            self.assertEqual(tokens, [])
            return result

        expected_modes = {"realms": "dynmap_my_dynasty", "holdings": "dynmap_dynasty_holdings",
                          "my_realm": "dynmap_my_realm_dynasty"}
        expected_routes = {(False, False): "compute", (True, False): "summary",
                           (False, True): "samples", (True, True): "audit"}
        fresh_root = r"GuiScope\s*\.SetRoot\(\s*GetPlayer.MakeScope\s*\)\s*\.End"
        valid_check = r"GetScriptedGui\('dynmap_r016_check'\)\.IsValid\(\s*" + fresh_root + r"\s*\)"
        buttons = list(blocks(views.split('name = "dynmap_r016_active_subviews"', 1)[1].split('name = "dynmap_r016_custom_header"', 1)[0], "button_round"))
        self.assertEqual(len(buttons), 6)
        for view, map_id in expected_modes.items():
            buttons_for_mode = [button for button in buttons if dict(properties(button)).get("down") == "[IsMapMode('" + map_id + "')]" ]
            self.assertEqual(len(buttons_for_mode), 2, view)
            for button in buttons:
                if dict(properties(button)).get("down") != "[IsMapMode('" + map_id + "')]":
                    continue
                for icon in blocks(button, "button_icon"):
                    self.assertFalse(any(key.startswith("on") for key, _ in properties(icon)))
            for shift in (False, True):
                for alt in (False, True):
                    for ctrl in (False, True):
                        with self.subTest(view=view, shift=shift, alt=alt, ctrl=ctrl):
                            keys = {"IsShiftDown": shift, "IsAltDown": alt, "IsCtrlDown": ctrl,
                                    "GetPlayer.IsValid": True, "CanChangeMapMode": True,
                                    "valid_context": True}
                            self.assertEqual(sum(evaluate(dict(properties(button))["visible"], dict(keys, **{"GetPlayer.IsValid": False})) for button in buttons_for_mode), 0)
                            audit_row = shift and alt
                            row_name = "dynmap_r016_audit_row" if audit_row else "dynmap_r016_normal_row"
                            row_match = re.search(r'name = "' + row_name + r'"(.*?)(?=\n\s*}\s*flowcontainer =|\n\s*}\s*}\s*flowcontainer =)', views, re.S)
                            self.assertIsNotNone(row_match, row_name)
                            row_visible = re.search(r'visible\s*=\s*"(\[[^\]]+\])"', row_match[1])[1]
                            self.assertTrue(evaluate(row_visible, keys))
                            other_name = "dynmap_r016_normal_row" if audit_row else "dynmap_r016_audit_row"
                            other_match = re.search(r'name = "' + other_name + r'"(.*?)(?=\n\s*}\s*flowcontainer =|\n\s*}\s*}\s*flowcontainer =)', views, re.S)
                            other_visible = re.search(r'visible\s*=\s*"(\[[^\]]+\])"', other_match[1])[1]
                            self.assertFalse(evaluate(other_visible, keys))
                            active = [button for button in buttons_for_mode
                                      if dict(properties(button)).get("name", "").endswith("_audit") == audit_row
                                      and evaluate(dict(properties(button))["visible"], keys)]
                            self.assertEqual(len(active), 1)
                            props = properties(active[0])
                            enabled, count = re.subn(valid_check, "valid_context", dict(props)["enabled"])
                            self.assertEqual(count, 1)
                            self.assertTrue(evaluate(enabled, keys))
                            for guard in ("CanChangeMapMode", "valid_context"):
                                self.assertFalse(evaluate(enabled, dict(keys, **{guard: False})))
                            callbacks = [value for key, value in props if key.startswith("on")]
                            self.assertEqual([key for key, _ in props if key.startswith("on")],
                                             ["onclick"] * len(callbacks))
                            dispatches, maps, order = [], [], []
                            for callback in callbacks:
                                execute = re.fullmatch(r"\[GetScriptedGui\((.*)\)\.Execute\(\s*" + fresh_root + r"\s*\)\]", callback)
                                select = re.fullmatch(r"\[SetMapMode\('([^']+)'\)\]", callback)
                                self.assertTrue(execute or select, callback)
                                if execute:
                                    dispatches.append(evaluate(execute[1], keys))
                                    order.append("execute")
                                else:
                                    maps.append(select[1])
                                    order.append("map")
                            route = expected_routes[shift, alt]
                            expected = "dynmap_r016_" + ("audit_" + view if route == "audit" else route + "_" + view)
                            self.assertEqual(dispatches, [expected])
                            self.assertEqual(maps, [] if shift and alt else [map_id])
                            self.assertEqual(order, ["execute"] if shift and alt else ["execute", "map"])
                            backend = list(blocks(sg, expected))
                            self.assertEqual(len(backend), 1)
                            self.assertRegex(backend[0], r"scope\s*=\s*character\b")
                            self.assertRegex(backend[0], r"is_valid\s*=\s*\{\s*is_alive\s*=\s*yes\s+exists\s*=\s*dynasty\s*\}")
                            if route in ("summary", "samples", "audit"):
                                effect = ("dynmap_r016_audit_" + view + "_selected_effect" if shift and alt else expected + "_effect")
                                self.assertEqual(list(blocks(backend[0], "effect"))[0].split(), [effect, "=", "yes"])

    def test_json_records_have_actual_expected_hierarchy_and_locations(self):
        result = self.assert_status(fixture(), "PASS")
        record = json.loads(json.dumps(result))["batches"][0]["records"][0]
        self.assertEqual(record["source"]["input"], 1)
        self.assertGreater(record["result_source"]["line"], record["source"]["line"])
        self.assertEqual(record["holder"]["subject"]["historical_id"], "900001")
        self.assertEqual(record["holder"]["subject"]["runtime_id"], "1")
        self.assertEqual(record["actual_role"], record["expected_role"])
        self.assertEqual(len(record["ordinary_chain"]), 1)


if __name__ == "__main__":
    unittest.main()
