#!/usr/bin/env python3
"""Offline lifecycle helper for cooperating workers, not an OS sandbox."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import html
import hashlib
import json
import os
import importlib.util
from pathlib import Path
import re
import sys
import tempfile

# Load the adjacent helper even when this module is imported from a test.
_registry_spec = importlib.util.spec_from_file_location("handoff_task_registry", Path(__file__).with_name("task_registry.py"))
task_registry = importlib.util.module_from_spec(_registry_spec)
_registry_spec.loader.exec_module(task_registry)

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


def validate_plan(plan):
    if not isinstance(plan, dict) or set(plan) != {"total_steps", "steps"}:
        raise HandoffError("execution_plan requires total_steps and steps")
    steps = plan["steps"]
    if (type(plan["total_steps"]) is not int or not isinstance(steps, list)
            or not 1 <= len(steps) <= 20 or plan["total_steps"] != len(steps)):
        raise HandoffError("execution_plan requires 1–20 matching steps")
    ids = []
    for step in steps:
        if (not isinstance(step, dict) or set(step) != {"id", "label"}
                or not isinstance(step["id"], str)
                or not re.fullmatch(r"[a-z][a-z0-9_-]{0,39}", step["id"])
                or not isinstance(step["label"], str) or not step["label"].strip()
                or len(step["label"]) > 160 or any(ord(c) < 32 or ord(c) == 127 for c in step["label"])):
            raise HandoffError("invalid execution_plan milestone ID or label")
        ids.append(step["id"])
    if len(set(ids)) != len(ids):
        raise HandoffError("duplicate execution_plan milestone ID")
    return plan


def frozen_plan(text):
    plans = []
    for block, closing in re.findall(r"(?ms)^```json[ \t]*\n(.*?)(^```[ \t]*(?:\n|\Z)|\Z)", text):
        if not closing and "execution_plan" in block:
            raise HandoffError("unclosed execution_plan JSON fence")
        try:
            value = json.loads(block)
        except ValueError as exc:
            if "execution_plan" in block:
                raise HandoffError("invalid execution_plan JSON") from exc
            continue
        if isinstance(value, dict) and "execution_plan" in value:
            plans.append(validate_plan(value["execution_plan"]))
    if len(plans) > 1:
        raise HandoffError("multiple execution plans")
    return plans[0] if plans else None


def plan_fingerprint(plan):
    return digest(json.dumps(validate_plan(plan), sort_keys=True, separators=(",", ":")).encode())


def validate_plan_summary(summary, plan):
    """Validate GUI-authored bullets against the exact frozen plan."""
    plan = validate_plan(plan)
    if not isinstance(summary, dict) or set(summary) != {"plan_sha256", "bullets"}:
        raise HandoffError("plan summary requires plan_sha256 and bullets")
    if summary["plan_sha256"] != plan_fingerprint(plan):
        raise HandoffError("plan summary is stale; regenerate it for the frozen plan")
    bullets = summary["bullets"]
    if not isinstance(bullets, list) or not 1 <= len(bullets) <= 10:
        raise HandoffError("plan summary requires 1–10 bullets")
    ids = [step["id"] for step in plan["steps"]]
    covered = []
    for bullet in bullets:
        if not isinstance(bullet, dict) or set(bullet) != {"ids", "text"}:
            raise HandoffError("each summary bullet requires ids and text")
        group, text = bullet["ids"], bullet["text"]
        if (not isinstance(group, list) or not group or any(x not in ids for x in group)
                or not isinstance(text, str) or not text.strip() or "\n" in text or "\r" in text):
            raise HandoffError("invalid plan summary bullet")
        covered.extend(group)
    if covered != ids:
        raise HandoffError("plan summary must cover milestone IDs once, in frozen order")
    return summary


def render_handoff_table(rows, plan=None, summary=None):
    """Append the frozen plan row to the five established GUI handoff rows."""
    if len(rows) != 5:
        raise HandoffError("handoff table requires the five established rows")
    output = ["| | Command / value |", "|---|---|"]
    cell = lambda value: html.escape(str(value), quote=False).replace("|", "\\|").replace("\n", " ").replace("\r", " ")
    for label, value in rows:
        output.append(f"| {cell(label)} | {cell(value)} |")
    if plan is not None:
        summary = validate_plan_summary(summary, plan)
        value = "<br>".join(
            f"• [{cell(', '.join(bullet['ids']))}] {cell(bullet['text'])}"
            for bullet in summary["bullets"]
        )
        output.append(f"| Plan of execution | {value} |")
    return "\n".join(output)


def frozen_plan_summary(text, plan):
    marker = "## Execution plan summary"
    sections = text.split(marker)
    if len(sections) == 1:
        return None
    if len(sections) != 2:
        raise HandoffError("duplicate execution plan summary")
    match = re.search(r"```json\s*\n(\{.*?\})\s*\n```", sections[1], re.S)
    if not match:
        raise HandoffError("invalid execution plan summary JSON")
    try:
        value = json.loads(match.group(1))
        if set(value) != {"plan_summary"}:
            raise ValueError
        return validate_plan_summary(value["plan_summary"], plan)
    except (ValueError, TypeError, KeyError) as exc:
        raise HandoffError("invalid execution plan summary") from exc


def plan_argument(raw):
    try:
        return validate_plan(json.loads(raw))
    except ValueError as exc:
        raise HandoffError("invalid execution_plan JSON") from exc


def new_progress(plan):
    return {"plan": plan, "completed": [], "current": None, "percent": 0, "amendments": []}


def check_amendment(before, after):
    validate_plan(after)
    old_ids = [s["id"] for s in before["steps"]]
    if [s["id"] for s in after["steps"]][:len(old_ids)] != old_ids:
        raise HandoffError("amendment must retain existing milestone IDs and order")
    if before == after:
        raise HandoffError("amendment must change the plan")


def progress_contract(status, plan):
    progress = status.get("progress")
    if progress is None:
        return  # Old frozen handoffs need no migration; bootstrap on first transition.
    if plan is None or not isinstance(progress, dict):
        raise HandoffError("progress requires a frozen GUI plan")
    if set(progress) != {"plan", "completed", "current", "percent", "amendments"}:
        raise HandoffError("invalid progress fields")
    amendments = progress["amendments"]
    if not isinstance(amendments, list) or len(amendments) > 20:
        raise HandoffError("invalid progress amendments")
    for amendment in amendments:
        if (not isinstance(amendment, dict) or set(amendment) != {"plan", "reason", "owner", "at", "revision"}
                or not isinstance(amendment["reason"], str) or not amendment["reason"].strip()):
            raise HandoffError("invalid amendment evidence")
        check_amendment(plan, amendment["plan"])
        plan = amendment["plan"]
    if progress["plan"] != plan:
        raise HandoffError("progress plan differs from frozen plan/amendment evidence")
    ids = [s["id"] for s in plan["steps"]]
    done, current, percent = progress["completed"], progress["current"], progress["percent"]
    if (not isinstance(done, list) or any(not isinstance(s, str) or s not in ids for s in done)
            or len(set(done)) != len(done) or (current is not None and (not isinstance(current, str) or current not in ids or current in done))
            or type(percent) is not int or not 0 <= percent <= 100):
        raise HandoffError("invalid progress state")
    finished = status["status"] in {"COMPLETED", "CONSUMED"}
    if (finished and (percent != 100 or set(done) != set(ids) or current is not None)
            or not finished and not min(99, len(done) * 100 // len(ids)) <= percent <= 99):
        raise HandoffError("invalid progress percentage/completion gate")


def progress_line(status):
    p = status.get("progress")
    if p is None:
        return None
    percent = p["percent"]
    filled = percent * 30 // 100
    bar = "█" * filled + "░" * (30 - filled)
    if status["status"] == "COMPLETED":
        label = "CLI complete; GUI review pending"
    elif p["current"] is None:
        label = "milestone boundary"
    else:
        label = next((step["label"] for step in p["plan"]["steps"]
                      if step["id"] == p["current"]), p["current"])
    cue = "●"
    if sys.stdout.isatty() and "NO_COLOR" not in os.environ:
        cue = "\x1b[32m●\x1b[0m"
    identity = status.get("parent_id") or status["id"]
    return f"{cue}  {identity} [{bar}] ~{percent}% — {label}"


def cmd_progress(args):
    root = repo_root(args.root)
    directory = task_dir(root, args.id)
    with locked(root, directory):
        no_pending(directory)
        status = checked_status(root, directory, args.revision)
        require_owner(status, args.owner)
        require_state(status, "IN_PROGRESS")
        contract(root, directory, status)
        plan = frozen_plan((directory / "CLI_TASK.md").read_text(encoding="utf-8"))
        if plan is None:
            raise HandoffError("planless handoff; CLI must not invent initial milestones")
        p = json.loads(json.dumps(status.get("progress") or new_progress(plan)))
        original = json.loads(json.dumps(p))
        if args.amend is not None:
            if not args.reason or not args.reason.strip() or len(args.reason) > 1000:
                raise HandoffError("amendment requires a bounded nonempty reason; scope stays frozen")
            if len(p["amendments"]) >= 20:
                raise HandoffError("maximum 20 amendments")
            amended = plan_argument(args.amend)
            check_amendment(p["plan"], amended)
            p["amendments"].append({"plan": amended, "reason": args.reason, "owner": args.owner,
                                    "at": now(), "revision": status["revision"]})
            p["plan"] = amended
        else:
            ids = [s["id"] for s in p["plan"]["steps"]]
            milestone = args.start or args.done
            if milestone not in ids:
                raise HandoffError("unknown milestone ID")
            if args.start:
                if milestone in p["completed"]:
                    raise HandoffError("milestone already completed")
                if p["current"] not in (None, milestone):
                    raise HandoffError("finish current milestone before starting another")
                p["current"] = milestone
            elif milestone not in p["completed"]:
                if p["current"] != milestone:
                    raise HandoffError("start milestone before completing it")
                p["completed"].append(milestone)
                p["current"] = None
        p["percent"] = max(p["percent"], min(99, len(p["completed"]) * 100 // p["plan"]["total_steps"]))
        if p == original and status.get("progress") is not None:
            return  # Restart/repeated transition: no revision churn or duplicate bar.
        updated = next_status(status, progress=p)
        progress_contract(updated, plan)
        atomic_json(root, directory / "STATUS.json", updated)
    print(progress_line(updated) + ("; plan amended" if args.amend is not None else ""))


def registry_check(root, status):
    try:
        task_registry.check_handoff(root, status)
    except task_registry.RegistryError as exc:
        raise HandoffError(str(exc)) from exc


def contract(root, directory, status, initial=False):
    registry_check(root, status)
    task = safe_path(root, directory / "CLI_TASK.md", "file", required=True)
    if digest(task.read_bytes()) != status["scope_sha256"]:
        raise HandoffError("frozen task description changed")
    progress_contract(status, frozen_plan(task.read_text(encoding="utf-8")))
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
    try:
        if args.issue is None:
            raise task_registry.RegistryError("--issue is required: bind the parent to its verified GitHub issue")
        github_issue = task_registry.binding(root, args.parent, args.issue)
    except task_registry.RegistryError as exc:
        raise HandoffError(str(exc)) from exc
    if args.task_file:
        source = Path(args.task_file)
        source = source if source.is_absolute() else root / source
        safe_path(root, source, "file", required=True)
        task_text = source.read_text(encoding="utf-8")
    else:
        task_text = args.task
    if args.context_preview:
        preview_path = Path(args.context_preview)
        preview_path = preview_path if preview_path.is_absolute() else root / preview_path
        safe_path(root, preview_path, "file", required=True)
        try:
            context = json.loads(preview_path.read_text(encoding="utf-8"))
            lines = context["preview"].splitlines()
            url = context["history_url"]
        except (ValueError, KeyError, TypeError, AttributeError) as exc:
            raise HandoffError("invalid GUI context preview") from exc
        expected_url = re.compile(r"https://github\.com/mhaduk/ck3-dynasty-map/blob/[A-Za-z0-9_./-]+/docs/telemetry/gui-context/" + re.escape(args.parent) + r"\.jsonl")
        if (len(lines) != 2
                or not re.fullmatch(r"GUI session estimate: ~[0-9,]+ estimated tokens(?: \(\+[0-9,]+ since previous handoff\))?", lines[0])
                or not re.fullmatch(r"GUI session: [0-9,]+ messages / [0-9,]+ UTF-8 bytes", lines[1])
                or not isinstance(url, str) or not expected_url.fullmatch(url) or ".." in url):
            raise HandoffError("GUI context preview must contain two short lines and the stable parent history URL")
        if any(len(line) > 160 for line in lines):
            raise HandoffError("GUI context preview line exceeds 160 characters")
        lines[1] += f" · [history]({url})"
        marker = "\n\n```json\n"
        if marker in task_text:
            before, after = task_text.split(marker, 1)
            task_text = before.rstrip() + "\n\n## GUI context (diagnostic estimate)\n" + "\n".join(lines) + marker + after
        else:
            task_text = task_text.rstrip() + "\n\n## GUI context (diagnostic estimate)\n" + "\n".join(lines) + "\n"
    if args.execution_plan is not None:
        plan = plan_argument(args.execution_plan)
        if frozen_plan(task_text) is not None:
            raise HandoffError("execution plan already supplied in task")
        task_text = task_text.rstrip() + "\n\n```json\n" + json.dumps({"execution_plan": plan}) + "\n```\n"
    plan = frozen_plan(task_text)
    if args.plan_summary is not None:
        if plan is None or frozen_plan_summary(task_text, plan) is not None:
            raise HandoffError("plan summary requires one plan and must be supplied only once")
        try:
            summary = json.loads(args.plan_summary)
        except ValueError as exc:
            raise HandoffError("invalid plan summary JSON") from exc
        validate_plan_summary(summary, plan)
        task_text = task_text.rstrip() + "\n\n## Execution plan summary\n\n```json\n" + json.dumps({"plan_summary": summary}) + "\n```\n"
    if plan is not None:
        frozen_plan_summary(task_text, plan)  # Freeze and validate GUI-authored summary with the plan.
    if not task_text.strip():
        raise HandoffError("task description is required")
    if "Self-review contract: execution-review/v1" not in task_text:
        task_text = task_text.rstrip() + "\n\nSelf-review contract: execution-review/v1\n"
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
            "id": args.id, "parent_id": args.parent, "github_issue": github_issue, "attempt": 1, "revision": 1,
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
        plan = frozen_plan((directory / "CLI_TASK.md").read_text(encoding="utf-8"))
        if plan is not None and "progress" not in status:
            status["progress"] = new_progress(plan)
        atomic_json(root, directory / "STATUS.json", status)
    print(f"claimed {args.id} attempt {status['attempt']} revision {status['revision']}")
    if progress_line(status):
        print(progress_line(status))


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
    return {"id": task_id, "parent_id": parent, "legacy": True, "status": status}


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
            registry_check(root, status)
            print(args.id)
            return
        old = legacy_candidate(root, state)
        if old and old["id"] == args.id:
            registry_check(root, old)
            print(args.id)
            return
        raise HandoffError(f"requested ID is not {state}; no product-task fallback")
    data = task_registry.load(root) if (root / "docs/task-registry.json").exists() else {}
    quarantines = data.get("handoff_reconciliation", {})
    eligible = [s for s in candidates(root) if s["status"] == state
                and not (quarantines.get(s["id"], {}).get("action") == "blocked"
                         or (quarantines.get(s["id"], {}).get("action") == "alias" and state == "READY"))]
    old = legacy_candidate(root, state)
    if old:
        eligible.append(old)
    if len(eligible) != 1:
        names = [s["id"] + (" (legacy)" if s.get("legacy") else "") for s in eligible]
        raise HandoffError(f"{'ambiguous' if eligible else 'no'} {state} candidates: {', '.join(names) or '(none)'}; no fallback to product work")
    registry_check(root, eligible[0])
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
            if "progress" in after:
                after["progress"] = {**after["progress"], "completed": [], "current": None}
            for key in ("claimed_at", "completed_at", "consumed_at", "failure", "recovered_at", "outputs",
                        "result_sha256", "result_provenance", "review_sha256"):
                after.pop(key, None)
            journal = {"command": {"operation": "retry", "revision": args.revision},
                       "before": status, "after": after, "evidence": evidence}
            atomic_json(root, directory / ".transition.json", journal)
            finish_transition(root, directory, journal)
    print(f"retry-ready {args.id} (previous evidence archived)")


def result_provenance(root, body, status, outputs):
    markers = list(re.finditer(r"(?ms)^```json\n(\{.*?\})\n```[ \t]*$", body))
    provenance_markers = []
    for candidate in markers:
        try:
            value = json.loads(candidate.group(1))
        except ValueError:
            continue
        if isinstance(value, dict) and {"id", "parent_id", "attempt", "inputs", "outputs"}.issubset(value):
            provenance_markers.append((candidate, value))
    if len(provenance_markers) != 1:
        raise HandoffError("result requires a fenced JSON provenance block")
    marker, candidate_provenance = provenance_markers[0]
    try:
        provenance = candidate_provenance
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
    task_path = safe_path(root, task_dir(root, status["id"]) / "CLI_TASK.md", "file", required=True)
    task_text = task_path.read_text(encoding="utf-8")
    if "Self-review contract: execution-review/v1" in task_text:
        try:
            from execution_review import extract_review, validate_review
            validate_review(extract_review(body, after=marker.end()))
        except (ValueError, OSError) as exc:
            raise HandoffError(f"new-contract task requires a valid post-execution self-review: {exc}") from exc
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
        provenance = result_provenance(root, data.decode(), status, outputs)
        progress = status.get("progress")
        plan = frozen_plan((directory / "CLI_TASK.md").read_text(encoding="utf-8"))
        if plan is not None:
            if progress is None or len(progress["completed"]) != progress["plan"]["total_steps"]:
                raise HandoffError("all supplied milestones must finish before CLI completion")
            status = {**status, "progress": {**progress, "percent": 100}}
        atomic_json(root, directory / "STATUS.json", next_status(status, status="COMPLETED", completed_at=now(),
                    outputs=outputs, result_sha256=digest(data), result_provenance=provenance))
    print(f"completed {args.id}")
    if progress_line(status):
        print(progress_line({**status, "status": "COMPLETED"}))


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
            result_data = result.read_bytes()
            if digest(result_data) != status["result_sha256"]:
                raise HandoffError("result changed after completion")
            task_path = safe_path(root, directory / "CLI_TASK.md", "file", required=True)
            if "Self-review contract: execution-review/v1" in task_path.read_text(encoding="utf-8"):
                try:
                    module_path = Path(__file__).resolve().with_name("execution_review.py")
                    spec = importlib.util.spec_from_file_location("execution_review_for_handoff", module_path)
                    if spec is None or spec.loader is None:
                        raise ValueError("review helper cannot be loaded")
                    review_helper = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(review_helper)
                    body = result_data.decode("utf-8")
                    provenance = re.search(r"(?ms)^```json\n(\{.*?\})\n```[ \t]*$", body)
                    if not provenance:
                        raise ValueError("result provenance is missing")
                    report = review_helper.extract_review(body, after=provenance.end())
                    review_helper.validate_review(report)
                    canonical = json.dumps(report, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
                    report_hash = digest(canonical)
                    inventory_path = safe_path(root, root / "docs/telemetry/optimization-inventory.json", "file")
                    inventory = review_helper._read_inventory(inventory_path)
                    identity = f"{status['id']}:{status['attempt']}"
                    entry = next((row for row in inventory["ledger"] if row.get("identity") == identity), None)
                    if entry is None or entry.get("report_sha256") != report_hash:
                        raise ValueError("matching GUI triage ledger entry is absent")
                except (ValueError, OSError, UnicodeError) as exc:
                    raise HandoffError(f"GUI inventory triage is required before receipt: {exc}") from exc
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
    p.add_argument("--issue", type=int, help="verified GitHub issue number for the parent task")
    p.add_argument("--task", default=""); p.add_argument("--task-file")
    p.add_argument("--execution-plan", help="GUI-supplied plan JSON, frozen into CLI_TASK before READY")
    p.add_argument("--plan-summary", help="GUI-authored summary JSON bound to the exact frozen plan")
    p.add_argument("--context-preview", help="optional private JSON preview from gui_context.py; diagnostic only")
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
    p = subs.add_parser("progress", help="record one meaningful milestone transition or justified plan amendment")
    p.add_argument("id"); p.add_argument("--owner", required=True); p.add_argument("--revision", type=int, required=True)
    actions = p.add_mutually_exclusive_group(required=True)
    actions.add_argument("--start"); actions.add_argument("--done"); actions.add_argument("--amend", help="replacement plan JSON; retains IDs, may append stages")
    p.add_argument("--reason"); p.set_defaults(func=cmd_progress)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        args.func(args)
    except (HandoffError, task_registry.RegistryError, OSError, UnicodeError) as exc:
        print(f"handoff: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
