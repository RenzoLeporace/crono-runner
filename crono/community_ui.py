"""Profiles, local classrooms and LAN room controls, shared with touch menus."""
from pathlib import Path
import pygame as pg
from .school import School,rankings,atomic_json
from .rooms import Room,RoomClient,local_addresses
from .text_field import TextField
from .art import text,rect,line,tracked,PAPER,CYAN,GOLD,MUTED
from .learning_ui import wrapped

class CommunityUI:
    def init_community(self,save_file=None):
        self.school=School(Path(save_file).parent if save_file else None)
        if save_file is None:self.save=self.school.select(self.school.data['active'])
        self.community_fields=[TextField('',64) for _ in range(6)]
        self.community_mode='profiles';self.community_message='';self.teacher_authenticated=False
        self.community_page=0;self.rank_mode='class';self.room=None;self.room_client=None
        self.room_rankings=None;self.room_future=None;self.room_pool=None
        self.room_job_profile=None
        self.room_topics=None;self.room_bank=None;self.shared_activity=None
        self.community_return='menu';self.pending_teacher=None
        session=self.save.data.get('session_room')
        if isinstance(session,dict) and isinstance(session.get('address'),str) and isinstance(session.get('token'),str):
            try:self.room_client=RoomClient(session['address'],session['token'])
            except ValueError:pass

    def open_community(self,mode='profiles'):
        if self.state not in ('community','profile_create','room_join','teacher_access'):
            self.community_return=self.state
        self.community_mode=mode;self.community_message='';self.community_page=0
        self.set_state('community')

    def open_form(self,state,action=None):
        self.pending_teacher=action
        for field in self.community_fields:field.set_value('');field.focused=False
        self.community_fields[0].focused=True
        self.set_state(state);pg.key.start_text_input();pg.key.set_repeat(350,35)

    def need_teacher(self,action):
        if self.teacher_authenticated or not self.school.config.get('pin'):
            self.teacher_authenticated=True;action()
        else:self.open_form('teacher_access',action)

    def select_profile(self,key):
        target=next(p for p in self.school.data['profiles'] if p['id']==key)
        def select():
            self.activate_profile(key)
            self.teacher_authenticated=target.get('role')=='teacher'
            self.set_state('menu')
        if target.get('role')=='teacher':self.need_teacher(select)
        else:self.teacher_authenticated=False;select()

    def activate_profile(self,key):
        from .physics import World
        if getattr(self,'session_started',False) and not self.world.complete:self.save.capture(self.world)
        self.save=self.school.select(key);self.audio.enabled=self.save.data['sound']
        self.world=World(0,0,self.save.effective_upgrades(),self.save.data['solved'],self.save.combat_band())
        self.world.player.skin=self.save.data['skin']
        self.session_started=False;self.camera=0.;self.particles=[];self.rift_return_memory=None
        self.room_client=None;self.room_rankings=None;self.question_history={}
        self.room_bank=None;self.room_topics=None;self.shared_activity=None
        session=self.save.data.get('session_room')
        if isinstance(session,dict):
            try:self.room_client=RoomClient(session['address'],session['token'])
            except (KeyError,ValueError,TypeError):pass

    def toggle_practice(self):
        entering=not self.save.data['practice']
        if entering:
            if getattr(self,'session_started',False):self.save.capture(self.world)
            self.practice_skin=self.save.data['skin']
        self.save.data['practice']=not self.save.data['practice'];self.save.write()
        if not entering:
            from .skins import available
            if not available(self.save,self.save.data['skin']):self.save.data['skin']=getattr(self,'practice_skin','crono')
            if not self.save.can_enter(self.world.level_id):
                self.load(*divmod(self.save.data['current'],3),restore=True)
            else:self.load(self.world.index,self.world.stage,restore=True)
        else:self.load(self.world.index,self.world.stage)
        self.set_state('pause');self.settings_return='pause'

    def start_room(self):
        from .mobile import bridge
        if bridge():
            self.community_message='Abre la sala en una PC docente y únete desde este dispositivo.';return
        try:
            if self.room:self.room.stop()
            self.room=Room(self.school.root/'salas'/'resultados.json',self.bank.records,self.school.config.get('topics',[]))
            port=self.room.start()
            self.community_message=f'Sala abierta · {", ".join(local_addresses())}:{port} · código {self.room.code}'
        except OSError as error:self.community_message=f'No se pudo abrir el puerto 8765: {error}'

    def room_task(self,fn):
        if self.room_future and not self.room_future.done():return
        try:from concurrent.futures import ThreadPoolExecutor
        except ImportError:
            self.community_message='Las salas móviles se conectan desde la aplicación Android instalada.';return
        if self.room_pool is None:self.room_pool=ThreadPoolExecutor(max_workers=1,thread_name_prefix='Crono LAN')
        self.room_job_profile=self.school.data['active']
        self.room_future=self.room_pool.submit(fn);self.community_message='Conectando con la sala…'

    def poll_room(self):
        if not self.room_future or not self.room_future.done():return
        future=self.room_future;self.room_future=None
        if self.room_job_profile!=self.school.data['active']:return
        try:
            result=future.result()
            if isinstance(result,dict) and 'joined_client' in result:
                self.room_client=result['joined_client'];self.shared_activity=result['activity']
                self.save.data['session_room']=dict(address=self.room_client.address,token=self.room_client.token);self.save.write()
                self.apply_room_activity(result['activity'])
                result=result['rankings']
            if isinstance(result,dict) and 'activity_update' in result:
                self.apply_room_activity(result['activity_update']);result=result.get('rankings',{})
            if isinstance(result,dict) and 'classroom' in result:self.room_rankings=result
            self.community_message='Sala actualizada. Los resultados docentes de prueba quedan fuera del ranking.'
        except Exception as error:self.community_message='Sin conexión: '+str(error)[:130]+'. Puedes seguir jugando sin red.'

    def sync_room(self):
        if not self.room_client:return
        from copy import deepcopy
        records=deepcopy(self.save.data['records']);practice=self.save.data['practice'];client=self.room_client
        from .mobile import bridge,NetworkFuture
        if bridge():
            if self.room_future and not self.room_future.done():return
            self.room_job_profile=self.school.data['active'];self.room_future=NetworkFuture(client,'sync',records=records,practice=practice)
            return
        def sync():
            client.call('/results',records=records,practice=practice)
            return dict(activity_update=client.call('/activity'),rankings=client.call('/rankings'))
        self.room_task(sync)

    def apply_room_activity(self,activity):
        from .question_bank import validate_record,QuestionBank
        if not isinstance(activity,dict):return
        topics=activity.get('topics',[])
        self.room_topics=sorted({i for i in topics if type(i) is int and 0<=i<72}) if isinstance(topics,list) else []
        try:
            records=[validate_record(r) for r in activity.get('bank',[])]
            QuestionBank.validate_pools(records)
            if len(records)>10000 or len({r['id'] for r in records})!=len(records):raise ValueError('IDs de sala repetidos.')
            self.room_bank=QuestionBank(self.school.root/'banco-sala-no-persistido.json');self.room_bank.records=records
        except (ValueError,TypeError):self.room_bank=None
        self.shared_activity=activity

    def learning_bank(self):return (getattr(self,'room_bank',None) if self.room_client is not None else None) or self.bank

    def submit_form(self):
        values=[f.value.strip() for f in self.community_fields]
        try:
            if self.state=='profile_create':
                role='teacher' if self.community_mode=='teacher' else 'student'
                self.school.create(values[0],values[1],values[2],role);self.activate_profile(self.school.data['active'])
                self.teacher_authenticated=role=='teacher';self.set_state('menu')
            elif self.state=='teacher_access':
                if not self.school.check_pin(values[0]):raise ValueError('PIN incorrecto.')
                self.teacher_authenticated=True
                action=self.pending_teacher;self.pending_teacher=None
                self.set_state('community')
                if action:action()
            elif self.state=='room_join':
                profile=dict(self.school.active);address,code=values[0],values[1]
                session=self.save.data.get('session_room') or {}
                client=RoomClient(address)
                if client.address==session.get('address'):client.token=session.get('token')
                from .mobile import bridge,NetworkFuture
                if bridge():
                    if self.room_future and not self.room_future.done():return
                    self.room_job_profile=self.school.data['active']
                    self.room_future=NetworkFuture(client,'join',code=code,profile=profile)
                    self.set_state('community');self.community_mode='rooms';return
                def join():
                    result=client.call('/join',code=code,alias=profile['alias'],classroom=profile.get('classroom',''),institution=profile.get('institution',''),role=profile.get('role','student'))
                    return dict(joined_client=client,activity=result,rankings=client.call('/rankings'))
                self.room_task(join);self.set_state('community');self.community_mode='rooms'
        except (OSError,ValueError) as error:self.community_message=str(error)

    def handle_community_event(self,event):
        if self.state not in ('profile_create','room_join','teacher_access'):return False
        count=3 if self.state=='profile_create' else 2 if self.state=='room_join' else 1
        fields=self.community_fields[:count]
        if event.type==pg.KEYDOWN and event.key==pg.K_ESCAPE:self.set_state('community');return True
        if event.type==pg.KEYDOWN and event.key==pg.K_TAB:
            index=next((i for i,f in enumerate(fields) if f.focused),-1)
            for f in fields:f.focused=False
            fields[(index+1)%count].focused=True;return True
        if event.type==pg.KEYDOWN and event.key==pg.K_RETURN:self.submit_form();return True
        if event.type in (pg.MOUSEBUTTONDOWN,pg.MOUSEBUTTONUP,pg.MOUSEMOTION):
            event=pg.event.Event(event.type,dict(event.dict,pos=self.logical_mouse(event.pos)))
            if event.type==pg.MOUSEBUTTONDOWN:
                for f in fields:f.focused=f.box.collidepoint(event.pos)
        return any(f.handle(event) for f in fields)

    def community_form(self):
        self.canvas.fill((13,27,37));s=self.canvas
        titles=dict(profile_create='Un perfil, un viaje',room_join='Entrar a una sala de la red',teacher_access='Acceso docente')
        self.community_fields[0].password=self.state=='teacher_access'
        text(s,titles[self.state],(66,65),40,PAPER,True,serif=True)
        labels=('Alias (sin nombre completo)','Clase','Institución') if self.state=='profile_create' else ('IP del docente : puerto (ej. 192.168.1.10:8765)','Código de sala') if self.state=='room_join' else ('PIN docente (vacío si todavía no configuraste uno)',)
        for i,label in enumerate(labels):
            y=180+i*106;text(s,label,(66,y),18,CYAN,True)
            self.community_fields[i].draw(s,(66,y+30,1110,57),'Escribir…',22)
        self.button('Continuar',(66,560,300,58),self.submit_form,True)
        self.button('Cancelar',(390,560,230,58),lambda:self.set_state('community'))
        wrapped(s,self.community_message,(66,645),1100,17,GOLD)

    def community(self):
        self.poll_room();s=self.canvas;s.fill((13,27,37))
        profile=self.school.active
        tracked(s,'AULA · DATOS GUARDADOS EN ESTE EQUIPO',(65,25),12,CYAN,2)
        text(s,profile['alias']+' · '+profile.get('classroom',''),(62,60),33,PAPER,True)
        for i,(label,mode) in enumerate((('Perfiles','profiles'),('Ranking de clase','class'),('De institución','institution'),('Salas LAN / WiFi','rooms'),('Docentes','teacher'))):
            self.button(label,(65+i*234,119,221,49),lambda m=mode:setattr(self,'community_mode',m),primary=self.community_mode==mode,small=True,arrow=False)
        mode=self.community_mode
        if mode=='profiles':
            profiles=self.school.data['profiles'];pages=max(1,(len(profiles)+4)//5);self.community_page=max(0,min(pages-1,self.community_page))
            for i,p in enumerate(profiles[self.community_page*5:self.community_page*5+5]):
                self.button(p['alias']+' · '+p.get('classroom','')+(' · docente' if p.get('role')=='teacher' else ''),(65,193+i*65,750,54),lambda k=p['id']:self.select_profile(k),small=True)
            self.button('+ Alumno',(850,193,360,54),lambda:(setattr(self,'community_mode','profiles'),self.open_form('profile_create')),True)
            self.button('Anterior',(850,264,170,48),lambda:setattr(self,'community_page',self.community_page-1),enabled=self.community_page>0,small=True)
            self.button('Siguiente',(1034,264,176,48),lambda:setattr(self,'community_page',self.community_page+1),enabled=self.community_page<pages-1,small=True)
            wrapped(s,'Usa alias. Cada perfil conserva su propio progreso. Los informes se exportan únicamente cuando tú lo eliges.',(850,347),350,20,MUTED)
        elif mode in ('class','institution'):
            if self.room:
                from copy import deepcopy
                with self.room.lock:members=deepcopy(list(self.room.members.values()))
                rows=rankings(members,profile.get('classroom') if mode=='class' else None,profile.get('institution'))
            else:rows=self.room_rankings.get('classroom' if mode=='class' else 'institution',[]) if self.room_rankings else rankings(self.school.rows(),profile.get('classroom') if mode=='class' else None,profile.get('institution'))
            text(s,'MEJORES PUNTUACIONES POR MAPA · SIN PARTIDAS DE PRUEBA',(65,190),15,GOLD,True)
            for i,row in enumerate(rows[self.community_page*7:self.community_page*7+7]):
                y=232+i*44;text(s,f'{self.community_page*7+i+1:02d}  {row["alias"]}',(65,y),21,PAPER,True)
                text(s,row['classroom'],(540,y),18,MUTED)
                text(s,f'{row["maps"]} mapas · {row["score"]:,} puntos',(1208,y),21,CYAN,True,'topright')
            self.button('Anterior',(65,560,180,48),lambda:setattr(self,'community_page',max(0,self.community_page-1)),small=True)
            self.button('Siguiente',(263,560,190,48),lambda:setattr(self,'community_page',self.community_page+1),enabled=(self.community_page+1)*7<len(rows),small=True)
            self.button('Actualizar sala',(850,560,360,48),self.sync_room,enabled=self.room_client is not None,small=True)
        elif mode=='rooms':
            wrapped(s,'El docente abre una sala en su computadora. Los alumnos se conectan desde la misma red local o WiFi con su IP y el código. No hace falta Internet.',(65,193),1100,23,PAPER,leading=34)
            self.button('Crear sala docente',(65,326,350,58),lambda:self.need_teacher(self.start_room),True)
            self.button('Unirme con IP y código',(437,326,380,58),lambda:self.open_form('room_join'))
            self.button('Enviar resultados',(839,326,371,58),self.sync_room,enabled=self.room_client is not None)
            if self.room:
                wrapped(s,f'Sala abierta: {", ".join(local_addresses())}:{self.room.server.server_port if self.room.server else 8765} · Código {self.room.code}',(65,421),1100,26,CYAN,True)
                self.button('Cerrar sala',(65,505,350,50),lambda:(self.room.stop(),setattr(self,'room',None)),small=True)
            wrapped(s,'Si el sistema pide acceso a la red, permite solo tu red privada. La conexión comparte alias, clase, institución y mejores puntajes; el progreso individual sigue en el dispositivo.',(437,469),750,18,MUTED)
        elif mode=='teacher':
            if not self.teacher_authenticated:
                wrapped(s,'Puedes proteger la zona docente con un PIN local. Al habilitar pruebas se desbloquea todo y los resultados quedan separados.',(65,200),1080,23,PAPER)
                self.button('Entrar como docente',(65,352,400,59),lambda:self.need_teacher(lambda:None),True)
            else:
                self.button('+ Perfil docente',(65,195,350,54),lambda:self.open_form('profile_create'),small=True)
                self.button('Todo desbloqueado: '+('SÍ' if self.save.data['practice'] else 'NO'),(435,195,400,54),self.toggle_practice,True,small=True)
                self.button('Exportar evidencia CSV',(855,195,355,54),self.export_student_evidence,small=True)
                self.button('Preguntas y respuestas',(65,270,350,54),lambda:self.set_state('teacher'),small=True)
                self.button('Ajustes de aula / banco',(435,270,400,54),lambda:self.set_state('school_settings'),small=True)
                self.button('Eliminar este progreso',(855,270,355,54),lambda:self.open_delete_profile(),small=True)
                wrapped(s,'Los datos se guardan aquí. El PIN limita acceso en los menús; una persona con acceso a los archivos del equipo puede modificarlos. Usa alias y exporta solo lo necesario.',(65,380),1100,21,MUTED)
        self.button('Volver',(65,639,220,50),lambda:self.set_state(self.community_return),True,small=True)
        wrapped(s,self.community_message,(320,631),890,17,GOLD,leading=23)

    def export_student_evidence(self):
        try:
            target=self.school.root/'informes'/f'intentos-{self.school.active["id"]}.csv'
            self.save.export_evidence(target,self.school.active);self.community_message='Informe creado: '+str(target)
            from .mobile import export_document
            if export_document(target,lambda r:setattr(self,'community_message','Informe exportado.' if r.get('saved') else 'Exportación cancelada.')):self.community_message='Elige dónde guardar el informe en Android.'
        except OSError:self.community_message='No se pudo escribir el informe.'
    def open_delete_profile(self):
        self.community_message='Para borrar, escribe BORRAR en el campo de confirmación de ajustes de aula.'
        self.set_state('school_settings')
