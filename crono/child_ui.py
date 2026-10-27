"""Touch-first screens: one next step, pictograms and large reading cards."""
import math
from functools import lru_cache
import pygame as pg
from .art import text,rect,line,circle,polygon,diamond,PAPER,CYAN,GOLD,MUTED,INK
from .learning_ui import wrapped,wrap_rows


@lru_cache(maxsize=32)
def pictogram(kind,color):
    s=pg.Surface((80,80),pg.SRCALPHA);c=color
    if kind=='play':polygon(s,c,[(22,10),(69,40),(22,70)])
    elif kind=='book':
        polygon(s,c,[(8,15),(40,23),(72,15),(72,62),(40,70),(8,62)],4);line(s,c,(40,24),(40,68),4)
    elif kind=='shirt':polygon(s,c,[(25,12),(35,20),(45,20),(55,12),(75,29),(62,44),(56,37),(56,70),(24,70),(24,37),(18,44),(5,29)],4)
    elif kind=='route':
        for x,y in ((13,61),(39,18),(67,49)):circle(s,c,(x,y),8,3)
        line(s,c,(18,54),(34,25),4);line(s,c,(46,24),(61,43),4)
    elif kind=='star':
        pts=[(40+math.sin(i*math.pi/5)*(34 if i%2==0 else 15),40-math.cos(i*math.pi/5)*(34 if i%2==0 else 15)) for i in range(10)];polygon(s,c,pts,3)
    elif kind=='hand':
        rect(s,c,(28,33,31,33),9)
        for x,h in ((29,22),(38,13),(47,17),(56,25)):line(s,c,(x,46),(x,h),7)
        line(s,c,(29,52),(16,36),9)
    elif kind=='gear':
        circle(s,c,(40,40),22,5);circle(s,c,(40,40),8,4)
        for i in range(8):
            a=i*math.tau/8;line(s,c,(40+math.cos(a)*23,40+math.sin(a)*23),(40+math.cos(a)*33,40+math.sin(a)*33),7)
    elif kind=='exit':
        rect(s,c,(13,12,30,56),4,4);line(s,c,(36,40),(69,40),5);polygon(s,c,[(59,26),(74,40),(59,54)])
    elif kind=='heart':polygon(s,c,[(40,67),(8,36),(9,21),(21,13),(33,16),(40,26),(47,16),(59,13),(71,21),(72,36)])
    else:
        for x in (14,40,66):circle(s,c,(x,40),7)
    return s


@lru_cache(maxsize=64)
def icon_image(kind,color,size):return pg.transform.scale(pictogram(kind,color),(size,size))


class ChildUI:
    def mobile_card(self,label,caption,box,action,kind='play',primary=False,enabled=True):
        self.button('',box,action,primary,enabled,arrow=False)
        x,y,w,h=box;color=INK if primary else PAPER if enabled else MUTED
        size=80 if h>=135 else 60
        icon=icon_image(kind,color,size)
        self.canvas.blit(icon,(x+22,y+(h-size)//2))
        left=x+size+43
        wrapped(self.canvas,label,(left,y+25 if h>=135 else y+16),w-size-64,36 if primary else 26,color,True,leading=33)
        if caption:wrapped(self.canvas,caption,(left,y+h-53 if h>=135 else y+h-36),w-size-64,18,INK if primary else CYAN,leading=22)

    def child_menu(self):
        s=self.canvas;s.fill((13,28,39))
        text(s,'CRONO',(62,39),66,PAPER,True,serif=True)
        text(s,'Una aventura por la historia',(66,120),25,CYAN)
        text(s,self.school.active['alias'],(1205,62),24,GOLD,True,'topright')
        text(s,'© 2026 Renzo Leporace',(1205,109),16,MUTED,False,'topright')
        if self.save.data['practice']:text(s,'PRUEBA DOCENTE',(65,174),18,GOLD,True)
        play=self.continue_game if self.save.data['started'] else self.start_tutorial
        self.mobile_card('JUGAR','Sigue tu aventura' if self.save.data['started'] else 'Aprende los primeros pasos',(65,205,730,188),play,primary=True)
        self.mobile_card('Aprender','Paso a paso',(825,205,380,188),self.start_tutorial,'book')
        self.mobile_card('Mis aventuras','Elige un lugar',(65,421,555,110),lambda:self.set_state('chapters'),'route')
        self.mobile_card('Mi personaje','Trajes y apariencias',(650,421,555,110),lambda:self.open_panel('skins'),'shirt')
        self.mobile_card('Más cosas','Historias, premios y cuaderno',(65,557,555,110),lambda:self.set_state('mobile_more'),'more')
        self.mobile_card('Para adultos','Ajustes, edades y docentes',(650,557,555,110),self.open_settings,'gear')

    def mobile_more(self):
        self.canvas.fill((13,28,39));text(self.canvas,'¿Qué quieres descubrir?',(65,35),38,PAPER,True)
        rows=(('Historias de países','Argentina y Brasil',lambda:self.set_state('dlc_menu'),'route'),
              ('Mis premios','Logros de tus aventuras',self.open_rewards,'star'),
              ('Mi cuaderno','Repasa lo aprendido',lambda:self.open_panel('notebook'),'book'),
              ('Mi aula','Perfiles, clase e institución',self.open_community,'gear'),
              ('Créditos','Quién hizo esta aventura',lambda:self.set_state('credits'),'star'),
              ('Salir','Cerrar el juego',lambda:setattr(self,'running',False),'exit'))
        for i,(label,caption,action,kind) in enumerate(rows):self.mobile_card(label,caption,(65+i%2*585,125+i//2*145,555,125),action,kind)
        self.mobile_card('Volver','',(65,590,1140,90),lambda:self.set_state('menu'),'route')

    def mobile_goal(self):
        w=self.world;m=w.mechanic;p=w.player.rect
        if self.tutorial_active:
            labels=('Toca las flechas para caminar','Toca SALTAR para subir','Prueba el botón del rayo','Toca PULSO para disparar','Busca el libro y toca USAR')
            target=self.tutorial_target() if self.tutorial_step==4 else None
            return labels[self.tutorial_step],target[:2] if target else None,'book'
        if w.traits.exposure_kind:
            traits=w.traits
            if traits.resource<30 or traits.safe() and traits.resource<85:
                point=min(traits.points,key=lambda v:abs(v[0]-p.centerx))
                return ('Espera aquí para recuperar calor' if traits.exposure_kind=='cold' else 'Espera aquí para recargar') if traits.safe() else 'Busca el punto de resguardo señalado',point,'route'
            if not traits.coat:return {'cold':'Busca el abrigo: el frío sigue aumentando','oxygen':'Busca el tanque de oxígeno de reserva','gas':'Busca la máscara de protección'}[traits.exposure_kind],traits.coat_pos,'shirt'
        if w.traits.era in (3,8) and (w.traits.resource<30 or w.traits.safe() and w.traits.resource<90):
            point=min(w.traits.points,key=lambda v:abs(v[0]-p.centerx))
            label=('Espera aquí para recuperar agua' if w.traits.safe() else 'Busca agua y sombra') if w.traits.era==8 else ('Espera junto al farol para recuperar luz' if w.traits.safe() else 'Busca un farol para recuperar luz')
            return label,point,'route'
        if w.traits.era==2 and w.traits.resource<20:return 'Descansa un momento en el suelo',None,'route'
        work=m.field.work_target()
        if work:return work['label']+' · mantén USAR',work['point'],'hand'
        if m.state['step']<3:return f'Visita el puesto {m.state["step"]+1} · toca USAR',m.devices[min(2,m.state['step'])],'hand'
        f=m.field
        if not f.done:
            if f.kind in ('supply','catalogue','printing','dialogue','moonrepair') and len(f.collected)==3:
                target=w.data['repair_ship'] if f.kind=='moonrepair' else m.devices[0 if f.kind=='catalogue' else 2]
                return 'Lleva lo que juntaste · mantén USAR',target,'hand'
            if f.kind in ('naval','canal','tide'):return 'Busca la entrada al barco · toca USAR',m.devices[1],'hand'
            if f.kind in ('escort','ballot','siren','manuscripts'):return 'Camina junto a tu ayudante',(f.escort_x,f.escort_y),'route'
            if f.lifts:
                lift=next((v for i,v in enumerate(f.lifts) if i not in f.crossed),f.lifts[-1])
                return 'Sube a las plataformas que activaste',lift.rect.midtop,'route'
            points=[point for i,point in enumerate(f.points) if i not in (f.crossed if f.kind in ('chain','cipher','race','wind','warmth','train','rail') else f.collected)]
            if points:
                x,y=min(points,key=lambda v:abs(v[0]-p.centerx))
                return ('Prepara las cadenas · mantén USAR' if f.kind=='chain' else 'Lee las señales · mantén USAR' if f.kind=='cipher' else 'Busca las tres piezas de la misión'),(x,y+40),'hand' if f.kind in ('chain','cipher') else 'route'
            return 'Busca un refugio y espera a salvo',m.devices[1],'route'
        if not ({w.level_id*2,w.level_id*2+1}&w.answered):
            station=min(w.data['stations'],key=lambda v:abs(v[0]-p.centerx))
            return 'Abre el libro y responde una pregunta',station[:2],'book'
        if len(w.shards)<3:
            point=min((v for i,v in enumerate(w.data['shards']) if i not in w.shards),key=lambda v:abs(v[0]-p.centerx))
            return f'Busca los cristales · {len(w.shards)}/3',point,'star'
        if w.boss and w.boss.alive:
            return ('¡Se iluminó! Toca PULSO' if w.boss.phase=='exposed' else 'Esquiva y espera que se ilumine'),w.boss.rect.midbottom,'star'
        return '¡Todo listo! Ve al reloj azul',w.data['portal'],'route'

    def mobile_hud(self):
        s=self.canvas;w=self.world;p=w.player
        rect(s,(9,22,32),(0,0,1280,94))
        for i in range(p.max_hp):
            s.blit(icon_image('heart',(231,141,125) if i<p.hp else (65,79,89),29),(25+i*33,25))
        text(s,'VIDA',(28,65),14,PAPER,True)
        if w.traits.exposure_kind or w.traits.era in (2,3,8):
            label={'cold':'FRÍO','oxygen':'OXÍGENO','gas':'FILTRO'}.get(w.traits.exposure_kind) or {2:'FUERZA',3:'LUZ',8:'AGUA'}[w.traits.era]
            color=GOLD if w.traits.resource<30 else CYAN
            text(s,label,(277,23),16,color,True)
            rect(s,(54,76,85),(277,52,110,12),6)
            value=100-w.traits.resource if w.traits.exposure_kind=='cold' else w.traits.resource
            if value>0:rect(s,color,(277,52,max(1,value*1.1),12),6)
        for i in range(3):diamond(s,(468+i*35,39),12,CYAN if i in w.shards else (80,102,111),i in w.shards)
        text(s,'CRISTALES',(445,65),14,PAPER,True)
        circle(s,GOLD,(699,39),9,2);text(s,str(len(w.echoes)),(722,24),28,GOLD,True)
        text(s,'ECOS',(688,65),14,PAPER,True)
        s.blit(icon_image('book',CYAN,32),(878,22))
        text(s,str(self.save.data['knowledge']),(927,24),28,CYAN,True);text(s,'IDEAS',(878,65),14,PAPER,True)
        self.button('II',(1165,15,86,64),lambda:self.set_state('pause'),True,arrow=False)
        label,point,kind=self.mobile_goal()
        self.mobile_card(label,'',(25,107,965,75),lambda:self.set_state('story'),kind)
        self.button('',(1010,107,100,75),lambda:self.set_state('story'),arrow=False)
        text(s,'?',(1060,143),39,PAPER,True,'center')
        self.button('',(1130,107,120,75),lambda:self.read_aloud(label),arrow=False)
        self.draw_speaker((1190,144))
        boss=w.boss
        if boss and boss.active and boss.alive:
            rect(s,(16,31,41),(275,200,730,54),8)
            text(s,'GUARDIÁN',(293,209),16,PAPER,True)
            text(s,'¡DISPARA!' if boss.phase=='exposed' else 'ESQUIVA',(981,209),18,GOLD if boss.phase=='exposed' else CYAN,True,'topright')
            rect(s,(61,77,83),(292,238,695,8),4);rect(s,GOLD,(292,238,695*boss.hp/boss.max_hp,8),4)
        if w.message_time>0:
            y=270 if boss and boss.active else 199
            rect(s,(13,30,40),(275,y,730,77),8)
            wrapped(s,w.message,(294,y+13),690,20,CYAN,leading=25)
        work=w.mechanic.field.work_target()
        if work:
            rect(s,(13,30,40),(470,585,340,96),10)
            text(s,'MANTÉN USAR' if work['ready'] else 'ESPERA LA SEÑAL',(640,600),22,PAPER,True,'midtop')
            rect(s,(60,80,87),(490,647,300,13),6)
            if work['progress']:rect(s,CYAN,(490,647,300*work['progress'],13),6)

    def mobile_story_hud(self):
        self.world_action_hotspots=[]
        label,point,kind=self.mobile_goal()
        if point:
            x,y=point[0]-self.camera,point[1]-128
            if 290<x<self.viewport_width-370:
                y=max(235,min(405,y))
                self.world_canvas.blit(icon_image(kind,GOLD,42),(int(x-21),int(y-54)))
                polygon(self.world_canvas,GOLD,[(x-12,y-6),(x+12,y-6),(x,y+10)])
                if kind in ('hand','book'):self.world_action_hotspots.append(pg.Rect(x-40,y-66,80,80))
            else:
                direction=1 if x>self.viewport_width/2 else -1
                x=self.viewport_width-44 if direction>0 else 44
                polygon(self.world_canvas,GOLD,[(x+direction*18,255),(x-direction*12,237),(x-direction*12,273)])

    def mobile_story_panel(self):
        s=self.canvas;s.fill((13,28,39));w=self.world;m=w.mechanic
        text(s,'Tu siguiente paso',(65,30),40,PAPER,True)
        label,_,kind=self.mobile_goal()
        self.mobile_card(label,'',(65,100,1140,100),lambda:self.set_state('play'),kind,True)
        learned=bool({w.level_id*2,w.level_id*2+1}&w.answered)
        rows=((m.state['step']>=3,'Visita los tres puestos'),(m.field.done,'Completa el trabajo de la misión'),(learned,'Lee un libro y responde'),(len(w.shards)==3,f'Junta los tres cristales · {len(w.shards)}/3'),(not w.boss or not w.boss.alive,'Libera al guardián' if w.boss else 'Busca el reloj de salida'))
        for i,(done,label) in enumerate(rows):
            y=220+i*65;rect(s,(25,47,56),(65,y,1140,55),8)
            text(s,'✓' if done else str(i+1),(92,y+10),27,CYAN if done else GOLD,True)
            text(s,label,(148,y+12),24,PAPER)
        self.mobile_card('Volver a jugar','',(65,587,1140,92),lambda:self.set_state('play'),primary=True)

    def draw_speaker(self,center):
        x,y=center
        polygon(self.canvas,CYAN,[(x-25,y-10),(x-13,y-10),(x+1,y-23),(x+1,y+23),(x-13,y+10),(x-25,y+10)])
        for radius in (14,24):pg.draw.arc(self.canvas,CYAN,pg.Rect(x-radius+5,y-radius,radius*2,radius*2),-.9,.9,3)

    def read_aloud(self,value):
        from .mobile import speak
        if speak(value):
            if self.state=='play':self.set_state('story')
        else:self.notice='La voz está disponible en Android si hay una voz española instalada.';self.notice_time=4

    def mobile_intro(self):
        from .journeys import date_for
        s=self.canvas;s.fill((13,28,39))
        wrapped(s,self.world.data['meta'].name,(65,36),1140,38,PAPER,True,leading=45)
        text(s,date_for(self.world.level_id),(65,141),24,GOLD,True)
        from .story_ui import map_summary
        wrapped(s,map_summary(self.world.level_id),(65,193),1140,self.save.data['reading_size']+5,PAPER,leading=self.save.data['reading_size']+12)
        rows=(('Sigue las señales','Te dicen cuál es tu siguiente paso','hand'),('Abre los libros','Lee una pista y responde','book'),('Junta 3 cristales','Después busca la salida','star'))
        for i,(label,caption,kind) in enumerate(rows):
            x=65+i*390;self.mobile_card(label,'',(x,418,365,112),lambda:None,kind)
        self.mobile_card('Entrar a jugar','',(65,578,730,104),self.begin,'play',True)
        self.mobile_card('Volver','',(825,578,380,104),self.to_menu,'route')

    def mobile_activity(self):
        s=self.canvas;s.fill((13,28,39));m=self.world.mechanic
        text(s,f'Puesto {self.activity_index+1} de 3',(65,30),38,PAPER,True)
        wrapped(s,m.objective,(65,97),1135,25,GOLD,leading=31)
        maritime=m.kind in ('naval','canal','tide')
        if self.activity_index in m.state['activated']:
            text(s,'¡Este puesto ya está listo!',(65,225),34,CYAN,True)
            wrapped(s,m.operations[self.activity_index],(65,305),1130,28,PAPER,True)
            if maritime and self.activity_index==1:self.mobile_card('Navegar','Volverás a este lugar al terminar',(65,430,1140,115),self.start_voyage,'route',True)
        else:
            if maritime:
                from .sea_fieldwork import shore_question
                prompt,options=shore_question(m.kind,self.activity_index)
            else:prompt,options='¿Cuál es el siguiente paso?',m.operations
            wrapped(s,self.activity_message or prompt,(65,176),1130,23,CYAN,True,leading=28)
            for i,option in enumerate(options):
                box=(65,248+i*115,1140,102)
                self.button('',box,lambda n=i:self.activity_answer(n),arrow=False)
                circle(s,CYAN,(105,box[1]+50),22,2);text(s,str(i+1),(105,box[1]+50),25,PAPER,True,'center')
                wrapped(s,option,(150,box[1]+20),1020,26,PAPER,leading=31)
        self.mobile_card('Volver al mapa','',(65,610,1140,76),lambda:self.set_state('play'),'route')

    def mobile_quiz(self):
        from .education import LESSONS,fact_for,SOURCES
        s=self.canvas;s.fill((13,28,39));q=self.question
        fact=self.reading_fact() if self.quiz_mode=='read' else q.explanation or fact_for(self.quiz_topic,self.save.data['age_band'])
        title='Una pista de la historia' if self.quiz_mode=='read' else 'Elige una respuesta' if self.quiz_mode=='question' else '¡Muy bien!' if self.quiz_mode=='correct' else 'Vamos a pensarlo otra vez'
        text(s,title,(65,31),39,CYAN if self.quiz_mode=='correct' else PAPER,True)
        spoken=(q.prompt+'. '+'. '.join(f'{i+1}: {value}' for i,value in enumerate(q.options))) if self.quiz_mode=='question' else fact
        self.button('',(1125,20,80,65),lambda:self.read_aloud(spoken),arrow=False)
        self.draw_speaker((1165,52))
        reading_size=self.save.data['reading_size']+7;leading=reading_size+9
        self.quiz_fact_view_height=280;self.quiz_fact_height=len(wrap_rows(fact,1070,reading_size))*leading
        self.quiz_feedback_height=self.quiz_fact_height
        if self.quiz_mode=='question':
            image=getattr(q,'kind','choice')=='image';left=65
            if image:
                from .heritage import illustration
                from .curiosities import MAP_CURIOSITIES
                s.blit(pg.transform.smoothscale(illustration(MAP_CURIOSITIES[self.quiz_topic//2]),(115,112)),(65,103));left=205
            size=self.save.data['reading_size']+8
            while size>20 and len(wrap_rows(q.prompt,1205-left,size,True))*(size+7)>108:size-=1
            wrapped(s,q.prompt,(left,111),1205-left,size,PAPER,True,leading=size+7)
            for i,option in enumerate(q.options):
                box=(65,230+i*123,1140,110)
                self.button('',box,lambda n=i:self.answer_question(n),arrow=False)
                circle(s,CYAN,(104,box[1]+54),23,2);text(s,str(i+1),(104,box[1]+53),26,PAPER,True,'center')
                option_size=self.save.data['reading_size']+5
                while option_size>19 and len(wrap_rows(option,1035,option_size))*(option_size+6)>88:option_size-=1
                wrapped(s,option,(149,box[1]+13),1035,option_size,PAPER,leading=option_size+6)
            self.mobile_card('Volver al mapa','',(65,610,1140,76),self.close_quiz,'route')
            return
        if self.quiz_mode=='read':
            wrapped(s,LESSONS[self.quiz_topic].title,(65,103),1135,28,GOLD,True)
            content=fact;top=182
        else:
            content='Respuesta: '+q.options[q.correct]+'\n\n'+fact;top=128
            if self.quiz_mode=='correct':
                text(s,'+2 IDEAS' if self.quiz_reward else '¡Ya lo recuerdas!',(1205,86),25,GOLD,True,'topright')
        rows=wrap_rows(content,1070,reading_size);page_size=max(1,265//leading);pages=max(1,math.ceil(len(rows)/page_size))
        self.quiz_page=max(0,min(pages-1,getattr(self,'quiz_page',0)))
        rect(s,(24,45,55),(65,top-10,1140,325),10)
        for i,row in enumerate(rows[self.quiz_page*page_size:(self.quiz_page+1)*page_size]):text(s,row,(94,top+8+i*leading),reading_size,PAPER)
        text(s,f'{self.quiz_page+1} / {pages}',(640,top+294),18,CYAN,True,'center')
        if pages>1:
            self.button('‹',(82,top+274,70,44),lambda:setattr(self,'quiz_page',self.quiz_page-1),enabled=self.quiz_page>0,arrow=False)
            self.button('›',(1118,top+274,70,44),lambda:setattr(self,'quiz_page',self.quiz_page+1),enabled=self.quiz_page<pages-1,arrow=False)
        source=next((label for label,url in SOURCES if url==q.source),'Fuente del docente')
        text(s,source[:105],(65,535),17,MUTED)
        if self.quiz_mode=='read':
            action=lambda:setattr(self,'quiz_page',self.quiz_page+1) if self.quiz_page<pages-1 else (setattr(self,'quiz_page',0),setattr(self,'quiz_mode','question'))
            self.mobile_card('Seguir leyendo' if self.quiz_page<pages-1 else 'Responder','',(420,591,785,96),action,'play',True)
            self.mobile_card('Volver','',(65,591,325,96),self.close_quiz,'route')
        elif self.quiz_mode=='correct':
            self.mobile_card('Volver a jugar','',(65,591,730,96),self.close_quiz,'play',True)
            self.mobile_card('Contarlo','',(825,591,380,96),self.open_reflection,'book')
        else:self.mobile_card('Intentar otra vez','',(65,591,1140,96),lambda:(setattr(self,'quiz_page',0),setattr(self,'quiz_mode','question')),'play',True)
