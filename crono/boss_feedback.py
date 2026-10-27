"""Shared damage reaction for every guardian, including image-based bodies."""
import math
from functools import lru_cache
from types import SimpleNamespace
import pygame as pg
from .art import PAPER,GOLD,CYAN,circle,line,text


@lru_cache(maxsize=128)
def body_image(render_body,era,variant,phase,direction,hit,alive,width,height,frame,rate,steps):
    # Guardian art is local: no full-viewport allocation or mask on damage.
    boss=SimpleNamespace(era=era,variant=variant,phase=phase,direction=direction,
        hit_flash=hit,alive=alive,hit_reaction=.1,telegraphs=[],aim_warning=0,aim_target=None,
        rect=pg.FRect(280-width/2,340-height,width,height))
    layer=pg.Surface((560,380),pg.SRCALPHA)
    render_body(layer,boss,0,frame*math.tau/steps/rate if rate else 0)
    bounds=layer.get_bounding_rect(min_alpha=1).inflate(6,6).clip(layer.get_rect())
    image=layer.subsurface(bounds).copy()
    flash=image.copy();flash.fill((85,85,85),special_flags=pg.BLEND_RGB_ADD)
    return image,flash,(bounds.x-280,bounds.y-340)


def animation_phase(boss,time):
    variant=getattr(boss,'variant','')
    if variant:
        rate,steps=(0,1) if variant in ('naval','battery','lighthouse','train','hospital','malvinas','andes','volcano') else (1,48)
    else:rate,steps=(5,16) if boss.era==3 else (.7,48) if boss.era==6 else (0,1)
    return round(time*rate*steps/math.tau)%steps,rate,steps

def draw(s,boss,camera,time,render_body):
    if not boss or (not boss.alive and boss.hit_reaction<=0):return
    x,y=boss.rect.centerx-camera,boss.rect.bottom
    if not -280<x<s.get_width()+280:return
    frame,rate,steps=animation_phase(boss,time)
    layer,flash,offset=body_image(render_body,boss.era,getattr(boss,'variant',''),boss.phase,
        boss.direction,bool(boss.hit_flash),boss.alive,boss.rect.w,boss.rect.h,frame,rate,steps)
    position=(round(x+offset[0]),round(y+offset[1]))
    remaining=boss.hit_reaction
    if remaining>0:
        duration=.65 if not boss.alive else .34
        progress=1-remaining/duration
        kick=round(math.sin(progress*math.pi*6)*7*(1-progress))
        recoil=round(math.sin(progress*math.pi)*6)
        if boss.alive:
            layer.set_alpha(255)
            s.blit(layer,(position[0]+kick,position[1]-recoil))
            flash.set_alpha(round(145*(1-progress)))
            s.blit(flash,(position[0]+kick,position[1]-recoil))
        else:
            layer.set_alpha(round(255*(1-progress)))
            s.blit(layer,(position[0]+kick,position[1]-recoil))
        color=GOLD if boss.alive else CYAN
        radius=18+progress*54
        circle(s,color,(x,y-78),radius,2)
        for n in range(8):
            a=n*math.tau/8+.2
            start=(x+math.cos(a)*(radius+4),y-78+math.sin(a)*(radius+4))
            end=(x+math.cos(a)*(radius+12),y-78+math.sin(a)*(radius+12))
            line(s,color,start,end,2)
        text(s,f'−{boss.last_damage}' if boss.alive else 'LIBERADO',(x,y-211-progress*26),21,color,True,'center')
    else:
        layer.set_alpha(255);s.blit(layer,position)
