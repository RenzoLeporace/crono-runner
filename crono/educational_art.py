"""Fifteen distinctive landmarks and original fictional guardian illustrations."""
import math
import pygame as pg
from .art import rect,line,circle,polygon,glow,diamond,text,mix,CYAN,GOLD,PAPER,INK,W,H
from .levels import ERAS
from .visuals import palette_for


def map_features(s,world,camera,time):
    if world.index<7:
        from .period_art import landscape
        landscape(s,world,camera,time)
    elif world.index==7:
        from .argentina_art import street
        street(s,world,camera,time)
    else:
        from .egypt_art import landscape
        landscape(s,world,camera,time)


def learning_objects(s,world,camera,time):
    if world.boss and world.boss.active and world.boss.alive:
        xx=world.width-W+6-camera
        line(s,CYAN,(xx,288),(xx,584),2)
        for n in range(8):
            circle(s,CYAN,(xx+math.sin(time*3+n)*7,300+n*35),2)
    for wx,wy,topic in world.data['stations']:
        x=wx-camera
        if not -80<x<W+80:
            continue
        solved=topic in world.answered
        color=CYAN if solved else GOLD
        glow(s,(x,wy-61),67,color)
        polygon(s,(32,50,58),[(x-24,wy),(x-17,wy-64),(x+17,wy-64),(x+24,wy)])
        rect(s,color,(x-21,wy-68,42,6),2)
        yy=wy-97+math.sin(time*2+topic)*4
        polygon(s,color,[(x-23,yy-6),(x,yy),(x,yy+27),(x-23,yy+21)],1)
        polygon(s,color,[(x,yy),(x+23,yy-6),(x+23,yy+21),(x,yy+27)],1)
        line(s,color,(x,yy),(x,yy+27),2)
        if abs(world.player.rect.centerx-wx)<250:
            text(s,'ARCHIVO RESUELTO' if solved else 'ARCHIVO · +2 SABER',(x,wy-132),11,color,True,'center')


def boss_art(s,boss,camera,time):
    if not boss or not boss.alive:
        return
    x,y=boss.rect.centerx-camera,boss.rect.bottom
    if not -230<x<W+230:
        return
    era=palette_for(boss.era,2)
    color=mix(era.top,era.near,.35)
    dark=era.rock
    core=GOLD if boss.phase=='exposed' else (219,120,105)
    if boss.hit_flash:
        color=PAPER
    if boss.era==0:
        polygon(s,dark,[(x-45,y-58),(x-150,y-90),(x-81,y-23)])
        pg.draw.ellipse(s,color,(int(x-69),int(y-104),135,81))
        for dx in (-38,37):
            line(s,dark,(x+dx,y-39),(x+dx-12,y-4),20)
        rect(s,color,(x+21,y-136,79,52),8)
        polygon(s,PAPER,[(x+28,y-91),(x+33,y-77),(x+41,y-91),(x+48,y-77),(x+57,y-91)])
        for j in range(5):
            diamond(s,(x-49+j*22,y-108),13,era.accent)
        circle(s,core,(x+79,y-116),5)
    elif boss.era==1:
        pg.draw.ellipse(s,color,(int(x-80),int(y-132),153,105))
        for dx in (-48,-21,31,54):
            line(s,dark,(x+dx,y-47),(x+dx-9,y-3),17)
        circle(s,color,(x+65,y-109),43)
        line(s,color,(x+91,y-102),(x+108,y-26),23)
        for dy in (0,15):
            pg.draw.arc(s,PAPER,(int(x+45),int(y-101+dy),80,60),3.1,5.8,6)
        circle(s,dark,(x+43,y-108),20)
        circle(s,core,(x+80,y-120),5)
    elif boss.era==2:
        for dx in (-32,32):
            rect(s,dark,(x+dx-13,y-49,26,49),4)
        polygon(s,color,[(x-59,y-111),(x+59,y-111),(x+42,y-45),(x-42,y-45)])
        rect(s,color,(x-29,y-151,58,44),7)
        rect(s,era.accent,(x-25,y-135,50,6))
        for dx in (-1,1):
            line(s,dark,(x+dx*55,y-99),(x+dx*88,y-39),23)
            circle(s,color,(x+dx*88,y-34),16)
    elif boss.era==3:
        wing=math.sin(time*5)*20 if boss.phase=='attack' else 0
        for dx in (-1,1):
            polygon(s,color,[(x,y-83),(x+dx*133,y-159+wing),(x+dx*114,y-91+wing),(x+dx*151,y-52+wing),(x+dx*35,y-41)])
        pg.draw.ellipse(s,dark,(int(x-47),int(y-115),94,99))
        circle(s,color,(x+15,y-125),29)
        polygon(s,era.accent,[(x+36,y-134),(x+80,y-119),(x+36,y-109)])
        circle(s,core,(x+21,y-133),6)
        for dx in (-20,20):
            line(s,era.accent,(x+dx,y-27),(x+dx-5,y-3),6)
    elif boss.era==4:
        for dx in (-42,42):
            circle(s,dark,(x+dx,y-22),24)
            circle(s,era.accent,(x+dx,y-22),15,4)
        rect(s,color,(x-73,y-127,146,90),9)
        for dx in (-55,37):
            rect(s,dark,(x+dx,y-176,21,70),3)
            for j in range(3):
                circle(s,mix(era.far,era.horizon,.3),(x+dx+10+j*7,y-190-j*14),10+j*3)
        rect(s,dark,(x-46,y-143,92,24),5)
        for j in range(4):
            line(s,era.accent,(x-44+j*29,y-62),(x-44+j*29,y-42),4)
        for dx in (-1,1):
            line(s,dark,(x+dx*65,y-96),(x+dx*103,y-55),17)
            circle(s,era.accent,(x+dx*103,y-55),14,5)
    else:
        from .expansion_art import new_boss
        new_boss(s,boss,x,y,time,color,dark,core)
    cx,cy=x,y-78
    glow(s,(cx,cy),65,core)
    circle(s,dark,(cx,cy),23)
    circle(s,core,(cx,cy),21,3)
    diamond(s,(cx,cy),13,core)
    if boss.phase=='warning':
        circle(s,core,(x,y-190),11,2)
        text(s,'!',(x,y-192),17,core,True,'center')
        line(s,core,(x-90,y+3),(x+90,y+3),3)
    for wx,remaining in boss.telegraphs:
        xx=wx-camera
        line(s,(238,151,111),(xx,214),(xx,580),1)
        circle(s,(238,151,111),(xx,579),22,3)
        text(s,'!',(xx,548),18,GOLD,True,'center')


def projectiles(s,world,camera):
    for shot in world.projectiles:
        x,y=shot.rect.centerx-camera,shot.rect.centery
        if not -40<x<W+40:
            continue
        color=CYAN if shot.owner=='player' else (244,151,115)
        if world.index==7 and shot.owner=='enemy' and shot.kind not in ('wave','fall'):
            line(s,(249,215,152),(x,y),(x-(1 if shot.vx>0 else -1)*17,y),2)
            circle(s,PAPER,(x,y),2)
            continue
        if shot.kind=='wave':
            polygon(s,color,[(x-18,584),(x-12,563),(x,552),(x+12,563),(x+18,584)],2)
            glow(s,(x,574),30,color)
        else:
            glow(s,(x,y),25,color)
            circle(s,color,(x,y),6)
            line(s,color,(x,y),(x-(1 if shot.vx>0 else -1)*19,y),3)
