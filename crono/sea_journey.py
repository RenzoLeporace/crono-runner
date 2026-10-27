from .campaign import TOTAL_LEVELS
"""Separate water-only excursions. Boats never participate in platform physics."""
import math
import pygame as pg
from .art import rect,line,circle,polygon,text,PAPER,CYAN,GOLD,MUTED
from .combat import Projectile

SEA_KINDS={'tide','canal','naval'}

def number(data,key,default,low,high):
    value=data.get(key,default)
    return max(low,min(high,value)) if type(value) in (int,float) and math.isfinite(value) else default

class SeaJourney:
    def __init__(self,level,kind,difficulty=0,state=None,upgrades=()):
        self.level=level;self.kind=kind;self.difficulty=difficulty;self.time=0.;self.width=6800
        self.x=120.;self.y=420.;self.hp=6;self.phase=0;self.collected=set();self.defeated=set()
        self.boss_hp=12;self.shots=[];self.cooldown=0.;self.invincible=0.;self.enemy_clock=1.8
        self.quiz=False;self.quiz_error=False;self.paused=False;self.finished=False;self.deaths=0
        self.enemies=[pg.FRect(x,y,106,46) for x,y in ((960,345),(1750,500),(2960,405),(3550,520),(4270,330),(4960,465))]
        self.cargo=((650,425),(1210,505),(1900,335))
        if isinstance(state,dict):
            self.x=number(state,'x',120,80,6600);self.y=number(state,'y',420,300,565)
            self.hp=int(number(state,'hp',6,1,6));self.phase=int(number(state,'phase',0,0,3))
            self.boss_hp=int(number(state,'boss_hp',12,0,12));self.deaths=int(number(state,'deaths',0,0,100000))
            self.collected={i for i in state.get('collected',[]) if type(i) is int and 0<=i<3} if isinstance(state.get('collected'),list) else set()
            self.defeated={i for i in state.get('defeated',[]) if type(i) is int and 0<=i<6} if isinstance(state.get('defeated'),list) else set()
        self.checkpoint=self.phase;self.hit_reaction=0.;self.boss_hit=0.;self.upgrades=set(upgrades)

    def payload(self):
        return dict(x=self.x,y=self.y,hp=self.hp,phase=self.phase,boss_hp=self.boss_hp,deaths=self.deaths,
                    collected=sorted(self.collected),defeated=sorted(self.defeated))

    def answer(self,index):
        if index!=0:self.quiz_error=True;return False
        self.phase+=1;self.quiz=False;self.quiz_error=False;self.hp=min(6,self.hp+1);return True

    def damage(self):
        if self.invincible:return False
        self.hp-=1;self.invincible=1.5;self.hit_reaction=.45
        self.x=max(80,self.x-22)
        return True

    def update(self,dt,axis,vertical,attack):
        if self.paused or self.quiz or self.finished:return []
        self.hit_reaction=max(0,self.hit_reaction-dt);self.boss_hit=max(0,self.boss_hit-dt)
        self.time+=dt;self.cooldown=max(0,self.cooldown-dt);self.invincible=max(0,self.invincible-dt)
        self.x=max(80,min(6600,self.x+axis*260*dt));self.y=max(300,min(565,self.y+vertical*175*dt))
        self.x=min(self.x,(2250,4400,5500,6600)[self.phase])
        events=[];body=pg.FRect(self.x-40,self.y-20,80,40)
        if attack and self.cooldown<=0:
            shot=Projectile(self.x+58,self.y-12,600,owner='player',damage=2,kind='cannonball')
            shot.range=800 if 'long_pulse' in self.upgrades else 540;shot.ttl=shot.range/600+.03;self.shots.append(shot);self.cooldown=.4;events.append('cannon')
        for i,(x,y) in enumerate(self.cargo):
            if body.inflate(45,40).collidepoint(x,y) and i not in self.collected:self.collected.add(i);events.append('echo')
        self.enemy_clock-=dt
        if self.enemy_clock<=0:
            self.enemy_clock=2.2/(1+self.difficulty*.2)
            for i,e in enumerate(self.enemies):
                if i not in self.defeated and abs(e.centerx-self.x)<680:
                    self.shots.append(Projectile(e.left,e.centery,-220,kind='arrow' if self.kind=='canal' else 'waterjet' if self.kind=='tide' else 'cannonball'))
            if self.phase==3 and self.boss_hp and abs(self.x-6050)<650:
                for offset in ((-55,55) if not self.difficulty else (-70,0,70)):self.shots.append(Projectile(5960,self.y+offset,-250,kind='cannonball'))
        for shot in self.shots:
            shot.update(dt)
            if shot.owner=='player':
                for i,e in enumerate(self.enemies):
                    if i not in self.defeated and e.colliderect(shot.rect):self.defeated.add(i);shot.alive=False;events.append('stomp');break
                if self.phase==3 and self.boss_hp and pg.FRect(5960,365,185,150).colliderect(shot.rect):
                    self.boss_hp=max(0,self.boss_hp-shot.damage);self.boss_hit=.3;shot.alive=False;events.append('block')
            elif body.colliderect(shot.rect) and not self.invincible:
                if self.damage():events.append('hurt')
                shot.alive=False
        self.shots=[s for s in self.shots if s.alive]
        for i,e in enumerate(self.enemies):
            if i not in self.defeated and body.colliderect(e) and self.damage():events.append('hurt')
        if self.hp<=0:
            self.deaths+=1;self.hp=6;self.x=(120,2300,4450,5500)[self.phase];self.y=420;self.shots=[];self.invincible=2;events.append('death')
        if (self.phase==0 and len(self.collected)==3 and self.x>=2100 or
            self.phase==1 and len(self.defeated)>=2 and self.x>=4250 or
            self.phase==2 and self.x>=5350):self.quiz=True
        self.finished=self.phase==3 and self.boss_hp==0 and self.x>6440
        return events

    def boat(self,s,x,y,enemy=False,boss=False):
        from .naval_art import draw_vessel
        draw_vessel(s,self.kind,x,y,self.time,enemy,boss,
                    self.boss_hit if boss else 0 if enemy else self.hit_reaction,
                    0 if enemy else self.invincible,self.hp)

    def draw(self,game):
        s=game.world_canvas;view=game.viewport_width;cam=max(0,min(self.width-view,self.x-320));s.fill((50,92,112))
        polygon(s,(154,153,114),[(0,165),(view*.2,105),(view*.4,172),(view*.7,138),(view,178),(view,235),(0,235)])
        rect(s,(36,98,119),(0,235,view,485))
        for y in range(270,680,42):
            for n in range(view//170+2):
                x=(n*170-cam*.35+self.time*13+y)%(view+140)-100;line(s,(80,145,157),(x,y),(x+55,y),2)
        for i,(x,y) in enumerate(self.cargo):
            if i not in self.collected:
                from .naval_art import cargo_image
                s.blit(cargo_image(),(round(x-cam-33),round(y-35)))
                text(s,'VÍVERES',(x-cam,y-48),11,GOLD,True,'center')
        for i,e in enumerate(self.enemies):
            if i not in self.defeated and -150<e.centerx-cam<view+150:self.boat(s,e.centerx-cam,e.centery,True)
        if self.boss_hp and 5800-cam<view+120:
            self.boat(s,6050-cam,440,True,True);text(s,'GUARDIÁN NAVAL',(6050-cam,275),17,GOLD,True,'center')
            rect(s,(21,43,54),(5960-cam,302,180,9));rect(s,(210,144,86),(5960-cam,302,180*self.boss_hp/12,9))
        self.boat(s,self.x-cam,self.y)
        for shot in self.shots:
            if shot.kind=='arrow':line(s,GOLD,(shot.rect.centerx-cam-12,shot.rect.centery),(shot.rect.centerx-cam+12,shot.rect.centery),3)
            else:circle(s,(92,198,210) if self.kind=='tide' else (38,40,39),(shot.rect.centerx-cam,shot.rect.centery),6)
        line(s,(199,174,113),(6570-cam,300),(6570-cam,590),6)
        rect(s,(95,73,50),(6480-cam,560,250,30))
        rect(s,(199,186,143),(5325-cam,150,35,90));polygon(s,(78,83,76),[(5316-cam,150),(5369-cam,150),(5342-cam,126)])
        circle(s,GOLD,(5342-cam,162),9)
        s=game.ui_canvas;s.fill((0,0,0,0))
        rect(s,(12,28,39),(0,0,1280,104))
        title='El Nilo: agua y abastecimiento' if self.kind=='canal' else 'Brown: convoy del Río de la Plata' if self.kind=='naval' else 'Cretácico: esquife temporal entre mareas'
        text(s,title,(35,20),26,PAPER,True)
        objectives=('Recupera 3 cargas y llega a la primera boya','Despeja 2 ecos acuáticos y alcanza la segunda boya','Alcanza el faro y prepara el paso del convoy','Libera el guardián naval y llega al muelle')
        text(s,objectives[self.phase],(35,61),18,CYAN)
        if self.hit_reaction:text(s,'IMPACTO · −1 CASCO',(640,124),22,(255,158,127),True,'center')
        text(s,f'CASCO {self.hp}/6 · HISTORIA {self.phase}/3',(1205,121),16,GOLD,True,'topright')
        game.button('II',(1200,20,55,53),lambda:setattr(self,'paused',True),small=True)
        if game.touch_enabled() and not self.quiz and not self.paused:game.draw_touch()
        elif not self.quiz and not self.paused:text(s,'A/D rumbo · ↑/↓ timón · F cañón · Esc pausa',(640,687),17,PAPER,False,'center')
        if self.paused:
            game.dim(215);text(s,'El convoy espera',(640,190),40,PAPER,True,'center')
            game.button('Seguir navegando',(350,285,580,80),lambda:setattr(self,'paused',False),True)
            game.button('Volver por la grieta sin completar',(350,390,580,80),lambda:game.leave_voyage(False))
        if self.quiz:
            game.dim(230)
            from .sea_fieldwork import SEA_QUESTIONS
            topics=SEA_QUESTIONS[self.kind]
            prompt,options=topics[self.phase]
            text(s,'Una decisión abre la ruta',(65,100),36,PAPER,True)
            from .learning_ui import wrapped
            wrapped(s,prompt,(65,175),1120,27,CYAN,True)
            # Rotate positions so the correct answer is not always the first.
            order=tuple((i+self.phase+1)%3 for i in range(3))
            for row,index in enumerate(order):game.button(options[index],(65,270+row*100,1140,80),lambda n=index:self.answer(n),small=True,wrap=True)
            text(s,'Pista: piensa en personas, recursos y contexto. Puedes volver a intentar.' if self.quiz_error else 'Una decisión informada abre el siguiente tramo.',(65,610),19,GOLD)

class SeaUI:
    def start_voyage(self,resume=False):
        w=self.world
        self.save.capture(w)
        if not resume:self.sea_origin=dict(level=w.level_id,x=w.player.rect.x,y=w.player.rect.y,hp=w.player.hp)
        state=self.save.data['voyage_progress'].get(str(w.level_id),{})
        self.voyage=SeaJourney(w.level_id,w.mechanic.kind,w.difficulty,state,self.save.effective_upgrades())
        self.set_state('voyage');self.persist_voyage();self.audio.play('portal')

    def persist_voyage(self):
        if self.save.data['practice']:return
        self.save.data['voyage_progress'][str(self.world.level_id)]=self.voyage.payload()
        self.save.data['sea_session']=dict(self.sea_origin);self.save.write()

    def resume_voyage(self):
        origin=self.save.data.get('sea_session')
        if not isinstance(origin,dict) or type(origin.get('level')) is not int or not 0<=origin['level']<TOTAL_LEVELS:return False
        self.sea_origin=origin;self.load(*divmod(origin['level'],3),restore=True)
        if self.world.mechanic.kind not in SEA_KINDS:self.save.data['sea_session']=None;return False
        self.start_voyage(True);return True

    def leave_voyage(self,completed):
        w=self.world;self.persist_voyage()
        if completed:
            w.mechanic.state['sea_complete']=True;w.mechanic.field.distance=900;w.mechanic.field.persist()
            if not self.save.data['practice'] and w.level_id not in self.save.data['voyages_completed']:
                self.save.data['voyages_completed'].append(w.level_id);self.save.data['coins']+=25
            self.save.data['voyage_progress'].pop(str(w.level_id),None)
        w.player.rect.topleft=(number(self.sea_origin,'x',w.player.rect.x,0,w.width-30),number(self.sea_origin,'y',w.player.rect.y,0,700))
        w.player.hp=int(number(self.sea_origin,'hp',w.player.hp,1,w.player.max_hp));w.player.invincible=2
        self.save.data['sea_session']=None;self.save.capture(w);self.save.write();self.set_state('play')
        w.say('Regresaste de la grieta marítima. Travesía registrada y 25 ecos la primera vez.' if completed else 'Volviste al punto de origen. Puedes retomar la travesía desde el puesto del barco.')

    def voyage_update(self,dt):
        keys=pg.key.get_pressed();v=self.voyage
        axis=int(keys[self.key_for('right')] or keys[pg.K_RIGHT] or self.touch_down('right'))-int(keys[self.key_for('left')] or keys[pg.K_LEFT] or self.touch_down('left'))
        vertical=int(keys[pg.K_DOWN] or keys[self.key_for('drop')] or self.touch_down('drop'))-int(keys[pg.K_UP] or keys[self.key_for('jump')] or self.touch_down('jump'))
        for event in v.update(min(dt,.05),axis,vertical,bool(keys[self.key_for('attack')] or self.touch_down('attack'))):self.audio.play(event)
        self.autosave+=dt
        if self.autosave>4:self.persist_voyage();self.autosave=0
        if v.finished:self.leave_voyage(True)
