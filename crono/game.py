import argparse
import math
import os
from pathlib import Path
import sys
import time as system_time
import pygame as pg
from .art import Artist, W, H, INK, PAPER, MUTED, CYAN, GOLD, text, tracked, rect, line, circle, diamond, clock_icon, glow, mix
from .audio import Audio
from .levels import ERAS
from .physics import World, Controls, STEP
from .save import Save, defaults
from .learning_ui import LearningUI, wrapped,wrap_rows
from .education import AGE_BANDS, STAGES
from .teacher_ui import TeacherUI
from .atlas import AtlasUI
from .campaign import MAIN_ERAS,MAIN_LEVELS,TOTAL_LEVELS,DLC_START,ERA_LABELS,DIFFICULTIES


def duration(seconds):
    value=int(seconds)
    return f'{value//60:02d}:{value%60:02d}'


class Game(TeacherUI,LearningUI,AtlasUI):
    def __init__(self, headless=False, save_file=None,bank_file=None):
        pg.mixer.pre_init(22050,-16,1,512)
        pg.init()
        self.save=Save(save_file)
        self.fullscreen=self.save.data['fullscreen'] and not headless
        self.display=pg.display.set_mode((W,H),pg.FULLSCREEN if self.fullscreen else pg.RESIZABLE)
        pg.display.set_caption('CRONO · Ecos del tiempo | Beta educativa 0.5')
        icon=pg.Surface((48,48),pg.SRCALPHA)
        clock_icon(icon,24,24,19,CYAN)
        pg.display.set_icon(icon)
        self.canvas=pg.Surface((W,H))
        self.artist=Artist()
        self.audio=Audio()
        self.audio.enabled=self.save.data['sound']
        self.world=World(0)
        self.init_learning()
        self.init_teacher(bank_file or (Path(save_file).parent/'preguntas.json' if save_file else None))
        self.state='menu'
        self.camera=0.
        self.clock=pg.time.Clock()
        self.running=True
        self.time=0.
        self.accumulator=0.
        self.jump_pending=self.dash_pending=False
        self.shoot_pending=False
        self.joy_jump=False
        self.joystick=None
        self.connect_controller()
        self.buttons=[]
        self.selection=0
        self.mouse=(-100,-100)
        self.particles=[]
        self.flash=0.
        self.intro_time=0.
        self.autosave=0.
        self.notice=self.save.warning
        self.notice_time=6 if self.notice else 0
        self.confirm_new=False
        self.audio.ambience(0)

    def connect_controller(self):
        try:
            if pg.joystick.get_count():
                self.joystick=pg.joystick.Joystick(0)
                self.joystick.init()
        except pg.error:
            self.joystick=None

    def set_state(self,state):
        self.state=state
        self.selection=0
        self.buttons=[]
        self.jump_pending=self.dash_pending=False
        self.shoot_pending=False
        self.accumulator=0
        if state not in ('teacher','question_edit'):
            pg.key.stop_text_input()
            pg.key.set_repeat()

    def load(self,index,stage=0,restore=False):
        self.chapter_era=index
        self.world=World(index,stage,self.save.data['upgrades'],self.save.data['solved'],self.save.data['age_band'])
        if restore:
            self.save.restore(self.world)
        self.camera=max(0,min(self.world.width-W,self.world.player.rect.centerx-W*.37))
        self.particles=[]
        self.flash=0
        self.intro_time=0
        self.autosave=0
        self.set_state('intro')
        self.audio.ambience(index)

    def continue_game(self):
        if self.save.data['finished'] and self.save.data['progress'] is None:
            self.world=World(6,2,difficulty=self.save.data['age_band'])
            self.chapter_era=6
            self.set_state('ending')
        else:
            era,stage=divmod(self.save.data['current'],3)
            self.load(era,stage,restore=True)

    def continue_dlc(self):
        self.chapter_era=7
        if self.save.data['dlc_finished'] and self.save.data['dlc_progress'] is None:
            self.world=World(7,2,difficulty=self.save.data['age_band'])
            self.set_state('ending')
        else:
            era,stage=divmod(self.save.data['dlc_current'],3)
            self.load(era,stage,restore=True)

    def begin(self):
        self.set_state('play')
        self.save.capture(self.world)

    def new_game(self):
        sound,full=self.save.data['sound'],self.save.data['fullscreen']
        age=self.save.data['age_band']
        self.save.data=defaults()
        self.save.data.update(sound=sound,fullscreen=full,age_band=age)
        self.save.write()
        self.load(0)

    def to_menu(self):
        if self.state in ('play','pause','help_play'):
            self.save.capture(self.world)
        self.confirm_new=False
        self.set_state('menu')

    def toggle_sound(self):
        self.audio.toggle(self.world.index)
        self.save.data['sound']=self.audio.enabled
        self.save.write()

    def toggle_fullscreen(self):
        self.fullscreen=not self.fullscreen
        self.display=pg.display.set_mode((W,H),pg.FULLSCREEN if self.fullscreen else pg.RESIZABLE)
        self.save.data['fullscreen']=self.fullscreen
        self.save.write()

    def button(self,label,box,action,primary=False,enabled=True,small=False,arrow=True,wrap=False):
        bounds=pg.Rect(box)
        index=len(self.buttons)
        hover=bounds.collidepoint(self.mouse) or self.selection==index
        self.buttons.append((bounds,action,enabled))
        fill=CYAN if primary else (28,43,51)
        if not enabled:
            fill=(25,34,42)
        elif hover:
            fill=mix(fill,PAPER,.15)
        rect(self.canvas,fill,bounds,5)
        if not primary:
            pg.draw.rect(self.canvas,(76,103,108) if hover and enabled else (47,64,73),bounds,1,border_radius=5)
        color=INK if primary else PAPER if enabled else (93,111,120)
        if wrap:
            from .art import font
            size=17
            while size>12 and len(wrap_rows(label,bounds.w-38,size,True))*(size+5)>bounds.h-20:
                size-=1
            wrapped(self.canvas,label,(bounds.x+19,bounds.y+10),bounds.w-38,size,color,True,leading=size+5)
        else:
            text(self.canvas,label,(bounds.centerx,bounds.centery) if bounds.w<80 or not arrow else (bounds.x+22,bounds.centery),17 if small else 20,color,True,'center' if bounds.w<80 or not arrow else 'midleft')
        if enabled and bounds.w>=80 and arrow:
            x=bounds.right-23
            line(self.canvas,color,(x-5,bounds.centery-4),(x,bounds.centery),2)
            line(self.canvas,color,(x,bounds.centery),(x-5,bounds.centery+4),2)

    def navigate(self,amount):
        if self.buttons:
            self.selection=(self.selection+amount)%len(self.buttons)
            for _ in range(len(self.buttons)):
                if self.buttons[self.selection][2]:
                    break
                self.selection=(self.selection+amount)%len(self.buttons)
            self.audio.play('ui')

    def activate(self):
        if self.buttons and self.selection<len(self.buttons):
            _,action,enabled=self.buttons[self.selection]
            if enabled:
                self.audio.play('ui')
                action()

    def events(self):
        for event in pg.event.get():
            if self.learning_scroll(event):
                continue
            if self.handle_teacher_event(event):
                continue
            if event.type==pg.QUIT:
                self.running=False
            elif event.type==pg.JOYDEVICEADDED:
                self.connect_controller()
            elif event.type==pg.JOYDEVICEREMOVED:
                self.joystick=None
                self.joy_jump=False
            elif event.type==pg.WINDOWFOCUSLOST and self.state=='play':
                self.set_state('pause')
            elif event.type==pg.MOUSEMOTION:
                self.mouse=self.logical_mouse(event.pos)
                for i,(box,_,enabled) in enumerate(self.buttons):
                    if enabled and box.collidepoint(self.mouse):
                        self.selection=i
            elif event.type==pg.MOUSEBUTTONDOWN and event.button==1:
                pos=self.logical_mouse(event.pos)
                for box,action,enabled in self.buttons[:]:
                    if enabled and box.collidepoint(pos):
                        self.audio.play('ui')
                        action()
                        break
            elif event.type==pg.KEYDOWN:
                key=event.key
                if key==pg.K_F11:
                    self.toggle_fullscreen()
                elif key==pg.K_m:
                    self.toggle_sound()
                elif key==pg.K_F12:
                    self.screenshot()
                elif self.state=='play':
                    if key in (pg.K_SPACE,pg.K_w,pg.K_UP):
                        self.jump_pending=True
                    elif key in (pg.K_LSHIFT,pg.K_RSHIFT,pg.K_x):
                        self.dash_pending=True
                    elif key==pg.K_f:
                        self.shoot_pending=True
                    elif key==pg.K_e:
                        self.interact()
                    elif key==pg.K_u:
                        self.open_panel('workshop')
                    elif key==pg.K_c:
                        self.open_panel('notebook')
                    elif key==pg.K_v:
                        self.open_atlas()
                    elif key in (pg.K_ESCAPE,pg.K_p):
                        self.set_state('pause')
                    elif key==pg.K_r:
                        self.world.respawn()
                        self.flash=.2
                elif key==pg.K_ESCAPE:
                    if self.state=='quiz':
                        self.close_quiz()
                    elif self.state in ('workshop','notebook','bestiary'):
                        self.close_panel()
                    elif self.state=='atlas':
                        self.set_state(self.atlas_return)
                    elif self.state in ('pause','help_play'):
                        self.set_state('play')
                    elif self.state=='intro':
                        self.begin()
                    elif self.state not in ('menu','ending'):
                        self.set_state('menu')
                    elif self.confirm_new:
                        self.confirm_new=False
                elif key in (pg.K_DOWN,pg.K_s,pg.K_TAB):
                    self.navigate(1)
                elif key in (pg.K_UP,pg.K_w):
                    self.navigate(-1)
                elif key in (pg.K_RETURN,pg.K_SPACE):
                    self.activate()
                elif self.state=='quiz' and self.quiz_mode=='question' and key in (pg.K_1,pg.K_2,pg.K_3):
                    self.answer_question(key-pg.K_1)
            elif event.type==pg.JOYBUTTONDOWN:
                if event.button==0:
                    self.joy_jump=True
                    if self.state=='play':
                        self.jump_pending=True
                    else:
                        self.activate()
                elif event.button in (2,5) and self.state=='play':
                    self.dash_pending=True
                elif event.button==1 and self.state=='play':
                    self.shoot_pending=True
                elif event.button==3 and self.state=='play':
                    self.interact()
                elif event.button in (6,7):
                    if self.state=='play':
                        self.set_state('pause')
                    elif self.state=='pause':
                        self.set_state('play')
            elif event.type==pg.JOYBUTTONUP and event.button==0:
                self.joy_jump=False
            elif event.type==pg.JOYHATMOTION and self.state!='play':
                if event.value[1]:
                    self.navigate(-event.value[1])

    def logical_mouse(self,pos):
        dw,dh=self.display.get_size()
        scale=min(dw/W,dh/H)
        return ((pos[0]-(dw-W*scale)/2)/scale,(pos[1]-(dh-H*scale)/2)/scale)

    def screenshot(self,path=None):
        if path is None:
            root=Path(sys.executable).parent if getattr(sys,'frozen',False) else Path(__file__).resolve().parents[1]
            folder=root/'capturas'
            folder.mkdir(exist_ok=True)
            path=folder/f'crono_{system_time.strftime("%Y%m%d_%H%M%S")}.png'
        pg.image.save(self.canvas,str(path))
        self.notice='Captura guardada en la carpeta capturas'
        self.notice_time=3

    def spawn_particles(self,event):
        p=self.world.player.rect
        color=CYAN if event in ('dash','shard','checkpoint') else GOLD
        count=25 if event in ('shard','checkpoint') else 10
        for n in range(count):
            a=n*2.399+self.time
            speed=40+n%7*25
            self.particles.append([p.centerx,p.centery,math.cos(a)*speed,math.sin(a)*speed-.3*speed,
                                   .35+n%5*.1,color])

    def update(self,dt):
        self.time+=dt
        self.notice_time=max(0,self.notice_time-dt)
        if self.state=='intro':
            self.intro_time+=dt
        if self.state!='play':
            return
        keys=pg.key.get_pressed()
        axis=float(bool(keys[pg.K_d] or keys[pg.K_RIGHT]))-float(bool(keys[pg.K_a] or keys[pg.K_LEFT]))
        if self.joystick:
            try:
                stick=self.joystick.get_axis(0)
                if abs(stick)>.2:
                    axis=stick
                if self.joystick.get_numhats():
                    hat=self.joystick.get_hat(0)[0]
                    if hat:
                        axis=hat
            except pg.error:
                self.joystick=None
        held=bool(keys[pg.K_SPACE] or keys[pg.K_w] or keys[pg.K_UP] or self.joy_jump)
        self.accumulator+=min(dt,.1)
        while self.accumulator>=STEP:
            controls=Controls(axis,self.jump_pending,held,self.dash_pending,self.shoot_pending or bool(keys[pg.K_f]),bool(keys[pg.K_s] or keys[pg.K_DOWN]))
            self.jump_pending=self.dash_pending=False
            self.shoot_pending=False
            old_player=self.world.player
            events=self.world.update(STEP,controls)
            for e in events:
                self.audio.play(e)
                if e in ('jump','dash','shard','echo','checkpoint','stomp'):
                    self.spawn_particles(e)
                if e in ('hurt','death'):
                    self.flash=.22
                if e in ('checkpoint','shard','boss'):
                    self.save.capture(self.world)
            if old_player is not self.world.player:
                self.camera=max(0,min(self.world.width-W,self.world.player.rect.centerx-W*.37))
            self.accumulator-=STEP
            if self.world.complete:
                self.save.completed(self.world)
                self.audio.play('portal')
                self.set_state('complete')
                break
        target=max(0,min(self.world.width-W,self.world.player.rect.centerx-W*.38+self.world.player.facing*55))
        if self.world.boss and self.world.boss.active and self.world.boss.alive:
            target=self.world.width-W
        self.camera+=(target-self.camera)*(1-math.exp(-5*dt))
        self.flash=max(0,self.flash-dt)
        for item in self.particles:
            item[0]+=item[2]*dt
            item[1]+=item[3]*dt
            item[3]+=180*dt
            item[4]-=dt
        self.particles=[p for p in self.particles if p[4]>0]
        self.autosave+=dt
        if self.autosave>15:
            self.save.capture(self.world)
            self.autosave=0

    def hud(self):
        s=self.canvas
        panel=pg.Surface((W,91),pg.SRCALPHA)
        panel.fill((9,19,28,228))
        s.blit(panel,(0,0))
        line(s,(49,73,79),(28,90),(W-28,90))
        clock_icon(s,48,41,19,CYAN,self.world.time*.4)
        tracked(s,'CRONO',(80,19),13,PAPER,3)
        text(s,f'{self.world.index+1}.{self.world.stage+1}  /  {self.world.data["meta"].name}',(80,43),13,MUTED)
        count=3 if self.world.index==7 else MAIN_ERAS
        progress=self.world.stage if self.world.index==7 else self.world.index
        for i in range(count):
            color=CYAN if i<=progress else (63,80,88)
            x=(557 if count==3 else 507)+i*25
            if i<count-1:
                line(s,(63,80,88),(x+7,39),(x+25,39))
            diamond(s,(x,39),7,color,i<=progress)
        text(s,ERAS[self.world.index].date+' · '+('mínima','media','alta')[self.world.difficulty],(586,63),10,MUTED,False,'center')
        for i in range(3):
            diamond(s,(801+i*23,32),10,CYAN if i<len(self.world.shards) else (65,91,95),i<len(self.world.shards))
        text(s,'FRAGMENTOS',(825,59),10,MUTED,True,'center')
        for i in range(self.world.player.max_hp):
            circle(s,(227,144,117) if i<self.world.player.hp else (65,67,72),(921+i*17,32),5)
        text(s,'ENERGÍA',(948,59),10,MUTED,True,'center')
        ready=self.world.player.dash_ready and self.world.player.cooldown<=0
        rect(s,(38,59,65),(1025,24,77,7),3)
        fraction=1 if ready else max(0,1-self.world.player.cooldown/.46) if self.world.player.grounded else 0
        if fraction>0:
            rect(s,CYAN if ready else (66,129,127),(1025,24,77*fraction,7),3)
        text(s,'IMPULSO',(1064,59),10,CYAN if ready else MUTED,True,'center')
        text(s,f'{self.save.data["knowledge"]:02d}',(1151,27),19,GOLD,True,'center')
        text(s,'SABER',(1151,59),10,MUTED,True,'center')
        self.button('II',(1200,22,51,43),lambda:self.set_state('pause'),small=True)
        boss=self.world.boss
        fighting=boss and boss.active and boss.alive
        if fighting:
            rect(s,(15,26,37),(350,105,580,59),6)
            color=GOLD if boss.phase=='exposed' else (224,132,114)
            text(s,boss.name,(370,112),16,PAPER,True)
            rect(s,(55,61,70),(370,144,540,8),3)
            if boss.hp:
                rect(s,color,(370,144,540*boss.hp/boss.max_hp,8),3)
            label='NÚCLEO ABIERTO · F' if boss.phase=='exposed' else 'PREPARA: '+boss.hint if boss.phase=='warning' else 'ESQUIVA'
            text(s,label,(906,119),11,color,True,'topright')
        if self.world.message_time>0:
            message=self.world.message
            tw=font_width(message,16)+46
            yy=175 if fighting else 111
            rect(s,(14,31,39),(W/2-tw/2,yy,tw,41),5)
            text(s,message,(W/2,yy+20),16,CYAN,False,'center')
        elif self.world.time<14 and not fighting:
            text(s,'Reúne 3 fragmentos y encuentra el umbral',(W/2,123),16,PAPER,False,'center')
        by=H-34
        rect(s,(13,27,35),(30,by-19,245,39),5)
        line(s,(62,90,93),(47,by),(257,by),2)
        for i,(wx,_) in enumerate(self.world.data['shards']):
            diamond(s,(47+wx/self.world.width*210,by),5,CYAN if i in self.world.shards else GOLD,i in self.world.shards)
        circle(s,PAPER,(47+self.world.player.rect.centerx/self.world.width*210,by),4)
        text(s,f'Ecos {len(self.world.echoes)}/{len(self.world.data["echoes"])}',(285,by),12,GOLD,False,'midleft')
        self.button('U  Mejoras',(846,H-51,180,35),lambda:self.open_panel('workshop'),small=True,arrow=False)
        self.button('C  Cuaderno',(1040,H-51,206,35),lambda:self.open_panel('notebook'),small=True,arrow=False)
        station=self.world.near_station()
        if station:
            rect(s,(12,32,42),(W/2-210,H-110,420,38),5)
            text(s,'E  ·  Repasar archivo' if station[2] in self.world.answered else 'E  ·  Descubrir y responder',(W/2,H-91),16,CYAN,True,'center')
        if self.world.time<24:
            text(s,'ESPACIO salto · SHIFT impulso · F disparo',(W/2,H-31),12,PAPER,False,'center')

    def menu(self):
        s=self.canvas
        self.artist.background(s,0,230,self.time)
        from .physics import Platform
        p=Platform(dict(x=650,y=544,w=650,h=190,moving=False))
        s.blit(self.artist.platform_image(p,0),(650,544))
        self.artist.portal(s,1050,544,self.time,True,1.85)
        hero=self.world.player
        old=(hero.grounded,hero.vx,hero.facing)
        hero.grounded=True
        hero.vx=0
        hero.facing=1
        self.artist.player(s,hero,0,self.time,1.9,(836,544))
        hero.grounded,hero.vx,hero.facing=old
        from .art import fern,tree
        tree(s,1220,550,320,(22,51,55))
        fern(s,746,565,1.35,(48,92,79),-1)
        fern(s,1190,573,1.3,(29,66,63),-1)
        s.blit(self.artist.menu_shade,(0,0))
        clock_icon(s,68,63,18,CYAN,self.time*.2)
        tracked(s,'UN VIAJE PARA VOLVER A CASA',(103,54),12,CYAN,2)
        text(s,'CRONO',(58,100),116,PAPER,True,serif=True)
        tracked(s,'E C O S  D E L  T I E M P O',(66,229),17,GOLD,3)
        text(s,'El pasado te separa de tu hogar.',(66,284),22,PAPER)
        text(s,'21 mapas + Argentina. Rutas amplias y combate por edad.',(66,318),16,MUTED)
        started=self.save.data['started']
        self.button('Continuar el viaje' if started else 'Comenzar el viaje',(66,411,350,52),
                    self.continue_game if started else lambda:self.load(0),True)
        self.button('Épocas',(66,475,166,46),lambda:self.set_state('chapters'),small=True)
        self.button('Configuración',(244,475,172,46),self.open_settings,small=True)
        self.button('Cuaderno',(66,533,166,43),lambda:self.open_panel('notebook'),small=True)
        self.button('Cómo jugar',(244,533,172,43),lambda:self.set_state('help'),small=True)
        if started:
            self.button('Nuevo viaje',(66,588,211,35),lambda:setattr(self,'confirm_new',True),small=True)
        self.button('Salir',(289 if started else 66,588,127 if started else 350,35),lambda:setattr(self,'running',False),small=True)
        self.age_switch(66,363)
        self.button('Argentina · expansión incluida',(850,549,360,49),self.continue_dlc,True,small=True)
        line(s,(62,83,83),(66,640),(1214,640))
        for i,label in enumerate(('ORÍGENES','DESHIELO','GRECIA','MEDIEVO','INDUSTRIA','GUERRAS','PRESENTE')):
            x=75+i*170
            color=CYAN if i*3<=self.save.data['unlocked'] else (112,129,133)
            diamond(s,(x,669),5,color)
            tracked(s,label,(x+18,660),10,color,2)
            if i<MAIN_ERAS-1:
                line(s,(57,77,78),(x+125,669),(x+150,669))
        text(s,f'BETA EDUCATIVA 0.5   /   {len(self.bank.records)} preguntas   ·   F11 pantalla completa',(1212,32),11,MUTED,False,'topright')
        text(s,'EL MUNDO PRIMIGENIO',(1045,604),11,CYAN,True,'center')
        if self.confirm_new:
            self.dim(210)
            self.buttons=[]
            rect(s,(18,32,42),(360,232,560,250),8)
            text(s,'¿Volver al principio?',(400,267),30,PAPER,True,serif=True)
            text(s,'Se reiniciarán los mapas, el conocimiento y las mejoras.',(400,320),16,MUTED)
            self.button('Conservar viaje',(400,393,217,50),lambda:setattr(self,'confirm_new',False),True,small=True)
            self.button('Reiniciar',(633,393,247,50),self.new_game,small=True)

    def dim(self,alpha=185):
        overlay=pg.Surface((W,H),pg.SRCALPHA)
        overlay.fill((5,13,23,alpha))
        self.canvas.blit(overlay,(0,0))

    def intro(self):
        self.artist.scene(self.canvas,self.world,self.camera,self.time)
        self.dim(195)
        era=ERAS[self.world.index]
        tracked(self.canvas,f'{"ARGENTINA · DLC" if self.world.index==7 else "ÉPOCA "+str(self.world.index+1)+" / 7"} · MAPA {self.world.stage+1} / 3',(88,118),13,CYAN,3)
        text(self.canvas,self.world.data['meta'].name,(85,164),43,PAPER,True,serif=True)
        text(self.canvas,era.name+' · '+era.date,(88,233),14,GOLD,True)
        line(self.canvas,(66,92,95),(88,285),(710,285))
        wrapped(self.canvas,self.world.data['meta'].focus,(88,317),770,24,PAPER,True,leading=35)
        wrapped(self.canvas,self.world.data['route_name']+'. V abre el plano. E permite aprender; U abre las mejoras.',(88,390),770,16,MUTED,leading=25)
        text(self.canvas,'3 fragmentos + el guardián final abren la siguiente época.' if self.world.stage==2 else 'Reúne 3 fragmentos para abrir el camino al siguiente mapa.',(88,478),16,CYAN)
        self.button('Entrar en este mapa',(88,519,344,57),self.begin,True)
        self.button('Volver',(449,519,157,57),self.to_menu,small=True)
        clock_icon(self.canvas,1030,320,82,CYAN,self.time*.3)
        progress=self.world.stage if self.world.index==7 else self.world.index
        for i in range(3 if self.world.index==7 else MAIN_ERAS):
            diamond(self.canvas,(926+i*32,457),8,CYAN if i<=progress else (72,91,98),i<=progress)
        text(self.canvas,'ESPACIO o ENTER para continuar',(88,637),13,MUTED)

    def chapters(self):
        s=self.canvas
        self.artist.background(s,0,0,self.time)
        self.dim(220)
        tracked(s,'21 MAPAS DE CAMPAÑA + 3 DE ARGENTINA',(65,28),11,CYAN,3)
        text(s,'Las huellas del tiempo',(62,61),39,PAPER,True,serif=True)
        text(s,'Cada ruta tiene desniveles, galerías y atajos. Argentina conserva su propio progreso.',(65,117),16,MUTED)
        for i,label in enumerate(ERA_LABELS):
            x=65+i%4*292
            y=160+i//4*56
            self.button(label,(x,y,274,44),lambda n=i:setattr(self,'chapter_era',n),primary=self.chapter_era==i,small=True,arrow=False)
        era=self.chapter_era
        for stage in range(3):
            level_id=era*3+stage
            meta=STAGES[level_id]
            x=65+stage*390
            unlocked=level_id<=self.save.data['dlc_unlocked' if era==7 else 'unlocked']
            rect(s,mix(ERAS[era].sky,INK,.35),(x,286,365,304),7)
            tracked(s,f'MAPA {stage+1} / 3'+(' · GUARDIÁN' if stage==2 else ''),(x+21,301),11,GOLD,1)
            wrapped(s,meta.name,(x+21,339),324,25,PAPER,True,leading=32)
            wrapped(s,meta.focus,(x+21,424),324,16,MUTED,leading=23)
            record=self.save.data['records'].get(str(level_id))
            label='Volver a explorar' if record else 'Entrar' if unlocked else 'Sin descubrir'
            self.button(label,(x+20,520,325,49),lambda e=era,n=stage:self.load(e,n),enabled=unlocked,small=True)
        self.button('Volver al inicio',(65,631,260,48),lambda:self.set_state('menu'),small=True)
        text(s,f'{len(self.save.data["records"])} / 24 mapas completados',(1210,655),15,CYAN,False,'midright')

    def help(self):
        s=self.canvas
        if self.state=='help_play':
            self.artist.scene(s,self.world,self.camera,self.time)
        else:
            self.artist.background(s,0,0,self.time)
        self.dim(220)
        tracked(s,'TU RELOJ ES LA LLAVE',(85,49),12,CYAN,3)
        text(s,'Aprende a cruzar el tiempo',(82,83),45,PAPER,True,serif=True)
        rows=[('A / D  o  ← / →','Moverte','Conserva el control también en el aire.'),
              ('ESPACIO / W / ↑','Saltar','Mantén para saltar alto; suelta para un salto corto.'),
              ('SHIFT / X','Impulso temporal','Cruza el aire y atraviesa enemigos. Se recarga al aterrizar.'),
              ('F','Pulso temporal','Dispara. Los jefes reciben daño cuando exponen su núcleo.'),
              ('E','Aprender','Activa archivos, lee y responde una pregunta al azar.'),
              ('U / C','Mejoras / cuaderno','Usa el conocimiento para mejorar tu equipo o repasa tus hallazgos.'),
              ('V · S / ↓','Plano / descender','Consulta las rutas o baja a través de las pasarelas delgadas.'),
              ('ESC / P · R','Pausa / ancla','Pausa la partida o reaparece en tu último punto de control.')]
        for i,(key,action,description) in enumerate(rows):
            y=150+i*48
            rect(s,(28,47,56),(85,y,228,41),5)
            text(s,key,(103,y+20),15,CYAN,True,'midleft')
            text(s,action,(341,y-2),18,PAPER,True)
            text(s,description,(341,y+24),14,MUTED)
        line(s,(51,76,83),(85,550),(1194,550))
        text(s,'La edad cambia preguntas y combate. Los archivos del jefe prolongan su vulnerabilidad.',(85,567),16,PAPER)
        text(s,'Mando: palanca · A salto · X / RB impulso · B disparo · Y archivo · START pausa',(85,599),14,MUTED)
        self.button('Entendido',(85,637,236,48),lambda:self.set_state('play' if self.state=='help_play' else 'menu'),True,small=True)
        text(s,'F11 pantalla completa   ·   M sonido   ·   F12 captura',(1193,660),13,MUTED,False,'midright')

    def pause(self):
        self.artist.scene(self.canvas,self.world,self.camera,self.time)
        self.dim(205)
        s=self.canvas
        rect(s,(17,31,42),(410,65,460,615),8)
        tracked(s,'EL TIEMPO PUEDE ESPERAR',(451,90),11,CYAN,2)
        text(s,'Una pausa en el viaje',(450,126),32,PAPER,True,serif=True)
        self.button('Continuar',(450,194,380,47),lambda:self.set_state('play'),True)
        def retry():
            self.world.respawn()
            self.set_state('play')
        self.button('Volver al ancla',(450,252,380,43),retry,small=True)
        self.button('Taller de mejoras',(450,306,380,43),lambda:self.open_panel('workshop'),small=True)
        self.button('Cuaderno de campo',(450,360,380,43),lambda:self.open_panel('notebook'),small=True)
        self.button('V · Mapa de rutas',(450,414,380,43),self.open_atlas,small=True)
        self.button('Configuración y docentes',(450,468,380,43),self.open_settings,small=True)
        self.button('Guardar y volver al inicio',(450,522,380,43),self.to_menu,small=True)
        text(s,f'Mapa {self.world.index+1}.{self.world.stage+1}   ·   {len(self.world.shards)}/3 fragmentos   ·   {duration(self.world.time)}',(640,609),15,MUTED,False,'center')
        text(s,'ESC para continuar',(640,648),12,MUTED,False,'center')

    def complete(self):
        s=self.canvas
        self.artist.scene(s,self.world,self.camera,self.time)
        self.dim(205)
        clock_icon(s,640,124,36,CYAN,self.time)
        tracked(s,'UMBRAL ESTABILIZADO',(464,191),13,CYAN,4)
        text(s,'Un paso más cerca de casa',(640,253),48,PAPER,True,'center',True)
        text(s,self.world.data['meta'].name,(640,311),19,MUTED,False,'center')
        for x,value,label in ((440,'3 / 3','FRAGMENTOS'),(640,f'{len(self.world.echoes)} / {len(self.world.data["echoes"])}','ECOS RECUPERADOS'),(840,duration(self.world.time),'TIEMPO EN ESTA ÉPOCA')):
            text(s,value,(x,395),35,CYAN if x==440 else PAPER,True,'center')
            tracked(s,label,(x-75,439),10,MUTED,1)
        line(s,(55,80,86),(340,484),(940,484))
        last=self.world.level_id in (MAIN_LEVELS-1,TOTAL_LEVELS-1)
        label='Volver al presente' if last else 'Cruzar a la siguiente época' if self.world.stage==2 else 'Explorar el siguiente mapa'
        def advance():
            if last:
                self.set_state('ending')
            else:
                era,stage=divmod(self.world.level_id+1,3)
                self.load(era,stage)
        self.button(label,(409,531,462,58),advance,True)
        self.button('Guardar y volver al inicio',(409,606,462,45),lambda:self.set_state('menu'),small=True)

    def ending(self):
        s=self.canvas
        self.artist.background(s,1,0,self.time)
        self.dim(90)
        for i in range(17):
            x=i*83
            height=80+(i*57)%140
            rect(s,(28,48,66),(x,580-height,68,height+160))
            for j in range(3):
                for k in range(height//31-1):
                    rect(s,(157,187,172),(x+12+j*18,590-height+k*28,6,10))
        self.dim(95)
        clock_icon(s,640,115,35,CYAN,0)
        tracked(s,'COORDENADAS ENCONTRADAS',(434,185),12,CYAN,3)
        text(s,'Memoria recuperada.' if self.world.index==7 else 'Estás en casa.',(640,275),76,PAPER,True,'center',True)
        text(s,'El presente ya no parece un lugar tan corriente.',(640,351),23,PAPER,False,'center')
        text(s,f'21 mapas + Argentina · 8 guardianes · {len(self.save.data["solved"])} archivos resueltos · {len(self.save.data["upgrades"])} mejoras',(640,394),17,CYAN,False,'center')
        self.button('Volver a explorar',(464,483,352,55),lambda:self.set_state('chapters'),True)
        self.button('Inicio',(464,554,352,47),lambda:self.set_state('menu'),small=True)
        text(s,'CRONO · ECOS DEL TIEMPO',(640,658),13,CYAN,True,'center')
        text(s,'Gracias por jugar esta beta.',(640,686),13,MUTED,False,'center')

    def render(self):
        self.buttons=[]
        if self.state=='menu':
            self.menu()
        elif self.state=='chapters':
            self.chapters()
        elif self.state in ('help','help_play'):
            self.help()
        elif self.state=='intro':
            self.intro()
        elif self.state=='pause':
            self.pause()
        elif self.state=='complete':
            self.complete()
        elif self.state=='ending':
            self.ending()
        elif self.state=='quiz':
            self.quiz()
        elif self.state=='workshop':
            self.workshop()
        elif self.state=='notebook':
            self.notebook()
        elif self.state=='bestiary':
            self.bestiary()
        elif self.state=='atlas':
            self.atlas()
        elif self.state=='settings':
            self.settings()
        elif self.state=='teacher':
            self.teacher()
        elif self.state=='question_edit':
            self.question_edit()
        elif self.state=='scenarios':
            self.scenarios()
        else:
            self.artist.scene(self.canvas,self.world,self.camera,self.time)
            for x,y,vx,vy,life,color in self.particles:
                circle(self.canvas,color,(x-self.camera,y),max(1,min(3,life*5)))
            self.hud()
            if self.flash>0:
                overlay=pg.Surface((W,H),pg.SRCALPHA)
                overlay.fill((205,92,83,int(80*self.flash/.22)))
                self.canvas.blit(overlay,(0,0))
        if self.notice_time>0:
            rect(self.canvas,(17,33,43),(W/2-390,H-78,780,42),5)
            text(self.canvas,self.notice,(W/2,H-57),15,GOLD,False,'center')
        if self.save.warning and self.state=='pause':
            text(self.canvas,self.save.warning,(W/2,H-35),14,GOLD,False,'center')
        dw,dh=self.display.get_size()
        ratio=min(dw/W,dh/H)
        size=(max(1,int(W*ratio)),max(1,int(H*ratio)))
        self.display.fill((5,9,14))
        image=self.canvas if size==(W,H) else pg.transform.smoothscale(self.canvas,size)
        self.display.blit(image,((dw-size[0])//2,(dh-size[1])//2))
        pg.display.flip()

    def run(self):
        while self.running:
            dt=min(self.clock.tick(120)/1000,.1)
            self.events()
            self.update(dt)
            self.render()
        active=self.state in ('play','pause','help_play','atlas') or (self.state=='quiz' and self.quiz_return=='play') or (self.state in ('workshop','notebook','bestiary') and self.panel_return in ('play','pause')) or (self.state in ('settings','teacher','question_edit','scenarios') and self.settings_return in ('play','pause'))
        if active:
            self.save.capture(self.world)
        pg.quit()


def font_width(value,size):
    from .art import font
    return font(size).size(value)[0]


def main():
    parser=argparse.ArgumentParser(description='CRONO · Ecos del tiempo')
    parser.add_argument('--headless',action='store_true',help='Render without opening a window')
    parser.add_argument('--capture',type=Path,help='Write a deterministic screenshot and exit')
    parser.add_argument('--scene',choices=['menu','play','intro','chapters','help','pause','complete','ending','quiz','workshop','notebook','bestiary','boss','settings','teacher','question_edit','scenarios','atlas'],default='menu')
    parser.add_argument('--era',type=int,choices=range(1,9),default=1)
    parser.add_argument('--map',type=int,choices=range(1,4),default=1)
    parser.add_argument('--camera',type=float,default=0)
    args=parser.parse_args()
    if args.headless:
        os.environ['SDL_VIDEODRIVER']='dummy'
        os.environ['SDL_AUDIODRIVER']='dummy'
    game=Game(args.headless)
    if args.capture:
        game.world=World(args.era-1,args.map-1)
        game.state=args.scene
        game.time=8
        game.world.time=8
        game.camera=max(0,min(game.world.width-W,args.camera))
        if args.scene=='play' and args.camera:
            game.world.player.rect.topleft=(game.camera+W*.38,440)
        if args.scene=='quiz':
            game.quiz_topic=game.world.level_id*2
            game.question=game.bank.choose(game.quiz_topic,game.save.data['age_band'])
            game.quiz_mode='question'
        if args.scene=='boss':
            game.world=World(args.era-1,2)
            game.world.shards={0,1,2}
            game.world.player.rect.midbottom=(game.world.data['arena_left']+200,584)
            game.world.boss.active=True
            game.world.boss.phase='warning'
            game.world.boss.timer=.8
            game.camera=game.world.width-W
            game.state='play'
        if args.scene=='question_edit':
            game.edit_question(0)
        if args.scene=='scenarios':
            game.preview_level=game.world.level_id
            game.change_scenario(0)
        if args.scene=='atlas':
            game.atlas_return='play'
        game.render()
        args.capture.parent.mkdir(parents=True,exist_ok=True)
        game.screenshot(args.capture)
        pg.quit()
    else:
        game.run()
