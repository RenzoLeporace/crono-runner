"""Render QA screenshots and a contact sheet, then report render cost."""
import os
import sys
from pathlib import Path
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'.vendor')]
os.environ.update(SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',PYGAME_HIDE_SUPPORT_PROMPT='1')
import pygame as pg
from PIL import Image,ImageDraw
from crono.game import Game
from crono.physics import World

game=Game(True,ROOT/'.test-tmp'/'capture-save.json')
out=ROOT/'capturas'
out.mkdir(exist_ok=True)
game.time=8
images=[]
for state in ('menu','intro','chapters','help','pause','complete','ending'):
    game.state=state
    game.render()
    pg.image.save(game.canvas,str(out/f'{state}.png'))
for era in range(5):
    game.world=World(era)
    game.world.time=20
    game.state='play'
    game.camera=780
    game.world.player.rect.midbottom=(1250,490)
    game.world.player.grounded=True
    game.render()
    path=out/f'epoca_{era+1}.png'
    pg.image.save(game.canvas,str(path))
    images.append(Image.open(path).resize((640,360)))
sheet=Image.new('RGB',(1280,1080),(8,17,25))
for i,image in enumerate(images):
    sheet.paste(image,((i%2)*640,(i//2)*360))
sheet.save(out/'epocas.png')
start=time.perf_counter()
for i in range(240):
    game.camera=500+i*8
    game.time+=1/60
    game.render()
elapsed=time.perf_counter()-start
print(f'Render benchmark: {elapsed/240*1000:.2f} ms/frame ({240/elapsed:.0f} frames/s), offscreen 1280x720')
pg.quit()
