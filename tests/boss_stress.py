"""Reproducible guardian render benchmark; native SDL, not Android FPS."""
import os,sys,time,json,tempfile,statistics,argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'.vendor')]
os.environ.update(SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',PYGAME_HIDE_SUPPORT_PROMPT='1')
import pygame as pg
from crono.game import Game
from crono.educational_art import boss_art

def benchmark():
    (ROOT/'.test-tmp').mkdir(exist_ok=True);result={}
    with tempfile.TemporaryDirectory(dir=ROOT/'.test-tmp') as folder:
        game=Game(True,Path(folder)/'save.json');game.configure_viewport(1600/720)
        for level in (2,11,23,26,29,48):
            game.load(*divmod(level,3));boss=game.world.boss;boss.active=True
            camera=boss.rect.centerx-1100
            for damage in (False,True):
                samples=[]
                for frame in range(240):
                    boss.phase='attack' if frame%120<60 else 'exposed'
                    boss.hit_reaction=.34-(frame%18)/60 if damage else 0
                    boss.hit_flash=.1 if damage and frame%18<8 else 0;boss.last_damage=1
                    game.world_canvas.fill((26,43,56))
                    start=time.perf_counter();boss_art(game.world_canvas,boss,camera,frame/60)
                    if frame>=60:samples.append((time.perf_counter()-start)*1000)
                result[f'{level}-'+('hit' if damage else 'normal')]=dict(median_ms=round(statistics.median(samples),3),p95_ms=round(sorted(samples)[int(len(samples)*.95)],3))
    pg.quit();return result

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path);args=parser.parse_args()
    result=benchmark()
    if args.output:args.output.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))
