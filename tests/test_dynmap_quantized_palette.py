"""Contract tests for the accepted tolerant 76-pair F-002 selector."""
import json
import re
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/'research/probes/my-dynasty-r016/mod'
TABLE=json.loads((ROOT/'data/dynmap-r016-palette.json').read_text())
class TolerantPaletteSourceTests(unittest.TestCase):
 def test_selector_writes_six_fresh_channels_then_matches_all_complete_rows(self):
  src=(MOD/'common/scripted_effects/dynmap_r016.txt').read_text(encoding='utf-8-sig')
  body=src.split('dynmap_r016_select_palette_effect = {',1)[1].split('\n}',1)[0]
  for channel in ('c1_r','c1_g','c1_b','c2_r','c2_g','c2_b'):
   self.assertIn(f'name = dynmap_r016_last_{channel}',body)
  self.assertEqual(body.count('value = scope:dynmap_r016_pair_c'),6)
  ids=set(map(int,re.findall(r'set_variable = \{ name = dynmap_r016_pair_cache_id value = (\d+) \}',body)))
  self.assertEqual(ids,{r['pair_id'] for r in TABLE['rows']}|{126})
  for row in TABLE['rows']:
   block=re.search(rf'(?s)(?:if|else_if) = \{{\s*limit = \{{ AND = \{{(.*?)\}} \}}\s*set_variable = \{{ name = dynmap_r016_pair_cache_id value = {row["pair_id"]} \}}',body)
   self.assertIsNotNone(block,row['pair_id'])
   for name,center in zip(('c1_r','c1_g','c1_b','c2_r','c2_g','c2_b'),row['rgb6_center']):
    self.assertIn(f'var:dynmap_r016_last_{name} >= {max(0,center-5)}',block.group(1))
    self.assertIn(f'var:dynmap_r016_last_{name} <= {min(255,center+5)}',block.group(1))
 def test_writers_cover_76_ids_and_exact_historical_fallback(self):
  src=(MOD/'common/scripted_effects/dynmap_r016.txt').read_text(encoding='utf-8-sig')
  for name,shade in [('dynmap_r016_paint_mixed_primary_effect','dark'),('dynmap_r016_paint_mixed_secondary_effect','light')]:
   body=src.split(name+' = {',1)[1].split('\n}',1)[0]
   cases={int(i):list(map(int,rgb.split())) for i,rgb in re.findall(r'scope:dynmap_r016_palette_id = (\d+) \} set_title_color = \{ ([0-9 ]+) \}',body)}
   expected={r['pair_id']:r[shade] for r in TABLE['rows']}
   self.assertEqual({i:cases[i] for i in expected},expected)
   self.assertEqual(re.search(r'else = \{ set_title_color = \{ ([0-9 ]+) \} \}',body)[1], ' '.join(map(str,TABLE['unknown_fallback'][shade])))
if __name__=='__main__': unittest.main()
