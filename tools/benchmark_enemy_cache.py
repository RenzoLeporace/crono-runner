"""Measure dense enemy rendering with changing timers; SDL timings, not phone FPS."""
import argparse,json,os,statistics,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'.vendor')]
os.environ.update(SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',PYGAME_HIDE_SUPPORT_PROMPT='1')
import pygame as pg
from crono.combat import Enemy
from crono.enemy_art import draw_enemy,enemy_picture

def benchmark():
    pg.init();s=pg.display.set_mode((1600,720));output={}
    for era in (0,3,6,7):
        enemy_picture.cache_clear();enemies=[]
        for n in range(36):
            x=80+(n*131)%1400
            e=Enemy(dict(x=x,y=430,left=x-30,right=x+160,kind=('walker','hopper','flyer','sentry','charger','armored')[n%6],stage=0),era)
            e.direction=(-1,1)[n%2];e.variant='berlin' if era==6 else '';e.show_label=era==7 and n%4==0
            enemies.append(e)
        samples=[]
        for frame in range(360):
            t=frame/60;s.fill((24,39,47))
            for n,e in enumerate(enemies):
                e.time=t;e.timer=(t+n*.053)%2.4
                e.mode='warning' if e.kind=='charger' and frame%120<20 else 'charge' if e.kind=='charger' and frame%120<50 else 'patrol'
            start=time.perf_counter()
            for e in enemies:draw_enemy(s,e,0,t,era,0)
            if frame>=60:samples.append((time.perf_counter()-start)*1000)
        output[str(era)]=dict(median_ms=round(statistics.median(samples),3),p95_ms=round(sorted(samples)[285],3),misses=enemy_picture.cache_info().misses,hits=enemy_picture.cache_info().hits)
    pg.quit();return output

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);a=p.parse_args();result=benchmark()
    if a.output:a.output.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))
