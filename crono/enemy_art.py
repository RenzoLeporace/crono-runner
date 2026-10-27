"""Eight silhouette families; historical creatures/objects transformed by the clock."""
import math
from functools import lru_cache
from types import SimpleNamespace
import pygame as pg
from .art import rect,line,circle,polygon,glow,text,mix,PAPER,INK,GOLD,W
from .visuals import palette_for

FAMILY_NAMES=('Reptiles del Cretácico','Fauna de la estepa','Hoplitas y bronce','Caballeros y ballesteros',
              'Guardias y máquinas de vapor','Infantería y blindajes','Vigilantes y drones','Argentina · figuras históricas',
              'Guardias del Nilo y criaturas de ficción')

def _draw_enemy(s,e,camera,t,era,stage=0):
    if not e.alive:
        return
    x,y=e.rect.centerx-camera,e.rect.bottom
    if not -90<x<W+90:
        return
    from .humanoid_roster import humanoid
    if humanoid(era,e.kind):
        from .humanoid_art import draw_humanoid
        draw_humanoid(s,e,camera,t,stage)
        return
    if era==8:
        from .humanoid_art import draw_egypt_creature
        draw_egypt_creature(s,e,camera,t)
        return
    pal=palette_for(era,stage);d=e.direction
    accent=pal.accent;dark=pal.rock
    body=mix(pal.top,pal.near,.45)
    gait=math.sin(t*10+e.left)*4
    def ellipse(color,box,width=0):
        pg.draw.ellipse(s,color,pg.Rect(*box),width)
    if e.kind=='flyer' and era in (4,5):
        if era==4:
            ellipse((161,132,87),(x-39,y-65,78,39));line(s,dark,(x-22,y-29),(x-13,y-5),2);line(s,dark,(x+22,y-29),(x+13,y-5),2)
            rect(s,(98,75,53),(x-16,y-9,32,13),3)
        else:
            polygon(s,(140,154,136),[(x-49,y-21),(x-12,y-29),(x-4,y-53),(x+7,y-53),(x+13,y-30),(x+51,y-18),(x+14,y-12),(x+8,y+4),(x-7,y+4),(x-14,y-13)])
            line(s,PAPER,(x-12,y-42),(x+13,y-42),2);circle(s,(48,63,66),(x,y-28),5)
        return
    if era==0:
        body=((194,117,67),(97,120,169),(91,154,170))[stage%3];accent=(249,210,134);dark=(44,35,44)
        # Raptors stand on two legs; armored animals have low shells.
        if e.kind=='flyer':
            for side in (-1,1):
                polygon(s,body,[(x,y-20),(x+side*51,y-49+gait),(x+side*22,y-19),(x+side*8,y-7)])
            polygon(s,accent,[(x+12*d,y-24),(x+43*d,y-19),(x+12*d,y-14)])
        else:
            ellipse(body,(x-22,y-36,43,25))
            polygon(s,body,[(x-16*d,y-28),(x-54*d,y-40),(x-27*d,y-12)])
            rect(s,body,(x+8*d-7,y-49,29,22),5)
            for side in (-1,1):
                line(s,dark,(x+side*9,y-15),(x+side*17+gait,y-2),6)
            if e.kind=='sentry':
                for side in (-1,1):
                    polygon(s,accent,[(x+10*d,y-29),(x+side*33,y-56),(x+side*22,y-14)])
            if e.kind=='armored':
                ellipse(body,(x-32,y-40,63,30))
                for dx in (-22,0,22):
                    polygon(s,accent,[(x+dx-6,y-34),(x+dx,y-49),(x+dx+7,y-34)])
            if e.kind=='charger':
                polygon(s,PAPER,[(x+24*d,y-46),(x+41*d,y-57),(x+31*d,y-36)])
    elif era==1:
        fur=(181,191,185)
        if e.kind=='flyer':
            for side in (-1,1):
                polygon(s,fur,[(x,y-24),(x+side*40,y-47+gait),(x+side*49,y-13),(x,y-9)])
            circle(s,fur,(x,y-27),13)
            for dx in (-6,6):circle(s,accent,(x+dx,y-29),3)
        else:
            ellipse(fur,(x-29,y-37,56,30))
            for dx in (-21,-9,12,23):line(s,dark,(x+dx,y-16),(x+dx+gait,y),5)
            circle(s,fur,(x+d*26,y-32),13)
            polygon(s,fur,[(x+d*19,y-40),(x+d*18,y-57),(x+d*29,y-40)])
            if e.kind in ('charger','armored'):
                for dy in (0,7):line(s,PAPER,(x+d*32,y-24+dy),(x+d*40,y-7+dy),3)
            if e.kind=='armored':
                ellipse((118,136,144),(x-30,y-43,57,35))
                line(s,fur,(x+d*33,y-30),(x+d*45,y-3),9)
    elif era==2:
        bronze=(184,139,75)
        if e.kind=='flyer':
            for side in (-1,1):
                polygon(s,bronze,[(x,y-13),(x+side*42,y-45+gait),(x+side*32,y-4)])
            circle(s,bronze,(x,y-28),12)
        elif e.kind=='hopper':
            ellipse(bronze,(x-23,y-24,44,21))
            for side in (-1,1):
                for j in range(3):line(s,bronze,(x+side*14,y-15),(x+side*(27+j*4),y-4+j*3),3)
            line(s,bronze,(x-22,y-18),(x-33,y-48),6)
            circle(s,accent,(x-33,y-49),4)
        else:
            polygon(s,bronze,[(x-18,y-39),(x+18,y-39),(x+12,y-12),(x-11,y-12)])
            for side in (-1,1):line(s,dark,(x+side*9,y-13),(x+side*12+gait,y),6)
            rect(s,bronze,(x-12,y-58,24,22),3)
            polygon(s,(174,79,58),[(x-13,y-58),(x-8,y-70),(x+15,y-65),(x+11,y-58)])
            ellipse(accent,(x-d*30,y-39,25,31),3)
            line(s,bronze,(x+d*26,y-6),(x+d*26,y-66),3)
            if e.kind=='sentry':polygon(s,accent,[(x+d*26,y-67),(x+d*34,y-56),(x+d*18,y-56)])
    elif era==3:
        steel=(145,158,170)
        if e.kind=='flyer':
            for side in (-1,1):
                polygon(s,dark,[(x,y-15),(x+side*44,y-51+gait),(x+side*35,y-11),(x+side*13,y)])
            polygon(s,accent,[(x+10*d,y-30),(x+30*d,y-24),(x+10*d,y-20)])
        elif e.kind=='sentry':
            rect(s,(115,85,69),(x-23,y-29,46,21))
            for side in (-1,1):line(s,dark,(x+side*12,y-8),(x+side*20,y),5)
            line(s,steel,(x-d*30,y-52),(x+d*28,y-21),5)
            pg.draw.arc(s,accent,(int(x-32),int(y-56),62,37),0,math.pi,3)
        elif e.kind in ('charger','hopper'):
            ellipse((117,112,104),(x-30,y-32,59,29))
            for dx in (-19,18):line(s,dark,(x+dx,y-11),(x+dx+gait,y),6)
            polygon(s,PAPER,[(x+d*23,y-22),(x+d*39,y-33),(x+d*30,y-16)])
        else:
            rect(s,steel,(x-18,y-43,36,31),5)
            rect(s,dark,(x-13,y-64,26,27),3)
            rect(s,steel,(x-10,y-51,21,5))
            for side in (-1,1):line(s,steel,(x+side*10,y-14),(x+side*13+gait,y),7)
            polygon(s,accent,[(x-34,y-35),(x-18,y-35),(x-18,y-15),(x-27,y-7),(x-35,y-17)])
    elif era==4:
        brass=(186,129,73)
        rect(s,brass,(x-24,y-43,48,32),6)
        for side in (-1,1):
            circle(s,dark,(x+side*17,y-9),11)
            circle(s,accent,(x+side*17,y-9),7,2)
        rect(s,dark,(x-10,y-63,14,25))
        for j in range(3):circle(s,pal.far,(x+j*7,y-71-j*9),5+j*2)
        circle(s,accent,(x,y-29),11,3)
        if e.kind=='flyer':
            line(s,dark,(x,y-61),(x,y-80),3)
            line(s,accent,(x-38,y-79+gait),(x+38,y-79-gait),5)
        if e.kind=='hopper':
            for side in (-1,1):
                line(s,brass,(x+side*18,y-15),(x+side*32,y-2),4)
        if e.kind=='armored':rect(s,accent,(x-30,y-46,61,12),2)
    elif era==5:
        # Unmanned fictional clock anomalies, no human or national uniform.
        olive=(129,140,113)
        ellipse(dark,(x-33,y-20,66,22))
        for dx in range(-23,28,12):circle(s,(166,173,151),(x+dx,y-9),5,2)
        polygon(s,olive,[(x-29,y-20),(x-17,y-45),(x+22,y-45),(x+33,y-20)])
        rect(s,dark,(x-7,y-60,24,20),3)
        line(s,olive,(x+7,y-51),(x+45*d,y-51),7)
        if e.kind=='flyer':
            polygon(s,olive,[(x-55,y-25),(x,y-48),(x+55,y-25),(x+7,y-19),(x,y-7),(x-7,y-19)])
        if e.kind=='hopper':
            for side in (-1,1):line(s,olive,(x+side*23,y-16),(x+side*39,y+2),5)
    elif era==6:
        shell=(114,183,194)
        polygon(s,shell,[(x-25,y-36),(x-15,y-48),(x+16,y-48),(x+27,y-33),(x+14,y-16),(x-13,y-16)])
        circle(s,dark,(x,y-32),13);circle(s,accent,(x,y-32),7)
        for side in (-1,1):
            if e.kind=='flyer':
                line(s,dark,(x+side*20,y-35),(x+side*40,y-49),5)
                ellipse(accent,(x+side*40-14,y-54,28,9),2)
            else:
                for j in (0,1):
                    line(s,shell,(x+side*(11+j*7),y-22),(x+side*(25+j*7),y-8),4)
                    line(s,dark,(x+side*(25+j*7),y-8),(x+side*(19+j*9)+gait,y),4)
        if e.kind=='armored':circle(s,accent,(x,y-32),29,3)
    else:
        from .argentina_enemies import draw_human
        draw_human(s,e,camera,t)
        return
    # Shared combat language leaves the silhouettes intact.
    if e.kind=='armored':
        for dx in (-16,0,16):polygon(s,accent,[(x+dx-4,y-60),(x+dx,y-69),(x+dx+4,y-60)])
    if e.kind in ('sentry','flyer') and e.timer<.5:glow(s,(x,y-45),30,accent)
    if e.kind=='charger' and e.mode=='warning':text(s,'!',(x,y-84),20,GOLD,True,'center')
    if e.max_hp>1:
        for n in range(e.max_hp):circle(s,accent if n<e.hp else dark,(x+(n-(e.max_hp-1)/2)*8,y-78),2)
    if e.hit_flash:circle(s,PAPER,(x,y-26),26,2)


@lru_cache(maxsize=128)
def enemy_picture(era,stage,kind,variant,faction,frame,human,direction,mode,timer,hp,max_hp,hit,label,moving):
    # Identical enemies share a bounded cyclic frame cache. Absolute game time
    # used to invalidate every enemy's mask at once, twelve times per second.
    # Cropping also avoids blending a mostly transparent 210x180 rectangle.
    origin=180 if label else 105
    proxy=SimpleNamespace(rect=pg.FRect(origin-22,100,44,50),alive=True,era=era,stage=stage,
        kind=kind,variant=variant,faction=faction,left=0,time=frame/10,direction=direction,
        mode=mode,timer=(.3,.45,1.)[timer],hp=hp,max_hp=max_hp,hit_flash=hit,
        show_label=label,speed=1 if moving else 0)
    draw_time=frame*math.tau/16/(9 if era==8 else 10)
    picture=pg.Surface((origin*2,180),pg.SRCALPHA)
    _draw_enemy(picture,proxy,0,draw_time,era,stage)
    bounds=picture.get_bounding_rect(min_alpha=1).inflate(4,4).clip(picture.get_rect())
    picture=picture.subsurface(bounds)
    mask=pg.mask.from_surface(picture,120)
    dark=mask.to_surface(setcolor=(20,30,38,255),unsetcolor=(0,0,0,0))
    light=mask.to_surface(setcolor=(245,218,160,255),unsetcolor=(0,0,0,0))
    outlined=pg.Surface(picture.get_size(),pg.SRCALPHA)
    for dx,dy in ((-2,0),(2,0),(0,-2),(0,2),(-2,-2),(2,2),(-2,2),(2,-2)):outlined.blit(dark,(dx,dy))
    for dx,dy in ((-1,0),(1,0),(0,-1),(0,1)):outlined.blit(light,(dx,dy))
    outlined.blit(picture,(0,0))
    from .art import display_alpha
    return display_alpha(outlined,True),(bounds.x-origin,bounds.y-150)


def draw_enemy(s,e,camera,t,era,stage=0):
    x,y=e.rect.centerx-camera,e.rect.bottom
    if not e.alive or not -190<x<s.get_width()+190 or y<-45 or y>s.get_height()+155:return
    from .humanoid_roster import humanoid
    human=humanoid(era,e.kind) or era==7
    moving=abs(e.speed)>0
    if human:
        frame=int(e.time*10)%8 if e.kind!='sentry' and (moving if era==7 else e.mode!='warning') else 0
    else:
        angle=t*9 if era==8 else t*10+e.left
        frame=round(angle*16/math.tau)%16
    timer,mode,label,cache_moving=visible_state(e,era,human,moving)
    picture,offset=enemy_picture(era,stage,e.kind,getattr(e,'variant',''),getattr(e,'faction',''),
        frame,human,e.direction,mode,timer,e.hp,e.max_hp,bool(e.hit_flash),label,cache_moving)
    s.blit(picture,(round(x)+offset[0],round(y)+offset[1]))


def visible_state(enemy,era,human,moving):
    """Do not regenerate outlines for a timer/mode that changes no pixels.

    The Argentina musket warns below .4 s; other visible ranged warnings use
    .5 s. Keep those distinctions, while a walker's countdown is invisible.
    """
    if era==7:warning=enemy.kind=='sentry' and enemy.timer<.4
    elif human:warning=enemy.kind=='sentry' and enemy.timer<.5
    elif era==8:warning=enemy.timer<.5
    else:warning=enemy.kind in ('sentry','flyer') and not (enemy.kind=='flyer' and era in (4,5)) and enemy.timer<.5
    timer=0 if warning else 2
    mode='warning' if enemy.mode=='warning' else 'patrol'
    return timer,mode,getattr(enemy,'show_label',False) if era==7 else False,moving if era==7 else False
