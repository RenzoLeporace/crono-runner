"""PC HUD: the same single next step as Android, with keyboard wording and a map marker."""
import os,sys,tempfile,unittest
from pathlib import Path
from collections import defaultdict
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'.vendor')]
os.environ.update(SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',PYGAME_HIDE_SUPPORT_PROMPT='1')
import pygame as pg
from crono.game import Game
from crono.i18n import set_language
from test_field_controls import stand_at

class PCGuidanceTests(unittest.TestCase):
    def setUp(self):
        set_language('es');(ROOT/'.test-tmp').mkdir(exist_ok=True);self.temp=tempfile.TemporaryDirectory(dir=ROOT/'.test-tmp')
        self.g=Game(True,Path(self.temp.name)/'save.json');self.g.save.data['touch_controls']=False
    def tearDown(self):set_language('es');pg.quit();self.temp.cleanup()
    def start(self,*level):
        g=self.g;g.load(*(level or (0,)));g.begin();g.tutorial_active=False;g.world.message_time=0;return g
    def test_goal_matches_android_but_names_the_bound_keys(self):
        g=self.start()
        self.assertEqual(g.pc_goal()[1:],g.mobile_goal()[1:])
        self.assertEqual(g.pc_goal()[0],'Visita el puesto 1 · pulsa E')
        g.save.data['key_bindings']['interact']=pg.K_q
        self.assertEqual(g.pc_goal()[0],'Visita el puesto 1 · pulsa Q')
    def test_goal_uses_keyboard_wording_in_portuguese(self):
        g=self.start();set_language('pt-BR')
        self.assertEqual(g.pc_goal()[0],'Visite o posto 1 · pressione E')
    def test_card_replaces_the_long_status_line_and_hides_for_messages_and_bosses(self):
        g=self.start();g.render()
        self.assertTrue(pg.Rect(0,0,1280,720).contains(g.pc_goal_rect))
        g.world.say('Mensaje de prueba');g.render();self.assertIsNone(g.pc_goal_rect)
        g.world.message_time=0;g.render();self.assertIsNotNone(g.pc_goal_rect)
        g.tutorial_active=True;g.render();self.assertIsNone(g.pc_goal_rect)
    def test_all_maps_render_a_single_next_step_on_pc(self):
        g=self.g
        for level in range(50):
            g=self.start(*divmod(level,3));label,point,kind=g.pc_goal()
            self.assertTrue(label);self.assertNotIn('toca ',label.lower())
            g.render()
            if g.pc_goal_rect:self.assertTrue(pg.Rect(0,0,1280,720).contains(g.pc_goal_rect),level)
    def test_holding_the_bound_key_shows_progress_and_finishes_the_work(self):
        g=self.start(12,0);field=g.world.mechanic.field;g.world.mechanic.state['step']=3;field.collected={0,1,2}
        stand_at(g.world,g.world.mechanic.devices[2])
        self.assertIn('mantén E',g.pc_goal()[0])
        with patch('pygame.key.get_pressed',return_value=defaultdict(bool,{pg.K_e:True})):
            for _ in range(40):g.update(1/60)
            self.assertGreater(g.world.mechanic.field.work_target()['progress'],0);g.render()
            for _ in range(80):g.update(1/60)
        self.assertTrue(field.done)

if __name__=='__main__':unittest.main(verbosity=2)
