#!/usr/bin/env python3
"""Build a bounded, deterministic inventory from an explicit evidence manifest."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import stat
import sys
from pathlib import Path, PurePosixPath

MANIFEST_LIMIT = 256 * 1024
ARTIFACT_LIMIT = 64 * 1024 * 1024
TOTAL_LIMIT = 128 * 1024 * 1024
ARTIFACTS_LIMIT = 32
LINKS_LIMIT = 64
BATCHES_LIMIT = 1000
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
HANDOFF_STATUS = {"READY", "IN_PROGRESS", "COMPLETED", "FAILED", "CONSUMED"}
DELTA_FIELDS = {"checkpoint_id": (str,), "baseline_id": (str,),
                "interval_status": (str,), "expectation_status": (str,),
                "observation_status": (str,)}
DELTA_ENUMS = {
    "interval_status": {"INCOMPLETE", "COMPLETE", "COMPLETE_WITH_OPTIONAL_GAPS"},
    "expectation_status": {"UNVERIFIED_INCOMPLETE_EVIDENCE", "MET", "UNMET"},
    "observation_status": {"ERRORS_OR_REJECTIONS_OBSERVED", "NONE_OBSERVED_IN_ANALYZED_LINES"},
}
CLASS_ENUMS = {
    "status": {"INCOMPLETE", "FAIL", "PASS"},
    "capture_completeness": {"INCOMPLETE", "COMPLETE"},
    "availability": {"AVAILABLE", "UNAVAILABLE"},
    "record_completeness": {"COMPLETE", "INCOMPLETE", "UNVERIFIED"},
    "classification_match": {"MATCH", "MISMATCH", "UNVERIFIED"},
    "intended_rgb_mapping": {"MATCH", "MISMATCH", "UNVERIFIED"},
}
LIMITATIONS = [
    "Inventory completeness describes file pins and declared links only; it is not an engine or runtime verdict.",
    "Selected upstream fields are a partial projection, not exhaustive evidence or contract validation.",
    "No storage, RGB, independent census, causality, or user acceptance is established.",
    "Upstream statuses and verdicts remain literal and separate; no aggregate PASS is produced.",
]


class Invalid(ValueError):
    pass


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise Invalid("duplicate_json_key")
        result[key] = value
    return result


def _constant(_):
    raise Invalid("non_finite_json_number")


def _finite_float(value):
    number = float(value)
    if not math.isfinite(number):
        raise Invalid("non_finite_json_number")
    return number


def _depth(value, level=0):
    if level > 64:
        raise Invalid("json_depth_limit")
    if isinstance(value, dict):
        for key, item in value.items():
            _depth(key, level + 1); _depth(item, level + 1)
    elif isinstance(value, list):
        for item in value:
            _depth(item, level + 1)


def _json(data):
    depth = 0
    in_string = escaped = False
    for byte in data:
        if in_string:
            if escaped: escaped = False
            elif byte == 92: escaped = True
            elif byte == 34: in_string = False
        elif byte == 34: in_string = True
        elif byte in (91, 123):
            depth += 1
            if depth > 64: raise Invalid("json_depth_limit")
        elif byte in (93, 125): depth -= 1
    try:
        value = json.loads(data.decode("utf-8"), object_pairs_hook=_pairs, parse_constant=_constant, parse_float=_finite_float)
    except RecursionError as exc:
        raise Invalid("json_depth_limit") from exc
    _depth(value)
    return value


def _path(value):
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        raise Invalid("invalid_relative_path")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in value):
        raise Invalid("invalid_relative_path")
    p = PurePosixPath(value)
    if p.is_absolute() or any(part in ("", ".", "..") for part in value.split("/")):
        raise Invalid("invalid_relative_path")
    return p


def _safe_target(root: Path, rel: str, *, must_exist: bool):
    parts = _path(rel).parts
    current = root
    for i, part in enumerate(parts):
        current = current / part
        try:
            st = current.lstat()
        except FileNotFoundError:
            if must_exist or i < len(parts) - 1:
                return None
            continue
        if stat.S_ISLNK(st.st_mode):
            raise Invalid("symlink_path")
        if i < len(parts) - 1 and not stat.S_ISDIR(st.st_mode):
            raise Invalid("non_directory_parent")
    if not must_exist and not current.parent.is_dir():
        raise Invalid("output_parent_missing")
    if must_exist and current.exists() and not current.is_file():
        raise Invalid("non_regular_file")
    return current


def _checked_root(value: Path):
    supplied = Path(os.fspath(value))
    if not supplied.is_absolute():
        supplied = Path.cwd() / supplied
    if ".." in supplied.parts:
        raise Invalid("invalid_root")
    current = Path(supplied.anchor)
    for part in supplied.parts[1:]:
        current = current / part
        try:
            st = current.lstat()
        except FileNotFoundError:
            raise Invalid("invalid_root")
        if stat.S_ISLNK(st.st_mode):
            raise Invalid("symlink_root")
    if not supplied.is_dir():
        raise Invalid("invalid_root")
    return supplied.resolve(strict=True)


def _read_regular(path: Path, limit: int):
    before = path.lstat()
    if not stat.S_ISREG(before.st_mode) or before.st_size > limit:
        raise Invalid("non_regular_or_oversized_input")
    with path.open("rb") as stream:
        opened = os.fstat(stream.fileno())
        if (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino):
            raise Invalid("input_drift")
        chunks, remaining = [], limit + 1
        while remaining:
            chunk = stream.read(min(1024 * 1024, remaining))
            if not chunk:
                break
            chunks.append(chunk); remaining -= len(chunk)
        data = b"".join(chunks)
    after = path.lstat()
    if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns) or len(data) != after.st_size:
        raise Invalid("input_drift")
    if len(data) > limit:
        raise Invalid("input_too_large")
    return data


def _schema(obj, keys, code):
    if not isinstance(obj, dict) or set(obj) != set(keys):
        raise Invalid(code)


def _positive(value):
    return type(value) is int and 0 < value <= 2**31 - 1


def _artifact_spec(item):
    _schema(item, {"id", "path", "required", "kind", "bytes", "sha256"}, "manifest_artifact_schema")
    if not isinstance(item["id"], str) or not ID_RE.fullmatch(item["id"]): raise Invalid("invalid_artifact_id")
    _path(item["path"])
    if type(item["required"]) is not bool: raise Invalid("invalid_required_flag")
    if not isinstance(item["kind"], str) or item["kind"] not in {"opaque", "handoff-status", "log-delta", "classification"}: raise Invalid("unsupported_kind")
    if type(item["bytes"]) is not int or item["bytes"] < 0: raise Invalid("invalid_expected_bytes")
    if not isinstance(item["sha256"], str) or not HASH_RE.fullmatch(item["sha256"]): raise Invalid("invalid_expected_hash")


def _projection(kind, obj):
    issues = []
    if not isinstance(obj, dict): return {}, ["adapter_schema"]
    if kind == "handoff-status":
        fields = {"id": str, "parent_id": str, "attempt": int, "revision": int, "status": str}
        out = {}
        for key, typ in fields.items():
            v = obj.get(key)
            ok = isinstance(v, typ) and (key not in {"attempt", "revision"} or _positive(v)) and not (typ is int and type(v) is not int)
            if key in {"id", "parent_id"}: ok = ok and ID_RE.fullmatch(v) is not None if isinstance(v, str) else False
            if key == "status": ok = ok and v in HANDOFF_STATUS
            if ok: out[key] = v
            else: issues.append("missing_or_invalid_" + key)
        return out, issues
    if kind == "log-delta":
        out = {}
        if type(obj.get("format")) is not int or obj.get("format") != 1: issues.append("unsupported_format")
        for key, types in DELTA_FIELDS.items():
            value = obj.get(key)
            valid = isinstance(value, types) and (key not in DELTA_ENUMS or value in DELTA_ENUMS[key])
            if key in {"checkpoint_id", "baseline_id"}: valid = valid and ID_RE.fullmatch(value) is not None if isinstance(value, str) else False
            if valid: out[key] = value
            else: issues.append("missing_or_unsupported_" + key)
        return out, issues
    if kind == "classification":
        out = {}
        if type(obj.get("schema")) is not int or obj.get("schema") != 2: issues.append("unsupported_schema")
        for key in ("status", "exit_code", "capture_completeness"):
            value = obj.get(key)
            ok = (key == "exit_code" and type(value) is int and value in (0, 1, 2)) or (key != "exit_code" and isinstance(value, str) and value in CLASS_ENUMS[key])
            if ok: out[key] = value
            else: issues.append("missing_or_unsupported_" + key)
        batches = obj.get("batches")
        selected = []
        if not isinstance(batches, list) or len(batches) > BATCHES_LIMIT:
            issues.append("missing_or_oversized_batches")
        else:
            for batch in batches:
                if not isinstance(batch, dict): issues.append("invalid_batch"); continue
                row = {}
                for key in ("sequence", "availability", "record_completeness", "classification_match", "intended_rgb_mapping"):
                    value = batch.get(key)
                    good = type(value) is int and _positive(value) if key == "sequence" else isinstance(value, str) and value in CLASS_ENUMS[key]
                    if good: row[key] = value
                    else: issues.append("missing_or_unsupported_batch_" + key)
                selected.append(row)
        out["batches"] = selected
        return out, issues
    return {}, []


def build_report(root: Path, manifest_rel: str, output_rel: str):
    root = _checked_root(root)
    manifest_path = _safe_target(root, manifest_rel, must_exist=True)
    if manifest_path is None: raise Invalid("manifest_missing")
    manifest_bytes = _read_regular(manifest_path, MANIFEST_LIMIT)
    manifest = _json(manifest_bytes)
    _schema(manifest, {"schema", "task_id", "artifacts", "links"}, "manifest_schema")
    if manifest["schema"] != "evidence-inventory-input/1": raise Invalid("unsupported_manifest_schema")
    if not isinstance(manifest["task_id"], str) or not ID_RE.fullmatch(manifest["task_id"]): raise Invalid("invalid_task_id")
    artifacts, links = manifest["artifacts"], manifest["links"]
    if not isinstance(artifacts, list) or len(artifacts) > ARTIFACTS_LIMIT: raise Invalid("artifact_count_limit")
    if not isinstance(links, list) or len(links) > LINKS_LIMIT: raise Invalid("link_count_limit")
    seen_ids, seen_paths, total = set(), set(), 0
    for item in artifacts:
        _artifact_spec(item)
        if item["id"] in seen_ids or item["path"] in seen_paths: raise Invalid("duplicate_artifact")
        seen_ids.add(item["id"]); seen_paths.add(item["path"])
        if item["bytes"] > ARTIFACT_LIMIT: raise Invalid("artifact_size_limit")
        total += item["bytes"]
    if total > TOTAL_LIMIT: raise Invalid("total_size_limit")
    link_ids = set()
    for link in links:
        _schema(link, {"id", "from", "to"}, "manifest_link_schema")
        if not isinstance(link["id"], str) or not ID_RE.fullmatch(link["id"]) or link["id"] in link_ids: raise Invalid("invalid_link_id")
        link_ids.add(link["id"])
        for endpoint in (link["from"], link["to"]):
            _schema(endpoint, {"artifact", "field"}, "manifest_endpoint_schema")
            if not isinstance(endpoint["artifact"], str) or endpoint["artifact"] not in seen_ids or not isinstance(endpoint["field"], str) or not ID_RE.fullmatch(endpoint["field"]): raise Invalid("invalid_link_endpoint")
            spec = next(a for a in artifacts if a["id"] == endpoint["artifact"])
            allowed = {"sha256"}
            if spec["kind"] == "handoff-status": allowed |= {"id", "parent_id", "attempt", "revision", "status"}
            elif spec["kind"] == "log-delta": allowed |= set(DELTA_FIELDS)
            elif spec["kind"] == "classification": allowed |= {"status", "exit_code", "capture_completeness"}
            if endpoint["field"] not in allowed: raise Invalid("unsupported_link_field")
    output_path = _safe_target(root, output_rel, must_exist=False)
    if output_path is None or output_path.exists(): raise Invalid("output_collision_or_parent_missing")
    if not (output_path == root / ".codex-sync" / output_path.name or (root / ".codex-sync") in output_path.parents):
        raise Invalid("output_must_be_private_sync_path")
    output_abs = output_path.absolute()
    if output_abs == manifest_path.absolute() or output_rel == manifest_rel: raise Invalid("output_is_input")

    entries, missing, unsupported = [], [], []
    by_id, pinned_values = {}, {}
    attempted_total = 0
    total_limit_failure = False
    for item in artifacts:
        row = {"id": item["id"], "path": item["path"], "kind": item["kind"], "required": item["required"],
               "expected": {"bytes": item["bytes"], "sha256": item["sha256"]}, "observed": None, "pin_state": "UNKNOWN",
               "selected_upstream_fields": {}, "adapter_issues": []}
        by_id[item["id"]] = row
        target = _safe_target(root, item["path"], must_exist=True)
        if target is None:
            row["adapter_issues"] = ["missing_input"]; missing.append({"artifact": item["id"], "code": "required_missing" if item["required"] else "optional_missing"})
            entries.append(row); continue
        try:
            remaining_total = TOTAL_LIMIT - attempted_total
            read_limit = min(ARTIFACT_LIMIT, item["bytes"], max(0, remaining_total - 1))
            # _read_regular may issue one extra byte to detect growth. Reserve the
            # entire attempted ceiling before touching the file; failed reads count too.
            if read_limit < item["bytes"] or read_limit + 1 > remaining_total:
                total_limit_failure = True
                raise Invalid("TOTAL_LIMIT")
            attempted_total += read_limit + 1
            data = _read_regular(target, read_limit)
        except Invalid as exc:
            code = str(exc)
            if code == "total_read_size_limit":
                code = "TOTAL_LIMIT"
                total_limit_failure = True
            if code == "TOTAL_LIMIT": total_limit_failure = True
            row["adapter_issues"] = [code]; unsupported.append({"artifact": item["id"], "code": code}); entries.append(row); continue
        actual_hash, actual_size = hashlib.sha256(data).hexdigest(), len(data)
        row["observed"] = {"bytes": actual_size, "sha256": actual_hash}
        good = actual_size == item["bytes"] and actual_hash == item["sha256"]
        row["pin_state"] = "MATCH" if good else "MISMATCH"
        pinned_values[item["id"]] = actual_hash
        if not good:
            row["adapter_issues"] = ["PIN_MISMATCH"]
        elif item["kind"] != "opaque":
            try:
                obj = _json(data)
                projection, issues = _projection(item["kind"], obj)
                row["selected_upstream_fields"] = projection
                row["adapter_issues"] = issues
                if issues: unsupported.extend({"artifact": item["id"], "code": code} for code in issues)
            except (Invalid, UnicodeDecodeError, json.JSONDecodeError):
                row["adapter_issues"] = ["malformed_or_unsupported_json"]
                unsupported.append({"artifact": item["id"], "code": "malformed_or_unsupported_json"})
        entries.append(row)

    links_out = []
    failed_link = False
    for link in links:
        vals, trusted = [], True
        for ep in (link["from"], link["to"]):
            row = by_id[ep["artifact"]]
            if row["pin_state"] != "MATCH" or row["adapter_issues"]: trusted = False; vals.append(None); continue
            if ep["field"] == "sha256": vals.append(row["observed"]["sha256"]); continue
            fields = row["selected_upstream_fields"]
            if ep["field"] == "status" and row["kind"] == "handoff-status": value = fields.get("status")
            else: value = fields.get(ep["field"])
            if value is None: trusted = False
            vals.append(value)
        if not trusted: state = "UNKNOWN"
        else: state = "MATCH" if type(vals[0]) is type(vals[1]) and vals[0] == vals[1] else "MISMATCH"
        failed_link |= state == "MISMATCH"
        links_out.append({"id": link["id"], "from": link["from"], "to": link["to"], "state": state})
    required_bad = any((not row["observed"] and row["required"]) or row["pin_state"] == "MISMATCH" or row["adapter_issues"] for row in entries if row["required"])
    fatal_codes = {"input_drift", "input_too_large", "non_regular_or_oversized_input", "malformed_or_unsupported_json", "TOTAL_LIMIT"}
    any_bad = any(row["pin_state"] == "MISMATCH" or fatal_codes.intersection(row["adapter_issues"]) for row in entries)
    unknown_link = any(link["state"] == "UNKNOWN" for link in links_out)
    optional_gaps = any(not row["observed"] or row["adapter_issues"] for row in entries if not row["required"])
    if required_bad or any_bad or failed_link or unknown_link or total_limit_failure: completeness = "INCOMPLETE"
    elif optional_gaps: completeness = "COMPLETE_WITH_OPTIONAL_GAPS"
    else: completeness = "COMPLETE"
    review = [{"artifact": row["id"], "code": code} for row in entries for code in row["adapter_issues"]]
    review.extend({"link": link["id"], "code": link["state"]} for link in links_out if link["state"] != "MATCH")
    report = {"schema": "evidence-inventory-report/1", "task_id": manifest["task_id"], "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
              "scope": "Explicit pinned file inventory and caller-declared equality links.", "limitations": LIMITATIONS,
              "inventory_completeness": completeness, "artifacts": entries, "links": links_out, "missing": missing,
              "unsupported": unsupported, "review_needed": review}
    return output_path, (json.dumps(report, sort_keys=True, ensure_ascii=True, indent=2) + "\n").encode("utf-8"), completeness


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    try:
        out, data, completeness = build_report(Path(args.root), args.manifest, args.output)
        fd = os.open(out, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(data); stream.flush(); os.fsync(stream.fileno())
        except Exception:
            try: out.unlink()
            except OSError: pass
            raise
        print(completeness)
        return 2 if completeness == "INCOMPLETE" else 0
    except (Invalid, OSError, UnicodeDecodeError, json.JSONDecodeError):
        print("evidence_report: invalid input or output operation", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
