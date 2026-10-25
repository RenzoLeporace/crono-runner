"""Distinct landscapes for Argentina, rescue bonuses and historical rifts."""
from functools import lru_cache
import math
import pygame as pg
from .argentina_art import Painter
from .art import W,H,mix,rect,line,circle,polygon,text,glow,GOLD,PAPER
from .journeys import combat_era,DATES

def ship(p,x,y,scale=1,side='rio'):
    s=scale;wood=(104,74,50);sail=(228,215,175)
    p.p((58,65,66),[(x,y),(x+310*s,y),(x+270*s,y+58*s),(x+39*s,y+58*s)])
    p.p(wood,[(x+8*s,y-8*s),(x+306*s,y-8*s),(x+270*s,y+41*s),(x+37*s,y+41*s)])
    for yy in range(0,40,8):p.l((163,120,74),(x+18*s,y+yy*s),(x+(300-yy*.6)*s,y+yy*s),2)
    for j in range(8):p.r((34,47,51),(x+(40+j*29)*s,y+11*s,15*s,13*s),1)
    for dx,h in ((105,175),(204,199)):
        p.l((109,91,61),(x+dx*s,y),(x+dx*s,y-h*s),4)
        for yy,ww in ((h-6,105),(h-65,124)):
            p.l(wood,(x+(dx-ww*.5)*s,y-yy*s),(x+(dx+ww*.5)*s,y-yy*s),3)
            p.p(sail,[(x+(dx-ww*.5)*s,y-yy*s),(x+(dx+ww*.5)*s,y-yy*s),(x+(dx+ww*.4)*s,y-(yy-49)*s),(x+(dx-ww*.39)*s,y-(yy-49)*s)])
            for dd in range(-40,45,16):p.l((196,181,139),(x+(dx+dd)*s,y-yy*s),(x+(dx+dd*.8)*s,y-(yy-48)*s),1)
        p.l((188,176,134),(x+dx*s,y-h*s),(x+22*s,y+8*s),1)
        p.l((188,176,134),(x+dx*s,y-h*s),(x+287*s,y+8*s),1)
    flag=(81,167,194) if side=='rio' else (61,111,83) if side=='imperial' else (150,112,84)
    p.r(flag,(x+205*s,y-202*s,41*s,22*s))
    if side=='rio':p.r((232,223,190),(x+205*s,y-195*s,41*s,8*s))
    elif side=='imperial':p.p((221,192,93),[(x+226*s,y-200*s),(x+244*s,y-191*s),(x+226*s,y-182*s),(x+208*s,y-191*s)])

@lru_cache(maxsize=3)
def vessel(side='rio'):
    p=Painter(370,300);ship(p,15,237,1,side);return p.image()

@lru_cache(maxsize=9)
def scene_image(level):
    if level>=36:
        from .country_art import scene
        return scene(level)
    p=Painter(1080,430);n=level-27
    if n in (0,2):
        ship(p,125,327,.95,'rio' if n==0 else 'imperial');ship(p,630,351,.8,'neutral' if n==0 else 'imperial')
        if n==0:
            for j in range(19):p.e((119,129,126),(50+j*55,388+(j%2)*5,76,21),4)
            for x in (18,996):
                p.r((110,90,62),(x,361,65,65));p.l((58,64,62),(x+11,360),(x+61,336),11)
    elif n==1:
        for x,h in ((0,290),(240,380),(535,316),(810,355)):
            p.p((93,119,139),[(x-90,430),(x+110,430-h),(x+343,430)])
            p.p((215,227,224),[(x+110,430-h),(x+30,509-h),(x+78,486-h),(x+101,518-h),(x+128,488-h),(x+169,519-h)])
            for j in range(6):p.l((143,169,180),(x+113,454-h+j*29),(x+186+j*14,543-h+j*35),2)
        for x in (214,695):
            p.p((177,166,132),[(x,425),(x+55,344),(x+110,425)])
            p.p((90,101,106),[(x+37,425),(x+56,371),(x+75,425)])
        for x in (401,448,844):
            p.e((126,100,73),(x,387,48,23));p.c((126,100,73),(x+44,384),10)
            for dx in (8,33):p.l((75,72,61),(x+dx,404),(x+dx,427),4)
            p.r((168,147,102),(x+13,374,27,23),3)
    elif n==3:
        from .period_art import column,blocks
        blocks(p,(407,219,255,207),(191,179,145))
        p.p((220,206,167),[(397,219),(441,118),(625,118),(673,219)])
        p.r((201,191,159),(472,62,125,60));p.r((117,152,158),(483,67,103,51))
        for x in (478,514,553,589):column(p,x,55,70,(220,204,157))
        p.p((185,151,100),[(466,52),(533,9),(605,52)])
        p.p((114,160,174),[(487,91),(3,172),(2,260),(487,109)])
        p.p((114,160,174),[(582,91),(1078,172),(1078,260),(582,109)])
        ship(p,34,381,.6)
    elif n==4:
        from .period_art import blocks
        blocks(p,(0,370,1080,60),(97,101,100),50,20)
        for j in range(4):
            x=35+j*235;p.r((65,77,85),(x,243,215,109),8)
            for xx in range(15,209,43):p.r((222,177,95),(x+xx,262,25,39),2)
            for dx in (35,175):p.c((36,47,55),(x+dx,355),21);p.c((143,152,143),(x+dx,355),14,3)
            p.r((127,103,71),(x,348,216,9))
        p.r((64,77,83),(907,189,52,107),4);p.l((65,79,88),(1030,409),(1030,156),8)
        for y,col in ((189,(178,92,72)),(220,(218,178,98)),(251,(115,191,145))):p.c(col,(1030,y),11)
    elif n in (5,6):
        for x in (45,350,698):
            p.p((99,120,112) if n==5 else (91,106,105),[(x,416),(x+107,277),(x+279,416)])
            p.p((59,74,74),[(x+85,416),(x+109,321),(x+139,416)])
            p.l((159,166,139),(x+106,275),(x+106,417),4)
            for j in range(6):p.l((142,146,124),(x+29+j*32,409),(x+43+j*30,390),1)
        if n==5:
            p.r((216,222,194),(463,315,25,80));p.r((216,222,194),(438,340,76,27))
            p.r((76,134,98),(468,320,15,70));p.r((76,134,98),(443,345,66,17))
        else:
            p.r((65,82,83),(502,335,120,83),6);p.l((162,169,149),(570,334),(589,215),3)
            for y in range(347,400,12):p.l((157,169,146),(511,y),(558,y),3)
        for x in range(10,1080,70):
            for j in range(4):p.l((117,141,111),(x,430),(x-8+j*6,414-j%2*9),2)
    elif n==7:
        from .period_art import blocks,column
        for x in (23,753):
            blocks(p,(x,246,296,178),(162,132,108));p.p((143,89,65),[(x-15,246),(x+143,195),(x+312,246)])
            for dx in (20,98,177,254):column(p,x+dx,267,155,(205,185,148))
        p.p((93,73,73),[(237,291),(550,26),(831,291)])
        p.p((54,52,62),[(502,68),(550,26),(600,71),(574,89),(535,83)])
        for j in range(8):p.c((75+j*3,70+j*2,76),(538+j*12,44-j*17),22+j*4)
        for x in range(0,1079,25):p.c((180,160,128),(x,420+x%5),2)
    else:
        for x,y,r in ((80,379,55),(300,404,62),(714,367,84),(965,405,73)):
            p.e((86,95,107),(x-r,y-r*.3,r*2,r*.6),3);p.e((123,130,134),(x-r+6,y-r*.3+7,r*2-12,r*.6-13),2)
        p.p((170,171,152),[(428,372),(465,261),(590,261),(628,372)])
        p.r((189,188,160),(466,230,124,81),6);p.p((51,68,88),[(475,241),(520,241),(519,277),(477,275)])
        p.r((174,158,102),(510,314,38,58));p.r((49,60,73),(488,324,82,16))
        for side in (-1,1):p.l((183,174,129),(526+side*60,321),(526+side*124,410),5);p.r((174,164,118),(526+side*124-20,409,40,7))
        p.l(PAPER,(699,416),(699,226),3);p.r((148,172,178),(700,227,66,41),2)
    return p.image()

@lru_cache(maxsize=12)
def sky(index,stage):
    from .visuals import palette_for
    pal=palette_for(index,stage);level=index*3+stage;s=pg.Surface((W,H))
    for y in range(H):line(s,mix(pal.sky,pal.horizon,min(1,y/590)),(0,y),(W,y))
    if level in (35,44):
        for n in range(65):circle(s,(186,195,196),((n*143)%W,107+(n*67)%270),1)
        circle(s,(91,151,183),(1020,176),39);polygon(s,(154,184,154),[(1001,151),(1022,148),(1040,169),(1027,191),(1008,183)])
    for y in range(584,H):line(s,mix(pal.near,(13,24,38),(y-584)/136),(0,y),(W,y))
    return s


def background(s,index,stage,camera,t):
    from .visuals import palette_for
    pal=palette_for(index,stage);level=index*3+stage
    s.blit(sky(index,stage),(0,0))
    if level not in (35,44):
        for layer in range(2):
            off=camera*(.035+layer*.04)
            for n in range(int(off//510)-1,int(off//510)+math.ceil(W/510)+1):
                x=n*510-off;h=80+(n*47)%125
                if level in (27,29,30,33):
                    polygon(s,pal.far if not layer else pal.near,[(x-80,488),(x+140,469-(n%3)*6),(x+310,480),(x+560,488),(x+560,584),(x-80,584)])
                    continue
                polygon(s,pal.far if not layer else pal.near,[(x-80,562),(x+140,440-h),(x+310,490-h*.5),(x+560,562),(x+560,584),(x-80,584)])
    if level in (27,29,30,33):
        rect(s,mix(pal.near,(39,111,133),.4),(0,472,W,112))
        for n in range(30):
            x=(n*97-camera*.11+t*13)%W;y=482+n%10*10;line(s,mix(pal.horizon,pal.far,.4),(x,y),(x+48,y),1)

def landscape(s,world,camera,t):
    if world.level_id>=36:
        from .country_art import landscape as new_landscape
        new_landscape(s,world,camera,t)
        text(s,DATES[world.level_id-27].upper(),(s.get_width()-25,119),12,GOLD,True,'topright');return
    level=world.level_id;off=camera*.4;focal=world.data['zones'][2][0]*.4+640
    img=scene_image(level);x=focal-off-540
    if -1080<x<W:s.blit(img,(int(x),143))
    if level in (27,29,30):
        for n in range(int(off//600)-1,int(off//600)+math.ceil(W/600)+1):
            wx=n*600-off
            if abs(wx-(focal-off))<520:continue
            side='rio' if n%2 else 'imperial' if level==29 else 'neutral'
            s.blit(vessel(side),(int(wx),266))
    elif level not in (28,33,34,35):
        from .period_art import module
        for n in range(int(off//311)-1,int(off//311)+math.ceil(W/311)+1):
            wx=n*311-off
            if abs(wx-(focal-off))<510:continue
            s.blit(module(combat_era(world.index,world.stage),0,n%6),(int(wx),206))
    if level in (28,33):
        for n in range(35):
            x=(n*127+t*59-camera*.4)%W;y=139+(n*73+t*21)%440;line(s,(185,205,209),(x,y),(x-8,y+3),1)
    elif level==34:
        for n in range(50):circle(s,(186,171,145),((n*137+t*35)%W,119+(n*61+t*27)%440),1)
    text(s,DATES[level-27].upper(),(W-25,119),12,GOLD,True,'topright')

def tile(index,stage,w,h,seed,moving):
    from .period_art import tile as base_tile
    level=index*3+stage
    if level==44:
        from .moon_art import rock
        return rock(w,h,seed,moving)
    base=1 if level==28 else combat_era(index,stage)
    if base==7:
        from .argentina_art import platform_tile
        return platform_tile(0,w,h,seed,moving)
    return base_tile(base,0,w,h,seed,moving)

def guardian(s,b,x,y,t,core):
    variant=b.variant
    if variant in ('naval','battery'):
        img=vessel('imperial' if variant=='naval' else 'neutral');s.blit(img,(int(x-185),int(y-298)))
    elif variant=='lighthouse':
        rect(s,(187,176,142),(x-49,y-147,98,147),5);polygon(s,(217,198,146),[(x-59,y-145),(x,y-199),(x+59,y-145)])
        for yy in range(int(y-136),int(y-20),23):line(s,(119,118,106),(x-42,yy),(x+42,yy),2)
        circle(s,core,(x,y-156),17)
    elif variant=='train':
        rect(s,(77,92,96),(x-120,y-113,240,88),13)
        for dx in (-82,-33,32,81):circle(s,(40,55,64),(x+dx,y-22),22);circle(s,core,(x+dx,y-22),13,3)
        rect(s,(50,67,79),(x+61,y-171,28,62),4)
    elif variant in ('hospital','malvinas'):
        for side in (-1,1):line(s,(136,154,151),(x+side*78,y),(x,y-171),8)
        circle(s,(66,96,111),(x,y-124),47);circle(s,core,(x,y-124),33,4)
        for j in range(3):pg.draw.arc(s,core,(int(x-70-j*14),int(y-188-j*14),140+j*28,140+j*28),.3,2.8,2)
    elif variant in ('andes','volcano'):
        polygon(s,(114,111,105),[(x-109,y),(x-70,y-130),(x+4,y-184),(x+88,y-116),(x+117,y)])
        polygon(s,(213,221,213) if variant=='andes' else (175,92,53),[(x-70,y-130),(x+4,y-184),(x+88,y-116),(x+22,y-139),(x-6,y-117)])
    else:
        circle(s,(134,155,164),(x,y-112),67,7)
        for j in range(4):
            a=t+j*math.tau/4;xx=x+math.cos(a)*87;yy=y-112+math.sin(a)*61
            line(s,(101,130,144),(x,y-112),(xx,yy),5);circle(s,core,(xx,yy),15,3)
