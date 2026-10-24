#!/usr/bin/env python3
"""Measure known text in one explicitly named saved GUI session.

This is a local estimate of saved text, not active model context or billing
usage. Public history contains aggregates only; source identity and byte cursors
stay in a private .codex-sync file.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import tempfile
import re

VERSION = "gui-context/1"
MAX_SESSION_BYTES = 16 * 1024 * 1024
PUBLIC_ROOT = Path("docs/telemetry/gui-context")
PRIVATE_STATE = Path(".codex-sync/gui-context-private.json")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_file(path: Path, *, exists: bool) -> Path:
    """Reject final symlinks and non-regular files before reading/writing."""
    absolute = path.absolute()
    if absolute.is_symlink():
        raise ValueError(f"symlink path component refused: {path}")
    absolute = absolute.resolve(strict=exists)
    if exists and (not absolute.exists() or not absolute.is_file()):
        raise ValueError(f"regular file required: {path}")
    if absolute.exists() and not absolute.is_file():
        raise ValueError(f"regular file required: {path}")
    if not absolute.parent.is_dir():
        raise ValueError(f"parent directory required: {absolute.parent}")
    return absolute


def safe_mkdirs(path: Path) -> None:
    absolute = path.absolute().resolve()
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"symlink directory component refused: {current}")
        if current.exists() and not current.is_dir():
            raise ValueError(f"directory required: {current}")
        current.mkdir(exist_ok=True)


def safe_repo_output(path: Path, repo_root: Path, lexical_root: Path | None = None) -> None:
    absolute = path.absolute()
    try:
        relative = absolute.relative_to(lexical_root) if lexical_root else absolute.resolve().relative_to(repo_root)
    except ValueError as exc:
        raise ValueError("output path must remain inside repository") from exc
    current = repo_root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"symlink output component refused: {current}")


def message_text(event: dict) -> tuple[str, str] | None:
    """Extract only user/assistant message text; ignore tools and metadata."""
    if event.get("type") != "response_item":
        return None
    payload = event.get("payload")
    if not isinstance(payload, dict) or payload.get("type") != "message":
        return None
    role = payload.get("role")
    if role not in {"user", "assistant"}:
        return None
    content = payload.get("content")
    if not isinstance(content, list):
        return None
    chunks = []
    for item in content:
        if not isinstance(item, dict) or item.get("type") not in {"input_text", "output_text", "text"}:
            continue
        value = item.get("text")
        if isinstance(value, str):
            chunks.append(value)
    return (payload.get("id", ""), "\n".join(chunks))


def inspect_session(raw: bytes) -> dict:
    if len(raw) > MAX_SESSION_BYTES:
        raise ValueError(f"session exceeds bounded read ({MAX_SESSION_BYTES} bytes)")
    messages: dict[str, str] = {}
    anonymous = 0
    model = reasoning = None
    timestamp = None
    for line_no, line in enumerate(raw.splitlines(), 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except (ValueError, UnicodeError) as exc:
            raise ValueError(f"malformed session JSONL at line {line_no}") from exc
        if not isinstance(event, dict):
            continue
        stamp = event.get("timestamp")
        if isinstance(stamp, str):
            timestamp = stamp
        extracted = message_text(event)
        if extracted is not None:
            identity, text = extracted
            key = identity or f"anonymous:{anonymous}"
            anonymous += not bool(identity)
            if key in messages and messages[key] != text:
                raise ValueError("conflicting duplicate message identity")
            messages[key] = text
        payload = event.get("payload")
        if event.get("type") == "turn_context" and isinstance(payload, dict):
            if isinstance(payload.get("model"), str):
                model = payload["model"]
            effort = payload.get("effort", payload.get("reasoning_effort"))
            reasoning = effort if isinstance(effort, str) else None
    text = "\n".join(messages.values())
    encoded = text.encode("utf-8")
    return {
        "message_count": len(messages),
        "character_count": len(text),
        "text_bytes": len(encoded),
        "estimated_tokens": (len(encoded) + 3) // 4,
        "model": model,
        "reasoning_level": reasoning,
        "source_timestamp": timestamp,
    }


def load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, UnicodeError) as exc:
        raise ValueError(f"malformed JSON: {path}") from exc


def atomic_write(path: Path, data: bytes) -> None:
    fd, temporary = tempfile.mkstemp(prefix=".gui-context-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def measure(session: Path, task: str, identity: str, private_path: Path,
            history_path: Path, preview_path: Path | None = None, *, now=None, handoff=None, repository_ref="main") -> dict:
    if not re.fullmatch(r"[A-Za-z0-9_/-]+(?:[.][A-Za-z0-9_/-]+)*", repository_ref) or ".." in repository_ref or repository_ref.startswith("/"):
        raise ValueError("invalid public repository ref")
    source = safe_file(session, exists=True)
    repo_root = private_path.parent.parent.resolve(strict=True)
    lexical_root = private_path.parent.parent.absolute()
    safe_repo_output(private_path, repo_root, lexical_root)
    safe_repo_output(history_path, repo_root, lexical_root)
    if preview_path:
        safe_repo_output(preview_path, repo_root, lexical_root)
    private_candidate = private_path.absolute().resolve()
    history_candidate = history_path.absolute().resolve()
    for candidate in (private_candidate, history_candidate):
        try:
            candidate.relative_to(repo_root)
        except ValueError as exc:
            raise ValueError("output path must remain inside repository") from exc
    safe_mkdirs(history_path.parent)
    private = safe_file(private_path, exists=False)
    history = safe_file(history_path, exists=False)
    for output in (private, history):
        try:
            relative = output.relative_to(repo_root)
        except ValueError as exc:
            raise ValueError("output path must remain inside repository") from exc
        current = repo_root
        for part in relative.parts:
            current = current / part
            if current.is_symlink():
                raise ValueError(f"symlink output component refused: {current}")
    if preview_path:
        preview_path = safe_file(preview_path, exists=False)
    outputs = [private, history] + ([preview_path] if preview_path else [])
    if len(set(outputs)) != len(outputs) or any(path == source or (path.exists() and path.samefile(source)) for path in outputs):
        raise ValueError("measurement outputs must not alias source or each other")
    if not re.fullmatch(r"[TRFB]-[0-9]{3,}", task):
        raise ValueError("task must be a public stable task ID")
    if handoff is not None and (not re.fullmatch(r"[A-Z0-9-]{1,100}", handoff) or not handoff.startswith((task, task.replace("-", "")))):
        raise ValueError("handoff must be a public delegation ID for the parent task")
    if not identity or len(identity) > 256 or any(ord(c) < 32 for c in identity):
        raise ValueError("private session identity must be a nonempty opaque value")
    if source.stat().st_size > MAX_SESSION_BYTES:
        raise ValueError(f"session exceeds bounded read ({MAX_SESSION_BYTES} bytes)")
    raw = source.read_bytes()
    report = inspect_session(raw)
    state = load_json(private, {"version": 1, "sessions": {}})
    if not isinstance(state, dict) or state.get("version") != 1 or not isinstance(state.get("sessions"), dict):
        raise ValueError("unsupported private state")
    key = hashlib.sha256(identity.encode()).hexdigest()
    saved_task = state["sessions"].get(task)
    history_raw = history.read_bytes() if history.exists() else b""
    if len(history_raw) > 2 * 1024 * 1024:
        raise ValueError("public history exceeds bounded read")
    existing = [json.loads(line) for line in history_raw.splitlines() if line.strip()]
    if any(not isinstance(item, dict) or item.get("task") != task for item in existing):
        raise ValueError("public history task/schema mismatch")
    if saved_task and saved_task.get("history_sha256") != sha(history_raw):
        raise ValueError("public history changed or incomplete write; coordinator recovery required")
    if existing and not saved_task:
        raise ValueError("private provenance missing for existing history")
    previous = state.get("last_session", saved_task)
    if previous is not None and not isinstance(previous, dict):
        raise ValueError("invalid private session cursor")
    delta = None
    delta_reason = "no previous measurement"
    if previous:
        if previous.get("method") != VERSION:
            delta_reason = "measurement method changed"
        elif previous.get("identity_hash") != key:
            delta_reason = "session identity changed"
        elif len(raw) < previous.get("cursor_bytes", 0):
            delta_reason = "session file shortened or reset"
        elif sha(raw[:previous["cursor_bytes"]]) != previous.get("prefix_sha256"):
            delta_reason = "saved session changed before prior cursor (compaction or rewrite)"
        else:
            prior_bytes = previous.get("text_bytes")
            if type(prior_bytes) is int and report["text_bytes"] >= prior_bytes:
                delta = report["estimated_tokens"] - ((prior_bytes + 3) // 4)
                delta_reason = None
            else:
                delta_reason = "measured text size decreased"
    stamp = now or datetime.now(timezone.utc).isoformat(timespec="seconds")
    def write_preview(row):
        preview = format_preview(row)
        if preview_path:
            relative = history.resolve().relative_to(repo_root).as_posix()
            atomic_write(preview_path, (json.dumps({"version": 1, "preview": preview,
                "history_url": f"https://github.com/mhaduk/ck3-dynasty-map/blob/{repository_ref}/{relative}"}, indent=2) + "\n").encode())
        return preview

    if (saved_task and saved_task.get("method") == VERSION
            and saved_task.get("identity_hash") == key
            and saved_task.get("source_sha256") == sha(raw)
            and saved_task.get("handoff") == handoff and existing):
        last = existing[-1]
        return {"record": last, "preview": write_preview(last), "idempotent": True}
    row = {
        "version": 1, "task": task, "measured_at": stamp, "method": VERSION,
        "handoff_sequence": len(existing) + 1, "handoff": handoff, "measurement_provenance": "heuristic",
        "session_text": {
            "messages": report["message_count"], "characters": report["character_count"],
            "utf8_bytes": report["text_bytes"],
        },
        "context_tokens": {"value": report["estimated_tokens"], "status": "estimated", "method": "ceil(known_utf8_bytes/4)"},
        "delta_tokens": {"value": delta, "status": "estimated" if delta is not None else "unknown", "reason": delta_reason},
        "model": report["model"], "reasoning_level": report["reasoning_level"],
        "source_timestamp": report["source_timestamp"],
        "provenance": "explicit local saved-session input; aggregate only",
    }
    if any(item.get("measured_at") == stamp for item in existing):
        raise ValueError("history retry conflicts with existing measurement")
    state["sessions"][task] = {
        "method": VERSION, "handoff": handoff, "identity_hash": key, "cursor_bytes": len(raw),
        "prefix_sha256": sha(raw), "text_bytes": report["text_bytes"],
        "source_path": str(source), "source_sha256": sha(raw), "source_timestamp": report["source_timestamp"],
    }
    history_data = "".join(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n" for item in existing + [row]).encode()
    state["sessions"][task]["history_sha256"] = sha(history_data)
    state["last_session"] = dict(state["sessions"][task])
    atomic_write(history, history_data)
    atomic_write(private, (json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode())
    return {"record": row, "preview": write_preview(row), "idempotent": False}


def format_preview(row: dict) -> str:
    token = row["context_tokens"]["value"]
    delta = row["delta_tokens"]["value"]
    first = f"GUI session estimate: ~{token:,} estimated tokens"
    if delta is not None:
        first += f" (+{delta:,} since previous handoff)"
    return first + f"\nGUI session: {row['session_text']['messages']} messages / {row['session_text']['utf8_bytes']:,} UTF-8 bytes"


def record_timing_pair(repo: Path, task_id: str, calibration_path: Path) -> dict:
    """Persist one completed task's frozen estimate and claim-to-complete interval."""
    if not re.fullmatch(r"[A-Z][A-Z0-9]*-[A-Z0-9]+(?:-[A-Z0-9]+)*", task_id):
        raise ValueError("invalid per-ID handoff ID")
    repo = repo.resolve(strict=True)
    task_dir = repo / ".codex-sync/tasks" / task_id
    for directory in (repo / ".codex-sync", repo / ".codex-sync/tasks", task_dir):
        if directory.is_symlink():
            raise ValueError("symlink handoff path refused")
    status_path = safe_file(task_dir / "STATUS.json", exists=True)
    task_path = safe_file(task_dir / "CLI_TASK.md", exists=True)
    for source in (status_path, task_path):
        try:
            relative = source.relative_to(repo)
        except ValueError as exc:
            raise ValueError("handoff input escapes repository") from exc
        current = repo
        for part in relative.parts:
            current = current / part
            if current.is_symlink():
                raise ValueError("symlink handoff input refused")
    status = json.loads(status_path.read_text(encoding="utf-8"))
    text = task_path.read_text(encoding="utf-8")
    if status.get("id") != task_id or status.get("status") not in {"COMPLETED", "CONSUMED"}:
        raise ValueError("timing pair requires a completed handoff")
    estimate = re.search(r"(?m)^Estimated CLI time(?:\s*/\s*steps)?: (\d+)\s*[–-]\s*(\d+)\s*(?:minutes?|minut|min)\b", text)
    low, high = (int(estimate.group(1)), int(estimate.group(2))) if estimate else (None, None)
    if low is not None and (low < 1 or high < low):
        raise ValueError("invalid frozen estimate range")
    claimed, completed = status.get("claimed_at"), status.get("completed_at")
    try:
        elapsed = (datetime.fromisoformat(completed) - datetime.fromisoformat(claimed)).total_seconds() / 60
    except (TypeError, ValueError) as exc:
        raise ValueError("claim/completion timestamps missing or invalid") from exc
    if elapsed < 0:
        raise ValueError("completion precedes claim")
    pair = {
        "delegation_id": task_id, "attempt": status.get("attempt"),
        "status": "COMPLETED", "claimed_at": claimed, "completed_at": completed,
        "original_estimate_range_minutes": [low, high] if low is not None else None,
        "claim_to_complete_elapsed_minutes": round(elapsed, 2),
        "elapsed_kind": "wall elapsed; may include pauses or non-compute time",
        "calibration_eligibility": "GUI comparability review required",
        "use": "candidate pair" if low is not None and status.get("attempt") == 1 else "excluded",
        "reason": None if low is not None and status.get("attempt") == 1 else "missing estimate or retried attempt",
    }
    safe_repo_output(calibration_path, repo, repo)
    calibration = safe_file(calibration_path, exists=calibration_path.exists())
    try:
        relative = calibration.relative_to(repo)
    except ValueError as exc:
        raise ValueError("calibration file must remain inside repository") from exc
    current = repo
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError("symlink calibration path refused")
    data = load_json(calibration, {"schema": "t012-cli-time-calibration/1", "comparable_pairs": 0, "samples": []})
    if not isinstance(data, dict):
        raise ValueError("calibration file must be a JSON object")
    samples = data.get("samples")
    if not isinstance(samples, list) or any(not isinstance(item, dict) for item in samples):
        raise ValueError("calibration samples must be a list")
    for old in samples:
        if old.get("delegation_id") == task_id and old.get("attempt") == status.get("attempt"):
            if old == pair:
                return {"pair": pair, "idempotent": True}
            raise ValueError("timing pair conflicts with existing calibration record")
    samples.append(pair)
    data["samples"] = samples
    data["comparable_pairs"] = sum(1 for item in samples if item.get("use") == "eligible pair")
    atomic_write(calibration, (json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode())
    return {"pair": pair, "idempotent": False}


def mark_timing_pair_eligible(calibration_path: Path, task_id: str, review_note: str,
                              repo_root: Path | None = None) -> dict:
    """Record the GUI's comparability decision; this helper does not make it."""
    if not review_note.strip() or len(review_note) > 500:
        raise ValueError("comparability review note must be nonempty and at most 500 characters")
    if calibration_path.is_symlink():
        raise ValueError("symlink calibration path refused")
    if repo_root is not None:
        repo_root = repo_root.resolve(strict=True)
        safe_repo_output(calibration_path, repo_root, repo_root)
    calibration = safe_file(calibration_path, exists=True)
    data = load_json(calibration, {})
    if not isinstance(data, dict) or not isinstance(data.get("samples"), list):
        raise ValueError("invalid calibration sample file")
    found = [row for row in data["samples"] if isinstance(row, dict) and row.get("delegation_id") == task_id]
    if len(found) != 1:
        raise ValueError("expected one saved timing candidate for the handoff")
    pair = found[0]
    if pair.get("use") not in {"candidate pair", "eligible pair"} or not pair.get("original_estimate_range_minutes"):
        raise ValueError("timing candidate lacks a frozen estimate range")
    if pair.get("attempt") != 1 or pair.get("status") not in {"COMPLETED", "CONSUMED"}:
        raise ValueError("only a completed first-attempt pair can be eligible")
    pair["use"] = "eligible pair"
    pair["calibration_eligibility"] = "GUI reviewed comparable"
    pair["comparability_review_note"] = review_note.strip()
    data["comparable_pairs"] = sum(1 for row in data["samples"] if isinstance(row, dict) and row.get("use") == "eligible pair")
    atomic_write(calibration, (json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode())
    return {"delegation_id": task_id, "comparable_pairs": data["comparable_pairs"]}


def calibrated_estimate(low: int, high: int, samples: list[dict], *, minimum_pairs: int = 3) -> dict:
    if type(low) is not int or type(high) is not int or low < 1 or high < low:
        raise ValueError("estimate range must contain positive ordered whole minutes")
    pairs = []
    for row in samples:
        if not isinstance(row, dict) or row.get("use") != "eligible pair":
            continue
        estimate = row.get("original_estimate_range_minutes")
        actual = row.get("claim_to_complete_elapsed_minutes")
        if (isinstance(estimate, list) and len(estimate) == 2
                and all(type(value) is int and value > 0 for value in estimate)
                and isinstance(actual, (int, float)) and actual >= 0):
            midpoint = (estimate[0] + estimate[1]) / 2
            pairs.append((actual / midpoint, row.get("delegation_id")))
    if len(pairs) >= minimum_pairs:
        ratios = sorted(value for value, _ in pairs)
        middle = len(ratios) // 2
        factor = ratios[middle] if len(ratios) % 2 else (ratios[middle - 1] + ratios[middle]) / 2
        return {
            "range_minutes": [max(1, math.floor(low * factor)), max(1, math.ceil(high * factor))],
            "basis": "measured median actual/estimate-midpoint ratio",
            "pairs_used": len(pairs), "multiplier": round(factor, 4),
            "observed_multiplier_range": [round(ratios[0], 4), round(ratios[-1], 4)],
            "uncertainty": "estimate span retained; observed pair ratio spread shown; small samples may shift",
        }
    return {
        "range_minutes": [max(1, math.floor(low / 3)), max(1, math.ceil(high / 2))],
        "basis": "user-observed 2–3× overestimate prior; not measured calibration",
        "pairs_used": len(pairs), "multiplier": None,
        "uncertainty": "broad prior range retained until at least three comparable pairs exist",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session", type=Path, help="one explicitly identified saved session file")
    parser.add_argument("--task", help="stable parent task ID")
    parser.add_argument("--repository-ref", default="main", help="published ref for stable aggregate history links")
    parser.add_argument("--handoff", help="public delegation ID; distinguishes distinct handoffs with unchanged text")
    parser.add_argument("--identity", help="stable opaque private identity; never persisted publicly")
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--preview", type=Path, help="private or ephemeral JSON preview file")
    parser.add_argument("--timing-task-id", help="record a completed handoff estimate/elapsed pair instead of measuring a session")
    parser.add_argument("--timing-eligible", help="mark a candidate comparable after explicit GUI review")
    parser.add_argument("--review-note", help="brief rationale required with --timing-eligible")
    parser.add_argument("--estimate-min", type=int, help="raw GUI range low endpoint for estimate mode")
    parser.add_argument("--estimate-max", type=int, help="raw GUI range high endpoint for estimate mode")
    parser.add_argument("--steps", type=int, help="frozen execution-plan step count")
    parser.add_argument("--calibration", type=Path, default=Path(".codex-sync/gui-context-calibration.json"))
    args = parser.parse_args(argv)
    repo = args.repo.resolve(strict=True)
    repo_argument = args.repo.absolute()

    def repo_path(path: Path) -> Path:
        if not path.is_absolute():
            return repo / path
        try:
            relative = path.absolute().relative_to(repo_argument)
        except ValueError as exc:
            raise ValueError("output path must be within the supplied repository path") from exc
        return repo / relative

    if args.timing_task_id:
        try:
            result = record_timing_pair(repo, args.timing_task_id, repo_path(args.calibration))
            print(json.dumps(result, sort_keys=True))
            return 0
        except (OSError, ValueError, UnicodeError) as exc:
            print(f"gui-context: {exc}", file=sys.stderr)
            return 2
    if args.timing_eligible:
        if not args.review_note:
            parser.error("--timing-eligible requires --review-note")
        try:
            calibration = repo_path(args.calibration)
            safe_repo_output(calibration, repo, repo)
            print(json.dumps(mark_timing_pair_eligible(calibration, args.timing_eligible, args.review_note, repo), sort_keys=True))
            return 0
        except (OSError, ValueError, UnicodeError) as exc:
            print(f"gui-context: {exc}", file=sys.stderr)
            return 2
    if args.estimate_min is not None or args.estimate_max is not None:
        if args.estimate_min is None or args.estimate_max is None:
            parser.error("estimate mode requires both --estimate-min and --estimate-max")
        try:
            calibration = repo_path(args.calibration)
            safe_repo_output(calibration, repo, repo)
            calibration = safe_file(calibration, exists=calibration.exists())
            data = load_json(calibration, {"samples": []})
            if not isinstance(data, dict) or not isinstance(data.get("samples"), list):
                raise ValueError("invalid calibration sample file")
            result = calibrated_estimate(args.estimate_min, args.estimate_max, data["samples"]) if args.steps is not None else {
                "range_minutes": [args.estimate_min, args.estimate_max],
                "basis": "uncalibrated planless estimate", "pairs_used": 0}
            if args.estimate_min < 1 or args.estimate_max < args.estimate_min:
                raise ValueError("estimate range must contain positive ordered whole minutes")
            if args.steps is not None:
                if not 1 <= args.steps <= 20:
                    raise ValueError("planned steps must be between 1 and 20")
                result["planned_steps"] = args.steps
            result["formatted"] = f"~{result['range_minutes'][0]}–{result['range_minutes'][1]} minutes ({result['basis']}); " + (f"{result['planned_steps']} planned steps" if args.steps is not None else "no plan")
            print(json.dumps(result, ensure_ascii=False, sort_keys=True))
            return 0
        except (OSError, ValueError, UnicodeError) as exc:
            print(f"gui-context: {exc}", file=sys.stderr)
            return 2
    if not args.session or not args.task or not args.identity:
        parser.error("session measurement requires --session, --task and --identity")
    history = repo / PUBLIC_ROOT / f"{args.task}.jsonl"
    private = repo / PRIVATE_STATE
    preview = repo_path(args.preview) if args.preview else None
    try:
        result = measure(args.session, args.task, args.identity, private, history, preview, handoff=args.handoff, repository_ref=args.repository_ref)
        print(result["preview"])
    except (OSError, ValueError, UnicodeError) as exc:
        print(f"gui-context: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
