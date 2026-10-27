#!/usr/bin/env python3
"""Read-only payload checks. Does not parse CK3 scripts or validate runtime APIs."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

BOM = b"\xef\xbb\xbf"
# Public, finite categories. The messages remain private to the legacy renderer.
MESSAGES = {
    "invalid_root": "payload root must be an existing ordinary directory",
    "misplaced_coa": "misplaced CoA folder; use common/coat_of_arms/coat_of_arms",
    "symlink": "symlinks are not supported in a reviewed payload",
    "incidental_file": "research/evidence or incidental file does not belong in payload",
    "read_error": "cannot read file",
    "missing_bom": "requires exactly one leading UTF-8 BOM (project convention)",
    "duplicate_bom": "duplicate leading UTF-8 BOM",
    "invalid_utf8": "invalid UTF-8",
    "bad_loc_header": "first substantive line must be l_<language>:",
    "loc_folder_mismatch": "localization folder and header language differ",
    "loc_filename_mismatch": "filename must end in _l_<language>.yml",
    "missing_descriptor": "required file missing",
    "descriptor_unavailable": "required file missing",
    "descriptor_declaration": "requires one quoted declaration",
    "version_mismatch": "supported_version must equal expected version",
    "inventory_missing": "missing from installed inventory",
    "inventory_extra": "extra installed file",
    "bytes_mismatch": "bytes/SHA-256 differ from source",
    "traversal_error": "filesystem traversal failed",
}
LIMITS = ["Offline file checks only; CK3 syntax, references/API, runtime/load/save, RGB and user acceptance remain unverified."]


class Findings:
    def __init__(self):
        self.rows = []  # (scope, code, message, legacy order)

    def add(self, scope, code, message=None):
        self.rows.append((scope, code, message or MESSAGES.get(code, "inspection failed")))


def _walk(root, scope, findings):
    """Sorted recursive walk while retaining traversal errors as incomplete evidence."""
    if not root.is_dir() or root.is_symlink():
        findings.add(scope, "invalid_root")
        return [], False
    entries, complete = [], True
    if (root / "coat_of_arms").exists():
        findings.add(scope, "misplaced_coa", f"coat_of_arms: {MESSAGES['misplaced_coa']}")

    def onerror(_error):
        nonlocal complete
        complete = False
        findings.add(scope, "traversal_error")

    import os
    try:
        for base, dirs, names in os.walk(root, topdown=True, onerror=onerror, followlinks=False):
            base_path = Path(base)
            dirs.sort(); names.sort()
            for dirname in list(dirs):
                p = base_path / dirname
                entries.append(p)
                if p.is_symlink():
                    dirs.remove(dirname)
            for filename in names:
                entries.append(base_path / filename)
    except OSError:
        complete = False
        findings.add(scope, "traversal_error")
    return sorted(entries, key=lambda path: path.relative_to(root).as_posix()), complete


def _inspect(root, scope, expected_version, findings):
    inventory = {}
    files, complete = _walk(root, scope, findings)
    for path in files:
        relative = path.relative_to(root)
        name = relative.as_posix()
        if path.is_symlink():
            complete = False
            findings.add(scope, "symlink", f"{name}: {MESSAGES['symlink']}")
            continue
        if not path.is_file():
            continue
        parts = [part.lower() for part in relative.parts]
        if (any(part in {"evidence", "alternatives", "logs", "saves", "__pycache__"} for part in parts)
                or path.name.lower().startswith("readme") or path.name in {".DS_Store", ".gitignore"}
                or path.suffix.lower() in {".log", ".ck3", ".pyc"}):
            findings.add(scope, "incidental_file", f"{name}: {MESSAGES['incidental_file']}")
        try:
            data = path.read_bytes()
        except OSError:
            complete = False
            findings.add(scope, "read_error", f"{name}: {MESSAGES['read_error']}")
            continue
        inventory[name] = data
        script = parts[0] in {"common", "gfx"} and path.suffix.lower() == ".txt"
        localization = parts[0] == "localization" and path.suffix.lower() == ".yml"
        utf8 = script or localization or path.suffix.lower() in {".gui", ".mod"}
        if not utf8:
            continue
        if (script or localization) and not data.startswith(BOM):
            findings.add(scope, "missing_bom", f"{name}: {MESSAGES['missing_bom']}")
        if data.startswith(BOM + BOM):
            findings.add(scope, "duplicate_bom", f"{name}: {MESSAGES['duplicate_bom']}")
        try:
            content = data.decode("utf-8-sig", errors="strict")
        except UnicodeDecodeError:
            findings.add(scope, "invalid_utf8", f"{name}: {MESSAGES['invalid_utf8']}")
            continue
        if localization:
            lines = [line.strip() for line in content.splitlines() if line.strip() and not line.lstrip().startswith("#")]
            header = re.fullmatch(r"l_([a-z_]+):(?:\s*#.*)?", lines[0]) if lines else None
            if not header:
                findings.add(scope, "bad_loc_header", f"{name}: {MESSAGES['bad_loc_header']}")
            else:
                language = header.group(1)
                if len(parts) < 3 or relative.parts[1] != language:
                    findings.add(scope, "loc_folder_mismatch", f"{name}: {MESSAGES['loc_folder_mismatch']}")
                if not path.name.endswith(f"_l_{language}.yml"):
                    findings.add(scope, "loc_filename_mismatch", f"{name}: {MESSAGES['loc_filename_mismatch']}")

    descriptor = inventory.get("descriptor.mod")
    if descriptor is None:
        if complete:
            findings.add(scope, "missing_descriptor", f"descriptor.mod: {MESSAGES['missing_descriptor']}")
        elif not any(row[0] == scope and row[1] == "invalid_root" for row in findings.rows):
            findings.add(scope, "descriptor_unavailable", f"descriptor.mod: {MESSAGES['missing_descriptor']}")
    else:
        try:
            content = descriptor.decode("utf-8-sig", errors="strict")
        except UnicodeDecodeError:
            content = ""  # Already reported above.
        for field in ("name", "version", "supported_version"):
            values = re.findall(r'^\s*' + field + r'\s*=\s*"([^"\n]+)"\s*(?:#.*)?$', content, flags=re.MULTILINE)
            if len(values) != 1:
                findings.add(scope, "descriptor_declaration", f"descriptor.mod: requires one quoted {field} declaration")
            elif field == "supported_version" and expected_version is not None and values[0] != expected_version:
                findings.add(scope, "version_mismatch", f"descriptor.mod: supported_version must equal {expected_version}")
    return inventory, complete


def inspect(root, label, expected_version, errors):
    """Compatibility wrapper retained for callers of the historical helper."""
    findings = Findings()
    inventory, _ = _inspect(Path(root), label, expected_version, findings)
    for _, code, detail in findings.rows:
        if ": " in detail:
            path, message = detail.split(": ", 1)
        else:
            path = {"invalid_root": ".", "traversal_error": ".", "misplaced_coa": "coat_of_arms",
                    "missing_descriptor": "descriptor.mod"}.get(code, "descriptor.mod")
            message = detail
        errors.append(f"{label}/{path}: {message}")
    return inventory


def _version_check(inventory, requested, expected):
    if not requested:
        return "NOT_REQUESTED"
    if expected is None:
        return "NOT_REQUESTED"
    descriptor = inventory.get("descriptor.mod")
    if descriptor is None:
        return "UNVERIFIED"
    try:
        content = descriptor.decode("utf-8-sig")
    except UnicodeDecodeError:
        return "UNVERIFIED"
    values = re.findall(r'^\s*supported_version\s*=\s*"([^"\n]+)"\s*(?:#.*)?$', content, flags=re.MULTILINE)
    if len(values) != 1:
        return "UNVERIFIED"
    return "MATCH" if values[0] == expected else "MISMATCH"


def _result(source, installed, findings, source_complete, installed_complete, args):
    rows = list(findings.rows)
    comparison_requested = installed is not None
    if comparison_requested:
        for name in sorted(source.keys() - installed.keys()):
            findings.add("comparison", "inventory_missing", f"installed/{name}: {MESSAGES['inventory_missing']}")
        for name in sorted(installed.keys() - source.keys()):
            findings.add("comparison", "inventory_extra", f"installed/{name}: {MESSAGES['inventory_extra']}")
        for name in sorted(source.keys() & installed.keys()):
            if source[name] != installed[name] or hashlib.sha256(source[name]).digest() != hashlib.sha256(installed[name]).digest():
                findings.add("comparison", "bytes_mismatch", f"installed/{name}: {MESSAGES['bytes_mismatch']}")
    rows = findings.rows
    if not source_complete or (comparison_requested and not installed_complete): status = "INCOMPLETE"
    elif rows: status = "FAIL"
    else: status = "PASS"
    if not comparison_requested: comparison = "NOT_REQUESTED"
    elif not source_complete or not installed_complete: comparison = "UNVERIFIED"
    elif any(row[0] == "comparison" for row in rows): comparison = "MISMATCH"
    else: comparison = "MATCH"
    code_order = {code: i for i, code in enumerate(MESSAGES)}
    counts = {}
    for scope, code, _ in rows:
        counts[(scope, code)] = counts.get((scope, code), 0) + 1
    enum = [{"scope": scope, "code": code, "count": count} for (scope, code), count in sorted(counts.items(), key=lambda x: (x[0][0], code_order.get(x[0][1], 999), x[0][1]))]
    installed_requested = comparison_requested
    return {
        "schema": "mod-preflight-result/1", "status": status, "exit_code": 0 if status == "PASS" else 1,
        "source_coverage": "COMPLETE" if source_complete else "INCOMPLETE", "source_files": len(source),
        "source_version_check": _version_check(source, True, args.expected_version),
        "installed_requested": installed_requested,
        "installed_coverage": ("NOT_REQUESTED" if not installed_requested else "COMPLETE" if installed_complete else "INCOMPLETE"),
        "installed_files": None if not installed_requested else len(installed),
        "installed_version_check": _version_check(installed or {}, installed_requested, args.expected_version),
        "comparison": comparison,
        "findings": enum,
        "limits": LIMITS,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("payload", type=Path, help="explicit source mod payload root")
    parser.add_argument("--installed", type=Path, help="compare exact installed inventory and bytes")
    parser.add_argument("--expected-version", help="exact supported_version declaration")
    parser.add_argument("--json", action="store_true", help="emit bounded structured evidence JSON")
    args = parser.parse_args(argv)
    findings = Findings()
    source, source_complete = _inspect(args.payload, "source", args.expected_version, findings)
    installed, installed_complete = (None, True)
    if args.installed is not None:
        installed, installed_complete = _inspect(args.installed, "installed", args.expected_version, findings)
    result = _result(source, installed, findings, source_complete, installed_complete, args)
    if args.json:
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    else:
        # Legacy output remains ordered and byte-compatible for ordinary findings.
        for scope, code, message in findings.rows:
            prefix = "" if scope == "comparison" else ("installed/" if scope == "installed" else "source/")
            if code == "invalid_root" and ": " not in message:
                message = f".: {message}"
            print(f"FAIL {prefix}{message}", file=sys.stderr)
        if findings.rows:
            print(f"Preflight failed: {len(findings.rows)} finding(s).", file=sys.stderr)
        else:
            comparison = "; installed inventory, bytes and SHA-256 match" if args.installed else ""
            print(f"Preflight passed: {len(source)} source files{comparison}.")
            print("Offline file checks only; CK3 syntax, APIs and runtime compatibility remain unverified.")
    return result["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
