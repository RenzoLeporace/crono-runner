"""Three distinct Egyptian landscapes, painted at double resolution and cached."""
from functools import lru_cache
import math
import random
import pygame as pg
from .argentina_art import Painter
from .art import line,polygon,circle,rect,text,mix,glow,W,H,GOLD

def glyph(p,x,y,variant,col=(123,90,56)):
    if variant%5==0:
        p.e(col,(x,y,12,7),1);p.c(col,(x+6,y+3),2);p.l(col,(x+1,y+8),(x+10,y+10),1)
    elif variant%5==1:
        p.l(col,(x+6,y),(x+6,y+15),2);p.e(col,(x+2,y,8,7),1);p.l(col,(x,y+8),(x+12,y+8),1)
    elif variant%5==2:
        for dy in (0,5,10):p.p(col,[(x,y+dy+3),(x+3,y+dy),(x+7,y+dy+3),(x+11,y+dy)],1)
    elif variant%5==3:
        p.p(col,[(x,y+10),(x+4,y+3),(x+9,y+6),(x+12,y),(x+11,y+12),(x+1,y+12)],1)
        p.l(col,(x+4,y+12),(x+2,y+16),1)
    else:
        p.p(col,[(x,y+13),(x+6,y),(x+12,y+13)],1);p.l(col,(x+3,y+10),(x+9,y+10),1)

@lru_cache(maxsize=3)
def sky(stage):
    s=pg.Surface((W,H))
    top,horizon=(((31,102,136),(244,211,144)),((105,72,89),(249,182,107)),((12,23,48),(102,104,133)))[stage]
    for y in range(H):line(s,mix(top,horizon,min(1,y/590)),(0,y),(W,y))
    if stage==2:
        rng=random.Random(818)
        for j in range(90):circle(s,(188,196,195),(rng.randrange(W),rng.randrange(105,360)),1)
        circle(s,(224,215,182),(1040,163),25);circle(s,(32,40,64),(1049,156),24)
    else:
        glow(s,(1030,174),110,(252,221,161));circle(s,(251,218,156),(1030,174),37)
    for y in range(584,H):line(s,mix((68,75,81),(21,33,48),(y-584)/136),(0,y),(W,y))
    return s

def background(s,stage,camera,t):
    s.blit(sky(stage),(0,0))
    for layer in range(3):
        factor=.035+layer*.035;off=camera*factor
        for n in range(int(off//650)-1,int(off//650)+4):
            x=n*650-off;base=509+layer*29
            col=((168,146,126),(194,156,106),(206,168,113))[layer] if stage<2 else ((71,76,106),(77,80,106),(92,91,108))[layer]
            polygon(s,col,[(x-100,base),(x+110,base-92+layer*14),(x+330,base-59),(x+670,base+21),(x+670,584),(x-100,584)])
    if stage==0:
        rect(s,(53,134,147),(0,471,W,113))
        for n in range(48):
            x=(n*73-camera*.18+t*6)%(W+100)-50;y=482+n%12*8
            line(s,(130,183,173),(x,y),(x+26+(n%5)*4,y),1)

@lru_cache(maxsize=6)
def pyramid(size,shade=0):
    w,h=size,int(size*.65);p=Painter(w+4,h+4)
    light=(234-shade*12,194-shade*10,132-shade*8);dark=(173-shade*10,127-shade*9,81-shade*5)
    p.p(light,[(2,h),(w*.48,2),(w*.68,h)])
    p.p(dark,[(w*.48,2),(w,h),(w*.68,h)])
    for yy in range(19,h,13):
        frac=yy/h;left=w*.48*(1-frac);mid=w*.48+(w*.2)*frac;right=w*.48+w*.52*frac
        p.l((193-shade*10,151-shade*9,101-shade*6),(left,yy),(mid,yy),1)
        p.l((143-shade*8,106-shade*6,74),(mid,yy),(right,yy),1)
        for xx in range(int(left+12),int(mid),28):p.l((201,160,107),(xx,yy),(xx-2,yy+8),1)
    return p.image()

@lru_cache(maxsize=1)
def temple():
    p=Painter(1100,390)
    p.r((101,78,64),(0,365,1100,25))
    for side in (0,710):
        p.p((190,151,99),[(side,360),(side+27,60),(side+343,60),(side+370,360)])
        p.r((226,189,126),(side+24,47,323,18),3)
        p.r((117,93,68),(side+42,72,290,8))
        for row in range(7):
            y=92+row*36
            p.l((166,129,85),(side+25,y+27),(side+343,y+27),1)
            for j in range(15):glyph(p,side+37+j*19,y,j+row)
        # Carved standing figures, identified as decorative reinterpretations.
        for dx in (91,243):
            p.e((151,113,76),(side+dx,166,24,28));p.l((151,113,76),(side+dx+12,195),(side+dx+12,279),9)
            p.p((151,113,76),[(side+dx+12,247),(side+dx-4,292),(side+dx+29,292)])
            p.l((151,113,76),(side+dx+12,215),(side+dx+44,231),6)
    p.r((52,52,53),(370,151,340,214));p.r((165,128,84),(368,132,344,23))
    for x in (391,465,539,613,683):
        p.r((115,94,70),(x,178,25,182));p.r((202,166,109),(x-4,159,33,20))
        p.p((110,146,135),[(x-7,152),(x+31,152),(x+25,171),(x,171)])
    for x in (357,718):
        p.r((102,80,62),(x,67,5,274));p.p((155,98,73),[(x+5,69),(x+5,185),(x+45,170),(x+46,81)])
    p.r((223,184,118),(345,349,410,13));p.r((165,127,84),(326,362,448,15))
    return p.image()

@lru_cache(maxsize=9)
def village(seed):
    rng=random.Random(seed);p=Painter(290,200)
    for x,w,base,h in ((0,110,193,103),(94,105,193,155),(190,94,193,118)):
        col=(186+rng.randrange(15),148+rng.randrange(17),96+rng.randrange(17))
        p.r((131,101,71),(x,base-h,w,h));p.r(col,(x+3,base-h+4,w-6,h-4))
        p.r((222,184,126),(x-3,base-h-6,w+6,9))
        p.r((81,76,65),(x+23,base-54,24,54),7)
        for xx in range(x+15,x+w-10,29):p.r((82,78,64),(xx,base-h+24,13,18))
        for yy in range(base-h+11,base,17):p.l((166,128,88),(x+5,yy),(x+w-3,yy),1)
    p.p((139,79,54),[(6,140),(72,140),(84,159),(0,159)])
    for x in (6,77):p.l((92,74,56),(x,145),(x,193),3)
    for x in (129,155,218):
        p.e((148,83,48),(x,172,18,20));p.r((210,155,87),(x+4,169,10,6),2)
    return p.image()

def palm(s,x,y,size=1):
    line(s,(108,93,63),(x,y),(x+9*size,y-106*size),round(8*size))
    for j in range(8):
        yy=y-j*12*size;line(s,(158,132,81),(x+2*size,yy),(x+7*size,yy-3),2)
    for direction in (-1,1):
        for j in range(3):
            polygon(s,(48+j*10,101+j*11,83),[(x+9*size,y-106*size),(x+direction*(57+j*12)*size,y-(86-j*12)*size),(x+direction*37*size,y-(112-j*9)*size)])

def landscape(s,world,camera,t):
    stage=world.stage;off=camera*.37
    if stage==0:
        for n in range(int(off//300)-1,int(off//300)+7):
            x=n*300-off;s.blit(village(n%9),(int(x),350));palm(s,x+255,553,1.15)
        # Sailboats move slowly along the background channel.
        for n in range(3):
            x=(n*470-camera*.23+t*8)%1550-120
            polygon(s,(99,74,53),[(x,506),(x+93,506),(x+78,521),(x+15,521)])
            line(s,(90,78,59),(x+45,507),(x+45,426),3)
            polygon(s,(233,214,164),[(x+43,430),(x+6,499),(x+43,499)])
            polygon(s,(212,191,141),[(x+48,430),(x+85,491),(x+48,499)])
        # Cultivation on raised riverbanks.
        for n in range(int(camera*.58//340)-1,int(camera*.58//340)+6):
            x=n*340-camera*.58
            polygon(s,(92,132,83),[(x,545),(x+207,545),(x+255,583),(x-24,583)])
            for j in range(18):
                xx=x+j*12;line(s,(182,178,95),(xx,574),(xx+4,551),2)
    elif stage==1:
        # One recognisable cluster at the Guiza district, varied scale behind it.
        anchor=world.data['zones'][2][0]*.37+580
        for dx,size,shade in ((-370,330,1),(0,490,0),(490,260,2)):
            img=pyramid(size,shade);x=anchor+dx-off-size*.5
            if -size<x<W:s.blit(img,(int(x),557-img.get_height()))
        for n in range(int(off//290)-1,int(off//290)+7):
            x=n*290-off
            for row in range(3):
                rect(s,(173+row*11,137+row*9,90+row*5),(x+row*14,553-row*22,155-row*25,22),2)
                for j in range(4-row):line(s,(139,110,76),(x+row*14+j*34,554-row*22),(x+row*14+j*34,572-row*22),1)
    else:
        anchor=world.data['zones'][2][0]*.42+640;off=camera*.42
        img=temple();x=anchor-off-550
        if -1100<x<W:s.blit(img,(int(x),564-img.get_height()))
        for n in range(int(off//195)-1,int(off//195)+9):
            xx=n*195-off
            if abs(xx-(anchor-off))<560:continue
            rect(s,(130,120,107),(xx,290,35,270));rect(s,(195,163,119),(xx+5,292,25,263))
            polygon(s,(86,130,134),[(xx-10,279),(xx+45,279),(xx+33,307),(xx+3,307)])
            for yy in range(322,543,31):
                line(s,(109,99,84),(xx+7,yy),(xx+27,yy),1)
                circle(s,(150,115,77),(xx+17,yy+13),3,1)
    label=('VALLE DEL NILO · AGUA Y VIDA','GUIZA · REINO ANTIGUO','TEMPLOS DEL REINO NUEVO · MEMORIA Y RELATOS')[stage]
    text(s,label,(1248,111),12,GOLD,True,'topright')

@lru_cache(maxsize=180)
def tile(stage,w,h,seed,moving):
    p=Painter(w,h)
    face=(135,107,76) if stage<2 else (87,87,95)
    top=(222,188,126) if stage<2 else (174,161,132)
    p.r(face,(0,0,w,h));p.r(top,(0,0,w,7))
    for y in range(8,h,26):
        p.l((109,88,65),(0,y),(w,y),1)
        for x in range(-31 if y%52 else 0,w,62):p.l((109,88,65),(x,y),(x,y+26),1)
    if h<60:
        for x in range(19,w-15,31):glyph(p,x,10,(seed+x)//31,(179,149,101) if stage<2 else (153,137,105))
        p.r((89,78,67),(0,h-4,w,4))
    else:
        for x in range(18,w-15,51):
            p.l((164,129,83),(x,18),(x+13,17),1)
    if moving:p.r((99,223,209),(0,0,w,3))
    return p.image()

def sentinel(s,b,x,y,t,core):
    # Fictional sandstone construct, never identified as a historical pharaoh.
    for side in (-1,1):
        rect(s,(88,79,73),(x+side*31-14,y-55,28,55),3)
        rect(s,(192,159,104),(x+side*31-11,y-48,22,42),3)
        line(s,(120,101,76),(x+side*50,y-104),(x+side*78,y-50),20)
        circle(s,(199,166,109),(x+side*79,y-45),14)
    polygon(s,(191,153,94),[(x-52,y-126),(x+52,y-126),(x+42,y-52),(x-42,y-52)])
    polygon(s,(64,131,142),[(x-57,y-126),(x+57,y-126),(x+39,y-103),(x-39,y-103)])
    for dx in range(-45,47,15):line(s,(221,181,104),(x+dx,y-123),(x+dx*.8,y-106),3)
    polygon(s,(202,171,117),[(x-24,y-165),(x+24,y-165),(x+40,y-120),(x-40,y-120)])
    for dx in range(-25,29,9):line(s,(51,104,127),(x+dx,y-160),(x+dx*1.3,y-126),4)
    rect(s,(194,157,101),(x-17,y-151,34,31),4)
    line(s,core,(x-12,y-140),(x+12,y-140),4)
    rect(s,(64,112,127),(x-5,y-125,10,20),2)
