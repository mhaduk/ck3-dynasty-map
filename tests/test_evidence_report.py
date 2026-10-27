import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import evidence_report as er


class EvidenceReportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        (self.root / ".codex-sync").mkdir()
        (self.root / "evidence").mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def write_json(self, rel, value):
        data = json.dumps(value, separators=(",", ":")).encode()
        (self.root / rel).write_bytes(data)
        return data

    def manifest(self, artifacts, links=(), raw=None):
        value = {"schema": "evidence-inventory-input/1", "task_id": "T-008", "artifacts": artifacts, "links": list(links)}
        data = raw if raw is not None else json.dumps(value, separators=(",", ":")).encode()
        (self.root / "manifest.json").write_bytes(data)
        return value

    def artifact(self, ident, rel, kind, data, required=True):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return {"id": ident, "path": rel, "required": required, "kind": kind,
                "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

    def run_report(self, output=".codex-sync/report.json"):
        return er.build_report(self.root, "manifest.json", output)

    def preflight_result(self, status="PASS", requested=False, **changes):
        value = {"schema": "mod-preflight-result/1", "status": status, "exit_code": 0 if status == "PASS" else 1,
                 "source_coverage": "COMPLETE", "source_files": 2, "source_version_check": "NOT_REQUESTED",
                 "installed_requested": requested, "installed_coverage": "COMPLETE" if requested else "NOT_REQUESTED",
                 "installed_files": 2 if requested else None, "installed_version_check": "NOT_REQUESTED",
                 "comparison": "MATCH" if requested else "NOT_REQUESTED", "findings": [],
                 "limits": ["Offline file checks only; CK3 syntax, references/API, runtime/load/save, RGB and user acceptance remain unverified."]}
        value.update(changes)
        return value

    def test_mod_preflight_adapter_projects_literal_status_without_producer(self):
        for status in ("PASS", "FAIL", "INCOMPLETE"):
            value = self.preflight_result(status, requested=True,
                findings=[] if status == "PASS" else [{"scope": "source", "code": "missing_bom", "count": 1}])
            data = json.dumps(value, separators=(",", ":")).encode()
            item = self.artifact("preflight", "evidence/preflight.json", "mod-preflight", data)
            self.manifest([item])
            _, output, state = self.run_report(f".codex-sync/{status}.json")
            report = json.loads(output); row = report["artifacts"][0]
            self.assertEqual(state, "COMPLETE")
            self.assertEqual(row["selected_upstream_fields"]["status"], status)
            self.assertEqual(row["selected_upstream_fields"]["exit_code"], value["exit_code"])
            self.assertNotIn("limits", row["selected_upstream_fields"])

    def test_mod_preflight_required_unknowns_and_pinned_link_trust(self):
        value = self.preflight_result("FAIL", findings=[{"scope": "source", "code": "missing_bom", "count": 1}])
        a = self.artifact("a", "evidence/a.json", "mod-preflight", json.dumps(value).encode())
        link = {"id": "same-status", "from": {"artifact": "a", "field": "status"}, "to": {"artifact": "a", "field": "status"}}
        self.manifest([a], [link]); _, output, state = self.run_report()
        self.assertEqual(state, "COMPLETE")
        self.assertEqual(json.loads(output)["links"][0]["state"], "MATCH")
        other_value = self.preflight_result("PASS")
        b = self.artifact("b", "evidence/b.json", "mod-preflight", json.dumps(other_value).encode())
        self.manifest([a, b], [{"id": "different-status", "from": {"artifact": "a", "field": "status"},
                               "to": {"artifact": "b", "field": "status"}}])
        _, output, state = self.run_report(".codex-sync/status-mismatch.json")
        self.assertEqual(state, "INCOMPLETE")
        self.assertEqual(json.loads(output)["links"][0]["state"], "MISMATCH")
        self.manifest([a], [{"id": "list-endpoint", "from": {"artifact": "a", "field": "findings"},
                            "to": {"artifact": "a", "field": "status"}}])
        with self.assertRaises(er.Invalid): self.run_report(".codex-sync/list-link.json")
        a["bytes"] += 1
        self.manifest([a], [link]); _, output, state = self.run_report(".codex-sync/pin.json")
        self.assertEqual(state, "INCOMPLETE")
        self.assertEqual(json.loads(output)["links"][0]["state"], "UNKNOWN")

    def test_mod_preflight_invalid_values_are_redacted_and_link_unknown(self):
        mutations = [
            {"schema": "future-private-schema"},
            {"remove": "source_version_check"},
            {"source_files": True},
            {"exit_code": True},
            {"status": "UNKNOWN-PRIVATE"},
            {"findings": [{"scope": "source", "code": "private/path", "count": 1}]},
            {"findings": [{"scope": "source", "code": "unknown_code", "count": 1}]},
            {"findings": [{"scope": "source", "code": "missing_bom", "count": -1}]},
            {"findings": [{"scope": "source", "code": "missing_bom", "count": 1}] * 129},
            {"installed_files": None, "installed_requested": True},
        ]
        for index, change in enumerate(mutations):
            value = self.preflight_result("FAIL")
            if "remove" in change:
                value.pop(change["remove"])
                change = {}
            value.update(change)
            ident = f"p{index}"
            a = self.artifact(ident, f"evidence/{ident}.json", "mod-preflight", json.dumps(value).encode())
            link = {"id": f"l{index}", "from": {"artifact": ident, "field": "status"}, "to": {"artifact": ident, "field": "status"}}
            self.manifest([a], [link]); _, output, state = self.run_report(f".codex-sync/invalid-{index}.json")
            report = json.loads(output)
            self.assertEqual(state, "INCOMPLETE")
            self.assertEqual(report["links"][0]["state"], "UNKNOWN")
            self.assertNotIn(b"private/path", output)
            self.assertNotIn(b"UNKNOWN-PRIVATE", output)

    def test_mod_preflight_subprocess_json_pipeline_preserves_source_exit_separately(self):
        checker = str(Path(er.__file__).with_name("check_mod_preflight.py"))
        cases = []
        passing = self.root / "passing"; passing.mkdir()
        (passing / "descriptor.mod").write_text('name = "Demo"\nversion = "1"\nsupported_version = "y"\n')
        failing = self.root / "failing"; failing.mkdir()
        (failing / "descriptor.mod").write_text('name = "Demo"\nversion = "1"\nsupported_version = "x"\n')
        cases.extend(((passing, "PASS", 0), (failing, "FAIL", 1), (self.root / "unavailable", "INCOMPLETE", 1)))
        for index, (payload, status, source_exit) in enumerate(cases):
            command = [sys.executable, checker, str(payload), "--expected-version", "y", "--json"]
            produced = subprocess.run(command, capture_output=True)
            self.assertEqual(produced.returncode, source_exit)
            self.assertEqual(produced.stderr, b"")
            result = json.loads(produced.stdout)
            self.assertEqual(result["status"], status)
            self.assertEqual(result["exit_code"], source_exit)
            self.assertNotIn(str(payload).encode(), produced.stdout)
            item = self.artifact(f"source{index}", f"evidence/source{index}.json", "mod-preflight", produced.stdout)
            self.manifest([item])
            _, output, inventory_state = self.run_report(f".codex-sync/pipeline-{index}.json")
            report = json.loads(output)
            self.assertEqual(inventory_state, "COMPLETE")
            self.assertEqual(report["inventory_completeness"], "COMPLETE")
            self.assertEqual(report["artifacts"][0]["selected_upstream_fields"]["status"], status)

    def test_mod_preflight_rejects_findings_limit_duplicate_and_unknown_link_fields(self):
        value = self.preflight_result("FAIL", findings=[{"scope": "source", "code": "missing_bom", "count": 1},
                                                          {"scope": "source", "code": "missing_bom", "count": 2}])
        projection, issues = er._projection("mod-preflight", value)
        self.assertIn("duplicate_finding", issues)
        self.assertNotIn("private", json.dumps(projection))
        value = self.preflight_result("FAIL", findings=[{"scope": "source", "code": "missing_bom", "count": 2**31}])
        _, issues = er._projection("mod-preflight", value)
        self.assertIn("invalid_finding_count", issues)
        for count in (True, 1.5, -1):
            value = self.preflight_result("FAIL", findings=[{"scope": "source", "code": "missing_bom", "count": count}])
            _, issues = er._projection("mod-preflight", value)
            self.assertIn("invalid_finding_count", issues)

    def test_mod_preflight_malformed_finding_scalars_are_finite_and_redacted(self):
        sentinel = "PRIVATE-FINDING-SENTINEL"
        for bad in ([sentinel], {"secret": sentinel}, None, True, 7):
            for field in ("scope", "code"):
                value = self.preflight_result("FAIL", findings=[{"scope": "source", "code": "missing_bom", "count": 1}])
                value["findings"][0][field] = bad
                projection, issues = er._projection("mod-preflight", value)
                self.assertIn("unsupported_finding", issues)
                self.assertEqual(projection["findings"], [])
                self.assertNotIn(sentinel, json.dumps(projection))

    def test_mod_preflight_malformed_finding_subprocess_required_and_optional(self):
        for required in (True, False):
            value = self.preflight_result("FAIL", findings=[{"scope": ["PRIVATE"], "code": "missing_bom", "count": 1}])
            data = json.dumps(value).encode()
            item = self.artifact("bad", "evidence/bad.json", "mod-preflight", data, required=required)
            link = {"id": "bad-status", "from": {"artifact": "bad", "field": "status"}, "to": {"artifact": "bad", "field": "status"}}
            self.manifest([item], [link])
            output_rel = f".codex-sync/malformed-{required}.json"
            command = [sys.executable, str(Path(er.__file__)), "--root", str(self.root), "--manifest", "manifest.json", "--output", output_rel]
            result = subprocess.run(command, capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, b"INCOMPLETE\n")
            self.assertEqual(result.stderr, b"")
            output = (self.root / output_rel).read_bytes()
            report = json.loads(output)
            self.assertEqual(report["links"][0]["state"], "UNKNOWN")
            self.assertNotIn(b"PRIVATE", output)
            self.assertNotIn(b"PRIVATE", result.stderr)
            self.assertTrue((self.root / output_rel).is_file())
            self.assertEqual(report["inventory_completeness"], "INCOMPLETE")

        value = self.preflight_result("FAIL", findings=[{"scope": {"secret": "PRIVATE"}, "code": "missing_bom", "count": 1}])
        data = json.dumps(value).encode()
        item = self.artifact("optional", "evidence/optional.json", "mod-preflight", data, required=False)
        self.manifest([item])
        output_rel = ".codex-sync/optional-gap.json"
        command = [sys.executable, str(Path(er.__file__)), "--root", str(self.root), "--manifest", "manifest.json", "--output", output_rel]
        result = subprocess.run(command, capture_output=True)
        self.assertEqual(result.returncode, 0)
        report = json.loads((self.root / output_rel).read_bytes())
        self.assertEqual(report["inventory_completeness"], "COMPLETE_WITH_OPTIONAL_GAPS")
        self.assertNotIn(b"PRIVATE", (self.root / output_rel).read_bytes())

    def test_complete_inventory_preserves_incomplete_upstream_and_is_deterministic(self):
        status = {"id": "child", "parent_id": "T-008", "attempt": 1, "revision": 3, "status": "COMPLETED",
                  "owner": "PRIVATE", "inputs": {"private/path": "secret"}}
        classification = {"schema": 2, "status": "INCOMPLETE", "exit_code": 2, "capture_completeness": "INCOMPLETE",
                          "batches": [{"sequence": 1, "availability": "AVAILABLE", "record_completeness": "INCOMPLETE",
                                       "classification_match": "UNVERIFIED", "intended_rgb_mapping": "UNVERIFIED", "records": ["secret"]}]}
        a = self.artifact("receipt", "evidence/status.json", "handoff-status", json.dumps(status).encode())
        b = self.artifact("audit", "evidence/classification.json", "classification", json.dumps(classification).encode())
        link = {"id": "same-parent", "from": {"artifact": "receipt", "field": "parent_id"}, "to": {"artifact": "receipt", "field": "parent_id"}}
        self.manifest([a, b], [link])
        p1, out1, state = self.run_report()
        p1.write_bytes(out1)
        _, out2, _ = self.run_report(".codex-sync/second.json")
        report = json.loads(out1)
        self.assertEqual(state, "COMPLETE")
        self.assertEqual(out1, out2)
        self.assertEqual(report["artifacts"][0]["selected_upstream_fields"]["status"], "COMPLETED")
        self.assertEqual(report["artifacts"][1]["selected_upstream_fields"]["status"], "INCOMPLETE")
        self.assertNotIn("PRIVATE", out1.decode()); self.assertNotIn("secret", out1.decode())
        self.assertNotIn("owner", report["artifacts"][0]["selected_upstream_fields"])

    def test_log_delta_optional_gap_literal_projects_and_inputs_unchanged(self):
        obj = {"format": 1, "checkpoint_id": "checkpoint-1", "baseline_id": "baseline-1",
               "interval_status": "COMPLETE_WITH_OPTIONAL_GAPS", "expectation_status": "UNVERIFIED_INCOMPLETE_EVIDENCE",
               "observation_status": "NONE_OBSERVED_IN_ANALYZED_LINES"}
        data = json.dumps(obj, separators=(",", ":")).encode()
        a = self.artifact("delta", "evidence/delta.json", "log-delta", data)
        self.manifest([a])
        before = hashlib.sha256((self.root / a["path"]).read_bytes()).hexdigest()
        _, output, state = self.run_report()
        self.assertEqual(state, "COMPLETE")
        projection = json.loads(output)["artifacts"][0]["selected_upstream_fields"]
        self.assertEqual(projection["interval_status"], obj["interval_status"])
        self.assertEqual(projection["expectation_status"], "UNVERIFIED_INCOMPLETE_EVIDENCE")
        self.assertEqual(hashlib.sha256((self.root / a["path"]).read_bytes()).hexdigest(), before)

    def test_handoff_synthetic_example(self):
        obj = {"id": "child-1", "parent_id": "T-008", "attempt": 1, "revision": 3, "status": "COMPLETED"}
        data = json.dumps(obj, separators=(",", ":")).encode()
        a = self.artifact("receipt", "evidence/status.json", "handoff-status", data)
        self.manifest([a]); _, output, state = self.run_report()
        projected = json.loads(output)["artifacts"][0]["selected_upstream_fields"]
        self.assertEqual(state, "COMPLETE")
        self.assertEqual(projected, {k: obj[k] for k in ("id", "parent_id", "attempt", "revision", "status")})

    def test_cli_smokes_synthetic_producer_contracts(self):
        examples = (("handoff-status", "receipt", {"id": "child-1", "parent_id": "T-008", "attempt": 1, "revision": 3, "status": "COMPLETED"}),
                    ("log-delta", "delta", {"format": 1, "checkpoint_id": "checkpoint-1", "baseline_id": "baseline-1",
                     "interval_status": "COMPLETE_WITH_OPTIONAL_GAPS", "expectation_status": "UNVERIFIED_INCOMPLETE_EVIDENCE",
                     "observation_status": "NONE_OBSERVED_IN_ANALYZED_LINES"}))
        for index, (kind, ident, value) in enumerate(examples):
            data = json.dumps(value, separators=(",", ":")).encode()
            rel = f"evidence/example-{index}.json"
            item = self.artifact(ident, rel, kind, data)
            self.manifest([item])
            output = f".codex-sync/example-{index}-report.json"
            command = [sys.executable, str(Path(er.__file__)), "--root", str(self.root), "--manifest", "manifest.json", "--output", output]
            run = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(json.loads((self.root / output).read_text())["inventory_completeness"], "COMPLETE")

    def test_source_failed_and_mismatches_are_literal_and_incomplete(self):
        item = {"id": "a", "parent_id": "p", "attempt": 1, "revision": 2, "status": "FAILED"}
        a = self.artifact("a", "evidence/a.json", "handoff-status", json.dumps(item).encode())
        self.manifest([a]); (self.root / a["path"]).write_bytes(b"changed")
        _, out, state = self.run_report()
        row = json.loads(out)["artifacts"][0]
        self.assertEqual(state, "INCOMPLETE"); self.assertEqual(row["pin_state"], "MISMATCH")
        self.assertEqual(row["selected_upstream_fields"], {})

    def test_size_mismatch_and_conflicting_source_verdicts_remain_distinct(self):
        c1 = {"schema": 2, "status": "FAIL", "exit_code": 1, "capture_completeness": "COMPLETE", "batches": []}
        c2 = {"schema": 2, "status": "INCOMPLETE", "exit_code": 2, "capture_completeness": "INCOMPLETE", "batches": []}
        a = self.artifact("a", "evidence/a.json", "classification", json.dumps(c1).encode())
        b = self.artifact("b", "evidence/b.json", "classification", json.dumps(c2).encode())
        a["bytes"] += 1
        link = {"id": "different-verdicts", "from": {"artifact": "a", "field": "status"}, "to": {"artifact": "b", "field": "status"}}
        self.manifest([a, b], [link]); _, out, state = self.run_report()
        report = json.loads(out)
        self.assertEqual(state, "INCOMPLETE")
        self.assertEqual(report["links"][0]["state"], "UNKNOWN")
        self.assertEqual(report["artifacts"][0]["pin_state"], "MISMATCH")
        self.assertEqual(report["artifacts"][1]["selected_upstream_fields"]["status"], "INCOMPLETE")

    def test_missing_optional_and_required(self):
        optional = {"id": "opt", "path": "evidence/absent.json", "required": False, "kind": "opaque", "bytes": 1, "sha256": "0" * 64}
        self.manifest([optional]); _, out, state = self.run_report()
        self.assertEqual(state, "COMPLETE_WITH_OPTIONAL_GAPS")
        self.assertEqual(json.loads(out)["missing"][0]["code"], "optional_missing")
        optional["required"] = True; self.manifest([optional]); _, _, state = self.run_report(".codex-sync/required.json")
        self.assertEqual(state, "INCOMPLETE")

    def test_optional_unsupported_is_gap_but_malformed_present_is_incomplete(self):
        data = b'{"format":9}'
        item = self.artifact("opt", "evidence/unsupported.json", "log-delta", data, required=False)
        self.manifest([item]); _, _, state = self.run_report()
        self.assertEqual(state, "COMPLETE_WITH_OPTIONAL_GAPS")
        malformed = self.artifact("opt", "evidence/unsupported.json", "log-delta", b"{broken", required=False)
        self.manifest([malformed]); _, _, state = self.run_report(".codex-sync/malformed.json")
        self.assertEqual(state, "INCOMPLETE")

    def test_link_mismatch_and_unknown_schema(self):
        d1 = json.dumps({"format": 1, "checkpoint_id": "new", "baseline_id": "old", "interval_status": "INCOMPLETE",
                         "expectation_status": "UNVERIFIED_INCOMPLETE_EVIDENCE", "observation_status": "NONE_OBSERVED_IN_ANALYZED_LINES"}).encode()
        d2 = json.dumps({"format": 1, "checkpoint_id": "older", "baseline_id": "x", "interval_status": "INCOMPLETE",
                         "expectation_status": "UNVERIFIED_INCOMPLETE_EVIDENCE", "observation_status": "NONE_OBSERVED_IN_ANALYZED_LINES"}).encode()
        a = self.artifact("a", "evidence/a.json", "log-delta", d1); b = self.artifact("b", "evidence/b.json", "log-delta", d2)
        link = {"id": "stale", "from": {"artifact": "a", "field": "checkpoint_id"}, "to": {"artifact": "b", "field": "checkpoint_id"}}
        self.manifest([a, b], [link]); _, out, state = self.run_report()
        self.assertEqual(state, "INCOMPLETE"); self.assertEqual(json.loads(out)["links"][0]["state"], "MISMATCH")
        d2 = d2.replace(b'"format": 1', b'"format": 9')
        b = self.artifact("b", "evidence/b.json", "log-delta", d2); self.manifest([a, b], [link])
        _, out, state = self.run_report(".codex-sync/unknown.json")
        self.assertEqual(state, "INCOMPLETE")
        self.assertEqual(json.loads(out)["links"][0]["state"], "UNKNOWN")

    def test_handoff_revision_and_id_links_are_explicit(self):
        a = {"id": "child-a", "parent_id": "T-008", "attempt": 1, "revision": 3, "status": "COMPLETED"}
        b = {"id": "child-b", "parent_id": "T-008", "attempt": 1, "revision": 2, "status": "FAILED"}
        aa = self.artifact("a", "evidence/a.json", "handoff-status", json.dumps(a).encode())
        bb = self.artifact("b", "evidence/b.json", "handoff-status", json.dumps(b).encode())
        links = [
            {"id": "revision", "from": {"artifact": "a", "field": "revision"}, "to": {"artifact": "b", "field": "revision"}},
            {"id": "child-id", "from": {"artifact": "a", "field": "id"}, "to": {"artifact": "b", "field": "id"}},
            {"id": "literal-status", "from": {"artifact": "a", "field": "status"}, "to": {"artifact": "b", "field": "status"}},
        ]
        self.manifest([aa, bb], links); _, out, state = self.run_report()
        report = json.loads(out)
        self.assertEqual(state, "INCOMPLETE")
        self.assertEqual([link["state"] for link in report["links"]], ["MISMATCH", "MISMATCH", "MISMATCH"])
        self.assertEqual([row["selected_upstream_fields"]["status"] for row in report["artifacts"]], ["COMPLETED", "FAILED"])

    def test_validation_duplicate_keys_types_limits_and_paths(self):
        with self.assertRaises(er.Invalid):
            er._json(b'{"a":1,"a":2}')
        with self.assertRaises(er.Invalid): er._json(b'{"x":NaN}')
        with self.assertRaises(er.Invalid): er._json(b'{"x":1e999}')
        with self.assertRaises(er.Invalid): er._json(b'{"nested":[-1e999]}')
        with self.assertRaises(er.Invalid): er._json((b"[" * 65) + (b"]" * 65))
        bad = self.artifact("a", "evidence/a", "opaque", b"x"); bad["bytes"] = True
        self.manifest([bad])
        with self.assertRaises(er.Invalid): self.run_report()
        for path in ("../secret", "/absolute", "a/./b", "a//b", "a\\b"):
            with self.assertRaises(er.Invalid, msg=path): er._path(path)
        with self.assertRaises(er.Invalid): er._path("a/../b")

    def test_symlink_input_parent_output_parent_and_nonregular(self):
        (self.root / "linkdir").symlink_to(self.root / "evidence", target_is_directory=True)
        with self.assertRaises(er.Invalid): er._safe_target(self.root, "linkdir/file", must_exist=False)
        (self.root / "evidence/link.json").symlink_to(self.root / "evidence/real.json")
        with self.assertRaises(er.Invalid): er._safe_target(self.root, "evidence/link.json", must_exist=True)
        self.assertIsNone(er._safe_target(self.root, ".codex-sync/missing/out.json", must_exist=False))
        (self.root / "evidence/fifo").write_text("x")
        os.mkfifo(self.root / "evidence/pipe")
        with self.assertRaises(er.Invalid): er._read_regular(self.root / "evidence/pipe", 20)

    def test_output_collision_never_overwrites(self):
        a = self.artifact("a", "evidence/a", "opaque", b"x"); self.manifest([a])
        destination = self.root / ".codex-sync/existing.json"; destination.write_bytes(b"keep")
        with self.assertRaises(er.Invalid): self.run_report(".codex-sync/existing.json")
        self.assertEqual(destination.read_bytes(), b"keep")

    def test_cli_exit_is_inventory_only(self):
        data = json.dumps({"schema": 2, "status": "INCOMPLETE", "exit_code": 2, "capture_completeness": "INCOMPLETE", "batches": []}).encode()
        a = self.artifact("x", "evidence/x.json", "classification", data); self.manifest([a])
        command = [sys.executable, str(Path(er.__file__)), "--root", str(self.root), "--manifest", "manifest.json", "--output", ".codex-sync/cli.json"]
        run = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0); self.assertIn("COMPLETE", run.stdout)
        self.assertEqual(json.loads((self.root / ".codex-sync/cli.json").read_text())["artifacts"][0]["selected_upstream_fields"]["status"], "INCOMPLETE")
        self.assertEqual(json.loads((self.root / ".codex-sync/cli.json").read_text())["inventory_completeness"], "COMPLETE")

    def test_output_must_be_private_sync_path(self):
        a = self.artifact("a", "evidence/a", "opaque", b"x"); self.manifest([a])
        with self.assertRaises(er.Invalid): self.run_report("evidence/public.json")

    def test_invalid_adapter_identities_are_redacted_and_links_unknown(self):
        sentinels = ("/private/secret", "alice@example.invalid", "bad\nvalue", "x" * 65)
        index = 0
        for field in ("id", "parent_id"):
            for sentinel in sentinels:
                obj = {"id": "child-1", "parent_id": "T-008", "attempt": 1, "revision": 1, "status": "COMPLETED"}
                obj[field] = sentinel
                ident = f"a{index}"
                item = self.artifact(ident, f"evidence/{ident}.json", "handoff-status", json.dumps(obj).encode())
                link = {"id": f"link{index}", "from": {"artifact": ident, "field": field}, "to": {"artifact": ident, "field": "parent_id"}}
                self.manifest([item], [link])
                _, output, state = self.run_report(f".codex-sync/identity-{index}.json")
                report = json.loads(output)
                self.assertEqual(state, "INCOMPLETE")
                self.assertNotIn(sentinel.encode(), output)
                self.assertEqual(report["links"][0]["state"], "UNKNOWN")
                self.assertNotIn(field, report["artifacts"][0]["selected_upstream_fields"])
                index += 1

    def test_log_identity_invalidity_is_redacted(self):
        for index, field in enumerate(("checkpoint_id", "baseline_id")):
            obj = {"format": 1, "checkpoint_id": "checkpoint-1", "baseline_id": "baseline-1",
                   "interval_status": "COMPLETE", "expectation_status": "MET", "observation_status": "NONE_OBSERVED_IN_ANALYZED_LINES"}
            obj[field] = "private/path"
            item = self.artifact("delta", "evidence/delta.json", "log-delta", json.dumps(obj).encode())
            self.manifest([item]); _, output, state = self.run_report(f".codex-sync/log-identity-{index}.json")
            self.assertEqual(state, "INCOMPLETE")
            self.assertNotIn(b"private/path", output)
            self.assertNotIn(field, json.loads(output)["artifacts"][0]["selected_upstream_fields"])

    def test_manifest_overflow_is_generic_invocation_error_and_evidence_overflow_incomplete(self):
        payload = b'{"schema":"evidence-inventory-input/1","task_id":"T-008","artifacts":[],"links":[],"unused":1e999}'
        self.manifest([], raw=payload)
        command = [sys.executable, str(Path(er.__file__)), "--root", str(self.root), "--manifest", "manifest.json", "--output", ".codex-sync/overflow.json"]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("1e999", result.stderr)
        self.assertFalse((self.root / ".codex-sync/overflow.json").exists())
        data = b'{"schema":2,"status":"INCOMPLETE","exit_code":2,"capture_completeness":"INCOMPLETE","batches":[],"ignored":1e999}'
        item = self.artifact("audit", "evidence/audit.json", "classification", data)
        self.manifest([item]); _, output, state = self.run_report(".codex-sync/evidence-overflow.json")
        self.assertEqual(state, "INCOMPLETE")
        self.assertNotIn(b"1e999", output)

    def test_root_and_ancestor_symlinks_rejected(self):
        alias = self.root / "root-alias"
        alias.symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(er.Invalid): er.build_report(alias, "manifest.json", ".codex-sync/no.json")
        with self.assertRaises(er.Invalid): er._checked_root(alias / ".." / self.root.name)
        ancestor = self.root / "ancestor-real"
        nested = ancestor / "repo"
        nested.mkdir(parents=True)
        alias_parent = self.root / "ancestor-alias"
        alias_parent.symlink_to(ancestor, target_is_directory=True)
        with self.assertRaises(er.Invalid): er._checked_root(alias_parent / "repo")

    def test_optional_total_limit_failure_is_incomplete_and_no_later_reads(self):
        one = self.artifact("one", "evidence/one", "opaque", b"x", required=False)
        two = self.artifact("two", "evidence/two", "opaque", b"y", required=False)
        self.manifest([one, two])
        calls = []
        original = er._read_regular
        def counted(path, limit):
            calls.append(path.name)
            return original(path, limit)
        with mock.patch.object(er, "TOTAL_LIMIT", 2), mock.patch.object(er, "ARTIFACT_LIMIT", 1), mock.patch.object(er, "_read_regular", side_effect=counted):
            _, output, state = self.run_report()
        report = json.loads(output)
        self.assertEqual(state, "INCOMPLETE")
        self.assertEqual(calls, ["manifest.json", "one"])
        self.assertEqual(report["artifacts"][1]["adapter_issues"], ["TOTAL_LIMIT"])

    def test_failed_read_reservation_is_not_reclaimed(self):
        one = self.artifact("one", "evidence/one", "opaque", b"x", required=False)
        two = self.artifact("two", "evidence/two", "opaque", b"y", required=False)
        self.manifest([one, two])
        calls = []
        original = er._read_regular
        def drifting(path, limit):
            if path.name == "manifest.json": return original(path, limit)
            calls.append((path.name, limit + 1))
            raise er.Invalid("input_drift")
        with mock.patch.object(er, "TOTAL_LIMIT", 2), mock.patch.object(er, "ARTIFACT_LIMIT", 1), mock.patch.object(er, "_read_regular", side_effect=drifting):
            _, output, state = self.run_report()
        report = json.loads(output)
        self.assertEqual(state, "INCOMPLETE")
        self.assertEqual(calls, [("one", 2)])
        self.assertEqual(report["artifacts"][0]["adapter_issues"], ["input_drift"])
        self.assertEqual(report["artifacts"][1]["adapter_issues"], ["TOTAL_LIMIT"])

    def test_manifest_artifact_link_and_per_file_caps(self):
        item = self.artifact("a", "evidence/a", "opaque", b"xx")
        self.manifest([item])
        with mock.patch.object(er, "ARTIFACT_LIMIT", 1):
            with self.assertRaisesRegex(er.Invalid, "artifact_size_limit"): self.run_report()
        with mock.patch.object(er, "MANIFEST_LIMIT", 1):
            with self.assertRaisesRegex(er.Invalid, "non_regular_or_oversized_input"): self.run_report(".codex-sync/manifest-cap.json")
        valid_items = [dict(item, id=f"a{idx}", path=f"evidence/a{idx}") for idx in range(2)]
        self.manifest(valid_items)
        with mock.patch.object(er, "ARTIFACTS_LIMIT", 1):
            with self.assertRaisesRegex(er.Invalid, "artifact_count_limit"): self.run_report(".codex-sync/artifact-cap.json")
        item2 = dict(item, id="b", path="evidence/b")
        self.manifest([item, item2], [{"id":"link","from":{"artifact":"a","field":"sha256"},"to":{"artifact":"b","field":"sha256"}}])
        with mock.patch.object(er, "LINKS_LIMIT", 0):
            with self.assertRaisesRegex(er.Invalid, "link_count_limit"): self.run_report(".codex-sync/link-cap.json")


if __name__ == "__main__":
    unittest.main()
