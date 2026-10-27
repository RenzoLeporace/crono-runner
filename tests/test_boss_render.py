"""Damage feedback uses bounded local art and keeps world warnings live."""
import os,sys,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'.vendor')]
os.environ.update(SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',PYGAME_HIDE_SUPPORT_PROMPT='1')
import pygame as pg
from crono.physics import World
from crono.educational_art import boss_art
from crono.boss_feedback import body_image

class BossRenderTests(unittest.TestCase):
    def setUp(self):pg.init();pg.display.set_mode((1600,720));body_image.cache_clear();self.surface=pg.Surface((1600,720))
    def tearDown(self):pg.quit()
    def draw(self,boss,camera):
        self.surface.fill((23,43,57));boss_art(self.surface,boss,camera,.4)
        return pg.image.tobytes(self.surface,'RGB')
    def test_wide_screen_damage_does_not_make_a_fullscreen_mask(self):
        boss=World(0,2).boss;boss.active=True;boss.phase='exposed';camera=boss.rect.centerx-1370
        normal=self.draw(boss,camera)
        self.assertNotEqual(self.surface.get_at((1370,round(boss.rect.bottom-78)))[:3],(23,43,57))
        boss.hit(1)
        with patch('pygame.mask.from_surface',side_effect=AssertionError('Full-screen damage mask')):hurt=self.draw(boss,camera)
        self.assertNotEqual(normal,hurt)
        boss.hit_flash=0;boss.hp=1;boss.hit(1);self.assertNotEqual(hurt,self.draw(boss,camera))
    def test_cached_guardian_does_not_freeze_attack_warnings(self):
        boss=World(6,2).boss;boss.active=True;boss.phase='attack';camera=boss.rect.centerx-1100
        boss.telegraphs=[[camera+400,1]];before=self.draw(boss,camera);misses=body_image.cache_info().misses
        boss.telegraphs=[[camera+700,.5]];after=self.draw(boss,camera)
        self.assertNotEqual(before,after);self.assertEqual(body_image.cache_info().misses,misses)
        self.assertEqual(body_image.cache_info().maxsize,128)

if __name__=='__main__':unittest.main(verbosity=2)
