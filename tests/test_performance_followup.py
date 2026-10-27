"""Cache keys may omit only state that makes no visual difference."""
import os,sys,unittest,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'.vendor')]
os.environ.update(SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',PYGAME_HIDE_SUPPORT_PROMPT='1')
import pygame as pg
from crono.combat import Enemy
from crono.enemy_art import draw_enemy,enemy_picture
from crono.humanoid_roster import humanoid

class EnemyCacheStateTests(unittest.TestCase):
    def setUp(self):
        pg.init();pg.display.set_mode((640,600));enemy_picture.cache_clear()
        from crono.art import font,rendered_text
        font.cache_clear();rendered_text.cache_clear()
    def tearDown(self):pg.quit()
    def test_normalized_state_matches_original_pixels_and_preserves_warnings(self):
        surface=pg.Surface((640,600));expected=surface.copy()
        for era in range(9):
            for kind in ('walker','hopper','flyer','sentry','charger','armored'):
                e=Enemy(dict(x=300,y=430,left=280,right=600,kind=kind,stage=0),era)
                e.time=.6;e.show_label=True;e.variant='berlin' if era==6 else 'timbuktu' if era==3 else ''
                human=humanoid(era,e.kind) or era==7
                for mode in ('patrol','charge','warning'):
                    e.mode=mode
                    for timer in (.3,.45,.8):
                        e.timer=timer;moving=abs(e.speed)>0
                        if human:frame=int(e.time*10)%8 if e.kind!='sentry' and (moving if era==7 else e.mode!='warning') else 0
                        else:frame=round((.6*9 if era==8 else .6*10+e.left)*16/math.tau)%16
                        old_timer=0 if timer<.4 else 1 if timer<.5 else 2
                        picture,offset=enemy_picture(era,0,e.kind,e.variant,e.faction,frame,human,e.direction,mode,old_timer,e.hp,e.max_hp,False,True,moving)
                        expected.fill((18,34,43));expected.blit(picture,(round(e.rect.centerx)+offset[0],round(e.rect.bottom)+offset[1]))
                        surface.fill((18,34,43));draw_enemy(surface,e,0,.6,era,0)
                        self.assertEqual(pg.image.tobytes(surface,'RGB'),pg.image.tobytes(expected,'RGB'),(era,kind,mode,timer))
    def test_invisible_walker_timer_does_not_rebuild_a_mask(self):
        e=Enemy(dict(x=300,y=430,left=280,right=600,kind='walker',stage=0),0);surface=pg.Surface((640,600))
        for timer in (.3,.45,.8):e.timer=timer;draw_enemy(surface,e,0,.6,0,0)
        self.assertEqual(enemy_picture.cache_info().misses,1);self.assertEqual(enemy_picture.cache_info().maxsize,128)

if __name__=='__main__':unittest.main()
