import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/task_registry.py'
spec = importlib.util.spec_from_file_location('registry', SCRIPT)
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)


def issue(number=25, task='T-003', title='Progress', state='CLOSED'):
    return {'number': number, 'title': f'{task} — {title}', 'state': state,
            'url': f'https://github.com/{r.REPO}/issues/{number}'}


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / 'docs').mkdir()
        self.path = self.root / 'docs/task-registry.json'

    def tearDown(self):
        self.temp.cleanup()

    def snapshot(self, issues=None, **extra):
        self.path.write_text(json.dumps({'version': 1, 'repository': r.REPO,
                                        'issues': issues or [issue()], **extra}))

    def test_existing_closed_id_recognized_and_reserved(self):
        self.snapshot()
        self.assertEqual(r.binding(self.root, 'T-003', 25)['number'], 25)
        self.assertEqual(r.next_id([issue()], 'T'), 'T-004')

    def test_mentions_and_issue_number_are_not_ids(self):
        mentioned = issue(31, 'F-001', 'Mention T-999', 'OPEN')
        mentioned['body'] = 'T-999 T-007'
        self.assertEqual(r.next_id([issue(), mentioned], 'T'), 'T-004')
        self.assertNotIn('T-031', r.inventory([mentioned]))

    def test_monotonic_per_class_gaps_and_retired_ids(self):
        self.assertEqual(r.next_id([issue(), issue(31, 'T-007'), issue(45, 'R-019')], 'T'), 'T-008')
        self.assertEqual(r.next_id([issue()], 'T', ['T-022']), 'T-023')

    def test_duplicate_ids_fail_even_if_closed(self):
        with self.assertRaisesRegex(r.RegistryError, 'duplicate'):
            r.inventory([issue(), issue(31)])

    def test_wrong_repo_or_duplicate_number_rejected(self):
        bad = issue(); bad['url'] = 'https://github.com/other/repo/issues/25'
        for rows in ([bad], [issue(), issue(25, 'T-004')]):
            with self.assertRaises(r.RegistryError):
                r.inventory(rows)

    def test_handoff_semantic_binding_conflict_rejected(self):
        self.snapshot()
        with self.assertRaisesRegex(r.RegistryError, 'conflict'):
            r.check_handoff(self.root, {'id': 'T003-WORK', 'parent_id': 'T-003',
                'status': 'READY', 'github_issue': {'number': 31, 'title': 'Other'}})
        with self.assertRaisesRegex(r.RegistryError, 'conflict'):
            r.binding(self.root, 'T-003', 31)

    def test_unregistered_and_missing_registry_rejected(self):
        with self.assertRaises(r.RegistryError):
            r.binding(self.root, 'T-003', 25)
        self.snapshot()
        with self.assertRaises(r.RegistryError):
            r.binding(self.root, 'T-007', 31)

    def test_quarantined_legacy_cannot_resume(self):
        self.snapshot(handoff_reconciliation={'T-003': {'action': 'blocked'}})
        with self.assertRaisesRegex(r.RegistryError, 'quarantined'):
            r.check_handoff(self.root, {'id': 'T-003', 'parent_id': 'T-003', 'status': 'READY'})

    def test_alias_is_evidence_only(self):
        self.snapshot(handoff_reconciliation={'T007-OLD': {'action': 'alias', 'canonical_parent': 'T-003', 'issue': 25}})
        status = {'id': 'T007-OLD', 'parent_id': 'T-007', 'status': 'CONSUMED'}
        r.check_handoff(self.root, status)
        with self.assertRaisesRegex(r.RegistryError, 'evidence only'):
            r.check_handoff(self.root, {**status, 'status': 'READY'})

    def test_network_failure_during_allocation_creates_nothing(self):
        with patch.object(r, 'fetch', side_effect=r.RegistryError('network')):
            with self.assertRaises(r.RegistryError):
                r.reserve(self.root, 'T', 'Task', 'body.md')
        self.assertFalse(self.path.exists())

    def test_creation_failure_creates_nothing(self):
        with patch.object(r, 'fetch', return_value=[issue()]), patch.object(r, 'gh', side_effect=r.RegistryError('denied')):
            with self.assertRaises(r.RegistryError):
                r.reserve(self.root, 'T', 'Task', 'body.md')
        self.assertFalse(self.path.exists())

    def test_concurrent_taken_id_fails_without_local_registration(self):
        before = [issue()]
        after = before + [issue(32, 'T-004'), issue(33, 'T-004')]
        with patch.object(r, 'fetch', side_effect=[before, after]), patch.object(r, 'gh', return_value=f'https://github.com/{r.REPO}/issues/33'), patch.object(r, 'readback'):
            with self.assertRaisesRegex(r.RegistryError, 'duplicate'):
                r.reserve(self.root, 'T', 'Progress', 'body.md')
        self.assertFalse(self.path.exists())

    def test_readback_failure_preserves_old_registry(self):
        self.snapshot()
        before = self.path.read_bytes()
        with patch.object(r, 'readback', side_effect=r.RegistryError('mismatch')):
            with self.assertRaises(r.RegistryError):
                r.save(self.root, [issue()])
        self.assertEqual(before, self.path.read_bytes())

    def test_reserved_task_can_create_handoff_offline(self):
        fresh = [issue(), issue(33, 'T-004', 'New task', 'OPEN')]
        with patch.object(r, 'fetch', side_effect=[[issue()], fresh]), patch.object(r, 'gh', return_value=f'https://github.com/{r.REPO}/issues/33'), patch.object(r, 'readback'):
            self.assertEqual(r.reserve(self.root, 'T', 'New task', 'body.md')[0], 'T-004')
        command = [sys.executable, str(SCRIPT.with_name('handoff.py')), '--root', str(self.root), 'create',
                   'T004-WORK', '--parent', 'T-004', '--issue', '33', '--task', 'Bounded task']
        completed = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        status = json.loads((self.root / '.codex-sync/tasks/T004-WORK/STATUS.json').read_text())
        self.assertEqual(status['github_issue']['number'], 33)

    def test_wrong_or_missing_issue_creates_no_handoff(self):
        self.snapshot()
        for arguments in ([], ['--issue', '31']):
            completed = subprocess.run([sys.executable, str(SCRIPT.with_name('handoff.py')), '--root', str(self.root),
                'create', 'T003-WORK', '--parent', 'T-003', '--task', 'Work', *arguments], capture_output=True, text=True)
            self.assertNotEqual(completed.returncode, 0)
            self.assertFalse((self.root / '.codex-sync/tasks/T003-WORK').exists())

    def test_audit_detects_conflicting_active_handoff(self):
        self.snapshot()
        directory = self.root / '.codex-sync/tasks/T003-WORK'
        directory.mkdir(parents=True)
        (directory / 'STATUS.json').write_text(json.dumps({'id': 'T003-WORK', 'parent_id': 'T-003',
            'status': 'READY', 'github_issue': {'number': 31}}))
        with self.assertRaisesRegex(r.RegistryError, 'conflicts'):
            r.audit(self.root)

    def test_audit_reports_quarantine_without_rewriting_evidence(self):
        self.snapshot(handoff_reconciliation={'T-003': {'action': 'blocked'}})
        directory = self.root / '.codex-sync/tasks/T-003'
        directory.mkdir(parents=True)
        path = directory / 'STATUS.json'
        path.write_text(json.dumps({'id': 'T-003', 'parent_id': 'T-003', 'status': 'READY'}))
        before = path.read_bytes()
        self.assertEqual(r.audit(self.root)[0]['disposition'], 'blocked')
        self.assertEqual(path.read_bytes(), before)

    def test_paginated_fetch_excludes_pull_requests(self):
        pages = [[{'number': 25, 'title': 'T-003 — Progress', 'state': 'closed', 'html_url': issue()['url']}],
                 [{'number': 99, 'title': 'T-099 — PR', 'state': 'closed', 'html_url': 'x', 'pull_request': {}}]]
        with patch.object(r, 'gh', return_value=json.dumps(pages)):
            self.assertEqual(r.inventory(r.fetch()), r.inventory([issue()]))

if __name__ == '__main__':
    unittest.main()
