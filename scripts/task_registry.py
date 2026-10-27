#!/usr/bin/env python3
"""GitHub-first task identity guard. Existing reservations work offline."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
import sys

REPO = 'mhaduk/ck3-dynasty-map'
TITLE = re.compile(r'^([A-Z][A-Z0-9]*-[0-9]{3,}) — (\S.*)$')
TASK = re.compile(r'^([A-Z][A-Z0-9]*)-([0-9]{3,})$')

class RegistryError(ValueError):
    pass


def inventory(issues):
    result = {}
    numbers = set()
    for issue in issues:
        match = TITLE.fullmatch(issue.get('title', ''))
        if not match:
            continue  # Body mentions and unclassified historical issues allocate nothing.
        task_id = match[1]
        number = issue.get('number')
        if type(number) is not int or number < 1 or number in numbers:
            raise RegistryError('invalid or repeated GitHub issue number')
        if task_id in result:
            raise RegistryError(f'duplicate canonical ID {task_id}: #{result[task_id]["number"]} and #{number}')
        if issue.get('state', '').upper() not in {'OPEN', 'CLOSED'}:
            raise RegistryError('invalid issue state')
        url = f'https://github.com/{REPO}/issues/{number}'
        if issue.get('url') != url:
            raise RegistryError('unexpected repository or issue URL')
        result[task_id] = {**issue, 'state': issue['state'].upper()}
        numbers.add(number)
    return result


def next_id(issues, prefix, reserved=()):
    if not re.fullmatch(r'[A-Z][A-Z0-9]*', prefix):
        raise RegistryError('invalid task class')
    keys = set(inventory(issues)) | set(reserved)
    values = [int(m[2]) for key in keys if (m := TASK.fullmatch(key)) and m[1] == prefix]
    return f'{prefix}-{max(values, default=0) + 1:03d}'


def gh(*args):
    try:
        result = subprocess.run(['gh', *args], check=True, capture_output=True, text=True, timeout=60)
        return result.stdout
    except (OSError, subprocess.SubprocessError) as exc:
        raise RegistryError('GitHub request failed; no local registration permitted') from exc


def fetch():
    # REST pagination, issues only (the repository issues endpoint also returns PRs).
    try:
        pages = json.loads(gh('api', '--paginate', '--slurp', f'repos/{REPO}/issues?state=all&per_page=100'))
        return [{'number': x['number'], 'title': x['title'], 'state': x['state'], 'url': x['html_url']}
                for page in pages for x in page if 'pull_request' not in x]
    except (ValueError, KeyError, TypeError) as exc:
        raise RegistryError('malformed GitHub inventory') from exc


def readback(number, title):
    try:
        item = json.loads(gh('issue', 'view', str(number), '--repo', REPO, '--json', 'number,title,state,url'))
        if item['number'] != number or item['title'] != title:
            raise RegistryError('issue readback identity mismatch')
        inventory([item])
        return item
    except (ValueError, KeyError, TypeError) as exc:
        raise RegistryError('issue readback failed') from exc


def load(root):
    path = Path(root) / 'docs/task-registry.json'
    if path.is_symlink() or path.parent.is_symlink():
        raise RegistryError('unsafe registry path')
    try:
        data = json.loads(path.read_text())
        if data['repository'] != REPO or data['version'] != 1:
            raise RegistryError('wrong registry repository/version')
        inventory(data['issues'])
        return data
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise RegistryError('verified GitHub registry missing or invalid; synchronize before creating a handoff') from exc


def binding(root, parent, issue=None):
    data = load(root)
    items = inventory(data['issues'])
    if parent not in items:
        raise RegistryError(f'unregistered parent {parent}; GitHub-first reservation required')
    item = items[parent]
    if issue is not None and issue != item['number']:
        raise RegistryError(f'task conflict: {parent} belongs to #{item["number"]}, not #{issue}')
    return {'task_id': parent, 'number': item['number'], 'url': item['url'], 'title': item['title']}


def check_handoff(root, status):
    # Old receipts remain evidence. Explicit conflict quarantines prevent resumption.
    path = Path(root) / 'docs/task-registry.json'
    if not path.exists():
        if status.get('github_issue'):
            raise RegistryError('bound handoff requires its offline registry')
        return  # Legacy repositories keep their existing lifecycle.
    data = load(root)
    override = data.get('handoff_reconciliation', {}).get(status['id'])
    if override:
        if override.get('action') == 'blocked':
            raise RegistryError('historical identity conflict; handoff quarantined, prepare a new registered handoff')
        if status['status'] not in {'CONSUMED', 'COMPLETED', 'FAILED'}:
            raise RegistryError('historical alias is evidence only; new execution needs canonical handoff')
        return
    expected = binding(root, status['parent_id'])
    actual = status.get('github_issue')
    if actual is not None and actual != expected:
        raise RegistryError('handoff GitHub task identity conflicts with canonical registry')


def save(root, issues, previous=None):
    inventory(issues)
    # Every canonical title must have an independent issue readback before mirroring.
    for item in inventory(issues).values():
        readback(item['number'], item['title'])
    path = Path(root) / 'docs/task-registry.json'
    if path.is_symlink() or path.parent.is_symlink():
        raise RegistryError('unsafe registry path')
    old = previous or {}
    data = {'version': 1, 'repository': REPO, 'verified_at': datetime.now(timezone.utc).isoformat(),
            'issues': issues, 'retired_ids': sorted(set(old.get('retired_ids', [])) | (set(inventory(old.get('issues', []))) - set(inventory(issues)))),
            'handoff_reconciliation': old.get('handoff_reconciliation', {})}
    temporary = path.with_suffix('.json.tmp')
    if temporary.exists() or temporary.is_symlink():
        raise RegistryError('registry temporary file exists; inspect before retry')
    with temporary.open('x') as stream:
        stream.write(json.dumps(data, indent=2, sort_keys=True) + '\n')
    temporary.replace(path)


def reserve(root, prefix, title, body_file):
    old = load(root) if (Path(root) / 'docs/task-registry.json').exists() else {}
    issues = fetch()
    task_id = next_id(issues, prefix, old.get('retired_ids', []))
    full_title = f'{task_id} — {title}'
    if not TITLE.fullmatch(full_title) or '\n' in full_title:
        raise RegistryError('invalid issue title')
    # GitHub has no unique-title transaction. Post-create collision must fail closed;
    # never edit/close somebody else's issue or automatically create duplicates.
    url = gh('issue', 'create', '--repo', REPO, '--title', full_title, '--body-file', str(body_file)).strip()
    match = re.fullmatch(r'https://github.com/' + re.escape(REPO) + r'/issues/([0-9]+)', url)
    if not match:
        raise RegistryError('creation result unknown; inspect GitHub before retry')
    readback(int(match[1]), full_title)
    fresh = fetch()
    items = inventory(fresh)  # Duplicate/taken ID => no local output.
    if items.get(task_id, {}).get('number') != int(match[1]):
        raise RegistryError('reservation raced; re-query GitHub before proceeding')
    save(root, fresh, old)
    return task_id, url



def audit(root):
    data = load(root)
    result = []
    base = Path(root) / '.codex-sync/tasks'
    if not base.exists():
        return result
    if base.is_symlink():
        raise RegistryError('unsafe handoff directory')
    for directory in sorted(base.iterdir()):
        path = directory / 'STATUS.json'
        if directory.is_symlink() or path.is_symlink():
            raise RegistryError('unsafe handoff path')
        if not path.is_file():
            continue
        status = json.loads(path.read_text())
        rule = data.get('handoff_reconciliation', {}).get(status['id'])
        if rule:
            if rule['action'] != 'blocked':
                check_handoff(root, status)
            result.append({'id': status['id'], 'status': status['status'], 'disposition': rule['action']})
        else:
            check_handoff(root, status)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', default='.')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('sync')
    sub.add_parser('audit')
    p = sub.add_parser('next'); p.add_argument('prefix')
    p = sub.add_parser('verify'); p.add_argument('task'); p.add_argument('--issue', type=int, required=True)
    p = sub.add_parser('reserve'); p.add_argument('prefix'); p.add_argument('--title', required=True); p.add_argument('--body-file', required=True)
    args = parser.parse_args()
    try:
        if args.command == 'audit':
            print(json.dumps(audit(args.root), indent=2))
        elif args.command == 'sync':
            old = load(args.root) if (Path(args.root) / 'docs/task-registry.json').exists() else {}
            save(args.root, fetch(), old)
        elif args.command == 'next':
            old = load(args.root) if (Path(args.root) / 'docs/task-registry.json').exists() else {}
            print(next_id(fetch(), args.prefix, old.get('retired_ids', [])))
        elif args.command == 'reserve':
            print(*reserve(args.root, args.prefix, args.title, args.body_file))
        else:
            print(json.dumps(binding(args.root, args.task, args.issue)))
    except (RegistryError, OSError) as exc:
        print(f'task-registry: {exc}', file=sys.stderr)
        return 2
    return 0

if __name__ == '__main__':
    sys.exit(main())
