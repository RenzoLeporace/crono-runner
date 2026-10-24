"""Review nine districts, historical enemy models and the final Argentine arena."""
import os
from pathlib import Path
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'.vendor')]
os.environ.update(SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',PYGAME_HIDE_SUPPORT_PROMPT='1')
import pygame as pg
from PIL import Image
from crono.game import Game
from crono.physics import World
from crono.combat import Enemy
from crono.art import text,PAPER,MUTED
from crono.argentina_enemies import draw_human

out=ROOT/'capturas'/'argentina-0.6';out.mkdir(parents=True,exist_ok=True)
g=Game(True,ROOT/'.test-tmp'/'qa-argentina.json');g.time=8
g.save.data.update(age_band=1,unlocked=20,dlc_unlocked=23)
shots=[]
names=(('1810-calles','1810-recova','1810-cabildo'),('1816-entrada','1816-patios','1816-casa'),('1983-calles','1983-barrios','1983-congreso'))
for stage in range(3):
    g.world=World(7,stage,difficulty=1)
    cameras=(300,g.world.data['zones'][1][0],g.world.data['zones'][2][0] if stage<2 else g.world.width-1280)
    for camera,name in zip(cameras,names[stage]):
        g.camera=camera
        p=min((g.world.platforms[k].rect for k in g.world.data['main_nodes']),key=lambda r:abs(r.centerx-camera-450))
        g.world.player.rect.midbottom=(max(p.left+24,min(p.right-24,camera+450)),p.top)
        g.world.player.grounded=True;g.state='play';g.render()
        path=out/f'{name}.png';pg.image.save(g.canvas,str(path))
        shots.append(Image.open(path).resize((640,360)))
    g.state='intro';g.render();pg.image.save(g.canvas,str(out/f'intro-{stage}.png'))
    g.state='bestiary';g.render();pg.image.save(g.canvas,str(out/f'guia-{stage}.png'))
sheet=Image.new('RGB',(1920,1080))
for n,img in enumerate(shots):sheet.paste(img,((n%3)*640,(n//3)*360))
sheet.save(out/'9-distritos.png')
g.state='play';g.camera=g.world.width-1280
g.world.shards={0,1,2};g.world.boss.active=True;g.world.boss.phase='warning'
g.world.player.rect.midbottom=(g.world.boss.left+180,584)
g.render();pg.image.save(g.canvas,str(out/'1983-guardian.png'))

sheet=pg.Surface((1280,720));sheet.fill((15,26,36))
rows=((0,'royalist','Realistas · 1810'),(1,'royalist','Realistas · 1816'),(2,'state_force','Militares · ecos del pasado'),(2,'armed_cell','Células terroristas · ecos del pasado'))
for row,(stage,faction,label) in enumerate(rows):
    y=45+row*168
    text(sheet,label,(20,y+10),16,PAPER,True)
    for n,kind in enumerate(('walker','hopper','sentry','charger','armored')):
        x=372+n*175
        e=Enemy(dict(x=x,y=y+105,left=0,right=2000,kind=kind,stage=stage,faction=faction),7)
        e.rect.bottom=y+118;e.time=1
        draw_human(sheet,e,0,1)
        text(sheet,('Patrulla','Saltador','Tirador','Carga','Protección')[n],(x+22,y+143),12,MUTED,False,'center')
pg.image.save(sheet,str(out/'adversarios-argentinos.png'))

g.world=World(7,0);g.state='play';g.camera=300
samples=[]
for tick in range(180):
    g.camera+=14;g.time+=1/60
    start=time.perf_counter();g.render();samples.append((time.perf_counter()-start)*1000)
samples.sort()
print(f'Argentina render: median {samples[len(samples)//2]:.2f} ms, p95 {samples[int(len(samples)*.95)]:.2f} ms')
pg.quit()
