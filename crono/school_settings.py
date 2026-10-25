"""Teacher file exchange, curriculum selection and independent accessibility."""
import json
import sys
from pathlib import Path
import pygame as pg
from .school import atomic_json
from .text_field import TextField
from .art import text,tracked,rect,PAPER,CYAN,GOLD,MUTED
from .learning_ui import wrapped
from .education import LESSONS,STAGES
from .touch import DEFAULT_KEYS,KEY_LABELS
from .storage import atomic_replace

class SchoolSettingsUI:
    def init_school_settings(self):
        self.exchange_path=TextField('',500);self.pin_field=TextField('',64);self.delete_field=TextField('',12)
        self.pin_field.password=True
        self.exchange_preview=None;self.exchange_message='';self.topic_page=0;self.access_message=''
        self.school_tab='files';self.reading_pane='fact'
        self.reflection_field=TextField('',1000,True)

    def handle_school_event(self,event):
        if self.state not in ('school_settings','reflection'):return False
        fields=[self.reflection_field] if self.state=='reflection' else [self.exchange_path] if self.school_tab=='files' else [self.pin_field,self.delete_field] if self.school_tab=='privacy' else []
        if event.type in (pg.MOUSEBUTTONDOWN,pg.MOUSEBUTTONUP,pg.MOUSEMOTION):
            event=pg.event.Event(event.type,dict(event.dict,pos=self.logical_mouse(event.pos)))
            if event.type==pg.MOUSEBUTTONDOWN:
                for f in fields:f.focused=f.box.collidepoint(event.pos)
                if any(f.focused for f in fields):pg.key.start_text_input()
        return any(f.handle(event) for f in fields)
    def open_reflection(self):
        self.reflection_field.set_value('');self.reflection_field.focused=True
        self.set_state('reflection');pg.key.start_text_input()
    def save_reflection(self):
        from datetime import datetime,timezone
        value=self.reflection_field.value.strip()
        if not value:return
        self.save.data['reviews'].append(dict(at=datetime.now(timezone.utc).isoformat(timespec='seconds'),question=self.question.id,
            topic=self.quiz_topic,text=value,prompt=self.question.prompt,practice=self.save.data['practice']))
        self.save.data['reviews']=self.save.data['reviews'][-5000:];self.save.write();self.set_state('quiz')
    def reflection(self):
        s=self.canvas;s.fill((13,27,37));text(s,'¿Qué evidencia apoya tu respuesta?',(62,60),39,PAPER,True,serif=True)
        wrapped(s,'Explica qué pista usaste y qué te gustaría comprobar en otra fuente. El docente podrá leer tu explicación; no se califica automáticamente.',(65,138),1110,22,CYAN,leading=33)
        self.reflection_field.draw(s,(65,257,1145,302),'Mi explicación…',22)
        self.button('Guardar explicación',(65,615,400,57),self.save_reflection,True)
        self.button('Volver sin guardar',(489,615,400,57),lambda:self.set_state('quiz'))

    def preview_import(self):
        from .mobile import import_bank
        if import_bank(self.preview_native_bank):return
        from .question_bank import validate_record
        try:
            path=Path(self.exchange_path.value.strip())
            if path.stat().st_size>4_000_000:raise ValueError('El archivo supera 4 MB.')
            document=json.loads(path.read_text(encoding='utf-8-sig'))
            if not isinstance(document,dict) or not isinstance(document.get('questions'),list):raise ValueError('Falta una lista questions en el JSON.')
            records=[validate_record(r) for r in document['questions']]
            if len(records)>10000 or len({r['id'] for r in records})!=len(records):raise ValueError('Hay IDs duplicados o demasiadas preguntas.')
            self.bank.validate_pools(records);self.exchange_preview=records
            self.exchange_message=f'Vista previa válida: {len(records)} preguntas, {len({r["topic"] for r in records})} temas. Aplicar reemplazará el banco local y creará un respaldo.'
        except (OSError,ValueError,TypeError,KeyError) as error:
            self.exchange_preview=None;self.exchange_message=str(error)
    def preview_native_bank(self,result):
        from .question_bank import validate_record
        self.exchange_preview=None
        if 'text' not in result:
            self.exchange_message=result.get('error','Importación cancelada.');return
        try:
            document=json.loads(result['text'].lstrip('\ufeff'))
            if not isinstance(document,dict) or not isinstance(document.get('questions'),list):raise ValueError('Falta una lista questions en el JSON.')
            if len(document['questions'])>10000:raise ValueError('Demasiadas preguntas: máximo 10000.')
            records=[validate_record(r) for r in document['questions']]
            self.bank.validate_pools(records)
            if len({r['id'] for r in records})!=len(records):raise ValueError('IDs repetidos.')
            self.exchange_preview=records;self.exchange_message=f'Archivo Android válido: {len(records)} preguntas. Aplicar crea un respaldo.'
        except (ValueError,KeyError,TypeError) as error:self.exchange_message=str(error)
    def apply_import(self):
        if not self.exchange_preview:return
        try:
            self.bank.backup();self.bank.path.parent.mkdir(parents=True,exist_ok=True)
            temporary=self.bank.path.with_suffix('.tmp');temporary.write_text(self.bank.serialise(self.exchange_preview),encoding='utf-8')
            atomic_replace(temporary,self.bank.path);self.bank.records=self.exchange_preview;self.exchange_preview=None
            from .mobile import persist
            persist(self.bank.path)
            if self.room:
                with self.room.lock:self.room.bank=list(self.bank.records)
            self.exchange_message='Banco aplicado. Las personalizaciones anteriores están en contenido/respaldos.'
        except OSError as error:self.exchange_message=str(error)
    def export_bank(self):
        try:
            target=self.school.root/'informes'/'banco-preguntas.json';target.parent.mkdir(parents=True,exist_ok=True)
            target.write_text(self.bank.serialise(self.bank.records),encoding='utf-8');self.exchange_message='Exportado: '+str(target)
            from .mobile import export_document
            if export_document(target,lambda r:setattr(self,'exchange_message','Banco exportado.' if r.get('saved') else 'Exportación cancelada.')):self.exchange_message='Elige dónde guardar el banco en Android.'
        except OSError as error:self.exchange_message=str(error)
    def toggle_topic(self,topic):
        selected=set(self.school.config.get('topics',[]))
        if topic in selected:selected.remove(topic)
        else:selected.add(topic)
        self.school.config['topics']=sorted(selected);atomic_json(self.school.config_path,self.school.config)
        if self.room:
            with self.room.lock:self.room.topics=list(self.school.config['topics'])
    def clear_topics(self):
        self.school.config['topics']=[];atomic_json(self.school.config_path,self.school.config)
        if self.room:
            with self.room.lock:self.room.topics=[]
    def set_motor(self,band):
        self.save.data['motor_band']=band;self.world.set_difficulty(self.save.combat_band());self.save.write()
    def accessibility(self):
        s=self.canvas;s.fill((13,27,37));text(s,'Jugar a tu manera',(62,48),41,PAPER,True,serif=True)
        text(s,'Asistencia motriz independiente de las preguntas',(65,122),23,CYAN,True)
        for i,(label,band) in enumerate((('Según edad',None),('Mínima',0),('Media',1),('Alta',2))):
            self.button(label,(65+i*292,166,270,54),lambda n=band:self.set_motor(n),primary=self.save.data['motor_band']==band,small=True,arrow=False)
        text(s,'Tamaño de lectura',(65,245),22,PAPER,True)
        for i,size in enumerate((19,22,25)):
            self.button(('Normal','Grande','Muy grande')[i],(65+i*230,287,210,52),lambda n=size:(self.save.data.update(reading_size=n),self.save.write()),primary=self.save.data['reading_size']==size,small=True,arrow=False)
        self.button('Controles táctiles: '+('SÍ' if self.touch_enabled() else 'NO'),(790,287,420,52),lambda:(self.save.data.update(touch_controls=not self.touch_enabled()),self.save.write()),small=True)
        for i,(action,label) in enumerate(KEY_LABELS.items()):
            x=65+i%4*292;y=378+i//4*78
            self.button(label+': '+('pulsa tecla…' if self.rebind_action==action else pg.key.name(self.key_for(action))),(x,y,270,57),lambda a=action:setattr(self,'rebind_action',a),small=True,arrow=False)
        wrapped(s,self.access_message or 'Reasigna una acción y pulsa una tecla. Esc cancela. En lectura: Tab alterna panel; RePág / AvPág desplazan el texto.',(65,562),1110,18,MUTED)
        self.button('Volver',(65,638,250,51),lambda:self.set_state('settings'),True,small=True)
        self.button('Restablecer teclas',(830,638,380,51),lambda:(self.save.data.update(key_bindings={}),self.save.write()),small=True)
    def school_settings(self):
        s=self.canvas;s.fill((13,27,37));text(s,'Herramientas del aula',(62,45),40,PAPER,True,serif=True)
        for i,(label,key) in enumerate((('Importar / exportar','files'),('Selección de temas','topics'),('PIN y privacidad','privacy'),('Guía docente','guide'))):
            self.button(label,(65+i*292,116,270,51),lambda k=key:setattr(self,'school_tab',k),primary=self.school_tab==key,small=True,arrow=False)
        if self.school_tab=='files':
            if sys.platform=='emscripten':
                text(s,'Elige un banco JSON con el selector de tu dispositivo',(65,200),23,PAPER,True)
                wrapped(s,'Revisar archivo abre tus documentos. Comprueba la vista previa antes de aplicar el banco.',(65,257),1110,21,CYAN)
            else:
                text(s,'Ruta de un banco JSON para revisar antes de aplicar',(65,200),23,PAPER,True)
                self.exchange_path.draw(s,(65,249,1145,56),'C:/carpeta/banco-preguntas.json',20)
            self.button('Revisar archivo',(65,337,350,55),self.preview_import,True,small=True)
            self.button('Aplicar vista previa',(437,337,400,55),self.apply_import,enabled=bool(self.exchange_preview),small=True)
            self.button('Exportar banco',(859,337,351,55),self.export_bank,small=True)
            if getattr(self,'shared_activity',None):
                self.button('Revisar banco de la sala',(65,425,490,55),self.preview_shared_bank,small=True)
            wrapped(s,self.exchange_message,(65,509),1110,20,GOLD,leading=30)
        elif self.school_tab=='topics':
            selected=set(self.school.config.get('topics',[]));self.topic_page=max(0,min(5,self.topic_page))
            text(s,'Sin selección se usan todos. La selección se aplica al entrar a otro mapa.',(65,194),18,GOLD)
            for i,topic in enumerate(range(self.topic_page*12,min(len(LESSONS),(self.topic_page+1)*12))):
                x=65+i%2*585;y=238+i//2*53
                self.button(('✓ ' if topic in selected else '○ ')+LESSONS[topic].title,(x,y,557,46),lambda n=topic:self.toggle_topic(n),primary=topic in selected,small=True,arrow=False,wrap=True)
            self.button('Anterior',(65,568,250,48),lambda:setattr(self,'topic_page',self.topic_page-1),enabled=self.topic_page>0,small=True)
            self.button('Siguiente',(335,568,250,48),lambda:setattr(self,'topic_page',self.topic_page+1),enabled=self.topic_page<5,small=True)
            self.button('Usar todos',(850,568,360,48),self.clear_topics,small=True)
        elif self.school_tab=='privacy':
            text(s,'Nuevo PIN (vacío lo desactiva)',(65,196),21,PAPER,True)
            self.pin_field.draw(s,(65,235,700,55),'Entre 4 y 64 caracteres',22)
            self.button('Guardar PIN',(790,235,420,55),self.apply_pin,small=True)
            wrapped(s,'Solo se guarda una derivación del PIN. Cada alumno usa un alias; no se necesitan nombres completos, correo ni cuentas en Internet. El ranking LAN comparte alias y puntajes con la sala local.',(65,332),1110,21,MUTED,leading=33)
            text(s,'Borrar el perfil actual y su progreso: escribe BORRAR',(65,472),21,GOLD,True)
            self.delete_field.draw(s,(65,514,700,55),'Confirmación',22)
            self.button('Eliminar perfil',(790,514,420,55),self.delete_confirmed,small=True)
            wrapped(s,self.exchange_message,(65,590),1110,17,GOLD)
        else:
            wrapped(s,'Sesión sugerida · 15–25 minutos',(65,196),1100,27,CYAN,True)
            rows=('1. Elegir alias, edad de preguntas y asistencia motriz. Presentar la época (3 min).',
                '2. Explorar una zona y recoger una curiosidad. Diferenciar evidencia y ficción (6 min).',
                '3. Resolver archivos y una actividad. Comparar la primera respuesta y las revisiones (6 min).',
                '4. Conversar sobre la fuente: quién la creó, qué permite saber y qué no demuestra (4 min).',
                '5. Exportar evidencia si hace falta y acordar una próxima pregunta (2 min).')
            for i,row in enumerate(rows):wrapped(s,row,(65,253+i*61),1110,20,PAPER,leading=28)
            wrapped(s,'El docente debe revisar adecuación curricular y formulaciones antes de usar una secuencia. Los rankings son un recurso opcional: acompaña la puntuación con conversación y progreso personal.',(65,571),1110,18,GOLD,leading=27)
        self.button('Volver al aula',(65,650,270,49),lambda:self.open_community('teacher'),True,small=True)
    def apply_pin(self):
        try:self.school.set_pin(self.pin_field.value);self.pin_field.set_value('');self.exchange_message='PIN actualizado.'
        except ValueError as error:self.exchange_message=str(error)
    def delete_confirmed(self):
        if self.delete_field.value!='BORRAR':self.exchange_message='Escribe BORRAR para confirmar.';return
        self.session_started=False
        self.school.delete(self.school.active['id']);self.activate_profile(self.school.data['active'])
        self.teacher_authenticated=False;self.delete_field.set_value('');self.set_state('menu')
    def preview_shared_bank(self):
        from .question_bank import validate_record
        try:
            records=[validate_record(r) for r in self.shared_activity['bank']]
            self.bank.validate_pools(records)
            if len({r['id'] for r in records})!=len(records):raise ValueError('IDs repetidos.')
            self.exchange_preview=records;self.exchange_message=f'Banco de sala revisado: {len(records)} preguntas. Puedes aplicarlo con respaldo.'
        except (ValueError,KeyError,TypeError) as error:self.exchange_message=str(error)
