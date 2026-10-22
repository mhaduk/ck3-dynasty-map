#!/usr/bin/env python3
"""Offline lifecycle helper for cooperating workers, not an OS sandbox."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile

ID_RE = re.compile(r"^[A-Z][A-Z0-9]*-[A-Z0-9]+(?:-[A-Z0-9]+)*$")
REQUIRED_SECTIONS = (
    "Identity", "Result", "Files", "Checks", "Self-healing / agent-instruction findings",
    "Permissions / Git state", "GUI next step",
)
ADMIN_FILES = ("STATUS.json", "CLI_TASK.md", "CLI_RESULT.md", "GUI_REVIEW.md",
               ".status-lock", ".transition.json")
ADMIN_DIRS = (".claim", "attempts", "baseline", "artifacts")


class HandoffError(Exception):
    pass


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_id(value):
    if not ID_RE.fullmatch(value):
        raise HandoffError(f"invalid task ID: {value!r}")
    return value


def repo_root(value):
    root = Path(value).resolve(strict=True)
    if not root.is_dir():
        raise HandoffError("repository root is not a directory")
    return root


def safe_path(root, path, kind=None, required=False):
    """Check every lexical component before following/reading any of them."""
    try:
        parts = path.relative_to(root).parts
    except ValueError as exc:
        raise HandoffError("path escapes repository") from exc
    if not parts or any(p in {".", ".."} for p in parts):
        raise HandoffError("invalid repository-relative path")
    current = root
    for index, part in enumerate(parts):
        current = current / part
        if current.is_symlink():  # includes broken links
            raise HandoffError(f"unsafe symlink: {current.relative_to(root)}")
        if current.exists():
            expected = kind if index == len(parts) - 1 else "dir"
            if expected == "dir" and not current.is_dir():
                raise HandoffError(f"not a directory: {current.relative_to(root)}")
            if expected == "file" and not current.is_file():
                raise HandoffError(f"not a regular file: {current.relative_to(root)}")
        elif required:
            raise HandoffError(f"missing path: {path.relative_to(root)}")
    return path


def inbox(root, create=False):
    base = root / ".codex-sync" / "tasks"
    safe_path(root, base, "dir")
    if create:
        base.mkdir(parents=True, exist_ok=True)
    return base


def task_dir(root, task_id, create_parent=False):
    directory = inbox(root, create_parent) / safe_id(task_id)
    return safe_path(root, directory, "dir")


def admin_paths(root, directory):
    safe_path(root, directory, "dir", required=True)
    for name in ADMIN_FILES:
        safe_path(root, directory / name, "file")
    for name in ADMIN_DIRS:
        path = safe_path(root, directory / name, "dir")
        if path.exists():
            # Do not follow links even inside archives, claims or output artifacts.
            for parent, dirs, files in os.walk(path, followlinks=False):
                for child in dirs:
                    safe_path(root, Path(parent) / child, "dir")
                for child in files:
                    safe_path(root, Path(parent) / child, "file")
    claim = directory / ".claim"
    if claim.exists() and any(p.name != "owner" for p in claim.iterdir()):
        raise HandoffError("unexpected claim evidence; coordinator inspection required")
    safe_path(root, claim / "owner", "file")


def atomic_bytes(root, path, data):
    safe_path(root, path, "file")
    safe_path(root, path.parent, "dir", required=True)
    fd, name = tempfile.mkstemp(prefix=".handoff-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def atomic_json(root, path, value):
    atomic_bytes(root, path, json_bytes(value))


def read_json(root, path):
    safe_path(root, path, "file", required=True)
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, UnicodeError) as exc:
        raise HandoffError(f"invalid JSON: {path.relative_to(root)}") from exc


def read_status(root, directory):
    status = read_json(root, directory / "STATUS.json")
    if status.get("id") != directory.name:
        raise HandoffError("status ID does not match directory")
    return status


@contextmanager
def locked(root, directory):
    admin_paths(root, directory)  # reject unsafe paths before creating a lock
    path = directory / ".status-lock"
    fd = os.open(path, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, "a+") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            admin_paths(root, directory)
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def checked_status(root, directory, revision):
    status = read_status(root, directory)
    if status["revision"] != revision:
        raise HandoffError("stale status revision")
    return status


def no_pending(directory):
    if (directory / ".transition.json").exists():
        raise HandoffError("interrupted transition pending; repeat its exact retry/consume command")


def require_owner(status, owner):
    if not owner or status.get("owner") != owner:
        raise HandoffError("worker owner mismatch")


def require_state(status, *states):
    if status["status"] not in states:
        raise HandoffError(f"state {status['status']} not in {', '.join(states)}")


def next_status(current, **changes):
    return {**current, **changes, "revision": current["revision"] + 1, "updated_at": now()}


def input_path(root, rel):
    path = Path(rel)
    if path.is_absolute() or not path.parts or ".." in path.parts or str(path) != rel:
        raise HandoffError(f"input/output must be a normalized relative path: {rel}")
    if path.parts[:2] == (".codex-sync", "tasks") or str(path) in {
        ".codex-sync/CLI_TASK.md", ".codex-sync/CLI_RESULT.md", ".codex-sync/GUI_REVIEW.md",
    }:
        raise HandoffError("handoff administration cannot be an assigned input/output")
    return safe_path(root, root / path, "file")


def inputs_fingerprint(root, paths, optional=()):
    result = {}
    for rel in paths:
        path = input_path(root, rel)
        if not path.exists():
            if rel not in optional:
                raise HandoffError(f"missing input: {rel}")
            result[rel] = None
        else:
            result[rel] = digest(path.read_bytes())
    return result


def contract(root, directory, status, initial=False):
    task = safe_path(root, directory / "CLI_TASK.md", "file", required=True)
    if digest(task.read_bytes()) != status["scope_sha256"]:
        raise HandoffError("frozen task description changed")
    # Initial dirty bytes and their manifest are retained across attempts.
    manifest = read_json(root, directory / "baseline" / "INPUTS.json")
    if manifest != status["inputs"]:
        raise HandoffError("baseline manifest changed")
    for index, (rel, expected) in enumerate(sorted(status["inputs"].items())):
        if expected is not None:
            path = safe_path(root, directory / "baseline" / f"{index}.bin", "file", required=True)
            if digest(path.read_bytes()) != expected:
                raise HandoffError(f"baseline bytes changed: {rel}")
    paths = [rel for rel in status["inputs"] if initial or rel not in status["owned"]]
    current = inputs_fingerprint(root, paths, optional=status["owned"])
    if current != {p: status["inputs"][p] for p in paths}:
        raise HandoffError("input fingerprint changed" + ("; new delegation required for changed retry inputs" if initial else ""))


def cmd_create(args):
    root = repo_root(args.root)
    # All supplied paths and inputs are checked before creating task directories.
    directory = task_dir(root, args.id)
    if directory.exists():
        raise HandoffError("task ID already exists; retry must be explicit")
    safe_id(args.parent)
    if args.task_file:
        source = Path(args.task_file)
        source = source if source.is_absolute() else root / source
        safe_path(root, source, "file", required=True)
        task_text = source.read_text(encoding="utf-8")
    else:
        task_text = args.task
    if not task_text.strip():
        raise HandoffError("task description is required")
    if any(not c or "\n" in c or "\r" in c for c in args.check):
        raise HandoffError("check names must be nonempty single lines")
    owned = sorted(set(args.owned))
    paths = sorted(set(args.input) | set(owned))
    fingerprints = inputs_fingerprint(root, paths, optional=set(owned) - set(args.input))
    baseline = {rel: input_path(root, rel).read_bytes() for rel, value in fingerprints.items() if value is not None}
    if any(digest(data) != fingerprints[rel] for rel, data in baseline.items()):
        raise HandoffError("inputs changed during creation")
    inbox(root, create=True)
    directory.mkdir()  # exclusive reservation: only one creator for this ID
    (directory / "artifacts").mkdir()
    (directory / "baseline").mkdir()
    atomic_json(root, directory / "baseline" / "INPUTS.json", fingerprints)
    for index, (rel, value) in enumerate(sorted(fingerprints.items())):
        if value is not None:
            atomic_bytes(root, directory / "baseline" / f"{index}.bin", baseline[rel])
    task_data = (task_text.rstrip() + "\n").encode()
    atomic_bytes(root, directory / "CLI_TASK.md", task_data)
    # Publish READY only after its description and initial evidence exist.
    with locked(root, directory):
        atomic_json(root, directory / "STATUS.json", {
            "id": args.id, "parent_id": args.parent, "attempt": 1, "revision": 1,
            "status": "READY", "owner": None, "created_at": now(), "updated_at": now(),
            "inputs": fingerprints, "owned": owned, "required_checks": args.check,
            "scope_sha256": digest(task_data),
        })
    print(directory.relative_to(root))


def cmd_claim(args):
    root = repo_root(args.root)
    directory = task_dir(root, args.id)
    with locked(root, directory):
        no_pending(directory)
        status = checked_status(root, directory, args.revision)
        require_state(status, "READY")
        if not args.owner.strip():
            raise HandoffError("owner must be nonempty")
        contract(root, directory, status, initial=True)
        claim = directory / ".claim"
        if claim.exists():
            raise HandoffError("task already has a claim; no age-based takeover")
        claim.mkdir()
        atomic_bytes(root, claim / "owner", args.owner.encode())
        status = next_status(status, status="IN_PROGRESS", owner=args.owner, claimed_at=now())
        atomic_json(root, directory / "STATUS.json", status)
    print(f"claimed {args.id} attempt {status['attempt']} revision {status['revision']}")


def candidates(root):
    base = inbox(root)
    if not base.exists():
        return []
    result = []
    for directory in sorted(base.iterdir()):
        safe_id(directory.name)
        safe_path(root, directory, "dir", required=True)
        admin_paths(root, directory)
        result.append(read_status(root, directory))
    return result


def legacy_candidate(root, state):
    sync = safe_path(root, root / ".codex-sync", "dir")
    task = safe_path(root, sync / "CLI_TASK.md", "file")
    if not task.exists():
        return None
    text = task.read_text(encoding="utf-8")
    def field(name):
        values = re.findall(r"(?m)^" + re.escape(name) + r": (.+)$", text)
        if len(values) != 1:
            raise HandoffError("inconsistent legacy handoff fields")
        return values[0].strip()
    status = field("Status")
    if status != state:
        return None
    task_id, parent = safe_id(field("Delegation ID")), safe_id(field("Parent task"))
    if state == "COMPLETED":
        safe_path(root, sync / "CLI_RESULT.md", "file", required=True)
    return {"id": task_id, "parent_id": parent, "legacy": True}


def cmd_list(args):
    root = repo_root(args.root)
    statuses = candidates(root)
    for status in statuses:
        print(f"{status['id']}\t{status['parent_id']}\t{status['status']}\tattempt={status['attempt']}\trevision={status['revision']}")
    if not statuses:
        print("no tasks")


def cmd_resolve(args):
    root = repo_root(args.root)
    state = "COMPLETED" if args.receipt else "READY"
    if args.id:
        # Named per-ID lookup is independent of the legacy inbox and other IDs.
        directory = task_dir(root, args.id)
        if directory.exists():
            admin_paths(root, directory)
            status = read_status(root, directory)
            require_state(status, state)
            print(args.id)
            return
        old = legacy_candidate(root, state)
        if old and old["id"] == args.id:
            print(args.id)
            return
        raise HandoffError(f"requested ID is not {state}; no product-task fallback")
    eligible = [s for s in candidates(root) if s["status"] == state]
    old = legacy_candidate(root, state)
    if old:
        eligible.append(old)
    if len(eligible) != 1:
        names = [s["id"] + (" (legacy)" if s.get("legacy") else "") for s in eligible]
        raise HandoffError(f"{'ambiguous' if eligible else 'no'} {state} candidates: {', '.join(names) or '(none)'}; no fallback to product work")
    print(eligible[0]["id"])


def cmd_validate(args):
    root = repo_root(args.root)
    directory = task_dir(root, args.id)
    with locked(root, directory):
        no_pending(directory)
        status = read_status(root, directory)
        contract(root, directory, status, initial=status["status"] == "READY")
        if status["status"] in {"COMPLETED", "CONSUMED"}:
            if inputs_fingerprint(root, status["owned"], optional=status["owned"]) != status["outputs"]:
                raise HandoffError("completed outputs changed")
    print(json.dumps({"id": status["id"], "status": status["status"], "revision": status["revision"], "contract_match": True}, sort_keys=True))


def cmd_fail(args):
    root = repo_root(args.root)
    directory = task_dir(root, args.id)
    with locked(root, directory):
        no_pending(directory)
        status = checked_status(root, directory, args.revision)
        require_owner(status, args.owner)
        require_state(status, "IN_PROGRESS")
        # Failure may record a broken scope/input contract rather than hiding it.
        atomic_json(root, directory / "STATUS.json", next_status(status, status="FAILED", failure=args.reason))
    print(f"failed {args.id}")


def cmd_recover(args):
    root = repo_root(args.root)
    directory = task_dir(root, args.id)
    with locked(root, directory):
        no_pending(directory)
        status = checked_status(root, directory, args.revision)
        require_state(status, "READY")
        claim = directory / ".claim"
        if not claim.is_dir():
            raise HandoffError("recovery requires a preserved interrupted claim")
        owner_path = claim / "owner"
        owner = owner_path.read_text(encoding="utf-8") if owner_path.exists() else "unknown"
        atomic_json(root, directory / "STATUS.json", next_status(status, status="FAILED", owner=owner,
                    failure="Interrupted claim: " + args.reason, recovered_at=now()))
    print(f"recovered {args.id}; explicit retry may follow")


def resume_transition(root, directory, args, operation):
    path = directory / ".transition.json"
    if not path.exists():
        return False
    journal = read_json(root, path)
    command = {"operation": operation, "revision": args.revision}
    if operation == "consume":
        command["review"] = args.review.rstrip() + "\n"
    if journal["command"] != command:
        raise HandoffError("interrupted transition pending; repeat its exact retry/consume command")
    current = read_status(root, directory)
    if current not in (journal["before"], journal["after"]):
        raise HandoffError("pending transition status conflict; coordinator inspection required")
    finish_transition(root, directory, journal)
    return True


def finish_transition(root, directory, journal):
    """Idempotent write-ahead transition, always called under this task's lock."""
    before, after = journal["before"], journal["after"]
    operation = journal["command"]["operation"]
    if operation == "retry":
        # If status committed before interruption, all archive/cleanup work is done.
        if read_status(root, directory) == before:
            contract(root, directory, before, initial=True)
            archive = directory / "attempts" / str(before["attempt"])
            safe_path(root, archive, "dir")
            archive.mkdir(parents=True, exist_ok=True)
            evidence = {"STATUS.json": json_bytes(before),
                        **{name: bytes.fromhex(data) for name, data in journal["evidence"].items()}}
            for name, data in evidence.items():
                target = safe_path(root, archive / name, "file")
                if target.exists() and target.read_bytes() != data:
                    raise HandoffError("retry archive conflicts with preserved evidence")
                if not target.exists():
                    atomic_bytes(root, target, data)
            for name, data in journal["evidence"].items():
                source = directory / (".claim/owner" if name == "claim-owner" else name)
                safe_path(root, source, "file")
                if source.exists():
                    if source.read_bytes() != bytes.fromhex(data):
                        raise HandoffError("active retry evidence changed; coordinator inspection required")
                    source.unlink()
            claim = directory / ".claim"
            if claim.exists():
                claim.rmdir()  # no recursive delete of unchecked children
    else:
        result = safe_path(root, directory / "CLI_RESULT.md", "file", required=True)
        if digest(result.read_bytes()) != before["result_sha256"]:
            raise HandoffError("result changed after completion")
        contract(root, directory, before)
        if inputs_fingerprint(root, before["owned"], optional=before["owned"]) != before["outputs"]:
            raise HandoffError("completed outputs changed")
        review = safe_path(root, directory / "GUI_REVIEW.md", "file")
        data = journal["command"]["review"].encode()
        if review.exists() and review.read_bytes() != data:
            raise HandoffError("GUI_REVIEW.md has conflicting content")
        if not review.exists():
            atomic_bytes(root, review, data)
    atomic_json(root, directory / "STATUS.json", after)
    (directory / ".transition.json").unlink()


def cmd_retry(args):
    root = repo_root(args.root)
    directory = task_dir(root, args.id)
    with locked(root, directory):
        if not resume_transition(root, directory, args, "retry"):
            status = checked_status(root, directory, args.revision)
            require_state(status, "FAILED", "IN_PROGRESS")
            contract(root, directory, status, initial=True)
            archive = directory / "attempts" / str(status["attempt"])
            if archive.exists():
                raise HandoffError("attempt archive already exists without pending retry")
            evidence = {}
            for name in ("CLI_RESULT.md", "GUI_REVIEW.md", ".claim/owner"):
                source = safe_path(root, directory / name, "file")
                if source.exists():
                    evidence["claim-owner" if name == ".claim/owner" else name] = source.read_bytes().hex()
            after = next_status(status, attempt=status["attempt"] + 1, status="READY", owner=None,
                                retry_of_attempt=status["attempt"], retried_at=now())
            for key in ("claimed_at", "completed_at", "consumed_at", "failure", "recovered_at", "outputs",
                        "result_sha256", "result_provenance", "review_sha256"):
                after.pop(key, None)
            journal = {"command": {"operation": "retry", "revision": args.revision},
                       "before": status, "after": after, "evidence": evidence}
            atomic_json(root, directory / ".transition.json", journal)
            finish_transition(root, directory, journal)
    print(f"retry-ready {args.id} (previous evidence archived)")


def result_provenance(body, status, outputs):
    marker = re.search(r"(?ms)^```json\n(\{.*?\})\n```[ \t]*$", body)
    if not marker:
        raise HandoffError("result requires a fenced JSON provenance block")
    try:
        provenance = json.loads(marker.group(1))
    except ValueError as exc:
        raise HandoffError("invalid result provenance JSON") from exc
    expected = {key: status[key] for key in ("id", "parent_id", "attempt", "inputs")}
    expected["outputs"] = outputs
    if not isinstance(provenance, dict) or any(provenance.get(k) != v for k, v in expected.items()):
        raise HandoffError("result identity, attempt, initial inputs or final outputs mismatch")
    sections = dict(re.findall(r"(?ms)^## ([^\n]+)\n(.*?)(?=^## |\Z)", body))
    for heading in REQUIRED_SECTIONS:
        if not sections.get(heading, "").strip():
            raise HandoffError(f"missing or empty result section: {heading}")
    for line in ("- Outcome: SUCCESS", "- Acceptance: PASS"):
        if line not in sections["Result"].splitlines():
            raise HandoffError("result must report Outcome: SUCCESS and Acceptance: PASS")
    for check in status["required_checks"]:
        if f"- {check}: PASS" not in sections["Checks"].splitlines():
            raise HandoffError(f"requested check not passed: {check}")
    return provenance


def cmd_complete(args):
    root = repo_root(args.root)
    directory = task_dir(root, args.id)
    with locked(root, directory):
        no_pending(directory)
        status = checked_status(root, directory, args.revision)
        require_owner(status, args.owner)
        require_state(status, "IN_PROGRESS")
        contract(root, directory, status)
        result = safe_path(root, directory / "CLI_RESULT.md", "file", required=True)
        data = result.read_bytes()
        outputs = inputs_fingerprint(root, status["owned"], optional=status["owned"])
        provenance = result_provenance(data.decode(), status, outputs)
        atomic_json(root, directory / "STATUS.json", next_status(status, status="COMPLETED", completed_at=now(),
                    outputs=outputs, result_sha256=digest(data), result_provenance=provenance))
    print(f"completed {args.id}")


def cmd_consume(args):
    root = repo_root(args.root)
    directory = task_dir(root, args.id)
    with locked(root, directory):
        if not resume_transition(root, directory, args, "consume"):
            status = checked_status(root, directory, args.revision)
            require_state(status, "COMPLETED")
            if not args.review.strip():
                raise HandoffError("GUI review text is required")
            contract(root, directory, status)
            if inputs_fingerprint(root, status["owned"], optional=status["owned"]) != status["outputs"]:
                raise HandoffError("completed outputs changed")
            result = safe_path(root, directory / "CLI_RESULT.md", "file", required=True)
            if digest(result.read_bytes()) != status["result_sha256"]:
                raise HandoffError("result changed after completion")
            review = args.review.rstrip() + "\n"
            target = directory / "GUI_REVIEW.md"
            if target.exists() and target.read_text(encoding="utf-8") != review:
                raise HandoffError("GUI_REVIEW.md has conflicting content")
            journal = {"command": {"operation": "consume", "revision": args.revision, "review": review},
                       "before": status, "after": next_status(status, status="CONSUMED", consumed_at=now(),
                                                              review_sha256=digest(review.encode()))}
            atomic_json(root, directory / ".transition.json", journal)
            finish_transition(root, directory, journal)
    print(f"consumed {args.id}")


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="repository root")
    subs = parser.add_subparsers(dest="command", required=True)
    p = subs.add_parser("create", help="create one frozen READY task")
    p.add_argument("id"); p.add_argument("--parent", required=True)
    p.add_argument("--task", default=""); p.add_argument("--task-file")
    p.add_argument("--input", action="append", default=[], help="immutable dependency (unless also --owned)")
    p.add_argument("--owned", action="append", default=[], help="owned editable input/output, including new files")
    p.add_argument("--check", action="append", default=[]); p.set_defaults(func=cmd_create)
    p = subs.add_parser("list", help="list per-ID task status"); p.set_defaults(func=cmd_list)
    p = subs.add_parser("resolve", help="resolve a named or sole eligible handoff")
    p.add_argument("id", nargs="?"); p.add_argument("--receipt", action="store_true", help="resolve COMPLETED receipt instead of READY pickup")
    p.set_defaults(func=cmd_resolve)
    for name, function in (("claim", cmd_claim), ("complete", cmd_complete), ("fail", cmd_fail),
                           ("recover", cmd_recover), ("retry", cmd_retry), ("consume", cmd_consume)):
        p = subs.add_parser(name)
        p.add_argument("id"); p.add_argument("--revision", type=int, required=True)
        if name in {"claim", "complete", "fail"}:
            p.add_argument("--owner", required=True)
        if name in {"fail", "recover"}:
            p.add_argument("--reason", required=True)
        if name == "consume":
            p.add_argument("--review", required=True)
        p.set_defaults(func=function)
    p = subs.add_parser("validate", help="validate frozen scope, baseline and applicable fingerprints")
    p.add_argument("id"); p.set_defaults(func=cmd_validate)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        args.func(args)
    except (HandoffError, OSError, UnicodeError) as exc:
        print(f"handoff: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
