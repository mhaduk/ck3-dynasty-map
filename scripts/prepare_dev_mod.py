#!/usr/bin/env python3
"""Prepare the current DEV payload; historical source identity stays intact."""
import argparse
import hashlib
from pathlib import Path
import re
import shutil

SOURCE = Path(__file__).resolve().parents[1] / 'research/probes/my-dynasty-r016/mod'
NAME = 'Dynasty Map [DEV]'
OMITTED = {
    Path('common/landed_titles/dynmap_r016_colors.txt'):
        'a07fda5fb91208dc184e05763c1bd1ea481255baf3dc97f40751fcfd98fea6cc',
    Path('common/coat_of_arms/coat_of_arms/dynmap_r016_colors.txt'):
        '8c89ee15588968da6f96d0e6e964f5268c52ec54210c5abb1c837fa3bbb39e98',
}
CURRENT_DEV_SOURCE_HASHES = {
    Path('common/scripted_effects/dynmap_r016.txt'): '3dcc3e171ceece48e80b1109f33d5507740d9e86dab88f5f76b71b771b24cdba',
    Path('common/scripted_guis/dynmap_r016.txt'): '0d25952481ea2e256d943d6168050f139115633d9951aeb4f9597d07fadbd210',
    Path('data_binding/dynmap_r016_palette.txt'): 'e998992d0ad0bdc68d7833b9dcc466f9226dfb344ffcd0a6dfddd72c57ef71c6',
    Path('descriptor.mod'): '038b5dc5e57842553003de6daa590d5076e77d47cbba43a9043e3f16d528b09f',
    Path('gfx/map/map_modes/dynmap_r016_modes.txt'): '2ba3d1d7dece542bf09aab11ca56ae0fdff3d452f95d6231c602b96cbd667660',
    Path('gui/zz_dynmap_r016_menu.gui'): '364029bb3a8524b3b40c3ea17f8a58f0c63ceb60901fd7ad21d602efd262ef54',
    Path('gui/zz_dynmap_r016_views.gui'): 'ff59841fc1b3992db232d26e8a98cce75713edc73f040f48895e9fa47d389d7a',
    Path('localization/english/dynmap_r016_l_english.yml'): '25947af99f7267fb3e92cae9006d6d9bdff10d3fcf41cdfff00de4e496f18b9a',
    **OMITTED,
}
CURRENT_DEV_OUTPUT_HASHES = {
    'common/scripted_effects/dynmap_r016.txt': '3dcc3e171ceece48e80b1109f33d5507740d9e86dab88f5f76b71b771b24cdba',
    'common/scripted_guis/dynmap_r016.txt': '0d25952481ea2e256d943d6168050f139115633d9951aeb4f9597d07fadbd210',
    'data_binding/dynmap_r016_palette.txt': 'e998992d0ad0bdc68d7833b9dcc466f9226dfb344ffcd0a6dfddd72c57ef71c6',
    'descriptor.mod': 'c70d4611c9c6f0c2e699255d8f7a8de61c0821258041fdcf73e8087373da7dc0',
    'gfx/map/map_modes/dynmap_r016_modes.txt': '2ba3d1d7dece542bf09aab11ca56ae0fdff3d452f95d6231c602b96cbd667660',
    'gui/zz_dynmap_r016_menu.gui': '364029bb3a8524b3b40c3ea17f8a58f0c63ceb60901fd7ad21d602efd262ef54',
    'gui/zz_dynmap_r016_views.gui': '5a6a7fce1fdcb6599c3e690c2b69b66293e1e98113314a36649376556e463cc9',
    'localization/english/dynmap_r016_l_english.yml': '25947af99f7267fb3e92cae9006d6d9bdff10d3fcf41cdfff00de4e496f18b9a',
}
GUI_ANCHOR = '        block "map_mode_banner_background" {}'
GUI_INSERT = '''        # Automatic presentation fallback; outside all player-scoped content.
        widget = {
            name = "dynmap_r016_absent_player_exit"
            size = { 0 0 }
            visible = yes
            state = {
                name = "dynmap_r016_absent_player_exit_to_realms"
                trigger_when = "[And(Not(GetPlayer.IsValid), Or3(IsMapMode('dynmap_my_dynasty'), IsMapMode('dynmap_dynasty_holdings'), IsMapMode('dynmap_my_realm_dynasty')))]"
                on_finish = "[SetMapMode('realms')]"
            }
        }
'''
OMITTED_KEYS = ('d_dynmap_r016_direct', 'd_dynmap_r016_controlled', 'd_dynmap_r016_other')
EXPECTED_CLEAN_FILES = {
    'common/scripted_effects/dynmap_r016.txt', 'common/scripted_guis/dynmap_r016.txt',
    'data_binding/dynmap_r016_palette.txt', 'descriptor.mod',
    'gfx/map/map_modes/dynmap_r016_modes.txt', 'gui/zz_dynmap_r016_menu.gui',
    'gui/zz_dynmap_r016_views.gui', 'localization/english/dynmap_r016_l_english.yml',
    *map(str, OMITTED),
}


def prepare(source, destination, profile='legacy'):
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
    if profile not in ('legacy', 'r009-clean', 'current-dev'):
        raise ValueError('unsupported profile')
    if profile in ('r009-clean', 'current-dev'):
        actual = {p.relative_to(source).as_posix() for p in source.rglob('*') if p.is_file()}
        if actual != EXPECTED_CLEAN_FILES:
            raise ValueError('clean profile requires the frozen ten-file source inventory')
        for relative, expected in OMITTED.items():
            if hashlib.sha256((source / relative).read_bytes()).hexdigest() != expected:
                raise ValueError(f'clean profile fixture drift: {relative.as_posix()}')
        keys = re.compile(r'\b(?:' + '|'.join(map(re.escape, OMITTED_KEYS)) + r')\b')
        for path in source.rglob('*'):
            if path.is_file() and path.relative_to(source) not in OMITTED:
                if keys.search(path.read_text(encoding='utf-8-sig')):
                    raise ValueError(f'clean profile retained reference: {path.relative_to(source)}')
    if profile == 'current-dev':
        for relative, expected in CURRENT_DEV_SOURCE_HASHES.items():
            if hashlib.sha256((source / relative).read_bytes()).hexdigest() != expected:
                raise ValueError(f'current-dev source drift: {relative.as_posix()}')
        gui = source / 'gui/zz_dynmap_r016_views.gui'
        gui_text = gui.read_text(encoding='utf-8')
        if gui_text.count(GUI_ANCHOR) != 1:
            raise ValueError('current-dev GUI insertion anchor missing or ambiguous')
    descriptor = (source / 'descriptor.mod').read_text(encoding='utf-8')
    if len(re.findall(r'^name\s*=\s*"[^"\r\n]*"\s*$', descriptor, re.M)) != 1:
        raise ValueError('expected exactly one name declaration')
    if re.search(r'^\s*(path|remote_file_id)\s*=', descriptor, re.M):
        raise ValueError('source descriptor must be portable and unassociated')
    descriptor = re.sub(r'^name\s*=\s*"[^"\r\n]*"[^\S\r\n]*',
                        f'name="{NAME}"', descriptor, count=1, flags=re.M)
    shutil.copytree(source, destination)
    (destination / 'descriptor.mod').write_text(descriptor, encoding='utf-8')
    if profile in ('r009-clean', 'current-dev'):
        for relative in OMITTED:
            (destination / relative).unlink()
    if profile == 'current-dev':
        gui = destination / 'gui/zz_dynmap_r016_views.gui'
        gui_text = gui.read_text(encoding='utf-8')
        gui.write_text(gui_text.replace(GUI_ANCHOR, GUI_INSERT + GUI_ANCHOR, 1), encoding='utf-8')
        actual = {p.relative_to(destination).as_posix() for p in destination.rglob('*') if p.is_file()}
        if actual != set(CURRENT_DEV_OUTPUT_HASHES):
            raise ValueError('current-dev output inventory drift')
        for relative, expected in CURRENT_DEV_OUTPUT_HASHES.items():
            digest = hashlib.sha256((destination / relative).read_bytes()).hexdigest()
            if digest != expected:
                raise ValueError(f'current-dev output mismatch: {relative}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--profile', choices=('legacy', 'r009-clean', 'current-dev'), default='legacy')
    args = parser.parse_args()
    try:
        prepare(SOURCE, args.output, profile=args.profile)
    except (OSError, ValueError) as exc:
        parser.exit(1, f'DEV preparation failed: {exc}\n')
    print('DEV payload prepared; run mod preflight before installation.')


if __name__ == '__main__':
    main()
