import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/task_ai_cost.py"
spec = importlib.util.spec_from_file_location("task_ai_cost", SCRIPT)
cost = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cost)


def usage(i=10, c=4, o=3, r=1):
    return dict(zip(cost.FIELDS, [i, c, o, r, i + o]))


def context(turn="t", model="model"):
    return {"type": "turn_context", "payload": {"turn_id": turn, "model": model}}


def response(identity="r", thread="s", turn="t", u=None):
    return {"type": "token_usage_record", "payload": {
        "thread_id": thread, "turn_id": turn, "response_id": identity,
        "usage": usage() if u is None else u}}


def counter(u):
    return {"type": "event_msg", "payload": {"type": "token_count", "info": {
        "total_token_usage": u, "last_token_usage": usage()}}}


class Accounting(unittest.TestCase):
    def test_responses_ignore_cumulative_and_last_duplicates(self):
        events = [context(), response(), counter(usage()), response()]
        self.assertEqual(len(list(cost.records(events, "s", {}))), 1)

    def test_fork_and_child_global_dedup(self):
        seen = {}
        self.assertEqual(len(list(cost.records([context(), response()], "s", seen))), 1)
        # Inherited parent records are omitted in the child's file.
        self.assertEqual(list(cost.records([context(), response()], "child", seen)), [])
        self.assertEqual(list(cost.records([context(), response()], "s", seen)), [])
        self.assertEqual(len(list(cost.records([context(), response("child-r", "child")], "child", seen))), 1)

    def test_duplicate_conflict(self):
        with self.assertRaises(ValueError):
            list(cost.records([context(), response(), response(u=usage(20))], "s", {}))

    def test_missing_response_identity(self):
        with self.assertRaises(ValueError):
            list(cost.records([response(None)], "s", {}))

    def test_cumulative_repeat_and_reset(self):
        es = [context(), counter(usage()), counter(usage()), counter(usage(20,8,6,2)),
              counter(usage(1,0,1,0)), counter(usage(11,4,4,1))]
        rows = list(cost.records(es, "s", {}, "cumulative"))
        self.assertEqual([r["usage"]["total_tokens"] for r in rows], [13,13])

    def test_model_and_turn_boundary_not_assigned(self):
        es = [context(), counter(usage()), context("u", "other"), counter(usage(20,8,6,2))]
        self.assertIsNone(list(cost.records(es, "s", {}, "cumulative"))[0]["turn"])

    def test_model_change_response(self):
        es = [context(model="one"), response(), context(model="two"), response("r2")]
        self.assertEqual([r["model"] for r in cost.records(es,"s",{})], ["one","two"])

    def test_unknown_model_missing_details(self):
        rows = list(cost.records([response(u={"input_tokens":10,"output_tokens":3,"total_tokens":13})], "s", {}))
        self.assertIsNone(rows[0]["model"])
        self.assertIsNone(rows[0]["usage"]["reasoning_output_tokens"])

    def test_invalid_subsets_and_total(self):
        for u in [usage(c=11), usage(r=4), {**usage(),"total_tokens":99}, usage(i=-1)]:
            with self.subTest(u=u), self.assertRaises(ValueError):
                cost.valid_usage(u)

    def test_subsets_not_addends(self):
        f = cost.fragment({"model":usage()}, "2026-10-22", "Partial.")
        self.assertIn("| model | 10 | 4 | 6 | 3 | 1 | 13 | partial |", f)

    def test_unavailable_is_not_zero(self):
        self.assertIn("| unknown | N/A | N/A", cost.fragment({}, "date", "Missing."))

    def test_cli_mapping_multitask_and_frozen_prefix(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            src, mapping, out = [d/x for x in ["source.jsonl","mapping.json","result.json"]]
            raw = b"".join((json.dumps(e)+"\n").encode() for e in [context(),response(),context("u"),response("r2",turn="u")])
            src.write_bytes(raw+b'{"later":true}\n')
            m={"version":1,"cutoff":"date","sources":[{"path":str(src),"size_bytes":len(raw),"sha256":cost.sha(raw),"thread":"s"}],"assignments":[{"source":0,"turn":"t","tasks":["A"]},{"source":0,"turn":"u","tasks":["A","B"]}]}
            mapping.write_text(json.dumps(m))
            subprocess.run([sys.executable,str(SCRIPT),"account","--mapping",str(mapping),"--output",str(out)],check=True)
            result=json.loads(out.read_text())
            self.assertEqual(result["totals"]["A"]["model"]["total_tokens"],13)
            self.assertIsNone(result["records"][1]["task"])
            # A changed frozen byte, unlike later appends, is rejected.
            src.write_bytes(b"X"+raw[1:])
            with self.assertRaises(ValueError):cost.account(m)

    def test_overlapping_mapping_refused(self):
        a={"source":0,"turn":"t","tasks":["A"]}
        with self.assertRaises(ValueError):
            cost.account({"version":1,"assignments":[a,a]})


class Descriptions(unittest.TestCase):
    def setUp(self):
        self.fragment=cost.fragment({"m":usage()},"date","Partial.")

    def replace(self,body,fragment=None):
        return cost.replace_suffix(body,fragment or self.fragment,cost.sha(body.encode()))

    def test_insert_preserve_bytes_idempotence(self):
        body="Original\r\nUnicode: ł\n"
        once=self.replace(body)
        self.assertTrue(once.startswith(body))
        self.assertEqual(self.replace(once),once)
        self.assertEqual(once.count(cost.START),1)

    def test_replace_only_suffix(self):
        body="Prefix \r\n\n"+self.fragment+"\n\n"
        new=cost.fragment({},"later","Missing.")
        self.assertEqual(self.replace(body,new),"Prefix \r\n\n"+new+"\n\n")

    def test_malformed_existing_sections(self):
        for body in [cost.START,cost.END,cost.END+cost.START,self.fragment+cost.START,self.fragment+"more text"]:
            with self.subTest(body=body),self.assertRaises(ValueError):self.replace(body)

    def test_gui_context_link_below_total_only_when_history_exists(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            history = root / "docs/telemetry/gui-context/T-012.jsonl"
            history.parent.mkdir(parents=True)
            self.assertEqual(cost.with_context_history(self.fragment, history, root), self.fragment)
            history.write_text(json.dumps({"method": "gui-context/1", "context_tokens": {"status": "estimated"}}) + "\n")
            linked = cost.with_context_history(self.fragment, history, root)
            total = linked.index("| **Total** |")
            link = linked.index("[GUI context history]")
            method = linked.index("Method:")
            self.assertGreater(link, total)
            self.assertLess(link, method)
            self.assertEqual(linked.count("[GUI context history]"), 1)
            self.assertEqual(cost.with_context_history(linked, history, root), linked)

    def test_gui_context_history_rejects_malformed_and_outside_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            history = root / "docs/telemetry/gui-context/T-012.jsonl"
            history.parent.mkdir(parents=True)
            history.write_text("bad\n")
            with self.assertRaisesRegex(ValueError, "malformed"):
                cost.with_context_history(self.fragment, history, root)
            outside = root / "outside.jsonl"
            outside.write_text("{}\n")
            with self.assertRaisesRegex(ValueError, "inside"):
                cost.with_context_history(self.fragment, outside, root)
            linked = history.parent / "linked.jsonl"
            linked.symlink_to(history)
            with self.assertRaisesRegex(ValueError, "symlink"):
                cost.with_context_history(self.fragment, linked, root)

    def test_concurrent_body_drift(self):
        with self.assertRaises(ValueError):
            cost.replace_suffix("changed",self.fragment,cost.sha(b"original"))

    def test_preview_cli_exact_bytes(self):
        with tempfile.TemporaryDirectory() as d:
            d=Path(d); body=d/"body"; frag=d/"fragment"; out=d/"preview"
            body.write_bytes(b"original\r\n");frag.write_bytes(self.fragment.encode())
            subprocess.run([sys.executable,str(SCRIPT),"preview","--body",str(body),"--fragment",str(frag),"--expected-sha256",cost.sha(body.read_bytes()),"--output",str(out)],check=True)
            self.assertEqual(out.read_bytes(),self.replace(body.read_bytes().decode()).encode())


class CliCorrections(unittest.TestCase):
    """All destructive alias attempts use disposable synthetic files only."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "source.jsonl"
        self.mapping = self.root / "mapping.json"
        self.output = self.root / "output"

    def run_cli(self, *args, success=True):
        result = subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                                capture_output=True, text=True)
        if success:
            self.assertEqual(result.returncode, 0, result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("output aliases input", result.stderr)
        return result

    def write_mapping(self, events, mode="cumulative"):
        raw = b"".join((json.dumps(e) + "\n").encode() for e in events)
        self.source.write_bytes(raw)
        self.mapping.write_text(json.dumps({
            "version": 1, "cutoff": "date", "sources": [{
                "path": str(self.source), "size_bytes": len(raw),
                "sha256": cost.sha(raw), "thread": "s", "mode": mode}],
            "assignments": [{"source": 0, "turn": t, "tasks": ["A"]}
                            for t in ("t", "u")]}))

    def cumulative(self, events):
        self.write_mapping(events)
        self.run_cli("account", "--mapping", self.mapping, "--output", self.output)
        return json.loads(self.output.read_bytes())

    def test_cumulative_missing_details_cli(self):
        for cached, reasoning in ((None, None), (None, 1), (4, None)):
            with self.subTest(cached=cached, reasoning=reasoning):
                expected = usage(c=cached, r=reasoning)
                result = self.cumulative([context(), counter(expected), counter(usage(
                    20, None if cached is None else 2 * cached,
                    6, None if reasoning is None else 2 * reasoning))])
                self.assertEqual([r["usage"] for r in result["records"]], [expected])
                self.assertEqual(result["totals"]["A"]["model"], expected)
                if cached is None and reasoning is None:
                    self.assertIn("| model | 10 | N/A | N/A | 3 | N/A | 13 | partial |",
                                  cost.fragment(result["totals"]["A"], "date", "Partial."))

    def test_cumulative_details_appear_disappear_cli(self):
        result = self.cumulative([
            context(), counter(usage(c=None, r=None)), counter(usage(20, 8, 6, 2)),
            counter(usage(30, 12, 9, 3)), counter(usage(40, None, 12, None)),
            counter(usage(50, 20, 15, 5)), counter(usage(60, 24, 18, 6))])
        self.assertEqual([r["usage"] for r in result["records"]], [
            usage(c=None, r=None), usage(), usage(c=None, r=None),
            usage(c=None, r=None), usage()])
        self.assertEqual(result["totals"]["A"]["model"], usage(50, None, 15, None))

    def test_cumulative_core_reset_without_details_cli(self):
        result = self.cumulative([
            context(), counter(usage(c=None, r=None)),
            counter(usage(20, None, 6, None)), counter(usage(1, None, 1, None)),
            counter(usage(11, None, 4, None))])
        self.assertEqual([r["usage"] for r in result["records"]],
                         [usage(c=None, r=None)] * 2)

    def test_cumulative_subset_reset_and_recovery_cli(self):
        result = self.cumulative([
            context(), counter(usage()), counter(usage(20, 2, 6, 0)),
            counter(usage(30, 6, 9, 1))])
        self.assertEqual([r["usage"] for r in result["records"]],
                         [usage(c=None, r=None), usage()])

    def test_cumulative_inconsistent_subset_delta_cli(self):
        result = self.cumulative([
            context(), counter(usage(c=1, r=0)), counter(usage(20, 15, 6, 4)),
            counter(usage(30, 16, 9, 5))])
        self.assertEqual([r["usage"] for r in result["records"]],
                         [usage(c=None, r=None), usage(c=1)])

    def test_cumulative_missing_core_not_inferred_cli(self):
        first, second = usage(c=None, r=None), usage(20, None, 6, None)
        del first["total_tokens"]
        del second["total_tokens"]
        result = self.cumulative([context(), counter(first), counter(second),
                                  counter(usage(30, None, 9, None)),
                                  counter(usage(40, None, 12, None))])
        unknown_total = {**usage(c=None, r=None), "total_tokens": None}
        self.assertEqual([r["usage"] for r in result["records"]],
                         [unknown_total, unknown_total, usage(c=None, r=None)])
        self.assertIsNone(result["totals"]["A"]["model"]["total_tokens"])

    def test_cumulative_boundary_missing_details_cli(self):
        for new_context in (context("u"), context(model="other"), context("u", "other")):
            with self.subTest(context=new_context):
                result = self.cumulative([
                    context(), counter(usage(c=None, r=None)), new_context,
                    counter(usage(20, None, 6, None)), counter(usage(30, None, 9, None))])
                first, second = result["records"]
                self.assertIsNone(first["turn"])
                self.assertIsNone(first["model"])
                self.assertIsNone(first["task"])
                self.assertEqual(first["usage"], usage(c=None, r=None))
                self.assertEqual(second["task"], "A")
                self.assertEqual(second["usage"], usage(c=None, r=None))
                self.assertEqual(sum(m["total_tokens"] for m in result["totals"]["A"].values()), 13)

    def alias_output(self, target, kind):
        if kind == "direct":
            return target
        output = self.root / (target.name + "." + kind)
        if kind == "symlink":
            output.symlink_to(target)
        else:
            os.link(target, output)
        return output

    def test_account_rejects_all_input_aliases_cli(self):
        self.write_mapping([context(), response()], mode="responses")
        originals = {p: p.read_bytes() for p in (self.source, self.mapping)}
        for target in originals:
            for kind in ("direct", "symlink", "hardlink"):
                with self.subTest(input=target.name, alias=kind):
                    self.run_cli("account", "--mapping", self.mapping, "--output",
                                 self.alias_output(target, kind), success=False)
                    self.assertEqual({p: p.read_bytes() for p in originals}, originals)
        # A distinct existing output can still be replaced normally.
        self.output.write_bytes(b"old result")
        self.run_cli("account", "--mapping", self.mapping, "--output", self.output)
        self.assertEqual(json.loads(self.output.read_bytes())["totals"]["A"]["model"], usage())
        self.assertEqual({p: p.read_bytes() for p in originals}, originals)

    def test_preview_rejects_all_input_aliases_cli(self):
        body, frag = self.root / "body", self.root / "fragment"
        body.write_bytes(b"Original\r\nUnicode: \xc5\x82\n")
        frag.write_text(cost.fragment({"model": usage()}, "date", "Partial."))
        originals = {p: p.read_bytes() for p in (body, frag)}
        args = ("preview", "--body", body, "--fragment", frag,
                "--expected-sha256", cost.sha(originals[body]), "--output")
        for target in originals:
            for kind in ("direct", "symlink", "hardlink"):
                with self.subTest(input=target.name, alias=kind):
                    self.run_cli(*args, self.alias_output(target, kind), success=False)
                    self.assertEqual({p: p.read_bytes() for p in originals}, originals)
        self.output.write_bytes(b"old preview")
        self.run_cli(*args, self.output)
        self.assertEqual(self.output.read_bytes(), cost.replace_suffix(
            originals[body].decode(), originals[frag].decode(), cost.sha(originals[body])).encode())
        self.assertEqual({p: p.read_bytes() for p in originals}, originals)


if __name__ == "__main__":
    unittest.main()
