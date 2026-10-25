"""Camera continuity and usable touch targets on wide Android screens."""
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'.vendor')]
os.environ.update(SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',PYGAME_HIDE_SUPPORT_PROMPT='1')
import pygame as pg
from crono.game import Game
from crono.touch import boxes_for_width
from crono.viewport import mobile_backdrop,width_for_aspect


class AndroidRenderTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=ROOT/'.test-tmp')
        self.g=Game(True,Path(self.temp.name)/'save.json')
        self.g.save.data['touch_controls']=True
        self.g.configure_viewport(1600/720)

    def tearDown(self):
        pg.quit();self.temp.cleanup()

    def test_sky_does_not_slide_or_snap_at_old_buffer_boundaries(self):
        g=self.g
        for level in (0,24,44):
            g.load(*divmod(level,3))
            samples=[]
            for camera in (0,158,160,638,640,642,958,960,962,1600,642,0):
                mobile_backdrop(g.artist,g.world_canvas,g.world,camera)
                samples.append(pg.image.tobytes(g.world_canvas.subsurface((0,105,1600,30)),'RGB'))
            self.assertTrue(all(sample==samples[0] for sample in samples),f'Sky jumped in map {level}')

    def test_camera_movement_keeps_sky_assets_and_render_width(self):
        from crono import period_art,art
        g=self.g;g.load(0)
        mobile_backdrop(g.artist,g.world_canvas,g.world,0)
        sky=period_art.sky(0,0);misses=period_art.sky.cache_info().misses
        for camera in range(0,6000,47):
            mobile_backdrop(g.artist,g.world_canvas,g.world,camera)
            self.assertEqual(art.W,1600)
        self.assertIs(period_art.sky(0,0),sky)
        self.assertEqual(period_art.sky.cache_info().misses,misses)

    def test_larger_targets_have_padding_and_never_overlap(self):
        for width in (960,1280,1600,1920,2560):
            boxes={key:pg.Rect(box) for key,box in boxes_for_width(width).items()}
            self.assertEqual(boxes['left'].left,32)
            self.assertEqual(width-boxes['jump'].right,32)
            self.assertEqual(boxes['jump'].size,(112,112))
            for key,box in boxes.items():
                self.assertGreaterEqual(min(box.size),96)
                self.assertTrue(pg.Rect(32,100,width-64,588).contains(box))
                self.assertFalse(any(box.colliderect(other) for name,other in boxes.items() if name!=key))

    def test_multitouch_works_at_enlarged_edges_and_after_sliding(self):
        g=self.g;g.load(0);g.begin();g.tutorial_active=False;g.render()
        # A different physical resolution must preserve the same touch targets.
        g.display=pg.display.set_mode((2400,1080))
        boxes=boxes_for_width(1600)
        def touch(kind,finger,action):
            box=pg.Rect(boxes[action])
            g.touch_event(pg.event.Event(kind,finger_id=finger,x=(box.right-5)/1600,y=(box.bottom-5)/720))
        touch(pg.FINGERDOWN,71,'right');touch(pg.FINGERDOWN,72,'jump')
        self.assertTrue(g.touch_down('right'));self.assertTrue(g.touch_down('jump'))
        self.assertTrue(g.jump_pending)
        touch(pg.FINGERMOTION,71,'left')
        self.assertFalse(g.touch_down('right'));self.assertTrue(g.touch_down('left'))
        touch(pg.FINGERUP,71,'left');touch(pg.FINGERUP,72,'jump')
        self.assertFalse(any(g.fingers.values()))

    def test_unchanged_or_clamped_viewport_does_not_recreate_surfaces(self):
        g=self.g;world=g.world_canvas;ui=g.ui_canvas;display=g.display
        g.configure_viewport(1600/720)
        self.assertIs(g.world_canvas,world);self.assertIs(g.ui_canvas,ui);self.assertIs(g.display,display)
        g.configure_viewport(4);world=g.world_canvas
        self.assertEqual(width_for_aspect(4),2560)
        g.configure_viewport(5);self.assertIs(g.world_canvas,world)


if __name__=='__main__':unittest.main(verbosity=2)
