#!/usr/bin/env python3
"""Read-only payload checks. Does not parse CK3 scripts or validate runtime APIs."""

import argparse
import hashlib
from pathlib import Path
import re
import sys


BOM = b"\xef\xbb\xbf"


def inspect(root, label, expected_version, errors):
    inventory = {}

    def fail(path, message):
        errors.append(f"{label}/{path}: {message}")

    if not root.is_dir() or root.is_symlink():
        fail(".", "payload root must be an existing ordinary directory")
        return inventory
    if (root / "coat_of_arms").exists():
        fail("coat_of_arms", "misplaced CoA folder; use common/coat_of_arms/coat_of_arms")

    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        name = relative.as_posix()
        if path.is_symlink():
            fail(name, "symlinks are not supported in a reviewed payload")
            continue
        if not path.is_file():
            continue
        parts = [part.lower() for part in relative.parts]
        if (any(part in {"evidence", "alternatives", "logs", "saves", "__pycache__"}
                for part in parts)
                or path.name.lower().startswith("readme")
                or path.name in {".DS_Store", ".gitignore"}
                or path.suffix.lower() in {".log", ".ck3", ".pyc"}):
            fail(name, "research/evidence or incidental file does not belong in payload")
        try:
            data = path.read_bytes()
        except OSError:
            fail(name, "cannot read file")
            continue
        inventory[name] = data
        script = parts[0] in {"common", "gfx"} and path.suffix.lower() == ".txt"
        localization = parts[0] == "localization" and path.suffix.lower() == ".yml"
        utf8 = script or localization or path.suffix.lower() in {".gui", ".mod"}
        if not utf8:
            continue
        if (script or localization) and not data.startswith(BOM):
            fail(name, "requires exactly one leading UTF-8 BOM (project convention)")
        if data.startswith(BOM + BOM):
            fail(name, "duplicate leading UTF-8 BOM")
        try:
            content = data.decode("utf-8-sig", errors="strict")
        except UnicodeDecodeError:
            fail(name, "invalid UTF-8")
            continue
        if localization:
            lines = [line.strip() for line in content.splitlines()
                     if line.strip() and not line.lstrip().startswith("#")]
            header = re.fullmatch(r"l_([a-z_]+):(?:\s*#.*)?", lines[0]) if lines else None
            if not header:
                fail(name, "first substantive line must be l_<language>:")
            else:
                language = header.group(1)
                if len(parts) < 3 or relative.parts[1] != language:
                    fail(name, "localization folder and header language differ")
                if not path.name.endswith(f"_l_{language}.yml"):
                    fail(name, "filename must end in _l_<language>.yml")

    descriptor = inventory.get("descriptor.mod")
    if descriptor is None:
        fail("descriptor.mod", "required file missing")
    else:
        try:
            content = descriptor.decode("utf-8-sig", errors="strict")
        except UnicodeDecodeError:
            content = ""  # Already reported above.
        for field in ("name", "version", "supported_version"):
            values = re.findall(r'^\s*' + field + r'\s*=\s*"([^"\n]+)"\s*(?:#.*)?$',
                                content, flags=re.MULTILINE)
            if len(values) != 1:
                fail("descriptor.mod", f"requires one quoted {field} declaration")
            elif field == "supported_version" and expected_version is not None:
                if values[0] != expected_version:
                    fail("descriptor.mod", f"supported_version must equal {expected_version}")
    return inventory


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("payload", type=Path, help="explicit source mod payload root")
    parser.add_argument("--installed", type=Path, help="compare exact installed inventory and bytes")
    parser.add_argument("--expected-version", help="exact supported_version declaration")
    args = parser.parse_args()
    errors = []
    try:
        source = inspect(args.payload, "source", args.expected_version, errors)
        if args.installed is not None:
            installed = inspect(args.installed, "installed", args.expected_version, errors)
            for name in sorted(source.keys() - installed.keys()):
                errors.append(f"installed/{name}: missing from installed inventory")
            for name in sorted(installed.keys() - source.keys()):
                errors.append(f"installed/{name}: extra installed file")
            for name in sorted(source.keys() & installed.keys()):
                # Check both bytes and their SHA-256, for reproducible install receipts.
                if (source[name] != installed[name]
                        or hashlib.sha256(source[name]).digest()
                        != hashlib.sha256(installed[name]).digest()):
                    errors.append(f"installed/{name}: bytes/SHA-256 differ from source")
    except OSError:
        errors.append("payload: filesystem inspection failed")
    for error in errors:
        print(f"FAIL {error}", file=sys.stderr)
    if errors:
        print(f"Preflight failed: {len(errors)} finding(s).", file=sys.stderr)
        return 1
    comparison = "; installed inventory, bytes and SHA-256 match" if args.installed else ""
    print(f"Preflight passed: {len(source)} source files{comparison}.")
    print("Offline file checks only; CK3 syntax, APIs and runtime compatibility remain unverified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
