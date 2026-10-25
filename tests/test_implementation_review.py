import importlib.util
import hashlib
import json
import concurrent.futures
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import subprocess
import sys

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "implementation_review.py"
HANDOFF = SCRIPT.with_name("handoff.py")
spec = importlib.util.spec_from_file_location("implementation_review", SCRIPT)
review = importlib.util.module_from_spec(spec); spec.loader.exec_module(review)


def contract(budget=3):
    summary = {"plan_sha256": "0" * 64, "bullets": [
        {"ids": ["stage0"], "text": "Inspect fixture"}, {"ids": ["stage1"], "text": "Verify result"}]}
    summary["plan_sha256"] = hashlib.sha256(json.dumps({"total_steps": 2, "steps": [
        {"id": "stage0", "label": "Inspect fixture"}, {"id": "stage1", "label": "Verify result"}]}, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
    summary_hash = hashlib.sha256(json.dumps(summary, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
    return {"version": 1, "task_id": "T-023", "revision": 1,
            "execution": {"scope": "bounded synthetic task", "acceptance": "result is correct", "permissions": "offline only",
                          "invariants": "do not leave temporary root", "inputs": ["input.md"],
                          "plan_of_execution": ["Inspect fixture", "Verify result"], "plan_summary_sha256": summary_hash,
                          "executor_profile": {"requested_model": "gpt-6-luna", "requested_reasoning": "medium", "justification": "bounded fixture"},
                          "validation": ["unit test"]},
            "review": {"dimensions": list(review.REVIEW_DIMENSIONS), "budget": {"max_changed_files": 10, "max_evidence_items": 20},
                       "profile": {"requested_model": "gpt-6.1-sol", "requested_reasoning": "high", "justification": "safety"}},
            "loop": {"enabled": True, "correction_budget": budget, "budget_rationale": "GUI selected for finite correction scope", "escalation": "scope/permission conflict"}}


def classified_contract(execution_class, review_route, *, finalization="RECEIPT_ONLY", reason="bounded synthetic scenario",
                        high_reason=None, targeted_trigger=None, enabled=True, reviewer="medium"):
    value = contract(); value["version"] = 2
    value["review"]["profile"]["requested_reasoning"] = reviewer
    value["loop"].update(correction_policy="MAX_CYCLES", correction_budget=3,
                          budget_rationale="bounded synthetic correction scope")
    if not enabled:
        value["loop"].update(enabled=False, correction_budget=None, budget_rationale=None)
    value["routing"] = {"execution_class": execution_class, "review_route": review_route,
        "gui_finalization": finalization, "reason": reason, "high_reason": high_reason,
        "targeted_trigger": targeted_trigger}
    return value


TASK_ID = "T-023"


class ImplementationReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.root = Path(self.temp.name)
        (self.root / ".codex-sync").mkdir(); (self.root / "docs").mkdir()
        (self.root / "input.md").write_text("frozen input\n")
        registry = {"version": 1, "repository": "mhaduk/ck3-dynasty-map", "issues": [{
            "number": 49, "title": "T-023 — Add independent CLI review/correction loop before GUI acceptance",
            "state": "OPEN", "url": "https://github.com/mhaduk/ck3-dynasty-map/issues/49"}]}
        (self.root / "docs/task-registry.json").write_text(json.dumps(registry))
        self._create_lifecycle(TASK_ID, contract())
        self.dims = {name: "checked: synthetic evidence" for name in review.REVIEW_DIMENSIONS}

    def tearDown(self): self.temp.cleanup()

    def handoff_cli(self, *args, ok=True):
        result = subprocess.run([sys.executable, str(HANDOFF), "--root", str(self.root), *args],
            capture_output=True, text=True)
        if ok: self.assertEqual(result.returncode, 0, result.stderr)
        else: self.assertNotEqual(result.returncode, 0)
        return result

    def _create_lifecycle(self, task_id, paired_contract, initialize=True):
        self.task_id = task_id
        self.source_path = f"synthetic_source_{task_id}.py"
        self.result_path = f".codex-sync/tasks/{task_id}/CLI_RESULT.md"
        plan = {"total_steps": 2, "steps": [{"id": "stage0", "label": "Inspect fixture"}, {"id": "stage1", "label": "Verify result"}]}
        summary = {"plan_sha256": hashlib.sha256(json.dumps(plan, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest(),
                   "bullets": [{"ids": ["stage0"], "text": "Inspect fixture"}, {"ids": ["stage1"], "text": "Verify result"}]}
        task_text = "Synthetic enabled review fixture.\n\n```json\n" + json.dumps({"execution_plan": plan}) + "\n```\n\n## Execution plan summary\n\n```json\n" + json.dumps({"plan_summary": summary}) + "\n```\n"
        create = subprocess.run([sys.executable, str(HANDOFF), "--root", str(self.root), "create", task_id,
            "--parent", "T-023", "--issue", "49", "--task", task_text,
            "--check", "synthetic check", "--input", "input.md", "--owned", self.source_path, "--review-contract", json.dumps(paired_contract)],
            capture_output=True, text=True)
        self.assertEqual(create.returncode, 0, create.stderr)
        self.handoff_cli("claim", task_id, "--owner", "executor-session", "--revision", "1")
        self.task = self.root / ".codex-sync/tasks" / task_id
        for milestone in ("stage0", "stage1"):
            status = json.loads((self.task / "STATUS.json").read_text())
            self.handoff_cli("progress", task_id, "--owner", "executor-session", "--revision", str(status["revision"]), "--start", milestone)
            status = json.loads((self.task / "STATUS.json").read_text())
            self.handoff_cli("progress", task_id, "--owner", "executor-session", "--revision", str(status["revision"]), "--done", milestone)
        (self.root / self.source_path).write_text("value = 1\n")
        self.write_handoff_result()
        status = json.loads((self.task / "STATUS.json").read_text())
        self.handoff_cli("complete", task_id, "--owner", "executor-session", "--revision", str(status["revision"]))
        if initialize:
            review.initialize(self.root, task_id, paired_contract, result_path=self.result_path,
                              changed_paths=[self.source_path], executor_identity="exec")

    def write_handoff_result(self):
        status = json.loads((self.task / "STATUS.json").read_text())
        out = {rel: hashlib.sha256((self.root / rel).read_bytes()).hexdigest() for rel in status["owned"]}
        provenance = {key: status[key] for key in ("id", "parent_id", "attempt", "inputs")}; provenance["outputs"] = out
        body = "# CLI result\n\n```json\n" + json.dumps(provenance, sort_keys=True) + "\n```\n"
        body += "\n## Identity\n\nSynthetic handoff.\n\n## Result\n\n- Outcome: SUCCESS\n- Acceptance: PASS\n"
        body += "\n## Files\n\nSynthetic files.\n\n## Checks\n\n- synthetic check: PASS\n"
        body += "\n## Self-healing / agent-instruction findings\n\nNo recovery needed.\n"
        body += "\n## Permissions / Git state\n\nTemporary synthetic fixture.\n\n## GUI next step\n\nReview synthetic result.\n"
        er_spec = importlib.util.spec_from_file_location("test_execution_review", SCRIPT.with_name("execution_review.py"))
        er = importlib.util.module_from_spec(er_spec); er_spec.loader.exec_module(er)
        report = {"type": "post_execution_self_review", "version": 1,
            "categories": {name: "NONE" for name in er.CATEGORIES}, "cost_hotspots": [],
            "metrics": {"elapsed_seconds": None, "tokens": None}}
        body += "\n```json\n" + json.dumps(report) + "\n```\n"
        (self.task / "CLI_RESULT.md").write_text(body)

    def submit(self, rid, verdict="CHANGES REQUIRED", findings=None, identity=None, telemetry=None, resolutions_override=None):
        identity = identity or f"reviewer-{rid}"
        review.begin_review(self.root, self.task_id, review_id=rid,
            result_path=self.result_path, changed_paths=[self.source_path],
            reviewer_identity=identity)
        state = review.status(self.root, self.task_id)
        resolutions = None
        if state["correction_count"]:
            latest = json.loads((self.task / "IMPLEMENTATION_REVIEW.json").read_text())["reviews"][-1]
            resolutions = {f["id"]: {"status": "RESOLVED", "evidence": "independent synthetic verification"}
                           for f in latest["findings"]}
        if resolutions_override is not None:
            resolutions = resolutions_override
        return review.submit_review(self.root, self.task_id, review_id=rid, verdict=verdict,
            findings=findings if findings is not None else ([{"id": "F1", "category": "correctness", "severity": "high", "criterion": "result is correct", "evidence": "tests", "problem": "fix it", "correction_boundary": "existing scope", "status": "OPEN"}] if verdict == "CHANGES REQUIRED" else []),
            result_path=self.result_path, changed_paths=[self.source_path],
            reviewer_identity=identity, reviewer_profile=None, dimensions=self.dims, read_only_attestation=True, telemetry=telemetry,
            resolutions=resolutions,
            escalation_reason="synthetic scope conflict requiring GUI decision" if verdict == "ESCALATE TO GUI" else None)

    def fix(self, cid="C1", evidence="changed source and rerun test", source_review=None):
        current = json.loads((self.task / "IMPLEMENTATION_REVIEW.json").read_text())
        source_review = source_review or current["reviews"][-1]["id"]
        dispositions = {f["id"]: {"disposition": "FIXED", "evidence": evidence}
                        for f in current["reviews"][-1]["findings"]}
        review.authorize_correction(self.root, self.task_id, correction_id=cid, source_review=source_review,
            dispositions=dispositions, executor_identity="exec")
        value = len(current["corrections"]) + 2
        (self.root / self.source_path).write_text(f"value = {value}\n")
        self.write_handoff_result()
        for milestone in ("stage0", "stage1"):
            status = json.loads((self.task / "STATUS.json").read_text())
            self.handoff_cli("progress", self.task_id, "--owner", "executor-session", "--revision", str(status["revision"]), "--start", milestone)
            status = json.loads((self.task / "STATUS.json").read_text())
            self.handoff_cli("progress", self.task_id, "--owner", "executor-session", "--revision", str(status["revision"]), "--done", milestone)
        status = json.loads((self.task / "STATUS.json").read_text())
        self.handoff_cli("complete", self.task_id, "--owner", "executor-session", "--revision", str(status["revision"]))
        return review.correct(self.root, self.task_id, correction_id=cid, source_review=source_review,
            dispositions=dispositions, new_result_path=self.result_path, changed_paths=[self.source_path], executor_identity="exec")

    def test_explicit_budget_accepts_one_three_and_ten(self):
        for value in (1, 3, 10): self.assertEqual(review.validate_contract(contract(value))["loop"]["correction_budget"], value)
        bad = contract(); bad["loop"]["correction_budget"] = None
        with self.assertRaises(review.ReviewError): review.validate_contract(bad)

    def test_v2_explicit_finite_and_open_policies(self):
        finite = contract(11); finite["version"] = 2
        finite["loop"]["correction_policy"] = "MAX_CYCLES"
        self.assertEqual(review.validate_contract(finite)["loop"]["correction_budget"], 11)
        finite["loop"]["correction_budget"] = 101
        self.assertEqual(review.validate_contract(finite)["loop"]["correction_budget"], 101)
        opened = contract(); opened["version"] = 2
        opened["loop"].update(correction_policy="UNTIL_ACCEPTED_OR_ESCALATED", correction_budget=None)
        self.assertIsNone(review.validate_contract(opened)["loop"]["correction_budget"])
        for change in ({"correction_policy": "MAX_CYCLES", "correction_budget": None},
                       {"correction_policy": "UNTIL_ACCEPTED_OR_ESCALATED", "correction_budget": 1},
                       {"correction_policy": "UNKNOWN", "correction_budget": None}):
            invalid = json.loads(json.dumps(opened)); invalid["loop"].update(change)
            with self.assertRaises(review.ReviewError): review.validate_contract(invalid)
        invalid = json.loads(json.dumps(finite)); invalid["loop"]["correction_budget"] = True
        with self.assertRaises(review.ReviewError): review.validate_contract(invalid)

    def test_t024_routing_guards_and_legacy_compatibility(self):
        legacy = contract()
        self.assertIsNone(review.validate_contract(legacy).get("routing"))

        def routed(execution_class, route, final="RECEIPT_ONLY", *, reason="bounded deterministic task",
                   high_reason=None, trigger=None, enabled=False, reviewer="medium"):
            value = contract(); value["version"] = 2
            value["review"]["profile"]["requested_reasoning"] = reviewer
            value["loop"].update(correction_policy="MAX_CYCLES", correction_budget=3,
                                  budget_rationale="bounded fixture")
            if not enabled:
                value["loop"].update(enabled=False, correction_budget=None, budget_rationale=None)
            value["routing"] = {"execution_class": execution_class, "review_route": route,
                "gui_finalization": final, "reason": reason, "high_reason": high_reason,
                "targeted_trigger": trigger}
            return value

        mechanical = routed("MECHANICAL", "NONE")
        self.assertEqual(review.validate_contract(mechanical)["routing"]["review_route"], "NONE")
        standard = routed("STANDARD", "SOL_MEDIUM", enabled=True)
        review.validate_contract(standard)
        complex_medium = routed("COMPLEX", "SOL_MEDIUM", enabled=True)
        review.validate_contract(complex_medium)  # complexity alone stays Medium
        high = routed("COMPLEX", "SOL_HIGH", enabled=True, reviewer="high",
                      high_reason="architecture_sensitive_correctness")
        review.validate_contract(high)
        bad_high = routed("COMPLEX", "SOL_HIGH", enabled=True, reviewer="high")
        with self.assertRaisesRegex(review.ReviewError, "allowed concrete reason"):
            review.validate_contract(bad_high)
        for tier in ("xhigh", "max"):
            expensive = routed("STANDARD", "SOL_MEDIUM", enabled=True, reviewer=tier)
            with self.assertRaisesRegex(review.ReviewError, "XHigh/Max"):
                review.validate_contract(expensive)
        diagnostic = routed("DIAGNOSTIC", "DIAGNOSTIC", final="TARGETED_REVIEW",
                            trigger="validation_gap")
        review.validate_contract(diagnostic)
        with self.assertRaisesRegex(review.ReviewError, "concrete listed trigger"):
            review.validate_contract(routed("STANDARD", "SOL_MEDIUM", final="TARGETED_REVIEW", enabled=True))
        malformed = routed("STANDARD", "SOL_MEDIUM", enabled=True)
        malformed["routing"]["execution_class"] = []
        with self.assertRaises(review.ReviewError):
            review.validate_contract(malformed)

    def test_t024_operational_and_ambiguous_validation_scenarios(self):
        expected_checks = ["unit test"]
        scenarios = ["accepted implementation closeout", "install an already-approved patch",
                     "inspect bounded error.log for known project prefixes"]
        for reason in scenarios:
            mechanical = classified_contract("MECHANICAL", "NONE", reason=reason, enabled=False)
            validated = review.validate_contract(mechanical)
            self.assertEqual(validated["routing"]["review_route"], "NONE")
            self.assertEqual(validated["execution"]["validation"], expected_checks)
        diagnostic = classified_contract("DIAGNOSTIC", "DIAGNOSTIC", finalization="TARGETED_REVIEW",
            reason="contradictory runtime evidence remains unexplained", targeted_trigger="evidence_conflict", enabled=False)
        self.assertEqual(review.validate_contract(diagnostic)["routing"]["execution_class"], "DIAGNOSTIC")

    def test_t024_receipt_only_after_current_acceptance_exposes_high_reason(self):
        paired = classified_contract("COMPLEX", "SOL_HIGH",
            reason="shared behavior has difficult independent verification", reviewer="high",
            high_reason="unresolved_material_uncertainty_after_medium")
        self._create_lifecycle("T024-RECEIPT-ONLY", paired)
        self.submit("R1", verdict="ACCEPTED", identity="reviewer-receipt-only")
        receipt = review.render_final_receipt(self.root, self.task_id)
        self.assertIn("GUI finalization RECEIPT_ONLY", receipt)
        self.assertIn("High reason: Unresolved material uncertainty after medium", receipt)

    def test_v2_open_policy_has_no_numeric_exhaustion_and_reports_counters(self):
        opened = contract(); opened["version"] = 2
        opened["loop"].update(correction_policy="UNTIL_ACCEPTED_OR_ESCALATED", correction_budget=None)
        self._create_lifecycle("T023-OPEN-LOOP", opened)
        for cycle in range(1, 12):
            self.submit(f"R{cycle}", identity=f"reviewer-open-{cycle}")
            self.fix(f"C{cycle}", source_review=f"R{cycle}")
        self.submit("R12", verdict="ACCEPTED", identity="reviewer-open-final")
        state = review.status(self.root, self.task_id)
        self.assertEqual((state["correction_policy"], state["correction_limit"], state["review_count"], state["correction_count"]),
                         ("UNTIL_ACCEPTED_OR_ESCALATED", None, 12, 11))
        self.assertTrue(state["ready_for_gui"])

    def test_first_review_acceptance_is_immediately_terminal(self):
        self.submit("R1", verdict="ACCEPTED", identity="reviewer-first-accept")
        state = review.status(self.root, self.task_id)
        self.assertEqual((state["review_count"], state["correction_count"]), (1, 0))
        self.assertTrue(state["ready_for_gui"])
        before = (self.task / "IMPLEMENTATION_REVIEW.json").read_bytes()
        with self.assertRaises(review.ReviewError): self.submit("R2", verdict="ACCEPTED", identity="reviewer-second")
        self.assertEqual(before, (self.task / "IMPLEMENTATION_REVIEW.json").read_bytes())

    def test_changed_current_result_invalidates_readiness(self):
        self.submit("R1", verdict="ACCEPTED", identity="reviewer-stale-result")
        self.assertTrue(review.status(self.root, self.task_id)["ready_for_gui"])
        (self.task / "CLI_RESULT.md").write_text("stale result bytes\n")
        self.assertFalse(review.status(self.root, self.task_id)["ready_for_gui"])

    def test_finite_one_allows_final_review_then_acceptance_or_escalation(self):
        self._create_lifecycle("T023-FINITE-ONE-ACCEPT", contract(1))
        self.submit("R1", identity="reviewer-one-r1")
        self.fix("C1", source_review="R1")
        self.submit("R2", verdict="ACCEPTED", identity="reviewer-one-r2")
        self.assertTrue(review.status(self.root, self.task_id)["ready_for_gui"])
        self._create_lifecycle("T023-FINITE-ONE-ESCALATE", contract(1))
        self.submit("R1", identity="reviewer-one-e1")
        self.fix("C1", source_review="R1")
        result = self.submit("R2", verdict="CHANGES REQUIRED", identity="reviewer-one-e2")
        self.assertEqual(result["verdict"], "ESCALATE TO GUI")
        state = review.status(self.root, self.task_id)
        self.assertEqual((state["review_count"], state["correction_count"]), (2, 1))
        self.assertTrue(state["ready_for_gui"])

    def test_open_policy_explicit_escalation_is_immediate(self):
        opened = contract(); opened["version"] = 2
        opened["loop"].update(correction_policy="UNTIL_ACCEPTED_OR_ESCALATED", correction_budget=None)
        self._create_lifecycle("T023-OPEN-ESCALATE", opened)
        result = self.submit("R1", verdict="ESCALATE TO GUI", identity="reviewer-open-escalate")
        self.assertEqual(result["verdict"], "ESCALATE TO GUI")
        state = review.status(self.root, self.task_id)
        self.assertEqual((state["review_count"], state["correction_count"]), (1, 0))
        self.assertTrue(state["ready_for_gui"])
        ledger = self.task / "IMPLEMENTATION_REVIEW.json"
        before = ledger.read_bytes()
        with self.assertRaises(review.ReviewError):
            review.begin_review(self.root, self.task_id, review_id="R2", result_path=self.result_path,
                changed_paths=[self.source_path], reviewer_identity="reviewer-open-after-stop")
        self.assertEqual(before, ledger.read_bytes())

    def test_concurrent_initialization_is_serialized_and_never_resets(self):
        task_id = "T023-INIT-RACE"
        paired = contract()
        self._create_lifecycle(task_id, paired, initialize=False)
        def initialize_once():
            try:
                review.initialize(self.root, task_id, paired,
                    result_path=f".codex-sync/tasks/{task_id}/CLI_RESULT.md",
                    changed_paths=[f"synthetic_source_{task_id}.py"], executor_identity="exec")
                return "created"
            except review.ReviewError:
                return "existing"
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda _: initialize_once(), range(2)))
        self.assertEqual(sorted(results), ["created", "existing"])
        ledger = json.loads((self.root / ".codex-sync/tasks" / task_id / "IMPLEMENTATION_REVIEW.json").read_text())
        self.assertEqual(ledger["reviews"], [])

    def test_initial_executor_snapshot_blocks_scalar_substitution_before_and_after_correction(self):
        self.submit("R1", identity="reviewer-initial-1")
        state_path = self.task / "IMPLEMENTATION_REVIEW.json"
        original = json.loads(state_path.read_text())
        state_path.write_text(json.dumps({**original, "executor": {**original["executor"], "identity": "replacement"}}))
        damaged = state_path.read_bytes()
        with self.assertRaises(review.ReviewError): review.status(self.root, self.task_id)
        self.assertEqual(damaged, state_path.read_bytes())
        state_path.write_text(json.dumps(original))
        self.fix("C1", source_review="R1")
        current = json.loads(state_path.read_text())
        self.assertEqual(review.cycle_reports(self.root, self.task_id)[0]["report_sha256"],
                         current["executor_initial"]["report_sha256"])
        forged_report = {**current["executor_report"], "metrics": {"elapsed_seconds": None, "tokens": 0}}
        forged_hash = review._sha(review._canonical(forged_report))
        state_path.write_text(json.dumps({**current, "executor_report": forged_report,
            "executor_report_sha256": forged_hash}))
        damaged = state_path.read_bytes()
        with self.assertRaises(review.ReviewError): review.cycle_reports(self.root, self.task_id)
        self.assertEqual(damaged, state_path.read_bytes())
        state_path.write_text(json.dumps(current))
        current = json.loads(state_path.read_text())
        state_path.write_text(json.dumps({**current, "executor": {**current["executor"],
            "requested_profile": {"requested_model": "forged", "requested_reasoning": "low", "justification": "fixture"}}}))
        damaged = state_path.read_bytes()
        with self.assertRaises(review.ReviewError): review.status(self.root, self.task_id)
        self.assertEqual(damaged, state_path.read_bytes())
        state_path.write_text(json.dumps(current))
        result = self.submit("R2", verdict="ACCEPTED", identity="reviewer-initial-2")
        self.assertEqual(result["verdict"], "ACCEPTED")

    def test_historical_lifecycle_without_initial_snapshot_rejects_without_backfill(self):
        state_path = self.task / "IMPLEMENTATION_REVIEW.json"
        state = json.loads(state_path.read_text())
        state.pop("executor_initial")
        state.pop("executor_initial_sha256")
        state_path.write_text(json.dumps(state))
        artifact_dir = self.task / "implementation-review/executor_initial"
        artifact_dir_path = artifact_dir / "INITIAL.json"
        artifact_dir_path.unlink()
        artifact_dir.rmdir()
        before = {p.relative_to(self.task).as_posix(): p.read_bytes() for p in self.task.rglob("*") if p.is_file()}
        with self.assertRaisesRegex(review.ReviewError, "GUI migration decision"):
            review.status(self.root, self.task_id)
        after = {p.relative_to(self.task).as_posix(): p.read_bytes() for p in self.task.rglob("*") if p.is_file()}
        self.assertEqual(before, after)
        self.assertFalse(artifact_dir.exists())

    def test_dropped_outstanding_finding_rejected_then_later_repair_is_finalized(self):
        self.submit("R1", identity="reviewer-findings-1")
        self.fix("C1", source_review="R1")
        finding2 = {"id": "F2", "category": "correctness", "severity": "high", "criterion": "second criterion",
            "evidence": "tests", "problem": "second defect", "correction_boundary": "existing scope", "status": "OPEN"}
        before = (self.task / "IMPLEMENTATION_REVIEW.json").read_bytes()
        with self.assertRaisesRegex(review.ReviewError, "carry every unresolved"):
            self.submit("R2-DROP", findings=[finding2], identity="reviewer-findings-drop",
                resolutions_override={"F1": {"status": "UNRESOLVED", "evidence": "still reproduces"}})
        # Failed review submission leaves its attempt open; close it as interrupted, then retry freshly.
        review.fail_review_attempt(self.root, self.task_id, review_id="R2-DROP", reason="invalid finding package rejected")
        self.assertNotEqual(before, (self.task / "IMPLEMENTATION_REVIEW.json").read_bytes())
        carry = [{"id": "F1", "category": "correctness", "severity": "high", "criterion": "result is correct",
            "evidence": "reproduced", "problem": "still unresolved", "correction_boundary": "existing scope", "status": "OPEN"}, finding2]
        self.submit("R2", findings=carry, identity="reviewer-findings-2",
            resolutions_override={"F1": {"status": "UNRESOLVED", "evidence": "still reproduces"}})
        self.fix("C2", source_review="R2")
        accepted = self.submit("R3", verdict="ACCEPTED", identity="reviewer-findings-3")
        self.assertEqual(accepted["verdict"], "ACCEPTED")
        receipt = review.render_final_receipt(self.root, self.task_id)
        self.assertIn("Final disposition by material finding:", receipt)
        self.assertIn("- F1: RESOLVED; result is correct; evidence: independent synthetic verification", receipt)
        self.assertIn("- F2: RESOLVED; second criterion; evidence: independent synthetic verification", receipt)

    def test_begin_review_before_correction_rejects_without_writes(self):
        self.submit("R1", identity="reviewer-early-review")
        before = {p.relative_to(self.task).as_posix(): p.read_bytes() for p in self.task.rglob("*") if p.is_file()}
        with self.assertRaisesRegex(review.ReviewError, "consumed correction"):
            review.begin_review(self.root, self.task_id, review_id="R2-EARLY", result_path=self.result_path,
                changed_paths=[self.source_path], reviewer_identity="reviewer-too-early")
        after = {p.relative_to(self.task).as_posix(): p.read_bytes() for p in self.task.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_shared_bridge_after_escalation_rejects_without_any_file_writes(self):
        self.submit("R1", identity="reviewer-bridge")
        review.escalate_correction(self.root, self.task_id, source_review="R1",
            dispositions={"F1": {"disposition": "BLOCKED", "evidence": "GUI decision required"}},
            reason="Blocked for GUI decision")
        status = json.loads((self.task / "STATUS.json").read_text())
        lifecycle = json.loads((self.task / "IMPLEMENTATION_REVIEW.json").read_text())
        before = {p.relative_to(self.task).as_posix(): p.read_bytes() for p in self.task.rglob("*") if p.is_file()}
        handoff_spec = importlib.util.spec_from_file_location("handoff_bridge_negative", HANDOFF)
        handoff = importlib.util.module_from_spec(handoff_spec); handoff_spec.loader.exec_module(handoff)
        with self.assertRaises(handoff.HandoffError):
            handoff.reopen_for_implementation_correction(self.root, self.task_id,
                expected_revision=status["revision"], correction_id="C-BRIDGE", review_id="R1",
                review_sha256=lifecycle["review_artifacts"]["R1"], prior_result_sha256=lifecycle["result_sha256"],
                prior_changed_files=lifecycle["changed_files"])
        after = {p.relative_to(self.task).as_posix(): p.read_bytes() for p in self.task.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_one_two_and_three_correction_cycles_can_reach_acceptance(self):
        for count in (1, 2, 3):
            self._create_lifecycle(f"T023-ACCEPT-{count}", contract(count))
            for cycle in range(1, count + 1):
                self.submit(f"R{cycle}", identity=f"reviewer-{count}-{cycle}")
                self.fix(f"C{cycle}", source_review=f"R{cycle}")
            result = self.submit(f"R{count + 1}", verdict="ACCEPTED", identity=f"reviewer-{count}-final")
            self.assertEqual(result["verdict"], "ACCEPTED")
            self.assertEqual(review.status(self.root, self.task_id)["correction_count"], count)
            self.assertTrue(review.status(self.root, self.task_id)["ready_for_gui"])

    def test_correction_then_fresh_distinct_reviewer_acceptance(self):
        self.submit("R1", identity="reviewer-1")
        self.assertFalse(review.status(self.root, self.task_id)["ready_for_gui"])
        self.fix()
        with self.assertRaises(review.ReviewError): self.submit("R2", verdict="ACCEPTED", identity="reviewer-1")
        self.submit("R2", verdict="ACCEPTED", identity="reviewer-2")
        self.assertTrue(review.status(self.root, self.task_id)["ready_for_gui"])
        review.require_final_receipt(self.root, self.task_id)
        before = (self.task / "STATUS.json").read_bytes()
        self.handoff_cli("consume", self.task_id, "--revision", str(json.loads(before)["revision"]), "--review", "GUI accepted synthetic simulation", ok=False)
        self.assertEqual(before, (self.task / "STATUS.json").read_bytes())
        inventory = self.root / "docs/telemetry/optimization-inventory.json"
        inventory.parent.mkdir(parents=True, exist_ok=True)
        er_spec = importlib.util.spec_from_file_location("triage_execution_review", SCRIPT.with_name("execution_review.py"))
        er = importlib.util.module_from_spec(er_spec); er_spec.loader.exec_module(er)
        cycles = review.cycle_reports(self.root, self.task_id)
        for cycle in cycles:
            er.ingest(inventory, cycle["report"], task_id=self.task_id, attempt=1,
                report_sha256=cycle["report_sha256"], observations=[], decision="KEEP OBSERVING",
                rationale="synthetic full lifecycle", evidence="handoff:synthetic", cycle_id=cycle["cycle_id"])
            review.record_cycle_triage(self.root, self.task_id, cycle_id=cycle["cycle_id"], inventory_path=inventory, actor="GUI")
        final_executor = json.loads((self.task / "IMPLEMENTATION_REVIEW.json").read_text())
        er.ingest(inventory, final_executor["executor_report"], task_id=self.task_id, attempt=1,
            report_sha256=final_executor["executor_report_sha256"], observations=[], decision="KEEP OBSERVING",
            rationale="synthetic final result receipt", evidence="handoff:synthetic")
        review.require_cycle_triage(self.root, self.task_id)
        status = json.loads((self.task / "STATUS.json").read_text())
        self.handoff_cli("consume", self.task_id, "--revision", str(status["revision"]), "--review", "GUI accepted synthetic simulation")
        self.assertEqual(json.loads((self.task / "STATUS.json").read_text())["status"], "CONSUMED")
        self.assertTrue((self.task / "implementation-review/handoff-cycles/C1/MANIFEST.json").is_file())

    def test_open_policy_correction_runs_through_normal_completion_and_gui_triage(self):
        opened = contract(); opened["version"] = 2
        opened["loop"].update(correction_policy="UNTIL_ACCEPTED_OR_ESCALATED", correction_budget=None)
        self._create_lifecycle("T023-OPEN-INTEGRATED", opened)
        self.submit("R1", identity="reviewer-open-integrated-1")
        self.fix("C1", source_review="R1")
        accepted = self.submit("R2", verdict="ACCEPTED", identity="reviewer-open-integrated-2")
        self.assertEqual(accepted["verdict"], "ACCEPTED")
        inventory = self.root / "docs/telemetry/optimization-inventory.json"
        inventory.parent.mkdir(parents=True, exist_ok=True)
        er_spec = importlib.util.spec_from_file_location("open_integrated_execution_review", SCRIPT.with_name("execution_review.py"))
        er = importlib.util.module_from_spec(er_spec); er_spec.loader.exec_module(er)
        for cycle in review.cycle_reports(self.root, self.task_id):
            er.ingest(inventory, cycle["report"], task_id=self.task_id, attempt=1,
                report_sha256=cycle["report_sha256"], observations=[], decision="KEEP OBSERVING",
                rationale="synthetic open-policy lifecycle", evidence="handoff:synthetic", cycle_id=cycle["cycle_id"])
            review.record_cycle_triage(self.root, self.task_id, cycle_id=cycle["cycle_id"], inventory_path=inventory, actor="GUI")
        final_executor = json.loads((self.task / "IMPLEMENTATION_REVIEW.json").read_text())
        er.ingest(inventory, final_executor["executor_report"], task_id=self.task_id, attempt=1,
            report_sha256=final_executor["executor_report_sha256"], observations=[], decision="KEEP OBSERVING",
            rationale="synthetic final result receipt", evidence="handoff:synthetic")
        review.require_cycle_triage(self.root, self.task_id)
        status = json.loads((self.task / "STATUS.json").read_text())
        self.handoff_cli("consume", self.task_id, "--revision", str(status["revision"]), "--review", "GUI accepted synthetic open-policy simulation")
        self.assertEqual(json.loads((self.task / "STATUS.json").read_text())["status"], "CONSUMED")

    def test_executor_loss_recovery_requires_gui_and_records_continuity_break(self):
        self.submit("R1")
        current = json.loads((self.task / "IMPLEMENTATION_REVIEW.json").read_text())
        dispositions = {f["id"]: {"disposition": "FIXED", "evidence": "synthetic replacement after loss"}
                        for f in current["reviews"][-1]["findings"]}
        review.authorize_correction(self.root, self.task_id, correction_id="C-REC", source_review="R1",
            dispositions=dispositions, executor_identity="exec")
        with self.assertRaises(review.ReviewError):
            review.authorize_executor_recovery(self.root, self.task_id, correction_id="C-REC",
                new_executor_identity="exec-replacement", reason="original session unavailable", actor="CLI")
        record = review.authorize_executor_recovery(self.root, self.task_id, correction_id="C-REC",
            new_executor_identity="exec-replacement", reason="original session unavailable", actor="GUI")
        self.assertTrue(record["continuity_break"])
        (self.root / self.source_path).write_text("value = recovered\n")
        self.write_handoff_result()
        for milestone in ("stage0", "stage1"):
            status = json.loads((self.task / "STATUS.json").read_text())
            self.handoff_cli("progress", self.task_id, "--owner", "executor-session", "--revision", str(status["revision"]), "--start", milestone)
            status = json.loads((self.task / "STATUS.json").read_text())
            self.handoff_cli("progress", self.task_id, "--owner", "executor-session", "--revision", str(status["revision"]), "--done", milestone)
        status = json.loads((self.task / "STATUS.json").read_text())
        self.handoff_cli("complete", self.task_id, "--owner", "executor-session", "--revision", str(status["revision"]))
        review.correct(self.root, self.task_id, correction_id="C-REC", source_review="R1", dispositions=dispositions,
            new_result_path=self.result_path, changed_paths=[self.source_path], executor_identity="exec-replacement")
        lifecycle = json.loads((self.task / "IMPLEMENTATION_REVIEW.json").read_text())
        self.assertEqual(len(lifecycle["executor_recoveries"]), 1)

    def test_recovered_executor_identities_remain_ineligible_as_reviewers(self):
        self.submit("R1")
        current = json.loads((self.task / "IMPLEMENTATION_REVIEW.json").read_text())
        dispositions = {f["id"]: {"disposition": "FIXED", "evidence": "recovered synthetic correction"}
                        for f in current["reviews"][-1]["findings"]}
        review.authorize_correction(self.root, self.task_id, correction_id="C-REC", source_review="R1",
            dispositions=dispositions, executor_identity="exec")
        review.authorize_executor_recovery(self.root, self.task_id, correction_id="C-REC",
            new_executor_identity="exec-mid", reason="first synthetic recovery", actor="GUI")
        (self.root / self.source_path).write_text("value = recovered\n")
        self.write_handoff_result()
        for milestone in ("stage0", "stage1"):
            status = json.loads((self.task / "STATUS.json").read_text())
            self.handoff_cli("progress", self.task_id, "--owner", "executor-session", "--revision", str(status["revision"]), "--start", milestone)
            status = json.loads((self.task / "STATUS.json").read_text())
            self.handoff_cli("progress", self.task_id, "--owner", "executor-session", "--revision", str(status["revision"]), "--done", milestone)
        status = json.loads((self.task / "STATUS.json").read_text())
        self.handoff_cli("complete", self.task_id, "--owner", "executor-session", "--revision", str(status["revision"]))
        review.correct(self.root, self.task_id, correction_id="C-REC", source_review="R1", dispositions=dispositions,
            new_result_path=self.result_path, changed_paths=[self.source_path], executor_identity="exec-mid")
        self.submit("R2", identity="reviewer-2")
        current = json.loads((self.task / "IMPLEMENTATION_REVIEW.json").read_text())
        dispositions = {f["id"]: {"disposition": "FIXED", "evidence": "second recovered synthetic correction"}
                        for f in current["reviews"][-1]["findings"]}
        review.authorize_correction(self.root, self.task_id, correction_id="C-REC-2", source_review="R2",
            dispositions=dispositions, executor_identity="exec-mid")
        review.authorize_executor_recovery(self.root, self.task_id, correction_id="C-REC-2",
            new_executor_identity="exec-new", reason="second synthetic recovery", actor="GUI")
        (self.root / self.source_path).write_text("value = recovered twice\n")
        self.write_handoff_result()
        for milestone in ("stage0", "stage1"):
            status = json.loads((self.task / "STATUS.json").read_text())
            self.handoff_cli("progress", self.task_id, "--owner", "executor-session", "--revision", str(status["revision"]), "--start", milestone)
            status = json.loads((self.task / "STATUS.json").read_text())
            self.handoff_cli("progress", self.task_id, "--owner", "executor-session", "--revision", str(status["revision"]), "--done", milestone)
        status = json.loads((self.task / "STATUS.json").read_text())
        self.handoff_cli("complete", self.task_id, "--owner", "executor-session", "--revision", str(status["revision"]))
        review.correct(self.root, self.task_id, correction_id="C-REC-2", source_review="R2", dispositions=dispositions,
            new_result_path=self.result_path, changed_paths=[self.source_path], executor_identity="exec-new")
        for identity in ("exec", "exec-mid", "exec-new"):
            before = (self.task / "IMPLEMENTATION_REVIEW.json").read_bytes()
            with self.assertRaises(review.ReviewError):
                review.begin_review(self.root, self.task_id, review_id=f"blocked-{identity}", result_path=self.result_path,
                    changed_paths=[self.source_path], reviewer_identity=identity)
            self.assertEqual(before, (self.task / "IMPLEMENTATION_REVIEW.json").read_bytes())
        script = Path(review.__file__).resolve()
        before = (self.task / "IMPLEMENTATION_REVIEW.json").read_bytes()
        cli = subprocess.run([sys.executable, str(script), "--root", str(self.root), "begin-review", self.task_id,
            "blocked-cli", self.result_path, "--changed", self.source_path, "--reviewer-identity", "exec-mid"],
            text=True, capture_output=True)
        self.assertNotEqual(cli.returncode, 0)
        self.assertEqual(before, (self.task / "IMPLEMENTATION_REVIEW.json").read_bytes())
        review.begin_review(self.root, self.task_id, review_id="R-BYPASS", result_path=self.result_path,
            changed_paths=[self.source_path], reviewer_identity="fresh-reviewer")
        payload = {"review_id": "R-BYPASS", "verdict": "ACCEPTED", "findings": [],
            "result_path": self.result_path, "changed_paths": [self.source_path], "reviewer_identity": "exec",
            "dimensions": self.dims, "read_only_attestation": True}
        payload_path = self.root / "review-payload.json"; payload_path.write_text(json.dumps(payload))
        before = (self.task / "IMPLEMENTATION_REVIEW.json").read_bytes()
        cli = subprocess.run([sys.executable, str(script), "--root", str(self.root), "review", self.task_id,
            "review-payload.json"], text=True, capture_output=True)
        self.assertNotEqual(cli.returncode, 0)
        self.assertEqual(before, (self.task / "IMPLEMENTATION_REVIEW.json").read_bytes())

    def test_read_only_reviewer_stale_bytes_and_replay_rejected(self):
        with self.assertRaises(review.ReviewError):
            review.submit_review(self.root, self.task_id, review_id="R1", verdict="ACCEPTED", findings=[], result_path=self.result_path, changed_paths=[self.source_path], reviewer_identity="r", reviewer_profile=None, dimensions=self.dims, read_only_attestation=False)
        (self.root / self.source_path).write_text("tampered\n")
        with self.assertRaises(review.ReviewError): self.submit("R1", verdict="ACCEPTED")

    def test_initialization_rejects_foreign_contract_result_changed_paths_and_input_tamper(self):
        ledger = self.task / "IMPLEMENTATION_REVIEW.json"
        ledger.unlink()
        foreign = contract(); foreign["review"]["profile"]["requested_reasoning"] = "max"
        for paired, result_path, changed in (
            (foreign, self.result_path, [self.source_path]),
            (contract(), f".codex-sync/tasks/{self.task_id}/CLI_TASK.md", [self.source_path]),
            (contract(), self.result_path, []),
            (contract(), self.result_path, [self.source_path, "input.md"]),
        ):
            with self.assertRaises(review.ReviewError):
                review.initialize(self.root, self.task_id, paired, result_path=result_path, changed_paths=changed)
            self.assertFalse(ledger.exists())
        (self.root / "input.md").write_text("tampered immutable input\n")
        with self.assertRaises(review.ReviewError):
            review.initialize(self.root, self.task_id, contract(), result_path=self.result_path, changed_paths=[self.source_path])
        self.assertFalse(ledger.exists())

    def test_budget_exhaustion_escalates_and_executor_alone_never_ready(self):
        self.submit("R1")
        self.fix("C1", source_review="R1")
        self.submit("R2", verdict="CHANGES REQUIRED", identity="reviewer-2")
        self.fix("C2", source_review="R2")
        self.submit("R3", verdict="CHANGES REQUIRED", identity="reviewer-3")
        self.fix("C3", source_review="R3")
        result = self.submit("R4", verdict="CHANGES REQUIRED", identity="reviewer-4")
        self.assertEqual(result["verdict"], "ESCALATE TO GUI")
        self.assertTrue(review.status(self.root, self.task_id)["ready_for_gui"])

    def test_budget_escalation_preserves_resolved_prior_finding(self):
        self._create_lifecycle("T023-BUDGET-RESOLVED", contract(1))
        self.submit("R1", findings=[{"id": "F1", "category": "correctness", "severity": "high", "criterion": "original criterion", "evidence": "initial evidence", "problem": "fix original", "correction_boundary": "existing scope", "status": "OPEN"}])
        self.fix("C1", source_review="R1")
        new_finding = {"id": "F2", "category": "correctness", "severity": "medium", "criterion": "new criterion", "evidence": "new evidence", "problem": "new issue", "correction_boundary": "existing scope", "status": "OPEN"}
        result = self.submit("R2", findings=[new_finding], identity="reviewer-final",
            resolutions_override={"F1": {"status": "RESOLVED", "evidence": "independent retest passed"}})
        self.assertEqual(result["verdict"], "ESCALATE TO GUI")
        self.assertEqual([f["id"] for f in result["escalated_findings"]], ["F2"])
        receipt = (self.task / "IMPLEMENTATION_REVIEW_FINAL_RECEIPT.md").read_text()
        self.assertIn("F1: RESOLVED; original criterion; evidence: independent retest passed", receipt)
        self.assertIn("F2: ESCALATED; new criterion", receipt)

    def test_ten_row_handoff_has_finite_selected_budget_and_legacy_independent(self):
        paired = contract(10)
        rendered = review.render_enabled_handoff("T023-PROBE", parent_id="T-023", contract=paired, time_steps="20–60 min / 8 steps", gui_estimate="3532 tokens; 11 messages")
        self.assertEqual(sum(line.startswith("| ") for line in rendered.splitlines()) - 1, 10)
        self.assertTrue(rendered.rstrip().endswith("| Plan of execution | • Inspect fixture<br>• Verify result |"))
        opened = contract(); opened["version"] = 2
        opened["loop"].update(correction_policy="UNTIL_ACCEPTED_OR_ESCALATED", correction_budget=None)
        open_rendered = review.render_enabled_handoff("T023-PROBE", parent_id="T-023", contract=opened, time_steps="20–60 min / 8 steps", gui_estimate="3532 tokens; 11 messages")
        self.assertIn("until accepted or escalated · no numeric correction limit", open_rendered)
        self.assertEqual(sum(line.startswith("| ") for line in open_rendered.splitlines()) - 1, 10)
        with self.assertRaises(review.ReviewError): review.render_enabled_handoff("T-023", parent_id="T-023", contract=contract(0), time_steps="x", gui_estimate="y")

    def test_symlink_escape_and_invalid_verdict_rejected(self):
        outside = self.root.parent / "outside-review.txt"; outside.write_text("private")
        (self.task / "link.txt").symlink_to(outside)
        with self.assertRaises(review.ReviewError): review._safe_file(self.root, ".codex-sync/tasks/T-023/link.txt")
        artifact_path = self.task / "implementation-review/executor_initial/INITIAL.json"
        saved_artifact = artifact_path.read_bytes()
        artifact_path.unlink()
        artifact_path.symlink_to(outside)
        with self.assertRaises(review.ReviewError): review.status(self.root, self.task_id)
        artifact_path.unlink()
        artifact_path.write_bytes(saved_artifact)
        with self.assertRaises(review.ReviewError): self.submit("R1", verdict="MAYBE")

    def test_ten_cycle_budget_is_supported_and_status_requires_current_terminal_review(self):
        self._create_lifecycle("T023-TEN-CYCLE", contract(10))
        for cycle in range(1, 11):
            self.submit(f"R{cycle}", identity=f"reviewer-{cycle}")
            self.fix(f"C{cycle}", evidence="synthetic test", source_review=f"R{cycle}")
        self.assertEqual(review.status(self.root, self.task_id)["correction_count"], 10)
        self.assertFalse(review.status(self.root, self.task_id)["ready_for_gui"])
        result = self.submit("R11", verdict="CHANGES REQUIRED", identity="reviewer-11")
        self.assertEqual(result["verdict"], "ESCALATE TO GUI")
        self.assertTrue(review.status(self.root, self.task_id)["ready_for_gui"])

    def test_immutable_review_artifact_tampering_is_detected(self):
        self.submit("R1", identity="reviewer-1")
        artifact = self.task / "implementation-review/reviews/R1.json"
        artifact.write_text("{}\n")
        with self.assertRaises(review.ReviewError): review.status(self.root, self.task_id)

    def test_interrupted_artifact_projection_commit_has_explicit_exact_recovery(self):
        review.begin_review(self.root, self.task_id, review_id="R-INT", result_path=self.result_path,
            changed_paths=[self.source_path], reviewer_identity="reviewer-int")
        original = review._write_atomic
        calls = {"count": 0}
        def interrupt_second(path, data):
            calls["count"] += 1
            if calls["count"] == 2:
                raise OSError("synthetic interruption before projection")
            return original(path, data)
        with mock.patch.object(review, "_write_atomic", side_effect=interrupt_second):
            with self.assertRaises(OSError):
                review.submit_review(self.root, self.task_id, review_id="R-INT", verdict="ACCEPTED", findings=[],
                    result_path=self.result_path, changed_paths=[self.source_path], reviewer_identity="reviewer-int",
                    reviewer_profile=None, dimensions=self.dims, read_only_attestation=True)
        with self.assertRaisesRegex(review.ReviewError, "recover-transition"):
            review.status(self.root, self.task_id)
        recovered = review.recover_transition(self.root, self.task_id)
        self.assertEqual(recovered["reviews"][-1]["verdict"], "ACCEPTED")
        review.require_final_receipt(self.root, self.task_id)

    def test_mutable_projection_cannot_override_immutable_verdict(self):
        self.submit("R1", identity="reviewer-1")
        path = self.task / "IMPLEMENTATION_REVIEW.json"
        state = json.loads(path.read_text())
        state["reviews"][0]["verdict"] = "ACCEPTED"
        path.write_text(json.dumps(state))
        with self.assertRaises(review.ReviewError): review.status(self.root, self.task_id)

    def test_effective_contract_is_rechecked_against_frozen_handoff_on_every_read(self):
        state_path = self.task / "IMPLEMENTATION_REVIEW.json"
        before = state_path.read_bytes()
        state = json.loads(before)
        state["contract"]["loop"]["correction_budget"] = 10
        state["contract_sha256"] = hashlib.sha256(json.dumps(state["contract"], sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
        state_path.write_text(json.dumps(state))
        with self.assertRaisesRegex(review.ReviewError, "exact registered frozen contract"):
            review.status(self.root, self.task_id)

    def test_frozen_contract_binds_scope_acceptance_permissions_profiles_and_plan_after_review(self):
        mutations = [
            ("execution", "scope", "altered scope"),
            ("execution", "acceptance", "altered acceptance"),
            ("execution", "permissions", "altered permissions"),
            ("execution", "plan_of_execution", ["altered plan"]),
            ("execution", "executor_profile", {"requested_model": "other", "requested_reasoning": "medium", "justification": "change"}),
            ("review", "profile", {"requested_model": "other", "requested_reasoning": "high", "justification": "change"}),
        ]
        for index, (section, key, value) in enumerate(mutations):
            task_id = f"T023-CONTRACT-MUTATION-{index}"
            self._create_lifecycle(task_id, contract())
            self.submit("R1", verdict="ACCEPTED", identity=f"reviewer-contract-{index}")
            state_path = self.task / "IMPLEMENTATION_REVIEW.json"
            state = json.loads(state_path.read_text())
            state["contract"][section][key] = value
            state["contract_sha256"] = hashlib.sha256(json.dumps(state["contract"], sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
            state_path.write_text(json.dumps(state))
            with self.assertRaises(review.ReviewError): review.status(self.root, self.task_id)

    def test_projection_only_escalation_never_enables_readiness(self):
        state_path = self.task / "IMPLEMENTATION_REVIEW.json"
        state = json.loads(state_path.read_text())
        state["escalation"] = "fabricated scalar"
        state["ready_for_gui"] = True
        state_path.write_text(json.dumps(state))
        status = review.status(self.root, self.task_id)
        self.assertFalse(status["ready_for_gui"])
        self.assertIsNone(status["escalation"])

    def test_missing_event_projection_fails_closed_without_writes(self):
        self.submit("R1", identity="reviewer-event-1")
        path = self.task / "IMPLEMENTATION_REVIEW.json"
        before = json.loads(path.read_text())
        damaged = json.loads(json.dumps(before))
        damaged["reviews"].clear()
        damaged["review_artifacts"].clear()
        path.write_text(json.dumps(damaged))
        rejected = path.read_bytes()
        with self.assertRaises(review.ReviewError): review.status(self.root, self.task_id)
        self.assertEqual(rejected, path.read_bytes())

    def test_fabricated_pending_authorization_fails_closed(self):
        path = self.task / "IMPLEMENTATION_REVIEW.json"
        state = json.loads(path.read_text())
        state["pending_corrections"]["C99"] = {"id": "C99", "source_review": "R1"}
        path.write_text(json.dumps(state))
        before = path.read_bytes()
        with self.assertRaisesRegex(review.ReviewError, "not derived from current events"):
            review.status(self.root, self.task_id)
        self.assertEqual(before, path.read_bytes())

    def test_correction_package_is_single_use_and_blocked_dispositions_escalate(self):
        self.submit("R1", identity="reviewer-1")
        self.fix()
        with self.assertRaises(review.ReviewError):
            review.correct(self.root, self.task_id, correction_id="C2", source_review="R1",
                dispositions={"F1": {"disposition": "FIXED", "evidence": "already handled"}},
                new_result_path=self.result_path, changed_paths=[self.source_path], executor_identity="exec")
        with self.assertRaises(review.ReviewError):
            review.correct(self.root, self.task_id, correction_id="C3", source_review="R1",
                dispositions={"F1": {"disposition": "BLOCKED", "evidence": "blocked by invariant"}},
                new_result_path=self.result_path, changed_paths=[self.source_path], executor_identity="exec")

    def test_concurrent_distinct_correction_ids_have_one_winner(self):
        self.submit("R1", identity="reviewer-1")
        dispositions = {"F1": {"disposition": "FIXED", "evidence": "bounded concurrent fixture"}}
        def authorize(correction_id):
            try:
                review.authorize_correction(self.root, self.task_id, correction_id=correction_id,
                    source_review="R1", dispositions=dispositions, executor_identity="exec")
                return correction_id
            except review.ReviewError:
                return None
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            outcomes = list(pool.map(authorize, ("C-RACE-A", "C-RACE-B")))
        self.assertEqual(sum(value is not None for value in outcomes), 1)
        state = json.loads((self.task / "IMPLEMENTATION_REVIEW.json").read_text())
        self.assertEqual(len(state["pending_corrections"]), 1)
        self.assertEqual(len(state["correction_authorizations"]), 1)

    def test_known_identity_cannot_be_omitted_and_blocked_finding_escalates_with_evidence(self):
        with self.assertRaises(review.ReviewError):
            review.begin_review(self.root, self.task_id, review_id="R-OMIT", result_path=self.result_path,
                changed_paths=[self.source_path], reviewer_identity=None)
        self.submit("R1")
        record = review.escalate_correction(self.root, self.task_id, source_review="R1",
            dispositions={"F1": {"disposition": "BLOCKED", "evidence": "requires GUI decision"}},
            reason="Frozen invariant prevents the requested change")
        state = review.status(self.root, self.task_id)
        self.assertTrue(state["ready_for_gui"])
        self.assertIn("Frozen invariant", state["escalation"])
        self.assertEqual(record["carried_findings"][0]["id"], "F1")
        ledger = self.task / "IMPLEMENTATION_REVIEW.json"
        before = ledger.read_bytes()
        with self.assertRaises(review.ReviewError):
            review.begin_review(self.root, self.task_id, review_id="R2", result_path=self.result_path,
                changed_paths=[self.source_path], reviewer_identity="reviewer-after-escalation")
        with self.assertRaises(review.ReviewError):
            review.authorize_correction(self.root, self.task_id, correction_id="C2", source_review="R1",
                dispositions={"F1": {"disposition": "FIXED", "evidence": "after escalation"}}, executor_identity="exec")
        self.assertEqual(before, ledger.read_bytes())

    def test_repeated_regression_remains_a_review_finding_not_automatic_escalation(self):
        self.submit("R1")
        self.fix("C1", source_review="R1")
        result = self.submit("R2", identity="reviewer-2", resolutions_override={
            "F1": {"status": "REGRESSION", "evidence": "independent regression reproduction"}})
        self.assertEqual(result["verdict"], "CHANGES REQUIRED")
        self.assertEqual(result["findings"][0]["id"], "F1")
        self.assertFalse(review.status(self.root, self.task_id)["ready_for_gui"])

    def test_repeated_unresolved_finding_stays_with_executor_until_reasoned_escalation(self):
        self.submit("R1")
        self.fix("C1", source_review="R1")
        result = self.submit("R2", identity="reviewer-2", resolutions_override={
            "F1": {"status": "UNRESOLVED", "evidence": "independent check still reproduces it"}})
        self.assertEqual(result["verdict"], "CHANGES REQUIRED")
        self.assertEqual(result["findings"][0]["id"], "F1")
        self.assertFalse(review.status(self.root, self.task_id)["ready_for_gui"])

    def test_gui_can_reject_current_reviewer_acceptance(self):
        self.submit("R1", verdict="ACCEPTED", identity="reviewer-1")
        self.assertTrue(review.status(self.root, self.task_id)["ready_for_gui"])
        review.record_gui_rejection(self.root, "T-023", reason="GUI found a missing acceptance case")
        self.assertFalse(review.status(self.root, self.task_id)["ready_for_gui"])

    def test_explicit_reviewer_escalation_enables_gui_action(self):
        self.submit("R1", verdict="ESCALATE TO GUI", identity="reviewer-1")
        current = review.status(self.root, self.task_id)
        self.assertTrue(current["ready_for_gui"])
        self.assertEqual(current["escalation"], "synthetic scope conflict requiring GUI decision")

    def test_cycle_telemetry_keeps_unknowns_null_and_rejects_transcripts(self):
        valid = {"cycle_role": "reviewer", "observation": "One stale-path rejection recovered by rechecking revision.",
                 "metrics": {"elapsed_seconds": None, "tokens": None}, "usage_refs": {"T-002": None},
                 "gui_context_ref": None}
        self.assertEqual(review.validate_cycle_telemetry(valid)["metrics"]["tokens"], None)
        bad = {**valid, "observation": "full transcript follows"}
        with self.assertRaises(review.ReviewError): review.validate_cycle_telemetry(bad)
        bad_ref = {**valid, "usage_refs": {"T-002": "/Users/private/session.jsonl"}}
        with self.assertRaises(review.ReviewError): review.validate_cycle_telemetry(bad_ref)
        encoded_ref = {**valid, "gui_context_ref": "gui-context:%252FUsers%252Fprivate%252Fsession.jsonl"}
        with self.assertRaises(review.ReviewError): review.validate_cycle_telemetry(encoded_ref)
        nonfinite = {**valid, "metrics": {"elapsed_seconds": float("nan"), "tokens": None}}
        with self.assertRaises(review.ReviewError): review.validate_cycle_telemetry(nonfinite)
        self.submit("R1", verdict="ACCEPTED", identity="reviewer-1", telemetry=valid)
        # Cycle facts remain with the immutable review artifact for GUI triage;
        # this helper never opens or writes any optimization inventory.
        root, _, state = review._load(self.root, self.task_id)
        self.assertIn("R1", state["review_artifacts"])
        artifact = json.loads((self.task / "implementation-review/reviews/R1.json").read_text())
        self.assertEqual(artifact["telemetry"], valid)
        # GUI triages the factual cycle attachment through the existing T-021
        # adapter using only a disposable inventory fixture.
        er_spec = importlib.util.spec_from_file_location("cycle_execution_review", SCRIPT.with_name("execution_review.py"))
        er = importlib.util.module_from_spec(er_spec); er_spec.loader.exec_module(er)
        report = {"type": "post_execution_self_review", "version": 1,
                  "categories": {name: "NONE" for name in er.CATEGORIES},
                  "cost_hotspots": [], "metrics": {"elapsed_seconds": None, "tokens": None}}
        report_hash = review._sha(json.dumps(report, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode())
        with tempfile.TemporaryDirectory() as inventory_root:
            inventory = Path(inventory_root) / "inventory.json"
            args = {"task_id": "T023-EXECUTE-20261025-01", "attempt": 1, "report_sha256": report_hash,
                    "observations": [{"key": "t023.review.stale-path", "category": "errors_recovery",
                        "summary": "Review caught stale path use", "text": valid["observation"], "trend": "NEW",
                        "metrics": {"time_seconds": None, "tokens": None, "rework_count": None,
                                    "manual_effort": None, "reliability_events": None},
                        "decision": "KEEP OBSERVING", "rationale": "Synthetic GUI triage fixture.",
                        "evidence": ["handoff:T023-EXECUTE-20261025-01"]}],
                    "decision": "ESCALATE FOR REVIEW", "rationale": "Synthetic cycle test only.",
                    "evidence": "handoff:T023-EXECUTE-20261025-01", "today": "2026-10-25"}
            result = er.ingest(inventory, report, **args)
            again = er.ingest(inventory, report, **args)
            self.assertEqual(len(result["ledger"]), 1)
            self.assertEqual(again["ledger"], result["ledger"])

    def test_interrupted_review_attempt_is_preserved_and_retry_uses_fresh_identity(self):
        review.begin_review(self.root, self.task_id, review_id="R1", result_path=self.result_path,
                            changed_paths=[self.source_path], reviewer_identity="reviewer-1")
        review.fail_review_attempt(self.root, self.task_id, review_id="R1", reason="session interrupted")
        with self.assertRaises(review.ReviewError): self.submit("R2", verdict="ACCEPTED", identity="reviewer-1")
        self.submit("R2", verdict="ACCEPTED", identity="reviewer-2")

    def test_concurrent_same_review_claim_has_one_winner(self):
        def begin():
            try:
                review.begin_review(self.root, self.task_id, review_id="R1",
                    result_path=self.result_path, changed_paths=[self.source_path],
                    reviewer_identity="reviewer-1")
                return "won"
            except review.ReviewError:
                return "rejected"
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            outcomes = list(pool.map(lambda _: begin(), range(2)))
        self.assertCountEqual(outcomes, ["won", "rejected"])


if __name__ == "__main__": unittest.main()
