"""Original cached vessel sprites: temporal research craft, Nile barge and corvette."""
from functools import lru_cache
import math
import pygame as pg
from .art import rect,line,circle,polygon,PAPER,CYAN,GOLD

@lru_cache(maxsize=12)
def vessel_image(kind,enemy=False,boss=False):
    from .argentina_art import Painter
    painter=Painter(220,200);s=painter.s;x,y=105,153
    rect=lambda surface,c,box,radius=0,width=0:painter.r(c,box,radius,width)
    line=lambda surface,c,a,b,width=1:painter.l(c,a,b,width)
    circle=lambda surface,c,pos,r,width=0:painter.c(c,pos,r,width)
    polygon=lambda surface,c,points,width=0:painter.p(c,points,width)
    ellipse=lambda surface,c,box,width=0:painter.e(c,box,width)
    ink=(22,38,47);metal=(90,130,147);wood=(125,77,44);edge=(224,177,103)
    if kind=='tide':
        if enemy:
            # A marine reptile: four paddles, long jaw and a two-lobed tail.
            olive=(113,137,102);belly=(202,188,139);back=(70,98,84)
            polygon(s,ink,[(130,141),(159,137),(180,141),(199,123),(196,146),(211,174),(187,164),(171,154),(146,158)])
            polygon(s,olive,[(134,143),(162,140),(181,145),(196,130),(191,148),(205,167),(186,160),(169,150),(145,154)])
            polygon(s,ink,[(73,138),(85,151),(77,181),(62,174),(58,148)])
            polygon(s,back,[(76,141),(80,152),(73,175),(65,170),(63,149)])
            polygon(s,ink,[(125,141),(141,151),(149,175),(134,173),(119,151)])
            polygon(s,back,[(127,145),(137,152),(144,169),(136,168),(124,150)])
            ellipse(s,ink,(51,123,111,42));ellipse(s,olive,(55,126,103,35))
            ellipse(s,back,(61,125,86,17));ellipse(s,belly,(62,146,86,13))
            polygon(s,ink,[(23,137),(39,127),(68,129),(81,139),(69,151),(38,153),(23,147)])
            polygon(s,olive,[(27,137),(40,131),(66,132),(76,139),(65,146),(36,148),(27,145)])
            polygon(s,belly,[(27,146),(43,147),(69,144),(64,152),(37,155),(27,151)])
            line(s,ink,(26,145),(66,143),2)
            for n in range(7):
                xx=29+n*5;polygon(s,PAPER,[(xx,145),(xx+3,145),(xx+1,149)])
            circle(s,ink,(60,136),5);circle(s,(219,173,71),(60,136),3);line(s,ink,(60,134),(60,138),1)
            circle(s,ink,(32,137),1)
            for n in range(4):line(s,(62,88,73),(75+n*4,133),(77+n*4,141),1)
            for row in range(3):
                for n in range(12):
                    xx=88+n*5;yy=132+row*6+(n%2)*2
                    ellipse(s,(132+row*8,151+row*7,111+row*5),(xx,yy,4,3),1)
            for xx in (87,103,119,135):line(s,(178,171,115),(xx,129),(xx+4,136),2)
            polygon(s,ink,[(75,150),(86,155),(70,187),(54,179),(59,165)])
            polygon(s,olive,[(76,153),(81,157),(67,181),(58,176),(63,166)])
            line(s,belly,(72,158),(62,175),1)
            polygon(s,ink,[(124,153),(135,153),(158,178),(144,183),(129,169)])
            polygon(s,olive,[(127,155),(133,156),(151,176),(144,178),(132,167)])
            line(s,belly,(135,162),(146,175),1)
        else:
            # Layered pressure hull, forward observation dome and stern screw.
            ellipse(s,ink,(35,126,151,49));ellipse(s,metal,(39,129,143,40))
            ellipse(s,(151,180,183),(48,130,119,15))
            polygon(s,ink,[(40,143),(15,130),(22,157),(43,160)])
            polygon(s,(181,153,84),[(39,145),(19,137),(26,156),(43,158)])
            line(s,ink,(32,151),(11,151),5);circle(s,(196,182,130),(13,151),12,2)
            rect(s,ink,(78,100,57,37),11);rect(s,(196,201,171),(83,104,47,27),8)
            ellipse(s,(37,90,114),(96,106,30,22));ellipse(s,(130,222,222),(101,108,21,14))
            line(s,PAPER,(104,110),(113,114),2);circle(s,(207,163,120),(92,116),5)
            line(s,ink,(88,104),(88,85),4);line(s,metal,(88,84),(102,84),4)
            rect(s,ink,(135,133,45,27),9);rect(s,CYAN,(141,138,33,13),6)
            for xx in (64,87,111):circle(s,ink,(xx,151),9);circle(s,CYAN,(xx,151),6);circle(s,(191,235,220),(xx-2,149),2)
            for xx in (49,77,105,133,160):
                line(s,(53,89,108),(xx,145),(xx+2,163),1)
                circle(s,edge,(xx,141),1);circle(s,edge,(xx+2,163),1)
            rect(s,(192,81,62),(81,130,31,4),1)
            line(s,CYAN,(48,168),(164,168),2)
    else:
        hull=[(31,142),(184,142),(170,166),(66,178),(44,168)]
        polygon(s,ink,hull);polygon(s,wood,[(35,144),(179,144),(167,162),(66,172),(48,163)])
        for yy in (149,155,161,167):line(s,edge,(49+(yy-149)*.7,yy),(174-(yy-149)*.55,yy),1)
        for xx in range(57,168,18):line(s,(77,54,40),(xx,147),(xx+3,165),1)
        line(s,(202,173,113),(28,140),(187,140),4)
        for xx in range(41,180,12):line(s,ink,(xx,139),(xx,132),2)
        line(s,edge,(39,132),(177,132),2)
        if kind=='naval':
            rect(s,ink,(39,121,31,18),3);rect(s,(170,126,72),(42,123,25,11),2)
            for xx in (47,58):rect(s,GOLD,(xx,125,5,5),1)
            for xx in (64,86,108,130,152):rect(s,ink,(xx,151,12,8),2);line(s,edge,(xx,150),(xx+12,150))
            for mast,h in ((88,115),(139,137)):
                line(s,ink,(mast,139),(mast,153-h),4)
                for sy,half in ((161-h,23),(196-h,29)):
                    line(s,(135,99,57),(mast-half-3,sy),(mast+half+3,sy),3)
                    polygon(s,ink,[(mast-half,sy),(mast+half,sy),(mast+half-5,sy+31),(mast-half+5,sy+31)])
                    polygon(s,(228,213,172),[(mast-half+2,sy+2),(mast+half-2,sy+2),(mast+half-6,sy+28),(mast-half+6,sy+28)])
                    for dx in (-12,0,12):line(s,(189,173,133),(mast+dx,sy+3),(mast+dx*.8,sy+27),1)
                line(s,(194,178,136),(mast,153-h),(37,139),1);line(s,(194,178,136),(mast,153-h),(180,139),1)
                for n in range(7):line(s,(157,145,112),(mast-12+n,128-n*10),(mast+12-n,128-n*10),1)
            line(s,edge,(178,139),(207,121),3)
            polygon(s,(227,217,183),[(145,37),(199,120),(150,117)])
            if enemy:
                rect(s,(44,109,62),(143,16,29,18));polygon(s,GOLD,[(157,18),(169,25),(157,32),(145,25)])
            else:
                for n,col in enumerate(((107,189,215),PAPER,(107,189,215))):rect(s,col,(143,16+n*6,29,6))
                circle(s,GOLD,(157,25),2)
            rect(s,ink,(143,129,40,7),3);circle(s,(65,60,48),(147,138),5)
        else:
            # Nile barge: woven canopy, square sail, reed bindings and oars.
            line(s,ink,(110,140),(110,33),4);line(s,edge,(72,43),(151,43),3)
            polygon(s,(231,211,155),[(75,46),(149,46),(143,109),(82,113)])
            for xx in range(83,145,9):line(s,(196,173,119),(xx,48),(xx-1,107),1)
            for yy in (62,82,101):line(s,(211,190,139),(80,yy),(144,yy),1)
            for xx in (52,93):line(s,edge,(xx,139),(xx,115),3)
            polygon(s,(125,112,65),[(41,116),(77,104),(104,117),(94,120),(49,121)])
            for xx in range(48,100,6):line(s,(196,166,94),(xx,117),(77,107),1)
            for xx in (59,81,148):line(s,ink,(xx,143),(xx-16,173),3)
            line(s,edge,(51,163),(43,176),5)
            line(s,(190,172,127),(110,36),(37,139),1);line(s,(190,172,127),(110,36),(180,139),1)
        if not enemy:
            circle(s,(214,172,128),(62,121),6);rect(s,(216,217,187),(56,126,14,12),3)
            polygon(s,(193,79,57),[(57,127),(40,122),(48,131),(59,131)])
    s=painter.image()
    if boss:s=pg.transform.smoothscale(s,(286,260))
    return s

def draw_vessel(s,kind,x,y,time,enemy=False,boss=False,hit=0.,invincible=0.,hp=6):
    image=vessel_image(kind,enemy,boss)
    scale=1.3 if boss else 1.
    bob=math.sin(time*2.6+x*.01)*1.5
    if hit:x+=math.sin(hit*90)*4;y-=math.sin(hit*40)*2
    pos=(round(x-105*scale),round(y-153*scale+bob))
    if hit or invincible and int(time*12)%2:
        image=image.copy()
        if hit and int(hit*26)%2:image.fill((100,80,60,0),special_flags=pg.BLEND_RGBA_ADD)
        elif invincible:image.set_alpha(125)
    s.blit(image,pos)
    for n in range(3):
        xx=x-73-(time*65+n*19)%50;yy=y+13+math.sin(time*4+n)*5
        line(s,(159,211,210),(xx,yy),(xx+18,yy),1)
    if hit:
        for n in range(7):
            a=n*math.tau/7;radius=(.45-hit)*65+15
            line(s,PAPER,(x+math.cos(a)*radius,y+math.sin(a)*radius),(x+math.cos(a)*(radius+7),y+math.sin(a)*(radius+7)),2)
    if not enemy and hp<=2:
        for n in range(3):circle(s,(99+n*15,99+n*14,96+n*13),(x-30+n*8,y-45-(time*22+n*13)%38),5+n*2)


@lru_cache(maxsize=2)
def cargo_image(size=66):
    if size!=66:return pg.transform.smoothscale(cargo_image(),(size,size))
    from .argentina_art import Painter
    p=Painter(66,66);ink=(54,44,36);edge=(207,166,97)
    p.p(ink,[(9,17),(43,9),(59,18),(59,52),(24,60),(8,49)])
    p.p((159,111,60),[(11,19),(42,13),(56,20),(23,28)])
    p.p((132,85,45),[(11,22),(23,31),(23,56),(11,48)])
    p.p((181,132,72),[(26,31),(56,23),(56,50),(26,57)])
    for yy in (35,42,49):p.l((105,67,40),(27,yy),(55,yy-6),1)
    for xx in (18,28,38,48):p.l((114,77,43),(xx,18),(xx+9,24),1)
    for yy in (29,37,45):p.l((88,62,40),(12,yy),(22,yy+7),1)
    p.p(edge,[(26,31),(31,30),(31,54),(26,56)])
    p.p(edge,[(50,25),(55,24),(55,50),(50,51)])
    p.l(edge,(26,33),(55,27),3);p.l(edge,(27,53),(55,47),3)
    for xx,yy in ((29,33),(53,28),(29,52),(53,47)):p.c((60,65,60),(xx,yy),1)
    p.l((69,57,43),(37,39),(47,37),3);p.l((207,173,112),(37,40),(47,38),1)
    p.p((215,196,145),[(35,45),(46,43),(46,49),(35,51)])
    for dx in (0,4,8):p.l((119,99,64),(36+dx,46),(36+dx,49),1)
    p.a((125,101,62),(13,31,10,14),1.2,5.9,2)
    return p.image()
