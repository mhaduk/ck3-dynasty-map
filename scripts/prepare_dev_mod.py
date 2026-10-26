#!/usr/bin/env python3
"""Prepare the current DEV payload; historical source identity stays intact."""
import argparse
from pathlib import Path
import re
import shutil

SOURCE = Path(__file__).resolve().parents[1] / 'research/probes/my-dynasty-r016/mod'
NAME = 'Dynasty Map [DEV]'


def prepare(source, destination):
    source, destination = Path(source), Path(destination)
    if source.is_symlink() or not source.is_dir():
        raise ValueError('source must be an ordinary payload directory')
    if any(p.is_symlink() for p in source.rglob('*')):
        raise ValueError('payload symlinks are not supported')
    if destination.exists() or destination.is_symlink():
        raise ValueError('output must be new; never overwrite an installed mod')
    resolved = destination.resolve()
    if resolved == source.resolve() or source.resolve() in resolved.parents:
        raise ValueError('output must be outside source')
    descriptor = (source / 'descriptor.mod').read_text(encoding='utf-8')
    if len(re.findall(r'^name\s*=\s*"[^"\r\n]*"\s*$', descriptor, re.M)) != 1:
        raise ValueError('expected exactly one name declaration')
    if re.search(r'^\s*(path|remote_file_id)\s*=', descriptor, re.M):
        raise ValueError('source descriptor must be portable and unassociated')
    descriptor = re.sub(r'^name\s*=\s*"[^"\r\n]*"[^\S\r\n]*',
                        f'name="{NAME}"', descriptor, count=1, flags=re.M)
    shutil.copytree(source, destination)
    (destination / 'descriptor.mod').write_text(descriptor, encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        prepare(SOURCE, args.output)
    except (OSError, ValueError) as exc:
        parser.exit(1, f'DEV preparation failed: {exc}\n')
    print('DEV payload prepared; run mod preflight before installation.')


if __name__ == '__main__':
    main()
