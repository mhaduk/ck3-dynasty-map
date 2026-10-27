#!/usr/bin/env python3
"""Validate post-execution observations and GUI-owned inventory triage."""
from __future__ import annotations

import argparse
from datetime import date
import hashlib
import json
import math
import os
from pathlib import Path
import re
import tempfile
from urllib.parse import unquote

VERSION = 1
MAX_INVENTORY_BYTES = 4 * 1024 * 1024
MAX_ITEMS = 5000
MAX_LEDGER = 10000
CATEGORIES = ("errors_recovery", "execution_time", "token_context_hotspots", "rework", "automation_candidates", "discovery_overhead", "repeated_knowledge_acquisition", "validation_gaps", "scope_process_anomalies")
METRICS = ("time_seconds", "tokens", "rework_count", "manual_effort", "reliability_events")
IMPACTS = {"TIME", "TOKENS", "REWORK", "MANUAL_EFFORT", "RELIABILITY"}
DECISIONS = {"NO ACTION", "KEEP OBSERVING", "MERGE WITH EXISTING OPTIMIZATION", "CREATE OPTIMIZATION TASK", "ESCALATE FOR REVIEW"}
TRENDS = {"NEW", "REPEATED", "WORSENING", "IMPROVING", "RESOLVED", "INCONCLUSIVE"}
KEY_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{1,79}$")
EVIDENCE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/#-]{0,159}$")
PRIVATE_RE = re.compile(r"(?i)(/Users/|/home/|/private/|[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}|(?:token|password|cookie|secret)\s*[:=]|session[_ -]?(?:id|key)?\s*[:=])")


def _public_text(value, label, limit):
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise ValueError(f"{label} must be bounded public-safe text")
    decoded = value
    for _ in range(4):
        nxt = unquote(decoded)
        if nxt == decoded: break
        decoded = nxt
    if PRIVATE_RE.search(decoded) or re.search(r"(?i)(?:^|[/:._ -])session(?:[-_.:]|$)", decoded):
        raise ValueError(f"{label} must be public-safe text without private paths or session identifiers")


def _evidence(value, label="evidence"):
    if not isinstance(value, str) or not EVIDENCE_RE.fullmatch(value):
        raise ValueError(f"{label} must be a bounded public-safe identifier")
    decoded = value
    for _ in range(4):
        nxt = unquote(decoded)
        if nxt == decoded:
            break
        decoded = nxt
    if PRIVATE_RE.search(decoded) or re.search(r"(?i)(?:^|[:/])(?:Users|home|private|var/folders)/", decoded) or re.search(r"(?i)(?:^|[/:._-])session(?:[-_.:]|$)", decoded):
        raise ValueError(f"{label} must not contain private paths or identifiers")
    return value


def _safe_obj(value, label):
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def validate_review(review):
    review = _safe_obj(review, "review")
    if review.get("type") != "post_execution_self_review" or review.get("version") != VERSION or set(review) != {"type", "version", "categories", "cost_hotspots", "metrics"}:
        raise ValueError("unsupported review version")
    categories = _safe_obj(review.get("categories"), "categories")
    if set(categories) != set(CATEGORIES):
        raise ValueError("categories must contain all nine review categories")
    for name, value in categories.items():
        if value != "NONE":
            _public_text(value, name, 1000)
    hotspots = review.get("cost_hotspots")
    if not isinstance(hotspots, list) or len(hotspots) > 5:
        raise ValueError("cost_hotspots must be a list of at most five items")
    for item in hotspots:
        item = _safe_obj(item, "hotspot")
        if set(item) - {"observation", "impacts", "evidence"}:
            raise ValueError("unknown hotspot field")
        _public_text(item.get("observation"), "hotspot observation", 500)
        impacts, evidence = item.get("impacts"), item.get("evidence", [])
        if not isinstance(impacts, list) or not impacts or set(impacts) - IMPACTS:
            raise ValueError("hotspot impacts must use known impact classes")
        if not isinstance(evidence, list):
            raise ValueError("hotspot evidence must be a list")
        for ref in evidence: _evidence(ref, "hotspot evidence")
    metrics = _safe_obj(review.get("metrics"), "metrics")
    allowed = {"elapsed_seconds", "tokens", "rework_count", "manual_operations", "reliability_events"}
    if set(metrics) - allowed: raise ValueError("unknown metric")
    for key, value in metrics.items():
        if value is not None and (not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value) or value < 0):
            raise ValueError(f"{key} must be nonnegative or null")
    return review


def extract_review(body, *, after=0):
    if not isinstance(body, str) or len(body.encode("utf-8")) > 2 * 1024 * 1024:
        raise ValueError("result exceeds the 2 MiB review validation limit")
    blocks = list(re.finditer(r"(?ms)^```json\n(\{.*?\})\n```[ \t]*$", body))
    found = []
    for match in blocks:
        try: value = json.loads(match.group(1))
        except ValueError: continue
        if isinstance(value, dict) and value.get("type") == "post_execution_self_review": found.append((match.start(), value))
    if len(found) != 1: raise ValueError("result must contain exactly one fenced post-execution review JSON")
    if found[0][0] < after: raise ValueError("post-execution review must follow provenance")
    return found[0][1]


def _check_path(path):
    """Reject every untrusted symlink component; permit only macOS /tmp alias."""
    absolute = Path(os.path.abspath(path))
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current = current / part
        if not current.is_symlink(): continue
        trusted_aliases = {"/tmp": "/private/tmp", "/var": "/private/var"}
        if str(current) in trusted_aliases and current.resolve(strict=False) == Path(trusted_aliases[str(current)]):
            current = Path(trusted_aliases[str(current)])
            continue
        raise ValueError("controlled path contains a symlink component")


def _date(value, label):
    try: return date.fromisoformat(value)
    except (TypeError, ValueError) as exc: raise ValueError(f"invalid {label}") from exc


def _empty_inventory(): return {"version": 1, "items": [], "ledger": []}


def _validate_inventory(data):
    if not isinstance(data, dict) or data.get("version") != 1 or not isinstance(data.get("items"), list) or not isinstance(data.get("ledger"), list):
        raise ValueError("invalid inventory schema")
    if len(data["items"]) > MAX_ITEMS or len(data["ledger"]) > MAX_LEDGER: raise ValueError("inventory record limit exceeded")
    keys = set()
    display_ids = set()
    for item in data["items"]:
        if not isinstance(item, dict) or not KEY_RE.fullmatch(str(item.get("key", ""))) or item["key"] in keys: raise ValueError("invalid or duplicate inventory semantic key")
        keys.add(item["key"])
        _validate_item(item)
        if item.get("display_id") is not None:
            if item["display_id"] in display_ids: raise ValueError("duplicate inventory display ID")
            display_ids.add(item["display_id"])
    identities = set()
    for entry in data["ledger"]:
        if not isinstance(entry, dict) or not isinstance(entry.get("identity"), str) or not re.fullmatch(r"[0-9a-f]{64}", str(entry.get("content_sha256", ""))) or not re.fullmatch(r"[0-9a-f]{64}", str(entry.get("report_sha256", ""))): raise ValueError("invalid inventory ledger entry")
        if "cycle_id" in entry and (not isinstance(entry["cycle_id"], str)
                or not re.fullmatch(r"[A-Z][A-Z0-9-]{0,63}", entry["cycle_id"])
                or not entry["identity"].endswith(":" + entry["cycle_id"])):
            raise ValueError("invalid cycle-specific ledger identity")
        if entry["identity"] in identities: raise ValueError("duplicate inventory ledger identity")
        identities.add(entry["identity"])
        if "observation_keys" in entry:
            observation_keys = entry["observation_keys"]
            if not isinstance(observation_keys, list) or any(not isinstance(k, str) or not KEY_RE.fullmatch(k) for k in observation_keys) or len(set(observation_keys)) != len(observation_keys): raise ValueError("invalid ledger observation keys")
        if "date" in entry: _date(entry["date"], "ledger date")
        if "evidence" in entry:
            if not isinstance(entry["evidence"], list): raise ValueError("invalid ledger evidence")
            for ref in entry["evidence"]: _evidence(ref, "ledger evidence")


def _validate_item(item):
    if "display_id" in item and not re.fullmatch(r"OPT-[0-9]{4,8}", str(item["display_id"])): raise ValueError("invalid inventory display ID")
    if "display_id" in item:
        required = {"category", "summary", "first_seen", "last_seen", "occurrence_count", "affected_tasks", "affected_executions", "metric_totals", "trend", "status", "link_history", "boundary_history", "history"}
        if required - set(item): raise ValueError("inventory item is missing required display/history fields")
        if item["category"] not in (*CATEGORIES, "unknown"): raise ValueError("invalid inventory category")
        _public_text(item["summary"], "inventory summary", 160)
        if item["status"] not in {"observing", "resolved", "unknown"}: raise ValueError("invalid inventory status")
        if item["trend"] not in TRENDS: raise ValueError("invalid inventory trend")
        if item.get("linked_optimization_task") is not None:
            link = item["linked_optimization_task"]
            if not isinstance(link, dict) or set(link) != {"status", "id"} or link["status"] not in {"proposed", "verified"} or not re.fullmatch(r"[A-Z][A-Z0-9-]{2,79}", str(link["id"])): raise ValueError("invalid persisted optimization link")
        if item.get("optimization_boundary") is not None: _date(item["optimization_boundary"], "optimization boundary")
    if "category" in item and item["category"] not in (*CATEGORIES, "unknown"): raise ValueError("invalid inventory category")
    for field in ("first_seen", "last_seen"):
        if field in item: _date(item[field], field)
    if "occurrence_count" in item and (not isinstance(item["occurrence_count"], int) or item["occurrence_count"] < 0): raise ValueError("invalid occurrence count")
    for field in ("affected_tasks", "affected_executions", "history"):
        if field in item and not isinstance(item[field], list): raise ValueError(f"invalid {field}")
    if "metric_totals" in item:
        totals = item["metric_totals"]
        if not isinstance(totals, dict): raise ValueError("invalid metric totals")
        for metric, values in totals.items():
            if metric not in METRICS or not isinstance(values, dict) or set(values) != {"known_total", "known_count", "unknown_count"}: raise ValueError("invalid metric total entry")
            if any(not isinstance(values[k], int) or values[k] < 0 for k in ("known_count", "unknown_count")): raise ValueError("invalid metric coverage")
            total = values["known_total"]
            if total is not None and (not isinstance(total, (int, float)) or isinstance(total, bool) or not math.isfinite(total) or total < 0): raise ValueError("invalid known metric total")
    for row in item.get("history", []):
        if not isinstance(row, dict) or not isinstance(row.get("task"), str) or not isinstance(row.get("attempt"), int): raise ValueError("invalid inventory occurrence history")
        _date(row.get("date"), "history date")
        if "evidence" in row:
            if not isinstance(row["evidence"], list): raise ValueError("invalid history evidence")
            for ref in row["evidence"]: _evidence(ref, "history evidence")
        if row.get("trend") is not None and row["trend"] not in TRENDS: raise ValueError("invalid history trend")
        if "metrics" in row and (not isinstance(row["metrics"], dict) or set(row["metrics"]) - set(METRICS)): raise ValueError("invalid history metrics")
        assessment = row.get("assessment")
        if assessment is not None:
            if not isinstance(assessment, dict) or set(assessment) != {"decision", "rationale", "evidence"} or assessment["decision"] not in DECISIONS: raise ValueError("invalid history assessment")
            _public_text(assessment["rationale"], "history rationale", 1000)
    if "history" in item and "occurrence_count" in item and item["occurrence_count"] != len(item["history"]): raise ValueError("occurrence count does not match history")
    if "first_seen" in item and "last_seen" in item and _date(item["first_seen"], "first_seen") > _date(item["last_seen"], "last_seen"): raise ValueError("invalid inventory chronology")
    for field in ("link_history", "boundary_history", "schema_history"):
        if field in item and not isinstance(item[field], list): raise ValueError(f"invalid {field}")


def migrate_inventory(data):
    """Deterministically add v1 display fields to the existing compact schema."""
    _validate_inventory(data)
    result = json.loads(json.dumps(data))
    used = {item["display_id"] for item in result["items"] if item.get("display_id")}
    next_id = 1
    for item in sorted(result["items"], key=lambda x: x["key"]):
        if "display_id" not in item:
            while f"OPT-{next_id:04d}" in used: next_id += 1
            item["display_id"] = f"OPT-{next_id:04d}"; used.add(item["display_id"]); next_id += 1
        item.setdefault("category", "unknown")
        item.setdefault("summary", "Legacy observation; summary unavailable")
        item.setdefault("status", "unknown")
        item.setdefault("affected_executions", list(item.get("affected_tasks", [])))
        item.setdefault("link_history", [])
        item.setdefault("boundary_history", [])
        item.setdefault("schema_history", [{"event": "legacy-migration", "date": item.get("first_seen"), "source": "legacy-v1", "mapped_fields_unknown": ["category", "summary", "status"]}])
        # Preserve old decisions and occurrence content. Never infer absent GUI decisions.
        for row in item.get("history", []):
            row.setdefault("assessment", None)
        decision = item.get("decision")
        if decision and not any(h.get("assessment") for h in item["history"]):
            item["legacy_decision"] = decision
    _validate_inventory(result)
    return result


def _read_inventory(path):
    _check_path(path)
    if not path.exists(): return _empty_inventory()
    try:
        if not path.is_file() or path.stat().st_size > MAX_INVENTORY_BYTES: raise ValueError("inventory must be a regular file within 4 MiB")
        data = json.loads(path.read_text(encoding="utf-8"))
        _validate_inventory(data)
        return data
    except (json.JSONDecodeError, UnicodeError, OSError) as exc:
        raise ValueError(f"malformed inventory: {exc}") from exc


def _write_atomic(path, data):
    _check_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    _check_path(path)
    _validate_inventory(data)
    encoded = (json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()
    if len(encoded) > MAX_INVENTORY_BYTES: raise ValueError("inventory would exceed 4 MiB")
    fd, tmp = tempfile.mkstemp(prefix=".optimization-inventory-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as f: f.write(encoded); f.flush(); os.fsync(f.fileno())
        _check_path(path)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)


def ingest(path, report, *, task_id, attempt, report_sha256, observations, decision, rationale, evidence, today=None, cycle_id=None):
    """GUI-only triage. Each observation owns its assessment and evidence history."""
    if decision not in DECISIONS: raise ValueError("invalid GUI decision")
    _public_text(rationale, "decision rationale", 1000)
    validate_review(report)
    canonical = json.dumps(report, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    if report_sha256 != hashlib.sha256(canonical).hexdigest(): raise ValueError("report_sha256 does not match canonical report JSON")
    if not re.fullmatch(r"[A-Z][A-Z0-9-]{2,79}", task_id) or not isinstance(attempt, int) or isinstance(attempt, bool) or attempt < 1: raise ValueError("invalid task identity")
    stamp = (today or date.today().isoformat()); stamp_date = _date(stamp, "ingestion date")
    if not isinstance(observations, list) or len(observations) > 50: raise ValueError("observations must be a bounded list")
    if isinstance(evidence, str): evidence = [evidence]
    if not isinstance(evidence, list): raise ValueError("evidence must be a list")
    for ref in evidence: _evidence(ref)
    keys = []
    for obs in observations:
        if not isinstance(obs, dict) or not KEY_RE.fullmatch(str(obs.get("key", ""))): raise ValueError("each observation needs a valid semantic key")
        if obs["key"] in keys: raise ValueError("duplicate semantic key in one report")
        keys.append(obs["key"])
        _public_text(obs.get("text"), "observation text", 1000)
        if obs.get("trend", "NEW") not in TRENDS: raise ValueError("invalid trend")
        obs_evidence = obs.get("evidence", evidence)
        if not isinstance(obs_evidence, list): raise ValueError("observation evidence must be a list")
        for ref in obs_evidence: _evidence(ref)
        metrics = obs.get("metrics", {})
        if not isinstance(metrics, dict) or set(metrics) - set(METRICS): raise ValueError("invalid observation metrics")
        for value in metrics.values():
            if value is not None and (not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value) or value < 0): raise ValueError("observation metrics must be nonnegative numbers or null")
        obs_decision = obs.get("decision", decision)
        if obs_decision not in DECISIONS: raise ValueError("invalid observation decision")
        _public_text(obs.get("rationale", rationale), "observation rationale", 1000)
        if "category" in obs and obs["category"] not in CATEGORIES: raise ValueError("invalid observation category")
        if "summary" in obs: _public_text(obs["summary"], "observation summary", 160)
        if obs.get("linked_optimization_task") is not None:
            link = obs["linked_optimization_task"]
            if not isinstance(link, dict) or set(link) != {"status", "id"} or link["status"] not in {"proposed", "verified"} or not re.fullmatch(r"[A-Z][A-Z0-9-]{2,79}", str(link["id"])): raise ValueError("invalid linked optimization")
        if "optimization_boundary" in obs: _date(obs["optimization_boundary"], "optimization boundary")
        provenance = obs.get("execution_provenance")
        if provenance is not None:
            if not isinstance(provenance, dict) or set(provenance) != {"task_id", "delegation_type", "date", "evidence"} or provenance["delegation_type"] != "EXECUTE" or not re.fullmatch(r"[A-Z][A-Z0-9-]{2,79}", str(provenance["task_id"])):
                raise ValueError("execution provenance must explicitly identify a bounded EXECUTE handoff")
            _date(provenance["date"], "execution provenance date")
            _evidence(provenance["evidence"], "execution provenance evidence")
            if provenance["task_id"] != task_id or provenance["date"] != stamp: raise ValueError("execution provenance must match the current task and occurrence date")
    if cycle_id is not None and (not isinstance(cycle_id, str) or not re.fullmatch(r"[A-Z][A-Z0-9-]{0,63}", cycle_id)):
        raise ValueError("cycle_id must be a stable bounded cycle identifier")
    identity = f"{task_id}:{attempt}" + (f":{cycle_id}" if cycle_id is not None else "")
    semantic = {"report_sha256": report_sha256, "observations": observations, "decision": decision, "rationale": rationale, "evidence": evidence}
    content_sha256 = hashlib.sha256(json.dumps(semantic, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
    ledger_id = hashlib.sha256((identity + content_sha256).encode()).hexdigest()
    data = _read_inventory(path)
    old = next((entry for entry in data["ledger"] if entry["identity"] == identity), None)
    if old:
        if old["content_sha256"] == content_sha256: return data
        raise ValueError("duplicate task attempt has changed report or triage content")
    # Work on a copy: every failure, including late chronology, is byte-atomic.
    data = migrate_inventory(data)
    for obs in observations:
        key = obs["key"]; trend = obs.get("trend", "NEW")
        item = next((x for x in data["items"] if x["key"] == key), None)
        if item and stamp_date < _date(item["last_seen"], "last_seen"): raise ValueError("out-of-order observation chronology")
        if trend in {"IMPROVING", "RESOLVED"}:
            link = item.get("linked_optimization_task") if item else None
            boundary = item.get("optimization_boundary") if item else None
            later = any((p := h.get("execution_provenance")) and p.get("delegation_type") == "EXECUTE" and p.get("task_id") == h.get("task") and p.get("evidence") in h.get("evidence", []) and p.get("date") == h.get("date") and _date(p.get("date"), "execution provenance date") > _date(boundary, "stored optimization boundary") for h in (item or {}).get("history", []) if boundary)
            if not link or link.get("status") != "verified" or not boundary or stamp_date <= _date(boundary, "stored optimization boundary") or not later:
                raise ValueError("effectiveness requires the existing verified link, persisted boundary, and later execution evidence")
            if obs.get("linked_optimization_task") != link: raise ValueError("effectiveness must retain the existing optimization link")
            if obs.get("optimization_boundary", boundary) != boundary: raise ValueError("effectiveness cannot replace the persisted implementation boundary")
        if item is None:
            item = {"key": key, "display_id": f"OPT-{len(data['items']) + 1:04d}", "category": obs.get("category", "scope_process_anomalies"), "summary": obs.get("summary", obs["text"][:160]), "status": "observing", "first_seen": stamp, "last_seen": stamp, "occurrence_count": 0, "affected_tasks": [], "affected_executions": [], "history": [], "metrics": {}, "metric_totals": {}, "trend": trend, "decision": None, "linked_optimization_task": None, "link_history": [], "boundary_history": [], "schema_history": []}
            data["items"].append(item)
        if stamp_date < _date(item["last_seen"], "last_seen"): raise ValueError("out-of-order observation chronology")
        metric_values = {name: obs.get("metrics", {}).get(name) for name in METRICS}
        for name, value in metric_values.items():
            agg = item["metric_totals"].setdefault(name, {"known_total": None, "known_count": 0, "unknown_count": 0})
            if value is None: agg["unknown_count"] += 1
            else: agg["known_total"] = (agg["known_total"] or 0) + value; agg["known_count"] += 1
        obs_decision = obs.get("decision", decision); obs_rationale = obs.get("rationale", rationale); obs_evidence = obs.get("evidence", evidence)
        history = {"task": task_id, "attempt": attempt, "date": stamp, "text": obs["text"], "trend": trend, "metrics": metric_values, "evidence": obs_evidence, "assessment": {"decision": obs_decision, "rationale": obs_rationale, "evidence": obs_evidence}}
        if obs.get("execution_provenance") is not None: history["execution_provenance"] = obs["execution_provenance"]
        item["history"].append(history); item["occurrence_count"] += 1; item["last_seen"] = stamp
        for field in ("affected_tasks", "affected_executions"):
            if task_id not in item[field]: item[field].append(task_id)
        item["decision"] = {"value": obs_decision, "rationale": obs_rationale, "evidence": obs_evidence, "date": stamp}
        item["trend"] = trend; item["status"] = "resolved" if trend == "RESOLVED" else "observing"
        linked = obs.get("linked_optimization_task")
        if linked is not None and linked != item.get("linked_optimization_task"):
            item["linked_optimization_task"] = linked; item["link_history"].append({"date": stamp, "task": task_id, "link": linked, "decision": obs_decision, "rationale": obs_rationale})
        boundary = obs.get("optimization_boundary")
        if boundary and boundary != item.get("optimization_boundary"):
            item["optimization_boundary"] = boundary; item["boundary_history"].append({"date": stamp, "task": task_id, "boundary": boundary, "decision": obs_decision, "rationale": obs_rationale})
    if len(data["ledger"]) >= MAX_LEDGER: raise ValueError("inventory record limit reached")
    data["ledger"].append({"id": ledger_id, "identity": identity, **({"cycle_id": cycle_id} if cycle_id is not None else {}), "report_sha256": report_sha256, "content_sha256": content_sha256, "observation_keys": keys, "date": stamp, "decision": decision, "rationale": rationale, "evidence": evidence})
    _write_atomic(path, data)
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("validate-review"); check.add_argument("result", type=Path)
    triage = sub.add_parser("ingest", help="GUI-only explicit inventory triage")
    triage.add_argument("inventory", type=Path); triage.add_argument("decision_json", type=Path)
    migrate = sub.add_parser("migrate", help="GUI-only deterministic inventory migration")
    migrate.add_argument("inventory", type=Path)
    args = parser.parse_args()
    if args.command == "validate-review":
        _check_path(args.result)
        if not args.result.is_file() or args.result.stat().st_size > 2 * 1024 * 1024: raise ValueError("result must be a regular file no larger than 2 MiB")
        validate_review(extract_review(args.result.read_text(encoding="utf-8"))); print("valid post-execution review")
    elif args.command == "migrate":
        data = _read_inventory(args.inventory); migrated = migrate_inventory(data); _write_atomic(args.inventory, migrated); print("GUI inventory migrated")
    elif args.command == "ingest":
        _check_path(args.decision_json)
        if not args.decision_json.is_file() or args.decision_json.stat().st_size > 1024 * 1024: raise ValueError("triage JSON must be a regular file no larger than 1 MiB")
        try: payload = json.loads(args.decision_json.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeError) as exc: raise ValueError(f"malformed triage JSON: {exc}") from exc
        required = {"report", "task_id", "attempt", "report_sha256", "observations", "decision", "rationale", "evidence"}
        if not isinstance(payload, dict) or set(payload) not in (required, required | {"cycle_id"}): raise ValueError("triage JSON must have exactly the documented fields, with optional cycle_id")
        ingest(args.inventory, payload["report"], task_id=payload["task_id"], attempt=payload["attempt"], report_sha256=payload["report_sha256"], observations=payload["observations"], decision=payload["decision"], rationale=payload["rationale"], evidence=payload["evidence"], cycle_id=payload.get("cycle_id"))
        print("GUI triage ingested")


if __name__ == "__main__": main()
