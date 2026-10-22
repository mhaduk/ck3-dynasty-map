import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "ck3_log_delta.py"
SPEC = importlib.util.spec_from_file_location("ck3_log_delta", SCRIPT)
HELPER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HELPER)


class LogDeltaTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.logs = self.root / "logs"
        self.logs.mkdir()
        self.log = self.logs / "debug.log"
        self.log.write_bytes(b"historic\n")
        self.base = self.root / "baseline.json"

    def tearDown(self):
        self.temp.cleanup()

    def invoke(self, *args, ok=True):
        import subprocess
        import sys
        result = subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True)
        if ok:
            self.assertEqual(result.returncode, 0, result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0)
        return result

    def baseline(self, *extra):
        self.invoke("baseline", "--file", self.log, "--output", self.base, "--payload-label", "fixture", *extra)

    def capture(self, name="run", *extra):
        out = self.root / name
        result = self.invoke("delta", "--baseline", self.base, "--output-dir", out, *extra)
        return out, result

    def manifest(self, out):
        return json.loads((out / "manifest.json").read_text())

    def test_repeated_errors_markers_chain_and_sources_are_preserved(self):
        self.baseline()
        original = self.log.read_bytes()
        self.log.write_bytes(original + b"[12] ERROR: same issue\n[13] ERROR: same issue\nBEGIN\nWRITE_RETURNED\nEND\n")
        spec = self.root / "spec.json"
        spec.write_text(json.dumps({"markers": [{"name": "write", "literal": "WRITE_RETURNED", "expected": 1}],
                                    "chains": [{"name": "write receipt", "begin": "BEGIN", "end": "END"}]}))
        out, result = self.capture("good", "--spec", spec)
        data = self.manifest(out)
        self.assertIn("interval: COMPLETE", result.stdout)
        self.assertEqual(data["analysis"]["unique_new_errors"][0]["occurrences"], 2)
        self.assertEqual(data["analysis"]["chains"][0]["pairs"], 1)
        self.assertEqual(self.log.read_bytes(), original + b"[12] ERROR: same issue\n[13] ERROR: same issue\nBEGIN\nWRITE_RETURNED\nEND\n")

    def test_zero_delta_is_complete_and_does_not_rewrite_baseline(self):
        self.baseline()
        base_bytes = self.base.read_bytes()
        out, result = self.capture()
        self.assertIn("interval: COMPLETE", result.stdout)
        self.assertEqual(self.manifest(out)["logs"]["debug.log"]["captured_bytes"], 0)
        self.assertEqual(self.base.read_bytes(), base_bytes)

    def test_missing_marker_and_incomplete_rejected_and_out_of_order_chains(self):
        self.baseline()
        self.log.write_bytes(self.log.read_bytes() + b"END\nBEGIN\nREJECT\nEND\n")
        spec = self.root / "spec.json"
        spec.write_text(json.dumps({"markers": [{"name": "missing", "literal": "NEVER", "expected": 1}],
                                    "chains": [{"name": "probe", "begin": "BEGIN", "end": "END", "reject": "REJECT"}]}))
        out, result = self.capture("uncertain", "--spec", spec)
        self.assertIn("interval: COMPLETE", result.stdout)
        self.assertIn("expectations: UNMET", result.stdout)
        chain = self.manifest(out)["analysis"]["chains"][0]
        self.assertEqual(chain["out_of_order"], 2)
        self.assertEqual(chain["rejected"], 1)
        self.assertGreaterEqual(chain["incomplete"], 1)

    def test_replacement_shrink_and_detectable_truncate_regrow_are_incomplete(self):
        self.baseline()
        other = self.logs / "replacement"
        other.write_bytes(b"historic\nnew\n")
        os.replace(other, self.log)
        out, _ = self.capture("replacement")
        self.assertEqual(self.manifest(out)["logs"]["debug.log"]["state"], "REPLACED")

        self.log.write_bytes(b"historic\n")
        self.base.unlink()
        self.baseline()
        self.log.write_bytes(b"x\n")
        out, _ = self.capture("shrink")
        self.assertEqual(self.manifest(out)["logs"]["debug.log"]["state"], "TRUNCATED")

        self.log.write_bytes(b"historic\n")
        self.base.unlink()
        self.baseline()
        self.log.write_bytes(b"rewritten\n")
        self.log.write_bytes(self.log.read_bytes() + b"regrown bytes\n")
        out, _ = self.capture("regrow")
        self.assertEqual(self.manifest(out)["logs"]["debug.log"]["state"], "BOUNDARY_CHANGED")

    def test_same_size_rewrite_at_sampled_file_head_is_detected(self):
        self.log.write_bytes(b"a" * 600)
        self.baseline()
        self.log.write_bytes(b"b" + b"a" * 599)
        out, _ = self.capture("head-rewrite")
        self.assertEqual(self.manifest(out)["logs"]["debug.log"]["state"], "BOUNDARY_CHANGED")

    def test_missing_baseline_log_and_partial_line_are_explicit(self):
        self.log.unlink()
        self.invoke("baseline", "--log-dir", self.logs, "--name", "debug.log", "--output", self.base)
        optional, result = self.capture("optional-missing")
        optional_item = self.manifest(optional)["logs"]["debug.log"]
        self.assertIn("COMPLETE_WITH_OPTIONAL_GAPS", result.stdout)
        self.assertFalse(optional_item["required"])
        self.assertTrue(optional_item["incomplete"])
        self.base.unlink()
        self.invoke("baseline", "--log-dir", self.logs, "--name", "debug.log", "--required-name", "debug.log", "--output", self.base)
        out, result = self.capture("missing")
        self.assertIn("INCOMPLETE", result.stdout)
        self.assertEqual(self.manifest(out)["logs"]["debug.log"]["state"], "MISSING")

        self.log.write_bytes(b"historic\n")
        self.base.unlink()
        self.baseline()
        self.log.write_bytes(self.log.read_bytes() + b"unfinished ERROR detail")
        out, result = self.capture("partial")
        self.assertIn("INCOMPLETE", result.stdout)
        self.assertTrue(self.manifest(out)["analysis"]["per_log"]["debug.log"]["partial_final_line"])

    def test_configured_cap_is_incomplete_and_records_only_frozen_bytes(self):
        self.baseline()
        self.log.write_bytes(self.log.read_bytes() + b"0123456789\n")
        out, result = self.capture("capped", "--max-bytes", "4")
        item = self.manifest(out)["logs"]["debug.log"]
        self.assertIn("INCOMPLETE", result.stdout)
        self.assertEqual(item["state"], "CAPPED")
        self.assertEqual(item["captured_bytes"], 4)
        self.assertEqual((out / item["captured_file"]).read_bytes(), b"0123")

    def test_error_summary_is_bounded_and_reports_omitted_lines(self):
        self.baseline()
        additions = "".join(f"ERROR: message {index}\n" for index in range(251)).encode()
        self.log.write_bytes(self.log.read_bytes() + additions)
        out, result = self.capture("summary-cap")
        analysis = self.manifest(out)["analysis"]
        self.assertEqual(len(analysis["unique_new_errors"]), 250)
        self.assertEqual(analysis["omitted_error_lines_after_summary_cap"], 1)
        self.assertIn("omitted after the 250-message summary cap: 1", result.stdout)

    def test_bytes_appended_after_frozen_boundary_wait_for_next_checkpoint(self):
        self.baseline()
        self.log.write_bytes(self.log.read_bytes() + b"captured\n")
        original_fstat = os.fstat
        appended = False

        def fstat_with_append(fd):
            nonlocal appended
            result = original_fstat(fd)
            if not appended:
                appended = True
                with self.log.open("ab") as stream:
                    stream.write(b"later\n")
            return result

        out = self.root / "frozen"
        with mock.patch.object(HELPER.os, "fstat", side_effect=fstat_with_append):
            args = type("Args", (), {"baseline": str(self.base), "output_dir": str(out), "spec": None, "max_bytes": 1000})()
            HELPER.delta(args)
        data = self.manifest(out)
        item = data["logs"]["debug.log"]
        captured = (out / item["captured_file"]).read_bytes()
        self.assertEqual(captured, b"captured\n")
        self.assertEqual(item["appended_after_boundary"], len(b"later\n"))

    def test_short_read_is_incomplete_and_does_not_claim_a_full_interval(self):
        self.baseline()
        self.log.write_bytes(self.log.read_bytes() + b"new complete line\n")
        original_fdopen = os.fdopen

        class EmptyFirstRead:
            def __init__(self, stream):
                self.stream = stream
                self.first = True

            def __enter__(self):
                return self

            def __exit__(self, *args):
                self.stream.close()

            def __getattr__(self, name):
                return getattr(self.stream, name)

            def read(self, size=-1):
                if self.first and self.stream.tell() >= len(b"historic\n"):
                    self.first = False
                    return b""
                return self.stream.read(size)

        out = self.root / "short-read"
        with mock.patch.object(HELPER.os, "fdopen", side_effect=lambda fd, mode: EmptyFirstRead(original_fdopen(fd, mode))):
            args = type("Args", (), {"baseline": str(self.base), "output_dir": str(out), "spec": None, "max_bytes": 1000})()
            HELPER.delta(args)
        item = self.manifest(out)["logs"]["debug.log"]
        self.assertEqual(item["state"], "PARTIAL_READ")
        self.assertEqual(item["captured_bytes"], 0)

    def test_error_channel_counts_keyword_free_repeats_and_full_identity(self):
        self.log = self.logs / "error.log"
        self.log.write_bytes(b"historic\n")
        self.baseline()
        prefix = "Unknown identifier " + "x" * 260
        additions = f"[12] {prefix}A\n[13] {prefix}A\n[14] {prefix}B\n".encode()
        self.log.write_bytes(self.log.read_bytes() + additions)
        out, result = self.capture("error-channel")
        data = self.manifest(out)
        self.assertEqual(data["interval_status"], "COMPLETE")
        self.assertEqual(data["observation_status"], "ERRORS_OR_REJECTIONS_OBSERVED")
        self.assertEqual(data["expectation_status"], "MET")
        self.assertNotIn("PASS", result.stdout)
        self.assertIn("do not establish clean logs", result.stdout)
        errors = data["analysis"]["unique_new_errors"]
        self.assertEqual(sorted(e["occurrences"] for e in errors), [1, 2])
        self.assertEqual(errors[0]["message"], errors[1]["message"])
        self.assertNotEqual(errors[0]["message_sha256"], errors[1]["message_sha256"])
        self.assertEqual(data["analysis"]["new_error_lines"], 3)

    def test_initial_fragment_is_preserved_but_not_parsed(self):
        self.log.write_bytes(b"historic\nER")
        self.baseline()
        baseline_bytes = self.base.read_bytes()
        self.assertFalse(json.loads(baseline_bytes)["logs"]["debug.log"]["line_boundary"])
        addition = b"ROR BEGIN END\nBEGIN END\n"
        self.log.write_bytes(self.log.read_bytes() + addition)
        source_bytes = self.log.read_bytes()
        spec = self.root / "spec.json"
        spec.write_text(json.dumps({"markers": [{"literal": "BEGIN", "expected": 2}],
                                    "chains": [{"begin": "BEGIN", "end": "END"}]}))
        out, result = self.capture("initial-fragment", "--spec", spec)
        data = self.manifest(out)
        self.assertEqual(data["interval_status"], "INCOMPLETE")
        self.assertEqual(data["expectation_status"], "UNVERIFIED_INCOMPLETE_EVIDENCE")
        item = data["logs"]["debug.log"]
        self.assertTrue(item["partial_initial_line"])
        self.assertEqual(item["start_offset"], len(b"historic\nER"))
        self.assertEqual(item["end_offset"], len(source_bytes))
        self.assertEqual((out / item["captured_file"]).read_bytes(), addition)
        info = data["analysis"]["per_log"]["debug.log"]
        self.assertEqual(info["excluded_initial_fragment_bytes"], len(b"ROR BEGIN END\n"))
        self.assertEqual(info["error_lines"], 0)
        self.assertEqual(data["analysis"]["chains"][0]["pairs"], 1)
        self.assertEqual(data["analysis"]["markers"][0]["observed"], 1)
        self.assertIn("initial fragment excluded", result.stdout)
        self.assertEqual(self.base.read_bytes(), baseline_bytes)
        self.assertEqual(self.log.read_bytes(), source_bytes)

    def test_same_line_events_follow_literal_position_order(self):
        self.baseline()
        spec = self.root / "spec.json"
        spec.write_text(json.dumps({"chains": [{"begin": "BEGIN", "end": "END", "reject": "REJECT"}]}))
        cases = [(b"END BEGIN\n", (0, 1, 0, 1)),
                 (b"BEGIN END\n", (1, 0, 0, 0)),
                 (b"BEGIN REJECT END\n", (0, 1, 1, 1)),
                 (b"BEGIN END BEGIN END\n", (2, 0, 0, 0)),
                 (b"BEGIN BEGIN END\n", (1, 1, 0, 1))]
        for index, (addition, expected) in enumerate(cases):
            with self.subTest(addition=addition):
                self.log.write_bytes(b"historic\n" + addition)
                out, result = self.capture(f"ordered-{index}", "--spec", spec)
                data = self.manifest(out)
                chain = data["analysis"]["chains"][0]
                self.assertEqual(tuple(chain[k] for k in ("pairs", "incomplete", "rejected", "out_of_order")), expected)
                self.assertEqual(data["interval_status"], "COMPLETE")
                self.assertEqual(data["expectation_status"], "MET" if expected == (expected[0], 0, 0, 0) else "UNMET")

    def test_overlapping_chain_occurrences_are_explicitly_refused(self):
        self.baseline()
        for index, (text, begin, end) in enumerate([("BEGIN END", "BEGIN", "BEGIN"),
                                                    ("ABABA END", "ABA", "END"),
                                                    ("BEGIN END", "BEGIN", "GIN")]):
            self.log.write_bytes(b"historic\n" + text.encode() + b"\n")
            spec = self.root / "spec.json"
            spec.write_text(json.dumps({"chains": [{"begin": begin, "end": end}]}))
            result = self.invoke("delta", "--baseline", self.base, "--output-dir", self.root / f"overlap-{index}", "--spec", spec, ok=False)
            self.assertIn("ambiguous overlapping chain literals", result.stderr)

    def test_refuses_existing_output_and_symlink_source_or_destination(self):
        self.baseline()
        out, _ = self.capture("exists")
        self.invoke("delta", "--baseline", self.base, "--output-dir", out, ok=False)
        self.invoke("baseline", "--file", self.log, "--output", self.base, ok=False)
        self.invoke("baseline", "--file", self.log, "--output", self.logs / "baseline.json", ok=False)
        self.invoke("delta", "--baseline", self.base, "--output-dir", self.logs / "checkpoint", ok=False)
        self.invoke("baseline", "--log-dir", self.logs, "--name", "debug.log", "--required-name", "missing.log", "--output", self.root / "bad-required.json", ok=False)
        link = self.root / "link.log"
        link.symlink_to(self.log)
        self.invoke("baseline", "--file", link, "--output", self.root / "linked.json", ok=False)
        linked_dir = self.root / "linked-out"
        linked_dir.symlink_to(self.root, target_is_directory=True)
        self.invoke("delta", "--baseline", self.base, "--output-dir", linked_dir, ok=False)


if __name__ == "__main__":
    unittest.main()
