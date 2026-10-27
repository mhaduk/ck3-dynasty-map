#!/usr/bin/env python3
"""Capture and summarize an explicit byte interval from local logs.

This is a bounded checkpoint tool, not a CK3 parser. It never changes source
files; stdout includes bounded error-message snippets.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import sys

DEFAULT_LOGS = ("debug.log", "error.log", "gui_warnings.log", "database_conflicts.log", "game.log")
CHUNK = 64 * 1024
SAMPLE = 256
MAX_ERROR_MESSAGES = 250
ERROR_RE = re.compile(r"\b(error|exception|failed|fatal)\b", re.IGNORECASE)
STAMP_RE = re.compile(r"^\s*\[[^]]+\]\s*")


class CheckpointError(Exception):
    pass


def now():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_write(path: Path, obj):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(obj, stream, indent=2, sort_keys=True)
        stream.write("\n")
    os.chmod(path, 0o600)


def checked_path(path: Path, *, must_exist=False, directory=None):
    path = Path(os.path.abspath(path))
    # macOS exposes these standard locations through root symlink aliases.
    if path.parts[:2] == ("/", "var") and Path("/var").is_symlink() and Path(os.path.realpath("/var")) == Path("/private/var"):
        path = Path("/private/var") / Path(*path.parts[2:])
    elif path.parts[:2] == ("/", "tmp") and Path("/tmp").is_symlink() and Path(os.path.realpath("/tmp")) == Path("/private/tmp"):
        path = Path("/private/tmp") / Path(*path.parts[2:])
    current = Path(path.anchor)
    for part in path.parts[1:]:
        current = current / part
        if current.is_symlink():
            raise CheckpointError(f"symlink path refused: {current}")
    if must_exist and not path.exists():
        raise CheckpointError(f"missing path: {path}")
    if path.exists():
        if directory is True and not path.is_dir():
            raise CheckpointError(f"expected directory: {path}")
        if directory is False and not path.is_file():
            raise CheckpointError(f"expected regular file: {path}")
    return path


def sample_file(stream, size):
    if size == 0:
        return {"head": sha(b""), "tail": sha(b"")}
    stream.seek(0)
    head = stream.read(min(SAMPLE, size))
    stream.seek(max(0, size - SAMPLE))
    tail = stream.read(min(SAMPLE, size))
    return {"head": sha(head), "tail": sha(tail)}


def collect_sources(args):
    paths = []
    explicit_names = set()
    if args.log_dir:
        root = checked_path(Path(args.log_dir), must_exist=True, directory=True)
        names = args.name or list(DEFAULT_LOGS)
        for name in names:
            if Path(name).name != name or name in {".", ".."}:
                raise CheckpointError(f"log name must be a direct child name: {name!r}")
            paths.append((name, root / name))
    for raw in args.file or []:
        p = checked_path(Path(raw), must_exist=True, directory=False)
        paths.append((p.name, p))
        explicit_names.add(p.name)
    if not paths:
        raise CheckpointError("provide --log-dir or at least one --file")
    names = [name for name, _ in paths]
    if len(set(names)) != len(names):
        raise CheckpointError("input names must be unique")
    required = explicit_names | set(args.required_name or [])
    unknown_required = required - set(names)
    if unknown_required:
        raise CheckpointError(f"required log name was not selected: {sorted(unknown_required)[0]}")
    return [(name, path, name in required) for name, path in paths]


def baseline(args):
    output = checked_path(Path(args.output))
    if output.exists():
        raise CheckpointError(f"refusing to overwrite: {output}")
    if not output.parent.is_dir():
        raise CheckpointError(f"output parent must already exist: {output.parent}")
    sources = collect_sources(args)
    for _, source, _ in sources:
        if output.parent == source.parent or source.parent in output.parent.parents:
            raise CheckpointError("baseline output must be outside source log directories")
    records = {}
    for name, path, required in sources:
        if not path.exists():
            records[name] = {"state": "MISSING", "path": str(path), "required": required}
            continue
        source = checked_path(path, must_exist=True, directory=False)
        fd = os.open(source, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        with os.fdopen(fd, "rb") as stream:
            before = os.fstat(stream.fileno())
            sample = sample_file(stream, before.st_size)
            stream.seek(max(0, before.st_size - 1))
            line_boundary = before.st_size == 0 or stream.read(1) in (b"\n", b"\r")
            after = os.fstat(stream.fileno())
        if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns):
            records[name] = {"state": "UNCERTAIN_DURING_BASELINE", "path": str(source), "required": required}
            continue
        records[name] = {
            "state": "READY", "path": str(source), "required": required, "device": before.st_dev,
            "inode": before.st_ino, "offset": before.st_size,
            "mtime_ns": before.st_mtime_ns, "boundary": sample,
            "line_boundary": line_boundary,
        }
    doc = {
        "format": 1, "checkpoint_id": args.checkpoint_id or secrets.token_hex(8),
        "captured_at": now(), "payload_label": args.payload_label or "unknown",
        "build_label": args.build_label or "unknown", "logs": records,
        "fingerprint_limits": "Samples cover the first and last 256 baseline bytes; arbitrary same-size overwrites elsewhere cannot be ruled out.",
    }
    json_write(output, doc)
    ready = sum(v["state"] == "READY" for v in records.values())
    missing = sum(v["state"] == "MISSING" for v in records.values())
    print(f"Baseline {doc['checkpoint_id']}: {ready} ready, {missing} missing; manifest {output}")


def safe_slug(value):
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("._")
    return slug[:80] or "log"


def read_spec(path):
    if not path:
        return {"markers": [], "chains": []}
    p = checked_path(Path(path), must_exist=True, directory=False)
    try:
        obj = json.loads(p.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        raise CheckpointError(f"cannot read marker specification: {exc}") from exc
    if not isinstance(obj, dict) or set(obj) - {"markers", "chains"}:
        raise CheckpointError("spec must contain only markers and chains")
    for key in ("markers", "chains"):
        if not isinstance(obj.get(key, []), list):
            raise CheckpointError(f"{key} must be a list")
    for entry in obj.get("markers", []):
        if not isinstance(entry, dict) or not isinstance(entry.get("literal"), str) or not entry["literal"]:
            raise CheckpointError("each marker needs a nonempty literal")
        if "expected" in entry and (not isinstance(entry["expected"], int) or isinstance(entry["expected"], bool) or entry["expected"] < 0):
            raise CheckpointError("marker expected count must be a nonnegative integer")
        if "name" in entry and not isinstance(entry["name"], str):
            raise CheckpointError("marker name must be text")
        if "log" in entry and not isinstance(entry["log"], str):
            raise CheckpointError("marker log must be text")
    for entry in obj.get("chains", []):
        if not isinstance(entry, dict) or not all(isinstance(entry.get(k), str) and entry[k] for k in ("begin", "end")):
            raise CheckpointError("each chain needs nonempty begin and end literals")
        if "reject" in entry and (not isinstance(entry["reject"], str) or not entry["reject"]):
            raise CheckpointError("chain reject must be nonempty text")
        for key in ("name", "log"):
            if key in entry and not isinstance(entry[key], str):
                raise CheckpointError(f"chain {key} must be text")
    return obj


def ordered_events(text, entry):
    """All literal occurrences; overlapping spans have no unambiguous order."""
    events = []
    for kind in ("begin", "end", "reject"):
        literal = entry.get(kind)
        if literal is None:
            continue
        start = text.find(literal)
        while start >= 0:
            events.append((start, start + len(literal), kind))
            start = text.find(literal, start + 1)
    events.sort()
    if any(left[1] > right[0] for left, right in zip(events, events[1:])):
        raise CheckpointError("ambiguous overlapping chain literals in captured text")
    return events


def analyze(captures, spec, log_status):
    per_log, errors, markers, chains = {}, {}, [], []
    expectations_met = True
    marker_counts = Counter()
    omitted_error_lines = 0
    for name, data in captures.items():
        initial = log_status[name].get("partial_initial_line", False)
        final = bool(data and not data.endswith((b"\n", b"\r")))
        info = {"partial_initial_line": initial, "partial_final_line": final,
                "error_detection": "error channel (nonempty complete lines)" if name == "error.log"
                else "English severity keyword heuristic (complete lines)"}
        # Preserve all bytes in the artifact, but analyze only complete lines.
        lines = data.splitlines(keepends=True)
        if initial and lines:
            info["excluded_initial_fragment_bytes"] = len(lines.pop(0))
        if final and lines:
            info["excluded_final_fragment_bytes"] = len(lines.pop())
        parsed = b"".join(lines)
        text = parsed.decode("utf-8", errors="replace")
        error_lines = 0
        for line in text.splitlines():
            if line.strip() and (name == "error.log" or ERROR_RE.search(line)):
                message = STAMP_RE.sub("", line).strip()
                # Hash the full normalized message; only its displayed summary is clipped.
                identity = sha(message.encode("utf-8"))
                if identity in errors:
                    errors[identity]["occurrences"] += 1
                elif len(errors) < MAX_ERROR_MESSAGES:
                    errors[identity] = {"message": message[:240], "message_sha256": identity, "occurrences": 1}
                else:
                    omitted_error_lines += 1
                error_lines += 1
        info["error_lines"] = error_lines
        per_log[name] = info
        for entry in spec.get("markers", []):
            if entry.get("log") in (None, name):
                marker_counts[entry.get("name", entry["literal"])] += parsed.count(entry["literal"].encode("utf-8"))
        for entry in spec.get("chains", []):
            if entry.get("log") not in (None, name):
                continue
            open_begin = False
            state = {"name": entry.get("name", "chain"), "log": name, "pairs": 0, "incomplete": 0, "rejected": 0, "out_of_order": 0}
            for _, _, kind in ordered_events(text, entry):
                if kind == "reject":
                    state["rejected"] += 1
                    if open_begin:
                        state["incomplete"] += 1
                        open_begin = False
                elif kind == "begin":
                    if open_begin:
                        state["incomplete"] += 1
                        state["out_of_order"] += 1
                    open_begin = True
                elif open_begin:
                    state["pairs"] += 1
                    open_begin = False
                else:
                    state["out_of_order"] += 1
            if open_begin:
                state["incomplete"] += 1
            if state["incomplete"] or state["rejected"] or state["out_of_order"]:
                expectations_met = False
            chains.append(state)
    for entry in spec.get("markers", []):
        name = entry.get("name", entry["literal"])
        observed = marker_counts[name]
        expected = entry.get("expected")
        markers.append({"name": name, "observed": observed, "expected": expected})
        if expected is not None and observed != expected:
            expectations_met = False
    return {"per_log": per_log, "unique_new_errors": list(errors.values()),
            "new_error_lines": sum(item["error_lines"] for item in per_log.values()),
            "omitted_error_lines_after_summary_cap": omitted_error_lines,
            "markers": markers, "chains": chains, "expectations_met": expectations_met}


def delta(args):
    baseline_path = checked_path(Path(args.baseline), must_exist=True, directory=False)
    try:
        base = json.loads(baseline_path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        raise CheckpointError(f"invalid baseline: {exc}") from exc
    if base.get("format") != 1 or not isinstance(base.get("logs"), dict):
        raise CheckpointError("unsupported baseline format")
    out = checked_path(Path(args.output_dir))
    if out.exists():
        raise CheckpointError(f"refusing to overwrite checkpoint: {out}")
    if not out.parent.is_dir():
        raise CheckpointError(f"output parent must already exist: {out.parent}")
    for record in base["logs"].values():
        if record.get("state") == "READY":
            source = Path(record["path"])
            if out == source.parent or out in source.parents or source.parent in out.parents:
                raise CheckpointError("output directory overlaps a source log directory")
    spec = read_spec(args.spec)
    out.mkdir(mode=0o700)
    manifest_logs, captures, global_complete = {}, {}, True
    remaining = args.max_bytes
    for name, record in base["logs"].items():
        required = record.get("required", True)
        status = {"captured_bytes": 0, "state": record.get("state", "INVALID_BASELINE"), "required": required}
        if record.get("state") != "READY":
            status.update(reason="baseline entry is missing or uncertain", incomplete=True)
            global_complete = global_complete and not required
            manifest_logs[name] = status
            continue
        source = Path(record["path"])
        if not source.exists():
            status.update(state="MISSING", reason="source disappeared", incomplete=True)
            global_complete = global_complete and not required
            manifest_logs[name] = status
            continue
        try:
            source = checked_path(source, must_exist=True, directory=False)
            fd = os.open(source, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
            with os.fdopen(fd, "rb") as stream:
                before = os.fstat(stream.fileno())
                if (before.st_dev, before.st_ino) != (record["device"], record["inode"]):
                    status.update(state="REPLACED", reason="file identity changed", incomplete=True)
                    global_complete = global_complete and not required
                    manifest_logs[name] = status
                    continue
                if before.st_size < record["offset"]:
                    status.update(state="TRUNCATED", reason="size is below baseline cursor", incomplete=True)
                    global_complete = global_complete and not required
                    manifest_logs[name] = status
                    continue
                stream.seek(record["offset"])
                stream.seek(0)
                current_head = stream.read(min(SAMPLE, record["offset"]))
                stream.seek(max(0, record["offset"] - SAMPLE))
                current_tail = stream.read(min(SAMPLE, record["offset"]))
                if (sha(current_head) != record["boundary"]["head"]
                        or sha(current_tail) != record["boundary"]["tail"]):
                    status.update(state="BOUNDARY_CHANGED", reason="sample before baseline cursor differs", incomplete=True)
                    global_complete = global_complete and not required
                    manifest_logs[name] = status
                    continue
                line_boundary = record["offset"] == 0 or current_tail[-1:] in (b"\n", b"\r")
                if "line_boundary" in record and record["line_boundary"] != line_boundary:
                    raise CheckpointError("baseline line boundary differs from source")
                status["partial_initial_line"] = not line_boundary
                started_at = now()
                start = record["offset"]
                end = before.st_size
                stream.seek(max(0, end - SAMPLE))
                frozen_end_sample = stream.read(min(SAMPLE, end))
                frozen_end_digest = sha(frozen_end_sample)
                allowance = max(0, remaining)
                capture_end = min(end, start + allowance)
                dest = out / (safe_slug(name) + ".delta")
                hasher = hashlib.sha256()
                captured = bytearray()
                with dest.open("xb") as target:
                    os.chmod(dest, 0o600)
                    stream.seek(start)
                    while stream.tell() < capture_end:
                        block = stream.read(min(CHUNK, capture_end - stream.tell()))
                        if not block:
                            break
                        target.write(block)
                        hasher.update(block)
                        captured.extend(block)
                    target.flush()
                    os.fsync(target.fileno())
                after = os.fstat(stream.fileno())
                try:
                    path_after = os.stat(source, follow_symlinks=False)
                    stream.seek(0)
                    post_head = stream.read(min(SAMPLE, record["offset"]))
                    stream.seek(max(0, record["offset"] - SAMPLE))
                    post_boundary = stream.read(min(SAMPLE, record["offset"]))
                    stream.seek(max(0, end - SAMPLE))
                    post_end_sample = stream.read(min(SAMPLE, end))
                except OSError:
                    path_after = None
                    post_head = b""
                    post_boundary = b""
                    post_end_sample = b""
                read_count = len(captured)
                captures[name] = bytes(captured)
                state = "CAPTURED"
                reasons = []
                if not line_boundary:
                    reasons.append("baseline cursor starts inside a line; initial fragment excluded from analysis")
                if read_count != capture_end - start:
                    state = "PARTIAL_READ"
                    reasons.append("short read before frozen end")
                if capture_end < end:
                    state = "CAPPED"
                    reasons.append("configured total byte cap reached")
                if ((after.st_dev, after.st_ino) != (before.st_dev, before.st_ino)
                        or after.st_size < end or path_after is None
                        or (path_after.st_dev, path_after.st_ino) != (before.st_dev, before.st_ino)
                        or sha(post_head) != record["boundary"]["head"]
                        or sha(post_boundary) != record["boundary"]["tail"]
                        or sha(post_end_sample) != frozen_end_digest):
                    state = "CHANGED_DURING_READ"
                    reasons.append("identity, size, or sampled boundary changed during capture")
                if after.st_size > end:
                    status["appended_after_boundary"] = after.st_size - end
                if not captured.endswith((b"\n", b"\r")) and captured:
                    status["partial_final_line"] = True
                    reasons.append("captured interval ends inside a line")
                if state != "CAPTURED" or reasons:
                    status["incomplete"] = True
                if (state != "CAPTURED" or reasons) and required:
                    global_complete = False
                status.update(state=state, reason="; ".join(reasons) or None, captured_bytes=read_count,
                              source_size_at_boundary=end, start_offset=start, end_offset=start + read_count,
                              sha256=hasher.hexdigest(), captured_file=dest.name,
                              started_at=started_at, ended_at=now())
                remaining -= read_count
        except (OSError, CheckpointError) as exc:
            status.update(state="READ_ERROR", reason=str(exc))
            status["required"] = required
            status["incomplete"] = True
            global_complete = global_complete and not required
        manifest_logs[name] = status
    analysis = analyze(captures, spec, manifest_logs)
    any_incomplete = any(item.get("incomplete") or item.get("state") != "CAPTURED" for item in manifest_logs.values())
    verdict = "COMPLETE" if global_complete and not any_incomplete else ("COMPLETE_WITH_OPTIONAL_GAPS" if global_complete else "INCOMPLETE")
    evidence_complete = not any_incomplete
    expectation_status = "UNVERIFIED_INCOMPLETE_EVIDENCE" if not evidence_complete else ("MET" if analysis["expectations_met"] else "UNMET")
    observation_status = "ERRORS_OR_REJECTIONS_OBSERVED" if analysis["new_error_lines"] or any(c["rejected"] for c in analysis["chains"]) else "NONE_OBSERVED_IN_ANALYZED_LINES"
    doc = {"format": 1, "checkpoint_id": secrets.token_hex(8), "baseline_id": base["checkpoint_id"],
           "captured_at": now(), "payload_label": base.get("payload_label", "unknown"),
           "build_label": base.get("build_label", "unknown"), "logs": manifest_logs,
           "analysis": analysis, "interval_status": verdict,
           "expectation_status": expectation_status, "observation_status": observation_status,
           "limits": ["A required gap makes the interval incomplete.", "Literal markers and equal counts do not prove event identity.",
                      "WRITE_RETURNED can support an execution receipt only; it does not prove stored RGB, classification or visual acceptance.",
                      "Per-log capture times are separate; this is not an atomic multi-file snapshot.",
                      "Exit success and interval completeness do not establish clean logs, correct classification, stored RGB or visual acceptance.",
                      "Initial and final line fragments are preserved but excluded from analysis; other-log severity detection is heuristic."]}
    json_write(out / "manifest.json", doc)
    report = [f"Checkpoint {doc['checkpoint_id']} — interval: {verdict}",
              f"Observations: {observation_status}; marker/chain expectations: {expectation_status}", f"Baseline: {doc['baseline_id']}; payload: {doc['payload_label']}; build: {doc['build_label']}"]
    for name, item in manifest_logs.items():
        line = f"{name}: {item.get('state')}, {item.get('captured_bytes', 0)} bytes, {'required' if item.get('required') else 'optional'}"
        if item.get("appended_after_boundary"):
            line += f"; {item['appended_after_boundary']} bytes appended after boundary"
        if item.get("reason"):
            line += f"; {item['reason']}"
        report.append(line)
    report.append("Error detection: error.log uses nonempty complete lines; other logs use an English severity keyword heuristic.")
    report.append(f"New error lines: {analysis['new_error_lines']}; unique summarized new error messages: {len(analysis['unique_new_errors'])}")
    report.extend(f"  {entry['occurrences']} × [{entry['message_sha256'][:12]}] {entry['message']}" for entry in analysis["unique_new_errors"][:20])
    if analysis["omitted_error_lines_after_summary_cap"]:
        report.append(f"Error lines omitted after the {MAX_ERROR_MESSAGES}-message summary cap: {analysis['omitted_error_lines_after_summary_cap']}")
    report.extend(f"Marker {entry['name']}: observed {entry['observed']}, expected {entry['expected']}" for entry in analysis["markers"])
    report.extend(f"Chain {entry['name']}: {entry['pairs']} pairs, {entry['incomplete']} incomplete, {entry['rejected']} rejected, {entry['out_of_order']} out of order" for entry in analysis["chains"])
    report.append("Limits: sampled fingerprints cannot detect every same-size rewrite; literal markers show observed text, not event identity; file intervals are not atomic across logs.")
    report.append("Exit success and interval completeness do not establish clean logs, correct classification, stored RGB or visual acceptance.")
    report.append("Captured bytes and private manifest are stored in this checkpoint directory.")
    (out / "report.txt").write_text("\n".join(report) + "\n", encoding="utf-8")
    os.chmod(out / "report.txt", 0o600)
    print("\n".join(report))


def parser():
    root = argparse.ArgumentParser(description=__doc__)
    sub = root.add_subparsers(dest="command", required=True)
    b = sub.add_parser("baseline", help="record explicit per-log cursors")
    b.add_argument("--log-dir")
    b.add_argument("--name", action="append", help="direct-child log name; repeatable")
    b.add_argument("--required-name", action="append", default=[], help="mark a named log as required; repeatable")
    b.add_argument("--file", action="append", help="explicit log file; repeatable")
    b.add_argument("--output", required=True)
    b.add_argument("--checkpoint-id")
    b.add_argument("--payload-label")
    b.add_argument("--build-label")
    b.set_defaults(func=baseline)
    d = sub.add_parser("delta", help="freeze and summarize bytes appended after a baseline")
    d.add_argument("--baseline", required=True)
    d.add_argument("--output-dir", required=True)
    d.add_argument("--spec", help="optional JSON literal marker and chain specification")
    d.add_argument("--max-bytes", type=int, default=8 * 1024 * 1024, help="total capture cap, default 8 MiB")
    d.set_defaults(func=delta)
    return root


def main(argv=None):
    args = parser().parse_args(argv)
    if getattr(args, "max_bytes", 1) < 0:
        parser().error("--max-bytes must be nonnegative")
    try:
        args.func(args)
    except (CheckpointError, OSError, ValueError, KeyError, TypeError) as exc:
        print(f"checkpoint error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
