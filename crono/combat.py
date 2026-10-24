"""Enemy archetypes and five telegraphed guardians. All guardians are fictional."""
import math
import pygame as pg

ENEMY_NAMES=dict(walker='Rondador',hopper='Saltador',flyer='Alado',sentry='Centinela',charger='Embistente',armored='Acorazado')
ENEMY_HINTS=dict(walker='Patrulla el suelo.',hopper='Salta al acercarte.',flyer='Oscila en el aire.',
                 sentry='Dispara a distancia.',charger='Avisa y embiste.',armored='Resiste tres impactos; evita sus púas.')
BOSS_NAMES=('El guardián del impacto','La matriarca de escarcha','El coloso de bronce','El vigía de las campanas','El titán de vapor',
            'El blindado del olvido','El núcleo de la red','El custodio de la memoria')
BOSS_HINTS=('Salta la onda de choque.','Esquiva la carga y dispara después.','Muévete entre sus proyectiles.',
            'Evita el picado; ataca al aterrizar.','Salta las descargas de vapor.',
            'Busca los huecos entre las salvas.','Esquiva los nodos marcados.','Alterna salto y desplazamiento.')


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
    def __init__(self,spec,era,difficulty=0):
        if not isinstance(spec,dict):
            x,y,left,right=spec
            spec=dict(x=x,y=y,left=left,right=right,kind='walker')
        self.kind=spec.get('kind','walker')
        self.era=era
        self.difficulty=0
        self.left,self.right=spec['left'],spec['right']
        height=36 if self.kind=='flyer' else (49,48,62,64,48,56,48,48)[era]
        self.rect=pg.FRect(spec['x'],spec['y']+34-height,44,height)
        self.base_y=self.rect.y
        if self.kind=='flyer':
            self.base_y-=100
            self.rect.y=self.base_y
        self.direction=-1
        self.speed=67+min(era,4)*9
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
        self.base_speed=self.speed
        self.base_hp=self.max_hp
        self.set_difficulty(difficulty)

    def set_difficulty(self,band):
        damage=self.max_hp-self.hp
        self.difficulty=band
        self.speed=self.base_speed*(1,1.3,1.65)[band]
        self.max_hp=self.base_hp+band
        self.hp=max(1,self.max_hp-damage) if self.alive else 0

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
        if p and distance>1400:
            return
        rate=(1,1.3,1.65)[self.difficulty]
        if self.kind=='sentry':
            speed=0
            if p and distance<650 and self.timer<=0:
                self.direction=1 if p.rect.centerx>self.rect.centerx else -1
                for vy in ((-85,0,85) if self.difficulty==2 else (0,)):
                    world.projectiles.append(Projectile(self.rect.centerx,self.rect.centery,self.direction*235*rate,vy))
                self.timer=2.4/rate
        elif self.kind=='hopper':
            if p and distance<470 and self.timer<=0 and self.rect.y>=self.base_y:
                self.vy=-360*(1+self.difficulty*.08)
                if self.difficulty:
                    self.direction=1 if p.rect.centerx>self.rect.centerx else -1
                self.timer=1.7/rate
            self.vy+=1500*dt
            self.rect.y+=self.vy*dt
            if self.rect.y>=self.base_y:
                self.rect.y=self.base_y
                self.vy=0
        elif self.kind=='flyer':
            self.rect.y=self.base_y+math.sin(self.time*2.4+self.left)*37
            speed=95*rate
            if self.difficulty==2 and p and distance<500 and self.timer<=0:
                # The hovering eye brightens before firing a single aimed shot.
                dx=p.rect.centerx-self.rect.centerx;dy=p.rect.centery-self.rect.centery
                scale=275/max(1,math.hypot(dx,dy))
                world.projectiles.append(Projectile(self.rect.centerx,self.rect.centery,dx*scale,dy*scale))
                self.timer=2.1
        elif self.kind=='charger':
            if self.mode=='patrol' and p and distance<380 and self.timer<=0:
                self.mode='warning'
                self.timer=(.75,.6,.45)[self.difficulty]
                self.direction=1 if p.rect.centerx>self.rect.centerx else -1
            elif self.mode=='warning':
                speed=0
                if self.timer<=0:
                    self.mode='charge'
                    self.timer=.6
            elif self.mode=='charge':
                speed=325*(1+self.difficulty*.18)
                if self.timer<=0:
                    self.mode='patrol'
                    self.timer=1.6/rate
        self.rect.x+=self.direction*speed*dt
        if self.rect.left<=self.left:
            self.rect.left=self.left
            self.direction=1
        if self.rect.right>=self.right:
            self.rect.right=self.right
            self.direction=-1


class Boss:
    def __init__(self,era,difficulty=0,left=4320,right=5670):
        self.era=era
        self.left,self.right=left,right
        self.name=BOSS_NAMES[era]
        self.hint=BOSS_HINTS[era]
        self.base_hp=18+min(era,4)*4
        self.max_hp=self.hp=self.base_hp
        self.difficulty=0
        self.rect=pg.FRect(left+(right-left)*.54,464,122,120)
        self.active=False
        self.alive=True
        self.phase='waiting'
        self.timer=self.attack_time=self.hit_flash=0.
        self.direction=-1
        self.cycle=0
        self.scholarly=False
        self.telegraphs=[]
        self.set_difficulty(difficulty)

    def set_difficulty(self,band):
        fraction=self.hp/self.max_hp
        self.difficulty=band
        self.max_hp=round(self.base_hp*(1,1.5,2.1)[band])
        self.hp=max(1,round(self.max_hp*fraction)) if self.alive else 0

    def hit(self,damage):
        if not self.active or not self.alive or self.phase!='exposed' or self.hit_flash>0:
            return False
        self.hp=max(0,self.hp-damage)
        self.hit_flash=(.23,.2,.16)[self.difficulty]
        if self.hp==0:
            self.alive=False
            self.phase='defeated'
            self.telegraphs=[]
            return True
        return False

    def begin_attack(self,world):
        self.phase='attack'
        self.attack_time=0
        self.timer=(.5,.85,.5,1.15,.75,.95,1.1,.85)[self.era]
        rate=(1,1.2,1.4)[self.difficulty]
        x=self.rect.centerx
        enraged=self.hp<self.max_hp*.5
        if self.era in (0,4,7):
            for direction in (-1,1):
                world.projectiles.append(Projectile(x,570,direction*(285 if self.era==0 else 345)*rate,kind='wave'))
                if self.era in (4,7):
                    world.projectiles.append(Projectile(x,470,direction*220*rate))
        elif self.era in (2,5):
            sign=1 if world.player.rect.centerx>x else -1
            angles=((-.38,-.18,0,.18,.38) if self.difficulty else (-.38,0,.38)) if self.era==5 else (-.23,0,.23)
            for angle in angles:
                world.projectiles.append(Projectile(x,self.rect.centery+15,sign*250*rate*math.cos(angle),250*rate*math.sin(angle)))
        elif self.era==6:
            target=world.player.rect.centerx
            for dx in (-150,150):
                self.telegraphs.append([max(self.left+50,min(self.right-50,target+dx)),1.05])
        # Upper profiles add mixed attacks, then an additional second phase.
        if self.difficulty and (self.cycle%2==0 or enraged):
            self.telegraphs.append([max(self.left+65,min(self.right-65,world.player.rect.centerx)),1.05 if self.difficulty==1 else .8])
        if self.difficulty==2 and enraged:
            for sign in (-1,1):
                world.projectiles.append(Projectile(x,510,sign*290))

    def update(self,dt,world):
        if not self.alive:
            return
        self.hit_flash=max(0,self.hit_flash-dt)
        if not self.active:
            if world.player.rect.centerx>self.left+130 and len(world.shards)==3:
                self.active=True
                self.phase='warning'
                self.timer=1.3
                world.projectiles=[]
                world.say(self.name+' · '+self.hint)
            return
        for mark in self.telegraphs:
            mark[1]-=dt
            if mark[1]<=0:
                world.projectiles.append(Projectile(mark[0],230,0,440,kind='fall'))
        self.telegraphs=[m for m in self.telegraphs if m[1]>0]
        self.scholarly=any(t in world.answered for t in (world.level_id*2,world.level_id*2+1))
        self.timer-=dt
        p=world.player
        rate=(1,1.15,1.3)[self.difficulty]
        if self.phase=='warning':
            self.direction=1 if p.rect.centerx>self.rect.centerx else -1
            if self.timer<=0:
                self.begin_attack(world)
        elif self.phase=='attack':
            self.attack_time+=dt
            if self.era==1:
                self.rect.x+=self.direction*435*rate*dt
            elif self.era==3:
                self.rect.x+=self.direction*320*rate*dt
                self.rect.bottom=584-math.sin(min(1,self.attack_time/1.15)*math.pi)*145
            elif self.era==0:
                self.rect.bottom=584-math.sin(min(1,self.attack_time/.5)*math.pi)*65
            elif self.era==7 and self.difficulty:
                self.rect.x+=self.direction*215*rate*dt
            if self.timer<=0:
                self.rect.bottom=584
                self.phase='exposed'
                self.timer=(1.65,1.25,.9)[self.difficulty]+(.8 if self.scholarly else 0)
        elif self.phase=='exposed' and self.timer<=0:
            self.phase='warning'
            base=1.2 if self.hp>self.max_hp/2 else .85
            self.timer=max(.48,base-self.difficulty*.16)
            self.cycle+=1
        self.rect.x=max(self.left+190,min(self.right-200-self.rect.w,self.rect.x))
