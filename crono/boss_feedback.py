"""Shared damage reaction for every guardian, including image-based bodies."""
import math
import pygame as pg
from .art import W,H,PAPER,GOLD,CYAN,circle,line,text

def draw(s,boss,camera,time,render_body):
    if not boss or (not boss.alive and boss.hit_reaction<=0):return
    x,y=boss.rect.centerx-camera,boss.rect.bottom
    if not -260<x<W+260:return
    layer=pg.Surface((W,H),pg.SRCALPHA)
    render_body(layer,boss,camera,time)
    remaining=boss.hit_reaction
    if remaining>0:
        duration=.65 if not boss.alive else .34
        progress=1-remaining/duration
        kick=round(math.sin(progress*math.pi*6)*7*(1-progress))
        recoil=round(math.sin(progress*math.pi)*6)
        if boss.alive:
            # One soft fading silhouette pulse; cached bodies no longer ignore hits.
            mask=pg.mask.from_surface(layer)
            flash=mask.to_surface(setcolor=(*PAPER,0),unsetcolor=(0,0,0,0))
            flash.fill((*PAPER,round(145*(1-progress))),special_flags=pg.BLEND_RGBA_MAX)
            flash.blit(layer,(0,0),special_flags=pg.BLEND_RGBA_MULT)
            layer.blit(flash,(0,0),special_flags=pg.BLEND_RGB_ADD)
        else:
            layer.set_alpha(round(255*(1-progress)))
        s.blit(layer,(kick,-recoil))
        color=GOLD if boss.alive else CYAN
        radius=18+progress*54
        circle(s,color,(x,y-78),radius,2)
        for n in range(8):
            a=n*math.tau/8+.2
            start=(x+math.cos(a)*(radius+4),y-78+math.sin(a)*(radius+4))
            end=(x+math.cos(a)*(radius+12),y-78+math.sin(a)*(radius+12))
            line(s,color,start,end,2)
        text(s,f'−{boss.last_damage}' if boss.alive else 'LIBERADO',(x,y-211-progress*26),21,color,True,'center')
    else:s.blit(layer,(0,0))
