"""Map-specific palettes and animated ambient storytelling; no gameplay damage."""
from dataclasses import dataclass,replace
from functools import lru_cache
import math
import pygame as pg
from .levels import ERAS


@dataclass(frozen=True)
class Mood:
    description: str
    weather: str
    sky: tuple
    horizon: tuple
    kind: str


MOODS=(
 Mood('Brisa marina, olas y reptiles en vuelo','coast',(16,54,69),(137,190,164),'jungle'),
 Mood('Cañón seco, estratos y polvo de roca','dust',(57,40,40),(199,149,99),'desert'),
 Mood('Cielo en llamas, meteoros, humo y cenizas','impact',(35,17,25),(211,80,43),'ash'),
 Mood('Ventisca sobre una estepa helada','snow',(32,53,83),(172,208,220),'ice'),
 Mood('Refugio oscuro con fogata y luz cálida','firelight',(11,19,32),(47,64,84),'cave'),
 Mood('Caverna violeta con pinturas y antorchas','cave',(27,22,47),(78,72,104),'cave'),
 Mood('Ágora luminosa y vida entre las columnas','agora',(67,96,115),(234,195,139),'ruins'),
 Mood('Puerto azul con barcos, gaviotas y mareas','harbor',(30,60,85),(153,177,179),'ruins'),
 Mood('Gradas de piedra y antorchas al atardecer','torch',(57,38,68),(224,140,91),'ruins'),
 Mood('Campos verdes, molino y semillas al viento','fields',(34,66,70),(169,190,137),'fields'),
 Mood('Ciudad de mercado bajo la lluvia','rain',(34,42,58),(121,136,146),'castle'),
 Mood('Catedral nocturna bañada por vidrieras','cathedral',(17,21,52),(74,76,122),'castle'),
 Mood('Hollín y nubes de vapor entre pistones','steam',(35,30,37),(153,103,78),'factory'),
 Mood('Una locomotora atraviesa el paisaje','railway',(66,59,70),(213,166,119),'factory'),
 Mood('Noche eléctrica, faroles y cables encendidos','electric',(10,22,47),(48,77,104),'factory'),
)


@lru_cache(maxsize=15)
def palette_for(era,stage=0):
    base=ERAS[era]
    mood=MOODS[era*3+stage]
    changes=dict(sky=mood.sky,horizon=mood.horizon,kind=mood.kind)
    if mood.kind=='ash':
        changes.update(far=(103,44,43),near=(48,31,36),rock=(43,35,39),top=(173,92,66),accent=(255,166,78))
    elif mood.kind=='desert':
        changes.update(far=(143,93,73),near=(94,66,61),rock=(76,55,51),top=(198,155,103),accent=(255,205,132))
    elif mood.kind=='cave':
        changes.update(far=(46,51,73),near=(28,36,54),rock=(43,47,64),top=(139,160,174),accent=(237,172,114) if stage==1 else (177,184,236))
    elif mood.kind=='fields':
        changes.update(far=(77,107,92),near=(43,74,68),rock=(53,65,58),top=(157,181,116),accent=(245,204,132))
    elif mood.weather in ('agora','harbor'):
        changes.update(far=(125,135,143) if mood.weather=='harbor' else (169,137,113),
                       near=(70,89,103) if mood.weather=='harbor' else (112,96,88))
    elif mood.weather=='electric':
        changes.update(far=(36,58,83),near=(23,40,62),rock=(37,48,65),top=(136,162,178),accent=(255,215,135))
    return replace(base,**changes)


def burnt_tree(surface,x,base,height,color):
    from .art import polygon,line
    polygon(surface,color,[(x-10,base),(x+11,base),(x+1,base-height),(x-9,base-height+17)])
    for j in range(3):
        yy=base-height*(.35+j*.18)
        side=-1 if j%2 else 1
        line(surface,color,(x,yy),(x+side*height*.22,yy-height*.17),max(2,int(height*.035)))
        line(surface,color,(x+side*height*.22,yy-height*.17),(x+side*height*.29,yy-height*.15),3)


def ambient_back(surface,world,camera,time):
    from .art import polygon,line,circle,glow,mix,rect,W,H
    mood=MOODS[world.level_id]
    era=palette_for(world.index,world.stage)
    weather=mood.weather
    if weather=='impact':
        # The devastation remains visible for the whole route and the boss arena.
        for layer in range(2):
            factor=.12+layer*.13
            spacing=190+layer*37
            offset=camera*factor
            start=int(offset//spacing)-1
            for n in range(start,start+10):
                x=n*spacing-offset
                base=526+layer*28
                height=100+(n*37)%115
                burnt_tree(surface,x,base,height,era.near if layer else era.far)
                glow(surface,(x+33,base-14),60,(244,103,43))
                flicker=math.sin(time*5+n)*9
                polygon(surface,(171,65,39),[(x+10,base),(x+21,base-39-flicker),(x+29,base-23),
                        (x+37,base-66+flicker),(x+55,base)])
                polygon(surface,(243,143,61),[(x+22,base),(x+33,base-33-flicker*.4),(x+43,base)])
                for j in range(4):
                    yy=base-90-j*43-(time*9+n*5)%30
                    xx=x+43+j*12+math.sin(time*.3+n+j)*14
                    circle(surface,mix(era.sky,era.far,.3+j*.12),(xx,yy),28+j*7)
        # Distant streaks are decorative: they never collide with Crono.
        for j in range(7):
            phase=(time*.16+j*.173)%1
            x=(j*219+camera*.07)%1550-160-phase*185
            y=95+phase*322
            tail=36+j%3*19
            line(surface,(138,66,49),(x+tail*1.5,y-tail),(x,y),7)
            line(surface,(237,128,63),(x+tail,y-tail*.67),(x,y),3)
            circle(surface,(255,209,132),(x,y),3+j%2)
        glow(surface,(850-camera*.055,436),180,(255,119,53))
    elif weather=='dust':
        for j in range(5):
            y=360+j*31
            x=(time*19+j*291-camera*.18)%1650-200
            polygon(surface,mix(era.horizon,era.near,.62),[(x,y),(x+160,y-5),(x+300,y+7),(x+112,y+11)])
    elif weather in ('firelight','cave'):
        polygon(surface,era.near,[(0,91),(W,91),(W,145),(1180,130),(1030,219),(887,141),(755,232),
                                   (620,147),(440,224),(278,139),(141,201),(0,153)])
        for n in range(7):
            x=(n*231-camera*.22)%1530-120
            polygon(surface,era.far,[(x,108),(x+24,210+n%3*23),(x+43,108)])
        if weather=='firelight':
            glow(surface,(830-camera*.15,478),175,(255,161,78))
    elif weather=='harbor':
        for j in range(9):
            y=460+j*9
            line(surface,mix(era.horizon,era.near,.45),(0,y),(W,y),2)
        for j in range(5):
            x=(j*255+time*10-camera*.1)%(W+160)-80
            y=199+j%3*35
            line(surface,era.accent,(x-9,y),(x,y+4),1)
            line(surface,era.accent,(x,y+4),(x+9,y),1)
    elif weather=='fields':
        for row in range(5):
            y=440+row*22
            polygon(surface,mix(era.far,era.top,.1+row*.09),[(0,y+24),(W,y-35),(W,y+3),(0,y+63)])
    elif weather=='cathedral':
        shafts=pg.Surface((W,H),pg.SRCALPHA)
        for n,color in enumerate(((137,164,244,16),(196,137,239,15),(122,220,209,14))):
            x=380+n*280-camera*.08
            polygon(shafts,color,[(x,120),(x+24,120),(x+270,584),(x+75,584)])
        surface.blit(shafts,(0,0))
    elif weather=='electric':
        for n in range(8):
            x=n*181-camera*.09
            glow(surface,(x,350+n%3*33),60,(244,197,106))
    elif weather=='steam':
        for n in range(6):
            x=(n*265-camera*.18+time*4)%1540-130
            y=230+n%3*48
            circle(surface,mix(era.far,era.horizon,.12),(x,y),33+n%3*10)


def ambient_front(surface,world,camera,time):
    from .art import line,circle,polygon,glow,mix,W,H
    mood=MOODS[world.level_id]
    era=palette_for(world.index,world.stage)
    weather=mood.weather
    if weather in ('impact','snow','rain','dust','fields'):
        count=64 if weather in ('snow','rain','impact') else 25
        for n in range(count):
            if weather=='impact':
                x=(n*137.31+time*25-camera*.36)%W
                y=95+(n*61.7+time*(20+n%4*6))%550
                color=(233,159,90) if n%5==0 else (130,116,112)
                circle(surface,color,(x,y),1 if n%3 else 2)
            elif weather=='snow':
                x=(n*131.7-time*55-camera*.4+math.sin(time+n)*19)%W
                y=95+(n*72.1+time*(28+n%4*8))%550
                circle(surface,(196,216,223),(x,y),1+n%3)
            elif weather=='rain':
                x=(n*139.1-time*83-camera*.4)%W
                y=95+(n*71.3+time*410)%535
                line(surface,(130,155,173),(x,y),(x-4,y+14),1)
            elif weather=='fields':
                x=(n*163.3+time*37-camera*.4)%W
                y=260+(n*89.7+math.sin(time*.6+n)*23)%310
                line(surface,(206,202,136),(x,y),(x+4,y-2),1)
            else:
                x=(n*151.3+time*35-camera*.5)%W
                y=300+(n*43.4+math.sin(time*.4+n)*17)%290
                circle(surface,(201,165,123),(x,y),1)
    if weather=='railway':
        # A complete, moving train passes behind the foreground UI, above the pits.
        x=(time*55-camera*.14)%2400-700
        from .art import rect
        for n in range(3):
            xx=x-n*154
            rect(surface,era.near,(xx,452,139,57),3)
            for j in range(4):
                rect(surface,era.accent,(xx+15+j*28,463,16,17),1)
            for dx in (25,112):
                circle(surface,era.rock,(xx+dx,514),13)
        for j in range(5):
            circle(surface,mix(era.far,era.horizon,.35),(x+90+j*18,408-j*15),11+j*3)
