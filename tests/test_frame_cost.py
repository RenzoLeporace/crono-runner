"""Fewer full-screen passes and no first-visit art builds, with identical pixels."""
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
from crono import argentina_art,period_art


class FrameCostTests(unittest.TestCase):
    def setUp(self):
        (ROOT/'.test-tmp').mkdir(exist_ok=True);self.temp=tempfile.TemporaryDirectory(dir=ROOT/'.test-tmp')
        self.g=Game(True,Path(self.temp.name)/'save.json')
    def tearDown(self):pg.quit();self.temp.cleanup()

    def frame(self,legacy):
        g=self.g;g.direct_touch_hud=not legacy
        if legacy:g.world_fits_display=lambda:False
        else:g.__dict__.pop('world_fits_display',None)
        g.render();return pg.image.tobytes(pg.display.get_surface(),'RGB')

    def test_direct_hud_and_window_drawing_match_the_composed_frame(self):
        for touch,width in ((True,1600),(True,1481),(False,1280)):
            g=self.g;g.save.data['touch_controls']=touch
            if touch:g.configure_viewport(width/720)
            for level in (0,23,44):
                g.load(*divmod(level,3));g.begin();g.tutorial_active=False;w=g.world
                for case in ('plain','flash','message','notice','boss'):
                    w.message_time=0;g.flash=0;g.notice_time=0
                    if case=='flash':g.flash=.15
                    if case=='message':w.say('Mensaje de prueba para el recuadro')
                    if case=='notice':g.notice='Aviso de prueba';g.notice_time=2
                    if case=='boss' and w.boss:w.boss.active=True;g.camera=w.width-g.viewport_width
                    self.assertEqual(self.frame(True),self.frame(False),(touch,width,level,case))
        self.assertIs(self.g.world_canvas,self.g.display)

    def test_resized_window_still_scales_from_its_own_world_canvas(self):
        g=self.g;g.load(0);g.begin();g.tutorial_active=False
        g.display=pg.display.set_mode((1600,900),pg.RESIZABLE);g.render()
        self.assertIs(g.world_canvas,g.offscreen_world)
        self.assertNotEqual(pg.display.get_surface().get_at((800,450))[:3],(0,0,0))

    def test_cached_skyline_blocks_match_the_drawn_rectangles(self):
        for stage in (0,1,2):
            for h in (48,77,100,163,209):
                for x in (3,3.4,57.99,812.5,1200.01):
                    drawn=pg.Surface((1500,720));drawn.fill((20,30,40));cached=drawn.copy()
                    argentina_art.skyline(drawn,stage,x,h)
                    cached.blit(argentina_art.skyline_block(stage,h),(int(x)-3,471-h))
                    self.assertEqual(pg.image.tobytes(drawn,'RGB'),pg.image.tobytes(cached,'RGB'),(stage,h,x))

    def test_platform_art_is_ready_before_it_enters_the_view(self):
        g=self.g;g.save.data['touch_controls']=True;g.configure_viewport(1480/720)
        for level in (3,9):
            g.load(*divmod(level,3));g.begin();g.tutorial_active=False;w=g.world;g.render()
            original=g.artist.scene;built=[]
            def scene(*args):
                before=period_art.tile.cache_info().misses;original(*args)
                built.append(period_art.tile.cache_info().misses-before)
            g.artist.scene=scene
            for camera in range(0,w.width-g.viewport_width,8):
                g.camera=camera;g.render()
            del g.artist.scene
            self.assertEqual(sum(built),0,level)

    def test_map_presentation_prepares_the_first_district(self):
        g=self.g;g.load(9);self.assertEqual(g.state,'intro')
        g.intro_time=1
        for _ in range(12):g.render()
        self.assertGreater(len(g.artist.prepared),3)


if __name__=='__main__':unittest.main(verbosity=2)
