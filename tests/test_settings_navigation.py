"""Regression checks for the settings and in-map return paths Renzo reported."""
import os,sys,tempfile,unittest
from pathlib import Path
from collections import defaultdict
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'.vendor')]
os.environ.update(SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',PYGAME_HIDE_SUPPORT_PROMPT='1')
import pygame as pg
from crono.game import Game
from crono.save import Save
from crono.physics import Controls,STEP,Platform
from crono.touch import boxes_for_width

class SettingsNavigationTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=ROOT/'.test-tmp');self.path=Path(self.temp.name)/'save.json'
        self.g=Game(True,self.path);self.g.load(0);self.g.begin();self.g.tutorial_active=False
    def tearDown(self):pg.quit();self.temp.cleanup()
    def escape(self):
        pg.event.clear();pg.event.post(pg.event.Event(pg.KEYDOWN,key=pg.K_ESCAPE));self.g.events()
    def test_escape_unwinds_nested_map_panels(self):
        g=self.g
        for state in ('story','activity','rescue_info'):
            g.set_state(state);self.escape();self.assertEqual(g.state,'play')
        g.open_settings();g.set_state('accessibility');self.escape();self.assertEqual(g.state,'settings')
        self.escape();self.assertEqual(g.state,'play')
        g.set_state('pause');g.open_settings();g.set_state('sound_settings')
        self.escape();self.assertEqual(g.state,'settings');self.escape();self.assertEqual(g.state,'pause')
        self.escape();self.assertEqual(g.state,'play')
    def test_teacher_unlock_does_not_leave_menu_or_change_real_records(self):
        g=self.g;g.open_settings();g.open_community('teacher');records=dict(g.save.data['records'])
        for value in (True,False):
            g.toggle_practice();self.assertEqual(g.state,'community')
            self.assertEqual(g.save.data['practice'],value);self.assertEqual(g.save.data['records'],records)
        self.escape();self.assertEqual(g.state,'settings');self.escape();self.assertEqual(g.state,'play')
    def test_binding_and_reset_persist_and_cancel_capture(self):
        g=self.g;g.open_settings();g.set_state('accessibility');g.begin_rebind('jump')
        pg.event.clear();pg.event.post(pg.event.Event(pg.KEYDOWN,key=pg.K_j));g.events()
        self.assertEqual(g.key_for('jump'),pg.K_j);self.assertIsNone(g.rebind_action)
        self.assertEqual(Save(self.path).data['key_bindings']['jump'],pg.K_j)
        g.begin_rebind('dash');g.reset_keys();self.assertIsNone(g.rebind_action)
        self.assertEqual(g.key_for('jump'),pg.K_SPACE);self.assertFalse(Save(self.path).data['key_bindings'])
    def test_sound_levels_survive_reload_and_apply_without_restart(self):
        g=self.g;g.set_volume('music_volume',25);g.set_volume('effects_volume',0)
        self.assertEqual(g.audio.music_volume,.25);self.assertEqual(g.audio.effects_volume,0)
        saved=Save(self.path);self.assertEqual(saved.data['music_volume'],25);self.assertEqual(saved.data['effects_volume'],0)
    def test_all_thin_default_ledges_can_be_descended_but_ground_stays_solid(self):
        g=self.g;p=g.world.player
        ledge=Platform(dict(x=200,y=400,w=300,h=28,moving=False));g.world.platforms=[ledge]
        p.rect.midbottom=(300,400);p.grounded=True;p.support=ledge
        with patch('pygame.key.get_pressed',return_value=defaultdict(bool,{pg.K_DOWN:True})):g.update(1/60)
        self.assertGreater(p.rect.bottom,400)
        self.assertFalse(Platform(dict(x=0,y=584,w=600,h=220,moving=False)).oneway)
    def test_dash_cannot_repeat_until_cooldown_and_upgrade_reduces_it(self):
        g=self.g;p=g.world.player;p.grounded=True
        self.assertIn('dash',p.update(STEP,Controls(dash=True),g.world));base=p.cooldown
        p.dash_time=0;p.dash_ready=True
        self.assertNotIn('dash',p.update(STEP,Controls(dash=True),g.world))
        p.cooldown=0;p.upgrades.add('dash')
        self.assertIn('dash',p.update(STEP,Controls(dash=True),g.world));self.assertLess(p.cooldown,base)
    def test_touch_jump_stays_held_when_thumb_drifts(self):
        g=self.g;g.save.data['touch_controls']=True;box=pg.Rect(boxes_for_width(g.viewport_width)['jump'])
        for kind,x,y in ((pg.FINGERDOWN,box.centerx,box.centery),(pg.FINGERMOTION,box.left-10,box.centery)):
            g.touch_event(pg.event.Event(kind,finger_id=1,x=x/g.viewport_width,y=y/720))
        self.assertTrue(g.touch_down('jump'))
        g.touch_event(pg.event.Event(pg.FINGERUP,finger_id=1,x=0,y=0));self.assertFalse(g.touch_down('jump'))
    def test_mobile_reading_size_changes_actual_glyphs_and_pagination(self):
        g=self.g;g.save.data['touch_controls']=True;g.open_lesson(0)
        images=[]
        for size in (19,25):
            g.save.data['reading_size']=size;g.render();images.append(pg.image.tobytes(g.canvas.subsurface((90,182,1070,250)),'RGB'))
        self.assertNotEqual(*images)

    def test_minimizing_pauses_world_and_releases_touch_and_pending_actions(self):
        g=self.g;before=g.world.player.rect.copy();elapsed=g.world.time
        g.fingers={1:'right',2:'jump'};g.finger_positions={1:(20,40)}
        g.jump_pending=g.dash_pending=g.shoot_pending=g.work_lock=True
        pg.event.clear();pg.event.post(pg.event.Event(pg.WINDOWMINIMIZED));g.events()
        self.assertEqual(g.state,'pause');self.assertFalse(g.fingers or g.finger_positions)
        self.assertFalse(g.jump_pending or g.dash_pending or g.shoot_pending or g.work_lock)
        g.update(.1)
        self.assertEqual(g.world.player.rect,before);self.assertEqual(g.world.time,elapsed)
        self.escape();self.assertEqual(g.state,'play')

    def test_focus_loss_pauses_voyage_without_stuck_helm_after_return(self):
        g=self.g;g.start_voyage();v=g.voyage
        g.fingers={1:'right',2:'attack'};g.finger_positions={1:(20,40)}
        pg.event.clear();pg.event.post(pg.event.Event(pg.WINDOWFOCUSLOST));g.events()
        self.assertTrue(v.paused);self.assertFalse(g.fingers or g.finger_positions)
        before=(v.x,v.y,v.time,len(v.shots));g.voyage_update(.1)
        self.assertEqual((v.x,v.y,v.time,len(v.shots)),before)
        v.paused=False;g.voyage_update(.05)
        self.assertEqual((v.x,v.y),before[:2]);self.assertFalse(v.shots)

if __name__=='__main__':unittest.main()
