"""Deterministic dense-scene render timings, not a physical Android FPS test."""
import argparse
import json
import os
from pathlib import Path
import statistics
import sys
import tempfile
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'.vendor')]
os.environ.update(SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',PYGAME_HIDE_SUPPORT_PROMPT='1')
import pygame as pg
from crono.game import Game
from crono.combat import Enemy,Projectile


def benchmark():
    output={}
    (ROOT/'.test-tmp').mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(dir=ROOT/'.test-tmp') as folder:
        game=Game(True,Path(folder)/'save.json');game.configure_viewport(1600/720)
        for level in (0,6,21):
            for mobile in (False,True):
                game.load(*divmod(level,3));world=game.world;world.mobile_render=mobile
                world.enemies=[]
                kinds=('walker','hopper','flyer','sentry','charger','armored')
                for i in range(36):
                    x=130+(i*137)%1300
                    enemy=Enemy(dict(x=x,y=490,left=x-80,right=x+80,kind=kinds[i%6],stage=world.stage),world.combat_era)
                    world.enemies.append(enemy)
                world.data['echoes']=[(100+(i*53)%1400,300+(i*37)%180) for i in range(96)]
                world.projectiles=[Projectile(120+(i*63)%1350,360+(i*31)%140,220,owner='player' if i%2 else 'enemy',kind='orb') for i in range(36)]
                samples=[]
                for frame in range(360):
                    seconds=frame/60
                    for enemy in world.enemies:enemy.time=seconds
                    start=time.perf_counter();game.artist.scene(game.world_canvas,world,0,seconds)
                    if frame>=60:samples.append((time.perf_counter()-start)*1000)
                ordered=sorted(samples)
                output[f'{level}-'+('mobile' if mobile else 'desktop')]=dict(median_ms=round(statistics.median(samples),3),p95_ms=round(ordered[int(len(ordered)*.95)],3),p99_ms=round(ordered[int(len(ordered)*.99)],3),max_ms=round(max(samples),3))
        pg.quit()
    return output


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path)
    args=parser.parse_args();result=benchmark()
    if args.output:args.output.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))
