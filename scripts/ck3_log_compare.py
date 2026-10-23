#!/usr/bin/env python3
"""Compare two explicitly pinned format-1 CK3 log-delta metadata manifests.

This tool compares declared metadata only. It never opens captured log bytes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys

import evidence_report as safe

ENVELOPE_LIMIT = 64 * 1024
SOURCE_LIMIT = 1024 * 1024
LOGS_LIMIT = 16
FINGERPRINT_LIMIT = 250
COLLECTION_ITEMS_LIMIT = 1024
COUNT_MAX = 2**63 - 1
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
LOG_NAMES = {"debug.log", "error.log", "game.log", "gui_warnings.log", "database_conflicts.log"}
STATES = {"CAPTURED", "PARTIAL_READ", "CAPPED", "CHANGED_DURING_READ", "READ_ERROR", "MISSING", "REPLACED", "TRUNCATED", "BOUNDARY_CHANGED", "INVALID_BASELINE", "UNCERTAIN_DURING_BASELINE", "READY"}
INTERVALS = {"INCOMPLETE", "COMPLETE", "COMPLETE_WITH_OPTIONAL_GAPS"}
EXPECTATIONS = {"UNVERIFIED_INCOMPLETE_EVIDENCE", "MET", "UNMET"}
OBSERVATIONS = {"ERRORS_OR_REJECTIONS_OBSERVED", "NONE_OBSERVED_IN_ANALYZED_LINES"}
LIMITS = [
    "Metadata comparison only; no generation or byte continuity is established.",
    "Declared ranges and digest fields are report metadata, not independently anchored source bytes.",
    "Capture gaps cannot be repaired by combining inputs; normalized content fingerprints are not events.",
    "Sampled boundaries cannot exclude arbitrary same-size rewrites; per-log captures are not atomic.",
    "Path, size and hash checks detect ordinary drift; hostile concurrent replacement is not ruled out.",
    "No engine, storage, RGB, independent census, user acceptance, or clean-run verdict is established.",
    "Global retained fingerprints are private summaries and are not attributed to individual logs.",
]


def exact_int(value, minimum=0):
    return type(value) is int and minimum <= value <= COUNT_MAX


def pin_spec(item):
    if not isinstance(item, dict) or set(item) != {"path", "bytes", "sha256"}:
        raise safe.Invalid("invalid_pin_schema")
    safe._path(item["path"])
    if not exact_int(item["bytes"]) or item["bytes"] > SOURCE_LIMIT:
        raise safe.Invalid("invalid_expected_bytes")
    if not isinstance(item["sha256"], str) or not HASH_RE.fullmatch(item["sha256"]):
        raise safe.Invalid("invalid_expected_hash")


def _count(value, *, positive=False):
    return exact_int(value, 1 if positive else 0)


def collections_bounded(value):
    pending = [value]
    while pending:
        current = pending.pop()
        if isinstance(current, dict):
            if len(current) > COLLECTION_ITEMS_LIMIT:
                raise safe.Invalid("collection_size_limit")
            pending.extend(current.keys()); pending.extend(current.values())
        elif isinstance(current, list):
            if len(current) > COLLECTION_ITEMS_LIMIT:
                raise safe.Invalid("collection_size_limit")
            pending.extend(current)


def _summary_projection(obj, role, issues):
    result = {"role": role, "pin_status": "VERIFIED", "upstream": {}, "logs": {}, "fingerprints": None,
              "summary_coverage": "UNKNOWN"}
    if not isinstance(obj, dict) or type(obj.get("format")) is not int or obj.get("format") != 1:
        issues.append("unsupported_source_format")
        return result
    enums = {"checkpoint_id": safe.ID_RE, "baseline_id": safe.ID_RE,
             "interval_status": INTERVALS, "expectation_status": EXPECTATIONS,
             "observation_status": OBSERVATIONS}
    for key, allowed in enums.items():
        value = obj.get(key)
        valid = bool(allowed.fullmatch(value)) if key.endswith("_id") and isinstance(value, str) else value in allowed if isinstance(value, str) else False
        if valid:
            result["upstream"][key] = value
        else:
            issues.append("invalid_upstream_" + key)
    coverage_unknown = any(key not in result["upstream"] for key in
                           ("interval_status", "expectation_status", "observation_status"))
    logs = obj.get("logs")
    if not isinstance(logs, dict) or len(logs) > LOGS_LIMIT:
        issues.append("invalid_logs_collection")
        logs = {}
        coverage_unknown = True
    observed_gap = (result["upstream"].get("interval_status") != "COMPLETE"
                    or result["upstream"].get("expectation_status") == "UNVERIFIED_INCOMPLETE_EVIDENCE")
    observed_fragment = False
    for name, row in logs.items():
        if name not in LOG_NAMES:
            issues.append("unsupported_log_name")
            coverage_unknown = True
            continue
        if not isinstance(row, dict):
            issues.append("invalid_log_row")
            coverage_unknown = True
            continue
        state = row.get("state")
        required = row.get("required")
        if not isinstance(state, str) or state not in STATES:
            issues.append("invalid_log_state")
            state = None
            coverage_unknown = True
        if type(required) is not bool:
            issues.append("missing_or_invalid_required")
            required = None
            coverage_unknown = True
        item = {"state": state, "required": required}
        for key in ("incomplete", "partial_initial_line", "partial_final_line"):
            value = row.get(key, False)
            if type(value) is not bool:
                issues.append("invalid_" + key)
                value = None
                coverage_unknown = True
            item[key] = value
            observed_fragment |= value is True
        observed_gap |= state != "CAPTURED" or item["incomplete"] is True
        count = row.get("captured_bytes")
        if not _count(count):
            issues.append("missing_or_invalid_captured_bytes")
            count = None
            coverage_unknown = True
        item["captured_bytes"] = count
        if state == "CAPTURED":
            fields = ("start_offset", "end_offset", "source_size_at_boundary", "sha256")
            values = {key: row.get(key) for key in fields}
            valid = all(_count(values[k]) for k in fields[:3]) and isinstance(values["sha256"], str) and HASH_RE.fullmatch(values["sha256"])
            valid = valid and values["start_offset"] <= values["end_offset"] <= values["source_size_at_boundary"]
            valid = valid and values["end_offset"] - values["start_offset"] == count
            if valid:
                clean_flags_known = all(item[key] is False for key in
                                        ("incomplete", "partial_initial_line", "partial_final_line"))
                item.update(start_offset=values["start_offset"], end_offset=values["end_offset"],
                            source_size_at_boundary=values["source_size_at_boundary"], sha256=values["sha256"],
                            range_valid=(clean_flags_known and item["incomplete"] is False
                                         and item["partial_initial_line"] is False
                                         and item["partial_final_line"] is False))
            else:
                issues.append("invalid_captured_range")
                item["range_valid"] = False
                observed_gap = True
                coverage_unknown = True
            if item["range_valid"] is False:
                observed_gap = True
        else:
            item["range_valid"] = False
        analysis_root = obj.get("analysis")
        per_log = analysis_root.get("per_log") if isinstance(analysis_root, dict) else None
        if not isinstance(per_log, dict):
            issues.append("invalid_per_log_collection")
            coverage_unknown = True
            item["range_valid"] = False
            per_log = {}
        analysis = per_log.get(name)
        if analysis is not None:
            if not isinstance(analysis, dict):
                issues.append("invalid_per_log_analysis")
                coverage_unknown = True
                item["range_valid"] = False
            else:
                n = analysis.get("error_lines")
                if _count(n): item["error_lines"] = n
                else:
                    issues.append("invalid_error_lines")
                    coverage_unknown = True
                for key in ("partial_initial_line", "partial_final_line"):
                    value = analysis.get(key)
                    if type(value) is not bool:
                        issues.append("invalid_analysis_" + key)
                        coverage_unknown = True
                        item["range_valid"] = False
                    else:
                        item["analysis_" + key] = value
                        observed_fragment |= value
                        if value:
                            item["range_valid"] = False
                            observed_gap = True
        elif state == "CAPTURED":
            issues.append("missing_per_log_analysis")
            coverage_unknown = True
            item["range_valid"] = False
        result["logs"][name] = item
    analysis = obj.get("analysis")
    if not isinstance(analysis, dict):
        issues.append("invalid_analysis")
        coverage_unknown = True
    else:
        for key in ("new_error_lines", "omitted_error_lines_after_summary_cap"):
            if _count(analysis.get(key)): result["upstream"][key] = analysis[key]
            else:
                issues.append("invalid_" + key)
                coverage_unknown = True
        fingerprints = analysis.get("unique_new_errors")
        if not isinstance(fingerprints, list) or len(fingerprints) > FINGERPRINT_LIMIT:
            issues.append("invalid_fingerprint_list")
        else:
            parsed, seen, total = [], set(), 0
            valid_set = True
            for entry in fingerprints:
                if not isinstance(entry, dict):
                    issues.append("invalid_fingerprint_row"); valid_set = False; continue
                digest, count = entry.get("message_sha256"), entry.get("occurrences")
                if not isinstance(digest, str) or not HASH_RE.fullmatch(digest) or not _count(count, positive=True):
                    issues.append("invalid_fingerprint_fields"); valid_set = False; continue
                if digest in seen:
                    issues.append("duplicate_fingerprint"); valid_set = False; continue
                seen.add(digest); total += count; parsed.append({"message_sha256": digest, "occurrences": count})
            omitted = result["upstream"].get("omitted_error_lines_after_summary_cap")
            new_lines = result["upstream"].get("new_error_lines")
            if total > COUNT_MAX or omitted is None or new_lines is None or total + omitted != new_lines:
                issues.append("inconsistent_fingerprint_summary")
                valid_set = False
            if valid_set:
                result["fingerprints"] = parsed
                if omitted > 0:
                    observed_gap = True
            else:
                result["summary_coverage"] = "UNKNOWN"
    result["summary_coverage"] = ("UNKNOWN" if coverage_unknown else
                                  "PARTIAL" if observed_gap or observed_fragment or result["upstream"].get("omitted_error_lines_after_summary_cap", 0) else "COMPLETE")
    if result["fingerprints"] is None:
        result["summary_coverage"] = "UNKNOWN"
    for item in result["logs"].values():
        item["error_lines_scope"] = "per-log analyzed lines"
        item["error_lines_coverage"] = "REPORTED" if "error_lines" in item else "UNKNOWN"
    result["global_summary"] = {
        "error_lines": result["upstream"].get("new_error_lines"),
        "omitted_error_lines_after_summary_cap": result["upstream"].get("omitted_error_lines_after_summary_cap"),
        "scope": "global analyzed lines across captured logs",
        "coverage": result["summary_coverage"],
    }
    return result


def relation(a, b):
    if a["start_offset"] == b["start_offset"] and a["end_offset"] == b["end_offset"]:
        return "IDENTICAL"
    if a["end_offset"] == b["start_offset"] or b["end_offset"] == a["start_offset"]:
        return "ADJACENT"
    if a["end_offset"] < b["start_offset"] or b["end_offset"] < a["start_offset"]:
        return "DISJOINT"
    if a["start_offset"] <= b["start_offset"] and a["end_offset"] >= b["end_offset"]:
        return "LEFT_CONTAINS"
    if b["start_offset"] <= a["start_offset"] and b["end_offset"] >= a["end_offset"]:
        return "RIGHT_CONTAINS"
    return "OVERLAP"


def compare_side(left, right, issues):
    logs = {}
    for name in sorted(set(left["logs"]) | set(right["logs"])):
        a, b = left["logs"].get(name), right["logs"].get(name)
        pair = {"left": a, "right": b, "declared_range_relation": "UNKNOWN", "declared_digest_equality": "UNKNOWN",
                "reported_count_relation": "UNKNOWN", "count_delta": None, "new_error_count": None}
        if a and b and a.get("range_valid") and b.get("range_valid"):
            pair["declared_range_relation"] = relation(a, b)
            pair["declared_digest_equality"] = "EQUAL" if a["sha256"] == b["sha256"] else "DIFFERENT"
        if a and b and _count(a.get("error_lines")) and _count(b.get("error_lines")):
            pair["reported_count_relation"] = "EQUAL" if a["error_lines"] == b["error_lines"] else "DIFFERENT"
        logs[name] = pair
    fingerprints = None
    if left["fingerprints"] is not None and right["fingerprints"] is not None:
        lm = {x["message_sha256"]: x["occurrences"] for x in left["fingerprints"]}
        rm = {x["message_sha256"]: x["occurrences"] for x in right["fingerprints"]}
        fingerprints = [{"message_sha256": key, "membership": "BOTH" if key in lm and key in rm else "LEFT_ONLY" if key in lm else "RIGHT_ONLY",
                         "left_occurrences": lm.get(key), "right_occurrences": rm.get(key)} for key in sorted(lm.keys() | rm.keys())]
    else:
        issues.append("fingerprint_overlap_unknown")
    left_global = left["upstream"].get("new_error_lines")
    right_global = right["upstream"].get("new_error_lines")
    global_relation = "UNKNOWN"
    if _count(left_global) and _count(right_global):
        global_relation = "EQUAL" if left_global == right_global else "DIFFERENT"
    return {"logs": logs, "retained_fingerprint_comparison": fingerprints,
            "global_reported_count_relation": global_relation,
            "generation_relation": "UNKNOWN", "byte_continuity": "UNKNOWN", "new_bytes": None,
            "count_delta": None, "new_error_count": None, "event_identity": "UNPROVEN", "causality": "UNPROVEN"}


def load_pinned(root, role, spec, issues):
    item = {"role": role, "expected_bytes": spec["bytes"], "expected_sha256": spec["sha256"],
            "observed_bytes": None, "observed_sha256": None, "pin_status": "UNKNOWN"}
    try:
        path = safe._safe_target(root, spec["path"], must_exist=True)
        if path is None:
            raise safe.Invalid("missing_source")
        data = safe._read_regular(path, SOURCE_LIMIT)
        item["observed_bytes"] = len(data); item["observed_sha256"] = hashlib.sha256(data).hexdigest()
        if len(data) != spec["bytes"] or item["observed_sha256"] != spec["sha256"]:
            item["pin_status"] = "MISMATCH"; issues.append("source_pin_mismatch")
            return item, None
        item["pin_status"] = "VERIFIED"
        try:
            parsed = safe._json(data)
            collections_bounded(parsed)
            return item, parsed
        except (ValueError, UnicodeError, OverflowError, RecursionError):
            issues.append("invalid_source_json")
            return item, None
    except (safe.Invalid, OSError):
        issues.append("source_read_or_path_failure")
        return item, None


def build(root, envelope, output):
    safe._schema(envelope, {"schema", "left", "right"}, "invalid_envelope_schema")
    if envelope["schema"] != "checkpoint-comparison-input/1": raise safe.Invalid("unsupported_envelope_schema")
    pin_spec(envelope["left"]); pin_spec(envelope["right"])
    if envelope["left"]["path"] == output or envelope["right"]["path"] == output: raise safe.Invalid("input_output_alias")
    issues = []
    pins, sides = {}, {}
    for role in ("left", "right"):
        pins[role], obj = load_pinned(root, role, envelope[role], issues)
        if obj is None:
            sides[role] = {"role": role, "pin_status": pins[role]["pin_status"], "upstream": {}, "logs": {}, "fingerprints": None, "summary_coverage": "UNKNOWN"}
            continue
        sides[role] = _summary_projection(obj, role, issues)
    for role in sides:
        sides[role]["pin_status"] = pins[role]["pin_status"]
    issues = sorted(set(issues))
    comparison_issues = []
    comparison = compare_side(sides["left"], sides["right"], comparison_issues)
    issues = sorted(set(issues + comparison_issues))
    structural = bool(issues) or any(p["pin_status"] != "VERIFIED" for p in pins.values())
    # A missing/invalid summary is an unavailable comparison, not an empty set.
    comparison["retained_fingerprint_comparison"] = comparison["retained_fingerprint_comparison"] if not any(s["fingerprints"] is None for s in sides.values()) else None
    report = {"schema": "checkpoint-comparison-result/1", "metadata_status": "INCOMPLETE" if structural else "COMPLETE",
              "pins": pins, "sources": sides, "comparison": comparison, "issues": issues, "limits": LIMITS}
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    created = None
    try:
        root = safe._checked_root(Path(args.root))
        manifest_path = safe._safe_target(root, args.manifest, must_exist=True)
        if manifest_path is None:
            raise safe.Invalid("missing_envelope")
        manifest_data = safe._read_regular(manifest_path, ENVELOPE_LIMIT)
        envelope = safe._json(manifest_data)
        output_rel = args.output
        if not output_rel.startswith(".codex-sync/"):
            raise safe.Invalid("output_outside_private_directory")
        out = safe._safe_target(root, output_rel, must_exist=False)
        if out is None or out.exists(): raise safe.Invalid("output_collision_or_missing_parent")
        if args.manifest == output_rel: raise safe.Invalid("input_output_alias")
        report = build(root, envelope, output_rel)
        payload = (json.dumps(report, ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n").encode()
        fd = os.open(out, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o600)
        created = out
        with os.fdopen(fd, "wb") as stream:
            stream.write(payload); stream.flush(); os.fsync(stream.fileno())
        os.chmod(out, 0o600)
        print("comparison report written")
        return 0 if report["metadata_status"] == "COMPLETE" else 2
    except (safe.Invalid, OSError, ValueError, TypeError, RecursionError):
        if created is not None:
            try: created.unlink()
            except OSError: pass
        print("comparison input or output failure", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
