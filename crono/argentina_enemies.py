"""Animated historical-inspired humans; no real named people or organizations."""
from functools import lru_cache
import math
import pygame as pg
from .art import text,circle,glow,PAPER,GOLD,CYAN
from .argentina_art import Painter
from .argentina_history import role_for

@lru_cache(maxsize=160)
def soldier_image(stage,faction,kind,frame,warning):
    p=Painter(100,112);x=48;y=104
    skin=(195,148,110);shade=(119,91,72);metal=(154,159,150)
    gait=math.sin(frame*math.tau/8)*5
    old=stage<2
    covert=faction=='armed_cell'
    coat=(40,65,87) if old else (66,83,63) if not covert else (67,65,64)
    trouser=(204,198,173) if old else (71,82,63) if not covert else (104,98,79)
    boots=(34,37,37);red=(151,56,43);brass=(198,164,94)
    # Shadow, separate knees and boots make the walk cycle readable.
    p.e((14,23,29,75),(22,y-3,54,7))
    for side in (-1,1):
        hip=x+side*7;knee=hip+side*gait*.75;ankle=hip-side*gait
        p.l(mix_color(trouser,.7),(hip,y-30),(knee,y-16),8)
        p.l(trouser,(knee,y-16),(ankle,y-7),7)
        p.r(boots,(ankle-4,y-10,13,10),2)
        p.l((91,86,69),(ankle-4,y-1),(ankle+9,y-1),1)
    # Coat silhouette with split tails and highlights.
    p.p(mix_color(coat,.65),[(x-14,y-62),(x+12,y-62),(x+16,y-31),(x+7,y-23),(x,y-30),(x-13,y-23),(x-17,y-37)])
    p.p(coat,[(x-12,y-61),(x+11,y-61),(x+12,y-33),(x-13,y-34)])
    p.l(mix_color(coat,1.35),(x-10,y-57),(x-9,y-37),2)
    p.r((47,42,34),(x-15,y-37,30,6))
    p.r(brass if old else (122,125,94),(x-2,y-37,6,5))
    # Neck and face profile; no anonymous skin-colour blocks stand in for factions.
    p.r(shade,(x-4,y-68,10,8),2)
    p.e(skin,(x-9,y-85,21,21))
    p.p(skin,[(x+9,y-80),(x+15,y-74),(x+10,y-72)])
    p.r((47,43,38),(x+6,y-79,3,2))
    p.l(shade,(x+4,y-68),(x+10,y-69),1)
    if old:
        # Shako/bicorn, collar, crossed white straps, brass buttons and cartridge box.
        if kind=='charger':
            p.p((31,36,38),[(x-21,y-84),(x-12,y-97),(x+6,y-94),(x+21,y-85)])
            p.l(brass,(x-19,y-84),(x+19,y-84),2)
            p.c(red,(x+1,y-92),4)
        else:
            p.r((37,40,39),(x-11,y-102,23,21),3)
            p.r((27,31,33),(x-12,y-84,31,4))
            p.l((179,150,89),(x-9,y-98),(x+10,y-98),2)
            p.c(brass,(x+2,y-91),4)
            p.l(red,(x-9,y-98),(x-12,y-110),4)
        p.r(red,(x-9,y-64,21,5))
        p.l((225,218,188),(x-12,y-60),(x+10,y-38),4)
        p.l((225,218,188),(x+11,y-60),(x-12,y-38),4)
        for yy in range(y-57,y-38,6):p.c(brass,(x+1,yy),1)
        p.r((42,37,31),(x-19,y-38,11,12),2)
        p.l(brass,(x-18,y-37),(x-10,y-37),1)
        for side in (-1,1):p.r(red,(x+side*13-3,y-61,8,5))
    elif covert:
        # Armed clandestine figure: civilian jacket, scarf and ammunition pouch.
        p.p((40,43,42),[(x-13,y-83),(x-10,y-94),(x+7,y-95),(x+14,y-85)])
        p.r((45,48,45),(x-10,y-74,22,9),2)
        p.l((133,120,91),(x-12,y-58),(x+9,y-37),5)
        p.r((92,83,62),(x-14,y-45,10,13),2)
        p.l((135,126,101),(x-12,y-41),(x-6,y-41),1)
        p.l((28,34,35),(x,y-58),(x,y-39),2)
    else:
        # Olive fatigues, steel helmet, webbing and pouches. No party insignia.
        p.e((66,82,60),(x-13,y-96,29,22))
        p.r((46,57,46),(x-14,y-84,33,4))
        p.l((134,137,101),(x-9,y-61),(x-8,y-35),3)
        p.l((134,137,101),(x+9,y-61),(x+9,y-35),3)
        for dx in (-12,6):p.r((92,103,72),(x+dx,y-47,9,11),1)
        p.l((142,146,107),(x-11,y-43),(x-5,y-43),1)
    # Elbows and hands around a musket/rifle, not an animal's emitter.
    sleeve=red if old else coat
    p.l(mix_color(coat,.8),(x-13,y-57),(x-18,y-42),8)
    p.l(coat,(x-18,y-42),(x+9,y-44),7)
    p.r(sleeve,(x+3,y-47,7,6),1);p.c(skin,(x+12,y-44),4)
    p.l(coat,(x+11,y-55),(x+20,y-43),8)
    p.c(skin,(x+27,y-43),4)
    if kind=='charger' and old:
        p.l((174,180,166),(x+23,y-46),(x+35,y-75),3)
        p.l(brass,(x+16,y-46),(x+29,y-41),3)
    else:
        p.r((88,61,38) if old else (48,46,40),(x-1,y-45,28,6),1)
        p.l((68,73,70),(x+16,y-48),(x+45,y-48),3)
        p.r((118,124,112),(x+23,y-49,12,2))
        if old:
            p.l(metal,(x+42,y-48),(x+48,y-57),2)
            p.l((159,129,77),(x+6,y-45),(x+11,y-52),2)
        else:p.r((37,39,38),(x+15,y-42,5,10),1)
    if kind=='armored':
        if old:
            p.p((129,142,140),[(x-13,y-58),(x+11,y-58),(x+13,y-37),(x-12,y-37)])
            p.l((202,202,170),(x-10,y-56),(x-8,y-40),3)
            p.l((77,93,96),(x+8,y-55),(x+9,y-39),2)
        elif not covert:
            p.p((81,100,103),[(x-24,y-62),(x-3,y-62),(x+1,y-17),(x-19,y-13),(x-28,y-25)])
            p.p((167,181,164),[(x-22,y-60),(x-6,y-60),(x-3,y-29),(x-19,y-25)],1)
            p.r((38,55,61),(x-22,y-51,17,7))
        else:
            p.r((52,54,49),(x-12,y-58,23,23),3)
            for yy in (y-53,y-46):p.l((110,105,81),(x-9,yy),(x+8,yy),2)
    if warning:
        p.c((247,195,105),(94,y-48),3)
        p.l((231,185,99),(87,y-48),(98,y-48),1)
    return pg.transform.smoothscale(p.image(),(82,92))

def mix_color(col,factor):return tuple(max(0,min(255,round(v*factor))) for v in col)

def draw_human(s,e,camera,t,stage=None):
    stage=e.stage if stage is None else stage
    frame=int(e.time*10)%8 if abs(e.speed)>0 and e.kind!='sentry' else 0
    warning=e.kind=='sentry' and e.timer<.4
    img=soldier_image(stage,e.faction,e.kind,frame,warning)
    if e.direction<0:img=pg.transform.flip(img,True,False)
    x=e.rect.centerx-camera;y=e.rect.bottom
    s.blit(img,(int(x-39),int(y-85)))
    if e.kind=='armored':
        from .art import armor_marker
        armor_marker(s,x+35,y-112)
    if e.max_hp>1:
        for n in range(e.max_hp):circle(s,GOLD if n<e.hp else (64,73,74),(x+(n-(e.max_hp-1)/2)*8,y-98),2)
    if e.kind=='charger' and e.mode=='warning':text(s,'!',(x,y-116),19,GOLD,True,'center')
    if e.hit_flash:circle(s,PAPER,(x,y-48),29,2)
    if getattr(e,'show_label',False) and e.mode!='warning':
        label=role_for(e)
        # Labels identify armed figures, never the non-combatant street scenery.
        from .art import font,rect
        width=font(10,True).size(label)[0]+16
        rect(s,(18,32,39),(x-width/2,y-127,width,20),3)
        text(s,label,(x,y-117),10,(231,208,159),True,'center')

@lru_cache(maxsize=2)
def carrier_image():
    p=Painter(280,183);olive=(83,99,72);dark=(31,42,43);metal=(130,142,111)
    for x in (55,113,220):
        p.c(dark,(x,155),25);p.c((80,87,76),(x,155),15)
        p.c(metal,(x,155),9,2)
        for dx,dy in ((-5,0),(5,0),(0,-5),(0,5)):p.c(dark,(x+dx,155+dy),2)
    p.p(dark,[(12,146),(9,113),(36,81),(211,81),(249,104),(268,141)])
    p.p(olive,[(18,134),(19,108),(47,70),(208,70),(246,106),(257,134)])
    p.p((112,124,89),[(40,78),(63,55),(185,55),(214,78)])
    p.r(dark,(89,58,77,43),3);p.r((122,139,127),(96,63,25,24),2)
    p.r((58,82,84),(126,63,31,24),2)
    p.r(metal,(17,119,237,7));p.r(dark,(20,135,235,9))
    for x in range(32,236,17):p.c((150,152,118),(x,124),2)
    for x in (43,211):p.r((213,188,125),(x,104,14,8),2)
    for x in range(54,200,19):p.l((43,58,53),(x,94),(x,110),3)
    p.r((49,63,50),(113,31,62,27),3);p.r(metal,(107,30,76,5))
    p.l((48,58,50),(145,37),(235,37),10)
    p.l((136,146,113),(183,33),(237,33),2)
    p.l((53,64,53),(195,73),(207,9),2)
    p.c((195,189,143),(63,87),10);p.c(dark,(63,87),6)
    return p.image()

def draw_carrier(s,boss,x,y,t):
    img=carrier_image()
    if boss.direction>0:img=pg.transform.flip(img,True,False)
    s.blit(img,(int(x-140),int(y-179)))
