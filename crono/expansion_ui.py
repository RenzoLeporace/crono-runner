from .campaign import TOTAL_LEVELS
"""Exploration missions, reversible rift excursions and persistent rewards."""
import pygame as pg
from .art import text,tracked,rect,line,circle,diamond,polygon,PAPER,CYAN,GOLD,MUTED
from .learning_ui import wrapped
from .journeys import rescue_for,RIFTS
from .campaign import is_rift

def prepare_world(world):
    rescue=rescue_for(world.level_id);world.rescue_site=None;world.rift_site=None
    if rescue:
        key,item=rescue
        # Existing upper galleries are genuine optional branches with returns.
        ledges=[p for p in world.platforms if p.oneway and not p.moving and p.rect.w>=180]
        platform=min(ledges,key=lambda p:abs(p.rect.centerx-world.width*.43))
        world.rescue_site=(platform.rect.centerx,platform.rect.top,key,item)
        candidates=sorted(range(len(world.enemies)),key=lambda i:abs(world.enemies[i].rect.centerx-platform.rect.centerx))
        world.rescue_guards=tuple(candidates[:2])
    if world.level_id in RIFTS:
        floors=[p for p in world.platforms if not p.oneway and p.rect.w>=280]
        platform=min(floors,key=lambda p:abs(p.rect.centerx-world.width*.67))
        world.rift_site=(platform.rect.centerx,platform.rect.top,RIFTS[world.level_id])

def draw_missions(s,world,camera,t):
    if world.rescue_site:
        wx,y,key,item=world.rescue_site;x=wx-camera
        if -220<x<s.get_width()+220:
            liberated=key in world.rescues_this_run
            circle(s,(202,158,119),(x,y-76),10);polygon(s,(77,116,118),[(x-10,y-63),(x+10,y-63),(x+15,y-26),(x-14,y-26)])
            for dx in (-6,6):line(s,(45,52,56),(x+dx,y-29),(x+dx,y-4),6)
            line(s,(205,178,121),(x-14,y-53),(x+14,y-53),3)
            if not liberated:
                for n in range(3):pg.draw.ellipse(s,(184,151,79),pg.Rect(x-29-n*5,y-99-n*5,58+n*10,99+n*10),1)
            text(s,item['name'],(x,y-134),17,CYAN if liberated else GOLD,True,'center')
            text(s,'E · '+('Conversar' if liberated else 'Rescate opcional · explora este desvío'),(x,y-113),12,PAPER,False,'center')
    if world.rift_site:
        wx,y,destination=world.rift_site;x=wx-camera
        if -150<x<s.get_width()+150:
            for n in range(4):pg.draw.ellipse(s,(171,142+n*12,221),pg.Rect(x-25-n*8,y-118-n*3,50+n*16,110+n*6),2)
            text(s,'GRIETA AL PASADO · E',(x,y-150),13,GOLD,True,'center')

class ExpansionUI:
    def init_expansion(self):
        self.activity_index=0;self.activity_message='';self.reward_page=0;self.skin_selected='granadero'
        self.reward_return='menu';self.rift_return_memory=None

    def teacher_tools(self):
        if not self.save.data['practice']:self.set_state('menu');return
        s=self.canvas;s.fill((13,27,37));text(s,'Pruebas docentes · desplazamiento',(62,40),38,PAPER,True,serif=True)
        wrapped(s,'Todo está disponible para probar. Los desplazamientos y recompensas de esta sesión no modifican el progreso real ni el ranking.',(65,102),1120,21,GOLD)
        w=self.world
        targets=[('Inicio',w.data['spawn'][0]+14,w.data['spawn'][1]+64,False)]
        targets += [(f'Puesto de actividad {i+1}',x,y,False) for i,(x,y) in enumerate(w.mechanic.devices)]
        targets += [('Curiosidad',w.data['cultural_sites'][0][0],w.data['cultural_sites'][0][1],False)]
        if w.rescue_site:targets.append(('Rescate opcional',w.rescue_site[0],w.rescue_site[1],False))
        if w.rift_site:targets.append(('Grieta al pasado',w.rift_site[0],w.rift_site[1],False))
        if w.boss:targets.append(('Guardián · 3 fragmentos',w.boss.left+180,584,True))
        else:targets.append(('Portal · 3 fragmentos',w.data['portal'][0]-75,w.data['portal'][1],True))
        for i,(label,x,y,shards) in enumerate(targets):
            self.button(label,(65+i%2*585,206+i//2*94,555,78),lambda xx=x,yy=y,ss=shards:self.teacher_teleport(xx,yy,ss),small=True)
        self.button('Volver al mapa',(65,627,555,73),lambda:self.set_state('play'),True)
        self.button('Elegir otro mapa',(650,627,555,73),lambda:self.set_state('chapters'))
    def teacher_teleport(self,x,y,shards=False):
        if not self.save.data['practice']:return
        w=self.world;w.mechanic.state['vehicle']=False;w.player.rect.midbottom=(x,y);w.player.vx=w.player.vy=0
        if w.boss and x<w.boss.left+130:
            b=w.boss;b.active=False;b.phase='warning';b.timer=1.3;b.telegraphs=[]
            b.aim_warning=0;b.camp_time=0;b.camp_position=None;w.projectiles=[]
        w.player.hp=w.player.max_hp;w.player.invincible=2
        if shards:w.shards={0,1,2}
        self.camera=max(0,min(w.width-1280,x-480));self.set_state('play')

    def expansion_interact(self):
        w=self.world;p=w.player.rect
        if w.mechanic.dismount():return True
        if w.rescue_site:
            x,y,key,item=w.rescue_site
            if abs(p.centerx-x)<100 and abs(p.bottom-y)<110:
                remaining=sum(w.enemies[i].alive for i in w.rescue_guards)
                if remaining and key not in self.save.data['rescued_ids'] and not self.save.data['practice']:
                    w.say(f'Señal bloqueada: libera los {remaining} ecos cercanos y vuelve al desvío.');return True
                self.save.rescue(key,w);self.rescue_info=item;self.set_state('rescue_info');return True
        if w.rift_site:
            x,y,destination=w.rift_site
            if abs(p.centerx-x)<90 and abs(p.bottom-y)<110:
                self.enter_rift(destination);return True
        index=w.mechanic.near()
        if index is not None:
            self.activity_index=index;self.activity_message='';self.set_state('activity');return True
        return False

    def activity_answer(self,choice):
        m=self.world.mechanic;result=m.activate(self.activity_index,choice)
        if result=='ok':
            if m.kind in ('naval','canal','tide') and self.activity_index==1:
                self.start_voyage();return
            if m.completed:
                if not self.save.data['practice'] and self.world.level_id not in self.save.data['mechanics_completed']:
                    self.save.data['mechanics_completed'].append(self.world.level_id);self.save.data['coins']+=15
                self.save.refresh_achievements()
            self.save.capture(self.world);self.set_state('play')
        elif result=='revisit':
            if m.kind in ('naval','canal','tide') and self.activity_index==1:
                self.start_voyage();return
            if m.vehicle_kind and self.activity_index==1:
                m.state['vehicle']=True;m.state['vehicle_x']=m.devices[1][0];m.state['vehicle_y']=m.devices[1][1]-32
            self.set_state('play')
        else:self.activity_message=result

    def activity(self):
        if self.touch_enabled():return self.mobile_activity()
        s=self.canvas;self.artist.scene(s,self.world,self.camera,self.time);self.dim(235)
        m=self.world.mechanic
        tracked(s,'TRABAJO DE CAMPO · PUESTO '+str(self.activity_index+1)+' / 3',(65,38),13,CYAN,2)
        text(s,m.title,(62,82),41,PAPER,True,serif=True)
        wrapped(s,m.objective,(65,150),1110,24,GOLD,leading=34)
        wrapped(s,m.note,(65,231),1110,self.save.data['reading_size'],PAPER,leading=31)
        wrapped(s,m.field.description(),(65,310),1110,16,GOLD)
        maritime=m.kind in ('naval','canal','tide')
        resolved=self.activity_index in m.state['activated']
        if resolved:
            text(s,'Este puesto ya está resuelto.',(65,347),24,CYAN,True)
            wrapped(s,m.operations[self.activity_index],(65,401),1110,23,PAPER)
            if maritime and self.activity_index==1:
                label='Repetir travesía · sin otro premio' if m.state.get('sea_complete') else 'Retomar la travesía marítima'
                self.button(label,(65,480,1140,65),self.start_voyage,True,small=True)
        else:
            if maritime:
                from .sea_fieldwork import shore_question
                prompt,operations=shore_question(m.kind,self.activity_index)
            else:prompt,operations='Elige la operación que corresponde a este paso:',m.operations
            wrapped(s,prompt,(65,347),1120,22,CYAN,True,leading=26)
            for i,operation in enumerate(operations):
                self.button(operation,(65,415+i*62,1140,54),lambda n=i:self.activity_answer(n),small=True,wrap=True)
        wrapped(s,self.activity_message,(65,608),1100,17,GOLD)
        self.button('Volver a explorar',(65,655,320,48),lambda:self.set_state('play'),small=True)

    def rescue_info_screen(self):
        s=self.canvas;s.fill((15,30,41));item=self.rescue_info
        tracked(s,'UNA PERSONA ABRE OTRA HISTORIA',(65,45),13,CYAN,2)
        text(s,item['name'],(62,103),47,PAPER,True,serif=True)
        text(s,item['date'],(65,178),23,GOLD,True)
        wrapped(s,item['text'],(65,253),1110,self.save.data['reading_size']+2,PAPER,leading=35)
        from .education import STAGES
        wrapped(s,'Nuevo mapa bonus: '+STAGES[item['bonus']].name+'. Ya puedes elegirlo en Épocas.',(65,447),1110,25,CYAN,True)
        self.button('Seguir por mi ruta',(65,600,420,61),lambda:self.set_state('play'),True)

    def enter_rift(self,destination):
        self.save.capture(self.world)
        p=self.world.player
        self.rift_return_memory=dict(level=self.world.level_id,x=p.rect.x,y=p.rect.y,hp=p.hp)
        if not self.save.data['practice']:
            self.save.data['rift_return']=dict(self.rift_return_memory)
            self.save.data['active_rift']=destination;self.save.data['rift_finished']=False;self.save.write()
        self.load(*divmod(destination,3),restore=True)

    def return_from_rift(self):
        origin=self.rift_return_memory or self.save.data.get('rift_return')
        if not self.save.data['practice']:
            self.save.data['active_rift']=None;self.save.data['rift_return']=None;self.save.data['rift_finished']=False;self.save.write()
        self.rift_return_memory=None
        if not isinstance(origin,dict) or type(origin.get('level')) is not int or not 0<=origin['level']<TOTAL_LEVELS:
            self.set_state('chapters');return
        self.load(*divmod(origin['level'],3),restore=True)
        p=self.world.player
        x,y=origin.get('x'),origin.get('y')
        if type(x) in (float,int) and type(y) in (float,int) and 0<=x<=self.world.width and 0<=y<760:
            p.rect.topleft=(x,y)
        p.hp=min(p.max_hp,max(1,origin.get('hp',p.max_hp))) if type(origin.get('hp')) is int else p.max_hp
        p.invincible=2;self.set_state('play');self.camera=max(0,min(self.world.width-1280,p.rect.centerx-480))
        self.world.say('Has vuelto al punto de origen. La primera excursión completa entrega 40 ecos de memoria.')

    def open_rewards(self,state='achievements'):
        if self.state not in ('achievements','skins','skin_card'):self.reward_return=self.state
        self.reward_page=0;self.set_state(state)

    def achievements(self):
        from .achievement_catalog import CATALOG
        s=self.canvas;s.fill((13,27,37));owned=set(self.save.data['achievements'])
        if self.save.data['practice']:owned={item['id'] for item in CATALOG}
        text(s,f'Los logros del Cronista · {len(owned)} / 60',(62,44),38,PAPER,True,serif=True)
        wrapped(s,'Los 60 logros entregan el Reloj del Cronista: +1 energía y +60 px de atracción. Admiten cualquier edad y asistencia.',(65,103),1120,19,CYAN)
        if self.save.data['practice']:text(s,'PREVISUALIZACIÓN DOCENTE · los logros reales no se modifican',(65,153),14,GOLD,True)
        pages=10;self.reward_page=max(0,min(pages-1,self.reward_page))
        for n,item in enumerate(CATALOG[self.reward_page*6:self.reward_page*6+6]):
            x=65+n%2*585;y=185+n//2*123;unlocked=item['id'] in owned
            rect(s,(25,46,53),(x,y,557,107),6)
            diamond(s,(x+24,y+28),9,CYAN if unlocked else GOLD,unlocked)
            text(s,item['name'],(x+47,y+13),21,CYAN if unlocked else PAPER,True)
            wrapped(s,item['description'],(x+19,y+51),520,17,MUTED,leading=25)
        self.button('Volver',(65,620,200,53),lambda:self.set_state(self.reward_return),True,small=True)
        self.button('Anterior',(285,620,200,53),lambda:setattr(self,'reward_page',self.reward_page-1),enabled=self.reward_page>0,small=True)
        self.button('Siguiente',(505,620,200,53),lambda:setattr(self,'reward_page',self.reward_page+1),enabled=self.reward_page<9,small=True)
        self.button('Apariencias',(725,620,220,53),lambda:self.open_rewards('skins'),small=True)
        self.button('Reloj: '+('SÍ' if self.save.data['master_enabled'] else 'NO'),(965,620,245,53),self.toggle_master,enabled=len(owned)==60,small=True)

    def toggle_master(self):
        self.save.data['master_enabled']=not self.save.data['master_enabled'];self.save.write()
        self.world.upgrades=self.save.effective_upgrades();self.world.player.configure(self.world.upgrades)

    def skins(self):
        from .skins import SKINS,available,unlocked_for_purchase,SKIN_MAPS
        s=self.canvas;s.fill((13,27,37));text(s,'El guardarropa del tiempo',(62,40),41,PAPER,True,serif=True)
        text(s,f'{self.save.data["coins"]} ecos disponibles',(1210,96),24,GOLD,True,'topright')
        text(s,'Cada eco pequeño se guarda una sola vez. Explorar compra historia y nuevas apariencias.',(65,117),19,MUTED)
        self.button('Crono original',(65,171,270,48),lambda:self.equip_skin('crono'),small=True)
        self.skin_page=max(0,min((len(SKINS)-1)//8,self.skin_page))
        for n,item in enumerate(SKINS[self.skin_page*8:self.skin_page*8+8]):
            x=65+n%4*292;y=250+n//4*177
            rect(s,(25,44,53),(x,y,270,155),6)
            old=getattr(self.world.player,'skin','crono');self.world.player.skin=item['id']
            self.artist.player(s,self.world.player,0,self.time,1,(x+39,y+113));self.world.player.skin=old
            wrapped(s,item['name'],(x+83,y+15),173,19,PAPER,True,leading=25)
            label='Equipado' if self.save.data['skin']==item['id'] else 'Equipar' if available(self.save,item['id']) else '60 logros' if item['id']=='cronista' else 'Completa su mapa' if not unlocked_for_purchase(self.save,item['id']) else f'{item["cost"]} ecos'
            self.button(label,(x+82,y+83,171,50),lambda k=item['id']:self.skin_action(k),enabled=available(self.save,item['id']) or item['id']!='cronista' and unlocked_for_purchase(self.save,item['id']),small=True,arrow=False)
            self.button('Ficha',(x+10,y+118,65,30),lambda k=item['id']:self.open_skin_card(k),small=True,arrow=False)
        self.button('Volver',(65,638,240,50),lambda:self.set_state(self.reward_return),True,small=True)
        self.button('Logros',(330,638,240,50),lambda:self.open_rewards('achievements'),small=True)
        self.button('Anterior',(690,638,240,50),lambda:setattr(self,'skin_page',self.skin_page-1),enabled=self.skin_page>0,small=True)
        self.button('Siguiente',(950,638,260,50),lambda:setattr(self,'skin_page',self.skin_page+1),enabled=(self.skin_page+1)*8<len(SKINS),small=True)

    def equip_skin(self,key):
        self.save.data['skin']=key;self.world.player.skin=key;self.save.write()
    def skin_action(self,key):
        from .skins import available,buy_skin
        if available(self.save,key):self.equip_skin(key)
        elif buy_skin(self.save,key):self.open_skin_card(key)
    def open_skin_card(self,key):
        from .skins import available
        self.skin_selected=key
        if available(self.save,key) and not self.save.data['practice'] and key not in self.save.data['skin_cards_seen']:
            self.save.data['skin_cards_seen'].append(key);self.save.refresh_achievements();self.save.write()
        self.set_state('skin_card')
    def skin_card(self):
        from .skins import SKINS
        import webbrowser
        item=next(s for s in SKINS if s['id']==self.skin_selected)
        s=self.canvas;s.fill((13,27,37));tracked(s,'VESTIR UNA HISTORIA',(65,40),14,CYAN,3)
        text(s,item['name'],(62,99),43,PAPER,True,serif=True)
        old=getattr(self.world.player,'skin','crono');self.world.player.skin=item['id']
        self.artist.player(s,self.world.player,0,self.time,3,(230,466));self.world.player.skin=old
        wrapped(s,item['history'],(430,220),760,self.save.data['reading_size']+2,PAPER,leading=35)
        from .skins import SKIN_MAPS,unlocked_for_purchase
        if item['id'] in SKIN_MAPS:
            from .education import STAGES
            wrapped(s,'Se habilita al completar: '+STAGES[SKIN_MAPS[item['id']]].name,(430,155),760,18,CYAN)
        if item['url']:self.button('Fuente de la ficha',(430,533,430,54),lambda:webbrowser.open(item['url']),small=True)
        self.button('Volver al guardarropa',(65,635,420,53),lambda:self.set_state('skins'),True)
