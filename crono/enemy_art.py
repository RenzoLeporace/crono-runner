"""Eight silhouette families; historical creatures/objects transformed by the clock."""
import math
import pygame as pg
from .art import rect,line,circle,polygon,glow,text,mix,PAPER,INK,GOLD,W
from .visuals import palette_for

FAMILY_NAMES=('Reptiles del Cretácico','Fauna de la estepa','Hoplitas y bronce','Caballeros y ballesteros',
              'Autómatas y máquinas de vapor','Infantería y blindajes','Robots bípedos y drones','Argentina · figuras históricas',
              'Guardias del Nilo y criaturas de ficción')

def draw_enemy(s,e,camera,t,era,stage=0):
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
    if era==0:
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
