"""Visual QA fixtures for the 15 maps, five guardians and educational overlays."""
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

out=ROOT/'capturas'/'educativa-0.4'
out.mkdir(parents=True,exist_ok=True)
game=Game(True,ROOT/'.test-tmp'/'qa-educativa.json')
game.save.data.update(unlocked=14,knowledge=13,discovered=list(range(30)),solved=[0,1,2,3],upgrades=['vitality','shield'])
game.time=5
maps=[]
for level_id in range(15):
    era,stage=divmod(level_id,3)
    game.world=World(era,stage,['vitality','shield'],[0,1,2,3])
    game.camera=600
    game.world.time=26
    game.world.player.rect.midbottom=(1080,584)
    game.world.player.grounded=True
    game.state='play'
    game.render()
    path=out/f'mapa-{era+1}-{stage+1}.png'
    pg.image.save(game.canvas,str(path))
    maps.append(Image.open(path).resize((426,240)))
sheet=Image.new('RGB',(1278,1200))
for i,img in enumerate(maps):
    sheet.paste(img,((i%3)*426,(i//3)*240))
sheet.save(out/'15-mapas.png')
guardians=[]
for era in range(5):
    game.world=World(era,2)
    game.world.shards={0,1,2}
    game.world.player.rect.midbottom=(4740,584)
    game.world.player.grounded=True
    game.world.boss.active=True
    game.world.boss.phase='exposed'
    game.world.boss.timer=1
    game.camera=game.world.width-1280
    game.render()
    path=out/f'guardian-{era+1}.png'
    pg.image.save(game.canvas,str(path))
    guardians.append(Image.open(path).resize((640,360)))
sheet=Image.new('RGB',(1280,1080),(8,17,25))
for i,img in enumerate(guardians):
    sheet.paste(img,((i%2)*640,(i//2)*360))
sheet.save(out/'5-guardianes.png')
game.world=World(0)
game.camera=0
game.world.player.rect.midbottom=(220,584)
game.world.player.grounded=True
for state in ('menu','workshop','notebook','bestiary','chapters','intro','play','pause','settings','teacher'):
    game.state=state
    game.render()
    pg.image.save(game.canvas,str(out/f'{state}.png'))
game.quiz_topic=0
game.question=game.bank.choose(0,1)
game.state='quiz'
for mode in ('read','question','correct','wrong'):
    game.quiz_mode=mode
    game.render()
    pg.image.save(game.canvas,str(out/f'quiz-{mode}.png'))

game.edit_question(0)
game.render()
pg.image.save(game.canvas,str(out/'question_edit.png'))
game.teacher_picker=True
game.render()
pg.image.save(game.canvas,str(out/'map_picker.png'))
game.teacher_picker=False
game.preview_level=2
game.change_scenario(0)
game.state='scenarios'
game.render()
pg.image.save(game.canvas,str(out/'scenarios.png'))
game.state='play'
start=time.perf_counter()
for i in range(240):
    game.camera=300+i*9
    game.time+=1/60
    game.render()
elapsed=time.perf_counter()-start
print(f'Educational render: {elapsed/240*1000:.2f} ms/frame ({240/elapsed:.0f} fps) offscreen')
pg.quit()
