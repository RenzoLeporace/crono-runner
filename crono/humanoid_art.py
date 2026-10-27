"""Articulated bodies with distinct equipment and silhouettes for each epoch."""
from functools import lru_cache
import math
import pygame as pg
from .argentina_art import Painter
from .humanoid_roster import HEIGHTS
from .art import text,circle,glow,GOLD,PAPER

@lru_cache(maxsize=128)
def civilian_guard(era,kind,frame,variant):
    p=Painter(112,112);ink=(29,36,43);skin=(190,139,101)
    historic=variant in ('berlin','detente');industrial=era==4
    cloth=(124,105,79) if industrial else (100,119,91) if historic else (47,81,120)
    trim=(205,178,117);gait=math.sin(frame*math.tau/8)*5
    for dx in (-9,9):
        p.l(ink,(54+dx,72),(54+dx+gait*(1 if dx>0 else -1),103),10)
        p.l(cloth,(54+dx,73),(54+dx+gait*.5,92),7)
        p.r(ink,(49+dx+gait*(1 if dx>0 else -1),99,16,8),2)
    p.r(ink,(38,36,34,42),5);p.r(cloth,(41,38,28,36),4)
    p.l(trim,(44,42),(64,65),3);p.r((78,61,45),(38,66,35,6),1)
    for y in (45,52,59):p.c(trim,(55,y),1)
    for x in (43,61):p.r((72,75,67),(x,68,7,9),1)
    p.r(skin,(49,29,13,11),2);p.e(skin,(44,12,24,25));p.c(ink,(62,24),1)
    p.p(skin,[(65,22),(72,27),(65,29)])
    if industrial:
        p.e((88,71,58),(39,9,32,14));p.r(ink,(41,18,33,5),2)
        p.r((142,114,75),(44,40,4,26));p.r((142,114,75),(64,40,4,26))
    elif historic:
        p.p(cloth,[(38,14),(44,7),(64,7),(72,16),(67,21),(40,21)])
        p.r((54,65,52),(40,20,34,5),1);p.c(trim,(55,15),2)
    else:
        p.e((43,62,81),(40,9,31,17));p.r((29,42,58),(40,20,35,5),1)
        p.r((184,200,206),(49,42,11,7),1)
    p.l(ink,(43,43),(31,62),9);p.l(cloth,(43,43),(32,61),6)
    p.l(skin,(32,62),(42,69),5);p.l(cloth,(66,44),(76,56),8);p.l(skin,(76,56),(83,52),5)
    if industrial:
        p.l((112,82,49),(85,44),(85,100),5);p.r((183,152,85),(81,35,9,15),2)
    else:
        p.l((88,66,47),(57,66),(82,53),6);p.l(ink,(78,55),(105,44),4)
        p.l((160,168,164),(101,46),(109,42),2)
    if kind=='armored':
        p.p((64,76,85),[(15,46),(43,46),(46,81),(29,94),(13,80)])
        p.p((184,192,187),[(15,46),(43,46),(46,81),(29,94),(13,80)],2)
    return pg.transform.smoothscale(p.image(),(90,90))

@lru_cache(maxsize=512)
def figure(era,kind,stage,frame,warning=False,variant=''):
    if era in (4,6):return civilian_guard(era,kind,frame,variant)
    if variant=='timbuktu':
        p=Painter(112,112);step=math.sin(frame*math.tau/8)*5;ink=(37,47,55);cloth=(72,103,129);trim=(206,177,115)
        for dx in (-7,7):p.l(ink,(54+dx,79),(54+dx+step*(1 if dx>0 else -1),103),8)
        p.p(ink,[(38,39),(67,39),(79,95),(31,95)]);p.p(cloth,[(40,42),(65,42),(74,92),(36,92)])
        for xx in (43,57):p.l(trim,(xx,49),(xx-2,82),2)
        p.e((133,90,62),(44,17,23,29));p.e((223,212,175),(37,9,36,24));p.r((213,197,153),(37,27,36,7),3)
        p.l(ink,(58,29),(63,29),2);p.l(trim,(45,46),(47,71),6)
        if kind=='sentry':p.a(trim,(69,33,21,55),-.9,1.1,3);p.l(ink,(75,37),(75,84),1)
        else:p.l((113,82,53),(80,30),(80,105),4);p.p((191,194,176),[(80,13),(74,34),(86,34)])
        if kind=='armored':p.e(ink,(18,53,37,39));p.e((154,117,68),(21,56,31,33));p.c(trim,(37,72),5)
        return p.image()
    p=Painter(112,112)
    step=math.sin(frame*math.tau/8)*6
    skin=(173,123,84);ink=(30,37,42);steel=(159,176,184);gold=(207,163,77)
    robot=era in (4,6)
    cloth={2:(224,213,179),3:(77,106,134),4:(101,92,73),5:(108,116,89),6:(155,208,211),8:(231,211,166)}[era]
    if era==5 and stage==0:cloth=(123,110,89)
    # Distinct rear equipment remains readable behind the moving limbs.
    if era==2:p.p((133,58,48),[(43,39),(35,81),(68,79),(64,39)])
    if era==3:p.p((96,53,64),[(39,39),(32,84),(66,78),(65,39)])
    if era==4:
        p.r(ink,(28,33,25,45),5);p.r(gold,(30,37,20,35),6)
        p.r(ink,(30,16,10,28),2);p.r(gold,(28,14,14,6),1)
        for yy in (43,51,59):p.l(ink,(33,yy),(47,yy),2)
    if era==5:p.r((71,77,63),(29,40,18,35),3)
    if era==6:
        p.p(ink,[(31,38),(40,28),(68,29),(79,43),(69,72),(35,72)])
        p.l((79,236,219),(31,46),(28,27),3)
    # Knees and ankles articulate; all soles share the collision plane.
    for side in (-1,1):
        hip=(53+side*7,72);knee=(53+side*10+side*step*.4,85);foot=(53+side*10+side*step,104)
        p.l(ink,hip,knee,11);p.l(ink,knee,foot,9)
        p.l(cloth if robot else (107,106,92),hip,knee,7)
        p.l(steel if robot or era==3 else gold if era==2 else skin,knee,(foot[0],100),6)
        p.r(ink,(foot[0]-4,100,12,6),2)
        if robot:
            p.c(gold if era==4 else steel,knee,5);p.c(ink,knee,2)
        elif era==8:
            p.l((81,62,46),(foot[0]-4,102),(foot[0]+8,102),3)
    if era in (2,8):
        p.r(skin,(42,36,24,30),4)
        p.p(cloth,[(41,64),(65,64),(71,78),(36,78)])
        for xx in range(40,67,5):p.l(gold,(xx,67),(xx-2,76),1)
        p.r(gold,(40,61,28,5),1)
        if era==2:p.p((159,119,64),[(42,39),(63,39),(66,61),(40,61)])
        else:
            p.p((57,155,166),[(40,37),(68,37),(64,46),(44,46)])
            for xx in range(44,67,5):p.l(gold,(xx,39),(xx+1,43),2)
    else:
        p.r(ink,(39,36,31,39),5);p.r(cloth,(41,38,27,34),4)
        p.r((76,63,46) if era==5 else gold if era==4 else steel,(39,64,31,5),1)
        if era==3:
            for yy in range(42,64,4):
                for xx in range(43,66,5):p.c((113,139,152),(xx+(yy%3),yy),1)
            p.p((58,83,106),[(46,39),(60,39),(62,69),(45,69)])
            p.l((196,182,130),(53,41),(53,63),2)
        elif era==5:
            p.l((171,151,106),(42,39),(64,64),4)
            for xx in (42,56,64):p.r((137,124,85),(xx,62,6,8),1)
            for yy in (46,52,58):p.c((192,179,133),(54,yy),1)
        elif era==4:
            p.r(gold,(44,42,21,18),3);p.c(ink,(54,51),6);p.c((245,172,74),(54,51),3)
            for xx in (43,64):
                for yy in (39,65):p.c(steel,(xx,yy),1)
        else:
            p.p(steel,[(42,40),(63,40),(59,58),(47,58)])
            p.l((49,124,137),(47,45),(59,45),3);p.c((83,245,219),(54,53),2)
    # Neck, face, era-specific headgear.
    p.r(ink if robot else skin,(48,30,12,10),2)
    if robot:
        if era==4:
            p.r(ink,(42,17,26,20),4);p.r(gold,(44,18,22,17),4)
            p.r(ink,(45,23,19,7),2);p.c((248,183,83),(59,26),3)
            p.l(steel,(46,34),(62,34),2)
        else:
            p.p(steel,[(43,14),(63,14),(70,23),(65,35),(43,35),(39,25)])
            p.r(ink,(45,21,22,8),2);p.l((79,247,224),(48,24),(64,24),3)
            p.p((68,115,132),[(44,29),(64,29),(58,35),(48,35)])
    else:
        p.e(skin,(44,18,23,23));p.p(skin,[(62,25),(70,30),(64,32)])
        p.c(ink,(61,27),1)
        if era==2:
            p.a(gold,(41,15,30,27),0,math.pi,5)
            p.r(gold,(42,21,7,20),2);p.l(gold,(65,20),(65,29),3)
            p.p((155,63,48),[(42,18),(39,7),(58,6),(71,16),(67,19),(57,14)])
        elif era==3:
            p.p(steel,[(44,13),(64,14),(70,24),(67,39),(44,39),(40,24)])
            p.l(ink,(49,24),(67,24),3)
            for xx in (52,57,62):p.l(ink,(xx,30),(xx,36),1)
            if kind=='charger':p.p((160,66,73),[(48,15),(44,4),(54,1),(62,9),(62,15)])
        elif era==5:
            if stage==0:
                p.r(cloth,(42,16,26,9),3);p.r(ink,(41,24,30,4),1)
            else:
                p.e(cloth,(39,13,32,20));p.r((78,88,65),(38,26,34,4),2)
                p.l((77,72,56),(45,30),(53,39),1)
        else:
            p.r((34,53,56),(43,16,25,9),2);p.r(gold,(42,22,28,5),1)
            p.l((230,222,189),(46,18),(63,18),2)
    # Arms and weapons. Each role reads as an actual item rather than a color.
    p.l(ink,(43,42),(34,58),9);p.l(skin if not robot and era in (2,8) else cloth,(43,42),(34,57),6)
    p.l(ink,(64,42),(74,55),9);p.l(skin if not robot and era in (2,8) else cloth,(64,42),(74,55),6)
    hand=steel if robot else skin
    p.l(hand,(34,57),(39,65),5);p.l(hand,(74,55),(81,52),5)
    if era in (2,8):
        if kind=='sentry':
            p.a((161,112,60),(68,31,27,52),-1.4,1.4,3);p.l((224,206,162),(82,33),(82,81),1)
            p.l((223,205,163),(65,54),(106,54),2)
        else:
            p.l((136,93,53),(83,23),(83,100),3)
            p.p(steel,[(78,25),(83,12),(88,25)])
            if era==2:
                p.e(gold,(22,48,35,36));p.e((116,77,42),(26,52,27,28),2);p.c(gold,(40,66),5)
                if kind=='armored':p.e((231,197,113),(20,46,39,40),3)
            else:
                p.r((121,73,42),(19,47,28,40),9);p.r(cloth,(21,49,24,36),8)
                for yy in range(54,81,8):p.l((149,107,60),(23,yy),(43,yy),1)
    elif era==3:
        if kind=='sentry':
            p.l((121,85,58),(64,59),(101,46),5);p.l(steel,(92,38),(103,60),3)
            p.l((222,205,168),(92,38),(86,53),1);p.l((222,205,168),(103,60),(86,53),1)
        else:
            p.l(gold,(82,57),(82,66),4);p.l(steel,(82,20),(82,59),4)
            p.p((57,82,115),[(20,48),(48,48),(46,74),(34,85),(22,74)])
            p.p(steel,[(20,48),(48,48),(46,74),(34,85),(22,74)],2)
            p.l(gold,(27,55),(42,69),2)
    elif era==4:
        p.c(steel,(80,55),7);p.r(ink,(78,52,26,8),2)
        if kind=='armored':
            p.c(gold,(29,65),12);p.c(ink,(29,65),7);p.p(ink,[(16,57),(28,57),(22,66),(15,68)])
        else:p.l((241,175,81),(90,53),(104,53),3)
    elif era==5:
        p.l((87,61,43),(57,66),(81,53),6);p.l(ink,(75,56),(105,43),3)
        p.l((177,178,163),(98,44),(108,40),2)
    else:
        p.r(ink,(73,48,30,12),3);p.r((191,225,221),(81,49,23,9),2)
        p.l((73,239,219),(96,52),(107,52),2)
        if kind=='armored':
            p.p((62,123,145),[(15,45),(35,41),(48,50),(45,83),(27,90),(13,79)])
            p.p((92,244,226),[(15,45),(35,41),(48,50),(45,83),(27,90),(13,79)],2)
    if kind=='armored':
        if era==3:
            for xx in (35,65):p.e(steel,(xx,36,15,14));p.e(ink,(xx+2,38,11,10),1)
            p.p((55,77,109),[(16,45),(47,45),(48,76),(33,94),(15,77)])
            p.p(steel,[(16,45),(47,45),(48,76),(33,94),(15,77)],3)
            p.l(gold,(21,55),(42,73),3);p.l(gold,(41,54),(22,76),3)
        elif era==8:
            p.p((169,126,61),[(39,39),(68,39),(66,62),(42,62)])
            for yy in range(42,61,5):p.l(gold,(43,yy),(64,yy),2)
            p.r((124,81,43),(15,44,36,51),10);p.r((224,186,115),(18,47,30,45),9)
            p.c((134,96,48),(33,68),8);p.c(gold,(33,68),5)
            for yy in (52,84):p.l((148,103,53),(20,yy),(46,yy),2)
        elif era==2:
            for xx in (35,64):p.e(gold,(xx,35,14,13))
    if variant=='roman':
        # Roman-inspired segmented cuirass and tall shield, distinct from hoplites.
        p.r((102,108,110),(39,35,31,32),4)
        for yy in range(39,65,5):p.l((187,185,166),(41,yy),(68,yy),3)
        p.r((137,52,46),(18,45,30,49),7);p.r((207,170,89),(20,47,26,45),6,2)
        p.l((207,170,89),(23,54),(42,86),2);p.l((207,170,89),(42,54),(23,86),2)
        p.e((155,164,162),(40,12,33,18));p.r((178,179,157),(40,25,32,5),2)
        p.l((189,185,157),(44,29),(46,39),4);p.l((189,185,157),(67,28),(66,38),4)
    elif variant=='malvinas':
        # Cold-weather field clothing: helmet cover, collar and weatherproof cape.
        p.p((89,103,85),[(33,37),(72,37),(79,75),(30,75)])
        p.l((139,147,117),(37,42),(72,70),3)
        for xx in (37,56):p.r((106,115,87),(xx,58,12,13),2)
        p.e((82,100,81),(38,12,36,23));p.r((48,64,62),(38,27,36,5),2)
        p.r((131,132,106),(44,33,23,9),3)
        p.l((47,53,48),(62,64),(104,49),5)
    return pg.transform.smoothscale(p.image(),(90,90))

def draw_humanoid(s,e,camera,t,stage):
    x,y=e.rect.centerx-camera,e.rect.bottom
    warning=e.kind=='charger' and e.mode=='warning' or e.kind=='sentry' and e.timer<.5
    frame=int(e.time*10)%8 if e.kind!='sentry' and e.mode!='warning' else 0
    img=figure(e.era,e.kind,stage,frame,warning,getattr(e,'variant',''))
    if e.direction<0:img=pg.transform.flip(img,True,False)
    s.blit(img,(int(x-43),int(y-85)))
    top=y-HEIGHTS[e.era]
    if e.kind=='armored':
        from .art import armor_marker
        armor_marker(s,x,top-32)
    if e.kind=='sentry' and warning:glow(s,(x+e.direction*33,y-42),22,(243,184,94))
    if e.kind=='charger' and warning:text(s,'!',(x,top-25),19,GOLD,True,'center')
    if e.max_hp>1:
        for n in range(e.max_hp):circle(s,GOLD if n<e.hp else (65,77,84),(x+(n-(e.max_hp-1)/2)*8,top-13),2)
    if e.hit_flash:circle(s,PAPER,(x,y-42),32,2)

def draw_egypt_creature(s,e,camera,t):
    from .art import polygon,line
    x,y=e.rect.centerx-camera,e.rect.bottom
    if e.kind=='flyer':
        for side in (-1,1):
            polygon(s,(121,140,147),[(x,y-22),(x+side*48,y-49+math.sin(t*9)*8),(x+side*29,y-8),(x,y-13)])
        circle(s,(206,171,93),(x,y-27),11);polygon(s,(237,203,122),[(x+5,y-29),(x+24,y-25),(x+5,y-22)])
    else:
        pg.draw.ellipse(s,(54,118,107),(int(x-25),int(y-32),50,29))
        pg.draw.ellipse(s,(203,163,75),(int(x-17),int(y-31),34,25),2)
        line(s,(203,163,75),(x,y-31),(x,y-7),2)
        for side in (-1,1):
            for j in range(3):line(s,(43,91,87),(x+side*19,y-23+j*7),(x+side*(34+j*3),y-26+j*12),3)
        circle(s,(41,84,79),(x,y-34),9)
    if e.timer<.5:glow(s,(x,y-26),22,GOLD)
    if e.hit_flash:circle(s,PAPER,(x,y-26),27,2)
