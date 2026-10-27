"""Formula and generated-table regression tests for F-002."""
import json, math, runpy, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
GEN=runpy.run_path(str(ROOT/'scripts/generate_dynmap_palette.py'))
DATA=json.loads((ROOT/'data/dynmap-r016-palette.json').read_text())
class PaletteFormulaTests(unittest.TestCase):
 def test_floor_and_light_formula(self):
  self.assertEqual(GEN['shades']((0,0,0),(0,0,0)),([40,40,40],[115,115,115]))
  self.assertEqual(GEN['shades']((10,5,0),(20,10,0))[0],[40,20,0])
  self.assertEqual(GEN['shades']((40,20,10),(40,20,10))[0],[40,20,10])
 def test_generated_table_matches_frozen_ordered_roster(self):
  inp=json.loads((ROOT/'data/f002-color-pairs.json').read_text())
  generated=GEN['build'](inp)
  self.assertEqual(generated,DATA)
  self.assertEqual((DATA['pair_count'],DATA['complete_pair_count'],DATA['missing_color2_count']),(88,76,12))
  self.assertEqual(DATA['matching'],{'channels':6,'inclusive_tolerance':5,'boxes_disjoint':True})
if __name__=='__main__': unittest.main()
