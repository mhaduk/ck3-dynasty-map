import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from contextlib import redirect_stdout

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/gui_context.py"
spec = importlib.util.spec_from_file_location("gui_context", SCRIPT)
ctx = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ctx)


def event(kind, payload, timestamp="2026-10-24T12:00:00Z"):
    return json.dumps({"timestamp": timestamp, "type": kind, "payload": payload}, ensure_ascii=False)


class SessionParsing(unittest.TestCase):
    def test_counts_only_user_assistant_text_and_deduplicates_ids(self):
        raw = "\n".join([
            event("response_item", {"type": "message", "id": "u1", "role": "user", "content": [{"type": "input_text", "text": "hello ł"}]}),
            event("response_item", {"type": "message", "id": "u1", "role": "user", "content": [{"type": "input_text", "text": "hello ł"}]}),
            event("response_item", {"type": "message", "id": "a1", "role": "assistant", "content": [{"type": "output_text", "text": "world"}]}),
            event("response_item", {"type": "function_call", "id": "tool", "name": "secret_tool"}),
            event("token_usage_record", {"input_tokens": 999}),
            event("turn_context", {"model": "gpt", "reasoning_effort": "medium"}),
        ]).encode()
        result = ctx.inspect_session(raw)
        self.assertEqual((result["message_count"], result["character_count"]), (2, len("hello ł\nworld")))
        self.assertEqual(result["model"], "gpt")
        self.assertEqual(result["reasoning_level"], "medium")
        self.assertEqual(result["estimated_tokens"], (len("hello ł\nworld".encode()) + 3) // 4)
        self.assertNotEqual(result["estimated_tokens"], 999)

    def test_runtime_effort_field(self):
        parsed = ctx.inspect_session(event("turn_context", {"model": "gpt", "effort": "low"}).encode())
        self.assertEqual(parsed["reasoning_level"], "low")

    def test_malformed_and_conflicting_messages_rejected(self):
        with self.assertRaisesRegex(ValueError, "malformed"):
            ctx.inspect_session(b"{bad}\n")
        raw = "\n".join([
            event("response_item", {"type": "message", "id": "same", "role": "user", "content": [{"type": "input_text", "text": "a"}]}),
            event("response_item", {"type": "message", "id": "same", "role": "user", "content": [{"type": "input_text", "text": "b"}]}),
        ]).encode()
        with self.assertRaisesRegex(ValueError, "conflicting"):
            ctx.inspect_session(raw)


class Persistence(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.session = self.root / "session.jsonl"
        self.private = self.root / ".codex-sync" / "private.json"
        self.private.parent.mkdir()
        self.history = self.root / "docs/telemetry/gui-context/T-012.jsonl"

    def tearDown(self):
        self.temp.cleanup()

    def write_session(self, text, stamp="s"):
        self.session.write_text(event("response_item", {"type": "message", "id": "m" + stamp, "role": "user", "content": [{"type": "input_text", "text": text}]}) + "\n")

    def measure(self, stamp="2026-10-24T12:00:00Z", identity="opaque-1"):
        return ctx.measure(self.session, "T-012", identity, self.private, self.history, now=stamp)

    def test_append_delta_and_retry_idempotence_public_privacy(self):
        self.write_session("first")
        one = self.measure()
        self.assertIsNone(one["record"]["delta_tokens"]["value"])
        self.assertFalse(one["idempotent"])
        retry = self.measure("2026-10-24T12:01:00Z")
        self.assertTrue(retry["idempotent"])
        with self.session.open("a") as stream:
            stream.write(event("response_item", {"type": "message", "id": "m2", "role": "user", "content": [{"type": "input_text", "text": "second"}]}) + "\n")
        two = self.measure("2026-10-24T12:02:00Z")
        self.assertEqual(two["record"]["delta_tokens"]["value"], two["record"]["context_tokens"]["value"] - one["record"]["context_tokens"]["value"])
        public = self.history.read_text()
        self.assertNotIn(str(self.session), public)
        self.assertNotIn("opaque-1", public)
        self.assertNotIn("first", public)
        self.assertEqual(len(public.splitlines()), 2)

    def test_unrelated_session_and_compaction_make_delta_unknown(self):
        self.write_session("long original", "1")
        self.measure()
        self.write_session("small", "2")
        unrelated = self.measure("2026-10-24T12:01:00Z", "opaque-2")["record"]
        self.assertIsNone(unrelated["delta_tokens"]["value"])
        self.write_session("small rewritten", "3")
        compacted = self.measure("2026-10-24T12:02:00Z", "opaque-2")["record"]
        self.assertIsNone(compacted["delta_tokens"]["value"])
        self.assertIn("changed before prior cursor", compacted["delta_tokens"]["reason"])

    def test_symlink_and_malformed_history_are_refused(self):
        self.write_session("x")
        outside = self.root / "outside.json"
        outside.write_text("{}")
        link = self.root / "linked.json"
        link.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "symlink"):
            ctx.measure(link, "T-012", "id", self.private, self.history)
        docs = self.root / "docs/telemetry/gui-context"
        docs.parent.mkdir(parents=True)
        outside_dir = self.root / "outside-history"
        outside_dir.mkdir()
        docs.symlink_to(outside_dir, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            self.measure()
        docs.unlink()
        self.history.parent.mkdir(parents=True)
        self.history.write_text("not-json\n")
        with self.assertRaises(ValueError):
            self.measure()

    def test_retry_regenerates_preview_and_detects_history_tamper(self):
        self.write_session("first")
        preview = self.private.parent / "preview.json"
        one = ctx.measure(self.session, "T-012", "same", self.private, self.history, preview)
        self.assertEqual(one["record"]["handoff_sequence"], 1)
        self.assertEqual(one["record"]["measurement_provenance"], "heuristic")
        preview.unlink()
        ctx.measure(self.session, "T-012", "same", self.private, self.history, preview)
        self.assertTrue(preview.exists())
        self.history.write_text(self.history.read_text() + "{}\n")
        with self.assertRaises(ValueError):
            ctx.measure(self.session, "T-012", "same", self.private, self.history, preview)

    def test_distinct_handoffs_record_zero_growth_without_duplication(self):
        self.write_session("first")
        first = ctx.measure(self.session, "T-012", "same", self.private, self.history, handoff="T012-ONE")
        second = ctx.measure(self.session, "T-012", "same", self.private, self.history,
            now="later", handoff="T012-TWO")
        self.assertEqual(second["record"]["handoff_sequence"], 2)
        self.assertEqual(second["record"]["delta_tokens"]["value"], 0)
        retry = ctx.measure(self.session, "T-012", "same", self.private, self.history, handoff="T012-TWO")
        self.assertTrue(retry["idempotent"])

    def test_delta_tracks_session_across_parent_tasks(self):
        self.write_session("first")
        one = self.measure(identity="same")
        with self.session.open("a") as stream:
            stream.write(event("response_item", {"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": "next"}]}) + "\n")
        other = self.history.with_name("T-013.jsonl")
        two = ctx.measure(self.session, "T-013", "same", self.private, other)
        self.assertEqual(two["record"]["delta_tokens"]["value"], two["record"]["context_tokens"]["value"] - one["record"]["context_tokens"]["value"])

    def test_preview_cannot_overwrite_input(self):
        self.write_session("first")
        original = self.session.read_bytes()
        with self.assertRaisesRegex(ValueError, "alias"):
            ctx.measure(self.session, "T-012", "same", self.private, self.history, self.session)
        self.assertEqual(self.session.read_bytes(), original)

    def test_published_ref_is_explicit_and_safe(self):
        self.write_session("first")
        preview = self.private.parent / "preview.json"
        ctx.measure(self.session, "T-012", "same", self.private, self.history, preview,
            repository_ref="research/native-menu-alternative")
        self.assertIn("/blob/research/native-menu-alternative/", json.loads(preview.read_text())["history_url"])
        with self.assertRaises(ValueError):
            ctx.measure(self.session, "T-012", "same", self.private, self.history, repository_ref="../private")

    def test_session_size_is_bounded(self):
        with self.assertRaisesRegex(ValueError, "bounded read"):
            ctx.inspect_session(b"x" * (ctx.MAX_SESSION_BYTES + 1))

    def test_timing_pair_is_retained_once_from_completed_metadata(self):
        task_dir = self.root / ".codex-sync/tasks/T-009-EXECUTE-20261024-01"
        task_dir.mkdir(parents=True)
        (task_dir / "CLI_TASK.md").write_text("Estimated CLI time: 10–20 minutes (prior-based); frozen plan: 3 steps.\n")
        (task_dir / "STATUS.json").write_text(json.dumps({
            "id": "T-009-EXECUTE-20261024-01", "status": "COMPLETED", "attempt": 1,
            "claimed_at": "2026-10-24T12:00:00+00:00", "completed_at": "2026-10-24T12:12:00+00:00",
        }))
        calibration = (self.root / ".codex-sync/calibration.json").resolve()
        one = ctx.record_timing_pair(self.root, "T-009-EXECUTE-20261024-01", calibration)
        self.assertEqual(one["pair"]["original_estimate_range_minutes"], [10, 20])
        self.assertEqual(one["pair"]["claim_to_complete_elapsed_minutes"], 12)
        self.assertEqual(one["pair"]["use"], "candidate pair")
        self.assertTrue(ctx.record_timing_pair(self.root, "T-009-EXECUTE-20261024-01", calibration)["idempotent"])
        marked = ctx.mark_timing_pair_eligible(calibration, "T-009-EXECUTE-20261024-01", "Comparable bounded file tooling", self.root)
        self.assertEqual(marked["comparable_pairs"], 1)
        self.assertEqual(len(json.loads(calibration.read_text())["samples"]), 1)

    def test_calibration_uses_prior_until_three_comparable_pairs(self):
        prior = ctx.calibrated_estimate(15, 25, [])
        self.assertEqual(prior["range_minutes"], [5, 13])
        self.assertIn("prior", prior["basis"])
        samples = [
            {"use": "eligible pair", "original_estimate_range_minutes": [10, 20], "claim_to_complete_elapsed_minutes": 6},
            {"use": "eligible pair", "original_estimate_range_minutes": [20, 40], "claim_to_complete_elapsed_minutes": 15},
            {"use": "eligible pair", "original_estimate_range_minutes": [5, 15], "claim_to_complete_elapsed_minutes": 5},
        ]
        measured = ctx.calibrated_estimate(30, 60, samples)
        self.assertEqual(measured["range_minutes"], [15, 30])
        self.assertEqual(measured["pairs_used"], 3)
        self.assertEqual(measured["observed_multiplier_range"], [0.4, 0.5])

    def test_estimate_command_includes_frozen_step_count_or_no_plan(self):
        calibration = self.root / ".codex-sync/calibration.json"
        calibration.write_text(json.dumps({"samples": []}))
        output = io.StringIO()
        with redirect_stdout(output):
            code = ctx.main(["--repo", str(self.root), "--estimate-min", "15", "--estimate-max", "25", "--steps", "5", "--calibration", str(calibration)])
        self.assertEqual(code, 0)
        self.assertIn("~5–13 minutes", json.loads(output.getvalue())["formatted"])
        self.assertIn("5 planned steps", json.loads(output.getvalue())["formatted"])
        output = io.StringIO()
        with redirect_stdout(output):
            code = ctx.main(["--repo", str(self.root), "--estimate-min", "15", "--estimate-max", "25", "--calibration", str(calibration)])
        self.assertEqual(code, 0)
        self.assertTrue(json.loads(output.getvalue())["formatted"].endswith("no plan"))
        self.assertEqual(json.loads(output.getvalue())["range_minutes"], [15, 25])


if __name__ == "__main__":
    unittest.main()
