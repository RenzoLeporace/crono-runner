"""Detailed, supersampled Argentine streets with unique historical landmarks.

Scenery uses separate depths and seeded materials. Buenos Aires has a flat
estuary horizon; Tucumán has low distant foothills. Landmarks are placed once,
not used as a repeated building tile. Nothing drawn here changes collision.
"""
from functools import lru_cache
import math
import random
import pygame as pg
from .art import W,H,rect,line,circle,polygon,text,mix,glow,PAPER,GOLD,CYAN

class Painter:
    def __init__(self,w,h):
        self.w,self.h=w,h
        self.s=pg.Surface((w*2,h*2),pg.SRCALPHA)
    def r(self,col,box,radius=0,width=0):
        pg.draw.rect(self.s,col,pg.Rect(*(round(v*2) for v in box)),width*2,border_radius=radius*2)
    def l(self,col,a,b,width=1):
        pg.draw.line(self.s,col,tuple(round(v*2) for v in a),tuple(round(v*2) for v in b),width*2)
    def p(self,col,points,width=0):
        pg.draw.polygon(self.s,col,[(round(x*2),round(y*2)) for x,y in points],width*2)
    def e(self,col,box,width=0):
        pg.draw.ellipse(self.s,col,pg.Rect(*(round(v*2) for v in box)),width*2)
    def c(self,col,pos,r,width=0):
        pg.draw.circle(self.s,col,tuple(round(v*2) for v in pos),round(r*2),width*2)
    def a(self,col,box,start,end,width=1):
        pg.draw.arc(self.s,col,pg.Rect(*(round(v*2) for v in box)),start,end,width*2)
    def label(self,value,x,y,size,col):
        self.s.blit(pg.font.SysFont('georgia',size*2,True).render(value,True,col),(int(x*2),int(y*2)))
    def image(self):return pg.transform.smoothscale(self.s,(self.w,self.h))

def arch(p,x,y,w,h,wall,inside,trim):
    p.e(trim,(x-3,y-3,w+6,w+6))
    p.r(trim,(x-3,y+w/2,w+6,h-w/2+3))
    p.e(inside,(x,y,w,w))
    p.r(inside,(x,y+w/2,w,h-w/2))
    p.r(mix(inside,wall,.12),(x+7,y+w/2+2,w-14,h-w/2-3))
    p.l(mix(trim,wall,.5),(x-5,y+h),(x+w+5,y+h),3)

def roof(p,x,y,w,col,depth=24):
    p.p(mix(col,(58,39,34),.3),[(x-9,y+depth),(x+12,y),(x+w-17,y),(x+w+10,y+depth)])
    for row in range(3):
        for dx in range(-2,int(w)+2,12):
            yy=y+8+row*6
            p.l(mix(col,(236,170,111),.15+row*.1),(x+dx+3,yy),(x+dx+10,yy+3),2)
    p.l((82,58,46),(x-9,y+depth+2),(x+w+10,y+depth+2),4)
    p.l(mix(col,(242,211,163),.45),(x-7,y+depth),(x+w+8,y+depth),2)

def window(p,x,y,w,h,wall,wood=(54,78,78),balcony=False,modern=False):
    trim=mix(wall,(251,235,201),.6)
    p.r(mix(wall,(62,46,39),.5),(x-5,y-5,w+10,h+10),2)
    p.r(trim,(x-3,y-3,w+6,h+6),1)
    p.r((33,44,49),(x,y,w,h))
    if modern:
        p.r((191,149,93),(x+3,y+3,w-6,h-6))
        p.r((225,197,128),(x+6,y+5,w*.35,h-10))
    else:
        p.r(wood,(x+2,y+2,w*.43,h-4))
        p.r(mix(wood,(246,226,183),.1),(x+w*.54,y+2,w*.4,h-4))
        for yy in range(int(y+8),int(y+h-3),8):
            p.l(mix(wood,(9,21,29),.45),(x+4,yy),(x+w*.42,yy),1)
            p.l(mix(wood,(9,21,29),.45),(x+w*.55,yy),(x+w-4,yy),1)
    p.l((57,53,47),(x+w/2,y+1),(x+w/2,y+h-1),2)
    p.r(trim,(x-7,y+h+2,w+14,6))
    if balcony:
        p.r((49,54,55),(x-12,y+h+10,w+24,6))
        for xx in range(int(x-10),int(x+w+12),8):p.l((43,53,55),(xx,y+h-15),(xx,y+h+10),2)
        p.l((73,82,79),(x-14,y+h-17),(x+w+14,y+h-17),3)
        p.l((23,36,42),(x-14,y+h+4),(x+w+14,y+h+4),2)

def plaster(p,x,y,w,h,col,seed):
    rng=random.Random(seed)
    p.r(col,(x,y,w,h))
    p.r(mix(col,(51,50,46),.25),(x,y+h-21,w,21))
    for _ in range(int(w*h/950)):
        xx=x+rng.randrange(max(1,int(w-8)));yy=y+rng.randrange(max(1,int(h-8)))
        p.l(mix(col,(105,87,70),.15),(xx,yy),(xx+rng.randint(2,10),yy),1)
    for dx in (13,w-27):
        xx=x+dx
        p.l(mix(col,(70,61,53),.3),(xx,y+h-52),(xx+5,y+h-39),1)
        p.l(mix(col,(70,61,53),.3),(xx+5,y+h-39),(xx+3,y+h-24),1)

@lru_cache(maxsize=96)
def house(stage,seed,depth=0):
    rng=random.Random(7700+stage*991+seed*17)
    w=rng.choice((222,252,282,312));h=rng.choice((198,238,278)) if stage<2 else rng.choice((278,322,362,402))
    p=Painter(w+26,h+36)
    col=rng.choice(((174,157,126),(201,185,151),(160,162,143),(174,143,122),(192,173,135)))
    if stage==2:col=rng.choice(((119,129,135),(143,129,120),(131,143,140),(152,145,128),(120,121,134)))
    if depth:col=mix(col,(96,119,122),.35)
    wall_x=13;wall_y=26
    plaster(p,wall_x,wall_y,w,h,col,seed)
    p.r(mix(col,(43,42,42),.27),(w+1,wall_y,12,h))
    if stage<2:roof(p,10,4,w+5,(143,83,57) if stage else (123,83,62))
    else:
        p.r((57,65,71),(6,15,w+15,14))
        p.r(mix(col,PAPER,.2),(9,12,w+10,5))
        p.r((57,64,66),(w-50,0,31,17))
        p.r((81,88,83),(w-48,0,27,5))
        for dx in (40,75):p.l((51,61,68),(dx,15),(dx,-1),1)
    floors=2 if stage<2 and h>210 else 1 if stage<2 else 3 if h<350 else 4
    step=(h-34)/(floors+(.8 if stage==2 else .55))
    for row in range(floors):
        yy=wall_y+20+row*step
        cols=3 if w>260 else 2
        for j in range(cols):
            xx=wall_x+24+j*(w-46)/cols
            window(p,xx,yy,34 if stage<2 else 30,49 if stage<2 else 43,col,balcony=(row%2==0 and seed%3!=0),modern=stage==2 and (j+row+seed)%3==0)
        if stage==2:
            p.l(mix(col,(219,207,173),.3),(wall_x,yy+59),(wall_x+w,yy+59),3)
    door_x=w*.5-12;door_y=h-58
    if stage<2:
        p.r((63,53,45),(door_x-3,door_y-7,47,86))
        p.r((81,67,51),(door_x,door_y-3,40,80))
        for j in range(2):
            for k in range(3):p.r((51,45,39),(door_x+4+j*19,door_y+4+k*22,13,15),1,1)
        p.c((184,151,90),(door_x+31,door_y+41),2)
        if seed%3==0:
            p.r((79,66,51),(22,h-47,91,22))
            p.label(('ALMACÉN','PULPERÍA','POSTA')[seed%3],27,h-44,9,(226,210,164))
    else:
        p.r((38,48,56),(23,h-53,w-35,73))
        for j in range(4):
            p.r((91,123,134),(28+j*(w-39)/4,h-45,(w-51)/4,57))
            p.l((196,189,157),(28+j*(w-39)/4,h-45),(28+j*(w-39)/4,h+12),2)
        p.r((42,68,75),(17,h-77,w-12,25))
        p.label(('LIBRERÍA','CAFÉ DEL BARRIO','KIOSCO','FARMACIA')[seed%4],27,h-73,12,(227,213,167))
        # A small election poster dates the street without turning citizens into enemies.
        if seed%2:
            p.r((209,196,164),(w-27,h-128,25,38))
            p.label('1983',w-25,h-124,6,(52,62,69))
            p.r((76,112,138),(w-24,h-110,19,3))
            p.r((96,108,108),(w-24,h-102,17,1))
    p.l((64,66,62),(6,h+28),(w+23,h+28),5)
    return p.image()

@lru_cache(maxsize=4)
def cabildo():
    p=Painter(1050,384);cream=(224,212,181);shadow=(94,99,91);trim=(247,231,194)
    plaster(p,19,158,1010,206,cream,44)
    roof(p,18,132,1014,(154,91,59),25)
    for n in range(11):
        x=37+n*90
        arch(p,x,270,63,86,cream,(65,77,72),trim)
        arch(p,x,178,63,69,cream,shadow,trim)
        p.l((138,132,112),(x+1,251),(x+63,251),3)
        for dx in range(4,62,8):p.l((57,69,67),(x+dx,227),(x+dx,249),2)
        p.l((70,79,74),(x-4,226),(x+67,226),2)
        for dx in (-8,70):p.r(trim,(x+dx,174,5,181))
    for yy in (160,255,264,359):p.r(trim,(15,yy,1021,5))
    p.r((177,165,136),(8,366,1036,8));p.r((101,100,85),(2,375,1047,7))
    # Colonial tower above the full double arcade, rather than a modern shortened front.
    plaster(p,474,67,105,98,(225,212,179),11)
    p.r(trim,(466,66,122,9));p.r(trim,(468,156,118,8))
    p.r((112,111,91),(485,43,82,27));arch(p,503,34,45,43,cream,(74,81,72),trim)
    p.r(trim,(484,28,84,8))
    roof(p,476,8,99,(139,84,56),22)
    for x in (480,568):p.c(trim,(x,27),4)
    p.c((113,107,86),(527,116),30);p.c(trim,(527,116),25)
    for n in range(12):
        a=n*math.tau/12;p.l((83,86,73),(527+math.cos(a)*20,116+math.sin(a)*20),(527+math.cos(a)*23,116+math.sin(a)*23),1)
    p.l((55,65,62),(527,116),(527,99),2);p.l((55,65,62),(527,116),(540,121),2)
    return p.image()

@lru_cache(maxsize=3)
def recova():
    p=Painter(810,247);cream=(190,173,139);trim=(223,207,167)
    plaster(p,12,63,786,161,cream,67);roof(p,10,34,791,(133,78,51),30)
    for n in range(9):
        arch(p,26+n*85,98,57,118,cream,(63,72,65),trim)
        p.r(trim,(19+n*85,88,6,130))
    p.r(trim,(8,78,794,9));p.r(trim,(6,221,802,8))
    p.p(cream,[(324,63),(405,3),(485,63)])
    p.l(trim,(318,63),(405,0),5);p.l(trim,(405,0),(492,63),5)
    p.e((107,112,93),(386,31,38,23),2)
    return p.image()

@lru_cache(maxsize=3)
def tucuman_house():
    p=Painter(750,300);cream=(232,217,182);blue=(45,84,108);trim=(250,235,203)
    plaster(p,20,115,710,164,cream,193);roof(p,17,81,718,(146,81,50),29)
    for x in (65,175,520,630):
        window(p,x,145,46,75,cream,blue)
        for dx in range(3,44,8):p.l((43,64,68),(x+dx,143),(x+dx,220),2)
        p.l((43,64,68),(x-2,165),(x+48,165),2)
    # The recognizable concave/convex portal with twisted columns.
    p.p(trim,[(266,278),(266,116),(285,100),(303,107),(319,77),(340,68),(355,51),(376,42),(398,51),(413,68),(437,77),(453,107),(472,100),(488,116),(488,278)])
    p.p((193,180,149),[(297,122),(310,100),(340,91),(356,72),(375,63),(395,72),(411,91),(441,100),(456,122)],2)
    p.r(blue,(326,130,102,145),3)
    p.a((33,61,80),(326,108,102,57),0,math.pi,3)
    for x in (331,382):
        for y in (143,191):p.r((28,62,83),(x,y,40,39),1,2)
    p.l((31,54,69),(378,130),(378,275),3)
    for x in (303,446):
        p.r((193,183,151),(x-8,139,17,124),5)
        for y in range(142,259,13):p.a(trim,(x-10,y,22,19),-.4,2.7,4)
        p.r(trim,(x-14,127,29,12));p.r(trim,(x-14,260,29,13))
    for x,side in ((285,-1),(465,1)):
        p.a((186,174,142),(x-15,88,34,36),0,math.tau,3)
    p.e((177,154,115),(362,88,29,31),2)
    p.r((182,163,128),(10,280,733,10));p.r((106,110,95),(0,291,750,8))
    return p.image()

@lru_cache(maxsize=3)
def congress():
    p=Painter(1050,440);stone=(160,162,148);light=(207,203,171);shade=(76,92,94);copper=(74,128,117)
    plaster(p,20,248,1010,172,stone,289)
    for wing in (35,688):
        for row in range(2):
            for n in range(7):
                x=wing+n*43;y=269+row*64
                p.r(shade,(x,y,24,43));p.r((192,163,108),(x+4,y+4,16,31))
                p.r(light,(x-5,y-5,34,4));p.r(light,(x-4,y+45,33,5))
        p.r(light,(wing-14,233,325,13));p.r(shade,(wing-9,420,325,9))
    # Central portico and flanking square pavilions.
    p.r((120,138,129),(352,191,341,226))
    for n in range(8):
        x=367+n*42
        p.r(shade,(x+5,266,21,136));p.r(light,(x,259,20,142))
        p.r(light,(x-4,252,29,10));p.r(light,(x-3,401,28,11))
    p.p(stone,[(330,251),(524,171),(716,251)])
    p.l(light,(328,251),(524,168),5);p.l(light,(524,168),(719,251),5)
    p.p(shade,[(365,239),(524,186),(682,239)],2)
    for dx in (-65,-32,0,32,65):p.c(light,(524+dx,223-abs(dx)*.16),7)
    p.r(light,(333,249,385,10))
    for x in (293,698):
        p.r(stone,(x,207,61,208));p.r(light,(x-9,197,78,15))
        p.p(copper,[(x-7,197),(x+6,174),(x+48,174),(x+68,197)])
        p.c(light,(x+28,169),6)
    # Verdigris dome, drum, ribs and lantern, rather than a repeated semicircle.
    p.r(stone,(440,139,165,55));p.e(copper,(432,39,182,154))
    p.r(copper,(430,127,186,28))
    for n in range(9):
        dx=(n-4)*20
        p.a(mix(copper,light,.4),(432+abs(dx)*.35,39,182-abs(dx)*.7,154),.1,math.pi-.1,2)
    for n in range(9):
        p.r(shade,(446+n*18,154,9,28));p.r(light,(442+n*18,151,4,33))
    p.r(light,(431,184,185,8));p.r(copper,(501,21,44,33))
    p.p(copper,[(494,22),(523,1),(552,22)])
    p.l(light,(523,2),(523,0),3)
    for x in (509,528):p.r((210,177,109),(x,27,8,15))
    for n in range(5):p.r(mix(stone,light,n*.12),(3+n*5,422+n*3,1044-n*10,4))
    return p.image()

@lru_cache(maxsize=3)
def sky(stage):
    s=pg.Surface((W,H))
    top,horizon=(((62,86,99),(186,176,148)),((69,119,141),(224,199,149)),((21,34,60),(139,120,114)))[stage]
    for y in range(H):line(s,mix(top,horizon,min(1,y/610)),(0,y),(W,y))
    rng=random.Random(1600+stage)
    for j in range(14):
        x=rng.randrange(-120,W);y=rng.randrange(120,330);w=rng.randrange(140,330)
        polygon(s,mix(horizon,top,.35+j%3*.12),[(x,y+12),(x+w*.14,y-4),(x+w*.5,y-12),(x+w*.76,y+3),(x+w,y+18)])
    if stage==1:
        glow(s,(1060,161),106,(246,216,154));circle(s,(239,213,158),(1060,161),28)
    elif stage==2:
        for j in range(19):circle(s,(173,176,176),(rng.randrange(W),rng.randrange(105,230)),1)
    return s

def background(s,stage,camera,t):
    s.blit(sky(stage),(0,0))
    # Low terrain or estuary, deliberately no alpine mountains in Buenos Aires.
    if stage==1:
        for layer in range(2):
            offset=camera*(.035+layer*.025)
            for n in range(int(offset//600)-1,int(offset//600)+4):
                x=n*600-offset;col=(111,147,131) if not layer else (88,130,117)
                polygon(s,col,[(x-100,490),(x+90,394-layer*8),(x+270,374+layer*13),(x+570,462),(x+640,610)])
    else:
        rect(s,(115,139,136) if stage==0 else (78,98,110),(0,422,W,125))
        if stage==0:
            for n in range(18):
                x=(n*97-camera*.08)%W;y=432+n%6*10
                line(s,(172,170,144),(x,y),(x+48,y),1)
            for n in range(3):
                x=(180+n*460-camera*.09)%(W+300)-100
                polygon(s,(85,112,112),[(x,439),(x+66,439),(x+56,450),(x+11,450)])
                line(s,(84,103,103),(x+35,439),(x+35,381),2)
                polygon(s,(186,183,153),[(x+33,385),(x+7,432),(x+33,432)])
    offset=camera*.15
    for n in range(int(offset//140)-1,int(offset//140)+12):
        x=n*140-offset;h=48+(n*37)%72 if stage<2 else 100+(n*47)%110
        col=(105,126,121) if stage<2 else (65,83,99)
        rect(s,col,(x,484-h,136,h+47))
        if stage<2:polygon(s,(115,113,99),[(x-3,484-h),(x+24,471-h),(x+113,471-h),(x+140,484-h)])
        else:
            for xx in range(12,128,23):
                for yy in range(int(495-h),481,25):rect(s,(130,132,120),(x+xx,yy,6,9))
    rect(s,(105,104,87) if stage<2 else (67,75,81),(0,539,W,45))
    for yy in range(584,H):
        line(s,mix((50,65,65),(19,31,39),(yy-584)/(H-584)),(0,yy),(W,yy))
    for j in range(6):
        yy=547+j*7
        line(s,(136,125,99) if stage<2 else (88,87,83),(0,yy),(W,yy),1)

def _place(s,img,x,base):
    if -img.get_width()<x<W:s.blit(img,(int(x),int(base-img.get_height())))

def street(s,world,camera,t):
    stage=world.stage
    offset=camera*.55
    # Independent, varied house fronts replace the repeating monumental building.
    first=int(offset//267)-2
    landmark_camera=world.data['zones'][2][0] if stage<2 else world.width-W
    landmark_x=landmark_camera*.55+620
    for n in range(first,first+9):
        wx=n*267
        if abs(wx-landmark_x)<(540 if stage!=1 else 395):continue
        img=house(stage,n)
        _place(s,img,wx-offset,565+(n%3-1)*4)
    if stage==0:
        recova_x=world.data['zones'][1][0]*.55+540
        _place(s,recova(),recova_x-offset-405,564)
        _place(s,cabildo(),landmark_x-offset-525,565)
    elif stage==1:
        _place(s,tucuman_house(),landmark_x-offset-375,566)
        # Courtyard walls and citrus trees are in a different district from the house.
        patio_x=world.data['zones'][1][0]*.55-camera*.55+440
        if -400<patio_x<W+400:
            for dx in (0,135,300):
                x=patio_x+dx
                rect(s,(150,149,111),(x-110,490,210,78))
                line(s,(90,82,63),(x,538),(x,423),7)
                for j in range(7):
                    circle(s,(77,114,80),(x+math.sin(j*2)*38,425+math.cos(j*2)*22),24)
                    circle(s,(205,151,63),(x+math.sin(j*3)*35,420+math.cos(j*3)*19),3)
    else:
        _place(s,congress(),landmark_x-offset-525,566)
    # Street lamps and period furniture are at a nearer depth.
    off=camera*.72
    for n in range(int(off//430)-1,int(off//430)+5):
        x=n*430-off+90
        lamp(s,x,566,stage,t)
        if n%2==0 and stage==2:
            bench(s,x+90,566)
        elif stage<2:
            barrel(s,x+82,563,1)
    if stage==0:
        # Overcast wet street: low contrast rain stays behind the playable route.
        for j in range(24):
            x=(j*93-camera*.25-t*30)%W;y=130+(j*63+t*110)%420
            line(s,(156,169,161),(x,y),(x-3,y+8),1)
    era=('BUENOS AIRES · MAYO DE 1810','TUCUMÁN · JULIO DE 1816','BUENOS AIRES · MEMORIA Y DEMOCRACIA')[stage]
    text(s,era,(W-26,121),11,(242,211,158),True,'topright')

def lamp(s,x,y,stage,t):
    dark=(48,59,57) if stage<2 else (38,50,62)
    line(s,dark,(x,y),(x,y-119),5);rect(s,dark,(x-6,y-8,12,8),2)
    if stage<2:
        line(s,dark,(x,y-120),(x+20,y-120),4)
        polygon(s,dark,[(x+8,y-122),(x+16,y-135),(x+24,y-122)])
        rect(s,(172,159,113),(x+10,y-122,13,22))
        rect(s,dark,(x+8,y-102,17,4));line(s,dark,(x+16,y-121),(x+16,y-103),2)
    else:
        line(s,dark,(x,y-119),(x+27,y-127),5)
        rect(s,(211,188,125),(x+17,y-128,26,6),3)
        glow(s,(x+29,y-122),67,(244,195,111))
        line(s,(107,108,98),(x,y-36),(x+25,y-35),2)

def barrel(s,x,y,scale=1):
    w=22*scale;h=31*scale
    rect(s,(103,76,51),(x-w/2,y-h,w,h),5)
    for dx in (-6,0,6):line(s,(136,101,61),(x+dx*scale,y-h+3),(x+dx*scale,y-3),1)
    for yy in (y-h+5,y-6):line(s,(56,60,52),(x-w/2,yy),(x+w/2,yy),3)
    pg.draw.ellipse(s,(144,110,69),pg.Rect(x-w/2,y-h,w,6*scale))

def bench(s,x,y):
    for yy in (y-30,y-22,y-11):line(s,(133,100,69),(x-30,yy),(x+31,yy),5)
    for dx in (-22,23):line(s,(38,49,53),(x+dx,y-35),(x+dx+5,y),4)

@lru_cache(maxsize=160)
def platform_tile(stage,w,h,seed,moving):
    s=pg.Surface((w,h+18),pg.SRCALPHA);rng=random.Random(seed+stage*101)
    if h>90:
        base=(96,78,56) if stage<2 else (70,75,78)
        s.fill(base,pg.Rect(0,0,w,h))
        for row,y in enumerate(range(14,h,16)):
            for x in range(-23 if row%2 else -2,w,46):
                col=mix(base,(179,143,91) if stage<2 else (145,143,128),rng.uniform(.05,.28))
                rect(s,col,(x+1,y+1,44,14),1)
                line(s,mix(base,(30,36,39),.4),(x,y),(x+45,y),1)
        # Cobbles/asphalt define a clear, bright collision edge.
        rect(s,(185,160,116) if stage<2 else (151,153,143),(0,0,w,12))
        for x in range(-10,w,21):
            col=(139,127,102) if stage<2 else (98,107,111)
            rect(s,col,(x,3,18+rng.randrange(3),6),2)
            line(s,mix(col,PAPER,.35),(x+2,3),(x+13,3),1)
        line(s,(232,205,152) if stage<2 else (189,198,192),(0,0),(w,0),2)
        if stage==0:
            for x in range(36,w-40,129):
                pg.draw.ellipse(s,(122,137,126),(x,5,43,4))
        for _ in range(w//95):
            x=rng.randrange(w);y=rng.randrange(25,h)
            line(s,mix(base,(34,38,37),.5),(x,y),(x+7,y+8),1)
    else:
        wood=(113,80,48) if stage<2 else (70,92,102)
        rect(s,wood,(0,0,w,min(h,21)),2)
        for x in range(2,w,14):
            line(s,mix(wood,(232,199,137),.3),(x,1),(x,10),1)
            circle(s,(42,48,48),(x+4,5),1)
        line(s,(214,181,116) if stage<2 else (181,193,187),(0,0),(w,0),3)
        line(s,(43,49,48),(2,15),(w-2,15),4)
        for x in range(10,w-20,45):
            line(s,mix(wood,(17,33,40),.3),(x,16),(x+23,min(h+9,30)),4)
            line(s,mix(wood,(17,33,40),.3),(x+23,min(h+9,30)),(x+43,16),4)
        if moving:
            line(s,CYAN,(0,2),(w,2),2)
            for x in (12,w-12):circle(s,CYAN,(x,10),3,1)
    return s

def props(s,world,camera,t):
    for n,k in enumerate(world.data['main_nodes']):
        p=world.platforms[k].rect
        if p.right<camera-50 or p.left>camera+W+50:continue
        x=p.right-camera-80;y=p.top
        if n%3==0:
            barrel(s,x,y,1.1)
            rect(s,(110,83,54),(x+18,y-30,31,30),2)
            line(s,(178,142,85),(x+20,y-28),(x+46,y-3),2)
            line(s,(178,142,85),(x+46,y-28),(x+20,y-3),2)
        elif n%3==1 and not world.stage==2:
            # Planter placed behind play, with clear leaves and terracotta rim.
            polygon(s,(142,83,57),[(x-10,y-20),(x+11,y-20),(x+7,y),(x-6,y)])
            line(s,(192,121,72),(x-12,y-20),(x+13,y-20),4)
            for j in range(5):
                line(s,(69,105,71),(x,y-20),(x-13+j*6,y-38-(j%2)*8),3)
        elif world.stage==2:
            bench(s,x,y)
