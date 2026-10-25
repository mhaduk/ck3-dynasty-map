import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "execution_review.py"
spec = importlib.util.spec_from_file_location("execution_review", SCRIPT)
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)


def sample():
    return {"type": "post_execution_self_review", "version": 1,
            "categories": {name: "NONE" for name in review.CATEGORIES},
            "cost_hotspots": [], "metrics": {"elapsed_seconds": None, "tokens": None}}


def report_sha(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return hashlib.sha256(encoded).hexdigest()


class ExecutionReviewTests(unittest.TestCase):
    def test_all_categories_none_and_unknown_metrics_are_valid(self):
        doc = sample()
        self.assertIs(review.validate_review(doc), doc)

    def test_hotspot_cap_impacts_evidence_and_metrics_are_checked(self):
        doc = sample()
        doc["cost_hotspots"] = [{"observation": "repeated check", "impacts": ["TIME"], "evidence": ["test:case-1"]}]
        review.validate_review(doc)
        doc["cost_hotspots"] *= 6
        with self.assertRaises(ValueError): review.validate_review(doc)
        doc["cost_hotspots"] = [{"observation": "x", "impacts": ["GUESS"]}]
        with self.assertRaises(ValueError): review.validate_review(doc)

    def test_extracts_review_after_provenance_fence(self):
        provenance = {"id": "T-1", "inputs": {}, "outputs": {}}
        body = "```json\n" + json.dumps(provenance) + "\n```\n\n```json\n" + json.dumps(sample()) + "\n```\n"
        self.assertEqual(review.extract_review(body), sample())
        self.assertEqual(review.extract_review(body, after=body.index("```json")), sample())
        with self.assertRaises(ValueError): review.extract_review(body[:body.index("\n\n```json")], after=1)
        with self.assertRaises(ValueError): review.extract_review(body + body[body.index("\n\n```json"):])

    def test_inventory_deduplicates_by_explicit_semantic_key_and_attempt(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "inventory.json"
            report = sample(); sha = report_sha(report)
            args = dict(task_id="T-021-ONE", attempt=1, report_sha256=sha,
                        observations=[{"key": "slow.check", "text": "Repeated check", "metrics": {"time_seconds": None}}],
                        decision="KEEP OBSERVING", rationale="Need recurrence", evidence="result:sha256")
            first = review.ingest(path, report, **args, today="2026-01-01")
            self.assertEqual(review.ingest(path, report, **args, today="2026-01-02"), first)
            second = review.ingest(path, report, **{**args, "task_id": "T-021-TWO", "attempt": 2,
                "report_sha256": report_sha(report)}, today="2026-01-03")
            item = second["items"][0]
            self.assertEqual(item["occurrence_count"], 2)
            self.assertEqual(item["affected_tasks"], ["T-021-ONE", "T-021-TWO"])
            self.assertIsNone(item["history"][0]["metrics"]["time_seconds"])
            self.assertIsNone(item["metric_totals"]["time_seconds"]["known_total"])
            with self.assertRaises(ValueError):
                review.ingest(path, report, **{**args, "report_sha256": "0" * 64})
            with self.assertRaises(ValueError):
                review.ingest(path, report, **{**args, "decision": "NO ACTION"})

    def test_same_task_attempt_accepts_distinct_cycle_identities(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "inventory.json"
            report = sample(); sha = report_sha(report)
            args = dict(task_id="T023-EXECUTE-TEST", attempt=1, report_sha256=sha,
                        observations=[], decision="KEEP OBSERVING", rationale="cycle evidence",
                        evidence="handoff:T023-EXECUTE-TEST", today="2026-01-01")
            one = review.ingest(path, report, **args, cycle_id="R1")
            two = review.ingest(path, report, **args, cycle_id="C1")
            again = review.ingest(path, report, **args, cycle_id="R1")
            self.assertEqual(len(two["ledger"]), 2)
            self.assertEqual(again["ledger"], two["ledger"])
            self.assertEqual({x["identity"] for x in two["ledger"]},
                             {"T023-EXECUTE-TEST:1:R1", "T023-EXECUTE-TEST:1:C1"})
            with self.assertRaises(ValueError):
                review.ingest(path, report, **args, cycle_id="bad/../id")

    def test_rejects_unverified_effectiveness_without_later_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "inventory.json"
            args = dict(task_id="T-021-ONE", attempt=1, report_sha256=report_sha(sample()),
                        observations=[{"key": "opt.test", "text": "Test", "trend": "RESOLVED"}],
                        decision="NO ACTION", rationale="No evidence", evidence="result:hash")
            with self.assertRaises(ValueError): review.ingest(path, sample(), **args)

    def test_decisions_trends_links_and_metric_totals_are_explicit(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "inventory.json"
            report = sample()
            first = dict(task_id="T-021-BASE", attempt=1, report_sha256=report_sha(report),
                         observations=[{"key": "repeat.run", "text": "Measured repeated run", "metrics": {"time_seconds": 8}}],
                         decision="CREATE OPTIMIZATION TASK", rationale="Repeated with measured cost", evidence="issue:47")
            data = review.ingest(path, report, **first, today="2026-01-01")
            self.assertEqual(data["items"][0]["metric_totals"]["time_seconds"]["known_total"], 8)
            linked = {"status": "verified", "id": "T-099-OPT"}
            second = dict(task_id="T-021-OPT", attempt=1, report_sha256=report_sha(report),
                          observations=[{"key": "repeat.run", "text": "Optimization boundary recorded", "trend": "REPEATED",
                                         "linked_optimization_task": linked, "optimization_boundary": "2026-01-02",
                                         "evidence": ["result:sha256", "handoff:T021-OPT"],
                                         "execution_provenance": {"task_id": "T-021-OPT", "delegation_type": "EXECUTE", "date": "2026-01-03", "evidence": "handoff:T021-OPT"}}],
                          decision="MERGE WITH EXISTING OPTIMIZATION", rationale="Track same pattern", evidence="result:sha256")
            data = review.ingest(path, report, **second, today="2026-01-03")
            self.assertEqual(data["items"][0]["occurrence_count"], 2)
            third = dict(task_id="T-021-LATER", attempt=1, report_sha256=report_sha(report),
                         observations=[{"key": "repeat.run", "text": "Later execution evidence", "trend": "IMPROVING",
                                        "linked_optimization_task": linked, "optimization_boundary": "2026-01-02",
                                        "metrics": {"time_seconds": 4}, "execution_provenance": {"task_id": "T-021-LATER", "delegation_type": "EXECUTE", "date": "2026-01-04", "evidence": "result:later"}}],
                         decision="KEEP OBSERVING", rationale="Continue collection", evidence="result:later")
            data = review.ingest(path, report, **third, today="2026-01-04")
            self.assertEqual(data["items"][0]["trend"], "IMPROVING")
            self.assertEqual(data["items"][0]["metric_totals"]["time_seconds"]["known_total"], 12)
            self.assertEqual(data["items"][0]["linked_optimization_task"]["status"], "verified")

    def test_all_gui_decisions_and_trends_are_allowed_and_unrelated_keys_stay_separate(self):
        self.assertEqual(len(review.DECISIONS), 5)
        self.assertEqual(len(review.TRENDS), 6)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "inventory.json"
            observations = [{"key": "pattern.one", "text": "One"}, {"key": "pattern.two", "text": "Different"}]
            data = review.ingest(path, sample(), task_id="T-021-X", attempt=1, report_sha256=report_sha(sample()),
                observations=observations, decision="ESCALATE FOR REVIEW", rationale="Need GUI attention", evidence="result:sha256")
            self.assertEqual([item["key"] for item in data["items"]], ["pattern.one", "pattern.two"])

    def test_duplicate_keys_and_private_evidence_reject_without_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "inventory.json"; report = sample(); sha = report_sha(report)
            obs = {"key": "same.key", "text": "A"}
            args = dict(task_id="T-021-DUP", attempt=1, report_sha256=sha, observations=[obs, dict(obs)],
                        decision="KEEP OBSERVING", rationale="review", evidence="result:sha256")
            with self.assertRaisesRegex(ValueError, "duplicate semantic key"):
                review.ingest(path, report, **args)
            self.assertFalse(path.exists())
            for bad in ("result:%252fUsers%252falice%252fsession", "session-id:abc", "result:/private/tmp/secret"):
                with self.assertRaises(ValueError):
                    review.ingest(path, report, **{**args, "observations": [obs], "evidence": bad})
                self.assertFalse(path.exists())
            for private_text in ("Looked at %2FUsers%2Falice%2Fsession", "session_opaque-123"):
                with self.assertRaises(ValueError):
                    review.ingest(path, report, **{**args, "observations": [{"key": "safe.key", "text": private_text}]})
                self.assertFalse(path.exists())

    def test_omitted_metrics_are_unknown_and_each_observation_has_assessment(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "inventory.json"; report = sample()
            observations = [
                {"key": "metric.one", "text": "Known", "metrics": {"time_seconds": 8}, "decision": "NO ACTION", "rationale": "one"},
                {"key": "metric.two", "text": "Unknown", "decision": "KEEP OBSERVING", "rationale": "two"},
            ]
            data = review.ingest(path, report, task_id="T-021-METR", attempt=1, report_sha256=report_sha(report), observations=observations,
                decision="ESCALATE FOR REVIEW", rationale="global", evidence="result:sha256", today="2026-01-01")
            one, two = data["items"]
            self.assertEqual(set(one["history"][0]["metrics"]), set(review.METRICS))
            self.assertEqual(one["metric_totals"]["time_seconds"], {"known_total": 8, "known_count": 1, "unknown_count": 0})
            self.assertEqual(two["metric_totals"]["time_seconds"], {"known_total": None, "known_count": 0, "unknown_count": 1})
            self.assertEqual(one["history"][0]["assessment"]["decision"], "NO ACTION")
            self.assertEqual(two["history"][0]["assessment"]["rationale"], "two")
            self.assertEqual(data["ledger"][0]["rationale"], "global")

    def test_effectiveness_cannot_replace_boundary_and_needs_later_execute_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "inventory.json"; report = sample(); sha = report_sha(report)
            base = dict(task_id="T-021-BASE", attempt=1, report_sha256=sha,
                observations=[{"key": "effect.key", "text": "baseline", "linked_optimization_task": {"status": "verified", "id": "T-099-OPT"}, "optimization_boundary": "2026-01-02"}],
                decision="KEEP OBSERVING", rationale="baseline", evidence="result:base")
            review.ingest(path, report, **base, today="2026-01-03")
            before = path.read_bytes()
            bad = dict(task_id="T-021-SAME", attempt=1, report_sha256=sha,
                observations=[{"key": "effect.key", "text": "resolved", "trend": "RESOLVED", "linked_optimization_task": {"status": "verified", "id": "T-099-OPT"}, "optimization_boundary": "2026-01-01"}],
                decision="NO ACTION", rationale="resolved", evidence="result:bad")
            with self.assertRaises(ValueError): review.ingest(path, report, **bad, today="2026-01-04")
            self.assertEqual(path.read_bytes(), before)
            later_provenance = {"task_id": "T-021-LATER", "delegation_type": "EXECUTE", "date": "2026-01-05", "evidence": "handoff:T021-LATER"}
            later = dict(task_id="T-021-LATER", attempt=1, report_sha256=sha,
                observations=[{"key": "effect.key", "text": "later execution", "trend": "REPEATED", "execution_provenance": later_provenance, "evidence": ["result:later", "handoff:T021-LATER"]}],
                decision="KEEP OBSERVING", rationale="later run", evidence="result:later")
            review.ingest(path, report, **later, today="2026-01-05")
            resolved = dict(task_id="T-021-RES", attempt=1, report_sha256=sha,
                observations=[{"key": "effect.key", "text": "resolved after later run", "trend": "RESOLVED", "linked_optimization_task": {"status": "verified", "id": "T-099-OPT"}, "optimization_boundary": "2026-01-02"}],
                decision="NO ACTION", rationale="later evidence", evidence="result:resolved")
            data = review.ingest(path, report, **resolved, today="2026-01-06")
            self.assertEqual(data["items"][0]["trend"], "RESOLVED")

    def test_migration_preserves_ledger_and_history_and_malformed_inventory_is_controlled(self):
        legacy = {"version": 1, "items": [{"key": "legacy.key", "first_seen": "2026-01-01", "last_seen": "2026-01-01", "occurrence_count": 1,
            "affected_tasks": ["T-021-OLD"], "history": [{"task": "T-021-OLD", "attempt": 1, "date": "2026-01-01", "text": "old", "trend": "NEW", "metrics": {}}],
            "metric_totals": {}, "trend": "NEW", "decision": {"value": "KEEP OBSERVING", "rationale": "old decision", "evidence": [], "date": "2026-01-01"}}],
            "ledger": [{"identity": "T-021-OLD:1", "content_sha256": "a"*64, "report_sha256": "b"*64}]}
        migrated = review.migrate_inventory(legacy)
        self.assertEqual(migrated["ledger"], legacy["ledger"])
        self.assertEqual(migrated["items"][0]["history"][0]["text"], "old")
        self.assertEqual(migrated["items"][0]["display_id"], "OPT-0001")
        self.assertEqual(migrated["items"][0]["history"][0]["assessment"], None)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"; path.write_text('{broken')
            before = path.read_bytes()
            with self.assertRaisesRegex(ValueError, "malformed inventory"): review._read_inventory(path)
            self.assertEqual(path.read_bytes(), before)

    def test_empty_review_keeps_report_level_decision_rationale_and_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "inventory.json"; report = sample()
            data = review.ingest(path, report, task_id="T-021-EMPTY", attempt=1, report_sha256=report_sha(report),
                observations=[], decision="KEEP OBSERVING", rationale="Empty review still needs a triage record.",
                evidence=["result:sha256", "issue:47"], today="2026-01-01")
            self.assertEqual(data["items"], [])
            self.assertEqual(len(data["ledger"]), 1)
            self.assertEqual(data["ledger"][0]["rationale"], "Empty review still needs a triage record.")
            self.assertEqual(data["ledger"][0]["evidence"], ["result:sha256", "issue:47"])

    def test_ancestor_symlink_and_out_of_order_reports_reject_atomically(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); real = root / "real" / "sub"; real.mkdir(parents=True)
            alias = root / "alias"; alias.symlink_to(root / "real", target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "symlink component"): review._check_path(alias / "sub" / "inventory.json")
            path = root / "inventory.json"; report = sample(); sha = report_sha(report)
            args = dict(report_sha256=sha, observations=[{"key":"chron.key", "text":"x"}], decision="NO ACTION", rationale="x", evidence="result:sha256")
            review.ingest(path, report, task_id="T-021-LATE", attempt=1, **args, today="2026-02-02")
            before = path.read_bytes()
            with self.assertRaisesRegex(ValueError, "chronology"):
                review.ingest(path, report, task_id="T-021-EARLY", attempt=1, **args, today="2026-02-01")
            self.assertEqual(path.read_bytes(), before)


if __name__ == "__main__": unittest.main()
