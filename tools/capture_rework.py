"""Full-size landmark review and frame times across all 21 renewed maps."""
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
out=ROOT/'capturas'/'rework-0.6';out.mkdir(parents=True,exist_ok=True)
g=Game(True,ROOT/'.test-tmp'/'qa-rework.json');g.time=11
shots=[];stats=[]
for era in range(7):
    for stage in range(3):
        g.world=World(era,stage,difficulty=1);g.state='play';g.world.time=30
        for district in range(3):
            g.camera=g.world.data['zones'][district][0]
            base=min((g.world.platforms[k].rect for k in g.world.data['main_nodes']),key=lambda r:abs(r.centerx-g.camera-400))
            g.world.player.rect.midbottom=(max(base.left+24,min(base.right-24,g.camera+400)),base.top)
            g.world.player.grounded=True;g.render()
            path=out/f'mapa-{era+1}-{stage+1}-zona-{district+1}.png';pg.image.save(g.canvas,str(path))
            if district==2:shots.append(Image.open(path).resize((640,360)))
        samples=[]
        for n in range(60):
            g.camera+=10;g.time+=1/60
            start=time.perf_counter();g.render();samples.append((time.perf_counter()-start)*1000)
        samples.sort();stats.append((era,stage,samples[30],samples[57]))
sheet=Image.new('RGB',(1920,2520))
for n,img in enumerate(shots):sheet.paste(img,((n%3)*640,(n//3)*360))
sheet.save(out/'21-escenarios-renovados.png')
for era,stage,median,p95 in stats:print(f'Map {era+1}.{stage+1}: median {median:.2f}ms p95 {p95:.2f}ms')
pg.quit()
