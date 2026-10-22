"""Fifteen distinctive landmarks and original fictional guardian illustrations."""
import math
import pygame as pg
from .art import rect,line,circle,polygon,glow,diamond,text,mix,CYAN,GOLD,PAPER,INK,W,H
from .levels import ERAS
from .visuals import palette_for


def map_features(s,world,camera,time):
    era=palette_for(world.index,world.stage)
    kind=world.data['meta'].landmark
    dark=mix(era.near,era.far,.35)
    lit=mix(era.far,era.accent,.16)
    x=1000-camera*.27
    y=505
    if kind=='coast':
        for j in range(9):
            yy=465+j*9
            line(s,mix(era.near,era.horizon,.15),(0,yy),(W,yy),4)
            for i in range(4):
                xx=(i*385+j*73-time*7-camera*.15)%1500-70
                line(s,mix(era.horizon,era.accent,.12),(xx,yy),(xx+70,yy),1)
        for i in range(3):
            xx=x+i*120
            polygon(s,lit,[(xx-34,220+i*23),(xx,234+i*23),(xx+36,220+i*23),(xx+4,241+i*23)])
    elif kind=='fossils':
        polygon(s,dark,[(x-220,y),(x-190,290),(x-80,260),(x+125,308),(x+180,y)])
        for j in range(7):
            line(s,lit,(x-185,320+j*24),(x+132,338+j*23),2)
        for n in range(18):
            a=n*.43
            r=5+n*2.3
            circle(s,mix(lit,era.top,.3),(x-40+math.cos(a)*r,377+math.sin(a)*r),4)
        line(s,mix(lit,era.top,.35),(x+20,432),(x+105,405),9)
        for dx,dy in ((20,432),(105,405)):
            circle(s,mix(lit,era.top,.35),(x+dx,dy),9)
    elif kind=='crater':
        polygon(s,dark,[(x-250,512),(x-155,405),(x-80,444),(x+70,454),(x+180,400),(x+290,512)])
        polygon(s,lit,[(x-155,405),(x-80,444),(x+70,454),(x+180,400),(x+115,478),(x-70,487)])
        for i in range(12):
            xx=x-95+i*22
            yy=420-(time*12+i*31)%170
            circle(s,mix(era.accent,dark,.6),(xx+math.sin(time+i)*12,yy),3)
        line(s,era.accent,(x+105,170),(x+190,116),2)
    elif kind=='mammoth':
        for xx,scale in ((x,1),(x+220,.6)):
            pg.draw.ellipse(s,lit,(int(xx-76*scale),int(y-100*scale),int(145*scale),int(81*scale)))
            for dx in (-48,-22,26,47):
                line(s,lit,(xx+dx*scale,y-35*scale),(xx+(dx-7)*scale,y),int(12*scale))
            circle(s,lit,(xx+65*scale,y-83*scale),32*scale)
            line(s,lit,(xx+86*scale,y-80*scale),(xx+93*scale,y-25*scale),int(14*scale))
            line(s,mix(lit,era.top,.4),(xx+71*scale,y-60*scale),(xx+108*scale,y-78*scale),int(5*scale))
    elif kind in ('cave','paintings'):
        polygon(s,dark,[(0,90),(W,90),(W,220),(W-170,164),(W-340,240),(W-490,179),
                         (W-650,250),(W-800,163),(W-990,221),(0,185)])
        for xx in (x-190,x+190):
            polygon(s,dark,[(xx-75,y),(xx-45,290),(xx+18,241),(xx+60,315),(xx+80,y)])
        if kind=='cave':
            glow(s,(x,482),120,era.accent)
            polygon(s,era.accent,[(x-22,502),(x-12,466),(x+1,481),(x+8,450),(x+22,500)])
            line(s,dark,(x-31,506),(x+33,493),9)
            line(s,dark,(x-31,493),(x+33,506),9)
            polygon(s,lit,[(x+85,506),(x+146,399),(x+223,506)])
        else:
            paint=mix(era.accent,era.near,.2)
            pg.draw.ellipse(s,paint,(int(x-70),333,106,48),3)
            for dx in (-45,-25,10,24):
                line(s,paint,(x+dx,374),(x+dx-4,408),3)
            line(s,paint,(x+32,347),(x+57,321),4)
            line(s,paint,(x+57,321),(x+80,324),4)
            for i in range(3):
                xx=x-147+i*55
                circle(s,paint,(xx,294),8,2)
                for f in range(5):
                    line(s,paint,(xx-9+f*4,289),(xx-12+f*5,275-abs(f-2)*2),2)
    elif kind=='agora':
        rect(s,dark,(x-170,490,340,18))
        rect(s,lit,(x-155,476,310,14))
        for j in range(7):
            xx=x-130+j*44
            rect(s,lit,(xx,331,21,145))
            rect(s,lit,(xx-7,328,35,13))
        polygon(s,lit,[(x-174,328),(x,251),(x+174,328)])
        for j in range(4):
            rect(s,dark,(x-270+j*140,511,90,11))
    elif kind=='harbor':
        rect(s,mix(era.near,era.horizon,.17),(0,469,W,87))
        for j in range(3):
            xx=x-250+j*210
            polygon(s,dark,[(xx-78,469),(xx+85,469),(xx+47,503),(xx-41,503)])
            line(s,dark,(xx,470),(xx,303),6)
            polygon(s,lit,[(xx-7,316),(xx-7,458),(xx-72,451)])
            polygon(s,mix(lit,era.accent,.12),[(xx+7,320),(xx+74,452),(xx+7,458)])
    elif kind=='stadium':
        for row in range(7):
            yy=337+row*24
            rect(s,lit if row%2 else dark,(x-285-row*8,yy,570+row*16,18))
        rect(s,dark,(x-60,313,120,201))
        for xx in (x-232,x+232):
            rect(s,dark,(xx-8,413,16,105))
            glow(s,(xx,407),45,era.accent)
            polygon(s,era.accent,[(xx-12,416),(xx,380),(xx+13,416)])
    elif kind=='fields':
        for row in range(5):
            polygon(s,lit if row%2 else dark,[(0,500+row*14),(W,480+row*14),(W,489+row*14),(0,509+row*14)])
        rect(s,dark,(x-27,350,54,160))
        polygon(s,dark,[(x-38,350),(x,309),(x+38,350)])
        for j in range(4):
            a=time*.15+j*math.pi/2
            line(s,lit,(x,378),(x+math.cos(a)*86,378+math.sin(a)*86),13)
        for j in range(4):
            xx=x-250+j*71
            pg.draw.ellipse(s,lit,(int(xx),479,40,22))
            circle(s,dark,(xx+37,487),8)
            line(s,dark,(xx+8,496),(xx+8,509),3)
            line(s,dark,(xx+27,496),(xx+27,509),3)
    elif kind=='market':
        for j in range(4):
            xx=x-290+j*176
            for dx in (0,130):
                rect(s,dark,(xx+dx,397,6,118))
            for stripe in range(7):
                polygon(s,lit if stripe%2 else era.far,[(xx-6+stripe*20,397),(xx+14+stripe*20,397),
                    (xx+21+stripe*20,429),(xx+1+stripe*20,429)])
            rect(s,dark,(xx-5,478,150,35))
            for k in range(5):
                circle(s,lit,(xx+14+k*25,472),8)
    elif kind=='cathedral':
        rect(s,dark,(x-190,238,380,300))
        for xx in (x-190,x+133):
            rect(s,dark,(xx,189,57,350))
            polygon(s,dark,[(xx-8,189),(xx+28,113),(xx+65,189)])
        polygon(s,lit,[(x-75,465),(x-75,334),(x,266),(x+75,334),(x+75,465)])
        for dx in (-48,-24,0,24,48):
            line(s,era.near,(x+dx,321+abs(dx)*.6),(x+dx,466),5)
        for yy in (356,389,422):
            line(s,era.near,(x-72,yy),(x+72,yy),5)
        circle(s,era.accent,(x,225),29,2)
        for j in range(8):
            a=j*math.pi/4
            line(s,era.accent,(x,225),(x+math.cos(a)*27,225+math.sin(a)*27),2)
    elif kind=='engine':
        rect(s,dark,(x-150,333,300,180))
        rect(s,lit,(x-129,378,72,126))
        rect(s,lit,(x+53,358,70,146))
        a=math.sin(time)*14
        line(s,lit,(x-128,310+a),(x+125,310-a),17)
        line(s,dark,(x,309),(x,495),19)
        for dx in (-93,88):
            line(s,era.accent,(x+dx,320+a*(1 if dx<0 else -1)),(x+dx,427),7)
        circle(s,lit,(x+183,439),61,11)
        line(s,lit,(x+183,439),(x+183+math.cos(time)*55,439+math.sin(time)*55),8)
    elif kind=='railway':
        for j in range(2):
            yy=506+j*13
            line(s,lit,(0,yy),(W,yy),4)
        for j in range(30):
            xx=(j*62-camera*.27)%W
            line(s,dark,(xx,503),(xx+8,523),6)
        rect(s,dark,(x-75,418,178,65),9)
        rect(s,lit,(x-84,383,75,101))
        rect(s,dark,(x+65,367,20,73))
        for dx in (-56,19,80):
            circle(s,lit,(x+dx,491),23,6)
        line(s,lit,(x-56,491),(x+80,491),6)
        for j in range(4):
            circle(s,mix(lit,era.horizon,.2),(x+78+j*16,338-j*21),13+j*4)
    elif kind=='electric':
        for j in range(6):
            xx=x-320+j*137
            rect(s,dark,(xx,315,8,205))
            line(s,dark,(xx-27,337),(xx+35,337),4)
            points=[(xx+i*10,337+math.sin(i/14*math.pi)*22) for i in range(15)]
            pg.draw.lines(s,dark,False,points,2)
            rect(s,era.accent,(xx-11,359,30,40),7)
            glow(s,(xx+4,379),55,era.accent)


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
    else:
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
    cx,cy=x,y-78
    glow(s,(cx,cy),65,core)
    circle(s,dark,(cx,cy),23)
    circle(s,core,(cx,cy),21,3)
    diamond(s,(cx,cy),13,core)
    if boss.phase=='warning':
        circle(s,core,(x,y-190),11,2)
        text(s,'!',(x,y-192),17,core,True,'center')
        line(s,core,(x-90,y+3),(x+90,y+3),3)


def projectiles(s,world,camera):
    for shot in world.projectiles:
        x,y=shot.rect.centerx-camera,shot.rect.centery
        if not -40<x<W+40:
            continue
        color=CYAN if shot.owner=='player' else (244,151,115)
        if shot.kind=='wave':
            polygon(s,color,[(x-18,584),(x-12,563),(x,552),(x+12,563),(x+18,584)],2)
            glow(s,(x,574),30,color)
        else:
            glow(s,(x,y),25,color)
            circle(s,color,(x,y),6)
            line(s,color,(x,y),(x-(1 if shot.vx>0 else -1)*19,y),3)
