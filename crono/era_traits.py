"""Visible, recoverable environmental mechanics; historical settings, fictional rules."""
from functools import lru_cache
import math
import pygame as pg
from .art import rect,line,circle,polygon,text,CYAN,GOLD,PAPER

NAMES={0:'Barro y vegetación',1:'Frío y abrigo',2:'Esfuerzo y recuperación',3:'Lámpara y visibilidad',
       4:'Vapor y válvulas',5:'Alarma y refugio',6:'Red de energía',7:'Cobertura y suministros',8:'Agua y sombra'}

class EraTraits:
    def __init__(self,world):
        self.world=world;self.era=10 if world.level_id==44 else 9 if world.level_id in (43,45) else world.combat_era;self.clock=0.;self.coat=False;self.resource=100.;self.damage_clock=0.
        floors=[world.platforms[i] for i in world.data['main_nodes'] if world.platforms[i].rect.w>=220]
        self.points=[]
        for f in (.04,.29,.53,.78):
            floor=min(floors,key=lambda p:abs(p.rect.centerx-world.width*f))
            self.points.append((floor.rect.left+min(260,floor.rect.w*.5),floor.rect.top))
        self.coat_pos=(min(335,floors[0].rect.right-45),floors[0].rect.top)

    def payload(self):return dict(coat=self.coat,resource=self.resource)

    def restore(self,data):
        if not isinstance(data,dict):return
        self.coat=data.get('coat') is True
        value=data.get('resource',100.)
        if type(value) in (int,float) and math.isfinite(value):self.resource=max(0,min(100,float(value)))

    def respawn(self):self.resource=100.;self.damage_clock=0.;self.clock=0.

    def safe(self):
        w=self.world
        return any(abs(w.player.rect.centerx-x)<90 and abs(w.player.rect.bottom-y)<100 for x,y in self.points)

    def update(self,dt,controls):
        w=self.world;p=w.player;events=[]
        if getattr(w,'practice_mode',False) or w.boss and w.boss.active:return events
        self.clock+=dt;near=self.safe();era=self.era
        if era==1 and not self.coat:
            x,y=self.coat_pos
            if abs(p.rect.centerx-x)<55 and abs(p.rect.bottom-y)<95:
                self.coat=True;w.say('Abrigo equipado: puedes recorrer el hielo sin perder calor.');events.append('checkpoint')
        if era==0:
            in_mud=any(abs(p.rect.centerx-x)<65 and abs(p.rect.bottom-y)<35 for x,y in self.points[1:])
            if in_mud and p.grounded:w.mechanic.speed*=.82
        elif era==1:
            if near or self.coat:self.damage_clock=0.
            else:
                self.damage_clock+=dt
                if self.damage_clock>(30,23,17)[w.difficulty]:
                    self.damage_clock=0.;events+=w.damage(p.rect.centerx)
                    w.say('El frío te alcanza: vuelve al abrigo de la primera posta o busca un refugio.')
        elif era==8:
            self.resource=min(100,self.resource+dt*32) if near else max(0,self.resource-dt*(1.6,2.1,2.6)[w.difficulty])
            if self.resource<=0:
                self.damage_clock+=dt
                if self.damage_clock>8:self.damage_clock=0.;events+=w.damage(p.rect.centerx);w.say('Busca agua y sombra en los puestos marcados.')
            else:self.damage_clock=0.
        elif era==2:
            self.resource=max(0,self.resource-dt*105) if p.dash_time>0 else min(100,self.resource+dt*(18 if not controls.axis else 5))
            if self.resource<12:p.cooldown=max(p.cooldown,.45)
        elif era==3:
            self.resource=min(100,self.resource+dt*24) if near else max(0,self.resource-dt*.65)
        elif era in (4,5):
            cycle=self.clock%(10 if era==4 else 14);warning=7<cycle<9;danger=9<=cycle<9.7
            if danger:
                if era==4 and any(abs(p.rect.centerx-x)<44 and abs(p.rect.bottom-y)<70 for x,y in self.points[1:]):events+=w.damage(p.rect.centerx)
                elif era==5 and not near and self.clock>18:events+=w.damage(p.rect.centerx)
            if warning and int(self.clock*2)!=int((self.clock-dt)*2) and not near:w.say('Vapor: espera fuera de la rejilla marcada.' if era==4 else 'Alarma: busca un refugio marcado antes del impacto.')
        elif era==6:
            if near:
                p.cooldown=max(0,p.cooldown-dt*2);p.dash_ready=True
                if not controls.axis:p.recovery_clock+=dt
        elif era==9 and near and controls.drop and p.grounded:
            p.cooldown=max(0,p.cooldown-dt);p.shot_cooldown=max(0,p.shot_cooldown-dt)
        elif era==7 and near and controls.drop and p.grounded:
            p.invincible=max(p.invincible,.06)
        return events

    def description(self):
        era=self.era
        if era==10:return 'Gravedad lunar · mantén salto para cruzar cráteres; frena antes de aterrizar. Recoge piezas y repara la nave.'
        if era==9:return 'Señal y comunicación · mantén ↓ junto a las antenas para sincronizar el equipo.'
        if era==1:return 'Frío · '+('abrigo equipado' if self.coat else 'recoge el abrigo de la primera posta; los refugios protegen')
        if era==8:return f'Agua {self.resource:.0f}% · repón en los pozos y zonas de sombra'
        if era==2:return f'Esfuerzo {self.resource:.0f}% · descansa entre impulsos'
        if era==3:return f'Lámpara {self.resource:.0f}% · recarga junto a los faroles'
        return {0:'El barro frena al caminar; salta o busca las pasarelas.',4:'Las rejillas avisan antes de expulsar vapor.',
                5:'Las alarmas anuncian impactos: entra en los refugios.',6:'Las placas de energía recargan el impulso, incluso en el aire.',
                7:'Mantén ↓ junto a los parapetos para cubrirte de los disparos.'}[era]

    def draw(self,s,camera,t):
        w=self.world;era=self.era
        for x,y in self.points:
            x-=camera
            if not -90<x<s.get_width()+90:continue
            if era==0:
                pg.draw.ellipse(s,(99,84,53),pg.Rect(x-59,y-3,118,13))
                for dx in (-37,-11,23):line(s,(151,128,71),(x+dx,y),(x+dx+13,y+3),2)
            elif era==1:
                polygon(s,(109,92,75),[(x-39,y-3),(x,y-60),(x+39,y-3)])
                polygon(s,(222,215,190),[(x-39,y-3),(x,y-60),(x-6,y-30),(x-30,y-3)])
                rect(s,(54,61,66),(x-10,y-26,20,24),3)
            elif era==8:
                rect(s,(163,134,82),(x-27,y-25,54,23),5);pg.draw.ellipse(s,(70,164,180),pg.Rect(x-20,y-25,40,9))
                for dx in (-35,35):line(s,(106,84,57),(x+dx,y-3),(x+dx,y-65),3)
                polygon(s,(168,155,97),[(x-44,y-68),(x+44,y-68),(x+35,y-49),(x-35,y-49)])
            elif era==3:
                line(s,(104,92,69),(x,y-1),(x,y-65),3);rect(s,(44,57,61),(x-12,y-68,24,27),3);circle(s,GOLD,(x,y-54),6)
            elif era in (4,5):
                rect(s,(69,81,82),(x-36,y-7,72,7),3)
                for dx in range(-27,28,9):line(s,(160,167,137),(x+dx,y-6),(x+dx,y-1),2)
                if era==5:
                    polygon(s,(103,118,115),[(x-42,y-7),(x-29,y-62),(x+29,y-62),(x+42,y-7)])
                    rect(s,(37,55,66),(x-17,y-37,34,30),3);text(s,'REFUGIO',(x,y-80),11,GOLD,True,'center')
                elif 7<self.clock%10<9.7:
                    for n in range(4):line(s,GOLD,(x-24+n*16,y-12),(x-28+n*16,y-55-(n%2)*17),2)
            elif era==9:
                line(s,(109,128,136),(x,y-4),(x,y-81),3);pg.draw.arc(s,CYAN,(x-23,y-109,46,36),3.2,6.1,2)
                circle(s,GOLD,(x,y-87),3)
            elif era==6:
                rect(s,(49,82,99),(x-40,y-7,80,7),3);line(s,CYAN,(x-29,y-3),(x+29,y-3),2)
                polygon(s,CYAN,[(x+4,y-50),(x-13,y-30),(x,y-30),(x-4,y-15),(x+15,y-38),(x+2,y-38)],1)
            elif era==7:
                for row in range(2):
                    for n in range(3):rect(s,(164-row*14,144-row*9,99),(x-38+n*25+row*6,y-20-row*16,27,16),6)
        if era==1 and not self.coat:
            x,y=self.coat_pos;x-=camera
            if -60<x<s.get_width()+60:
                polygon(s,(192,150,101),[(x-17,y-55),(x+16,y-55),(x+26,y-12),(x,y-22),(x-24,y-12)])
                pg.draw.arc(s,(237,226,196),(int(x-17),int(y-66),34,27),0,math.pi,7)
                text(s,'ABRIGO · RECOGER',(x,y-89),12,GOLD,True,'center')

    def lighting(self,s,camera):
        if self.era!=3:return
        radius=310 if self.resource>15 else 195
        p=self.world.player.rect;cx=round(p.centerx-camera);cy=round(p.centery)
        width,height=s.get_size();mask=lamp_mask(width,height,radius)
        s.blit(mask,(cx-width,cy-height))

@lru_cache(maxsize=1)
def lamp_mask(width,height,radius):
    s=pg.Surface((width*2,height*2),pg.SRCALPHA);s.fill((7,15,27,105))
    for n in range(7):pg.draw.circle(s,(7,15,27,round(105*(1-n/6))),(width,height),round(radius*(1-n*.065)))
    return s
