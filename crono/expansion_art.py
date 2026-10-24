"""Code-native architecture for wars, contemporary cities and Argentina."""
import math
import pygame as pg
from .art import rect,line,circle,polygon,text,mix,PAPER,CYAN,GOLD,W
from .visuals import palette_for

def landmark(s,world,camera,t):
    pal=palette_for(world.index,world.stage)
    kind=world.data['meta'].landmark
    dark=pal.near;light=mix(pal.top,pal.horizon,.4)
    offset=camera*.22
    for n in range(int(offset//340)-1,int(offset//340)+6):
        x=n*340-offset
        if world.index==5:
            if kind=='trenches':
                for row in range(3):
                    rect(s,dark,(x,451+row*20,350,13))
                    for j in range(8):line(s,light,(x+j*47,449+row*20),(x+j*47,463+row*20),2)
                for j in range(4):
                    line(s,dark,(x+j*78,430),(x+j*78+30,461),5)
                    line(s,dark,(x+j*78+30,430),(x+j*78,461),5)
            else:
                h=110+(n*53)%110
                rect(s,dark,(x,510-h,220,h+30))
                if kind=='shelter':
                    polygon(s,pal.far,[(x,510-h),(x+32,489-h),(x+60,521-h),(x+100,487-h),(x+147,510-h)])
                for a in range(5):
                    for b in range(max(1,h//34-1)):
                        rect(s,light,(x+15+a*39,525-h+b*31,10,15))
                if kind=='peace':
                    line(s,light,(x+248,510),(x+248,289),4)
                    rect(s,(117,183,207),(x+250,290,70,44))
                    circle(s,PAPER,(x+285,311),13,2)
            if kind=='shelter':
                # Low-contrast, steady searchlight, no flashing.
                polygon(s,mix(pal.far,pal.horizon,.2),[(x+91,499),(x-120+math.sin(t*.2)*35,147),(x+42,132)])
        elif world.index==6:
            if kind=='network':
                h=160+(n*71)%120
                rect(s,dark,(x,520-h,187,h+50),7)
                for a in range(4):
                    for b in range(5):rect(s,CYAN,(x+19+a*43,540-h+b*30,10,12),2)
                line(s,light,(x+93,520-h),(x+93,474-h),3)
                circle(s,CYAN,(x+93,466-h),9,2)
                pg.draw.arc(s,CYAN,(int(x+57),int(429-h),72,74),.4,2.7,2)
            elif kind=='renewables':
                polygon(s,pal.far,[(x-40,538),(x+80,441),(x+350,478),(x+380,550)])
                polygon(s,(36,78,115),[(x,466),(x+130,466),(x+159,506),(x+28,506)])
                for a in range(5):line(s,light,(x+a*26,466),(x+28+a*26,506),1)
                line(s,light,(x+210,514),(x+210,283),7)
                for j in range(3):
                    angle=t*.6+j*math.tau/3
                    line(s,light,(x+210,283),(x+210+math.cos(angle)*75,283+math.sin(angle)*75),8)
            else:
                rect(s,dark,(x,440,215,96),6)
                pg.draw.arc(s,light,(int(x+15),341,186,181),0,math.pi,7)
                line(s,light,(x+35,422),(x+165,361),15)
                for j in range(4):rect(s,CYAN,(x+15+j*48,466,25,15),2)
                for j in range(7):circle(s,PAPER,((x+j*137)%W,130+(j*61)%180),1)
        else:
            if kind=='democracy':
                rect(s,dark,(x,355,272,170))
                polygon(s,light,[(x-10,355),(x+136,301),(x+282,355)])
                for j in range(7):rect(s,light,(x+16+j*37,367,15,135))
                pg.draw.arc(s,light,(int(x+87),222,98,129),0,math.pi,5)
                rect(s,dark,(x+92,283,90,35))
            else:
                rect(s,light,(x,392,292,130))
                for j in range(7):
                    pg.draw.arc(s,dark,(int(x+9+j*41),408,28,77),0,math.pi,5)
                    rect(s,dark,(x+10+j*41,447,27,60))
                rect(s,dark,(x-5,383,303,12))
                if kind=='cabildo' and n%3==0:
                    rect(s,light,(x+110,301,68,84))
                    circle(s,dark,(x+144,337),18,3)
                    line(s,dark,(x+144,337),(x+144,324),2)
                    polygon(s,dark,[(x+106,301),(x+144,272),(x+182,301)])
                elif kind=='tucuman' and n%3==0:
                    rect(s,(224,205,162),(x+92,354,112,63))
                    rect(s,(72,111,141),(x+118,376,59,130))
                    polygon(s,dark,[(x+86,354),(x+148,326),(x+210,354)])
            line(s,light,(x+318,513),(x+318,283),3)
            # Colonial 1810 has no Argentine flag yet; sky-blue flags appear later.
            if kind!='cabildo':
                for j,col in enumerate(((130,203,232),PAPER,(130,203,232))):
                    rect(s,col,(x+320,286+j*14,68,14))
    text(s,{'cabildo':'BUENOS AIRES · MAYO DE 1810','tucuman':'TUCUMÁN · JULIO DE 1816',
            'democracy':'ARGENTINA · DICIEMBRE DE 1983'}.get(kind,''),(W-32,123),12,GOLD,True,'topright')

def new_boss(s,b,x,y,t,color,dark,core):
    if b.era==5:
        pg.draw.ellipse(s,dark,(int(x-103),int(y-42),206,45))
        for dx in range(-76,90,29):circle(s,color,(x+dx,y-20),14,3)
        polygon(s,color,[(x-98,y-43),(x-68,y-112),(x+66,y-112),(x+99,y-43)])
        rect(s,dark,(x-35,y-148,72,43),8)
        line(s,color,(x,y-127),(x+b.direction*132,y-127),19)
    elif b.era==6:
        for j in range(6):
            a=t*.7+j*math.tau/6
            xx=x+math.cos(a)*95;yy=y-92+math.sin(a)*76
            line(s,dark,(x,y-78),(xx,yy),9)
            circle(s,color,(xx,yy),19);circle(s,core,(xx,yy),10,3)
        polygon(s,color,[(x-48,y-125),(x+48,y-125),(x+67,y-80),(x+28,y-20),(x-28,y-20),(x-67,y-80)])
    else:
        # Ceramic archive guardian, a fictional creature rather than an adversary nation.
        rect(s,color,(x-70,y-117,140,102),9)
        for dx in (-48,48):
            line(s,dark,(x+dx,y-21),(x+dx,y),18)
            pg.draw.arc(s,dark,(int(x+dx-13),int(y-94),26,59),0,math.pi,5)
        rect(s,color,(x-32,y-172,64,59),4)
        polygon(s,dark,[(x-43,y-172),(x,y-202),(x+43,y-172)])
        circle(s,core,(x,y-145),16,3)
