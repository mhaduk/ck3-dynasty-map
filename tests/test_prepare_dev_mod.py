import hashlib
import tempfile
from pathlib import Path
import shutil
import unittest

from scripts.prepare_dev_mod import (
    CURRENT_DEV_OUTPUT_HASHES,
    EXPECTED_CLEAN_FILES,
    OMITTED,
    SOURCE,
    prepare,
)


class PrepareDevTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'source'
        self.source.mkdir()
        (self.source / 'descriptor.mod').write_text(
            'name="Historical Probe"\nversion="0.0.0"\nsupported_version="1.20.1.2"\n')
        (self.source / 'runtime.txt').write_bytes(b'\xef\xbb\xbfunchanged\r\n')
        self.output = self.root / 'dynasty_map_dev'

    def test_metadata_only_and_source_preserved(self):
        original = (self.source / 'descriptor.mod').read_bytes()
        prepare(self.source, self.output)
        self.assertEqual((self.output / 'runtime.txt').read_bytes(),
                         (self.source / 'runtime.txt').read_bytes())
        self.assertEqual((self.source / 'descriptor.mod').read_bytes(), original)
        self.assertEqual((self.output / 'descriptor.mod').read_bytes(),
                         original.replace(b'Historical Probe', b'Dynasty Map [DEV]'))

    def test_existing_destination_rejected(self):
        self.output.mkdir()
        with self.assertRaises(ValueError):
            prepare(self.source, self.output)

    def test_symlink_rejected(self):
        (self.source / 'link').symlink_to(self.source / 'runtime.txt')
        with self.assertRaises(ValueError):
            prepare(self.source, self.output)
        self.assertFalse(self.output.exists())

    def test_output_inside_source_rejected(self):
        with self.assertRaises(ValueError):
            prepare(self.source, self.source / 'nested')

    def test_nonportable_descriptor_rejected(self):
        with (self.source / 'descriptor.mod').open('a') as stream:
            stream.write('path="private-location"\n')
        with self.assertRaises(ValueError):
            prepare(self.source, self.output)
        self.assertFalse(self.output.exists())

    def test_clean_profile_builds_exact_eight_and_keeps_retained_bodies(self):
        out = self.root / 'clean'
        prepare(SOURCE, out, profile='r009-clean')
        actual = {p.relative_to(out).as_posix() for p in out.rglob('*') if p.is_file()}
        self.assertEqual(actual, EXPECTED_CLEAN_FILES - {str(p) for p in OMITTED})
        for rel in actual - {'descriptor.mod'}:
            self.assertEqual((out / rel).read_bytes(), (SOURCE / rel).read_bytes(), rel)
        self.assertIn('name="Dynasty Map [DEV]"', (out / 'descriptor.mod').read_text())

    def test_clean_profile_rejects_fixture_drift_before_output(self):
        changed = self.root / 'changed'
        shutil.copytree(SOURCE, changed)
        fixture = changed / next(iter(OMITTED))
        fixture.write_bytes(fixture.read_bytes() + b'\n')
        with self.assertRaisesRegex(ValueError, 'fixture drift'):
            prepare(changed, self.output, profile='r009-clean')
        self.assertFalse(self.output.exists())

    def test_clean_profile_rejects_retained_reference_before_output(self):
        changed = self.root / 'referencing'
        shutil.copytree(SOURCE, changed)
        retained = changed / 'common/scripted_effects/dynmap_r016.txt'
        retained.write_bytes(retained.read_bytes() + b'\nd_dynmap_r016_direct\n')
        with self.assertRaisesRegex(ValueError, 'retained reference'):
            prepare(changed, self.output, profile='r009-clean')
        self.assertFalse(self.output.exists())

    def test_current_dev_matches_accepted_eight_file_candidate(self):
        out = self.root / 'current-dev'
        prepare(SOURCE, out, profile='current-dev')
        actual = {p.relative_to(out).as_posix() for p in out.rglob('*') if p.is_file()}
        self.assertEqual(actual, set(CURRENT_DEV_OUTPUT_HASHES))
        for rel in actual:
            self.assertEqual(
                hashlib.sha256((out / rel).read_bytes()).hexdigest(),
                CURRENT_DEV_OUTPUT_HASHES[rel],
                rel,
            )

    def test_current_dev_rejects_gui_source_drift(self):
        changed = self.root / 'gui-drift'
        shutil.copytree(SOURCE, changed)
        gui = changed / 'gui/zz_dynmap_r016_views.gui'
        gui.write_bytes(gui.read_bytes() + b'\n')
        with self.assertRaisesRegex(ValueError, 'current-dev source drift'):
            prepare(changed, self.output, profile='current-dev')
        self.assertFalse(self.output.exists())

    def test_current_dev_rejects_retained_source_drift(self):
        changed = self.root / 'script-drift'
        shutil.copytree(SOURCE, changed)
        script = changed / 'common/scripted_effects/dynmap_r016.txt'
        script.write_bytes(script.read_bytes() + b'\n')
        with self.assertRaisesRegex(ValueError, 'current-dev source drift'):
            prepare(changed, self.output, profile='current-dev')
        self.assertFalse(self.output.exists())


if __name__ == '__main__':
    unittest.main()
