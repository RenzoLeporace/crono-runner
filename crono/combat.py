"""Enemy archetypes and five telegraphed guardians. All guardians are fictional."""
import math
import pygame as pg

ENEMY_NAMES=dict(walker='Rondador',hopper='Saltador',flyer='Alado',sentry='Centinela',charger='Embistente',armored='Acorazado')
ENEMY_HINTS=dict(walker='Patrulla el suelo.',hopper='Salta al acercarte.',flyer='Oscila en el aire.',
                 sentry='Dispara a distancia.',charger='Avisa y embiste.',armored='Resiste tres impactos; evita sus púas.')
BOSS_NAMES=('El guardián del impacto','La matriarca de escarcha','El coloso de bronce','El vigía de las campanas','El titán de vapor')
BOSS_HINTS=('Salta la onda de choque.','Esquiva la carga y dispara después.','Muévete entre sus proyectiles.',
            'Evita el picado; ataca al aterrizar.','Salta las descargas de vapor.')


class Projectile:
    def __init__(self,x,y,vx,vy=0,owner='enemy',damage=1,kind='orb'):
        self.rect=pg.FRect(x-7,y-5,14,10) if kind!='wave' else pg.FRect(x-15,559,30,25)
        self.vx,self.vy=vx,vy
        self.owner,self.damage,self.kind=owner,damage,kind
        self.ttl=3.2
        self.alive=True

    def update(self,dt):
        self.rect.x+=self.vx*dt
        self.rect.y+=self.vy*dt
        self.ttl-=dt
        if self.ttl<=0:
            self.alive=False


class Enemy:
    def __init__(self,spec,era):
        if not isinstance(spec,dict):
            x,y,left,right=spec
            spec=dict(x=x,y=y,left=left,right=right,kind='walker')
        self.kind=spec.get('kind','walker')
        self.left,self.right=spec['left'],spec['right']
        self.rect=pg.FRect(spec['x'],spec['y'],44,34)
        self.base_y=self.rect.y
        if self.kind=='flyer':
            self.base_y-=100
            self.rect.y=self.base_y
        self.direction=-1
        self.speed=67+era*9
        if self.kind=='armored':
            self.speed=48
        self.max_hp=3 if self.kind=='armored' else 2 if self.kind=='charger' else 1
        self.hp=self.max_hp
        self.alive=True
        self.time=0.
        self.timer=1.1+(self.left%10)/10
        self.vy=0.
        self.mode='patrol'
        self.hit_flash=0.

    def hit(self,damage):
        if not self.alive:
            return False
        self.hp-=damage
        self.hit_flash=.16
        self.alive=self.hp>0
        return not self.alive

    def update(self,dt,world=None):
        self.time+=dt
        self.timer-=dt
        self.hit_flash=max(0,self.hit_flash-dt)
        speed=self.speed
        p=world.player if world else None
        distance=abs(p.rect.centerx-self.rect.centerx) if p else 9999
        if self.kind=='sentry':
            speed=0
            if p and distance<650 and self.timer<=0:
                self.direction=1 if p.rect.centerx>self.rect.centerx else -1
                world.projectiles.append(Projectile(self.rect.centerx,self.rect.centery,self.direction*235))
                self.timer=2.4
        elif self.kind=='hopper':
            if p and distance<470 and self.timer<=0 and self.rect.y>=self.base_y:
                self.vy=-360
                self.timer=1.7
            self.vy+=1500*dt
            self.rect.y+=self.vy*dt
            if self.rect.y>=self.base_y:
                self.rect.y=self.base_y
                self.vy=0
        elif self.kind=='flyer':
            self.rect.y=self.base_y+math.sin(self.time*2.4+self.left)*37
            speed=95
        elif self.kind=='charger':
            if self.mode=='patrol' and p and distance<380 and self.timer<=0:
                self.mode='warning'
                self.timer=.75
                self.direction=1 if p.rect.centerx>self.rect.centerx else -1
            elif self.mode=='warning':
                speed=0
                if self.timer<=0:
                    self.mode='charge'
                    self.timer=.6
            elif self.mode=='charge':
                speed=325
                if self.timer<=0:
                    self.mode='patrol'
                    self.timer=1.6
        self.rect.x+=self.direction*speed*dt
        if self.rect.left<=self.left:
            self.rect.left=self.left
            self.direction=1
        if self.rect.right>=self.right:
            self.rect.right=self.right
            self.direction=-1


class Boss:
    def __init__(self,era):
        self.era=era
        self.name=BOSS_NAMES[era]
        self.hint=BOSS_HINTS[era]
        self.max_hp=18+era*4
        self.hp=self.max_hp
        self.rect=pg.FRect(4960,464,122,120)
        self.active=False
        self.alive=True
        self.phase='waiting'
        self.timer=0.
        self.attack_time=0.
        self.direction=-1
        self.cycle=0
        self.scholarly=False
        self.hit_flash=0.

    def hit(self,damage):
        if not self.active or not self.alive or self.phase!='exposed' or self.hit_flash>0:
            return False
        self.hp=max(0,self.hp-damage)
        self.hit_flash=.23
        if self.hp==0:
            self.alive=False
            self.phase='defeated'
            return True
        return False

    def begin_attack(self,world):
        self.phase='attack'
        self.attack_time=0
        self.timer=(.5, .85, .5, 1.15, .75)[self.era]
        x=self.rect.centerx
        if self.era in (0,4):
            for direction in (-1,1):
                world.projectiles.append(Projectile(x,570,direction*(285 if self.era==0 else 345),kind='wave'))
                if self.era==4:
                    world.projectiles.append(Projectile(x,490,direction*220))
        elif self.era==2:
            for angle in (-.23,0,.23):
                sign=1 if world.player.rect.centerx>x else -1
                world.projectiles.append(Projectile(x,self.rect.centery+15,sign*250*math.cos(angle),250*math.sin(angle)))

    def update(self,dt,world):
        if not self.alive:
            return
        self.hit_flash=max(0,self.hit_flash-dt)
        if not self.active:
            if world.player.rect.centerx>4470 and len(world.shards)==3:
                self.active=True
                self.phase='warning'
                self.timer=1.3
                world.projectiles=[]
                world.say(self.name+' · '+self.hint)
            return
        self.scholarly=any(t in world.answered for t in (world.level_id*2,world.level_id*2+1))
        self.timer-=dt
        p=world.player
        if self.phase=='warning':
            self.direction=1 if p.rect.centerx>self.rect.centerx else -1
            if self.timer<=0:
                self.begin_attack(world)
        elif self.phase=='attack':
            self.attack_time+=dt
            if self.era==1:
                self.rect.x+=self.direction*435*dt
            elif self.era==3:
                self.rect.x+=self.direction*320*dt
                self.rect.bottom=584-math.sin(min(1,self.attack_time/1.15)*math.pi)*145
            elif self.era==0:
                self.rect.bottom=584-math.sin(min(1,self.attack_time/.5)*math.pi)*65
            if self.timer<=0:
                self.rect.bottom=584
                self.phase='exposed'
                self.timer=1.65+(.8 if self.scholarly else 0)
        elif self.phase=='exposed' and self.timer<=0:
            self.phase='warning'
            self.timer=1.2 if self.hp>self.max_hp/2 else .85
            self.cycle+=1
        self.rect.x=max(4510,min(5430-self.rect.w,self.rect.x))
