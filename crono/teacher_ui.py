"""In-game settings and a complete local question editor for teachers."""
from copy import deepcopy
import pygame as pg
from .art import text,tracked,rect,line,PAPER,MUTED,CYAN,GOLD,W,H,font
from .education import STAGES,LESSONS,AGE_BANDS
from .learning_ui import wrapped
from .question_bank import QuestionBank,builtin_records
from .text_field import TextField
from .campaign import chapter_levels
from .campaign import ERA_LABELS,TOTAL_ERAS,TOTAL_LEVELS,DIFFICULTIES,level_label,CHAPTER_ORDER,DISPLAY_LEVEL_IDS
from .i18n import tr,literal,language,LANGUAGES


def shortened(value,width,size=16):
    value=tr(value)
    if font(size).size(value)[0]<=width:
        return value
    while value and font(size).size(value+'…')[0]>width:
        value=value[:-1]
    return literal(value+'…')


class TeacherUI:
    def init_teacher(self,bank_file=None):
        self.bank=QuestionBank(bank_file)
        self.settings_return='menu'
        self.teacher_era=self.teacher_stage=self.teacher_band=-1
        self.teacher_page=0
        self.teacher_selected=0
        self.teacher_detail_scroll=0
        self.teacher_detail_height=0
        self.teacher_query=TextField('',120)
        self.teacher_fields=[]
        self.teacher_draft=None
        self.teacher_original=None
        self.teacher_message=''
        self.teacher_discard=False
        self.teacher_quit=False
        self.teacher_picker=False
        self.preview_level=0
        self.preview_world=None

    def open_settings(self):
        if self.state not in ('settings','teacher','question_edit','scenarios'):
            self.settings_return=self.state
        self.teacher_query.focused=False
        self.teacher_message=''
        self.set_state('settings')

    def close_settings(self):
        self.set_state(self.settings_return)

    def settings_background(self):
        if self.settings_return in ('play','pause','help_play'):
            self.artist.scene(self.canvas,self.world,self.camera,self.time)
        else:
            self.artist.background(self.canvas,0,0,self.time)
        self.dim(230)

    def settings(self):
        if self.touch_enabled():self.mobile_settings();return
        s=self.canvas
        self.settings_background()
        tracked(s,'PERSONALIZA EL VIAJE',(65,38),12,CYAN,3)
        text(s,'Configuración',(62,73),45,PAPER,True,serif=True)
        rect(s,(19,35,45),(65,160,537,445),8)
        text(s,'Partida y presentación',(88,184),24,PAPER,True)
        self.button('Música y sonidos',(88,241,491,50),lambda:self.set_state('sound_settings'),small=True)
        self.button('Pantalla: '+('completa' if self.fullscreen else 'ventana'),(88,307,491,50),self.toggle_fullscreen,small=True)
        self.button('Idioma · '+dict(LANGUAGES)[language()],(88,369,491,40),lambda:self.set_state('language_settings'),small=True)
        self.age_switch(88,423,491)
        wrapped(s,'La edad cambia preguntas y combate: 6–9 mínima, 10–14 media y 15+ alta. Los jefes ganan patrones y los enemigos reaccionan más rápido.',(88,487),481,15,MUTED,leading=23)
        rect(s,(19,35,45),(627,160,588,445),8)
        text(s,'Zona docente',(650,184),26,PAPER,True)
        wrapped(s,f'{len(self.bank.records)} preguntas con sus respuestas. Puedes consultar todo el banco, editar contenidos y agregar preguntas para cada mapa y edad.',(650,239),532,19,PAPER,leading=30)
        self.button('Ver y editar preguntas',(650,371,542,58),lambda:self.need_teacher(lambda:self.set_state('teacher')),True)
        self.button('Ver los 36 escenarios',(650,448,542,49),self.open_scenarios,small=True)
        text(s,'Las respuestas son visibles en la zona docente.',(650,524),14,GOLD)
        self.button('Volver',(65,628,249,49),self.close_settings,True,small=True)
        self.button('Accesibilidad',(335,628,265,49),lambda:self.set_state('accessibility'),small=True)
        self.button('Aula y salas',(620,628,265,49),lambda:self.open_community('rooms'),small=True)
        if self.bank.warning:
            wrapped(s,self.bank.warning,(345,615),860,13,GOLD,leading=20)
        else:
            text(s,'Edición local · el banco se conserva separado del progreso.',(1210,653),14,MUTED,False,'midright')

    def cycle_teacher_filter(self,name,total):
        value=getattr(self,name)
        setattr(self,name,-1 if value==total-1 else value+1)
        self.teacher_page=0
        self.teacher_query.focused=False

    def select_teacher_question(self,key):
        self.teacher_selected=key
        self.teacher_detail_scroll=0

    def teacher(self):
        s=self.canvas
        self.settings_background()
        tracked(s,'ZONA DOCENTE · RESPUESTAS VISIBLES',(65,28),11,CYAN,2)
        text(s,'Banco de preguntas',(62,58),38,PAPER,True,serif=True)
        self.button('+ Nueva pregunta',(946,56,269,48),lambda:self.edit_question(None),True,small=True)
        eras=ERA_LABELS
        self.button('Época: '+('todas' if self.teacher_era<0 else eras[self.teacher_era]),(65,126,222,41),
                    lambda:self.cycle_teacher_filter('teacher_era',TOTAL_ERAS),small=True,arrow=False)
        self.button('Mapa: '+('todos' if self.teacher_stage<0 else str(self.teacher_stage+1)),(301,126,192,41),
                    lambda:self.cycle_teacher_filter('teacher_stage',len(chapter_levels(self.teacher_era)) if self.teacher_era>=0 else 4),small=True,arrow=False)
        self.button('Edad: '+('todas' if self.teacher_band<0 else ('6–9','10–14','15+')[self.teacher_band]),(507,126,251,41),
                    lambda:self.cycle_teacher_filter('teacher_band',3),small=True,arrow=False)
        self.teacher_query.draw(s,(65,182,693,43),'Buscar en preguntas, respuestas o explicaciones…',16)
        results=self.bank.filtered(self.teacher_era,self.teacher_stage,self.teacher_band,self.teacher_query.value)
        pages=max(1,(len(results)+5)//6)
        self.teacher_page=max(0,min(pages-1,self.teacher_page))
        if results and self.teacher_selected not in {q['id'] for q in results}:
            self.select_teacher_question(results[0]['id'])
        visible=results[self.teacher_page*6:self.teacher_page*6+6]
        for n,q in enumerate(visible):
            q=self.bank.display_record(q)
            y=241+n*59
            selected=q['id']==self.teacher_selected
            self.button('',(65,y,693,53),lambda key=q['id']:self.select_teacher_question(key),primary=selected,arrow=False)
            color=(16,36,44) if selected else PAPER
            meta=f'#{q["id"]+1:03d}   ·   {level_label(q["topic"]//2)}   ·   {("6–9","10–14","15+")[q["band"]]} años'
            text(s,meta,(78,y+4),11,color,True)
            text(s,shortened(q['prompt'],660,16),(78,y+23),16,color)
        if not results:
            wrapped(s,'No hay preguntas con esos filtros. Puedes cambiar la búsqueda o crear una nueva.',(89,291),641,22,MUTED)
        rect(s,(20,36,47),(784,126,431,481),7)
        if results:
            q=self.bank.display_record(self.bank.get(self.teacher_selected))
            text(s,'VISTA CON RESPUESTA',(805,145),11,CYAN,True)
            old_clip=s.get_clip()
            s.set_clip(pg.Rect(801,175,402,302))
            top=180-self.teacher_detail_scroll
            yy=wrapped(s,q['prompt'],(805,top),389,21,PAPER,True,leading=28)
            yy=max(yy+18,top+104)
            for n,option in enumerate(q['options']):
                label=literal(str(tr('[Correcta] ' if n==q['correct'] else ''))+'ABC'[n]+'. '+str(tr(option)))
                yy=wrapped(s,label,(805,yy),389,16,CYAN if n==q['correct'] else MUTED,leading=23)+12
            self.teacher_detail_height=yy-top
            s.set_clip(old_clip)
            text(s,'Correcta: '+'ABC'[q['correct']],(805,486),15,CYAN,True)
            if self.teacher_detail_height>297:
                text(s,'Rueda: desplazar respuestas',(1194,489),11,MUTED,False,'topright')
            self.button('Editar',(805,520,180,46),lambda:self.edit_question(self.teacher_selected),True,small=True)
            self.button('Duplicar',(1000,520,194,46),lambda:self.edit_question(self.teacher_selected,duplicate=True),small=True)
        self.button('Configuración',(65,626,224,46),lambda:self.set_state('settings'),small=True)
        self.button('Anterior',(303,626,143,46),lambda:setattr(self,'teacher_page',self.teacher_page-1),enabled=self.teacher_page>0,small=True,arrow=False)
        self.button('Siguiente',(459,626,151,46),lambda:setattr(self,'teacher_page',self.teacher_page+1),enabled=self.teacher_page<pages-1,small=True,arrow=False)
        self.button('Crear respaldo',(784,626,431,46),self.backup_questions,small=True)
        text(s,f'{len(results)} de {len(self.bank.records)} preguntas · página {self.teacher_page+1}/{pages}',(65,694),12,MUTED,False,'bottomleft')
        if self.teacher_message:
            text(s,shortened(self.teacher_message,758,12),(1212,694),12,GOLD,False,'bottomright')

    def backup_questions(self):
        try:
            self.bank.backup()
            self.teacher_message='Copia creada en contenido/respaldos.'
        except OSError:
            self.teacher_message='No se pudo crear el respaldo en esta carpeta.'

    def edit_question(self,question_id,duplicate=False):
        self.teacher_edit_language=language()
        if question_id is None:
            era=max(0,self.teacher_era)
            stage=max(0,self.teacher_stage)
            draft=dict(id=None,topic=chapter_levels(era)[stage%len(chapter_levels(era))]*2,band=max(0,self.teacher_band) if self.teacher_band>=0 else self.save.data['age_band'],
                       prompt='',options=['','',''],correct=0,explanation='',source='')
        else:
            draft=self.bank.get(question_id)
            if duplicate:
                draft['id']=None
        self.teacher_draft=deepcopy(draft)
        self.teacher_edit_translation=question_id is not None and not duplicate and self.teacher_edit_language!=draft.get('language','es')
        view=self.bank.display_record(self.bank.get(question_id)) if question_id is not None else draft
        if question_id is None or duplicate:
            if language()!='es':self.teacher_draft['language']=language()
        self.teacher_fields=[TextField(str(tr(view['prompt'])),220,True),
                             *[TextField(str(tr(o)),180,True) for o in view['options']],
                             TextField(str(tr(view['explanation'])),700,True),TextField(str(tr(view['source'])),300)]
        self.teacher_original=self.current_draft()
        self.teacher_fields[0].focused=True
        self.teacher_query.focused=False
        self.teacher_discard=self.teacher_quit=False
        self.teacher_picker=False
        self.teacher_message=''
        pg.key.start_text_input()
        self.set_state('question_edit')

    def current_draft(self):
        draft=deepcopy(self.teacher_draft)
        fields=dict(prompt=self.teacher_fields[0].value,options=[f.value for f in self.teacher_fields[1:4]],
                    explanation=self.teacher_fields[4].value,source=self.teacher_fields[5].value)
        if self.teacher_edit_translation:draft.setdefault('translations',{})[self.teacher_edit_language]=fields
        else:draft.update(fields)
        return draft

    def teacher_dirty(self):
        return self.teacher_draft is not None and self.current_draft()!=self.teacher_original

    def leave_editor(self,quitting=False):
        if self.teacher_dirty():
            self.teacher_discard=True
            self.teacher_quit=quitting
            self.selection=0
            self.buttons=[]
        elif quitting:
            self.running=False
        else:
            self.set_state('teacher')

    def discard_editor(self):
        self.teacher_discard=False
        if self.teacher_quit:
            self.running=False
        else:
            self.set_state('teacher')

    def save_question(self):
        try:
            key=self.bank.upsert(self.current_draft())
            if self.room:
                with self.room.lock:self.room.bank=list(self.bank.records)
        except (ValueError,OSError) as error:
            self.teacher_message=str(error) if isinstance(error,ValueError) else 'No se pudo guardar. Revisa el permiso de escritura de la carpeta del juego.'
            return
        self.teacher_selected=key
        self.teacher_era=self.teacher_stage=self.teacher_band=-1
        self.teacher_query.set_value('')
        results=self.bank.filtered()
        self.teacher_page=next(i for i,q in enumerate(results) if q['id']==key)//6
        self.teacher_message='Pregunta guardada. Ya está disponible en los archivos de ese mapa y edad.'
        self.audio.play('checkpoint')
        self.set_state('teacher')

    def restore_original_question(self):
        original=next(q for q in builtin_records() if q['id']==self.teacher_draft['id'])
        if not self.teacher_edit_translation:self.teacher_draft=deepcopy(original)
        view=self.bank.display_record(original)
        values=[str(tr(v)) for v in [view['prompt'],*view['options'],view['explanation'],view['source']]]
        for field,value in zip(self.teacher_fields,values):
            field.set_value(value)
        self.teacher_message='Original cargado en el formulario. Pulsa Guardar para aplicarlo.'

    def question_edit(self):
        s=self.canvas
        self.settings_background()
        new=self.teacher_draft['id'] is None
        tracked(s,'EDITOR DOCENTE',(65,22),11,CYAN,3)
        text(s,'Nueva pregunta' if new else f'Editar pregunta #{self.teacher_draft["id"]+1:03d}',(62,49),33,PAPER,True,serif=True)
        topic=self.teacher_draft['topic']
        level_id=topic//2
        self.button(f'{level_label(level_id)} · '+shortened(STAGES[level_id].name,280,14),(65,99,550,36),
                    lambda:setattr(self,'teacher_picker',True),small=True,arrow=False)
        self.button('Archivo '+str(topic%2+1),(630,99,225,36),lambda:self.teacher_draft.update(topic=topic//2*2+(1-topic%2)),small=True,arrow=False)
        self.button(('6–9 años','10–14 años','15+ años')[self.teacher_draft['band']],(870,99,345,36),
                    lambda:self.teacher_draft.update(band=(self.teacher_draft['band']+1)%3),small=True,arrow=False)
        text(s,'Pregunta',(65,144),13,MUTED,True)
        self.teacher_fields[0].draw(s,(65,165,1150,66),'Escribe una pregunta clara…',18)
        for n in range(3):
            x=65+n*390
            text(s,'Respuesta '+'ABC'[n],(x,237),13,MUTED,True)
            self.teacher_fields[n+1].draw(s,(x,259,370,67),'Escribe la opción '+str(n+1),16)
            correct=n==self.teacher_draft['correct']
            self.button(('Correcta: ' if correct else 'Marcar como correcta: ')+'ABC'[n],(x,335,370,32),
                        lambda choice=n:self.teacher_draft.update(correct=choice),primary=correct,small=True,arrow=False)
        text(s,'Explicación / pista educativa que verá el alumno',(65,381),13,MUTED,True)
        self.teacher_fields[4].draw(s,(65,404,1150,91),'Explica por qué la respuesta es correcta. Esta pista también se puede leer antes de responder.',17)
        text(s,'Fuente o referencia (opcional)',(65,508),13,MUTED,True)
        self.teacher_fields[5].draw(s,(65,531,1150,41),'URL, libro o referencia del docente',16)
        if self.teacher_message:
            wrapped(s,self.teacher_message,(65,584),1147,14,GOLD,leading=19)
        self.button('Guardar pregunta',(65,632,293,49),self.save_question,True,small=True)
        self.button('Cancelar',(374,632,185,49),self.leave_editor,small=True)
        text(s,'Idioma · '+dict(LANGUAGES)[self.teacher_edit_language],(1210,649),16,CYAN,False,'midright')
        if not new and any(q['id']==self.teacher_draft['id'] for q in builtin_records()):
            self.button('Cargar original',(575,632,245,49),self.restore_original_question,small=True)
        text(s,'Tab cambia de campo · Ctrl+Enter guarda · Ctrl+C/V copia y pega',(1210,701),12,MUTED,False,'bottomright')
        if self.teacher_picker:
            self.dim(235)
            self.buttons=[]
            rect(s,(20,36,47),(42,57,1196,605),8)
            text(s,'Elegir mapa para esta pregunta',(66,77),30,PAPER,True,serif=True)
            for row,n in enumerate(DISPLAY_LEVEL_IDS):
                meta=STAGES[n]
                x=66+row%5*236
                y=128+row//5*45
                self.button(f'{level_label(n)} · {meta.name}',(x,y,224,40),lambda value=n:self.pick_teacher_map(value),
                            primary=n==level_id,small=True,arrow=False,wrap=True)
            self.button('Volver',(66,602,218,42),lambda:setattr(self,'teacher_picker',False),small=True)
        if self.teacher_discard:
            self.dim(225)
            self.buttons=[]
            rect(s,(20,36,47),(335,239,610,246),8)
            text(s,'Hay cambios sin guardar',(368,272),30,PAPER,True,serif=True)
            wrapped(s,'Puedes seguir editando o descartar los cambios de este formulario.',(368,329),540,17,MUTED)
            self.button('Seguir editando',(368,411,260,47),lambda:setattr(self,'teacher_discard',False),True,small=True)
            self.button('Descartar y cerrar' if self.teacher_quit else 'Descartar',(645,411,265,47),self.discard_editor,small=True)

    def pick_teacher_map(self,level_id):
        self.teacher_draft['topic']=level_id*2+self.teacher_draft['topic']%2
        self.teacher_picker=False
        self.selection=0

    def handle_teacher_event(self,event):
        if self.state not in ('settings','teacher','question_edit','scenarios'):
            return False
        if event.type==pg.KEYDOWN and event.key==pg.K_ESCAPE:
            if self.state=='question_edit':
                if self.teacher_picker:
                    self.teacher_picker=False
                elif self.teacher_discard:
                    self.teacher_discard=False
                else:
                    self.leave_editor()
            elif self.state=='settings':
                self.close_settings()
            else:
                self.teacher_query.focused=False
                self.set_state('settings')
            return True
        if self.state=='question_edit' and event.type==pg.QUIT and self.teacher_dirty():
            self.leave_editor(True)
            return True
        if self.state=='scenarios' and event.type==pg.KEYDOWN and event.key in (pg.K_LEFT,pg.K_RIGHT):
            self.change_scenario(-1 if event.key==pg.K_LEFT else 1)
            return True
        if self.state not in ('teacher','question_edit') or self.teacher_discard or self.teacher_picker:
            return False
        if self.state=='teacher' and event.type==pg.MOUSEWHEEL:
            if pg.Rect(784,126,431,389).collidepoint(self.mouse):
                self.teacher_detail_scroll=max(0,min(max(0,self.teacher_detail_height-297),self.teacher_detail_scroll-event.y*55))
            else:
                self.teacher_page=max(0,self.teacher_page-event.y)
            return True
        fields=[self.teacher_query] if self.state=='teacher' else self.teacher_fields
        if event.type in (pg.MOUSEBUTTONDOWN,pg.MOUSEBUTTONUP,pg.MOUSEMOTION):
            # Native window events use display pixels; text fields use the canvas.
            if hasattr(event,'pos'):
                attrs=event.dict.copy()
                attrs['pos']=self.logical_mouse(event.pos)
                event=pg.event.Event(event.type,attrs)
            if event.type==pg.MOUSEBUTTONDOWN and event.button==1:
                for field in fields:
                    field.focused=field.box.collidepoint(event.pos)
                if any(f.focused for f in fields):
                    pg.key.start_text_input()
                    pg.key.set_repeat(350,35)
            for field in fields:
                if field.handle(event):
                    return True
            return False
        if self.state=='question_edit' and event.type==pg.KEYDOWN and event.key in (pg.K_RETURN,pg.K_KP_ENTER,pg.K_s) and getattr(event,'mod',pg.key.get_mods())&pg.KMOD_CTRL:
            self.save_question()
            return True
        if event.type==pg.KEYDOWN and event.key==pg.K_TAB:
            if self.state=='teacher' and self.teacher_query.focused:
                self.teacher_query.focused=False
                return True
            focused=next((i for i,f in enumerate(fields) if f.focused),-1)
            shift=bool(getattr(event,'mod',pg.key.get_mods())&pg.KMOD_SHIFT)
            for f in fields:
                f.focused=False
            fields[(focused+(-1 if shift else 1))%len(fields)].focused=True
            return True
        for field in fields:
            before=field.value
            if field.handle(event):
                if self.state=='teacher' and before!=field.value:
                    self.teacher_page=0
                return True
        return False

    def open_scenarios(self):
        self.preview_level=self.world.level_id
        self.change_scenario(0)
        self.set_state('scenarios')

    def change_scenario(self,delta):
        from .physics import World
        self.preview_level=(self.preview_level+delta)%TOTAL_LEVELS
        self.preview_world=World(*divmod(self.preview_level,3))
        p=self.preview_world.platforms[1].rect
        self.preview_world.player.rect.midbottom=(p.left+150,p.top)
        self.preview_camera=max(0,p.left+150-480)
        self.preview_world.player.grounded=True
        self.preview_world.time=30

    def scenarios(self):
        from .visuals import MOODS
        if self.preview_world is None:
            self.change_scenario(0)
        s=self.canvas
        self.artist.scene(s,self.preview_world,self.preview_camera,self.time)
        rect(s,(12,25,35),(0,0,W,107))
        meta=STAGES[self.preview_level]
        tracked(s,f'GALERÍA · {level_label(self.preview_level)}',(35,17),11,CYAN,3)
        text(s,meta.name,(33,45),33,PAPER,True,serif=True)
        rect(s,(12,25,35),(0,621,W,99))
        self.button('Configuración',(35,649,235,43),lambda:self.set_state('settings'),small=True)
        self.button('Anterior',(287,649,174,43),lambda:self.change_scenario(-1),small=True)
        self.button('Siguiente',(477,649,174,43),lambda:self.change_scenario(1),True,small=True)
        text(s,MOODS[self.preview_level].description,(W-35,616),13,GOLD,False,'midright')
