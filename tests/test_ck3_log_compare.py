import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "ck3_log_compare.py"


def source(start=10, end=20, digest="a", fingerprints=None, state="CAPTURED", count=2):
    fingerprint_rows = fingerprints if fingerprints is not None else [
        {"message": "PRIVATE MESSAGE", "message_sha256": digest * 64, "occurrences": count}
    ]
    return {
        "format": 1, "checkpoint_id": "cp_1", "baseline_id": "base_1",
        "interval_status": "COMPLETE", "expectation_status": "MET",
        "observation_status": "ERRORS_OR_REJECTIONS_OBSERVED",
        "logs": {"debug.log": {"state": state, "required": True, "captured_bytes": end-start,
                 "start_offset": start, "end_offset": end, "source_size_at_boundary": end,
                 "sha256": "b"*64, "partial_initial_line": False}},
        "analysis": {"new_error_lines": sum(row.get("occurrences", 0) for row in fingerprint_rows),
            "omitted_error_lines_after_summary_cap": 0,
            "per_log": {"debug.log": {"error_lines": count, "partial_initial_line": False,
                    "partial_final_line": False}}, "unique_new_errors": fingerprint_rows},
    }


class CompareCliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=Path(tempfile.gettempdir()).resolve())
        self.root = Path(self.tmp.name)
        (self.root / ".codex-sync").mkdir()
        self.left = self.root / "left.json"
        self.right = self.root / "right.json"
        self.manifest = self.root / "input.json"
        self.output = ".codex-sync/out.json"
        self.write_source(self.left, source())
        self.write_source(self.right, source(20, 30, "c"))
        self.write_envelope()

    def tearDown(self):
        self.tmp.cleanup()

    def write_source(self, path, obj):
        path.write_text(json.dumps(obj), encoding="utf-8")

    def pin(self, path):
        data = path.read_bytes()
        return {"path": path.name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

    def write_envelope(self, *, left=None, right=None):
        obj = {"schema": "checkpoint-comparison-input/1", "left": left or self.pin(self.left),
               "right": right or self.pin(self.right)}
        self.manifest.write_text(json.dumps(obj), encoding="utf-8")

    def invoke(self, *, output=None, expect=0):
        result = subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root), "--manifest", "input.json",
                                 "--output", output or self.output], capture_output=True, text=True)
        self.assertEqual(result.returncode, expect, (result.stdout, result.stderr))
        return result

    def report(self):
        return json.loads((self.root / self.output).read_text(encoding="utf-8"))

    def test_adjacent_ranges_and_fixed_nonclaims_and_private_projection(self):
        before = (self.left.read_bytes(), self.right.read_bytes(), self.manifest.read_bytes())
        self.invoke()
        report = self.report()
        self.assertEqual(report["metadata_status"], "COMPLETE")
        item = report["comparison"]["logs"]["debug.log"]
        self.assertEqual(item["declared_range_relation"], "ADJACENT")
        self.assertEqual(item["declared_digest_equality"], "EQUAL")
        self.assertEqual(item["reported_count_relation"], "EQUAL")
        self.assertEqual(report["comparison"]["retained_fingerprint_comparison"][0]["membership"], "LEFT_ONLY")
        self.assertIsNone(item["count_delta"])
        self.assertEqual(report["comparison"]["generation_relation"], "UNKNOWN")
        self.assertEqual(report["comparison"]["byte_continuity"], "UNKNOWN")
        self.assertEqual(report["comparison"]["event_identity"], "UNPROVEN")
        self.assertEqual(report["comparison"]["causality"], "UNPROVEN")
        self.assertIn("message_sha256", json.dumps(report))
        self.assertNotIn("PRIVATE MESSAGE", json.dumps(report))
        self.assertEqual((self.root / self.output).stat().st_mode & 0o777, 0o600)
        self.assertEqual(before, (self.left.read_bytes(), self.right.read_bytes(), self.manifest.read_bytes()))
        self.invoke(output=".codex-sync/deterministic-copy.json")
        self.assertEqual((self.root / self.output).read_bytes(), (self.root / ".codex-sync/deterministic-copy.json").read_bytes())

    def test_missing_or_invalid_analysis_blocks_dependent_range_claims(self):
        for side in ("left", "right"):
            for case in range(5):
                with self.subTest(side=side, case=case):
                    bad = source()
                    if case == 0:
                        del bad["analysis"]["per_log"]
                    elif case == 1:
                        bad["analysis"]["per_log"] = []
                    elif case == 2:
                        del bad["analysis"]["per_log"]["debug.log"]
                    elif case == 3:
                        bad["analysis"]["per_log"]["debug.log"] = []
                    else:
                        bad["analysis"]["per_log"]["debug.log"] = None
                    self.write_source(self.left, bad if side == "left" else source())
                    self.write_source(self.right, bad if side == "right" else source())
                    self.write_envelope()
                    output = f".codex-sync/analysis-{side}-{case}.json"
                    self.invoke(output=output, expect=2)
                    report = json.loads((self.root / output).read_text())
                    self.assertEqual(report["metadata_status"], "INCOMPLETE")
                    self.assertEqual(report["sources"][side]["summary_coverage"], "UNKNOWN")
                    peer = "right" if side == "left" else "left"
                    self.assertEqual(report["sources"][peer]["summary_coverage"], "COMPLETE")
                    row = report["comparison"]["logs"]["debug.log"]
                    self.assertEqual(row["declared_range_relation"], "UNKNOWN")
                    self.assertEqual(row["declared_digest_equality"], "UNKNOWN")

    def test_same_retained_fingerprint_with_different_occurrences(self):
        self.write_source(self.left, source(10, 20, "f", count=1))
        self.write_source(self.right, source(20, 30, "f", count=2))
        self.write_envelope()
        self.invoke()
        report = self.report()
        row = report["comparison"]["retained_fingerprint_comparison"][0]
        self.assertEqual(row["membership"], "BOTH")
        self.assertEqual((row["left_occurrences"], row["right_occurrences"]), (1, 2))
        self.assertEqual(report["comparison"]["logs"]["debug.log"]["reported_count_relation"], "DIFFERENT")
        self.assertEqual(report["comparison"]["global_reported_count_relation"], "DIFFERENT")
        self.assertIsNone(report["comparison"]["count_delta"])

    def test_range_geometry_matrix_and_symmetry_via_cli(self):
        cases = [
            ((4, 4), (4, 4), "IDENTICAL"), ((4, 4), (4, 9), "ADJACENT"),
            ((5, 5), (2, 8), "RIGHT_CONTAINS"), ((2, 8), (5, 5), "LEFT_CONTAINS"),
            ((0, 2), (4, 6), "DISJOINT"), ((0, 8), (2, 6), "LEFT_CONTAINS"),
            ((2, 6), (0, 8), "RIGHT_CONTAINS"), ((0, 5), (3, 8), "OVERLAP"),
            ((0, 3), (3, 8), "ADJACENT"),
        ]
        for index, (a, b, expected) in enumerate(cases):
            self.write_source(self.left, source(a[0], a[1]))
            self.write_source(self.right, source(b[0], b[1], "c"))
            self.write_envelope()
            out = f".codex-sync/geometry-{index}.json"
            self.invoke(output=out)
            self.assertEqual(json.loads((self.root / out).read_text())["comparison"]["logs"]["debug.log"]["declared_range_relation"], expected)
            self.write_source(self.left, source(b[0], b[1]))
            self.write_source(self.right, source(a[0], a[1], "c"))
            self.write_envelope()
            reverse = f".codex-sync/geometry-reverse-{index}.json"
            self.invoke(output=reverse)
            observed = json.loads((self.root / reverse).read_text())["comparison"]["logs"]["debug.log"]["declared_range_relation"]
            mirror = {"LEFT_CONTAINS":"RIGHT_CONTAINS", "RIGHT_CONTAINS":"LEFT_CONTAINS"}.get(expected, expected)
            self.assertEqual(observed, mirror)

    def test_bool_counter_and_stale_pin_are_untrusted(self):
        obj = source()
        obj["logs"]["debug.log"]["captured_bytes"] = True
        self.write_source(self.left, obj)
        self.write_envelope()
        self.invoke(expect=2)
        self.assertIn("missing_or_invalid_captured_bytes", self.report()["issues"])
        self.left.write_text("{}", encoding="utf-8")
        self.invoke(output=".codex-sync/stale.json", expect=2)
        stale = json.loads((self.root / ".codex-sync/stale.json").read_text())
        self.assertEqual(stale["pins"]["left"]["pin_status"], "MISMATCH")
        self.assertEqual(stale["sources"]["left"]["upstream"], {})

    def test_incomplete_capture_and_known_metadata_mismatch_coexist(self):
        obj = source(30, 40, "d")
        obj["interval_status"] = "INCOMPLETE"
        obj["analysis"]["new_error_lines"] = 3
        self.write_source(self.left, obj)
        self.write_envelope()
        self.invoke(expect=2)
        report = self.report()
        self.assertEqual(report["metadata_status"], "INCOMPLETE")
        self.assertEqual(report["sources"]["left"]["upstream"]["interval_status"], "INCOMPLETE")
        pair = report["comparison"]["logs"]["debug.log"]
        self.assertEqual(pair["declared_range_relation"], "ADJACENT")
        self.assertEqual(pair["declared_count_relation"] if "declared_count_relation" in pair else pair["reported_count_relation"], "EQUAL")
        self.assertIsNone(pair["new_error_count"])

    def test_partial_capture_keeps_numeric_relation_unknown_without_structural_failure(self):
        obj = source()
        obj["interval_status"] = "INCOMPLETE"
        obj["logs"]["debug.log"]["incomplete"] = True
        obj["logs"]["debug.log"]["partial_final_line"] = True
        self.write_source(self.left, obj)
        self.write_envelope()
        self.invoke(expect=0)
        report = self.report()
        self.assertEqual(report["metadata_status"], "COMPLETE")
        self.assertEqual(report["sources"]["left"]["summary_coverage"], "PARTIAL")
        self.assertEqual(report["comparison"]["logs"]["debug.log"]["declared_range_relation"], "UNKNOWN")

    def test_pin_mismatch_emits_no_untrusted_source_projection(self):
        pin = self.pin(self.left)
        pin["bytes"] += 1
        self.write_envelope(left=pin)
        self.invoke(expect=2)
        report = self.report()
        self.assertEqual(report["pins"]["left"]["pin_status"], "MISMATCH")
        self.assertEqual(report["sources"]["left"]["upstream"], {})
        self.assertIsNone(report["comparison"]["retained_fingerprint_comparison"])

    def test_bad_envelope_has_no_output_and_collision_is_preserved(self):
        self.manifest.write_text('{"schema":"bad","left":{},"right":{}}', encoding="utf-8")
        self.invoke(expect=1)
        self.assertFalse((self.root / self.output).exists())
        target = self.root / self.output
        target.write_text("keep", encoding="utf-8")
        self.invoke(expect=1)
        self.assertEqual(target.read_text(), "keep")

    def test_duplicate_json_keys_and_outside_root_paths_fail_without_echo(self):
        self.manifest.write_text('{"schema":"checkpoint-comparison-input/1","schema":"secret-path","left":{},"right":{}}', encoding="utf-8")
        result = self.invoke(expect=1)
        self.assertFalse((self.root / self.output).exists())
        self.assertNotIn("secret-path", result.stderr)
        self.left.write_text('{"format":1,"format":1}', encoding="utf-8")
        self.write_envelope()
        self.invoke(expect=2)
        self.assertIn("invalid_source_json", self.report()["issues"])
        pin = self.pin(self.left); pin["path"] = "../outside.json"
        self.write_envelope(left=pin)
        result = self.invoke(output=".codex-sync/outside.json", expect=1)
        self.assertFalse((self.root / ".codex-sync/outside.json").exists())
        self.assertNotIn("outside.json", result.stderr)

    def test_unknown_logname_and_unselected_private_strings_are_not_exported(self):
        obj = source()
        obj["build_label"] = "SECRET BUILD SENTINEL"
        obj["payload_label"] = "PRIVATE LABEL"
        obj["limits"] = ["PRIVATE LIMIT"]
        obj["logs"]["private/path.log"] = {"state":"CAPTURED","required":False,"captured_bytes":0}
        obj["logs"]["debug.log"]["reason"] = "PRIVATE REASON"
        obj["logs"]["debug.log"]["captured_file"] = "PRIVATE_PATH_SENTINEL"
        obj["checkpoint_id"] = "not valid/private id"
        self.write_source(self.left, obj)
        self.write_envelope()
        result = self.invoke(expect=2)
        rendered = json.dumps(self.report()) + result.stdout + result.stderr
        for secret in ("PRIVATE", "private/path.log", "not valid/private id", "SECRET BUILD"):
            self.assertNotIn(secret, rendered)
        self.assertIn("unsupported_log_name", self.report()["issues"])

    def test_symlink_source_is_rejected_and_untrusted(self):
        link = self.root / "link.json"
        link.symlink_to(self.left)
        pin = self.pin(self.left); pin["path"] = "link.json"
        self.write_envelope(left=pin)
        self.invoke(expect=2)
        report = self.report()
        self.assertEqual(report["pins"]["left"]["pin_status"], "UNKNOWN")
        self.assertEqual(report["sources"]["left"]["upstream"], {})

    def test_missing_envelope_fails_cleanly_and_missing_source_stays_unknown(self):
        self.manifest.unlink()
        result = subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root), "--manifest", "input.json",
                                 "--output", self.output], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stderr.strip(), "comparison input or output failure")
        self.assertFalse((self.root / self.output).exists())
        self.write_envelope()
        pin = self.pin(self.left); pin["path"] = "missing.json"
        self.write_envelope(left=pin)
        self.invoke(expect=2)
        self.assertEqual(self.report()["pins"]["left"]["pin_status"], "UNKNOWN")

    def test_partial_fingerprint_set_cannot_be_used_as_full_overlap(self):
        obj = source(fingerprints=[{"message_sha256": "z"*64, "occurrences": 2}])
        self.write_source(self.left, obj)
        self.write_envelope()
        self.invoke(expect=2)
        report = self.report()
        self.assertIsNone(report["sources"]["left"]["fingerprints"])
        self.assertIsNone(report["comparison"]["retained_fingerprint_comparison"])

    def test_duplicate_fingerprints_make_global_overlap_unknown(self):
        obj = source(fingerprints=[{"message_sha256":"f"*64,"occurrences":1},
                                   {"message_sha256":"f"*64,"occurrences":1}])
        self.write_source(self.left, obj)
        self.write_envelope()
        self.invoke(expect=2)
        report = self.report()
        self.assertIn("duplicate_fingerprint", report["issues"])
        self.assertEqual(report["sources"]["left"]["summary_coverage"], "UNKNOWN")
        self.assertIsNone(report["comparison"]["retained_fingerprint_comparison"])

    def test_omitted_and_optional_gap_summaries_keep_scope_and_coverage(self):
        obj = source()
        obj["interval_status"] = "COMPLETE_WITH_OPTIONAL_GAPS"
        obj["expectation_status"] = "UNVERIFIED_INCOMPLETE_EVIDENCE"
        obj["logs"]["game.log"] = {"state":"MISSING", "required":False, "captured_bytes":0, "incomplete":True}
        obj["analysis"]["new_error_lines"] = 5
        obj["analysis"]["omitted_error_lines_after_summary_cap"] = 3
        self.write_source(self.left, obj)
        self.write_envelope()
        self.invoke()
        report = self.report()
        side = report["sources"]["left"]
        self.assertEqual(side["upstream"]["interval_status"], "COMPLETE_WITH_OPTIONAL_GAPS")
        self.assertEqual(side["summary_coverage"], "PARTIAL")
        self.assertEqual(side["global_summary"]["error_lines"], 5)
        self.assertEqual(side["global_summary"]["omitted_error_lines_after_summary_cap"], 3)
        self.assertEqual(side["global_summary"]["scope"], "global analyzed lines across captured logs")
        self.assertEqual(side["logs"]["debug.log"]["error_lines_scope"], "per-log analyzed lines")
        self.assertEqual(report["comparison"]["global_reported_count_relation"], "DIFFERENT")
        self.assertIsNotNone(report["comparison"]["retained_fingerprint_comparison"])

    def test_cap_of_250_retained_rows_with_zero_omitted_is_not_assumed_partial(self):
        rows = [{"message_sha256":f"{index:064x}", "occurrences":1} for index in range(250)]
        obj = source(fingerprints=rows)
        obj["analysis"]["new_error_lines"] = 250
        self.write_source(self.left, obj)
        self.write_source(self.right, obj)
        self.write_envelope()
        self.invoke()
        report = self.report()
        self.assertEqual(report["sources"]["left"]["summary_coverage"], "COMPLETE")
        self.assertEqual(len(report["comparison"]["retained_fingerprint_comparison"]), 250)

    def test_malformed_selected_types_are_finite_cli_reports(self):
        mutations = [
            ("analysis", "unique_new_errors", None), ("analysis", "unique_new_errors", {}),
            ("analysis", "unique_new_errors", True), ("analysis", "new_error_lines", True),
            ("analysis", "new_error_lines", None), ("analysis", "new_error_lines", -1),
            ("analysis", "new_error_lines", 2**63),
        ]
        for index, (section, field, value) in enumerate(mutations):
            obj = source()
            obj[section][field] = value
            self.write_source(self.left, obj)
            self.write_envelope()
            self.invoke(output=f".codex-sync/type-{index}.json", expect=2)
            report = json.loads((self.root / f".codex-sync/type-{index}.json").read_text())
            self.assertEqual(report["metadata_status"], "INCOMPLETE")
            self.assertTrue(all(isinstance(code, str) for code in report["issues"]))

    def test_envelope_size_cap_and_output_parent_symlink_are_refused(self):
        self.manifest.write_text('{"schema":"checkpoint-comparison-input/1","left":{},"right":{}}' + " "*70000,
                                 encoding="utf-8")
        self.invoke(expect=1)
        self.assertFalse((self.root / self.output).exists())
        self.write_envelope()
        parent = self.root / ".codex-sync/linked-parent"
        parent.symlink_to(self.root / ".codex-sync", target_is_directory=True)
        self.invoke(output=".codex-sync/linked-parent/refused.json", expect=1)
        self.assertFalse((self.root / ".codex-sync/refused.json").exists())

    def test_portable_public_only_copy_runs_cli(self):
        isolated = self.root / "portable"
        isolated.mkdir()
        (isolated / "scripts").mkdir(); (isolated / "tests").mkdir(); (isolated / ".codex-sync").mkdir()
        shutil.copy(SCRIPT, isolated / "scripts" / SCRIPT.name)
        helper = SCRIPT.parent / "evidence_report.py"
        shutil.copy(helper, isolated / "scripts" / helper.name)
        script_copy = isolated / "scripts" / SCRIPT.name
        # The smoke is public-only and relies on the script's unchanged helper dependency.
        left = isolated / "l.json"; right = isolated / "r.json"
        self.write_source(left, source()); self.write_source(right, source(20, 30, "e"))
        (isolated / "in.json").write_text(json.dumps({"schema":"checkpoint-comparison-input/1",
            "left": {**self.pin(left), "path":"l.json"}, "right": {**self.pin(right), "path":"r.json"}}))
        result = subprocess.run([sys.executable, str(script_copy), "--root", str(isolated), "--manifest", "in.json",
                                 "--output", ".codex-sync/o.json"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_invalid_coverage_flags_never_enable_clean_ranges_or_coverage(self):
        invalid_values = [[], {}, None, "SENTINEL_FLAG", 7]
        index = 0
        for role in ("left", "right"):
            for flag in ("incomplete", "partial_initial_line", "partial_final_line"):
                for value in invalid_values:
                    obj = source()
                    obj["logs"]["debug.log"][flag] = value
                    path = self.left if role == "left" else self.right
                    self.write_source(path, obj)
                    self.write_envelope()
                    result = self.invoke(output=f".codex-sync/invalid-flag-{index}.json", expect=2)
                    report = json.loads((self.root / f".codex-sync/invalid-flag-{index}.json").read_text())
                    pair = report["comparison"]["logs"]["debug.log"]
                    self.assertEqual(pair["declared_range_relation"], "UNKNOWN")
                    self.assertEqual(pair["declared_digest_equality"], "UNKNOWN")
                    self.assertEqual(report["sources"][role]["summary_coverage"], "UNKNOWN")
                    self.assertIsNone(pair["count_delta"])
                    self.assertEqual(report["comparison"]["event_identity"], "UNPROVEN")
                    self.assertEqual(report["comparison"]["causality"], "UNPROVEN")
                    rendered = json.dumps(report) + result.stdout + result.stderr
                    self.assertNotIn("SENTINEL_FLAG", rendered)
                    index += 1

    def test_invalid_analysis_fragment_metadata_blocks_clean_coverage(self):
        invalid_values = [[], {}, None, "SENTINEL_FRAGMENT", 7]
        for index, value in enumerate(invalid_values):
            obj = source()
            obj["analysis"]["per_log"]["debug.log"]["partial_final_line"] = value
            self.write_source(self.left, obj)
            self.write_envelope()
            result = self.invoke(output=f".codex-sync/invalid-fragment-{index}.json", expect=2)
            report = json.loads((self.root / f".codex-sync/invalid-fragment-{index}.json").read_text())
            self.assertEqual(report["sources"]["left"]["summary_coverage"], "UNKNOWN")
            self.assertEqual(report["comparison"]["logs"]["debug.log"]["declared_range_relation"], "UNKNOWN")
            self.assertNotIn("SENTINEL_FRAGMENT", json.dumps(report) + result.stdout + result.stderr)

    def test_source_parse_failures_emit_incomplete_report_and_keep_valid_peer(self):
        malformed = [
            b"{broken", b"", b'{"format":1', b"\xff", b'{"number":1e9999}',
            b"[" * 66 + b"0" + b"]" * 66,
            b'{"duplicate":1,"duplicate":2}',
            b'{"items":[' + b"0," * 1024 + b"0]}",
        ]
        for index, raw in enumerate(malformed):
            role = "left" if index % 2 == 0 else "right"
            path = self.left if role == "left" else self.right
            peer_path = self.right if role == "left" else self.left
            self.write_source(peer_path, source(20, 30, "c") if role == "left" else source())
            path.write_bytes(raw)
            self.write_envelope()
            output = f".codex-sync/source-parse-{index}.json"
            result = self.invoke(output=output, expect=2)
            report = json.loads((self.root / output).read_text())
            self.assertEqual(report["metadata_status"], "INCOMPLETE")
            self.assertIn("invalid_source_json", report["issues"])
            self.assertEqual(report["pins"][role]["pin_status"], "VERIFIED")
            self.assertEqual(report["sources"][role]["upstream"], {})
            peer = "right" if role == "left" else "left"
            self.assertEqual(report["pins"][peer]["pin_status"], "VERIFIED")
            self.assertIn("cp_1", report["sources"][peer]["upstream"]["checkpoint_id"])
            self.assertNotIn("Traceback", result.stderr)
            self.assertNotIn(str(self.root), result.stderr)

    def test_well_typed_coverage_flags_keep_false_and_true_semantics(self):
        obj = source()
        self.write_source(self.left, obj)
        self.write_envelope()
        self.invoke(output=".codex-sync/absent-flags.json")
        absent = json.loads((self.root / ".codex-sync/absent-flags.json").read_text())
        self.assertEqual(absent["sources"]["left"]["summary_coverage"], "COMPLETE")
        self.assertEqual(absent["comparison"]["logs"]["debug.log"]["declared_range_relation"], "ADJACENT")

        obj["logs"]["debug.log"]["partial_final_line"] = True
        self.write_source(self.left, obj)
        self.write_envelope()
        self.invoke(output=".codex-sync/true-flag.json")
        marked = json.loads((self.root / ".codex-sync/true-flag.json").read_text())
        self.assertEqual(marked["sources"]["left"]["summary_coverage"], "PARTIAL")
        self.assertEqual(marked["comparison"]["logs"]["debug.log"]["declared_range_relation"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
