"""Educational overlays, age selection, workshop and an illustrated field guide."""
import random
import webbrowser
from .education import AGE_BANDS, LESSONS, SOURCES, STAGES, UPGRADES, fact_for
from .art import text, tracked, rect, line, circle, diamond, clock_icon, PAPER, MUTED, CYAN, GOLD, INK, W, H
from .combat import ENEMY_NAMES, ENEMY_HINTS, BOSS_NAMES, BOSS_HINTS, Enemy


def wrap_rows(value,width,size=18,bold=False):
    from .art import font
    words=[]
    for word in value.split():
        while font(size,bold).size(word)[0]>width:
            cut=1
            while cut<len(word) and font(size,bold).size(word[:cut+1])[0]<=width:
                cut+=1
            words.append(word[:cut])
            word=word[cut:]
        if word:
            words.append(word)
    rows=[]
    row=''
    for word in words:
        test=(row+' '+word).strip()
        if row and font(size,bold).size(test)[0]>width:
            rows.append(row)
            row=word
        else:
            row=test
    if row:
        rows.append(row)
    return rows


def wrapped(surface,value,pos,width,size=18,color=PAPER,bold=False,leading=None):
    x,y=pos
    leading=leading or size+9
    for row in wrap_rows(value,width,size,bold):
        text(surface,row,(x,y),size,color,bold)
        y+=leading
    return y


class LearningUI:
    def init_learning(self):
        self.panel_return='menu'
        self.quiz_return='play'
        self.quiz_topic=0
        self.quiz_mode='read'
        self.question=None
        self.question_history={}
        self.quiz_reward=False
        self.notebook_page=0
        self.heritage_key='wing'
        self.heritage_scroll=0;self.heritage_height=0
        self.chapter_era=0
        self.quiz_scroll=0
        self.quiz_feedback_scroll=0
        self.quiz_fact_height=0
        self.quiz_feedback_height=0
        self.quiz_fact_view_height=205

    def set_age(self,band):
        self.save.data['age_band']=band
        self.world.set_difficulty(self.save.combat_band())
        self.save.write()

    def age_switch(self,x,y,width=350):
        tracked(self.canvas,'EDAD · PREGUNTAS, COMBATE Y ANCLAS',(x,y-22),10,MUTED,2)
        for band,label in enumerate(('6–9 años','10–14 años','15+ años')):
            self.button(label,(x+band*(width+9)/3,y,(width-18)/3,34),lambda n=band:self.set_age(n),
                        primary=band==self.save.data['age_band'],small=True,arrow=False)

    def open_panel(self,name):
        if self.state not in ('workshop','notebook','bestiary','heritage'):
            self.panel_return=self.state
        self.set_state(name)

    def close_panel(self):
        self.set_state(self.panel_return)

    def open_curiosities(self):
        from .curiosities import MAP_CURIOSITIES
        self.heritage_key=MAP_CURIOSITIES[self.world.level_id]
        self.heritage_scroll=0
        self.open_panel('heritage')

    def interact(self):
        if self.expansion_interact():return
        from .heritage import near_site
        site=near_site(self.world)
        if site:
            self.heritage_key=site[2]
            self.heritage_scroll=0
            self.save.visit_curiosity(site[2],self.world)
            self.open_panel('heritage')
            return
        station=self.world.near_station()
        if station:
            self.open_lesson(station[2])
        else:
            self.world.say('Acércate a un archivo luminoso y pulsa E. U abre las mejoras; C, el cuaderno.')

    def open_lesson(self,topic):
        self.quiz_return=self.state if self.state in ('play','notebook') else 'play'
        self.save.discover(topic)
        self.quiz_topic=topic
        band=self.save.data['age_band']
        key=(topic,band)
        self.question=self.learning_bank().choose(topic,band,random,self.question_history.get(key))
        self.question_history[key]=self.question.id
        self.quiz_mode='read'
        self.quiz_reward=False
        self.quiz_scroll=self.quiz_feedback_scroll=0
        self.set_state('quiz')

    def answer_question(self,choice):
        if self.quiz_mode!='question':
            return
        first=not any(a.get('question')==self.question.id and a.get('practice',False)==self.save.data['practice'] for a in self.save.data['attempts'])
        self.save.record_attempt(self.question,choice,first)
        if choice==self.question.correct:
            self.quiz_reward=self.save.answer(self.quiz_topic)
            self.world.answered.add(self.quiz_topic)
            self.quiz_mode='correct'
            self.audio.play('shard')
        else:
            self.quiz_mode='wrong'
            self.audio.play('ui')
        self.selection=0
        self.buttons=[]
        self.quiz_feedback_scroll=0

    def learning_scroll(self,event):
        import pygame as pg
        if self.state=='heritage':
            if event.type==pg.MOUSEWHEEL:delta=-event.y*45
            elif event.type==pg.KEYDOWN and event.key in (pg.K_PAGEUP,pg.K_PAGEDOWN):delta=140 if event.key==pg.K_PAGEDOWN else -140
            else:return False
            self.heritage_scroll=max(0,min(max(0,self.heritage_height-295),self.heritage_scroll+delta));return True
        if self.state!='quiz':
            return False
        if event.type==pg.KEYDOWN and event.key==pg.K_TAB:
            self.reading_pane='feedback' if self.reading_pane=='fact' else 'fact';return True
        if event.type==pg.MOUSEWHEEL:
            delta=-event.y*40;left=self.mouse[0]<520
        elif event.type==pg.KEYDOWN and event.key in (pg.K_PAGEUP,pg.K_PAGEDOWN):
            delta=140 if event.key==pg.K_PAGEDOWN else -140;left=self.reading_pane=='fact'
        else:return False
        if left:
            self.quiz_scroll=max(0,min(max(0,self.quiz_fact_height-self.quiz_fact_view_height),self.quiz_scroll+delta))
        else:
            self.quiz_feedback_scroll=max(0,min(max(0,self.quiz_feedback_height-265),self.quiz_feedback_scroll+delta))
        return True

    def close_quiz(self):
        if self.quiz_return=='play':
            self.save.capture(self.world)
        self.set_state(self.quiz_return)

    def educational_background(self):
        if self.panel_return=='menu':
            self.artist.background(self.canvas,0,0,self.time)
        else:
            self.artist.scene(self.canvas,self.world,self.camera,self.time)
        self.dim(235)

    def quiz(self):
        s=self.canvas
        self.artist.scene(s,self.world,self.camera,self.time)
        self.dim(220)
        lesson=LESSONS[self.quiz_topic]
        fact=self.question.explanation or fact_for(self.quiz_topic,self.save.data['age_band'])
        stage=STAGES[self.quiz_topic//2]
        tracked(s,'ARCHIVO DE CAMPO',(65,43),12,CYAN,3)
        text(s,stage.name,(65,73),32,PAPER,True,serif=True)
        text(s,f'{AGE_BANDS[self.save.data["age_band"]]}  ·  Banco de {len(self.bank.records)} preguntas',(1210,53),13,MUTED,False,'topright')
        rect(s,(22,39,48),(65,139,439,469),8)
        clock_icon(s,106,182,19,CYAN,self.time*.2)
        wrapped(s,lesson.title,(88,225),391,26,PAPER,True)
        import pygame as pg
        image_question=getattr(self.question,'kind','choice')=='image'
        if image_question:
            from .heritage import illustration
            from .curiosities import MAP_CURIOSITIES
            rect(s,(22,39,48),(79,155,412,233),6)
            s.blit(pg.transform.smoothscale(illustration(MAP_CURIOSITIES[self.quiz_topic//2]),(215,209)),(176,164))
        top=391 if image_question else 312
        self.quiz_fact_view_height=122 if image_question else 205
        old_clip=s.get_clip()
        s.set_clip(pg.Rect(87,top-6,394,self.quiz_fact_view_height+2))
        self.quiz_fact_height=wrapped(s,fact,(88,top-self.quiz_scroll),391,self.save.data['reading_size'],PAPER,leading=self.save.data['reading_size']+11)-(top-self.quiz_scroll)
        s.set_clip(old_clip)
        if self.quiz_fact_height>self.quiz_fact_view_height:
            text(s,'Rueda / RePág–AvPág / deslizar: leer',(88,517),10,CYAN)
        source=self.question.source
        source=next((label for label,url in SOURCES if url==source),source or 'Material del docente')
        wrapped(s,'Fuente: '+(source[:137]+'…' if len(source)>140 else source),(88,539),390,12,MUTED,leading=18)
        if self.quiz_mode=='read':
            text(s,'Observa. Aprende. Ponlo a prueba.',(550,170),27,PAPER,True,serif=True)
            wrapped(s,'Este archivo guarda una pista sobre el lugar que estás recorriendo. Léela y responde una pregunta elegida al azar.',(550,231),632,20,MUTED,leading=33)
            wrapped(s,'Cada archivo resuelto por primera vez otorga 2 puntos de conocimiento. Puedes gastarlos en mejoras permanentes para Crono.',(550,365),632,19,CYAN,leading=31)
            if self.world.stage==2:
                wrapped(s,'Comprender un archivo de este mapa prolonga la exposición del núcleo del jefe.',(550,475),632,16,GOLD)
            self.button('Ponerme a prueba',(550,550,636,57),lambda:setattr(self,'quiz_mode','question'),True)
        elif self.quiz_mode=='question':
            size=26
            while size>16 and len(wrap_rows(self.question.prompt,632,size,True))*(size+8)>130:
                size-=1
            y=wrapped(s,self.question.prompt,(550,166),632,size,PAPER,True,leading=size+8)
            y=max(y+22,286)
            for i,option in enumerate(self.question.options):
                self.button(f'{i+1}. {option}',(550,y+i*101,636,90),lambda n=i:self.answer_question(n),small=True,arrow=False,wrap=True)
        else:
            correct=self.quiz_mode=='correct'
            text(s,'¡Conocimiento recuperado!' if correct else 'Una pista para volver a pensar',(550,169),28,CYAN if correct else GOLD,True,serif=True)
            old_clip=s.get_clip()
            s.set_clip(pg.Rect(549,229,639,267))
            top=232-self.quiz_feedback_scroll
            y=wrapped(s,'Respuesta: '+self.question.options[self.question.correct],(550,top),630,21,PAPER,True,leading=31)
            y=wrapped(s,fact,(550,y+21),630,self.save.data['reading_size'],MUTED,leading=self.save.data['reading_size']+11)
            self.quiz_feedback_height=y-top
            s.set_clip(old_clip)
            if self.quiz_feedback_height>265:
                text(s,'Rueda del ratón: desplazar respuesta y explicación',(550,494),10,CYAN)
            if correct:
                wrapped(s,'+2 puntos de conocimiento' if self.quiz_reward else 'Archivo ya resuelto: este repaso no vuelve a dar puntos.',(550,515),630,16,CYAN)
                self.button('Seguir explorando',(550,550,399,56),self.close_quiz,True)
                self.button('Mejoras',(965,550,221,56),lambda:(self.close_quiz(),self.open_panel('workshop')),small=True)
            else:
                wrapped(s,'Equivocarse no quita energía ni puntos. Puedes volver a intentarlo.',(550,515),630,15,GOLD)
                self.button('Intentar otra vez',(550,550,636,56),lambda:setattr(self,'quiz_mode','question'),True)
        self.button('Volver sin responder',(65,642,303,45),self.close_quiz,small=True)
        if self.quiz_mode=='correct':self.button('Explicar mi respuesta',(390,642,285,45),self.open_reflection,small=True)
        text(s,'El juego permanece en pausa mientras aprendes.',(1210,663),13,MUTED,False,'midright')

    def purchase(self,upgrade_id):
        if self.save.buy(upgrade_id):
            p=self.world.player
            previous=p.max_hp
            self.world.upgrades=set(self.save.data['upgrades'])
            p.configure(self.world.upgrades)
            if p.max_hp>previous:
                p.hp+=p.max_hp-previous
            if upgrade_id=='shield':
                p.shield=1
            self.audio.play('checkpoint')

    def workshop(self):
        s=self.canvas
        self.educational_background()
        tracked(s,'APRENDER TE HACE MÁS FUERTE',(65,34),12,CYAN,3)
        text(s,'El taller de Crono',(62,68),41,PAPER,True,serif=True)
        text(s,f'{self.save.data["knowledge"]} puntos disponibles',(1208,84),24,GOLD,True,'topright')
        text(s,'Resuelve archivos por primera vez para obtener puntos. Las mejoras se conservan entre mapas y al morir.',(65,130),15,MUTED)
        owned=self.save.data['upgrades']
        self.workshop_page=max(0,min((len(UPGRADES)-1)//8,self.workshop_page))
        for n,item in enumerate(UPGRADES[self.workshop_page*8:self.workshop_page*8+8]):
            x=65+(n%2)*585
            y=175+(n//2)*105
            rect(s,(22,38,48),(x,y,558,93),6)
            text(s,item['name'],(x+18,y+12),20,PAPER,True)
            wrapped(s,item['description'],(x+18,y+46),382,13,MUTED,leading=20)
            purchased=item['id'] in owned
            available=not purchased and self.save.data['knowledge']>=item['cost'] and (not item['requires'] or item['requires'] in owned)
            label='Instalada' if purchased else f'{item["cost"]} puntos'
            self.button(label,(x+419,y+21,121,49),lambda key=item['id']:self.purchase(key),
                        primary=available,enabled=available,small=True,arrow=False)
            if item['requires'] and item['requires'] not in owned:
                requirement=next(u['name'] for u in UPGRADES if u['id']==item['requires'])
                text(s,'Requiere '+requirement,(x+18,y+73),10,GOLD)
        self.button('Volver al viaje',(65,630,270,49),self.close_panel,True,small=True)
        self.button('Cuaderno',(353,630,205,49),lambda:self.open_panel('notebook'),small=True)
        self.button('Anterior',(590,630,180,49),lambda:setattr(self,'workshop_page',self.workshop_page-1),enabled=self.workshop_page>0,small=True)
        self.button('Siguiente',(790,630,180,49),lambda:setattr(self,'workshop_page',self.workshop_page+1),enabled=(self.workshop_page+1)*8<len(UPGRADES),small=True)
        text(s,f'{len(owned)} / {len(UPGRADES)} habilidades',(1208,654),15,CYAN,False,'midright')

    def notebook(self):
        s=self.canvas
        self.educational_background()
        tracked(s,'LA MEMORIA DEL VIAJERO',(65,32),12,CYAN,3)
        text(s,'Cuaderno de campo',(62,65),41,PAPER,True,serif=True)
        text(s,f'{len(self.save.data["solved"])} / {len(LESSONS)} archivos resueltos',(1208,83),20,CYAN,True,'topright')
        text(s,'La historia real se consulta aquí. Los enemigos y guardianes son ecos de ficción del reloj roto.',(65,125),15,MUTED)
        discovered=sorted(self.save.data['discovered'])
        pages=max(1,(len(discovered)+3)//4)
        self.notebook_page=max(0,min(pages-1,self.notebook_page))
        if not discovered:
            text(s,'Tu primera página te espera junto a un archivo luminoso.',(640,350),25,PAPER,False,'center',True)
            text(s,'Durante la partida, acércate y pulsa E para descubrirlo.',(640,398),18,MUTED,False,'center')
        for n,topic in enumerate(discovered[self.notebook_page*4:self.notebook_page*4+4]):
            lesson=LESSONS[topic]
            x,y=65+n%2*585,164+n//2*217
            rect(s,(21,37,47),(x,y,558,200),6)
            text(s,STAGES[topic//2].name,(x+17,y+13),12,GOLD)
            text(s,lesson.title,(x+17,y+36),21,PAPER,True)
            wrapped(s,fact_for(topic,self.save.data['age_band']),(x+17,y+73),524,14,MUTED,leading=22)
            self.button('Repasar',(x+17,y+151,150,36),lambda key=topic:self.open_lesson(key),small=True)
            self.button('Fuente',(x+179,y+151,125,36),lambda src=lesson.source:webbrowser.open(SOURCES[src][1]),small=True)
            text(s,'RESUELTO' if topic in self.save.data['solved'] else 'POR RESOLVER',(x+534,y+168),11,CYAN,True,'midright')
        self.button('Volver',(65,628,171,48),self.close_panel,True,small=True)
        self.button('Mejoras',(250,628,190,48),lambda:self.open_panel('workshop'),small=True)
        self.button('Ecos y guardianes',(454,628,230,48),lambda:self.open_panel('bestiary'),small=True)
        self.button('Curiosidades',(698,628,155,48),self.open_curiosities,small=True,arrow=False)
        self.button('Anterior',(867,628,157,48),lambda:setattr(self,'notebook_page',self.notebook_page-1),enabled=self.notebook_page>0,small=True)
        self.button('Siguiente',(1039,628,177,48),lambda:setattr(self,'notebook_page',self.notebook_page+1),enabled=self.notebook_page<pages-1,small=True)
        text(s,f'Página {self.notebook_page+1} / {pages}',(1210,698),12,MUTED,False,'bottomright')

    def bestiary(self):
        s=self.canvas
        self.educational_background()
        tracked(s,'GUÍA DE LOS ECOS · FICCIÓN',(65,32),12,CYAN,3)
        text(s,'Reconoce antes de atacar',(62,65),40,PAPER,True,serif=True)
        era=self.world.combat_era
        stage=self.world.stage
        entries=[(kind,ENEMY_NAMES[kind],ENEMY_HINTS[kind],'royalist') for kind in ENEMY_NAMES]
        from .humanoid_roster import ROLES
        entries=[(kind,ROLES.get(era,{}).get(kind,label),hint,faction) for kind,label,hint,faction in entries]
        if era==7 and stage<2:
            from .argentina_history import ROLE_NAMES
            entries=[(kind,ROLE_NAMES[kind],ENEMY_HINTS[kind],'royalist') for kind in ('walker','hopper','sentry','charger','armored')]
        elif era==7:
            entries=[('walker','Patrulla militar','Eco de fuerzas de represión estatal. Patrulla el suelo.','state_force'),
                     ('sentry','Tirador militar','Eco del pasado. Avisa antes de disparar.','state_force'),
                     ('armored','Guardia militar','Escudo y protección. Evita saltar sobre él.','state_force'),
                     ('walker','Célula terrorista','Eco de terrorismo de organizaciones armadas.','armed_cell'),
                     ('hopper','Armado clandestino','Se desplaza y salta al acercarte.','armed_cell'),
                     ('sentry','Tirador clandestino','Figura armada ficticia. Dispara a distancia.','armed_cell')]
        for n,(kind,label,hint,faction) in enumerate(entries):
            x,y=65+n%3*390,146+n//3*155
            rect(s,(22,38,48),(x,y,365,135),6)
            e=Enemy(dict(x=x+25,y=y+58,left=0,right=2000,kind=kind,stage=stage,faction=faction),era)
            if kind=='flyer':
                e.rect.y+=100
            self.artist.enemy(s,e,0,self.time,self.world.index,stage)
            text(s,label,(x+95,y+23),19,PAPER,True)
            wrapped(s,hint,(x+95,y+61),245,14,MUTED,leading=22)
        from .campaign import ERA_LABELS
        era=self.world.combat_era
        from .enemy_art import FAMILY_NAMES
        text(s,FAMILY_NAMES[era],(65,466),22,CYAN,True)
        if era==7:
            from .argentina_history import CONTEXT
            wrapped(s,CONTEXT[stage],(65,506),1120,15,MUTED,leading=23)
            text(s,BOSS_NAMES[era],(65,568),21,GOLD,True)
            text(s,'Las figuras y el blindado son ficción del viaje temporal; la recuperación democrática se explica en los archivos.',(65,606),14,MUTED)
        else:
            text(s,BOSS_NAMES[era],(65,511),24,GOLD,True)
            wrapped(s,BOSS_HINTS[era]+' Los perfiles mayores añaden salvas, marcas de caída y una fase más intensa.',(65,553),1120,17,MUTED)
        self.button('Volver',(65,638,200,47),lambda:self.set_state('notebook'),True,small=True)
        text(s,'Los ataques se anuncian. Aprender en el mapa del jefe prolonga su vulnerabilidad.',(1208,661),14,CYAN,False,'midright')

    def heritage(self):
        from .heritage import panel
        panel(self)
