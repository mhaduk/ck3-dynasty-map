import tempfile
from pathlib import Path
import unittest

from scripts.prepare_dev_mod import prepare


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


if __name__ == '__main__':
    unittest.main()
