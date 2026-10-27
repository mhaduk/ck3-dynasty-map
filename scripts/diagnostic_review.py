#!/usr/bin/env python3
"""Build and validate immutable, explicitly sourced diagnostic review packets.

This manual-first helper never contacts a reviewer or changes project state.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path, PurePosixPath

SCHEMA = "diagnostic-review/1"
MANIFEST_LIMIT = 256 * 1024
SOURCE_LIMIT = 1024 * 1024
TOTAL_SOURCE_LIMIT = 4 * 1024 * 1024
INPUT_LIMIT = 64
LINE_LIMIT = 400
EXCERPT_LIMIT = 64 * 1024
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
SENSITIVE = re.compile(r"(?i)(?:\b(?:password|passwd|token|api[_ -]?key|secret|authorization|cookie)\s*[:=]\s*(?:bearer\s+)?\S+|\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b|/(?:Users|home|private|Volumes)/[^/\s]+|[A-Z]:\\Users\\[^\\\s]+)")
REVIEWER_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 _.-]{0,79}$")


class Invalid(ValueError):
    pass


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise Invalid("duplicate_json_key")
        result[key] = value
    return result


def _json(data: bytes):
    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=_pairs,
                          parse_constant=lambda _: (_ for _ in ()).throw(Invalid("non_finite_number")))
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError) as exc:
        raise Invalid("invalid_json") from exc


def _rel(value):
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        raise Invalid("invalid_relative_path")
    p = PurePosixPath(value)
    if p.is_absolute() or any(part in ("", ".", "..") for part in value.split("/")):
        raise Invalid("invalid_relative_path")
    return p


def _root(path: Path) -> Path:
    p = Path(os.fspath(path))
    if not p.is_absolute():
        p = Path.cwd() / p
    if ".." in p.parts:
        raise Invalid("invalid_root")
    cur = Path(p.anchor)
    for part in p.parts[1:]:
        cur /= part
        try:
            if stat.S_ISLNK(cur.lstat().st_mode):
                raise Invalid("symlink_root")
        except FileNotFoundError as exc:
            raise Invalid("invalid_root") from exc
    if not p.is_dir():
        raise Invalid("invalid_root")
    return p.resolve(strict=True)


def _target(root: Path, rel: str, *, must_exist=True) -> Path:
    current = root
    parts = _rel(rel).parts
    for i, part in enumerate(parts):
        current /= part
        try:
            st = current.lstat()
        except FileNotFoundError:
            if must_exist or i < len(parts) - 1:
                raise Invalid("missing_input")
            continue
        if stat.S_ISLNK(st.st_mode):
            raise Invalid("symlink_path")
        if i < len(parts) - 1 and not stat.S_ISDIR(st.st_mode):
            raise Invalid("non_directory_parent")
    if must_exist and not current.is_file():
        raise Invalid("non_regular_input")
    if not must_exist and not current.parent.is_dir():
        raise Invalid("output_parent_missing")
    return current


def _output(root: Path, rel: str, *, preview=False) -> Path:
    parts = _rel(rel).parts
    if len(parts) != 3 or parts[:2] != (".codex-sync", "diagnostics"):
        raise Invalid("output_must_be_private")
    private = root / ".codex-sync"
    if not private.is_dir() or private.is_symlink():
        raise Invalid("private_root_unavailable")
    diagnostics = private / "diagnostics"
    if diagnostics.exists() and (diagnostics.is_symlink() or not diagnostics.is_dir()):
        raise Invalid("unsafe_private_root")
    if preview and not diagnostics.exists():
        return root / rel
    if not preview:
        diagnostics.mkdir(mode=0o700, exist_ok=True)
    return _target(root, rel, must_exist=False)


def _read(path: Path, cap: int) -> bytes:
    before = path.lstat()
    if not stat.S_ISREG(before.st_mode) or before.st_size > cap:
        raise Invalid("input_size_or_type")
    with path.open("rb") as stream:
        opened = os.fstat(stream.fileno())
        if (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino):
            raise Invalid("input_drift")
        data = stream.read(cap + 1)
    after = path.lstat()
    if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns) or len(data) != after.st_size:
        raise Invalid("input_drift")
    if len(data) > cap:
        raise Invalid("input_too_large")
    return data


def _schema(manifest):
    required = {"schema", "review_id", "parent", "timestamp", "cutoff", "repository", "build", "problem", "architecture", "evidence", "experiments", "hypotheses", "contradictions", "constraints", "question", "inputs"}
    if not isinstance(manifest, dict) or set(manifest) != required:
        raise Invalid("manifest_schema")
    if manifest["schema"] != SCHEMA or not isinstance(manifest["review_id"], str) or not ID_RE.fullmatch(manifest["review_id"]):
        raise Invalid("manifest_identity")
    for field in ("parent", "timestamp", "cutoff", "repository", "build", "problem", "architecture", "question"):
        if not isinstance(manifest[field], str) or not manifest[field].strip():
            raise Invalid("missing_" + field)
    if not isinstance(manifest["inputs"], list):
        raise Invalid("invalid_inputs")
    if len(manifest["inputs"]) > INPUT_LIMIT:
        raise Invalid("input_count_limit")
    ids = set()
    for item in manifest["inputs"]:
        if not isinstance(item, dict) or set(item) != {"id", "path", "class", "selector", "required"}:
            raise Invalid("input_schema")
        if not isinstance(item["id"], str) or not ID_RE.fullmatch(item["id"]) or item["id"] in ids:
            raise Invalid("invalid_input_id")
        ids.add(item["id"])
        _rel(item["path"])
        if not isinstance(item["class"], str) or item["class"] not in {"VERIFIED", "OBSERVED", "INFERRED", "UNKNOWN"}:
            raise Invalid("invalid_evidence_class")
        if type(item["required"]) is not bool or not isinstance(item["selector"], dict):
            raise Invalid("invalid_input_selector")
        sel = item["selector"]
        if set(sel) == {"lines"}:
            lines = sel["lines"]
            if not isinstance(lines, list) or not lines or len(lines) > LINE_LIMIT or any(type(n) is not int or n < 1 for n in lines):
                raise Invalid("invalid_line_selector")
            if sorted(set(lines)) != lines:
                raise Invalid("unordered_line_selector")
        elif set(sel) == {"json_fields"}:
            fields = sel["json_fields"]
            if not isinstance(fields, list) or not fields or len(fields) > 128 or any(not isinstance(k, str) or not k for k in fields):
                raise Invalid("invalid_field_selector")
            if len(set(fields)) != len(fields):
                raise Invalid("duplicate_field_selector")
        else:
            raise Invalid("unsupported_selector")
    for field in ("evidence", "experiments", "hypotheses", "contradictions", "constraints"):
        if not isinstance(manifest[field], list) or len(manifest[field]) > 128 or any(not isinstance(x, str) for x in manifest[field]):
            raise Invalid("invalid_" + field)


def _select_json(value, keys):
    out = {}
    for key in keys:
        cur = value
        try:
            for part in key.split("."):
                cur = cur[part] if isinstance(cur, dict) else cur[int(part)]
            out[key] = cur
        except (KeyError, IndexError, ValueError, TypeError):
            out[key] = {"availability": "UNAVAILABLE"}
    return out


def _extract(root: Path, item):
    try:
        path = _target(root, item["path"])
        source = _read(path, SOURCE_LIMIT)
    except Invalid as exc:
        # Only absence is an ordinary optional gap. Unsafe paths, symlinks,
        # malformed files and size/type violations must remain visible.
        if item["required"] or str(exc) != "missing_input":
            raise
        return {"id": item["id"], "path": item["path"], "class": item["class"], "availability": "UNAVAILABLE", "reason": str(exc)}
    selector = item["selector"]
    if "lines" in selector:
        try:
            lines = source.decode("utf-8").splitlines()
        except UnicodeDecodeError as exc:
            raise Invalid("invalid_utf8_input") from exc
        chosen = []
        for number in selector["lines"]:
            if number <= len(lines):
                chosen.append(f"{number}: {lines[number - 1]}")
            else:
                chosen.append(f"{number}: [UNAVAILABLE]")
        extracted = "\n".join(chosen)
    else:
        obj = _json(source)
        extracted = json.dumps(_select_json(obj, selector["json_fields"]), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    data = extracted.encode("utf-8")
    if len(data) > EXCERPT_LIMIT:
        raise Invalid("excerpt_too_large")
    if SENSITIVE.search(extracted):
        raise Invalid("sensitive_excerpt")
    return {"id": item["id"], "path": item["path"], "class": item["class"], "availability": "AVAILABLE", "selector": selector, "source_sha256": digest(source), "extracted_sha256": digest(data), "excerpt": extracted}


def _markdown(manifest, extracted):
    lines = [f"# Diagnostic Review Packet — {manifest['review_id']}", "", "Bounded snapshot from explicitly named inputs; not a complete project history.", "", "## Identity and provenance", "", f"- Parent / issue: {manifest['parent']}", f"- Timestamp / cutoff: {manifest['timestamp']} / {manifest['cutoff']}", f"- Repository revision: {manifest['repository']}", f"- CK3 build: {manifest['build']}", "", "## Problem", "", manifest["problem"], "", "## Architecture and invariants", "", manifest["architecture"], "", "## Evidence ledger", ""]
    for item in manifest["evidence"]:
        lines.append(f"- {item}")
    lines += ["", "## Completed experiments", ""]
    for item in manifest["experiments"]:
        lines.append(f"- {item}")
    lines += ["", "## Hypotheses", ""]
    for item in manifest["hypotheses"]:
        lines.append(f"- {item}")
    lines += ["", "## Contradictions", ""]
    lines.extend(f"- {item}" for item in manifest["contradictions"])
    lines += ["", "## Constraints / non-repeat rules", ""]
    lines.extend(f"- {item}" for item in manifest["constraints"])
    lines += ["", "## Selected source excerpts", ""]
    for item in extracted:
        body = item.get("excerpt", item.get("reason", "Evidence unavailable"))
        fence = "`" * max(3, max((len(m.group(0)) for m in re.finditer(r"`+", body)), default=0) + 1)
        lines += [f"### {item['id']} — {item['class']} / {item['availability']}", "", f"- Source: `{item['path']}`", f"- Selector: `{json.dumps(item.get('selector', {}), sort_keys=True)}`", f"- Source SHA-256: `{item.get('source_sha256', 'UNAVAILABLE')}`", f"- Extracted SHA-256: `{item.get('extracted_sha256', 'UNAVAILABLE')}`", "", fence + "text", body, fence, ""]
    lines += ["## Decision requested", "", manifest["question"], ""]
    return "\n".join(lines).encode("utf-8")


def build(root: Path, manifest_rel: str, output_rel: str, *, preview=False):
    root = _root(root)
    raw = _read(_target(root, manifest_rel), MANIFEST_LIMIT)
    manifest = _json(raw)
    _schema(manifest)
    output = _output(root, output_rel, preview=preview)
    if PurePosixPath(output_rel).name != manifest["review_id"]:
        raise Invalid("output_review_id_mismatch")
    if output.exists():
        raise Invalid("packet_exists")
    extracted, total = [], 0
    for item in sorted(manifest["inputs"], key=lambda x: x["id"]):
        row = _extract(root, item)
        total += len(row.get("excerpt", "").encode("utf-8"))
        if total > TOTAL_SOURCE_LIMIT:
            raise Invalid("total_excerpt_limit")
        extracted.append(row)
    packet = _markdown(manifest, extracted)
    prompt = ("# Independent diagnostic review prompt\n\n"
              "You are a read-only, advisory reviewer. Analyze only the supplied immutable\n"
              "Diagnostic Review Packet. Do not edit files, Issues, game state or task status.\n"
              "Do not request private chain-of-thought. Distinguish supported facts,\n"
              "observations, inferences and speculation. Preserve all `UNKNOWN`, `INCOMPLETE`\n"
              "and upstream status values.\n\n"
              "Challenge assumptions; identify contradictions and missing evidence links;\n"
              "rank remaining hypotheses with support, weakening evidence, confidence and\n"
              "limitations; propose the smallest discriminating next experiment; recommend a\n"
              "fix only when evidence supports it; say what would falsify your recommendation;\n"
              "flag external/current claims with source and provenance. Do not repeat listed\n"
              "completed experiments or non-repeat actions. If evidence is insufficient, say\n"
              "what exact missing observation would decide the question.\n\n"
              "Return concise conclusions under these headings:\n\n"
              "```text\nROOT-CAUSE ASSESSMENT\nASSUMPTIONS TO CHALLENGE\nEVIDENCE / CONTRADICTIONS\n"
              "RANKED HYPOTHESES\nSMALLEST NEXT EXPERIMENT\nRECOMMENDED FIX (only if justified)\n"
              "WHAT WOULD FALSIFY THIS\nUNRESOLVED / UNKNOWN\nEXTERNAL SOURCES / CLAIMS\n```\n\n"
              "Your review is advice, not project evidence or acceptance. The Coordinator\n"
              "validates and owns synthesis.\n").encode()
    identity = json.dumps({"schema": SCHEMA, "review_id": manifest["review_id"], "manifest_sha256": digest(raw), "packet_sha256": digest(packet), "prompt_sha256": digest(prompt), "inputs": extracted}, ensure_ascii=False, sort_keys=True, indent=2).encode() + b"\n"
    if SENSITIVE.search(packet.decode("utf-8")) or SENSITIVE.search(manifest["review_id"]):
        raise Invalid("sensitive_packet_content")
    if not preview:
        output.mkdir(parents=True, mode=0o700)
        (output / "manifest.json").write_bytes(raw)
        (output / "PACKET.md").write_bytes(packet)
        (output / "REVIEW_PROMPT.md").write_bytes(prompt)
        (output / "IDENTITY.json").write_bytes(identity)
    return {"review_id": manifest["review_id"], "packet_sha256": digest(packet), "prompt_sha256": digest(prompt), "inputs": len(extracted), "preview": preview}


def validate(root: Path, output_rel: str):
    root = _root(root)
    parts = _rel(output_rel).parts
    if len(parts) != 3 or parts[:2] != (".codex-sync", "diagnostics"):
        raise Invalid("output_must_be_private")
    folder = _target(root, output_rel + "/IDENTITY.json")
    identity = _json(_read(folder, 1024 * 1024))
    keys = {"schema", "review_id", "manifest_sha256", "packet_sha256", "prompt_sha256", "inputs"}
    if not isinstance(identity, dict) or set(identity) != keys:
        raise Invalid("invalid_identity")
    if (identity["schema"] != SCHEMA or not isinstance(identity["review_id"], str)
            or not ID_RE.fullmatch(identity["review_id"])
            or any(not isinstance(identity[k], str) or not HASH_RE.fullmatch(identity[k])
                   for k in ("manifest_sha256", "packet_sha256", "prompt_sha256"))
            or not isinstance(identity["inputs"], list)):
        raise Invalid("invalid_identity")
    if PurePosixPath(output_rel).name != identity["review_id"]:
        raise Invalid("output_review_id_mismatch")
    manifest_path = _target(root, output_rel + "/manifest.json")
    manifest_raw = _read(manifest_path, MANIFEST_LIMIT)
    manifest = _json(manifest_raw)
    _schema(manifest)
    if manifest["review_id"] != identity["review_id"]:
        raise Invalid("review_id_mismatch")
    for name, key in (("PACKET.md", "packet_sha256"), ("REVIEW_PROMPT.md", "prompt_sha256"), ("manifest.json", "manifest_sha256")):
        data = _read(_target(root, output_rel + "/" + name), 8 * 1024 * 1024)
        if digest(data) != identity[key]:
            raise Invalid("immutable_artifact_hash_mismatch")
    return {"review_id": identity["review_id"], "state": "VALID", "packet_sha256": identity["packet_sha256"]}


def import_review(root: Path, output_rel: str, response_rel: str, reviewer: str):
    root = _root(root)
    if not isinstance(reviewer, str) or not REVIEWER_RE.fullmatch(reviewer) or SENSITIVE.search(reviewer):
        raise Invalid("invalid_reviewer_label")
    valid = validate(root, output_rel)
    response = _read(_target(root, response_rel), EXCERPT_LIMIT)
    try:
        text = response.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise Invalid("response_invalid_utf8") from exc
    if SENSITIVE.search(text):
        raise Invalid("sensitive_response")
    folder = _target(root, output_rel + "/REVIEWERS", must_exist=False)
    if not folder.exists():
        try:
            folder.mkdir(mode=0o700)
        except FileExistsError:
            # Re-resolve an entry created concurrently; a symlink is rejected.
            folder = _target(root, output_rel + "/REVIEWERS", must_exist=False)
    index = 1
    while True:
        candidate = _target(root, output_rel + f"/REVIEWERS/review-{index:02d}.md", must_exist=False)
        try:
            candidate.lstat()
        except FileNotFoundError:
            break
        index += 1
    if index > 8:
        raise Invalid("reviewer_count_limit")
    destination = candidate
    fence = "`" * max(3, max((len(m.group(0)) for m in re.finditer(r"`+", text)), default=0) + 1)
    receipt = f"# Advisory reviewer response {index}\n\n- Reviewer label: {reviewer}\n- Packet SHA-256: {valid['packet_sha256']}\n- Response SHA-256: {digest(response)}\n- Trust: UNTRUSTED ADVISORY TEXT; no project state changed\n\n{fence}text\n{text}\n{fence}\n"
    try:
        fd = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write(receipt)
    except FileExistsError:
        raise Invalid("review_file_exists")
    return {"review_id": valid["review_id"], "review_file": destination.relative_to(root).as_posix(), "packet_sha256": valid["packet_sha256"], "response_sha256": digest(response)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("build", "preview"):
        p = sub.add_parser(name)
        p.add_argument("--root", type=Path, default=Path(".")); p.add_argument("--manifest", required=True); p.add_argument("--output", required=True)
    p = sub.add_parser("validate"); p.add_argument("--root", type=Path, default=Path(".")); p.add_argument("--output", required=True)
    p = sub.add_parser("import-response"); p.add_argument("--root", type=Path, default=Path(".")); p.add_argument("--output", required=True); p.add_argument("--response", required=True); p.add_argument("--reviewer", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command in {"build", "preview"}: result = build(args.root, args.manifest, args.output, preview=args.command == "preview")
        elif args.command == "validate": result = validate(args.root, args.output)
        else: result = import_review(args.root, args.output, args.response, args.reviewer)
        print(json.dumps(result, sort_keys=True))
        return 0
    except (Invalid, OSError) as exc:
        print(f"diagnostic_review: {exc if isinstance(exc, Invalid) else 'io_error'}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
