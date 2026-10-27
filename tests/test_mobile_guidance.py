"""Touch comfort, clear next actions and separate work/descent intents."""
import os,sys,tempfile,unittest
from pathlib import Path
from collections import defaultdict
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'.vendor')]
os.environ.update(SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',PYGAME_HIDE_SUPPORT_PROMPT='1')
import pygame as pg
from crono.game import Game
from crono.physics import Controls,STEP
from crono.touch import boxes_for_width
from test_field_controls import stand_at

class MobileGuidanceTests(unittest.TestCase):
    def setUp(self):
        (ROOT/'.test-tmp').mkdir(exist_ok=True);self.temp=tempfile.TemporaryDirectory(dir=ROOT/'.test-tmp')
        self.g=Game(True,Path(self.temp.name)/'save.json');self.g.save.data['touch_controls']=True;self.g.configure_viewport(1600/720)
    def tearDown(self):pg.quit();self.temp.cleanup()
    def task(self):
        g=self.g;g.load(12,0);g.begin();g.tutorial_active=False
        field=g.world.mechanic.field;g.world.mechanic.state['step']=3;field.collected={0,1,2}
        floor=stand_at(g.world,g.world.mechanic.devices[2]);return field,floor
    def test_jump_is_largest_and_actions_orbit_above_or_left(self):
        for width in (960,1280,1600,2560):
            boxes={k:pg.Rect(v) for k,v in boxes_for_width(width).items()};jump=boxes['jump']
            self.assertEqual(jump.size,(156,156));self.assertEqual(width-jump.right,32)
            for action in ('attack','dash','interact'):
                box=boxes[action];self.assertEqual(box.size,(104,104))
                self.assertTrue(box.centery<jump.centery or box.centerx<jump.centerx)
            for name,box in boxes.items():self.assertFalse(any(box.colliderect(v) for key,v in boxes.items() if key!=name))
    def test_long_use_keeps_its_platform_and_release_resets_progress(self):
        field,floor=self.task();g=self.g
        g.press_interact();self.assertEqual(g.state,'play')
        for _ in range(60):g.world.update(STEP,Controls(work=True))
        self.assertGreater(field.work_elapsed,.4);self.assertFalse(field.done)
        g.world.update(STEP,Controls());self.assertEqual(field.work_elapsed,0)
        for _ in range(120):g.world.update(STEP,Controls(work=True))
        self.assertFalse(field.done)
        for _ in range(70):g.world.update(STEP,Controls(work=True))
        self.assertTrue(field.done);self.assertEqual(g.world.player.rect.bottom,floor.rect.top)
    def test_keyboard_e_holds_work_while_down_only_descends(self):
        field,floor=self.task();g=self.g
        with patch('pygame.key.get_pressed',return_value=defaultdict(bool,{pg.K_e:True})):
            for _ in range(110):g.update(1/60)
        self.assertTrue(field.done);self.assertEqual(g.world.player.drop_time,0)
        field,floor=self.task()
        with patch('pygame.key.get_pressed',return_value=defaultdict(bool,{pg.K_DOWN:True})):g.update(1/60)
        self.assertGreater(g.world.player.drop_time,0);self.assertFalse(field.done)
    def test_goal_changes_with_progress_and_does_not_skip_history(self):
        g=self.g;g.load(0);g.begin();g.tutorial_active=False
        self.assertIn('puesto 1',g.mobile_goal()[0])
        g.world.shards={0,1,2};self.assertIn('puesto',g.mobile_goal()[0])
        g.world.mechanic.state.update(step=3,sea_complete=True)
        self.assertIn('libro',g.mobile_goal()[0])
        g.world.answered.add(0);self.assertIn('Todo listo',g.mobile_goal()[0])
    def test_camera_keeps_the_player_clear_of_thumb_areas_without_moving_geometry(self):
        g=self.g;g.load(0);before=[tuple(p.rect) for p in g.world.platforms]
        self.assertGreater(g.world.player.rect.centerx-g.camera,290)
        g.world.player.rect.right=g.world.width;camera=g.follow_camera_target()
        self.assertLess(g.world.player.rect.centerx-camera,g.viewport_width-345)
        self.assertEqual(before,[tuple(p.rect) for p in g.world.platforms])
    def test_all_maps_have_a_renderable_single_next_step(self):
        g=self.g
        for level in range(50):
            g.load(*divmod(level,3));g.begin();g.tutorial_active=False
            label,point,kind=g.mobile_goal();self.assertTrue(label)
            g.render()
        g.activity_index=0;g.activity_message=''
        for state in ('menu','mobile_more','story','intro','activity'):
            g.set_state(state);g.render()
            self.assertTrue(all(pg.Rect(0,0,1280,720).contains(box) for box,_,_ in g.buttons))
    def test_voice_reads_the_choices_without_identifying_the_correct_one(self):
        g=self.g;g.load(0);g.begin();g.open_lesson(0);g.quiz_mode='question';g.render()
        with patch.object(g,'read_aloud') as read:
            g.buttons[0][1]()
            value=read.call_args.args[0]
        self.assertIn(g.question.prompt,value)
        for option in g.question.options:self.assertIn(option,value)
        self.assertNotIn('Respuesta:',value)
        with patch('crono.mobile.bridge',return_value=None):g.read_aloud('Busca el libro')
        self.assertEqual(g.state,'quiz');self.assertGreater(g.notice_time,0)
    def test_low_water_temporarily_guides_to_a_refill(self):
        g=self.g;g.load(8,0);g.begin();g.tutorial_active=False;g.world.traits.resource=15
        self.assertIn('agua',g.mobile_goal()[0].lower())
        self.assertIn(g.mobile_goal()[1],g.world.traits.points)
        g.world.traits.resource=100;self.assertIn('puesto',g.mobile_goal()[0])
    def test_the_marked_task_can_be_held_directly_on_the_map(self):
        field,floor=self.task();g=self.g;g.camera=g.follow_camera_target();g.render()
        self.assertTrue(g.world_action_hotspots)
        pos=g.world_action_hotspots[0].center
        g.touch_event(pg.event.Event(pg.FINGERDOWN,finger_id=34,x=pos[0]/1600,y=pos[1]/720))
        self.assertTrue(g.touch_down('interact'));self.assertEqual(g.state,'play')
        with patch('pygame.key.get_pressed',return_value=defaultdict(bool)):
            for _ in range(110):g.update(1/60)
        self.assertTrue(field.done);self.assertEqual(g.world.player.drop_time,0)

if __name__=='__main__':unittest.main(verbosity=2)
