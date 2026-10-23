import json
import hashlib
import importlib.util
import threading
from unittest import mock
import os
from pathlib import Path
import subprocess
import sys
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

    def tearDown(self):
        self.temp.cleanup()

    def run_cli(self, *args, ok=True):
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
        (directory / "CLI_RESULT.md").write_text(body)

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
        (directory / "GUI_REVIEW.md").write_text("Reviewed result and files.\n")
        self.run_cli("consume", "T-001-GATE", "--revision", "3", "--review", "Reviewed result and files.")
        self.assertEqual(json.loads((directory / "STATUS.json").read_text())["status"], "CONSUMED")

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

    def planned(self, task_id="T-007-PLAN", count=3):
        self.run_cli("create", task_id, "--parent", "T-007", "--task", "Bounded offline work.",
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
            task_id = f"T-007-BAD-{index}"
            self.run_cli("create", task_id, "--parent", "T-007", "--task", "Work",
                         "--execution-plan", json.dumps(plan), ok=False)
            self.assertFalse((self.root / ".codex-sync/tasks" / task_id).exists())
        self.run_cli("create", "T-007-JSON", "--parent", "T-007", "--task", "Work", "--execution-plan", "{", ok=False)
        self.run_cli("create", "T-007-EMPTY", "--parent", "T-007", "--task", "Work", "--execution-plan", "", ok=False)
        self.planned("T-007-MAX", 20)

    def test_frozen_inline_plan_bootstrap_and_malformed_blocks(self):
        task = "Work\n\n```json\n" + json.dumps({"execution_plan": self.plan(1)}) + "\n```\n"
        self.run_cli("create", "T-007-INLINE", "--parent", "T-007", "--task", task)
        directory = self.root / ".codex-sync/tasks/T-007-INLINE"
        self.claim(directory.name)
        # Simulates a pre-feature frozen task claimed by the previous helper.
        status = self.status(directory)
        status.pop("progress")
        (directory / "STATUS.json").write_text(json.dumps(status))
        self.progress(directory, "--start", "stage0")
        self.assertEqual(self.status(directory)["progress"]["plan"], self.plan(1))
        for index, bad in enumerate((task + task, '```json\n{"execution_plan":\n```\n', task.rsplit("```", 1)[0])):
            self.run_cli("create", f"T-007-INLINE-BAD-{index}", "--parent", "T-007", "--task", bad, ok=False)

    def test_planless_compatibility_does_not_invent_plan(self):
        directory = self.create("T-007-OLD")
        self.assertNotIn("[", self.claim(directory.name).stdout)
        before = self.snapshot(directory)
        self.assertIn("planless", self.progress(directory, "--start", "inspect", ok=False).stderr)
        self.assertEqual(before, self.snapshot(directory))
        self.write_result(directory)
        self.run_cli("complete", directory.name, "--owner", "worker-a", "--revision", "2")
        self.assertNotIn("progress", self.status(directory))

    def test_transition_restart_and_no_fake_drift_or_duplicate_output(self):
        directory = self.planned()
        self.assertIn("~0% stage0", self.progress(directory, "--start", "stage0").stdout)
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
        self.run_cli("create", "T-007-DEMO", "--parent", "T-007", "--task", "Offline demo", "--check", "unit suite",
                     "--execution-plan", json.dumps(self.plan(2)))
        directory = self.root / ".codex-sync/tasks/T-007-DEMO"
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
        transcript.append(self.run_cli("consume", directory.name, "--revision", str(revision + 1), "--review", "ACCEPTED: offline demonstration only").stdout.strip())
        self.run_cli("validate", directory.name)
        print("\n" + "\n".join(transcript))


if __name__ == "__main__":
    unittest.main()
