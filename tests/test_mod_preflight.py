import hashlib
import json
import argparse
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import check_mod_preflight as preflight


class ModPreflightTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def payload(self, name="source", version="1.20.1.2"):
        root = self.root / name
        root.mkdir()
        (root / "descriptor.mod").write_text(f'name = "Demo"\nversion = "1"\nsupported_version = "{version}"\n')
        (root / "gfx").mkdir()
        (root / "gfx" / "mode.txt").write_bytes(b"\xef\xbb\xbfmode = { }\n")
        return root

    def cli(self, root, *args):
        return subprocess.run([sys.executable, str(ROOT / "scripts/check_mod_preflight.py"), str(root), *args],
                              capture_output=True)

    def structured(self, root, *args):
        run = self.cli(root, *args, "--json")
        self.assertEqual(run.stderr, b"")
        return run, json.loads(run.stdout)

    def test_legacy_cli_explicit_output_and_exit_contract(self):
        root = self.payload()
        run = self.cli(root)
        self.assertEqual(run.returncode, 0)
        self.assertEqual(run.stdout.decode(), "Preflight passed: 2 source files.\nOffline file checks only; CK3 syntax, APIs and runtime compatibility remain unverified.\n")
        (root / "gfx/mode.txt").write_bytes(b"mode = { }\n")
        run = self.cli(root)
        self.assertEqual(run.returncode, 1)
        self.assertEqual(run.stdout, b"")
        self.assertEqual(run.stderr.decode(), "FAIL source/gfx/mode.txt: requires exactly one leading UTF-8 BOM (project convention)\nPreflight failed: 1 finding(s).\n")

    def test_historical_inspect_wrapper_keeps_error_shape(self):
        root = self.payload()
        (root / "coat_of_arms").mkdir()
        errors = []
        inventory = preflight.inspect(root, "source", None, errors)
        self.assertEqual(len(inventory), 2)
        self.assertEqual(errors, ["source/coat_of_arms: misplaced CoA folder; use common/coat_of_arms/coat_of_arms"])
        run = self.cli(root)
        self.assertEqual(run.returncode, 1)
        self.assertEqual(run.stderr.decode(), "FAIL source/coat_of_arms: misplaced CoA folder; use common/coat_of_arms/coat_of_arms\nPreflight failed: 1 finding(s).\n")

    def test_expected_version_and_deterministic_json(self):
        root = self.payload()
        before = {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob("*") if p.is_file()}
        a = self.structured(root, "--expected-version", "1.20.1.2")
        b = self.structured(root, "--expected-version", "1.20.1.2")
        self.assertEqual(a[0].returncode, 0)
        self.assertEqual(a[0].stdout, b[0].stdout)
        self.assertEqual(a[1]["status"], "PASS")
        self.assertEqual(a[1]["source_version_check"], "MATCH")
        self.assertEqual(a[1]["source_files"], 2)
        self.assertEqual(a[1]["installed_files"], None)
        self.assertEqual(a[1]["comparison"], "NOT_REQUESTED")
        self.assertEqual(a[1]["findings"], [])
        after = {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_incomplete_read_and_known_missing_descriptor_are_distinct(self):
        root = self.payload()
        source_file = root / "gfx/mode.txt"
        original = Path.read_bytes
        def denied(path):
            if path == source_file: raise PermissionError("private read failure")
            return original(path)
        with mock.patch.object(Path, "read_bytes", denied):
            findings = preflight.Findings()
            source, complete = preflight._inspect(root, "source", None, findings)
            result = preflight._result(source, None, findings, complete, True, argparse.Namespace(expected_version=None))
        self.assertEqual(result["status"], "INCOMPLETE")
        self.assertEqual(result["source_coverage"], "INCOMPLETE")
        self.assertNotIn("private", json.dumps(result))
        missing = self.payload("missing")
        (missing / "descriptor.mod").unlink()
        _, known = self.structured(missing)
        self.assertEqual(known["status"], "FAIL")
        self.assertEqual(known["source_coverage"], "COMPLETE")

    def test_symlink_plus_absent_descriptor_retains_legacy_diagnostic(self):
        root = self.root / "combined"
        root.mkdir()
        (root / "dangling").symlink_to(root / "absent-target")
        run = self.cli(root)
        self.assertEqual(run.returncode, 1)
        self.assertEqual(run.stdout, b"")
        self.assertEqual(run.stderr.decode(), "FAIL source/dangling: symlinks are not supported in a reviewed payload\nFAIL source/descriptor.mod: required file missing\nPreflight failed: 2 finding(s).\n")
        errors = []
        preflight.inspect(root, "source", None, errors)
        self.assertEqual(errors, ["source/dangling: symlinks are not supported in a reviewed payload",
                                  "source/descriptor.mod: required file missing"])
        structured, result = self.structured(root)
        self.assertEqual(structured.returncode, 1)
        self.assertEqual(result["status"], "INCOMPLETE")
        self.assertEqual(result["source_coverage"], "INCOMPLETE")
        self.assertEqual({row["code"] for row in result["findings"]}, {"symlink", "descriptor_unavailable"})

    def test_invalid_roots_keep_early_diagnostic_only(self):
        missing = self.root / "absent"
        run = self.cli(missing)
        self.assertEqual(run.stderr.decode(), "FAIL source/.: payload root must be an existing ordinary directory\nPreflight failed: 1 finding(s).\n")
        _, result = self.structured(missing)
        self.assertEqual({row["code"] for row in result["findings"]}, {"invalid_root"})

    def test_unreadable_descriptor_preserves_legacy_messages(self):
        root = self.payload()
        descriptor = root / "descriptor.mod"
        original = Path.read_bytes
        def denied(path):
            if path == descriptor: raise PermissionError("private descriptor failure")
            return original(path)
        stderr, stdout = io.StringIO(), io.StringIO()
        with mock.patch.object(Path, "read_bytes", denied), mock.patch("sys.stderr", stderr), mock.patch("sys.stdout", stdout):
            code = preflight.main([str(root)])
        self.assertEqual(code, 1)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue(), "FAIL source/descriptor.mod: cannot read file\nFAIL source/descriptor.mod: required file missing\nPreflight failed: 2 finding(s).\n")
        self.assertNotIn("private", stderr.getvalue())
        errors = []
        with mock.patch.object(Path, "read_bytes", denied):
            preflight.inspect(root, "source", None, errors)
        self.assertEqual(errors, ["source/descriptor.mod: cannot read file",
                                  "source/descriptor.mod: required file missing"])

    def test_bad_version_bom_localization_and_incidental_findings(self):
        root = self.payload(version="wrong")
        (root / "gfx/mode.txt").write_bytes(b"\xef\xbb\xbf\xef\xbb\xbfabc")
        loc = root / "localization/french/bad_l_french.yml"
        loc.parent.mkdir(parents=True)
        loc.write_bytes(b"\xef\xbb\xbfl_english:\n key:0 \"x\"\n")
        invalid = root / "localization/english/broken_l_english.yml"
        invalid.parent.mkdir(parents=True)
        invalid.write_bytes(b"\xff\xfe")
        (root / "README.txt").write_text("private sentinel")
        run, result = self.structured(root, "--expected-version", "expected-private-version")
        self.assertEqual(run.returncode, 1)
        self.assertEqual(result["status"], "FAIL")
        codes = {row["code"] for row in result["findings"]}
        self.assertTrue({"duplicate_bom", "invalid_utf8", "version_mismatch", "loc_folder_mismatch", "loc_filename_mismatch", "incidental_file"} <= codes)
        for forbidden in (str(root), "expected-private-version", "README.txt", "private sentinel"):
            self.assertNotIn(forbidden.encode(), run.stdout)
        duplicate = self.payload("duplicate-declaration")
        (duplicate / "descriptor.mod").write_text('name = "Demo"\nname = "Other"\nversion = "1"\nsupported_version = "x"\n')
        _, result = self.structured(duplicate)
        self.assertIn("descriptor_declaration", {r["code"] for r in result["findings"]})

    def test_installed_match_mismatch_and_incomplete_comparison(self):
        source = self.payload()
        installed = self.payload("installed")
        args = ("--installed", str(installed), "--expected-version", "1.20.1.2")
        run, result = self.structured(source, *args)
        self.assertEqual(run.returncode, 0)
        self.assertEqual(result["comparison"], "MATCH")
        (installed / "gfx/mode.txt").write_bytes(b"\xef\xbb\xbfchanged")
        run, result = self.structured(source, *args)
        self.assertEqual(run.returncode, 1)
        self.assertEqual(result["comparison"], "MISMATCH")
        self.assertIn("bytes_mismatch", {r["code"] for r in result["findings"]})
        (installed / "gfx/mode.txt").unlink()
        (installed / "extra.bin").write_bytes(b"extra")
        _, result = self.structured(source, "--installed", str(installed))
        codes = {r["code"] for r in result["findings"]}
        self.assertTrue({"inventory_missing", "inventory_extra"} <= codes)
        unreadable = self.payload("unreadable")
        denied_path = unreadable / "gfx/mode.txt"
        original = Path.read_bytes
        def deny_installed(path):
            if path == denied_path: raise PermissionError("private read failure")
            return original(path)
        with mock.patch.object(Path, "read_bytes", deny_installed):
            findings = preflight.Findings()
            source_files, source_complete = preflight._inspect(source, "source", None, findings)
            installed_files, installed_complete = preflight._inspect(unreadable, "installed", None, findings)
            result = preflight._result(source_files, installed_files, findings, source_complete, installed_complete,
                                       argparse.Namespace(expected_version=None))
        self.assertEqual(result["comparison"], "UNVERIFIED")
        self.assertIn("inventory_missing", {r["code"] for r in result["findings"]})

    def test_symlink_and_traversal_failure_are_incomplete(self):
        root = self.payload()
        (root / "linked").symlink_to(root / "gfx", target_is_directory=True)
        _, result = self.structured(root)
        self.assertEqual(result["status"], "INCOMPLETE")
        self.assertIn("symlink", {r["code"] for r in result["findings"]})
        with mock.patch("os.walk", side_effect=PermissionError("private traversal")):
            blocked = self.payload("blocked")
            findings = preflight.Findings()
            source, complete = preflight._inspect(blocked, "source", None, findings)
            result = preflight._result(source, None, findings, complete, True, argparse.Namespace(expected_version=None))
        self.assertEqual(result["source_coverage"], "INCOMPLETE")
        self.assertIn("traversal_error", {r["code"] for r in result["findings"]})


if __name__ == "__main__":
    unittest.main()
