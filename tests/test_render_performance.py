"""Shared drawing work must retain combat feedback and all collectible objects."""
import os
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'.vendor')]
os.environ.update(SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',PYGAME_HIDE_SUPPORT_PROMPT='1')
import pygame as pg
from crono.combat import Enemy
from crono.enemy_art import draw_enemy,enemy_picture
from crono.art import echo_image,glow,circle,PAPER
from crono.educational_art import pulse_image


class RenderPerformanceTests(unittest.TestCase):
    def setUp(self):
        pg.init();pg.display.set_mode((320,240));enemy_picture.cache_clear()
        self.surface=pg.Surface((400,240))

    def tearDown(self):pg.quit()

    def enemy(self,era=2):
        return Enemy(dict(x=180,y=160,left=100,right=260,kind='walker'),era)

    def pixels(self,e,t=.1):
        self.surface.fill((29,48,61));draw_enemy(self.surface,e,0,t,e.era,e.stage)
        return pg.image.tobytes(self.surface,'RGB')

    def test_identical_humanoids_share_a_cyclic_picture(self):
        a=self.enemy();b=self.enemy();a.time=b.time=.1
        expected=self.pixels(a);info=enemy_picture.cache_info()
        self.assertEqual(expected,self.pixels(b))
        self.assertEqual(enemy_picture.cache_info().misses,info.misses)
        b.time=.9
        self.assertEqual(expected,self.pixels(b,1000))
        self.assertEqual(enemy_picture.cache_info().misses,info.misses)

    def test_hit_direction_and_historical_variant_remain_visible(self):
        e=self.enemy();base=self.pixels(e)
        e.hit_flash=.15;self.assertNotEqual(base,self.pixels(e))
        e.hit_flash=0;e.direction=1;self.assertNotEqual(base,self.pixels(e))
        e.direction=-1;e.variant='roman';self.assertNotEqual(base,self.pixels(e))

    def test_argentine_factions_and_their_warning_threshold_are_distinct(self):
        e=Enemy(dict(x=180,y=160,left=100,right=260,kind='sentry',stage=2),7)
        e.timer=.45;base=self.pixels(e)
        e.timer=.3;self.assertNotEqual(base,self.pixels(e))
        e.timer=.45;e.faction='armed_cell';self.assertNotEqual(base,self.pixels(e))

    def test_offscreen_entities_do_not_generate_pictures(self):
        e=self.enemy();e.rect.x=3000;self.pixels(e)
        self.assertEqual(enemy_picture.cache_info().misses,0)
        e.rect.x=180;e.rect.y=-500;self.pixels(e)
        self.assertEqual(enemy_picture.cache_info().misses,0)
        self.assertEqual(enemy_picture.cache_info().maxsize,128)

    def test_cached_orbs_keep_their_original_glow_and_center(self):
        color=(116,237,219);reference=pg.Surface((80,80));reference.fill((29,48,61))
        glow(reference,(40,40),21,color);circle(reference,color,(40,40),5,1);circle(reference,PAPER,(40,40),2)
        result=pg.Surface((80,80));result.fill((29,48,61));result.blit(echo_image(color),(19,19))
        self.assertEqual(pg.image.tobytes(reference,'RGB'),pg.image.tobytes(result,'RGB'))
        self.assertIs(echo_image(color),echo_image(color))
        self.assertIs(pulse_image(color,1),pulse_image(color,1))


if __name__=='__main__':unittest.main(verbosity=2)
