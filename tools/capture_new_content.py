"""Inspect Egypt, mixed humanoid rosters, cultural stops and navigation."""
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
from crono.combat import Enemy,ENEMY_NAMES
from crono.enemy_art import draw_enemy,FAMILY_NAMES
from crono.humanoid_roster import ROLES
from crono.art import text,PAPER,MUTED

out=ROOT/'capturas'/'novedades-0.6';out.mkdir(parents=True,exist_ok=True)
g=Game(True,ROOT/'.test-tmp'/'qa-novedades.json');g.time=9
g.save.data.update(unlocked=20,dlc_unlocked=23,age_band=1)
shots=[]
for stage in range(3):
    g.world=World(8,stage,difficulty=1)
    for zone in range(3):
        g.camera=g.world.data['zones'][zone][0]
        base=min((g.world.platforms[k].rect for k in g.world.data['main_nodes']),key=lambda r:abs(r.centerx-g.camera-400))
        g.world.player.rect.midbottom=(max(base.left+24,min(base.right-24,g.camera+400)),base.top)
        g.world.player.grounded=True;g.state='play';g.render()
        path=out/f'egipto-{stage+1}-{zone+1}.png';pg.image.save(g.canvas,str(path))
        shots.append(Image.open(path).resize((640,360)))
    g.state='intro';g.render();pg.image.save(g.canvas,str(out/f'egipto-intro-{stage+1}.png'))
    g.state='bestiary';g.render();pg.image.save(g.canvas,str(out/f'egipto-guia-{stage+1}.png'))
sheet=Image.new('RGB',(1920,1080))
for n,img in enumerate(shots):sheet.paste(img,((n%3)*640,(n//3)*360))
sheet.save(out/'egipto-distritos.png')
g.state='play';g.camera=g.world.width-1280;g.world.boss.active=True;g.world.boss.phase='warning'
g.world.shards={0,1,2};g.render();pg.image.save(g.canvas,str(out/'egipto-boss.png'))

sheet=pg.Surface((1280,1020));sheet.fill((13,26,37))
for row,era in enumerate((2,3,4,5,6,8)):
    y=40+row*161
    text(sheet,FAMILY_NAMES[era],(20,y),16,PAPER,True)
    for n,kind in enumerate(ENEMY_NAMES):
        x=295+n*160
        e=Enemy(dict(x=x,y=y+45,left=0,right=2000,kind=kind,stage=1),era)
        e.rect.bottom=y+103;e.time=.6
        draw_enemy(sheet,e,0,1,era,1)
        label=ROLES.get(era,{}).get(kind,ENEMY_NAMES[kind])
        text(sheet,label,(x+22,y+128),11,MUTED,False,'center')
pg.image.save(sheet,str(out/'humanoides-y-variedad.png'))
for key in ('lujan','itati','moses'):
    g.state='heritage';g.heritage_key=key;g.render();pg.image.save(g.canvas,str(out/f'patrimonio-{key}.png'))
    g.world=World(8,2) if key=='moses' else World(7,0)
    site=next(v for v in g.world.data['cultural_sites'] if v[2]==key)
    g.camera=site[0]-470;g.world.player.rect.midbottom=(site[0]-90,site[1]);g.world.player.grounded=True
    g.state='play';g.render();pg.image.save(g.canvas,str(out/f'visita-{key}.png'))
for state in ('menu','chapters','settings'):
    g.state=state;g.render();pg.image.save(g.canvas,str(out/f'{state}.png'))
g.edit_question(2000000);g.teacher_picker=True;g.render();pg.image.save(g.canvas,str(out/'map-picker-27.png'))
g.teacher_picker=False;g.state='question_edit';g.render();pg.image.save(g.canvas,str(out/'editor-egipto.png'))
g.world=World(8,2);g.state='play';samples=[]
for n in range(180):
    g.camera=g.world.data['zones'][2][0]+n*8
    start=time.perf_counter();g.render();samples.append((time.perf_counter()-start)*1000)
samples.sort();print(f'Egypt render: median {samples[90]:.2f}ms, p95 {samples[171]:.2f}ms')
pg.quit()
