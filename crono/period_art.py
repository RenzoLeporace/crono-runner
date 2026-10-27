"""Detailed materials and authored scenery for the original twenty-one maps.

Every stage has a distinct focal landmark. Small buildings vary by seed; only
the landscape moves with parallax. Art never adds hidden collision surfaces.
"""
from functools import lru_cache
import math
import random
import pygame as pg
from .argentina_art import Painter,arch,roof,window
from .art import W,H,mix,line,rect,circle,polygon,glow,text,PAPER,GOLD,display_alpha
from .visuals import palette_for

def blocks(p,box,col,bw=43,bh=22):
    x,y,w,h=box;p.r(col,box)
    seam=mix(col,(28,35,43),.23)
    for row,yy in enumerate(range(int(y),int(y+h),bh)):
        p.l(seam,(x,yy),(x+w,yy),1)
        for xx in range(int(x)-(bw//2 if row%2 else 0),int(x+w),bw):
            left=max(x,xx);right=min(x+w,xx+bw);bottom=min(y+h,yy+bh)
            variation=((xx*7+yy*11)%17-8)/100
            tint=mix(col,PAPER,variation) if variation>=0 else mix(col,(33,39,44),-variation)
            p.r(tint,(left+1,yy+1,max(1,right-left-2),max(1,bottom-yy-2)))
            p.l(mix(tint,PAPER,.08),(left+2,yy+2),(right-2,yy+2),1)
            if xx>=x:p.l(seam,(xx,yy),(xx,bottom),1)
            if (xx+yy)%5==0 and right-left>18:
                p.l(mix(tint,seam,.4),(left+8,yy+bh*.6),(left+17,yy+bh*.6-1),1)

def pointed_arch(p,x,y,w,h,wall,inside,trim):
    shape=[(x,y+h),(x,y+w*.55),(x+w*.12,y+w*.28),(x+w*.5,y),
           (x+w*.88,y+w*.28),(x+w,y+w*.55),(x+w,y+h)]
    p.p(inside,shape);p.p(trim,shape,4)
    p.l(wall,(x+7,y+h),(x+w-7,y+h),4)

def column(p,x,y,h,col,style='doric'):
    p.r(mix(col,(34,36,43),.2),(x+2,y,25,h))
    p.r(col,(x+5,y,18,h))
    for dx in (8,13,18):p.l(mix(col,PAPER,.2),(x+dx,y+5),(x+dx,y+h-5),1)
    p.r(mix(col,PAPER,.12),(x-4,y-8,38,12),2)
    p.r(mix(col,PAPER,.16),(x-6,y+h-4,42,10),1)
    if style=='gothic':p.p(col,[(x-4,y),(x+15,y-20),(x+34,y)])

def rose(p,cx,cy,r):
    p.c((42,51,79),(cx,cy),r);p.c((190,178,151),(cx,cy),r,4)
    for j in range(12):
        a=j*math.tau/12;xx=cx+math.cos(a)*r*.63;yy=cy+math.sin(a)*r*.63
        p.e(((172,90,97),(82,138,163),(196,158,86))[j%3],(xx-5,yy-9,10,18))
        p.l((190,178,151),(cx,cy),(cx+math.cos(a)*r,cy+math.sin(a)*r),2)
    p.c((208,171,96),(cx,cy),r*.19)

def pine(p,x,base,h,col):
    p.r((72,68,57),(x-4,base-h*.8,8,h*.8))
    for j in range(4):
        yy=base-h+j*h*.19;ww=h*(.15+j*.065)
        p.p(mix(col,(170,193,175),j*.06),[(x,yy),(x-ww,yy+h*.36),(x+ww,yy+h*.36)])

def fossil(p,x,y,scale=1):
    col=(214,196,147);s=scale
    p.l(col,(x,y),(x+150*s,y-13*s),5)
    for j in range(10):
        xx=x+j*13*s;yy=y-j*1.2*s
        p.a(col,(xx-8*s,yy,23*s,40*s),3.3,6.1,3)
        p.c((173,150,108),(xx,yy),3*s)
    p.e(col,(x+145*s,y-27*s,37*s,20*s));p.e((101,83,68),(x+165*s,y-23*s,8*s,7*s))
    for dx in (25,106):p.l(col,(x+dx*s,y+16*s),(x+(dx-14)*s,y+54*s),5)
    p.p(col,[(x,y),(x-46*s,y-7*s),(x-81*s,y-30*s),(x-37*s,y-12*s)])

@lru_cache(maxsize=21)
def landmark(era,stage):
    p=Painter(930,430);stone=(173,161,139);dark=(53,62,66);wood=(108,77,54)
    if era==0:
        if stage==0:
            # Mangrove roots, mossy reef, layered ferns and a distant fallen trunk.
            for i in range(5):
                x=70+i*180;h=240+(i*37)%100
                p.p((46,77,69),[(x-19,420),(x-3,420-h),(x+12,420-h),(x+30,420)])
                for side in (-1,1):
                    for j in range(3):p.l((60,95,72),(x+9,366-j*17),(x+side*(43+j*20),420),8-j)
                for j in range(7):p.e((59+j%3*8,111+j%2*8,81),(x-110+j%3*37,420-h-39+j//3*16,120,58))
            p.l((79,93,69),(190,420),(594,350),30)
            for j in range(20):p.l((132,144,91),(201+j*19,414-j*3.3),(210+j*19,405-j*3.3),2)
        elif stage==1:
            for j in range(7):
                x=j*146;top=115+(j*41)%80
                p.p((139+j%3*10,104+j%2*11,77),[(x,420),(x-19,top+21),(x+22,top),(x+118,top-14),(x+156,420)])
                for yy in range(top+25,420,29):p.l((170,130,91),(x-2,yy),(x+132,yy-14),3)
            fossil(p,251,280,1.45)
            for x,y in ((74,267),(806,314),(636,161)):
                for r in range(6,27,4):p.a((206,176,122),(x-r,y-r,r*2,r*2),.4,r*.33,2)
        else:
            p.p((84,51,47),[(0,420),(160,294),(320,367),(478,249),(702,314),(930,420)])
            p.e((51,42,43),(205,323,530,107));p.e((129,66,45),(233,339,474,72),3)
            for i in range(11):
                x=30+i*87;h=99+(i*37)%110
                p.l((46,41,42),(x,420),(x+13,420-h),11)
                p.l((46,41,42),(x+8,420-h*.65),(x-27,420-h*.9),6)
                p.l((46,41,42),(x+11,420-h*.74),(x+45,420-h),5)
                p.p((181,85,44),[(x-13,420),(x+3,391),(x+7,404),(x+21,377),(x+27,420)])
    elif era==1:
        if stage==0:
            for x,h in ((0,180),(145,280),(324,204),(528,320),(742,235)):
                p.p((139,176,197),[(x,420),(x+30,420-h),(x+90,400-h),(x+165,420)])
                p.p((203,224,226),[(x+30,420-h),(x+50,431-h),(x+90,400-h),(x+96,453-h),(x+69,442-h),(x+44,454-h)])
                for yy in range(int(440-h),410,29):p.l((171,204,217),(x+41,yy),(x+99,yy+12),2)
            # Mammoth silhouette with fur strands and curled tusks.
            p.e((116,110,101),(370,285,180,102));p.e((120,113,105),(512,269,78,82))
            for x in (400,432,491,522):p.l((96,98,97),(x,361),(x-5,420),18)
            p.l((112,107,101),(573,312),(588,394),17)
            p.a((224,213,179),(548,333,57,56),3.3,6.1,5)
            for xx in range(390,545,9):p.l((143,127,109),(xx,307),(xx-7,341+(xx%13)),2)
        else:
            p.p((62,74,89),[(0,430),(0,120),(170,51),(380,84),(534,29),(754,72),(930,125),(930,430)])
            p.e((18,32,49),(139,78,652,652));p.r((18,32,49),(139,290,652,140))
            for side in (-1,1):
                for j in range(4):
                    x=465+side*(310-j*17)
                    p.p((90+j*9,105+j*9,118+j*7),[(x,117+j*31),(x-side*26,430),(x+side*44,430),(x+side*72,157+j*28)])
            if stage==1:
                p.l((98,71,49),(368,416),(532,388),12);p.l((112,79,48),(385,386),(516,417),10)
                p.p((213,125,54),[(390,408),(429,329),(448,364),(472,308),(491,373),(522,408)])
                p.p((245,192,88),[(423,410),(444,364),(462,387),(478,355),(497,410)])
                for x in (244,660):
                    p.l((133,106,79),(x,420),(x+25,362),7);p.l((133,106,79),(x+50,420),(x+25,362),7)
            else:
                # Painted hands and animal outlines, visibly distinct from live foes.
                for n in range(10):
                    x=260+n%5*89;y=181+n//5*104;col=(161+n%3*19,82+n%2*12,73)
                    p.e(col,(x,y,19,26))
                    for j in range(5):p.l(col,(x+3+j*4,y+6),(x-4+j*6,y-13-(j%3)*4),4)
                fossil(p,322,345,.9)
    elif era==2:
        cream=(221,199,159);shadow=(151,137,117)
        if stage==0:
            blocks(p,(33,303,864,111),shadow)
            p.r(cream,(28,303,874,17));p.r((119,108,98),(80,184,770,119))
            for x in range(89,843,86):column(p,x,190,113,cream)
            p.r(cream,(61,162,807,27));p.p((179,146,114),[(62,162),(466,44),(869,162)])
            p.p(cream,[(81,158),(466,60),(849,158)],4)
            for j in range(17):p.r(shadow,(89+j*45,172,9,15))
            for x in (125,750):
                p.e((165,107,69),(x,362,37,43));p.r((180,128,81),(x+9,355,19,11),2)
        elif stage==1:
            for x in (0,231,677):
                blocks(p,(x,210,212,185),(185,163,128));roof(p,x,179,212,(148,90,63),32)
                arch(p,x+30,251,51,133,stone,(65,77,79),(213,189,148))
                arch(p,x+115,251,51,133,stone,(65,77,79),(213,189,148))
            p.p((102,75,55),[(266,368),(654,368),(604,412),(316,412)])
            p.l((114,89,62),(451,368),(451,107),7)
            p.p((234,216,176),[(444,116),(305,347),(444,347)])
            p.p((215,191,145),[(459,116),(598,323),(459,347)])
            for yy in range(370,412,9):p.l((144,111,73),(279+(yy-370),yy),(643-(yy-370),yy),2)
        else:
            for row in range(8):
                y=397-row*23;inset=row*19
                blocks(p,(inset,y,930-inset*2,23),(155+row*5,137+row*5,119+row*4),50,23)
            for x in (185,702):
                column(p,x,99,169,cream);p.r(cream,(x-13,79,57,20))
            p.r((207,185,149),(153,63,609,20));p.p((180,149,119),[(140,62),(459,4),(779,62)])
            p.e((86,106,106),(313,364,300,31),2)
    elif era==3:
        if stage==0:
            blocks(p,(180,222,547,189),(136,143,127));roof(p,170,176,566,(97,83,73),49)
            for x in range(207,701,89):arch(p,x,267,48,132,stone,(53,69,65),(177,176,145))
            blocks(p,(92,88,110,325),(147,149,131));roof(p,82,48,130,(95,87,81),41)
            for x in (113,153):arch(p,x,133,21,54,stone,dark,stone)
            for j in range(4):p.r(stone,(89+j*30,69,20,24))
            # Waterwheel and a small mill in the fields.
            p.c((91,72,51),(757,340),72,8);p.c((153,120,72),(757,340),61,3)
            for j in range(12):
                a=j*math.tau/12;p.l((108,82,54),(757,340),(757+math.cos(a)*65,340+math.sin(a)*65),5)
        elif stage==1:
            for n in range(4):
                x=15+n*232;blocks(p,(x,145+n%2*31,217,268-n%2*31),(173-n%2*15,151-n%3*9,123))
                roof(p,x-3,86+n%2*31,223,(118+n%2*14,73,57),63)
                for xx in (x+27,x+111):window(p,xx,178+n%2*31,44,58,(173,151,123),wood=(69,84,77))
                for yy in (149+n%2*31,264):p.r((67,62,54),(x,yy,217,8))
                p.l((67,62,54),(x+7,150+n%2*31),(x+207,264),6)
                p.l((67,62,54),(x+207,150+n%2*31),(x+7,264),6)
                p.r((54,57,54),(x+74,304,59,109),8)
                p.p(((128,72,63),(102,128,103),(162,134,84),(94,116,143))[n],[(x-8,292),(x+225,292),(x+210,327),(x+4,327)])
                for j in range(7):p.r((186,160,113),(x+8+j*30,294,14,27))
                for dx in (14,207):p.l((93,73,52),(x+dx,317),(x+dx,417),4)
        else:
            blocks(p,(209,100,510,317),(130,133,142))
            for x in (95,714):
                blocks(p,(x,40,118,380),(117,124,137));p.p((79,91,115),[(x-9,40),(x+59,0),(x+127,40)])
                for xx in (x+20,x+70):pointed_arch(p,xx,77,25,97,stone,(37,48,69),(178,176,158))
            p.p((163,163,162),[(204,101),(462,20),(726,101)])
            rose(p,463,183,62)
            for x in (269,605):
                p.p((177,174,157),[(x,402),(x+9,154),(x+38,154),(x+48,402)])
                pointed_arch(p,x+8,278,29,90,stone,(50,63,84),(195,185,157))
            pointed_arch(p,411,294,105,124,stone,(32,42,62),(195,184,155))
            for x in (359,546):column(p,x,282,137,(160,159,152),'gothic')
    elif era==4:
        brick=(133,83,65);metal=(65,81,87);brass=(190,145,75)
        if stage==0:
            blocks(p,(70,208,775,210),brick,35,17)
            for x in (94,756):
                blocks(p,(x,40,43,376),(117,78,65),25,16);p.r((64,60,58),(x-6,36,55,14))
            for n in range(3):
                x=236+n*173;p.r(metal,(x,188,119,202),32);p.r((124,133,121),(x+7,205,105,143),30)
                p.r(metal,(x,350,120,38),3);p.c((42,54,61),(x+60,285),33);p.c(brass,(x+60,285),28,4)
                p.l((239,206,133),(x+60,285),(x+74,273),3)
                for yy in range(223,339,23):p.c(brass,(x+9,yy),3);p.c(brass,(x+110,yy),3)
                p.l(metal,(x+60,191),(x+60,137),18);p.l(metal,(x+60,137),(x+145,137),18)
        elif stage==1:
            blocks(p,(85,166,751,250),brick,35,17);roof(p,59,108,798,(76,83,89),61)
            for x in range(118,821,112):arch(p,x,224,65,165,stone,(42,54,64),(181,155,111))
            p.r((200,179,134),(325,147,265,35),3);p.label('ESTACIÓN · 1889',355,153,19,(52,64,70))
            p.r((45,56,63),(0,409,930,8));p.r((133,116,84),(0,419,930,7))
            for x in range(12,920,33):p.r((53,62,66),(x,410,7,17))
        else:
            blocks(p,(98,149,735,268),(101,84,79),35,17)
            p.p(metal,[(83,149),(175,102),(305,149),(426,101),(560,149),(696,102),(848,149)])
            for x in range(130,813,100):
                p.r((49,62,77),(x,183,62,106),5)
                for yy in range(189,279,22):p.l((207,178,113),(x+5,yy),(x+57,yy),2)
                p.l((207,178,113),(x+31,184),(x+31,286),2)
            for x in (182,700):
                p.l(metal,(x,416),(x,73),11);p.l(metal,(x-37,100),(x+38,100),7)
                for dx in (-26,26):p.r((187,179,147),(x+dx-6,83,12,20),4)
            p.r((57,79,88),(374,314,180,91),8)
            for x in range(389,550,27):p.r(brass,(x,330,11,53),3)
    elif era==5:
        if stage==0:
            for j in range(4):
                y=326+j*25;p.r((101+j*5,94+j*4,77),(0,y,930,25))
                for x in range(-15,930,31):p.l((67,73,68),(x,y+2),(x+18,y+23),2)
            for x in range(32,920,89):p.r((83,80,64),(x,287,12,139));p.r((122,112,82),(x+3,289,3,130))
            for x in (130,650):
                p.r((72,77,70),(x,228,156,104),8);p.r((129,117,88),(x+7,236,142,13),3)
                p.r((31,44,47),(x+37,257,84,75),5)
                p.p((144,129,92),[(x-13,230),(x+80,174),(x+171,230)])
            for j in range(25):
                x=10+j*36;p.a((145,141,116),(x,276,39,21),0,5.8,1)
            p.r((172,157,116),(350,255,210,92),4);p.label('CORREO · 1914',371,272,16,(69,77,70))
        elif stage==1:
            for n in range(5):
                x=n*191;h=180+(n*43)%120
                blocks(p,(x,418-h,176,h),(111,109,103),35,19)
                p.p((81,85,87),[(x,418-h),(x+23,390-h),(x+54,432-h),(x+83,401-h),(x+107,437-h),(x+159,403-h),(x+176,418-h)])
                for a in range(3):
                    for b in range(3):
                        xx=x+15+a*53;yy=450-h+b*50
                        p.r((38,51,59),(xx,yy,29,36));p.l((153,143,119),(xx+15,yy),(xx+15,yy+36),2)
                p.l((62,65,65),(x+73,420-h),(x+54,466-h),3)
            p.r((156,150,127),(331,302,256,114),8);p.r((41,57,63),(359,332,202,84),4)
            p.r((194,186,155),(355,313,208,18));p.label('REFUGIO',408,314,12,(48,60,62))
            p.r((142,89,72),(583,352,69,60),4);p.r((222,211,170),(609,359,14,44));p.r((222,211,170),(594,374,43,14))
        else:
            blocks(p,(88,198,748,219),(168,166,146),42,20)
            p.p((125,145,145),[(70,198),(464,90),(854,198)]);p.r((206,195,156),(84,198,758,16))
            for x in range(129,821,91):column(p,x,238,175,(193,187,158))
            p.r((107,131,140),(342,131,245,55),4);p.label('PAZ · DERECHOS · 1948',359,150,14,(232,222,187))
            p.l((177,173,147),(57,413),(57,121),4);p.r((107,161,180),(61,124,97,58))
            p.c((224,226,206),(109,152),18,2)
    else:
        steel=(73,111,131);glass=(49,94,123)
        if stage==0:
            for n in range(4):
                x=n*236;h=235+(n%2)*118
                p.r((54+n*7,85+n*6,109+n*6),(x,418-h,222,h),7)
                for a in range(6):
                    for b in range(int(h//33)-1):
                        p.r((93+a%2*11,162+b%2*14,177+b%3*8),(x+14+a*34,434-h+b*32,20,19),2)
                p.r(steel,(x+95,395-h,29,24),2);p.l(steel,(x+109,395-h),(x+109,355-h),3)
                p.a((104,209,210),(x+82,342-h,56,39),.2,2.9,2)
            for x in (74,699):
                p.r((34,60,79),(x,331,134,85),6)
                for yy in range(341,409,15):p.r((68,119,138),(x+9,yy,115,9),2);p.c((99,232,207),(x+112,yy+4),2)
        elif stage==1:
            for n in range(3):
                x=30+n*310
                p.l((176,204,194),(x+130,411),(x+130,118),9)
                p.c((196,216,201),(x+130,118),12)
                for j in range(3):
                    a=j*math.tau/3-.6
                    p.p((188,215,204),[(x+130,118),(x+130+math.cos(a)*131,118+math.sin(a)*131),(x+130+math.cos(a+.08)*83,118+math.sin(a+.08)*83)])
                p.p((41,83,119),[(x-14,344),(x+174,344),(x+225,408),(x+36,408)])
                for j in range(8):p.l((124,172,184),(x-14+j*24,344),(x+36+j*24,408),1)
                for yy in range(359,407,16):p.l((124,172,184),(x,yy),(x+190,yy),1)
            p.r((60,121,143),(349,376,231,42),6);p.label('AGUA · ENERGÍA',377,386,14,(202,231,210))
        else:
            blocks(p,(60,278,816,139),(120,153,160),50,25)
            p.e((174,191,184),(267,57,388,388));p.r((174,191,184),(267,235,388,94))
            p.r((39,68,93),(427,67,45,219),8)
            p.l((72,102,123),(382,257),(540,147),33);p.r((45,81,105),(511,140,49,36),4)
            p.r((192,206,194),(369,322,192,95),5)
            for x in (89,677):
                p.r((73,117,140),(x,305,158,99),5)
                for a in range(3):
                    for b in range(3):p.r((124,216,208),(x+12+a*48,317+b*26,31,15),2)
            p.label('OBSERVATORIO',372,347,19,(55,82,99))
    return display_alpha(p.image(),True)

@lru_cache(maxsize=126)
def module(era,stage,seed):
    rng=random.Random(seed*71+era*977+stage*31);p=Painter(330,360)
    if era==0:
        if stage==0:
            x=150;h=250+rng.randrange(80)
            p.p((50,79,66),[(x-16,360),(x-5,360-h),(x+11,360-h),(x+33,360)])
            for j in range(6):
                side=(-1,1)[j%2];yy=360-h+j*33
                p.l((50,79,66),(x,yy+45),(x+side*95,yy),8)
                for a in range(3):p.e((57+a*11,111+a*7,78),(x+side*95-51+a*13,yy-23+a*7,95,43))
            for j in range(8):p.p((63,111,77),[(40+j*38,360),(60+j*34,315-j%3*15),(73+j*32,360)])
        else:
            col=(125,96,75) if stage==1 else (70,47,46)
            for j in range(4):
                x=j*90;h=rng.randrange(50,190)
                p.p(col,[(x-15,360),(x+12,360-h),(x+48,344-h),(x+94,360)])
                for yy in range(374-h,360,20):p.l(mix(col,(213,165,107),.25),(x+9,yy),(x+66,yy-7),2)
            if stage==1 and seed%2:fossil(p,83,258,.75)
            if stage==2:
                for x in (60,245):
                    p.l((48,41,42),(x,360),(x+15,139),11);p.l((48,41,42),(x+9,210),(x-39,168),6)
    elif era==1:
        if stage==0:
            for x in (30,180):pine(p,x,360,190+rng.randrange(100),(67,101,121))
            p.p((197,219,222),[(0,350),(80,337),(164,348),(275,333),(330,350),(330,360),(0,360)])
        else:
            for j in range(5):
                x=j*73;h=rng.randrange(70,170)
                p.p((51+j%2*8,64+j%2*9,82+j%2*9),[(x-20,0),(x+34,h),(x+65,0)])
                p.p((62+j%2*11,75+j%2*8,94+j%2*11),[(x-30,360),(x+16,360-h*.6),(x+65,360)])
    elif era==2:
        cream=(186+rng.randrange(15),171,144);blocks(p,(8,193,313,167),(155,146,128))
        p.r((95,110,112),(34,211,260,139))
        for x in range(43,290,54):column(p,x,222,128,cream)
        p.r(cream,(15,199,309,14));p.p((158,131,109),[(10,199),(163,142-rng.randrange(20)),(325,199)])
        for x in (24,270):p.e((143,94,62),(x,324,24,34));p.r((160,113,72),(x+6,318,12,9),2)
    elif era==3:
        if stage==0:
            for x in (60,225):pine(p,x,360,215,(66,103,81))
            blocks(p,(31,270,270,90),(121,137,108));roof(p,24,231,285,(100,83,62),42)
            arch(p,127,282,58,78,wall=(157,153,123),inside=(47,69,60),trim=(184,176,132))
        else:
            wall=(142+rng.randrange(25),132+rng.randrange(16),119)
            blocks(p,(15,137,299,223),wall);roof(p,7,76,315,(104,73,64),64)
            for x in (40,122,224):window(p,x,182,39,57,wall)
            for y in (146,263):p.r((64,61,55),(15,y,299,8))
            for x in (24,155,304):p.r((64,61,55),(x,144,7,213))
            p.l((64,61,55),(24,148),(155,263),5);p.l((64,61,55),(155,148),(304,263),5)
            arch(p,123,287,59,73,wall,(49,54,54),(173,154,119))
    elif era==4:
        blocks(p,(10,150,310,210),(105+rng.randrange(25),76,65),31,16)
        p.p((63,72,77),[(0,151),(69,110),(119,150),(182,112),(229,150),(290,109),(330,150)])
        for x in (32,129,229):
            p.r((38,53,65),(x,185,64,84));p.r((149,141,107),(x,185,64,84),2)
            for xx in (x+21,x+43):p.l((149,141,107),(xx,186),(xx,267),1)
            for yy in range(204,264,20):p.l((149,141,107),(x,yy),(x+64,yy),1)
        blocks(p,(249,35,38,326),(104,76,65),23,14);p.r((58,61,65),(243,31,50,11))
        for yy in (293,321):p.l((54,68,75),(16,yy),(219,yy),8)
    elif era==5:
        if stage==0:
            pine(p,76,360,240,(76,92,85));p.l((100,91,70),(200,360),(200,225),8)
            for j in range(8):p.r((111+j%2*9,101,78),(111+j*28,334-j%3*4,31,24),9)
        else:
            h=200+rng.randrange(100);blocks(p,(10,360-h,307,h),(125,128,126) if stage==1 else (164,167,151),39,22)
            for xx in range(30,303,61):
                for yy in range(int(387-h),340,43):
                    p.r((43,61,72),(xx,yy,29,31));p.l((159,155,135),(xx+15,yy),(xx+15,yy+31),2)
            if stage==1:p.p((67,76,82),[(10,360-h),(67,337-h),(101,383-h),(167,341-h),(215,375-h),(317,360-h)])
            else:p.r((193,188,161),(5,360-h-9,319,12))
    else:
        h=240+rng.randrange(110);p.r((41,76+rng.randrange(12),105),(12,360-h,303,h),6)
        for xx in range(29,309,44):
            for yy in range(int(379-h),349,27):
                p.r((80+rng.randrange(34),147+rng.randrange(30),172),(xx,yy,24,15),2)
        p.r((115,160,166),(5,355,319,5))
        for yy in range(int(376-h),350,54):p.l((52,94,118),(15,yy),(313,yy),3)
    return display_alpha(p.image(),True)

@lru_cache(maxsize=21)
def sky(era,stage):
    pal=palette_for(era,stage);s=pg.Surface((W,H))
    for y in range(H):line(s,mix(pal.sky,pal.horizon,min(1,y/620)),(0,y),(W,y))
    if pal.kind not in ('cave','ash'):
        if stage==2 or era in (3,6):
            rng=random.Random(era*31+stage)
            for _ in range(40):circle(s,mix(pal.horizon,PAPER,.3),(rng.randrange(W),rng.randrange(105,325)),1)
        glow(s,(1040,174),105,pal.accent);circle(s,mix(pal.accent,pal.horizon,.38),(1040,174),33)
    for yy in range(584,H):line(s,mix(pal.near,(12,23,35),(yy-584)/136),(0,yy),(W,yy))
    return s

def background(s,era,stage,camera,t):
    s.blit(sky(era,stage),(0,0));pal=palette_for(era,stage)
    for layer in range(2):
        off=camera*(.035+layer*.04)
        for n in range(int(off//620)-1,int(off//620)+math.ceil(W/620)+1):
            x=n*620-off;h=90+(n*47)%100
            col=mix(pal.far,pal.horizon,.22) if not layer else pal.far
            polygon(s,col,[(x-50,560),(x+61,480-h*.3),(x+182,460-h),(x+328,480-h*.6),(x+500,509),(x+670,560),(x+670,584),(x-50,584)])
    if era==0 and stage==0 or era==2 and stage==1:
        rect(s,mix(pal.far,(40,116,134),.5),(0,512,W,72))
        for n in range(30):
            x=(n*111-camera*.12+t*5)%W;y=520+n%7*9
            line(s,mix(pal.horizon,pal.near,.6),(x,y),(x+37,y),1)
    if pal.kind!='cave':
        for n in range(5):
            x=(n*377-camera*.07+t*(1+n%3))%1700-200;y=149+n%3*49
            col=mix(pal.sky,pal.horizon,.3)
            polygon(s,col,[(x,y+9),(x+43,y-2),(x+122,y-12),(x+200,y),(x+249,y+12)])

def landscape(s,world,camera,t):
    era,stage=world.index,world.stage;pal=palette_for(era,stage)
    off=camera*.35
    focal=world.data['zones'][2][0]*.35+640
    first=int(off//311)-1
    for n in range(first,first+math.ceil(W/311)+2):
        x=n*311-off
        if abs(n*311-focal)<470:continue
        img=module(era,stage,n%6)
        s.blit(img,(int(x),203))
    x=focal-off-465
    if -930<x<W:s.blit(landmark(era,stage),(int(x),136))
    # Additional mid-route detail changes with each district.
    mid=world.data['zones'][1][0]*.5-camera*.5+470
    if -210<mid<W+210:
        if era in (2,3):
            for dx in (-95,95):
                line(s,mix(pal.near,pal.top,.45),(mid+dx,558),(mid+dx,441),4)
                polygon(s,(145,87,68) if era==2 else (102,95,129),[(mid+dx,442),(mid+dx+47,455),(mid+dx+41,511),(mid+dx,495)])
        elif era==4:
            for dx in (-80,80):
                line(s,(68,80,85),(mid+dx,558),(mid+dx,421),9)
                circle(s,(183,145,87),(mid+dx,486),26,5)
                for j in range(8):
                    a=t*.2+j*math.tau/8;line(s,(183,145,87),(mid+dx,486),(mid+dx+math.cos(a)*24,486+math.sin(a)*24),3)
        elif era==6 and stage==0:
            for dx in (-70,70):
                rect(s,(37,69,94),(mid+dx,437,52,116),4)
                for yy in range(446,540,17):rect(s,(85,140,156),(mid+dx+6,yy,40,9),2);circle(s,(103,232,209),(mid+dx+37,yy+4),2)
    text(s,world.data['meta'].name.upper(),(W-26,121),11,mix(pal.accent,PAPER,.15),True,'topright')

@lru_cache(maxsize=320)
def tile(era,stage,w,h,seed,moving):
    pal=palette_for(era,stage);p=Painter(w,h+12);rng=random.Random(seed+era*719+stage*23)
    if era<2:
        base=mix(pal.rock,(48,42,37),.28)
        p.r(base,(0,0,w,h))
        for row,y in enumerate(range(10,h,18)):
            col=mix(base,pal.top,.07+row%3*.025)
            points=[(x,y+rng.randrange(-4,5)) for x in range(0,w+50,35)]
            for a,b in zip(points,points[1:]):p.l(col,a,b,2)
        for _ in range(w//9):
            x=rng.randrange(w);y=rng.randrange(8,max(9,h))
            p.l(mix(base,pal.top,.2),(x,y),(x+rng.randrange(2,9),y+1),1)
        p.r(pal.top,(0,0,w,6),2)
        if era==1 and stage==0:
            for x in range(3,w,21):p.e((205,230,233),(x,-2,27,10))
            if h>30:
                for x in range(13,w-10,67):p.p((135,184,208),[(x,7),(x+9,37+rng.randrange(22)),(x+17,7)])
        elif era==0 and stage==0:
            for x in range(8,w,34):
                p.l((71,111,75),(x,7),(x+10,28),2);p.l((100,131,78),(x+6,18),(x+19,21),1)
        elif era==0 and stage==2:
            for x in range(21,w,97):p.l((141,66,43),(x,10),(x+21,23),2)
    elif era in (2,3):
        col=(131,121,106) if era==2 else (100,108,109)
        blocks(p,(0,0,w,h),col,57 if era==2 else 43,23 if era==2 else 18)
        p.r((219,198,153) if era==2 else (161,165,147),(0,0,w,8))
        for x in range(4,w,29):p.l(mix(col,PAPER,.35),(x,2),(x+23,2),1)
        if h<50:
            p.r((71,76,74),(0,h-4,w,4))
            for x in range(18,w-10,43):p.p((176,155,120),[(x,12),(x+8,17),(x,22),(x-8,17)],1)
        for _ in range(w//75):
            x=rng.randrange(w);y=rng.randrange(12,max(13,h))
            p.l(mix(col,(42,52,58),.35),(x,y),(x+9,y+8),1)
    else:
        col=(55,69,77) if era==4 else (80,85,84) if era==5 else (39,68,91)
        p.r(col,(0,0,w,h))
        for x in range(0,w,68):
            p.r(mix(col,pal.top,.12),(x+2,10,64,max(7,h-17)),2)
            p.l(mix(col,(20,31,42),.6),(x,8),(x,h),2)
            for xx in (x+7,x+59):
                for yy in (14,h-7):p.c((150,145,114) if era<6 else (97,174,179),(xx,yy),2)
        p.r((168,141,100) if era==4 else (165,166,141) if era==5 else (147,208,204),(0,0,w,6))
        if era==4:
            for x in range(14,w-7,30):p.p((95,90,67),[(x,6),(x+10,6),(x+3,12),(x-7,12)])
        elif era==5:
            for x in range(31,w,127):p.l((51,61,65),(x,19),(x-8,34),2);p.l((51,61,65),(x-8,34),(x+3,48),1)
        else:
            for x in range(18,w-22,85):
                p.l((58,111,139),(x,19),(x+29,19),1);p.l((58,111,139),(x+29,19),(x+43,33),1);p.c((103,194,190),(x+43,33),2)
        p.r(mix(col,(18,31,39),.6),(0,h-4,w,4))
    if moving:
        p.r((119,233,217),(0,0,w,3))
        for x in (11,w-11):p.c((119,233,217),(x,10),3,1)
    return display_alpha(p.image(),True)

def props(s,world,camera,t):
    era=world.index;stage=world.stage
    for n,k in enumerate(world.data['main_nodes']):
        r=world.platforms[k].rect;x=r.right-camera-68;y=r.top
        if not -60<x<W+60:continue
        # Keep every prop behind the actors and away from required jump edges.
        if era==0:
            col=(48,103,74) if stage==0 else (145,110,73) if stage==1 else (90,55,44)
            for j in range(5):
                xx=x+(j-2)*9;line(s,col,(x,y),(xx,y-22-j%3*7),2)
                if stage==0:polygon(s,col,[(xx,y-22-j%3*7),(xx-12,y-14),(xx+3,y-11)])
        elif era==1:
            for j in range(3):polygon(s,(157,200,216) if stage==0 else (83,108,133),[(x+j*12-18,y),(x+j*12-12,y-15-j*4),(x+j*12,y)])
        elif era==2:
            pg.draw.ellipse(s,(157,102,66),(int(x-13),int(y-37),26,36));rect(s,(204,158,97),(x-8,y-42,16,8),2)
            line(s,(71,77,74),(x-11,y-24),(x+11,y-24),3);line(s,(71,77,74),(x-10,y-19),(x+10,y-19),2)
        elif era==3:
            rect(s,(117,86,57),(x-20,y-31,40,31),3)
            for dx in (-14,0,14):line(s,(168,130,75),(x+dx,y-29),(x+dx,y-2),2)
            line(s,(58,65,60),(x-20,y-23),(x+20,y-23),3);line(s,(58,65,60),(x-20,y-9),(x+20,y-9),3)
        elif era==4:
            rect(s,(86,99,101),(x-22,y-43,44,43),6);circle(s,(186,143,76),(x,y-23),13,3)
            for dx in (-15,15):circle(s,(177,170,134),(x+dx,y-36),2)
            line(s,(72,85,92),(x,y-44),(x,y-57),7)
        elif era==5:
            rect(s,(117,115,88),(x-25,y-27,50,27),3);line(s,(73,82,74),(x-20,y-19),(x+20,y-19),3)
            if stage==1:
                rect(s,(218,206,166),(x-4,y-22,8,18));rect(s,(218,206,166),(x-9,y-17,18,7))
        else:
            rect(s,(43,81,104),(x-16,y-44,32,44),4);rect(s,(121,200,195),(x-10,y-36,20,18),3)
            for yy in (y-12,y-7):line(s,(81,136,151),(x-8,yy),(x+8,yy),2)
