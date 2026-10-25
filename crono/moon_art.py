"""Lunar equipment and terminal repair craft; all original cached illustrations."""
from functools import lru_cache
import math
from .argentina_art import Painter
from .art import circle,text,GOLD,CYAN

@lru_cache(maxsize=3)
def component(index):
    p=Painter(48,52);ink=(34,47,58);gold=(197,156,76);metal=(166,182,180)
    if index==0:
        p.r(ink,(12,10,24,35),8);p.r((197,213,207),(15,12,18,31),6)
        p.r((75,136,162),(15,23,18,9));p.r(gold,(18,5,12,10),2)
        p.l(ink,(24,6),(35,6),3);p.c(gold,(35,6),4)
        for y in (17,37):p.l((141,163,167),(17,y),(30,y),1)
    elif index==1:
        p.r(ink,(8,12,31,33),3);p.r((90,124,145),(11,15,25,27),2)
        for x in (15,23,31):
            for y in (18,27,36):p.r((87,173,190),(x,y,6,6),1)
        for x in (14,30):p.r(gold,(x,6,6,8))
        p.l(gold,(12,44),(37,44),2)
    else:
        p.p(ink,[(11,11),(36,11),(31,30),(42,45),(5,45),(17,30)])
        p.p(metal,[(15,14),(32,14),(27,31),(36,41),(12,41),(21,31)])
        p.r(gold,(12,8,24,8),2);p.e(ink,(13,37,23,8));p.e((84,146,164),(17,39,15,4))
        for x in (17,25,33):p.l(ink,(x,16),(x-2,29),1)
    return p.image()

@lru_cache(maxsize=2)
def lander(repaired=False):
    p=Painter(300,240);ink=(34,43,57);gold=(197,150,64);foil=(231,189,97);metal=(176,189,187)
    for side in (-1,1):
        p.l(ink,(150+side*49,149),(150+side*108,224),8)
        p.l(metal,(150+side*49,149),(150+side*108,224),4)
        p.l(metal,(150+side*48,179),(150+side*94,188),3)
        p.l((98,119,135),(150+side*71,176),(150+side*51,206),3)
        p.e(ink,(150+side*108-22,218,44,11));p.e(gold,(150+side*108-18,219,36,7))
    p.p(ink,[(82,119),(217,119),(235,180),(194,206),(102,206),(65,180)])
    p.p(gold,[(87,124),(211,124),(227,177),(191,199),(106,199),(73,176)])
    for pts,c in (([(87,125),(149,150),(75,175)],foil),([(149,150),(212,125),(225,176)],(163,119,58)),([(149,150),(191,198),(106,198)],(222,173,80))):p.p(c,pts)
    for a,b in (((88,128),(191,196)),((208,128),(108,196)),((79,176),(225,176))):p.l((139,104,58),a,b,1)
    p.p(ink,[(104,52),(180,44),(209,88),(201,129),(91,129),(83,91)])
    p.p(metal,[(108,58),(177,50),(202,91),(195,122),(97,122),(90,92)])
    p.p((67,100,127),[(108,66),(138,65),(141,95),(108,100)]);p.p(CYAN,[(112,69),(134,69),(136,91),(112,95)])
    p.p((67,100,127),[(155,63),(177,61),(190,86),(157,90)]);p.p((119,188,207),[(159,66),(175,65),(184,83),(160,86)])
    p.r(ink,(139,103,35,26),3);p.r((166,180,178),(144,108,25,18),3);p.c(gold,(157,117),5)
    p.l(metal,(153,53),(153,15),3);p.l(metal,(133,22),(176,22),2);p.e((103,139,159),(199,40,50,17));p.l(metal,(208,74),(224,48),3)
    p.l(ink,(108,128),(93,207),6)
    for y in range(139,205,12):p.l(metal,(101, y),(117,y-2),2)
    for x in (122,177):p.p(ink,[(x-9,196),(x+8,196),(x+13,222),(x-15,222)]);p.e((86,110,130),(x-11,218,23,6))
    p.r(ink,(205,145,30,30),3)
    if repaired:
        p.c(CYAN,(220,159),7)
        for y in (149,168):p.l((116,171,169),(210,y),(230,y),1)
    else:
        p.c((230,104,71),(220,159),7)
        for x in (214,222,229):p.l((79,84,80),(x,145),(x+4,171),2)
        p.l((155,54,44),(237,152),(250,187),3);p.l((79,132,162),(231,165),(246,199),3)
    return p.image()

def draw_lander(s,x,y,t,repaired):
    if not -190<x<s.get_width()+190:return
    s.blit(lander(repaired),(int(x-150),int(y-231)))
    if not repaired and int(t*3)%2:circle(s,GOLD,(x+70,y-72),6,2)
    text(s,'MÓDULO REPARADO' if repaired else '↓ · REPARAR CON LAS 3 PIEZAS',(x,y-260),13,CYAN if repaired else GOLD,True,'center')


@lru_cache(maxsize=80)
def rock(width,height,seed,moving=False):
    import random
    rng=random.Random(seed);p=Painter(width,height+18)
    p.p((61,71,84),[(0,0),(width,0),(width-13,height),(width*.7,height+10),(width*.4,height+17),(12,height)])
    p.p((123,134,144),[(0,1),(width,1),(width-8,15),(width*.65,20),(width*.3,14),(8,17)])
    p.l((196,198,179),(0,2),(width,2),3)
    for n in range(max(7,width//20)):
        x=rng.randrange(max(1,width-8));y=rng.randrange(7,max(8,height))
        p.l((80,93,108),(x,y),(x+7,min(y+4,height+5)),1)
    if moving:
        for x in range(18,width,24):p.c((171,167,127),(x,10),2)
    return p.image()
