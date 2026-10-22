#!/usr/bin/env python3
"""Offline, explicitly mapped Codex usage accounting and description preview.

No discovery, network calls or source writes. Source intervals and attribution
are supplied in a private JSON manifest; output contains aggregates only.
"""
import argparse
import hashlib
import json
from pathlib import Path

VERSION = "task-ai-cost/1"
START = "<!-- ai-cost:start -->"
END = "<!-- ai-cost:end -->"
FIELDS = ("input_tokens", "cached_input_tokens", "output_tokens",
          "reasoning_output_tokens", "total_tokens")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def replace_suffix(body, fragment, expected_sha256):
    """Preserve every prefix character; refuse drift and ambiguous markers."""
    if sha(body.encode()) != expected_sha256:
        raise ValueError("description body drift")
    if (fragment.count(START) != 1 or fragment.count(END) != 1
            or not fragment.startswith(START) or not fragment.endswith(END)):
        raise ValueError("invalid fragment")
    if START in body or END in body:
        if body.count(START) != 1 or body.count(END) != 1:
            raise ValueError("ambiguous existing section")
        a, b = body.index(START), body.index(END)
        if a >= b or body[b + len(END):].strip():
            raise ValueError("managed section must be a suffix")
        # Trailing newlines outside the markers belong to the original body.
        return body[:a] + fragment + body[b + len(END):]
    separator = "" if not body or body.endswith("\n\n") else "\n" if body.endswith("\n") else "\n\n"
    return body + separator + fragment


def valid_usage(u):
    if not isinstance(u, dict):
        raise ValueError("missing usage")
    for k in FIELDS:
        v = u.get(k)
        if v is not None and (type(v) is not int or v < 0):
            raise ValueError("invalid token counter")
    for subset, whole in [("cached_input_tokens", "input_tokens"),
                          ("reasoning_output_tokens", "output_tokens")]:
        if u.get(subset) is not None and u.get(whole) is not None and u[subset] > u[whole]:
            raise ValueError("subset exceeds total")
    if all(u.get(k) is not None for k in ["input_tokens", "output_tokens", "total_tokens"]):
        if u["input_tokens"] + u["output_tokens"] != u["total_tokens"]:
            raise ValueError("unreconciled total")
    return {k: u.get(k) for k in FIELDS}


def records(events, source_thread, seen, mode="responses"):
    """Yield own responses once. Counter-only fallback requires explicit mode.

    The first cumulative counter is a baseline, not newly measured work: forks
    can inherit it. A decrease in any comparable input/output/total counter
    establishes a new baseline for the whole interval. Other fields are
    differenced independently: appearance, loss or a subset decrease yields
    None for that field until two consecutive comparable readings exist.
    Subset deltas exceeding a known whole delta are also unknown. Missing
    counters can hide resets; no missing counter or total is inferred.
    last_token_usage is never added on top. Deltas spanning a model/turn
    change remain unallocated.
    """
    turn, model, previous, previous_turn, previous_model = None, None, None, None, None
    for line, event in enumerate(events, 1):
        p = event.get("payload", {})
        if event["type"] == "event_msg" and p.get("type") == "task_started":
            turn, model = p.get("turn_id"), None
        if event["type"] == "turn_context":
            turn, model = p.get("turn_id"), p.get("model")
        if mode == "responses" and event["type"] == "token_usage_record":
            # Fork histories may contain the parent's usage records.
            if p.get("thread_id") != source_thread:
                continue
            key = p.get("response_id")
            if not key:
                raise ValueError("response identity missing")
            signature = (p.get("thread_id"), p.get("turn_id"), p.get("usage"))
            if key in seen:
                if seen[key] != signature:
                    raise ValueError("conflicting duplicate response")
                continue
            seen[key] = signature
            yield {"line": line, "turn": p.get("turn_id"),
                   "model": model if turn == p.get("turn_id") else None,
                   "usage": valid_usage(p.get("usage"))}
        if mode == "cumulative" and event["type"] == "event_msg" and p.get("type") == "token_count":
            u = (p.get("info") or {}).get("total_token_usage")
            if u is None:
                continue
            u = valid_usage(u)
            core = ("input_tokens", "output_tokens", "total_tokens")
            reset = previous is not None and any(
                u[k] is not None and previous[k] is not None and u[k] < previous[k]
                for k in core)
            if previous is not None and not reset:
                delta = {k: u[k] - previous[k]
                         if u[k] is not None and previous[k] is not None
                         and u[k] >= previous[k] else None for k in FIELDS}
                for subset, whole in [("cached_input_tokens", "input_tokens"),
                                      ("reasoning_output_tokens", "output_tokens")]:
                    if (delta[subset] is not None and delta[whole] is not None
                            and delta[subset] > delta[whole]):
                        delta[subset] = None
                if any(v is not None and v > 0 for v in delta.values()):
                    safe = turn == previous_turn and model == previous_model
                    yield {"line": line, "turn": turn if safe else None,
                           "model": model if safe else None, "usage": valid_usage(delta)}
            previous, previous_turn, previous_model = u, turn, model


def account(mapping):
    if mapping.get("version") != 1:
        raise ValueError("unsupported mapping version")
    assignments = {}
    for a in mapping["assignments"]:
        key = (a["source"], a["turn"])
        if key in assignments:
            raise ValueError("overlapping turn assignment")
        assignments[key] = a["tasks"]
    totals, audit, seen = {}, [], {}
    for i, source in enumerate(mapping["sources"]):
        p = Path(source["path"])
        if not p.is_file():
            raise ValueError("source missing")
        with p.open("rb") as f:
            raw = f.read(source["size_bytes"])
        if len(raw) != source["size_bytes"] or sha(raw) != source["sha256"] or (raw and not raw.endswith(b"\n")):
            raise ValueError("source interval drift or incomplete line")
        es = [json.loads(line) for line in raw.splitlines()]
        mode = source.get("mode", "responses")
        if mode not in ("responses", "cumulative"):
            raise ValueError("unsupported counter mode")
        for r in records(es, source["thread"], seen, mode):
            tasks = assignments.get((i, r["turn"]), [])
            task = tasks[0] if len(tasks) == 1 else None
            model = r["model"] or "unknown"
            audit.append({"source": i, **r, "task": task})
            if task is None:
                continue
            dest = totals.setdefault(task, {}).setdefault(model, {k: 0 for k in FIELDS})
            for k in FIELDS:
                dest[k] = None if dest[k] is None or r["usage"][k] is None else dest[k] + r["usage"][k]
    return {"method": VERSION, "cutoff": mapping["cutoff"], "totals": totals,
            "records": audit}


def fragment(models, cutoff, limitation):
    def row(name, u, coverage):
        v = [u.get(k) for k in FIELDS]
        uncached = v[0] - v[1] if v[0] is not None and v[1] is not None else None
        cells = [v[0], v[1], uncached, v[2], v[3], v[4]]
        return "| " + " | ".join([name] + ["N/A" if x is None else str(x) for x in cells] + [coverage]) + " |"
    lines = [START, "## AI cost", "",
             "| Model | Input total | Cached input (subset) | Uncached input | Output total | Reasoning output (subset) | Total tokens | Coverage |",
             "|---|---:|---:|---:|---:|---:|---:|---|"]
    total = {k: sum(u[k] for u in models.values()) if models and all(u.get(k) is not None for u in models.values()) else None for k in FIELDS}
    for model, usage in sorted(models.items()):
        lines.append(row(model, usage, "partial"))
    if not models:
        lines.append(row("unknown", {}, "unavailable"))
    lines += [row("**Total**", total, "partial" if models else "unavailable"), "",
              f"Method: {VERSION}; evidence cutoff: {cutoff}. Measured response counters only; cached input and reasoning output are subsets, not addends. Uncached input = input minus cached input; total = input plus output where recorded.",
              limitation, END]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    a = sub.add_parser("account")
    a.add_argument("--mapping", type=Path, required=True)
    a.add_argument("--output", type=Path, required=True)
    p = sub.add_parser("preview")
    p.add_argument("--body", type=Path, required=True)
    p.add_argument("--fragment", type=Path, required=True)
    p.add_argument("--expected-sha256", required=True)
    p.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "account":
        mapping = json.loads(args.mapping.read_bytes())
        inputs = [args.mapping] + [Path(s["path"]) for s in mapping["sources"]]
    else:
        inputs = [args.body, args.fragment]
    # Resolution catches path/symlink aliases; samefile catches hardlinks.
    # Check before writing. This is not a concurrent path replacement defense.
    for path in inputs:
        if (args.output.resolve() == path.resolve()
                or (args.output.exists() and args.output.samefile(path))):
            raise ValueError("output aliases input")
    if args.command == "account":
        result = json.dumps(account(mapping), indent=2) + "\n"
    else:
        result = replace_suffix(args.body.read_bytes().decode(), args.fragment.read_bytes().decode(), args.expected_sha256)
    args.output.write_bytes(result.encode())


if __name__ == "__main__":
    main()
