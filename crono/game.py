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
from .community_ui import CommunityUI
from .expansion_ui import ExpansionUI
from .touch import TouchUI
from .school_settings import SchoolSettingsUI
from .mobile_ui import MobileUI
from .sea_journey import SeaUI
from .story_ui import StoryUI
from .viewport import ViewportUI
from .campaign import MAIN_ERAS,MAIN_LEVELS,TOTAL_LEVELS,DLC_START,ERA_LABELS,DIFFICULTIES,MAIN_ERA_IDS,CHAPTER_ORDER,rank,successor,final_level,unlocked,level_label,chapter_levels,is_rift,is_bonus,DLC_LEVEL_IDS


def duration(seconds):
    value=int(seconds)
    return f'{value//60:02d}:{value%60:02d}'


class Game(ViewportUI,SeaUI,StoryUI,MobileUI,CommunityUI,ExpansionUI,TouchUI,SchoolSettingsUI,TeacherUI,LearningUI,AtlasUI):
    def __init__(self, headless=False, save_file=None,bank_file=None):
        pg.mixer.pre_init(22050,-16,1,512)
        pg.init()
        from .art import font
        font.cache_clear()
        from .art import rendered_text
        rendered_text.cache_clear()
        self.save=Save(save_file)
        self.init_community(save_file)
        self.init_expansion()
        self.init_story()
        self.init_touch()
        self.init_school_settings()
        self.fullscreen=self.save.data['fullscreen'] and not headless
        self.display=pg.display.set_mode((W,H),pg.FULLSCREEN if self.fullscreen else pg.RESIZABLE)
        pg.display.set_caption('CRONO · Ecos del tiempo | Beta educativa 0.8')
        icon=pg.Surface((48,48),pg.SRCALPHA)
        clock_icon(icon,24,24,19,CYAN)
        pg.display.set_icon(icon)
        self.configure_viewport(1280/720)
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
        if hasattr(self,'fingers'):self.fingers.clear()
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
        if self.room_client:self.sync_room()

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
        if hasattr(self,'fingers'):self.fingers.clear()
        self.accumulator=0
        if state not in ('teacher','question_edit','profile_create','room_join','teacher_access','school_settings','reflection'):
            pg.key.stop_text_input()
            pg.key.set_repeat()

    def load(self,index,stage=0,restore=False):
        self.chapter_era=index
        self.world=World(index,stage,self.save.effective_upgrades(),self.save.data['solved'],self.save.combat_band())
        self.world.player.skin=self.save.data['skin']
        self.world.practice_mode=self.save.data['practice']
        self.world.mobile_render=self.touch_enabled()
        topics=self.room_topics if self.room_client is not None and self.room_topics is not None else self.school.config.get('topics',[])
        if topics:
            original=self.world.data['stations']
            self.world.data['stations']=[s for s in original if s[2] in topics] or original[:1]
        if restore:
            self.save.restore(self.world)
        self.camera=max(0,min(self.world.width-W,self.world.player.rect.centerx-W*.37))
        self.particles=[]
        self.flash=0
        self.intro_time=0
        self.autosave=0
        self.set_state('intro')
        self.audio.ambience(self.world.combat_era)
        self.session_started=False

    def continue_game(self):
        if self.resume_voyage():return
        if self.save.data.get('active_rift') is not None:
            if self.save.data.get('rift_finished'):
                self.return_from_rift();return
            self.load(*divmod(self.save.data['active_rift'],3),restore=True);return
        if self.save.data['finished'] and self.save.data['progress'] is None:
            self.world=World(6,2,difficulty=self.save.data['age_band'])
            self.chapter_era=6
            self.set_state('ending')
        else:
            era,stage=divmod(self.save.data['current'],3)
            self.load(era,stage,restore=True)

    def continue_dlc(self):
        if self.resume_voyage():return
        if self.save.data.get('active_rift') is not None:
            self.continue_game();return
        self.chapter_era=7
        if self.save.data['dlc_finished'] and self.save.data['dlc_progress'] is None:
            self.world=World(7,2,difficulty=self.save.data['age_band'])
            self.set_state('ending')
        else:
            era,stage=divmod(self.save.data['dlc_current'],3)
            self.load(era,stage,restore=True)

    def begin(self):
        self.session_started=True
        self.set_state('play')
        self.save.capture(self.world)
        if self.world.level_id==0 and not self.save.data['tutorial_done'] and not self.save.data['practice']:
            self.tutorial_active=True;self.tutorial_step=0

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
            # SDL also emits a mouse event for each finger. Discard it before
            # text-field handlers, otherwise one tap opens two native editors.
            if getattr(event,'touch',False) and event.type in (pg.MOUSEBUTTONDOWN,pg.MOUSEBUTTONUP,pg.MOUSEMOTION):continue
            if self.touch_event(event) or self.binding_event(event) or self.handle_community_event(event) or self.handle_school_event(event):
                continue
            if self.learning_scroll(event):
                continue
            if self.handle_teacher_event(event):
                continue
            if event.type==pg.QUIT:
                if self.state=='voyage':self.persist_voyage()
                self.running=False
            elif event.type==pg.WINDOWFOCUSLOST and self.state=='voyage':
                self.voyage.paused=True;self.persist_voyage()
            elif event.type==pg.JOYDEVICEADDED:
                self.connect_controller()
            elif event.type==pg.JOYDEVICEREMOVED:
                self.joystick=None
                self.joy_jump=False
            elif event.type==pg.WINDOWFOCUSLOST and self.state=='play':
                self.save.capture(self.world)
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
                if self.state=='voyage' and key in (pg.K_ESCAPE,pg.K_p):
                    self.voyage.paused=not self.voyage.paused;continue
                if key==pg.K_F11:
                    self.toggle_fullscreen()
                elif key==pg.K_m:
                    self.toggle_sound()
                elif key==pg.K_F12:
                    self.screenshot()
                elif self.state=='play':
                    if key==pg.K_h:self.set_state('story');continue
                    if key in (self.key_for('jump'),pg.K_UP):
                        self.jump_pending=True
                    elif key==self.key_for('dash'):
                        self.dash_pending=True
                    elif key==self.key_for('attack'):
                        self.shoot_pending=True
                    elif key==self.key_for('interact'):
                        self.interact()
                    elif key==pg.K_u:
                        self.open_panel('workshop')
                    elif key==pg.K_c:
                        self.open_panel('notebook')
                    elif key==pg.K_v:
                        self.open_atlas()
                    elif key==self.key_for('pause'):
                        self.set_state('pause')
                    elif key==pg.K_r:
                        self.world.respawn()
                        self.flash=.2
                elif key==pg.K_ESCAPE:
                    if self.state=='quiz':
                        self.close_quiz()
                    elif self.state in ('workshop','notebook','bestiary','heritage'):
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
        vw=self.viewport_width;scale=min(dw/vw,dh/H)
        return (((pos[0]-(dw-vw*scale)/2)/scale-self.ui_offset[0])/self.ui_scale,
                ((pos[1]-(dh-H*scale)/2)/scale-self.ui_offset[1])/self.ui_scale)

    def screenshot(self,path=None):
        if path is None:
            root=Path(sys.executable).parent if getattr(sys,'frozen',False) else Path(__file__).resolve().parents[1]
            folder=root/'capturas'
            folder.mkdir(exist_ok=True)
            path=folder/f'crono_{system_time.strftime("%Y%m%d_%H%M%S")}.png'
        pg.image.save(self.world_canvas,str(path))
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
        from .mobile import poll_text,poll_files
        poll_text()
        poll_files()
        self.poll_room()
        self.time+=dt
        self.notice_time=max(0,self.notice_time-dt)
        if self.state=='voyage':self.voyage_update(dt);return
        if self.state=='intro':
            self.intro_time+=dt
        if self.state!='play':
            return
        keys=pg.key.get_pressed()
        axis=float(bool(keys[self.key_for('right')] or keys[pg.K_RIGHT] or self.touch_down('right')))-float(bool(keys[self.key_for('left')] or keys[pg.K_LEFT] or self.touch_down('left')))
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
        held=bool(keys[self.key_for('jump')] or keys[pg.K_UP] or self.joy_jump or self.touch_down('jump'))
        self.accumulator+=min(dt,.1)
        tick=1/60 if self.touch_enabled() else STEP
        while self.accumulator>=tick:
            controls=Controls(axis,self.jump_pending,held,self.dash_pending,self.shoot_pending or bool(keys[self.key_for('attack')] or self.touch_down('attack')),bool(keys[self.key_for('drop')] or keys[pg.K_DOWN] or self.touch_down('drop')))
            self.jump_pending=self.dash_pending=False
            self.shoot_pending=False
            old_player=self.world.player
            self.world.mobile_render=self.touch_enabled()
            events=self.world.update(tick,controls)
            self.tutorial_progress(events)
            for e in events:
                self.audio.play(e)
                if e in ('jump','dash','shard','echo','checkpoint','stomp'):
                    self.spawn_particles(e)
                if e in ('hurt','death'):
                    self.flash=.22
                if e in ('checkpoint','shard','boss','field_complete'):
                    self.save.capture(self.world)
            if old_player is not self.world.player:
                self.camera=max(0,min(self.world.width-W,self.world.player.rect.centerx-W*.37))
            self.accumulator-=tick
            if self.world.complete:
                self.save.completed(self.world)
                self.sync_room()
                self.audio.play('portal')
                self.set_state('complete')
                break
        vw=self.viewport_width
        target=max(0,min(self.world.width-vw,self.world.player.rect.centerx-vw*.38+self.world.player.facing*55))
        if self.world.boss and self.world.boss.active and self.world.boss.alive:
            target=self.world.width-vw
        self.camera+=(target-self.camera)*(1-math.exp(-5*dt))
        self.flash=max(0,self.flash-dt)
        for item in self.particles:
            item[0]+=item[2]*dt
            item[1]+=item[3]*dt
            item[3]+=180*dt
            item[4]-=dt
        self.particles=[p for p in self.particles if p[4]>0]
        self.autosave+=dt
        if self.autosave>15 and self.state=='play':
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
        text(s,f'{level_label(self.world.level_id)}  /  {self.world.data["meta"].name}',(80,43),13,MUTED)
        count=4 if self.world.level_id in DLC_LEVEL_IDS else 3 if self.world.index>=9 else MAIN_ERAS
        progress=DLC_LEVEL_IDS.index(self.world.level_id) if self.world.level_id in DLC_LEVEL_IDS else self.world.stage if self.world.index>=9 else MAIN_ERA_IDS.index(self.world.index)
        for i in range(count):
            color=CYAN if i<=progress else (63,80,88)
            x=(557 if count==3 else 507)+i*25
            if i<count-1:
                line(s,(63,80,88),(x+7,39),(x+25,39))
            diamond(s,(x,39),7,color,i<=progress)
        from .journeys import date_for
        text(s,date_for(self.world.level_id)+' · '+('mínima','media','alta')[self.world.difficulty]+f' · {len(self.world.checkpoint_ids)} anclas',(586,63),10,MUTED,False,'center')
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
        if self.save.data['practice']:text(s,'PRUEBA DOCENTE · SIN RANKING',(1175,79),10,GOLD,True,'topright')
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
        if self.world.mechanic.state['step']:
            text(s,self.world.mechanic.field.description(),(W/2,232 if fighting and self.world.message_time>0 else 185 if fighting else 161),13,CYAN,True,'center')
        by=H-34
        rect(s,(13,27,35),(30,by-19,245,39),5)
        line(s,(62,90,93),(47,by),(257,by),2)
        for i,(wx,_) in enumerate(self.world.data['shards']):
            diamond(s,(47+wx/self.world.width*210,by),5,CYAN if i in self.world.shards else GOLD,i in self.world.shards)
        circle(s,PAPER,(47+self.world.player.rect.centerx/self.world.width*210,by),4)
        text(s,f'Ecos {len(self.world.echoes)}/{len(self.world.data["echoes"])}',(285,by),12,GOLD,False,'midleft')
        if not self.touch_enabled():
            self.button('U  Mejoras',(846,H-51,180,35),lambda:self.open_panel('workshop'),small=True,arrow=False)
            self.button('C  Cuaderno',(1040,H-51,206,35),lambda:self.open_panel('notebook'),small=True,arrow=False)
        station=self.world.near_station()
        from .heritage import near_site
        site=near_site(self.world)
        if site:
            rect(s,(12,32,42),(W/2-230,H-110,460,38),5)
            text(s,'E · Conocer esta referencia cultural',(W/2,H-91),16,GOLD,True,'center')
        elif station:
            rect(s,(12,32,42),(W/2-210,H-110,420,38),5)
            text(s,'E  ·  Repasar archivo' if station[2] in self.world.answered else 'E  ·  Descubrir y responder',(W/2,H-91),16,CYAN,True,'center')
        if self.world.time<24 and not self.touch_enabled():
            text(s,'ESPACIO salto · SHIFT impulso · F disparo',(W/2,H-31),12,PAPER,False,'center')

    def menu(self):
        if self.touch_enabled():self.mobile_menu();return
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
        text(s,'36 mapas · rescates, grietas y memorias para descubrir.',(66,318),16,MUTED)
        started=self.save.data['started']
        self.button('Continuar el viaje' if started else 'Comenzar el viaje',(66,411,350,52),
                    self.continue_game if started else lambda:self.load(0),True)
        self.button('Épocas',(66,475,166,46),lambda:self.set_state('chapters'),small=True)
        self.button('Configuración',(244,475,172,46),self.open_settings,small=True)
        self.button('Cuaderno',(66,533,166,43),lambda:self.open_panel('notebook'),small=True)
        self.button('Tutorial',(244,533,172,43),self.start_tutorial,small=True)
        if started:
            self.button('Nuevo viaje',(66,588,211,35),lambda:setattr(self,'confirm_new',True),small=True)
        self.button('Salir',(289 if started else 66,588,127 if started else 350,35),lambda:setattr(self,'running',False),small=True)
        self.button('Perfiles / aula',(450,411,280,52),self.open_community,small=True)
        self.button('Logros y apariencias',(450,475,280,46),self.open_rewards,small=True)
        self.button('Créditos',(450,533,280,43),lambda:self.set_state('credits'),small=True)
        self.age_switch(66,363)
        self.button('Expansiones · Argentina y Brasil',(850,549,360,49),lambda:self.set_state('dlc_menu'),True,small=True)
        line(s,(62,83,83),(66,640),(1214,640))
        for i,label in enumerate(('ORÍGENES','DESHIELO','EGIPTO','GRECIA','MEDIEVO','INDUSTRIA','GUERRAS','PRESENTE')):
            x=66+i*148
            color=CYAN if unlocked(MAIN_ERA_IDS[i]*3,self.save.data['unlocked']) else (112,129,133)
            diamond(s,(x,669),5,color)
            tracked(s,label,(x+18,660),10,color,2)
            if i<MAIN_ERAS-1:
                line(s,(57,77,78),(x+116,669),(x+132,669))
        text(s,f'BETA EDUCATIVA 0.8   /   {len(self.bank.records)} preguntas   ·   F11 pantalla completa',(1212,32),11,MUTED,False,'topright')
        text(s,'EL MUNDO PRIMIGENIO',(1045,604),11,CYAN,True,'center')
        text(s,'© 2026 Renzo Leporace · Todos los derechos reservados',(1212,699),11,MUTED,False,'bottomright')
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
        tracked(self.canvas,f'{ERA_LABELS[self.world.index]} · MAPA {level_label(self.world.level_id)}',(88,118),13,CYAN,3)
        text(self.canvas,self.world.data['meta'].name,(85,164),43,PAPER,True,serif=True)
        from .journeys import date_for
        text(self.canvas,era.name+' · '+date_for(self.world.level_id),(88,233),14,GOLD,True)
        line(self.canvas,(66,92,95),(88,285),(710,285))
        wrapped(self.canvas,self.world.data['meta'].focus,(88,317),770,24,PAPER,True,leading=35)
        wrapped(self.canvas,self.world.data['route_name']+'. V abre el plano. E permite aprender; U abre las mejoras.',(88,390),770,16,MUTED,leading=25)
        text(self.canvas,'Completa la misión histórica, comprende un archivo y reúne 3 fragmentos.',(88,478),16,CYAN)
        self.button('Entrar en este mapa',(88,519,344,57),self.begin,True)
        self.button('Volver',(449,519,157,57),self.to_menu,small=True)
        clock_icon(self.canvas,1030,320,82,CYAN,self.time*.3)
        progress=self.world.stage if self.world.index not in MAIN_ERA_IDS else MAIN_ERA_IDS.index(self.world.index)
        for i in range(3 if self.world.index not in MAIN_ERA_IDS else MAIN_ERAS):
            diamond(self.canvas,(916+i*30,457),8,CYAN if i<=progress else (72,91,98),i<=progress)
        if self.world.index==7:
            from .argentina_history import CONTEXT,SIMPLE_CONTEXT
            context=SIMPLE_CONTEXT if self.world.stage==2 and self.save.data['age_band']==0 else CONTEXT[self.world.stage]
            wrapped(self.canvas,context,(88,591),1100,13,MUTED,leading=19)
        text(self.canvas,'ESPACIO o ENTER para continuar',(88,637),13,MUTED)

    def chapters(self):
        if self.touch_enabled():self.mobile_chapters();return
        s=self.canvas
        self.artist.background(s,0,0,self.time)
        self.dim(220)
        tracked(s,'24 MAPAS DE CAMPAÑA · 4 ARGENTINOS · 5 BONUS · 3 GRIETAS',(65,28),11,CYAN,3)
        text(s,'Las huellas del tiempo',(62,61),39,PAPER,True,serif=True)
        text(s,'Cada ruta tiene desniveles, galerías y atajos. Argentina conserva su propio progreso.',(65,117),16,MUTED)
        for i,era_id in enumerate(CHAPTER_ORDER):
            label=ERA_LABELS[era_id]
            x=65+i%6*195
            y=151+i//6*51
            self.button(label,(x,y,185,44),lambda n=era_id:setattr(self,'chapter_era',n),primary=self.chapter_era==era_id,small=True,arrow=False)
        era=self.chapter_era
        levels=chapter_levels(era)
        for position,level_id in enumerate(levels):
            map_era,stage=divmod(level_id,3)
            meta=STAGES[level_id]
            card_width=1170/len(levels)
            x=65+position*card_width
            available=self.save.can_enter(level_id)
            rect(s,mix(ERAS[map_era].sky,INK,.35),(x,273,card_width-20,330),7)
            tracked(s,f'MAPA {level_label(level_id)}',(x+16,289),11,GOLD,1)
            wrapped(s,meta.name,(x+16,326),card_width-52,23,PAPER,True,leading=29)
            wrapped(s,meta.focus,(x+16,416),card_width-52,15,MUTED,leading=22)
            record=self.save.data['records'].get(str(level_id))
            label='Volver a explorar' if record else 'Entrar' if available else 'Sin descubrir'
            self.button(label,(x+16,537,card_width-52,49),lambda e=map_era,n=stage:self.load(e,n,restore=True),enabled=available,small=True)
        self.button('Volver al inicio',(65,631,260,48),lambda:self.set_state('menu'),small=True)
        text(s,f'{len(self.save.data["records"])} / {TOTAL_LEVELS} mapas completados',(1210,655),15,CYAN,False,'midright')

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
        if self.save.data['practice']:self.button('Pruebas docentes: ir a…',(35,120,335,65),lambda:self.set_state('teacher_tools'),small=True)
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
        text(s,f'Mapa {level_label(self.world.level_id)}   ·   {len(self.world.shards)}/3 fragmentos   ·   {duration(self.world.time)}',(640,609),15,MUTED,False,'center')
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
        last=final_level(self.world.level_id)
        from .progression import map_score
        text(s,f'PUNTUACIÓN {map_score(self.world)["score"]:,} · velocidad + exploración + combate + cuidado',(640,482),16,GOLD,True,'center')
        label='Volver al presente' if last else 'Cruzar a la siguiente época' if self.world.stage==2 else 'Explorar el siguiente mapa'
        def advance():
            if is_rift(self.world.level_id):
                self.return_from_rift()
            elif is_bonus(self.world.level_id):
                self.set_state('chapters')
            elif last:
                self.set_state('ending')
            else:
                era,stage=divmod(successor(self.world.level_id),3)
                self.load(era,stage)
        label='Regresar al mapa de origen' if is_rift(self.world.level_id) else 'Ver rutas desbloqueadas' if is_bonus(self.world.level_id) else label
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
        text(s,f'36 mapas · {len(self.save.data["solved"])} archivos resueltos · {len(self.save.data["upgrades"])} mejoras',(640,394),17,CYAN,False,'center')
        self.button('Volver a explorar',(464,483,352,55),lambda:self.set_state('chapters'),True)
        self.button('Inicio',(464,554,352,47),lambda:self.set_state('menu'),small=True)
        text(s,'CRONO · ECOS DEL TIEMPO',(640,658),13,CYAN,True,'center')
        text(s,'Gracias por jugar esta beta.',(640,686),13,MUTED,False,'center')

    def render(self):
        self.canvas=self.ui_canvas
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
        elif self.state=='heritage':
            self.heritage()
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
        elif self.state=='community':self.community()
        elif self.state in ('profile_create','room_join','teacher_access'):self.community_form()
        elif self.state=='activity':self.activity()
        elif self.state=='rescue_info':self.rescue_info_screen()
        elif self.state=='achievements':self.achievements()
        elif self.state=='skins':self.skins()
        elif self.state=='skin_card':self.skin_card()
        elif self.state=='accessibility':self.accessibility()
        elif self.state=='school_settings':self.school_settings()
        elif self.state=='reflection':self.reflection()
        elif self.state=='teacher_tools':self.teacher_tools()
        elif self.state=='story':self.story_panel()
        elif self.state=='dlc_menu':self.dlc_menu()
        elif self.state=='voyage':self.voyage.draw(self)
        elif self.state=='credits':
            from .credits import draw
            draw(self)
        else:
            self.artist.scene(self.world_canvas,self.world,self.camera,self.time)
            self.canvas.fill((0,0,0,0))
            for x,y,vx,vy,life,color in self.particles:
                circle(self.canvas,color,(x-self.camera,y),max(1,min(3,life*5)))
            self.hud()
            self.story_hud()
            if self.touch_enabled():self.draw_touch()
            if self.flash>0:
                overlay=pg.Surface((W,H),pg.SRCALPHA)
                overlay.fill((205,92,83,int(80*self.flash/.22)))
                self.canvas.blit(overlay,(0,0))
        if self.notice_time>0:
            rect(self.canvas,(17,33,43),(W/2-390,H-78,780,42),5)
            text(self.canvas,self.notice,(W/2,H-57),15,GOLD,False,'center')
        if self.save.warning and self.state=='pause':
            text(self.canvas,self.save.warning,(W/2,H-35),14,GOLD,False,'center')
        self.present()

    def run(self):
        while self.running:
            dt=min(self.clock.tick(120)/1000,.1)
            self.events()
            self.update(dt)
            self.render()
        active=self.state in ('play','pause','help_play','atlas') or (self.state=='quiz' and self.quiz_return=='play') or (self.state in ('workshop','notebook','bestiary','heritage') and self.panel_return in ('play','pause')) or (self.state in ('settings','teacher','question_edit','scenarios') and self.settings_return in ('play','pause'))
        if active or getattr(self,'session_started',False) and not self.world.complete:
            self.save.capture(self.world)
        if self.room:self.room.stop()
        if self.room_pool:self.room_pool.shutdown(wait=False,cancel_futures=True)
        pg.quit()


def font_width(value,size):
    from .art import font
    return font(size).size(value)[0]


def main():
    parser=argparse.ArgumentParser(description='CRONO · Ecos del tiempo')
    parser.add_argument('--headless',action='store_true',help='Render without opening a window')
    parser.add_argument('--serve-ios',action='store_true',help='Host the packaged iPhone web version on the local network')
    parser.add_argument('--port',type=int,default=8080)
    parser.add_argument('--capture',type=Path,help='Write a deterministic screenshot and exit')
    parser.add_argument('--scene',choices=['menu','play','intro','chapters','help','pause','complete','ending','quiz','workshop','notebook','bestiary','boss','settings','teacher','question_edit','scenarios','atlas','heritage','community','school_settings','accessibility','activity','achievements','skins','skin_card','credits','teacher_tools','story','dlc_menu','voyage'],default='menu')
    parser.add_argument('--aspect',type=float,default=16/9,help='Preview a real camera aspect ratio without stretching')
    parser.add_argument('--era',type=int,choices=range(1,13),default=1)
    parser.add_argument('--map',type=int,choices=range(1,4),default=1)
    parser.add_argument('--camera',type=float,default=0)
    parser.add_argument('--touch',action='store_true',help='Preview multitouch controls')
    args=parser.parse_args()
    if args.serve_ios:
        from .ios_host import run
        run(args.port);return
    if args.headless:
        os.environ['SDL_VIDEODRIVER']='dummy'
        os.environ['SDL_AUDIODRIVER']='dummy'
    game=Game(args.headless)
    game.configure_viewport(args.aspect)
    if args.capture:
        game.world=World(args.era-1,args.map-1)
        game.chapter_era=game.world.index
        if args.touch:game.save.data['touch_controls']=True;game.world.mobile_render=True
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
        if args.scene=='teacher_tools':game.save.data['practice']=True
        if args.scene=='voyage':
            from .sea_journey import SeaJourney
            game.voyage=SeaJourney(game.world.level_id,game.world.mechanic.kind if game.world.mechanic.kind in ('canal','tide','naval') else 'naval')
            game.sea_origin=dict(level=game.world.level_id,x=100,y=520,hp=3)
        if args.scene=='question_edit':
            game.edit_question(next(q['id'] for q in game.bank.records if q['topic']==game.world.level_id*2))
        if args.scene=='heritage':
            from .curiosities import MAP_CURIOSITIES
            game.heritage_key=MAP_CURIOSITIES[game.world.level_id]
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
