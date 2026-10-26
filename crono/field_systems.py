"""Physical applications of the field devices, beyond answering their panels."""
import math
import pygame as pg
from .art import rect,line,circle,diamond,polygon,text,PAPER,CYAN,GOLD,MUTED

PICKUPS={
 'excavate':('Muestra estratificada','Registrar restos sin perder su contexto'),
 'assembly':('Propuesta ciudadana','Escuchar propuestas y reconocer a quienes no participaban'),
 'trade':('Pesa de mercado','Contrastar tres pesas antes de acordar el intercambio'),
 'courier':('Carta protegida','Recuperar cartas y llevarlas al siguiente refugio'),
 'documents':('Comunicación fechada','Reunir comunicaciones antes de preparar la posta'),
 'plaza':('Noticia bajo cubierta','Buscar documentos protegidos de la lluvia'),
 'provisions':('Carga de provisiones','Reunir víveres en las postas de altura'),
 'radio':('Componente de radio','Recuperar antena, batería y receptor'),
 'lunar':('Muestra lunar','Recoger muestras con poca gravedad'),
 'telescope':('Registro de observación','Comparar registros desde distintas alturas'),
}
LIFTS={'crane','wheel','steam','counterweight','lever'}
LIGHTS={'reveal','beam','glyph','circuit','energy','packet','beacon','broadcast'}
ESCORTS={'ballot','escort','siren'}
HAZARDS={'shelter','ash'}
PICKUPS.update(supply=('Carga de abastecimiento','Reúne las cargas y entrégalas al campamento'),
               catalogue=('Ficha de catálogo','Recupera las fichas y ordénalas en el escritorio inicial'),
               printing=('Caja de tipos','Recoge las letras y prepara una página en la prensa'),
               manuscripts=('Manuscrito protegido','Recupera los documentos y acompaña a su guardiana'))

PICKUPS.update(moonrepair=('Pieza del módulo','Recupera las tres piezas y repara la nave con ↓'),dialogue=('Documento de perspectiva','Reúne las fuentes y contrástalas en la mesa final'))

class FieldSystem:
    def __init__(self,m):
        self.m=m;self.world=m.world;self.kind=m.kind
        self.collected=set();self.marks=[];self.clock=0.;self.distance=0.;self.goal=0.;self.started=False
        self.lifts=[];self.beams=[];self.sheltered_time=0.;self.crossed=set()
        floors=[p for p in self.world.platforms if not p.moving and p.rect.w>=180 and (self.kind!='chain' or not p.oneway)]
        self.points=[]
        for fraction in (.26,.57,.85):
            candidates=[p for p in floors if .15*self.world.width<p.rect.centerx<.92*self.world.width]
            platform=min(candidates,key=lambda p:abs(p.rect.centerx-self.world.width*fraction))
            self.points.append((platform.rect.centerx,platform.rect.top-40))
        if self.kind=='moonrepair':self.points=list(self.world.data['repair_parts'])
        if self.kind in LIFTS:
            from .physics import Platform
            for x,y in m.devices:
                p=Platform(dict(x=x+85,y=y-108,w=110,h=16,moving=True,oneway=True,axis='y',amplitude=90,speed=.85))
                p.active=False;self.world.platforms.append(p);self.lifts.append(p)
        if self.kind in LIGHTS or self.kind=='bridge':
            from .physics import Platform
            for x,y in self.points:
                top=y-88;width=145 if self.kind in LIGHTS else 220
                # Put the reward ledge above nearby geometry, never inside it.
                nearby=[floor.rect.top for floor in self.world.platforms if floor.rect.left<x+width*.5 and floor.rect.right>x-width*.5 and abs(floor.rect.top-top)<35]
                if nearby:top=min(nearby)-58
                p=Platform(dict(x=x-70,y=top,w=width,h=14,moving=False,oneway=True))
                p.active=False;self.world.platforms.append(p);self.lifts.append(p)
        self.escort_x=m.devices[0][0];self.escort_y=m.devices[0][1]

    def restore(self,state):
        self.collected={i for i in state.get('field_collected',[]) if type(i) is int and 0<=i<3} if isinstance(state.get('field_collected',[]),list) else set()
        self.crossed={i for i in state.get('field_crossed',[]) if type(i) is int and 0<=i<3} if isinstance(state.get('field_crossed',[]),list) else set()
        for name in ('distance','goal','sheltered_time'):
            value=state.get('field_'+name,0.)
            if type(value) in (int,float) and math.isfinite(value):setattr(self,name,max(0,min(1e6,value)))
        value=state.get('field_escort_x',self.escort_x)
        if type(value) in (int,float) and math.isfinite(value):self.escort_x=max(0,min(self.world.width,value))

    def persist(self):
        self.m.state.update(field_collected=sorted(self.collected),field_crossed=sorted(self.crossed),field_distance=self.distance,
            field_goal=self.goal,field_sheltered_time=self.sheltered_time,field_escort_x=self.escort_x)

    @property
    def done(self):
        if self.kind in ('supply','catalogue','printing','dialogue','moonrepair'):return len(self.collected)==3 and self.goal>=1
        if self.kind=='manuscripts':return len(self.collected)==3 and self.escort_x>=self.m.devices[2][0]-100
        if self.kind=='cipher':return len(self.crossed)==3
        if self.kind in ('naval','canal','tide'):return self.m.state.get('sea_complete',False)
        if self.kind in PICKUPS:return len(self.collected)==3
        if self.kind in LIFTS:return len(self.crossed)>=2
        if self.kind in LIGHTS or self.kind in ('bridge','chain'):return len(self.crossed)>=2
        if self.kind in ESCORTS:return self.escort_x>=self.m.devices[2][0]-100
        if self.kind in HAZARDS:return self.sheltered_time>=3 and len(self.crossed)>=2
        if self.kind in ('train','rail'):return len(self.crossed)>=3
        if self.kind=='race':return len(self.crossed)>=3
        if self.kind in ('warmth','wind'):return len(self.crossed)>=3
        return self.m.state['step']>=3

    def update(self,dt,controls):
        events=[]
        w=self.world;m=self.m;p=w.player;step=m.state['step'];self.clock+=dt
        if not step:return events
        self.started=True
        for i,lift in enumerate(self.lifts):
            lift.active=step>i
            if lift.active and p.support is lift:self.crossed.add(i)
        if self.kind in PICKUPS:
            pickup_area=p.rect.inflate(32,32)
            for i,point in enumerate(self.points):
                if i not in self.collected and pickup_area.collidepoint(point):
                    self.collected.add(i);w.say(PICKUPS[self.kind][0]+f' · {len(self.collected)} / 3')
            if self.kind=='trade' and len(self.collected)<3:m.speed=.93
            if self.kind=='provisions':
                m.wind=-35 if w.difficulty==0 else -65; m.speed=.92 if len(self.collected)<2 else 1.
            if self.kind=='telescope' and controls.drop and p.grounded:p.cooldown=max(0,p.cooldown-dt*.5)
        if self.kind in ('supply','catalogue','printing','dialogue','moonrepair') and len(self.collected)==3:
            target=w.data['repair_ship'] if self.kind=='moonrepair' else m.devices[0 if self.kind=='catalogue' else 2]
            if abs(p.rect.centerx-target[0])<95 and abs(p.rect.bottom-target[1])<80 and controls.drop and p.grounded:
                self.sheltered_time+=dt
                if self.sheltered_time>=(3 if self.kind=='moonrepair' else 1.5) and not self.goal:self.goal=1;w.say('Trabajo registrado y entrega completada.');events.append('checkpoint')
        if self.kind=='cipher':
            for i,(x,y) in enumerate(self.points):
                if i not in self.crossed and abs(p.rect.centerx-x)<90 and abs(p.rect.bottom-y-40)<80 and controls.drop and p.grounded and (self.clock+i)%3<1.2:
                    self.crossed.add(i);w.say(f'Señal {i+1} contrastada.');events.append('checkpoint')
        if self.kind in ('naval','train','rail','canal','tide') and m.state['vehicle']:
            self.distance+=abs(p.vx)*dt
            if self.kind=='train' and controls.axis<0:p.vx*=.65
        if self.kind in ('race','wind','warmth','train','rail'):
            for i,(x,y) in enumerate(self.points):
                if abs(p.rect.centerx-x)<100 and abs(p.rect.bottom-(y+40))<150:self.crossed.add(i)
            if self.kind=='race' and len(self.crossed)==3:self.goal=1
            if self.kind=='wind':m.wind=math.sin(w.time*.8)*75
        if self.kind in ESCORTS or self.kind=='manuscripts' and len(self.collected)==3:
            self.escort_y=self.m.devices[0][1]
            threats=[e for e in w.enemies if e.alive and abs(e.rect.centerx-self.escort_x)<160]
            if not threats and 30<p.rect.centerx-self.escort_x<360:
                self.escort_x=min(m.devices[2][0],self.escort_x+135*dt)
            floor=next((f for f in w.platforms if not f.oneway and f.rect.left<=self.escort_x<=f.rect.right),None)
            if floor:self.escort_y=floor.rect.top
            # Civilian follows an abstract safe route across gaps, never a target.
            if p.rect.centerx-self.escort_x>800:w.say('Tu acompañante espera: vuelve y despeja los ecos cercanos.') if int(w.time*120)%600==0 else None
        if self.kind in HAZARDS:
            if m.sheltered:self.sheltered_time+=dt
            for i,(x,y) in enumerate(m.devices):
                if abs(p.rect.centerx-x)<110:self.crossed.add(i)
            if int(self.clock/4)!=int((self.clock-dt)/4) and abs(p.rect.centerx-m.devices[min(step-1,2)][0])<650:
                self.marks.append([p.rect.centerx,p.rect.bottom,1.2])
            for mark in self.marks:
                mark[2]-=dt
                if mark[2]<=0 and not m.sheltered and abs(p.rect.centerx-mark[0])<38:
                    events.extend(w.damage(mark[0]))
            self.marks=[mark for mark in self.marks if mark[2]>0]
        if self.kind=='chain':
            near=next((i for i,(x,y) in enumerate(self.points[:2]) if abs(p.rect.centerx-x)<90 and abs(p.rect.bottom-y-40)<55),None)
            if near is not None and controls.drop and p.grounded and near not in self.crossed:
                self.sheltered_time+=dt
                if self.sheltered_time>=1.5:self.crossed.add(near);self.sheltered_time=0;w.say('Batería coordinada: cadena y defensa ribereña preparadas.');events.append('checkpoint')
        self.persist()
        return events

    def description(self):
        if self.kind in ('supply','catalogue','printing','dialogue','moonrepair'):
            place='la nave de Crono' if self.kind=='moonrepair' else 'el escritorio inicial' if self.kind=='catalogue' else 'el último puesto'
            return f'Recupera 3 elementos ({len(self.collected)}/3) y mantén ↓ en {place} · '+('HECHO' if self.goal else 'pendiente')
        if self.kind=='manuscripts':return f'Manuscritos {len(self.collected)}/3; después acompaña a la guardiana al depósito.'
        if self.kind=='cipher':return f'Mantén ↓ junto a cada señal cuando esté iluminada · {len(self.crossed)}/3'
        if self.kind=='chain':return f'En las dos baterías señaladas, mantén ↓ para coordinar la defensa · {len(self.crossed)}/2'
        if self.kind in ('naval','canal','tide'):return 'Travesía marítima completada' if self.done else 'Entra en la grieta del segundo puesto y completa el convoy marítimo.'
        if self.kind in PICKUPS:return PICKUPS[self.kind][1]+f' · {len(self.collected)}/3'
        if self.kind in LIFTS:return f'Usa dos elevadores activados · {len(self.crossed)}/2'
        if self.kind in LIGHTS or self.kind in ('bridge','chain'):return f'Recorre dos pasarelas restauradas · {len(self.crossed)}/2'
        if self.kind in ESCORTS:return 'Acompaña a tu aliado hasta el tercer puesto; despeja su camino.'
        if self.kind in HAZARDS:return f'Cruza dos refugios y espera a salvo tres segundos · {min(3,self.sheltered_time):.1f}/3 s'
        if self.kind in ('train','rail'):return f'Comprueba las tres señales de la ruta ferroviaria · {len(self.crossed)}/3'
        return f'Alcanza las tres balizas de la ruta · {len(self.crossed)}/3'

    def draw(self,s,camera,t):
        if self.m.state['step']==0:return
        for i,(wx,y) in enumerate(self.points):
            x=wx-camera
            if not -100<x<s.get_width()+100:continue
            if self.kind=='cipher':
                active=i in self.crossed or (self.clock+i)%3<1.2
                rect(s,(28,43,53),(x-28,y-39,56,68),5)
                for n in range(3):circle(s,CYAN if active else (105,109,102),(x-15+n*15,y-14),5)
                text(s,'↓ · SEÑAL '+str(i+1),(x,y-62),12,CYAN if active else GOLD,True,'center')
            if self.kind=='chain' and i<2:
                rect(s,(111,92,68),(x-19,y+12,38,25),4)
                circle(s,CYAN if i in self.crossed else GOLD,(x,y-1),16,3)
                for n in range(12):
                    px=x+28+n*13;py=y-3+math.sin(n/11*math.pi)*(7 if i in self.crossed else 25)
                    pg.draw.ellipse(s,(181,173,142),pg.Rect(px,py,18,9),2)
                text(s,'↓ COORDINAR BATERÍA',(x,y-41),12,GOLD,True,'center')
            if self.kind in PICKUPS and i not in self.collected:
                color=GOLD if self.kind not in ('lunar','radio') else CYAN
                if self.kind=='moonrepair':
                    from .moon_art import component
                    s.blit(component(i),(int(x-23),int(y-25)))
                elif self.kind in ('supply','printing'):
                    from .naval_art import cargo_image
                    s.blit(cargo_image(40),(int(x-20),int(y-20)))
                else:circle(s,(19,39,48),(x,y),18);diamond(s,(x,y+math.sin(t*2+i)*3),11,color)
                text(s,('OXÍGENO','BATERÍA','PROPULSOR')[i] if self.kind=='moonrepair' else PICKUPS[self.kind][0],(x,y-36),11,color,True,'center')
            elif self.kind in ('race','wind','warmth','train','rail'):
                line(s,(156,144,111),(x,y+40),(x,y-70),3)
                polygon(s,CYAN if i in self.crossed else GOLD,[(x,y-69),(x+52,y-53),(x,y-40)])
        if self.kind in ESCORTS or self.kind=='manuscripts':
            x=self.escort_x-camera;y=self.escort_y
            if -100<x<s.get_width()+100:
                if self.kind=='ballot':rect(s,(177,142,84),(x-18,y-49,36,28),3);line(s,(55,61,62),(x-9,y-45),(x+9,y-45),2)
                else:
                    line(s,(144,152,134),(x-37,y-18),(x+38,y-18),5);rect(s,(119,142,134),(x-30,y-36,60,17),3)
                    circle(s,(203,164,126),(x+24,y-42),8)
                for dx in (-29,29):circle(s,(44,55,61),(x+dx,y-10),7)
                text(s,'CUIDAR Y ACOMPAÑAR',(x,y-79),11,CYAN,True,'center')
        for x,y,remaining in self.marks:
            x-=camera;circle(s,GOLD,(x,y-8),36,2);text(s,'CENIZA' if self.kind=='ash' else 'IMPACTO',(x,y-55),12,GOLD,True,'center')
            line(s,(219,140,83),(x+40,y-260),(x,y-30),2)
