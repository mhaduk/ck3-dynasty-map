"""Player-context guards in the accepted F-002 source."""
from pathlib import Path
import re, unittest
ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/'research/probes/my-dynasty-r016/mod'
class PaletteContextTests(unittest.TestCase):
 def test_character_scoped_actions_guard_living_dynasty_context(self):
  source=(MOD/'common/scripted_guis/dynmap_r016.txt').read_text(encoding='utf-8-sig')
  blocks=re.findall(r'(?ms)^(dynmap_r016_\w+) = \{(.*?)^\}',source)
  self.assertEqual(len(blocks),19)
  for name,body in blocks:
   if name=='dynmap_r016_pair_cache_has_value': continue
   with self.subTest(name=name):
    self.assertIn('scope = character',body)
    self.assertRegex(body,r'is_valid = \{ is_alive = yes exists = dynasty \}')
    self.assertLess(body.index('is_valid'),body.index('effect ='))
 def test_custom_controls_are_hidden_without_a_valid_player(self):
  menu=(MOD/'gui/zz_dynmap_r016_menu.gui').read_text(encoding='utf-8-sig')
  views=(MOD/'gui/zz_dynmap_r016_views.gui').read_text(encoding='utf-8-sig')
  self.assertIn('GetPlayer.IsValid',menu+views)
  self.assertIn('GetPlayer.GetDynasty.GetDynastyCoA',menu+views)
  self.assertIn('130 40',views)
if __name__=='__main__': unittest.main()
