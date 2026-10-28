import json
import hashlib
import importlib.util
import threading
from unittest import mock
import os
from pathlib import Path
import subprocess
import sys
import re
import shlex
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "handoff.py"


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.temp_root = Path(self.temp.name).resolve()
        self.root = self.temp_root / "repo"
        self.root.mkdir()
        (self.root / ".codex-sync").mkdir()
        (self.root / "input.md").write_text("input-v1\n")
        (self.root / "fixture.md").write_text("fixture input\n")
        (self.root / "docs").mkdir()
        fixture = {"version": 1, "repository": "mhaduk/ck3-dynasty-map", "issues": [
            {"number": n, "title": f"{task} — Synthetic offline fixture", "state": "OPEN",
             "url": f"https://github.com/mhaduk/ck3-dynasty-map/issues/{n}"}
            for task, n in (("T-001", 23), ("T-003", 25), ("T-024", 26))]}
        (self.root / "docs/task-registry.json").write_text(json.dumps(fixture))

    def tearDown(self):
        self.temp.cleanup()

    def run_cli(self, *args, ok=True):
        if args and args[0] == "create" and "--issue" not in args:
            args = (*args, "--issue", "25" if args[args.index("--parent") + 1] == "T-003" else "23")
        result = subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root), *args], text=True, capture_output=True, timeout=15)
        if ok:
            self.assertEqual(result.returncode, 0, result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0)
        return result

    def create(self, task_id, checks=(), owned=()):
        args = ["create", task_id, "--parent", "T-001", "--task", "Do bounded work.", "--input", "input.md"]
        for path in owned:
            args += ["--owned", path]
        for check in checks:
            args += ["--check", check]
        self.run_cli(*args)
        return self.root / ".codex-sync/tasks" / task_id

    def claim(self, task_id, owner="worker-a", revision=1, ok=True):
        return self.run_cli("claim", task_id, "--owner", owner, "--revision", str(revision), ok=ok)

    def write_result(self, directory, *, identity=None, sections=True, passed=("unit suite",)):
        status = json.loads((directory / "STATUS.json").read_text())
        provenance = identity or {k: status[k] for k in ("id", "parent_id", "attempt", "inputs")}
        provenance["outputs"] = {rel: hashlib.sha256((self.root / rel).read_bytes()).hexdigest() if (self.root / rel).exists() else None for rel in status["owned"]}
        body = "# CLI result\n\n```json\n" + json.dumps(provenance, sort_keys=True) + "\n```\n"
        names = ["Identity", "Result", "Files", "Checks", "Self-healing / agent-instruction findings", "Permissions / Git state", "GUI next step"]
        if not sections:
            names.remove("Self-healing / agent-instruction findings")
        for name in names:
            body += f"\n## {name}\n\n"
            if name == "Checks":
                body += "".join(f"- {check}: PASS\n" for check in passed)
            elif name == "Result":
                body += "- Outcome: SUCCESS\n- Acceptance: PASS\n"
            elif name == "Identity":
                body += f"ID: {status['id']}; parent: {status['parent_id']}; attempt: {status['attempt']}.\n"
            elif name == "Files":
                body += "Declared outputs: " + (", ".join(status["owned"]) or "none") + ". Initial bytes remain in baseline/.\n"
            elif name == "Self-healing / agent-instruction findings":
                body += "Observation: assigned files now match the final fingerprints. Cause: authorized edits. Recovery: none needed. Outcome: ready for review. Suggestion: inspect both initial and final evidence.\n"
            elif name == "Permissions / Git state":
                body += "Isolated offline fixture only; no stage, commit, push, network or application access.\n"
            elif name == "GUI next step":
                body += "Review actual output bytes and required checks before consuming this result; parent remains active.\n"
        if "Self-review contract: execution-review/v1" in (directory / "CLI_TASK.md").read_text():
            from importlib.util import spec_from_file_location, module_from_spec
            helper_spec = spec_from_file_location("execution_review_test_helper", SCRIPT.with_name("execution_review.py"))
            helper = module_from_spec(helper_spec); helper_spec.loader.exec_module(helper)
            review = {"type": "post_execution_self_review", "version": 1,
                      "categories": {key: "NONE" for key in helper.CATEGORIES}, "cost_hotspots": [],
                      "metrics": {"elapsed_seconds": None, "tokens": None}}
            body += "\n```json\n" + json.dumps(review) + "\n```\n"
        (directory / "CLI_RESULT.md").write_text(body)

    def ingest_review(self, directory, *, decision="NO ACTION", rationale="Synthetic GUI triage"):
        helper_spec = importlib.util.spec_from_file_location("execution_review_test_ingest", SCRIPT.with_name("execution_review.py"))
        helper = importlib.util.module_from_spec(helper_spec); helper_spec.loader.exec_module(helper)
        status = self.status(directory)
        report = helper.extract_review((directory / "CLI_RESULT.md").read_text())
        sha = hashlib.sha256(json.dumps(report, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
        helper.ingest(self.root / "docs/telemetry/optimization-inventory.json", report,
                      task_id=status["id"], attempt=status["attempt"], report_sha256=sha,
                      observations=[], decision=decision, rationale=rationale, evidence="tests:test_handoff",
                      today="2026-01-01")

    def preview_snapshot(self):
        return {str(p.relative_to(self.root)): (p.lstat().st_mode, p.lstat().st_mtime_ns,
                os.readlink(p) if p.is_symlink() else p.read_bytes() if p.is_file() else None)
                for p in self.root.rglob("*")}

    def preview(self, directory, mode="commands", ok=True):
        before = self.preview_snapshot()
        result = self.run_cli("preview", directory.name, "--mode", mode, ok=ok)
        self.assertEqual(before, self.preview_snapshot())
        if not ok:
            self.assertEqual(result.stdout, "")
        return result

    def test_preview_ready_planless_quotes_owner_and_current_revision(self):
        directory = self.create("T-001-PREVIEW")
        (directory / ".status-lock").unlink()
        output = self.preview(directory).stdout
        command = shlex.split(output.splitlines()[-1])
        self.assertEqual(command[4:], ["claim", directory.name, "--owner", "<OWNER>", "--revision", "1"])
        owner = "owner with spaces ' $(touch injected) ; `false`"
        self.claim(directory.name, owner=owner)
        output = self.preview(directory).stdout
        command = shlex.split(output.splitlines()[-1])
        self.assertEqual(command[4:], ["complete", directory.name, "--owner", owner, "--revision", "2"])
        self.assertFalse((self.root / "injected").exists())

    def test_preview_planned_commands_refresh_and_stale_revision_still_fails(self):
        directory = self.planned(count=1)
        first = shlex.split(self.preview(directory).stdout.splitlines()[-1])
        self.assertEqual(first[-2:], ["--start", "stage0"])
        self.progress(directory, "--start", "stage0")
        second = shlex.split(self.preview(directory).stdout.splitlines()[-1])
        self.assertEqual(second[-4:], ["--revision", "3", "--done", "stage0"])
        self.run_cli(*first[4:], ok=False)
        self.progress(directory, "--done", "stage0")
        self.assertEqual(shlex.split(self.preview(directory).stdout.splitlines()[-1])[4], "complete")

    def test_preview_scaffold_actual_hashes_headings_and_end_to_end_completion(self):
        directory = self.create("T-001-SCAFFOLD", checks=("synthetic",), owned=("input.md", "output.txt"))
        before = self.preview(directory, "result").stdout
        blocks = [json.loads(x) for x in re.findall(r"(?ms)^```json\n(.*?)\n```", before)]
        self.assertIsNone(blocks[0]["outputs"]["output.txt"])
        self.assertIn("missing required deliverables cannot complete", before)
        self.assertNotIn("- Outcome: SUCCESS", before)
        self.assertNotIn("- Acceptance: PASS", before)
        self.claim(directory.name)
        (self.root / "input.md").write_text("modified synthetic input\n")
        (self.root / "output.txt").write_text("synthetic output\n")
        body = self.preview(directory, "result").stdout
        blocks = [json.loads(x) for x in re.findall(r"(?ms)^```json\n(.*?)\n```", body)]
        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0]["inputs"], self.status(directory)["inputs"])
        self.assertNotEqual(blocks[0]["inputs"]["input.md"], blocks[0]["outputs"]["input.md"])
        self.assertEqual(blocks[0]["outputs"]["output.txt"], hashlib.sha256(b"synthetic output\n").hexdigest())
        self.assertEqual(blocks[1]["metrics"], {"elapsed_seconds": None, "tokens": None})
        for heading in ("QUESTION / SCOPE", "FINDINGS", "EVIDENCE", "OPTIONS", "RECOMMENDATION", "UNRESOLVED / UNKNOWN", "DECISION REQUIRED"):
            self.assertIn("### " + heading, body)
        (directory / "CLI_RESULT.md").write_text(body)
        self.run_cli("complete", directory.name, "--owner", "worker-a", "--revision", "2", ok=False)
        body = body.replace("- Outcome: <FILL FROM ACTUAL EVIDENCE>", "- Outcome: SUCCESS")
        body = body.replace("- Acceptance: <FILL FROM ACTUAL EVIDENCE>", "- Acceptance: PASS")
        body = body.replace("- synthetic: <FILL FROM ACTUAL CHECK>", "- synthetic: PASS")
        body = body.replace("<FILL: factual observation or NONE after verification>", "NONE")
        body = re.sub(r"<[^>]+>", "Synthetic fixture: output bytes and rejection verified; no external operations.", body)
        (directory / "CLI_RESULT.md").write_text(body)
        (self.root / "output.txt").write_text("changed after scaffold\n")
        stale = self.run_cli("complete", directory.name, "--owner", "worker-a", "--revision", "2", ok=False)
        self.assertIn("final outputs mismatch", stale.stderr)
        (self.root / "output.txt").write_text("synthetic output\n")
        self.run_cli("complete", directory.name, "--owner", "worker-a", "--revision", "2")
        self.assertIn("gotowe " + directory.name, self.preview(directory).stdout)
        self.ingest_review(directory)
        self.run_cli("consume", directory.name, "--revision", "3", "--review", "Synthetic evidence checked.")
        self.assertIn("No action: CONSUMED", self.preview(directory).stdout)

    def test_preview_legacy_without_review_marker_has_single_json(self):
        directory = self.create("T-001-LEGACYPREVIEW")
        task = directory / "CLI_TASK.md"
        task.write_text("Legacy per-ID frozen scope.\n")
        status = self.status(directory)
        status["scope_sha256"] = hashlib.sha256(task.read_bytes()).hexdigest()
        (directory / "STATUS.json").write_text(json.dumps(status))
        self.assertEqual(self.preview(directory, "result").stdout.count("```json"), 1)

    def test_preview_rejects_unsafe_outputs_and_administration_without_writes(self):
        directory = self.create("T-001-UNSAFE", owned=("output",))
        self.claim(directory.name)
        output = self.root / "output"
        for kind in ("symlink", "directory", "fifo"):
            with self.subTest(kind=kind):
                if kind == "symlink": output.symlink_to(self.root / "missing")
                elif kind == "directory": output.mkdir()
                else: os.mkfifo(output)
                result = self.preview(directory, "result", ok=False)
                self.assertEqual(result.stdout, "")
                self.assertIn("symlink" if kind == "symlink" else "regular file", result.stderr)
                if kind == "directory": output.rmdir()
                else: output.unlink()
        ledger = directory / "IMPLEMENTATION_REVIEW.json"
        ledger.symlink_to(self.root / "missing")
        self.preview(directory, ok=False)
        ledger.unlink()
        (directory / "implementation-review").symlink_to(self.root / "missing")
        self.preview(directory, ok=False)

    def test_preview_identity_inputs_baseline_and_inventory_fail_closed(self):
        directory = self.create("T-001-CONFLICT")
        original = (directory / "STATUS.json").read_bytes()
        status = self.status(directory)
        status["id"] = "T-001-OTHER"
        (directory / "STATUS.json").write_text(json.dumps(status))
        self.preview(directory, ok=False)
        (directory / "STATUS.json").write_bytes(original)
        (self.root / "input.md").write_text("stale\n")
        self.preview(directory, ok=False)
        (self.root / "input.md").write_text("input-v1\n")
        baseline = directory / "baseline/0.bin"
        baseline.write_text("tampered\n")
        self.preview(directory, ok=False)
        baseline.write_text("input-v1\n")
        status = self.status(directory)
        status["owned"].append("docs/telemetry/optimization-inventory.json")
        (directory / "STATUS.json").write_text(json.dumps(status))
        self.assertIn("live GUI inventory", self.preview(directory, "result", ok=False).stderr)

    def test_preview_unknown_owner_interrupted_and_nonregistered(self):
        directory = self.create("T-001-PENDING")
        self.claim(directory.name)
        status = self.status(directory); status["owner"] = None
        (directory / "STATUS.json").write_text(json.dumps(status))
        self.assertIn("owner is unknown", self.preview(directory).stdout)
        (directory / ".transition.json").write_text("{}")
        self.assertIn("interrupted transition", self.preview(directory, ok=False).stderr)
        self.run_cli("preview", "T-001-NONREGISTERED", ok=False)
        self.run_cli("preview", "../../escape", ok=False)
        self.run_cli("preview", directory.name, "--output", "forbidden.md", ok=False)
        self.assertFalse((self.root / "forbidden.md").exists())

    def test_preview_enabled_ready_and_disabled_planned_in_progress(self):
        spec = importlib.util.spec_from_file_location("preview_review", SCRIPT.with_name("implementation_review.py"))
        helper = importlib.util.module_from_spec(spec); spec.loader.exec_module(helper)
        plan = self.plan(1)
        paired = self.paired_contract(helper, plan)
        summary = {"plan_sha256": self.load_helper().plan_fingerprint(plan),
                   "bullets": [{"ids": ["stage0"], "text": plan["steps"][0]["label"]}]}
        for enabled in (True, False):
            task_id = "T-003-ENABLED" if enabled else "T-003-DISABLED"
            if not enabled:
                paired["loop"].update(enabled=False, correction_budget=None, budget_rationale=None)
                paired["routing"] = {"execution_class": "MECHANICAL", "review_route": "NONE",
                                     "gui_finalization": "RECEIPT_ONLY", "reason": "synthetic read-only fixture",
                                     "high_reason": None, "targeted_trigger": None}
            self.run_cli("create", task_id, "--parent", "T-003", "--task", "Synthetic preview fixture",
                         "--input", "input.md", "--execution-plan", json.dumps(plan),
                         "--plan-summary", json.dumps(summary), "--review-contract", json.dumps(paired))
            directory = self.root / ".codex-sync/tasks" / task_id
            output = self.preview(directory).stdout
            self.assertIn("enabled" if enabled else "disabled", output)
            self.assertIn("<OWNER>", output)
            self.claim(task_id)
            self.assertIn("--start stage0", self.preview(directory).stdout)
            self.preview(directory, "result")

    def test_independent_ids_progress_and_one_claim_wins(self):
        first = self.create("T-001-A")
        second = self.create("T-001-B")
        self.claim("T-001-B", "worker-b")
        self.assertEqual(json.loads((second / "STATUS.json").read_text())["status"], "IN_PROGRESS")
        commands = [[sys.executable, str(SCRIPT), "--root", str(self.root), "claim", "T-001-A", "--owner", f"worker-{i}", "--revision", "1"] for i in (1, 2)]
        procs = [subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for cmd in commands]
        outputs = [proc.communicate() for proc in procs]
        codes = [proc.returncode for proc in procs]
        self.assertEqual(sorted(codes), [0, 2])
        status = json.loads((first / "STATUS.json").read_text())
        self.assertEqual(status["status"], "IN_PROGRESS")
        self.assertIn(status["owner"], {"worker-1", "worker-2"})

    def test_identity_owner_revision_and_input_change_are_rejected(self):
        directory = self.create("T-001-STALE")
        self.claim("T-001-STALE")
        self.run_cli("complete", "T-001-STALE", "--owner", "worker-a", "--revision", "2", ok=False)
        self.write_result(directory, identity={"id": "T-001-OTHER"})
        self.run_cli("complete", "T-001-STALE", "--owner", "worker-a", "--revision", "2", ok=False)
        self.run_cli("complete", "T-001-STALE", "--owner", "stranger", "--revision", "2", ok=False)
        self.write_result(directory)
        provenance = {k: json.loads((directory / "STATUS.json").read_text())[k] for k in ("id", "parent_id", "attempt", "inputs")}
        provenance["attempt"] += 1
        self.write_result(directory, identity=provenance)
        self.run_cli("complete", "T-001-STALE", "--owner", "worker-a", "--revision", "2", ok=False)
        self.write_result(directory)
        self.run_cli("complete", "T-001-STALE", "--owner", "worker-a", "--revision", "1", ok=False)
        (self.root / "input.md").write_text("input-v2\n")
        self.run_cli("complete", "T-001-STALE", "--owner", "worker-a", "--revision", "2", ok=False)

    def test_required_sections_and_requested_checks_gate_completion(self):
        directory = self.create("T-001-GATE", checks=("unit suite", "markdown links"))
        self.claim("T-001-GATE")
        self.write_result(directory)
        self.run_cli("complete", "T-001-GATE", "--owner", "worker-a", "--revision", "2", ok=False)
        self.write_result(directory, sections=False)
        self.run_cli("complete", "T-001-GATE", "--owner", "worker-a", "--revision", "2", ok=False)
        self.write_result(directory, passed=("unit suite", "markdown links"))
        self.run_cli("complete", "T-001-GATE", "--owner", "worker-a", "--revision", "2")
        self.run_cli("consume", "T-001-GATE", "--revision", "3", "--review", "Reviewed result and files.", ok=False)
        self.ingest_review(directory)
        (directory / "GUI_REVIEW.md").write_text("Reviewed result and files.\n")
        self.run_cli("consume", "T-001-GATE", "--revision", "3", "--review", "Reviewed result and files.")
        self.assertEqual(json.loads((directory / "STATUS.json").read_text())["status"], "CONSUMED")

    def test_new_handoffs_freeze_self_review_and_preexisting_contracts_remain_compatible(self):
        directory = self.create("T-001-REVIEW")
        self.assertIn("Self-review contract: execution-review/v1", (directory / "CLI_TASK.md").read_text())
        self.claim("T-001-REVIEW")
        self.write_result(directory)
        self.run_cli("complete", "T-001-REVIEW", "--owner", "worker-a", "--revision", "2")
        self.run_cli("consume", "T-001-REVIEW", "--revision", "3", "--review", "Reviewed result.", ok=False)
        self.ingest_review(directory)
        self.run_cli("consume", "T-001-REVIEW", "--revision", "3", "--review", "Reviewed result.")
        old = self.create("T-001-OLD", owned=("input.md",))
        task = old / "CLI_TASK.md"
        task.write_text("Do bounded work.\n")
        status = self.status(old)
        status["scope_sha256"] = hashlib.sha256(task.read_bytes()).hexdigest()
        (old / "STATUS.json").write_text(json.dumps(status))
        self.claim("T-001-OLD")
        self.write_result(old)
        self.run_cli("complete", "T-001-OLD", "--owner", "worker-a", "--revision", "2")

    def test_new_review_must_follow_provenance(self):
        directory = self.create("T-001-ORDER")
        self.claim("T-001-ORDER")
        self.write_result(directory)
        result = directory / "CLI_RESULT.md"
        body = result.read_text()
        # Move the structured review before provenance while preserving its bytes.
        opening = body.rfind("```json")
        review_fence = body[opening:]
        body = body[:opening]
        body = review_fence + "\n" + body
        result.write_text(body)
        self.run_cli("complete", "T-001-ORDER", "--owner", "worker-a", "--revision", "2", ok=False)

    def test_new_review_rejects_second_provenance_object(self):
        directory = self.create("T-001-DUP-PROVENANCE")
        self.claim("T-001-DUP-PROVENANCE")
        self.write_result(directory)
        result = directory / "CLI_RESULT.md"
        body = result.read_text()
        first = re.search(r"(?ms)^```json\n(\{.*?\})\n```[ \t]*$", body)
        self.assertIsNotNone(first)
        body = body[:first.end()] + "\n\n" + first.group(0) + "\n" + body[first.end():]
        result.write_text(body)
        self.run_cli("complete", "T-001-DUP-PROVENANCE", "--owner", "worker-a", "--revision", "2", ok=False)

    def test_invalid_ids_and_symlink_escape_are_rejected(self):
        self.run_cli("create", "../escape", "--parent", "T-001", "--task", "x", ok=False)
        outside = self.temp_root / "outside"
        outside.mkdir()
        (self.root / ".codex-sync/tasks").symlink_to(outside, target_is_directory=True)
        self.run_cli("create", "T-001-ESCAPE", "--parent", "T-001", "--task", "x", ok=False)

    def test_unsafe_input_escape_and_ambiguous_legacy_pickup(self):
        outside = self.temp_root / "outside-input"
        outside.write_text("private\n")
        (self.root / "escape.md").symlink_to(outside)
        self.run_cli("create", "T-001-LINK", "--parent", "T-001", "--task", "x", "--input", "escape.md", ok=False)
        self.create("T-001-ONE")
        self.assertEqual(self.run_cli("resolve").stdout.strip(), "T-001-ONE")
        self.create("T-001-TWO")
        self.assertIn("T-001-ONE, T-001-TWO", self.run_cli("resolve", ok=False).stderr)


    def test_retry_preserves_failed_attempt_and_no_age_theft(self):
        directory = self.create("T-001-RETRY")
        self.claim("T-001-RETRY")
        self.run_cli("claim", "T-001-RETRY", "--owner", "worker-b", "--revision", "2", ok=False)
        self.run_cli("fail", "T-001-RETRY", "--owner", "worker-a", "--revision", "2", "--reason", "interrupted")
        self.run_cli("retry", "T-001-RETRY", "--revision", "3")
        status = json.loads((directory / "STATUS.json").read_text())
        self.assertEqual((status["attempt"], status["status"]), (2, "READY"))
        archived = directory / "attempts/1/STATUS.json"
        self.assertTrue(archived.is_file())
        self.assertEqual(json.loads(archived.read_text())["status"], "FAILED")

    def test_interrupted_claim_can_be_recorded_and_explicitly_retried(self):
        directory = self.create("T-001-INTERRUPT")
        marker = directory / ".claim"
        marker.mkdir()
        (marker / "owner").write_text("worker-cut-off")
        self.run_cli("recover", "T-001-INTERRUPT", "--revision", "1", "--reason", "process stopped during claim")
        self.run_cli("retry", "T-001-INTERRUPT", "--revision", "2")
        status = json.loads((directory / "STATUS.json").read_text())
        self.assertEqual((status["status"], status["attempt"]), ("READY", 2))
        archived = json.loads((directory / "attempts/1/STATUS.json").read_text())
        self.assertEqual(archived["owner"], "worker-cut-off")



    def load_helper(self):
        spec = importlib.util.spec_from_file_location("handoff_under_test", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def invoke(self, helper, *args):
        parsed = helper.build_parser().parse_args(["--root", str(self.root), *args])
        parsed.func(parsed)

    def status(self, directory):
        return json.loads((directory / "STATUS.json").read_text())

    def snapshot(self, directory):
        files = {}
        for parent, dirs, names in os.walk(directory, followlinks=False):
            for name in dirs + names:
                path = Path(parent) / name
                rel = str(path.relative_to(directory))
                files[rel] = ("link", os.readlink(path)) if path.is_symlink() else ("dir",) if path.is_dir() else ("file", path.read_bytes())
        return files

    def test_real_edit_and_new_output_full_flow_retains_both_provenances(self):
        initial = (self.root / "input.md").read_bytes()
        directory = self.create("T-001-EDIT", checks=("unit suite",), owned=("input.md", "new.md"))
        self.assertFalse((self.root / ".codex-sync/CLI_TASK.md").exists())
        self.assertEqual(self.run_cli("resolve", "T-001-EDIT").stdout.strip(), "T-001-EDIT")
        self.run_cli("validate", "T-001-EDIT")
        self.claim("T-001-EDIT")
        (self.root / "input.md").write_text("assigned edit\n")
        (self.root / "new.md").write_text("assigned new output\n")
        self.run_cli("validate", "T-001-EDIT")
        self.write_result(directory)
        self.run_cli("complete", "T-001-EDIT", "--owner", "worker-a", "--revision", "2")
        status = self.status(directory)
        self.assertEqual(status["inputs"]["input.md"], hashlib.sha256(initial).hexdigest())
        self.assertIsNone(status["inputs"]["new.md"])
        self.assertNotEqual(status["inputs"]["input.md"], status["outputs"]["input.md"])
        self.assertEqual((directory / "baseline/0.bin").read_bytes(), initial)
        self.assertEqual(status["result_provenance"]["inputs"], status["inputs"])
        self.assertEqual(status["result_provenance"]["outputs"], status["outputs"])
        self.assertEqual(self.run_cli("resolve", "--receipt").stdout.strip(), "T-001-EDIT")
        self.ingest_review(directory)
        self.run_cli("consume", "T-001-EDIT", "--revision", "3", "--review", "Reviewed actual edit and initial/final evidence.")
        self.run_cli("validate", "T-001-EDIT")
        self.assertEqual(self.status(directory)["status"], "CONSUMED")

    def test_owned_and_immutable_drift_before_claim_have_no_claim_side_effect(self):
        for owned in ((), ("input.md",)):
            with self.subTest(owned=owned):
                task_id = "T-001-OWNED" if owned else "T-001-IMMUTABLE"
                (self.root / "input.md").write_text("input-v1\n")
                directory = self.create(task_id, owned=owned)
                (self.root / "input.md").write_text("external drift\n")
                before = self.snapshot(directory)
                self.assertIn("fingerprint changed", self.claim(task_id, ok=False).stderr)
                self.assertEqual(before, self.snapshot(directory))
                self.run_cli("validate", task_id, ok=False)

    def test_immutable_edit_during_assigned_work_blocks_completion(self):
        (self.root / "source.md").write_text("initial\n")
        directory = self.create("T-001-MIXED", owned=("source.md",))
        self.claim("T-001-MIXED")
        (self.root / "source.md").write_text("allowed edit\n")
        (self.root / "input.md").write_text("forbidden dependency drift\n")
        self.write_result(directory)
        self.assertIn("fingerprint changed", self.run_cli("complete", "T-001-MIXED", "--owner", "worker-a", "--revision", "2", ok=False).stderr)
        self.assertEqual(self.status(directory)["status"], "IN_PROGRESS")

    def test_frozen_scope_before_and_after_claim_blocks_success(self):
        for after_claim in (False, True):
            with self.subTest(after_claim=after_claim):
                task_id = "T-001-AFTER" if after_claim else "T-001-BEFORE"
                directory = self.create(task_id)
                if after_claim:
                    self.claim(task_id)
                (directory / "CLI_TASK.md").write_text("changed scope\n")
                before = self.snapshot(directory)
                self.assertIn("frozen task", self.run_cli("validate", task_id, ok=False).stderr)
                if after_claim:
                    self.write_result(directory)
                    self.assertIn("frozen task", self.run_cli("complete", task_id, "--owner", "worker-a", "--revision", "2", ok=False).stderr)
                    # Failure must still be reportable after the contract violation.
                    self.run_cli("fail", task_id, "--owner", "worker-a", "--revision", "2", "--reason", "scope changed")
                else:
                    self.assertIn("frozen task", self.claim(task_id, ok=False).stderr)
                    self.assertEqual(before, self.snapshot(directory))

    def test_retry_rejects_stale_revision_after_controlled_valid_fail(self):
        directory = self.create("T-001-RACE")
        self.claim("T-001-RACE")
        observed = self.status(directory)
        self.assertEqual(observed["revision"], 2)
        helper = self.load_helper()
        at_lock, release = threading.Event(), threading.Event()
        original_lock = helper.locked
        from contextlib import contextmanager
        @contextmanager
        def delayed_lock(root, task):
            at_lock.set()
            if not release.wait(10):
                raise AssertionError("race test did not release retry")
            with original_lock(root, task):
                yield
        errors = []
        def retry():
            try:
                self.invoke(helper, "retry", "T-001-RACE", "--revision", str(observed["revision"]))
            except Exception as exc:
                errors.append(exc)
        with mock.patch.object(helper, "locked", delayed_lock):
            thread = threading.Thread(target=retry)
            thread.start()
            self.assertTrue(at_lock.wait(10))
            self.run_cli("fail", "T-001-RACE", "--owner", "worker-a", "--revision", "2", "--reason", "valid newer failure")
            newer = self.snapshot(directory)
            release.set()
            thread.join(10)
        self.assertFalse(thread.is_alive())
        self.assertEqual(len(errors), 1)
        self.assertIn("stale status revision", str(errors[0]))
        self.assertEqual(newer, self.snapshot(directory))
        self.assertEqual(self.status(directory)["revision"], 3)

    def test_retry_holds_lock_during_fingerprint_and_evidence_operations(self):
        directory = self.create("T-001-LOCK")
        independent = self.create("T-001-INDEPENDENT")
        self.claim("T-001-LOCK")
        helper = self.load_helper()
        at_fingerprint, release = threading.Event(), threading.Event()
        original = helper.inputs_fingerprint
        errors = []
        def pause(*args, **kwargs):
            at_fingerprint.set()
            if not release.wait(10):
                raise AssertionError("fingerprint not released")
            return original(*args, **kwargs)
        def retry():
            try:
                self.invoke(helper, "retry", "T-001-LOCK", "--revision", "2")
            except Exception as exc:
                errors.append(exc)
        with mock.patch.object(helper, "inputs_fingerprint", pause):
            worker = threading.Thread(target=retry)
            worker.start()
            self.assertTrue(at_fingerprint.wait(10))
            # The former read/fail-write/retry-write ordering is excluded:
            # fingerprinting and evidence changes are already inside this lock.
            import fcntl
            with (directory / ".status-lock").open("a+") as contender:
                with self.assertRaises(BlockingIOError):
                    fcntl.flock(contender.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            self.claim("T-001-INDEPENDENT", owner="worker-b")
            self.assertEqual(self.status(independent)["status"], "IN_PROGRESS")
            command = [sys.executable, str(SCRIPT), "--root", str(self.root), "fail", "T-001-LOCK", "--owner", "worker-a", "--revision", "2", "--reason", "late failure"]
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            # Synchronize with a second contender using the OS lock itself.
            release.set()
            worker.join(10)
            stdout, stderr = proc.communicate(timeout=10)
        self.assertFalse(worker.is_alive())
        self.assertFalse(errors, errors)
        self.assertEqual(proc.returncode, 2, stdout + stderr)
        self.assertIn("stale status revision", stderr)
        self.assertEqual(self.status(directory)["status"], "READY")

    def test_retry_interruption_resumes_without_losing_attempt_evidence(self):
        directory = self.create("T-001-RESUME")
        self.claim("T-001-RESUME")
        self.write_result(directory)
        (directory / "GUI_REVIEW.md").write_text("previous observations\n")
        self.run_cli("fail", "T-001-RESUME", "--owner", "worker-a", "--revision", "2", "--reason", "retry later")
        result, review = (directory / "CLI_RESULT.md").read_bytes(), (directory / "GUI_REVIEW.md").read_bytes()
        helper = self.load_helper()
        original = helper.atomic_bytes
        def interrupt(root, path, data):
            if path == directory / "attempts/1/GUI_REVIEW.md":
                raise OSError("injected archive interruption")
            return original(root, path, data)
        with mock.patch.object(helper, "atomic_bytes", interrupt):
            with self.assertRaisesRegex(OSError, "injected"):
                self.invoke(helper, "retry", "T-001-RESUME", "--revision", "3")
        self.assertEqual(self.status(directory)["status"], "FAILED")
        self.assertEqual((directory / "CLI_RESULT.md").read_bytes(), result)
        self.assertTrue((directory / ".transition.json").exists())
        self.run_cli("claim", "T-001-RESUME", "--owner", "intruder", "--revision", "3", ok=False)
        self.run_cli("retry", "T-001-RESUME", "--revision", "3")
        self.assertEqual((directory / "attempts/1/CLI_RESULT.md").read_bytes(), result)
        self.assertEqual((directory / "attempts/1/GUI_REVIEW.md").read_bytes(), review)
        self.assertEqual((directory / "attempts/1/claim-owner").read_text(), "worker-a")
        self.assertFalse((directory / ".transition.json").exists())
        self.assertFalse((directory / "CLI_RESULT.md").exists())
        self.assertEqual(self.status(directory)["attempt"], 2)
        before = self.snapshot(directory)
        self.run_cli("retry", "T-001-RESUME", "--revision", "3", ok=False)
        self.assertEqual(before, self.snapshot(directory))

    def test_retry_interruption_after_cleanup_and_after_status_commit(self):
        for stop_after_commit in (False, True):
            with self.subTest(stop_after_commit=stop_after_commit):
                task_id = "T-001-COMMIT" if stop_after_commit else "T-001-CLEANUP"
                directory = self.create(task_id)
                self.claim(task_id)
                self.write_result(directory)
                helper = self.load_helper()
                original = helper.atomic_json
                def interrupt(root, path, value):
                    if path == directory / "STATUS.json":
                        if stop_after_commit:
                            original(root, path, value)
                        raise OSError("injected commit interruption")
                    return original(root, path, value)
                with mock.patch.object(helper, "atomic_json", interrupt):
                    with self.assertRaisesRegex(OSError, "injected"):
                        self.invoke(helper, "retry", task_id, "--revision", "2")
                self.assertTrue((directory / "attempts/1/CLI_RESULT.md").exists())
                self.assertFalse((directory / "CLI_RESULT.md").exists())
                self.run_cli("retry", task_id, "--revision", "2")
                self.assertEqual(self.status(directory)["status"], "READY")
                self.assertEqual(self.status(directory)["attempt"], 2)

    def test_consume_interruption_is_idempotent_and_rejects_different_review(self):
        for stop_after_commit in (False, True):
            with self.subTest(stop_after_commit=stop_after_commit):
                task_id = "T-001-RECEIPT-A" if stop_after_commit else "T-001-RECEIPT-B"
                directory = self.create(task_id)
                self.claim(task_id)
                self.write_result(directory)
                self.run_cli("complete", task_id, "--owner", "worker-a", "--revision", "2")
                self.run_cli("consume", task_id, "--revision", "3", "--review", "Reviewed actual diff.", ok=False)
                self.ingest_review(directory)
                result = (directory / "CLI_RESULT.md").read_bytes()
                helper = self.load_helper()
                original = helper.atomic_json
                def interrupt(root, path, value):
                    if path == directory / "STATUS.json":
                        if stop_after_commit:
                            original(root, path, value)
                        raise OSError("injected receipt interruption")
                    return original(root, path, value)
                with mock.patch.object(helper, "atomic_json", interrupt):
                    with self.assertRaisesRegex(OSError, "injected"):
                        self.invoke(helper, "consume", task_id, "--revision", "3", "--review", "Reviewed actual diff.")
                before = self.snapshot(directory)
                self.run_cli("consume", task_id, "--revision", "3", "--review", "Conflicting review.", ok=False)
                self.assertEqual(before, self.snapshot(directory))
                self.run_cli("consume", task_id, "--revision", "3", "--review", "Reviewed actual diff.")
                self.assertEqual(self.status(directory)["status"], "CONSUMED")
                self.assertEqual((directory / "CLI_RESULT.md").read_bytes(), result)
                self.assertEqual((directory / "GUI_REVIEW.md").read_text(), "Reviewed actual diff.\n")

    def test_safe_paths_for_all_administrative_symlinks_without_outside_io(self):
        file_paths = ["STATUS.json", "CLI_TASK.md", "CLI_RESULT.md", "GUI_REVIEW.md", ".status-lock", ".transition.json", ".claim/owner", "attempts/1/STATUS.json", "baseline/INPUTS.json", "baseline/0.bin"]
        dir_paths = ["attempts", "attempts/1", ".claim", "baseline", "artifacts"]
        outside = self.temp_root / "outside"
        outside.mkdir()
        (outside / "sentinel").write_text("must not change\n")
        sentinel = self.temp_root / "outside-file"
        sentinel.write_text("must not read or write\n")
        for index, rel in enumerate(file_paths + dir_paths):
            with self.subTest(rel=rel):
                task_id = f"T-001-LINK-{index}"
                directory = self.create(task_id)
                self.claim(task_id)
                self.run_cli("fail", task_id, "--owner", "worker-a", "--revision", "2", "--reason", "test")
                target = directory / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                if target.exists():
                    if target.is_dir():
                        import shutil
                        shutil.rmtree(target)
                    else:
                        target.unlink()
                target.symlink_to(outside if rel in dir_paths else sentinel, target_is_directory=rel in dir_paths)
                before = self.snapshot(directory)
                outside_before = self.snapshot(outside)
                self.assertIn("symlink", self.run_cli("retry", task_id, "--revision", "3", ok=False).stderr)
                self.assertEqual(before, self.snapshot(directory))
                self.assertEqual(outside_before, self.snapshot(outside))
                self.assertEqual(sentinel.read_text(), "must not read or write\n")
                # Instrument reads to ensure rejection precedes following the link.
                helper = self.load_helper()
                original_read = Path.read_bytes
                original_text = Path.read_text
                def guarded_read(path, *args, **kwargs):
                    self.assertTrue(path.resolve().is_relative_to(self.root), "external bytes read")
                    return original_read(path, *args, **kwargs)
                def guarded_text(path, *args, **kwargs):
                    self.assertTrue(path.resolve().is_relative_to(self.root), "external text read")
                    return original_text(path, *args, **kwargs)
                with mock.patch.object(Path, "read_bytes", guarded_read), mock.patch.object(Path, "read_text", guarded_text):
                    with self.assertRaises(helper.HandoffError):
                        self.invoke(helper, "retry", task_id, "--revision", "3")

    def test_hidden_parent_task_and_broken_symlinks_reject_list_resolve(self):
        directory = self.create("T-001-HIDDEN")
        sync = self.root / ".codex-sync"
        for target in (sync, sync / "tasks", directory):
            with self.subTest(target=target.name):
                moved = self.temp_root / (target.name + "-moved")
                target.rename(moved)
                target.symlink_to(moved, target_is_directory=True)
                for command in (("list",), ("resolve",), ("resolve", "T-001-HIDDEN")):
                    self.assertIn("symlink", self.run_cli(*command, ok=False).stderr)
                target.unlink()
                moved.rename(target)
        result = directory / "CLI_RESULT.md"
        result.symlink_to(self.temp_root / "missing")
        self.assertIn("symlink", self.run_cli("resolve", ok=False).stderr)

    def test_explicit_pickup_ignores_legacy_and_bare_pickup_or_receipt_never_guesses(self):
        directory = self.create("T-001-NAMED")
        legacy = self.root / ".codex-sync/CLI_TASK.md"
        legacy.write_text("Status: READY\nDelegation ID: T-001-LEGACY\nParent task: T-001\n")
        self.assertEqual(self.run_cli("resolve", "T-001-NAMED").stdout.strip(), "T-001-NAMED")
        ambiguous = self.run_cli("resolve", ok=False).stderr
        self.assertIn("T-001-NAMED", ambiguous)
        self.assertIn("T-001-LEGACY (legacy)", ambiguous)
        self.claim("T-001-NAMED")
        self.write_result(directory)
        self.run_cli("complete", "T-001-NAMED", "--owner", "worker-a", "--revision", "2")
        self.assertEqual(self.run_cli("resolve", "--receipt").stdout.strip(), "T-001-NAMED")
        legacy.write_text(legacy.read_text().replace("READY", "COMPLETED"))
        (legacy.parent / "CLI_RESULT.md").write_text("Legacy result for GUI inspection.\n")
        self.assertIn("ambiguous COMPLETED", self.run_cli("resolve", "--receipt", ok=False).stderr)
        self.assertEqual(self.run_cli("resolve", "T-001-NAMED", "--receipt").stdout.strip(), "T-001-NAMED")
        self.ingest_review(directory)
        self.run_cli("consume", "T-001-NAMED", "--revision", "3", "--review", "Reviewed")
        self.assertEqual(self.run_cli("resolve", "--receipt").stdout.strip(), "T-001-LEGACY")
        self.run_cli("resolve", "T-001-NAMED", "--receipt", ok=False)

    def test_changed_owned_retry_requires_new_delegation_and_preserves_evidence(self):
        directory = self.create("T-001-RETRY-EDIT", owned=("input.md",))
        self.claim("T-001-RETRY-EDIT")
        (self.root / "input.md").write_text("partial assigned edit\n")
        self.write_result(directory)
        self.run_cli("fail", "T-001-RETRY-EDIT", "--owner", "worker-a", "--revision", "2", "--reason", "partial edit")
        before = self.snapshot(directory)
        self.assertIn("new delegation", self.run_cli("retry", "T-001-RETRY-EDIT", "--revision", "3", ok=False).stderr)
        self.assertEqual(before, self.snapshot(directory))

    def test_completion_requires_exact_check_lines_and_final_output_hashes(self):
        directory = self.create("T-001-GRAMMAR", checks=("unit suite",), owned=("input.md",))
        self.claim("T-001-GRAMMAR")
        self.write_result(directory)
        result = directory / "CLI_RESULT.md"
        original = result.read_text()
        for line in ("- unit suite: PASS (claimed)", "* unit suite: PASS", "- unit suite: PASS extra"):
            result.write_text(original.replace("- unit suite: PASS", line))
            self.run_cli("complete", "T-001-GRAMMAR", "--owner", "worker-a", "--revision", "2", ok=False)
        result.write_text(original)
        (self.root / "input.md").write_text("edited after report\n")
        self.assertIn("final outputs mismatch", self.run_cli("complete", "T-001-GRAMMAR", "--owner", "worker-a", "--revision", "2", ok=False).stderr)
        self.write_result(directory)
        self.run_cli("complete", "T-001-GRAMMAR", "--owner", "worker-a", "--revision", "2")

    def test_stale_mutations_cannot_change_claim_archive_or_review(self):
        directory = self.create("T-001-STALE-ALL")
        self.claim("T-001-STALE-ALL")
        self.write_result(directory)
        self.run_cli("complete", "T-001-STALE-ALL", "--owner", "worker-a", "--revision", "2")
        before = self.snapshot(directory)
        for args in (("retry", "--revision", "2"), ("consume", "--revision", "2", "--review", "stale"), ("claim", "--revision", "2", "--owner", "worker-b"), ("fail", "--revision", "2", "--owner", "worker-a", "--reason", "stale"), ("recover", "--revision", "2", "--reason", "stale")):
            self.run_cli(args[0], "T-001-STALE-ALL", *args[1:], ok=False)
            self.assertEqual(before, self.snapshot(directory))

    def plan(self, count=3):
        return {"total_steps": count, "steps": [{"id": f"stage{i}", "label": f"Major stage {i}"} for i in range(count)]}

    def paired_contract(self, review_module, plan, budget=3):
        module = self.load_helper()
        summary = {"plan_sha256": module.plan_fingerprint(plan), "bullets": [
            {"ids": [step["id"]], "text": step["label"]} for step in plan["steps"]]}
        summary_hash = hashlib.sha256(json.dumps(summary, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
        return {"version": 1, "task_id": "T-003", "revision": 2,
                "execution": {"scope": "bounded", "acceptance": "receipt verified", "permissions": "offline",
                    "invariants": "fixture only", "inputs": ["input.md"],
                    "plan_of_execution": [b["text"] for b in summary["bullets"]], "plan_summary_sha256": summary_hash,
                    "executor_profile": {"requested_model": "gpt-6-luna", "requested_reasoning": "medium", "justification": "fixture"},
                    "validation": ["test"]},
                "review": {"dimensions": list(review_module.REVIEW_DIMENSIONS), "budget": {"max_changed_files": 10, "max_evidence_items": 20},
                    "profile": {"requested_model": "gpt-6.1-sol", "requested_reasoning": "medium", "justification": "fixture"}},
                "loop": {"enabled": True, "correction_budget": budget, "budget_rationale": "GUI-selected fixture budget", "escalation": "scope conflict"}}

    def planned(self, task_id="T-003-PLAN", count=3):
        self.run_cli("create", task_id, "--parent", "T-003", "--task", "Bounded offline work.",
                     "--input", "input.md", "--check", "unit suite", "--execution-plan", json.dumps(self.plan(count)))
        directory = self.root / ".codex-sync/tasks" / task_id
        self.claim(task_id)
        return directory

    def progress(self, directory, *action, ok=True, owner="worker-a", revision=None):
        return self.run_cli("progress", directory.name, "--owner", owner, "--revision",
                            str(revision if revision is not None else self.status(directory)["revision"]), *action, ok=ok)

    def finish_stage(self, directory, milestone):
        self.progress(directory, "--start", milestone)
        return self.progress(directory, "--done", milestone)

    def test_plan_validation_before_ready_has_no_partial_task(self):
        invalid = [None, [], {}, {"total_steps": True, "steps": []}, self.plan(0), self.plan(21),
                   {**self.plan(), "total_steps": 2},
                   {"total_steps": 2, "steps": [self.plan()["steps"][0]] * 2},
                   {"total_steps": 1, "steps": [{"id": "../escape", "label": "Read"}]},
                   {"total_steps": 1, "steps": [{"id": "read", "label": "escape\x1b"}]},
                   {"total_steps": 1, "steps": [{"id": "read", "label": " "}]},
                   {"total_steps": 1, "steps": [{"id": "read", "label": "Read", "extra": 1}]}]
        for index, plan in enumerate(invalid):
            task_id = f"T-003-BAD-{index}"
            self.run_cli("create", task_id, "--parent", "T-003", "--task", "Work",
                         "--execution-plan", json.dumps(plan), ok=False)
            self.assertFalse((self.root / ".codex-sync/tasks" / task_id).exists())
        self.run_cli("create", "T-003-JSON", "--parent", "T-003", "--task", "Work", "--execution-plan", "{", ok=False)
        self.run_cli("create", "T-003-EMPTY", "--parent", "T-003", "--task", "Work", "--execution-plan", "", ok=False)
        self.planned("T-003-MAX", 20)

    def test_frozen_inline_plan_bootstrap_and_malformed_blocks(self):
        task = "Work\n\n```json\n" + json.dumps({"execution_plan": self.plan(1)}) + "\n```\n"
        self.run_cli("create", "T-003-INLINE", "--parent", "T-003", "--task", task)
        directory = self.root / ".codex-sync/tasks/T-003-INLINE"
        self.claim(directory.name)
        # Simulates a pre-feature frozen task claimed by the previous helper.
        status = self.status(directory)
        status.pop("progress")
        (directory / "STATUS.json").write_text(json.dumps(status))
        self.progress(directory, "--start", "stage0")
        self.assertEqual(self.status(directory)["progress"]["plan"], self.plan(1))
        for index, bad in enumerate((task + task, '```json\n{"execution_plan":\n```\n', task.rsplit("```", 1)[0])):
            self.run_cli("create", f"T-003-INLINE-BAD-{index}", "--parent", "T-003", "--task", bad, ok=False)

    def test_review_contract_is_frozen_and_rendered_as_one_ten_row_table(self):
        module = self.load_helper()
        review_module_spec = importlib.util.spec_from_file_location("review_contract_fixture", SCRIPT.with_name("implementation_review.py"))
        review_module = importlib.util.module_from_spec(review_module_spec); review_module_spec.loader.exec_module(review_module)
        plan = self.plan(2); paired = self.paired_contract(review_module, plan, budget=10)
        summary = {"plan_sha256": module.plan_fingerprint(plan), "bullets": [
            {"ids": ["stage0"], "text": "Major stage 0"}, {"ids": ["stage1"], "text": "Major stage 1"}]}
        task = "Work\n\n```json\n" + json.dumps({"execution_plan": plan}) + "\n```\n\n## Execution plan summary\n\n```json\n" + json.dumps({"plan_summary": summary}) + "\n```\n"
        self.run_cli("create", "T-003-PAIRED", "--parent", "T-003", "--task", task, "--input", "input.md", "--review-contract", json.dumps(paired))
        directory = self.root / ".codex-sync/tasks/T-003-PAIRED"
        self.assertTrue((directory / "IMPLEMENTATION_REVIEW_CONTRACT.json").is_file())
        self.assertTrue(self.run_cli("validate", "T-003-PAIRED").stdout)
        plan = self.plan(2)
        rows = [("CLI pickup", "old"), ("GUI receipt", "old"), ("Model / reasoning level", "old"),
                ("Estimated CLI time / steps", "20–60 min / 8 steps"), ("szacowane tokeny/wiadomości", "3532 tokenów; 11 wiadomości")]
        loop = {"task_id": "T-003-PAIRED", "parent_id": "T-003", "contract": paired,
                "time_steps": "20–60 min / 8 steps", "gui_estimate": "3532 tokenów; 11 wiadomości"}
        rendered = module.render_handoff_table(rows, plan, summary, review_loop=loop, root=self.root)
        self.assertEqual(sum(line.startswith("| ") for line in rendered.splitlines()) - 1, 10)
        for command in ("wykonaj T-003-PAIRED", "sprawdź T-003-PAIRED", "popraw T-003-PAIRED R&lt;n&gt;", "gotowe T-003-PAIRED"):
            self.assertIn(command, rendered)
        self.assertNotIn("wykonaj T-003 ", rendered)
        self.assertIn("max 10 corrections", rendered)
        self.assertTrue(rendered.endswith("| Plan of execution | • Major stage 0<br>• Major stage 1 |"))
        self.assertIn("gpt-6-luna / Medium", rendered)
        self.assertIn("gpt-6.1-sol / Medium", rendered)
        mechanical = json.loads(json.dumps(paired)); mechanical["version"] = 2
        mechanical["loop"].update(enabled=False, correction_policy="MAX_CYCLES",
                                  correction_budget=None, budget_rationale=None)
        mechanical["routing"] = {"execution_class": "MECHANICAL", "review_route": "NONE",
            "gui_finalization": "RECEIPT_ONLY", "reason": "deterministic publication readback",
            "high_reason": None, "targeted_trigger": None}
        mechanical_task = "Work\n\n```json\n" + json.dumps({"execution_plan": plan}) + "\n```\n\n## Execution plan summary\n\n```json\n" + json.dumps({"plan_summary": summary}) + "\n```\n"
        self.run_cli("create", "T-003-MECHANICAL", "--parent", "T-003", "--task", mechanical_task,
                     "--input", "input.md", "--check", "synthetic preflight", "--review-contract", json.dumps(mechanical))
        mechanical_loop = {**loop, "task_id": "T-003-MECHANICAL", "contract": mechanical}
        mechanical_render = module.render_handoff_table(rows, plan, summary, review_loop=mechanical_loop, root=self.root)
        self.assertIn("MECHANICAL · NONE · GUI finalization RECEIPT_ONLY", mechanical_render)
        self.assertIn("Independent review | none", mechanical_render)
        self.assertIn("GUI finalization", mechanical_render)
        self.assertIn("Reason: deterministic publication", mechanical_render)
        self.assertIn("after required checks; no independent review", mechanical_render)
        self.assertNotIn("after ACCEPTED", mechanical_render)
        self.assertNotIn("sprawdź T-003-MECHANICAL", mechanical_render)
        mechanical_dir = self.root / ".codex-sync/tasks/T-003-MECHANICAL"
        self.claim("T-003-MECHANICAL")
        for step in ("stage0", "stage1"):
            self.finish_stage(mechanical_dir, step)
        self.write_result(mechanical_dir, passed=("synthetic preflight",))
        mechanical_status = self.status(mechanical_dir)
        self.run_cli("complete", "T-003-MECHANICAL", "--owner", "worker-a",
                     "--revision", str(mechanical_status["revision"]))
        self.assertEqual(self.run_cli("resolve", "T-003-MECHANICAL", "--receipt").stdout.strip(), "T-003-MECHANICAL")

        high = json.loads(json.dumps(paired)); high["version"] = 2
        high["loop"]["correction_policy"] = "MAX_CYCLES"
        high["review"]["profile"]["requested_reasoning"] = "high"
        high["routing"] = {"execution_class": "COMPLEX", "review_route": "SOL_HIGH",
            "gui_finalization": "RECEIPT_ONLY", "reason": "shared behavior has difficult verification",
            "high_reason": "unresolved_material_uncertainty_after_medium", "targeted_trigger": None}
        self.run_cli("create", "T-003-HIGH-REASON", "--parent", "T-003", "--task", mechanical_task,
                     "--input", "input.md", "--review-contract", json.dumps(high))
        high_loop = {**loop, "task_id": "T-003-HIGH-REASON", "contract": high}
        high_render = module.render_handoff_table(rows, plan, summary, review_loop=high_loop, root=self.root)
        self.assertIn("High reason: Unresolved material uncertainty after medium", high_render)
        with self.assertRaises(module.HandoffError):
            module.render_handoff_table(rows, plan, summary, review_loop={**loop, "contract": {**paired,
                "execution": {**paired["execution"], "plan_of_execution": ["different", "plan"]}},
                }, root=self.root)
        with self.assertRaises(module.HandoffError):
            module.render_handoff_table(rows, plan, summary, review_loop={**loop, "parent_id": "T-004"}, root=self.root)
        opened = json.loads(json.dumps(paired))
        opened["version"] = 2
        opened["loop"].update(correction_policy="UNTIL_ACCEPTED_OR_ESCALATED", correction_budget=None)
        open_task = "Work\n\n```json\n" + json.dumps({"execution_plan": plan}) + "\n```\n\n## Execution plan summary\n\n```json\n" + json.dumps({"plan_summary": summary}) + "\n```\n"
        self.run_cli("create", "T-003-PAIRED-OPEN", "--parent", "T-003", "--task", open_task,
                     "--input", "input.md", "--review-contract", json.dumps(opened))
        open_loop = {**loop, "task_id": "T-003-PAIRED-OPEN", "contract": opened}
        opened_rendered = module.render_handoff_table(rows, plan, summary, review_loop=open_loop, root=self.root)
        self.assertIn("wykonaj T-003-PAIRED", opened_rendered)
        self.assertIn("until accepted or escalated · no numeric correction limit", opened_rendered)
        with self.assertRaises(module.HandoffError):
            module.render_handoff_table(rows, plan, summary, review_loop={**open_loop, "task_id": "T999-UNREGISTERED"}, root=self.root)
        unrelated = json.loads(json.dumps(paired)); unrelated["task_id"] = "T-024"
        self.run_cli("create", "T-024-OTHER", "--parent", "T-024", "--issue", "26", "--task", task,
                     "--input", "input.md", "--review-contract", json.dumps(unrelated))
        with self.assertRaises(module.HandoffError):
            module.render_handoff_table(rows, plan, summary,
                review_loop={**loop, "task_id": "T-024-OTHER", "parent_id": "T-023"}, root=self.root)
        with self.assertRaises(module.HandoffError):
            module.render_handoff_table(rows, plan, summary, review_loop=loop)

    def test_enabled_receipt_resolution_requires_current_reviewer_terminal_verdict(self):
        review_module_spec = importlib.util.spec_from_file_location("review_gate_fixture", SCRIPT.with_name("implementation_review.py"))
        review_module = importlib.util.module_from_spec(review_module_spec); review_module_spec.loader.exec_module(review_module)
        plan = self.plan(1); paired = self.paired_contract(review_module, plan, budget=1)
        paired["execution"]["inputs"] = ["fixture.md"]
        directory = self.root / ".codex-sync/tasks/T-003-REVIEW-GATE"
        summary = {"plan_sha256": self.load_helper().plan_fingerprint(plan), "bullets": [{"ids": ["stage0"], "text": "Major stage 0"}]}
        task = "Work\n\n```json\n" + json.dumps({"execution_plan": plan}) + "\n```\n\n## Execution plan summary\n\n```json\n" + json.dumps({"plan_summary": summary}) + "\n```\n"
        self.run_cli("create", directory.name, "--parent", "T-003", "--task", task, "--input", "fixture.md", "--owned", "input.md", "--review-contract", json.dumps(paired))
        self.claim(directory.name)
        self.progress(directory, "--start", "stage0")
        self.progress(directory, "--done", "stage0")
        (self.root / "input.md").write_text("changed for reviewed fixture\n")
        self.write_result(directory)
        self.run_cli("complete", directory.name, "--owner", "worker-a", "--revision", str(self.status(directory)["revision"]))
        self.run_cli("resolve", directory.name, "--receipt", ok=False)
        review_module.initialize(self.root, directory.name, paired,
            result_path=f".codex-sync/tasks/{directory.name}/CLI_RESULT.md", changed_paths=["input.md"])
        review_module.begin_review(self.root, directory.name, review_id="R1",
            result_path=f".codex-sync/tasks/{directory.name}/CLI_RESULT.md", changed_paths=["input.md"], reviewer_identity="reviewer-1")
        review_module.submit_review(self.root, directory.name, review_id="R1", verdict="ACCEPTED", findings=[],
            result_path=f".codex-sync/tasks/{directory.name}/CLI_RESULT.md", changed_paths=["input.md"], reviewer_identity="reviewer-1",
            reviewer_profile=None, dimensions={name: "checked: fixture" for name in review_module.REVIEW_DIMENSIONS}, read_only_attestation=True)
        execution_review_spec = importlib.util.spec_from_file_location("triage_execution_review", SCRIPT.with_name("execution_review.py"))
        execution_review = importlib.util.module_from_spec(execution_review_spec); execution_review_spec.loader.exec_module(execution_review)
        inventory = self.root / "docs/telemetry/optimization-inventory.json"
        inventory.parent.mkdir(parents=True, exist_ok=True)
        reports = review_module.cycle_reports(self.root, directory.name)
        with self.assertRaises(review_module.ReviewError):
            review_module.require_cycle_triage(self.root, directory.name)
        for cycle in reports:
            execution_review.ingest(inventory, cycle["report"], task_id=directory.name, attempt=1,
                report_sha256=cycle["report_sha256"], observations=[], decision="KEEP OBSERVING",
                rationale="synthetic lifecycle evidence", evidence="handoff:synthetic", cycle_id=cycle["cycle_id"])
            review_module.record_cycle_triage(self.root, directory.name, cycle_id=cycle["cycle_id"],
                inventory_path=inventory, actor="GUI")
        result_body = (directory / "CLI_RESULT.md").read_text(encoding="utf-8")
        provenance_end = result_body.index("\n```", result_body.index("```json")) + len("\n```")
        final_report = execution_review.extract_review(result_body, after=provenance_end)
        final_hash = hashlib.sha256(json.dumps(final_report, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
        execution_review.ingest(inventory, final_report, task_id=directory.name, attempt=1,
            report_sha256=final_hash, observations=[], decision="KEEP OBSERVING",
            rationale="synthetic final receipt", evidence="handoff:synthetic")
        review_module.require_cycle_triage(self.root, directory.name)
        self.assertEqual(self.run_cli("resolve", directory.name, "--receipt").stdout.strip(), directory.name)
        status = self.status(directory)
        self.run_cli("consume", directory.name, "--revision", str(status["revision"]), "--review", "GUI accepted first-pass fixture")
        self.assertEqual(self.status(directory)["status"], "CONSUMED")

    def test_plan_summary_table_order_grouping_staleness_and_legacy(self):
        spec = importlib.util.spec_from_file_location("handoff_summary", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        rows = [("CLI pickup", "`pobierz zadanie X`"), ("GUI receipt", "`gotowe X`"),
                ("Model / reasoning level", "Luna / Medium"), ("Estimated CLI time / steps", "5–13 minutes / 5 steps"),
                ("szacowane tokeny/wiadomości", "100 tokenów; 2 wiadomości")]
        for count, groups in ((1, [["stage0"]]), (5, [[f"stage{i}"] for i in range(5)]),
                              (12, [[f"stage{i}", f"stage{i+1}"] for i in range(0, 12, 2)])):
            plan = self.plan(count)
            summary = {"plan_sha256": module.plan_fingerprint(plan),
                       "bullets": [{"ids": group, "text": "Milestone " + ", ".join(group)} for group in groups]}
            rendered = module.render_handoff_table(rows, plan, summary)
            self.assertEqual(len(rendered.splitlines()), 8)
            self.assertEqual(rendered.splitlines()[2:7], [f"| {label} | {value} |" for label, value in rows])
            self.assertEqual(rendered.splitlines()[-1].split("|")[1].strip(), "Plan of execution")
            self.assertEqual(rendered.splitlines()[-1].count("•"), len(groups))
        escaped = module.render_handoff_table([("x|y", "a|b")] + rows[1:], None, None)
        self.assertIn("x\\|y", escaped)
        self.assertNotIn("Plan of execution", escaped)
        stale = {"plan_sha256": "0" * 64, "bullets": [{"ids": ["stage0"], "text": "x"}]}
        with self.assertRaisesRegex(module.HandoffError, "stale"):
            module.render_handoff_table(rows, self.plan(1), stale)
        bad_order = {"plan_sha256": module.plan_fingerprint(self.plan(2)),
                     "bullets": [{"ids": ["stage1", "stage0"], "text": "x"}]}
        with self.assertRaisesRegex(module.HandoffError, "cover"):
            module.render_handoff_table(rows, self.plan(2), bad_order)
        eleven = self.plan(11)
        too_many = {"plan_sha256": module.plan_fingerprint(eleven),
                    "bullets": [{"ids": [f"stage{i}"], "text": f"Step {i}"} for i in range(11)]}
        with self.assertRaisesRegex(module.HandoffError, "1–10"):
            module.render_handoff_table(rows, eleven, too_many)
        plan = self.plan(1)
        frozen_summary = {"plan_sha256": module.plan_fingerprint(plan),
                          "bullets": [{"ids": ["stage0"], "text": "Inspect the supplied evidence"}]}
        self.run_cli("create", "T-003-SUMMARY", "--parent", "T-003", "--task", "Work",
                     "--execution-plan", json.dumps(plan), "--plan-summary", json.dumps(frozen_summary))
        frozen_text = (self.root / ".codex-sync/tasks/T-003-SUMMARY/CLI_TASK.md").read_text()
        self.assertEqual(module.frozen_plan_summary(frozen_text, plan), frozen_summary)
        stale_plan = self.plan(1)
        stale_plan["steps"][0]["label"] = "Changed source plan"
        self.run_cli("create", "T-003-SUMMARY-STALE", "--parent", "T-003", "--task", "Work",
                     "--execution-plan", json.dumps(stale_plan), "--plan-summary", json.dumps(frozen_summary), ok=False)
        self.assertFalse((self.root / ".codex-sync/tasks/T-003-SUMMARY-STALE").exists())

    def test_planless_compatibility_does_not_invent_plan(self):
        directory = self.create("T-003-OLD")
        self.assertNotIn("[", self.claim(directory.name).stdout)
        before = self.snapshot(directory)
        self.assertIn("planless", self.progress(directory, "--start", "inspect", ok=False).stderr)
        self.assertEqual(before, self.snapshot(directory))
        self.write_result(directory)
        self.run_cli("complete", directory.name, "--owner", "worker-a", "--revision", "2")
        self.assertNotIn("progress", self.status(directory))

    def test_transition_restart_and_no_fake_drift_or_duplicate_output(self):
        directory = self.planned()
        out = self.progress(directory, "--start", "stage0").stdout
        self.assertIn("~0% — Major stage 0", out)
        self.assertEqual(len(out.split("[")[1].split("]")[0]), 30)
        self.assertIn("●  T-003", out)
        before = self.snapshot(directory)
        # New subprocesses emulate restart and an arbitrary number of ordinary logs/commands.
        for _ in range(3):
            self.run_cli("validate", directory.name)
            self.assertEqual(self.progress(directory, "--start", "stage0").stdout, "")
        self.assertEqual(before, self.snapshot(directory))
        self.assertIn("~33%", self.progress(directory, "--done", "stage0").stdout)
        before = self.snapshot(directory)
        self.assertEqual(self.progress(directory, "--done", "stage0").stdout, "")
        self.assertEqual(before, self.snapshot(directory))
        self.assertIsNone(self.status(directory)["progress"]["current"])

    def test_progress_rejects_unknown_stale_owner_scope_and_input_without_writes(self):
        directory = self.planned()
        for action, kwargs in [(("--start", "unknown"), {}), (("--done", "stage0"), {}),
                               (("--start", "stage0"), {"owner": "intruder"}),
                               (("--start", "stage0"), {"revision": 1})]:
            before = self.snapshot(directory)
            self.progress(directory, *action, ok=False, **kwargs)
            self.assertEqual(before, self.snapshot(directory))
        self.progress(directory, "--start", "stage0")
        before = self.snapshot(directory)
        self.progress(directory, "--start", "stage1", ok=False)
        self.assertEqual(before, self.snapshot(directory))
        for path in (self.root / "input.md", directory / "CLI_TASK.md", directory / "baseline/0.bin"):
            original = path.read_bytes()
            path.write_bytes(original + b"drift")
            before = self.snapshot(directory)
            self.progress(directory, "--done", "stage0", ok=False)
            self.assertEqual(before, self.snapshot(directory))
            path.write_bytes(original)
        self.progress(directory, "--start", "../outside", ok=False)
        self.run_cli("progress", "../outside", "--owner", "worker-a", "--revision", "2", "--start", "stage0", ok=False)

    def test_amendment_clamps_percent_preserves_original_and_bounds_evidence(self):
        directory = self.planned(count=2)
        frozen = (directory / "CLI_TASK.md").read_bytes()
        self.finish_stage(directory, "stage0")
        self.assertEqual(self.status(directory)["progress"]["percent"], 50)
        plan = self.plan(4)
        plan["steps"][1]["label"] = "Adapt original intent"
        self.assertIn("~50%", self.progress(directory, "--amend", json.dumps(plan), "--reason", "Necessary independent validation").stdout)
        self.assertIn("~50%", self.finish_stage(directory, "stage1").stdout)
        self.assertIn("~75%", self.finish_stage(directory, "stage2").stdout)
        self.assertIn("~99%", self.finish_stage(directory, "stage3").stdout)
        self.assertEqual((directory / "CLI_TASK.md").read_bytes(), frozen)
        evidence = self.status(directory)["progress"]["amendments"][0]
        self.assertEqual(evidence["owner"], "worker-a")
        self.assertEqual(evidence["reason"], "Necessary independent validation")
        for bad, reason in ((self.plan(21), "Too many"), (self.plan(1), "Remove stage"),
                            (self.plan(5), ""), (plan, "No change")):
            before = self.snapshot(directory)
            self.progress(directory, "--amend", json.dumps(bad), "--reason", reason, ok=False)
            self.assertEqual(before, self.snapshot(directory))
        self.run_cli("validate", directory.name)

    def test_completion_gates_percentage_and_consumed_state(self):
        directory = self.planned(count=1)
        self.write_result(directory)
        before = self.snapshot(directory)
        self.run_cli("complete", directory.name, "--owner", "worker-a", "--revision", "2", ok=False)
        self.assertEqual(before, self.snapshot(directory))
        self.finish_stage(directory, "stage0")
        result = directory / "CLI_RESULT.md"
        result.write_text(result.read_text().replace("- unit suite: PASS", "- unit suite: FAIL"))
        self.run_cli("complete", directory.name, "--owner", "worker-a", "--revision", "4", ok=False)
        self.assertEqual(self.status(directory)["progress"]["percent"], 99)
        self.write_result(directory)
        output = self.run_cli("complete", directory.name, "--owner", "worker-a", "--revision", "4").stdout
        self.assertIn("~100%", output)
        self.assertIn("GUI review pending", output)
        self.run_cli("validate", directory.name)
        before = self.snapshot(directory)
        self.progress(directory, "--start", "stage0", ok=False)
        self.assertEqual(before, self.snapshot(directory))
        self.ingest_review(directory)
        self.run_cli("consume", directory.name, "--revision", "5", "--review", "CHANGES REQUIRED: independent review")
        self.run_cli("validate", directory.name)
        self.assertEqual(self.status(directory)["progress"]["percent"], 100)
        self.progress(directory, "--done", "stage0", ok=False)

    def test_failure_retry_archives_progress_and_retains_display_floor(self):
        directory = self.planned(count=2)
        self.finish_stage(directory, "stage0")
        self.progress(directory, "--amend", json.dumps(self.plan(3)), "--reason", "Required verification")
        revision = self.status(directory)["revision"]
        self.run_cli("fail", directory.name, "--owner", "worker-a", "--revision", str(revision), "--reason", "Interrupted")
        failed = self.status(directory)
        self.assertEqual(failed["progress"]["percent"], 50)
        before = self.snapshot(directory)
        self.progress(directory, "--done", "stage1", ok=False)
        self.assertEqual(before, self.snapshot(directory))
        self.run_cli("retry", directory.name, "--revision", str(failed["revision"]))
        self.assertEqual(json.loads((directory / "attempts/1/STATUS.json").read_text()), failed)
        status = self.status(directory)
        self.assertEqual(status["progress"]["completed"], [])
        self.assertEqual(status["progress"]["percent"], 50)
        self.assertEqual(len(status["progress"]["amendments"]), 1)
        self.claim(directory.name, revision=status["revision"])
        self.assertIn("~50%", self.finish_stage(directory, "stage0").stdout)

    def test_progress_rejects_symlink_and_pending_journal_before_mutation(self):
        directory = self.planned()
        sentinel = self.temp_root / "outside"
        sentinel.write_text("unchanged")
        (directory / "artifacts/link").symlink_to(sentinel)
        before = self.snapshot(directory)
        self.assertIn("symlink", self.progress(directory, "--start", "stage0", ok=False).stderr)
        self.assertEqual(before, self.snapshot(directory))
        self.assertEqual(sentinel.read_text(), "unchanged")
        (directory / "artifacts/link").unlink()
        (directory / ".transition.json").write_text("{}")
        before = self.snapshot(directory)
        self.assertIn("pending", self.progress(directory, "--start", "stage0", ok=False).stderr)
        self.assertEqual(before, self.snapshot(directory))

    def test_optional_context_preview_is_diagnostic_and_plan_count_remains_frozen(self):
        preview = self.root / "preview.json"
        preview.write_text(json.dumps({
            "version": 1,
            "preview": "GUI session estimate: ~123 estimated tokens\nGUI session: 2 messages / 8 UTF-8 bytes",
            "history_url": "https://github.com/mhaduk/ck3-dynasty-map/blob/main/docs/telemetry/gui-context/T-001.jsonl",
        }))
        task = "Work\n\n```json\n" + json.dumps({"execution_plan": self.plan(2)}) + "\n```\n"
        self.run_cli("create", "T-001-CONTEXT", "--parent", "T-001", "--task", task,
                     "--context-preview", "preview.json")
        directory = self.root / ".codex-sync/tasks/T-001-CONTEXT"
        text = (directory / "CLI_TASK.md").read_text()
        self.assertEqual(text.count("GUI session"), 2)
        self.assertIn("[history](https://github.com/mhaduk/ck3-dynasty-map/blob/main/docs/telemetry/gui-context/T-001.jsonl)", text)
        self.assertEqual(self.status(directory)["inputs"], {})
        self.claim(directory.name)
        self.assertEqual(len(self.status(directory)["progress"]["plan"]["steps"]), 2)

    def test_progress_rendering_no_color_and_parent_fallback(self):
        spec = importlib.util.spec_from_file_location("handoff_for_render", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        status = {"id": "T-001-LONG-ID", "parent_id": "T-001", "status": "IN_PROGRESS",
                  "progress": {"percent": 34, "current": "stage0", "plan": {"steps": [{"id": "stage0", "label": "Readable stage"}]}}}
        line = module.progress_line(status)
        self.assertIn("●  T-001 [██████████░░░░░░░░░░░░░░░░░░░░] ~34% — Readable stage", line)
        self.assertNotIn("\x1b[", line)
        with mock.patch.object(module.sys.stdout, "isatty", return_value=True), mock.patch.dict(os.environ, {}, clear=True):
            colored = module.progress_line(status)
        self.assertTrue(colored.startswith("\x1b[32m●\x1b[0m  T-001"))
        with mock.patch.object(module.sys.stdout, "isatty", return_value=True), mock.patch.dict(os.environ, {"NO_COLOR": "1"}):
            no_color = module.progress_line(status)
        self.assertTrue(no_color.startswith("●  T-001"))
        self.assertNotIn("\x1b[", no_color)
        status["parent_id"] = None
        self.assertIn("  T-001-LONG-ID [", module.progress_line(status))

    def test_progress_plan_evidence_tampering_and_premature_100_rejected(self):
        directory = self.planned()
        original = self.status(directory)
        for change in ({"percent": 100}, {"plan": self.plan(4)}, {"completed": ["unknown"]}, {"completed": [[], []]}):
            status = json.loads(json.dumps(original))
            status["progress"].update(change)
            (directory / "STATUS.json").write_text(json.dumps(status))
            self.run_cli("validate", directory.name, ok=False)
        (directory / "STATUS.json").write_text(json.dumps(original))

    def test_progress_atomic_interruption_and_exclusive_lock(self):
        directory = self.planned()
        helper = self.load_helper()
        before = self.snapshot(directory)
        original = helper.atomic_json
        import fcntl
        def interrupt(root, path, value):
            self.assertEqual(path, directory / "STATUS.json")
            with (directory / ".status-lock").open("a+") as contender:
                with self.assertRaises(BlockingIOError):
                    fcntl.flock(contender.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            raise OSError("injected before progress commit")
        with mock.patch.object(helper, "atomic_json", interrupt):
            with self.assertRaisesRegex(OSError, "injected"):
                self.invoke(helper, "progress", directory.name, "--owner", "worker-a", "--revision", "2", "--start", "stage0")
        self.assertEqual(before, self.snapshot(directory))
        def after_commit(root, path, value):
            original(root, path, value)
            raise OSError("injected after progress commit")
        with mock.patch.object(helper, "atomic_json", after_commit):
            with self.assertRaisesRegex(OSError, "injected"):
                self.invoke(helper, "progress", directory.name, "--owner", "worker-a", "--revision", "2", "--start", "stage0")
        committed = self.snapshot(directory)
        self.assertEqual(self.progress(directory, "--start", "stage0").stdout, "")
        self.assertEqual(committed, self.snapshot(directory))

    def test_concurrent_progress_only_one_revision_wins(self):
        directory = self.planned()
        commands = [[sys.executable, str(SCRIPT), "--root", str(self.root), "progress", directory.name,
                     "--owner", "worker-a", "--revision", "2", "--start", milestone]
                    for milestone in ("stage0", "stage1")]
        workers = [subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for cmd in commands]
        output = [worker.communicate(timeout=15) for worker in workers]
        self.assertEqual(sorted(worker.returncode for worker in workers), [0, 2])
        self.assertEqual(self.status(directory)["revision"], 3)
        self.assertEqual(sum("~0%" in stdout for stdout, _ in output), 1)
        self.assertTrue(any("stale status revision" in stderr for _, stderr in output))

    def test_amendment_count_cap_and_interrupted_attempt_retry(self):
        directory = self.planned(count=1)
        for index in range(20):
            plan = self.plan(1)
            plan["steps"][0]["label"] = f"Adapt intent {index}"
            self.progress(directory, "--amend", json.dumps(plan), "--reason", "Preserve original intent")
        before = self.snapshot(directory)
        self.progress(directory, "--amend", json.dumps(self.plan(2)), "--reason", "One more", ok=False)
        self.assertEqual(before, self.snapshot(directory))
        self.progress(directory, "--start", "stage0")
        previous = self.status(directory)
        self.run_cli("retry", directory.name, "--revision", str(previous["revision"]))
        self.assertEqual(json.loads((directory / "attempts/1/STATUS.json").read_text()), previous)
        self.assertIsNone(self.status(directory)["progress"]["current"])
        self.assertEqual(len(self.status(directory)["progress"]["amendments"]), 20)

    def test_temporary_root_end_to_end_progress_transcript(self):
        transcript = ["Temporary-root offline demonstration; no live task receipt."]
        self.run_cli("create", "T-003-DEMO", "--parent", "T-003", "--task", "Offline demo", "--check", "unit suite",
                     "--execution-plan", json.dumps(self.plan(2)))
        directory = self.root / ".codex-sync/tasks/T-003-DEMO"
        transcript += ["create: frozen GUI plan with two major stages", self.claim(directory.name).stdout.strip()]
        transcript.append(self.progress(directory, "--start", "stage0").stdout.strip())
        transcript.append("ordinary log: inspected bounded fixture")
        transcript.append(self.progress(directory, "--done", "stage0").stdout.strip())
        transcript.append(self.progress(directory, "--amend", json.dumps(self.plan(3)), "--reason", "Additional independent fixture verification").stdout.strip())
        for milestone in ("stage1", "stage2"):
            transcript.append(self.progress(directory, "--start", milestone).stdout.strip())
            transcript.append("ordinary log: verified fixture stage")
            transcript.append(self.progress(directory, "--done", milestone).stdout.strip())
        self.write_result(directory)
        revision = self.status(directory)["revision"]
        transcript.append(self.run_cli("complete", directory.name, "--owner", "worker-a", "--revision", str(revision)).stdout.strip())
        transcript.append("ordinary log: independent fixture review completed")
        self.ingest_review(directory)
        transcript.append(self.run_cli("consume", directory.name, "--revision", str(revision + 1), "--review", "ACCEPTED: offline demonstration only").stdout.strip())
        self.run_cli("validate", directory.name)
        print("\n" + "\n".join(transcript))


if __name__ == "__main__":
    unittest.main()
