"""Large landscape entry menus for touch screens; shares the campaign state."""
from .art import text,tracked,rect,line,PAPER,CYAN,GOLD,MUTED
from .campaign import CHAPTER_ORDER,ERA_LABELS,chapter_levels,level_label
from .education import STAGES
from .learning_ui import wrapped

class MobileUI:
    def mobile_menu(self):
        s=self.canvas;self.artist.background(s,8,0,self.time,0);self.dim(180)
        tracked(s,'ECOS DEL TIEMPO',(65,38),15,CYAN,4)
        text(s,'CRONO',(60,77),84,PAPER,True,serif=True)
        text(s,self.school.active['alias'],(1205,66),25,GOLD,True,'topright')
        text(s,'© 2026 Renzo Leporace',(1205,111),18,MUTED,False,'topright')
        if self.save.data['practice']:text(s,'PRUEBA DOCENTE · TODO DESBLOQUEADO · SIN RANKING',(65,181),18,GOLD,True)
        started=self.save.data['started']
        actions=(('Continuar el viaje' if started else 'Comenzar el viaje',self.continue_game if started else lambda:self.load(0)),
            ('Argentina',self.continue_dlc),('Épocas y rutas',lambda:self.set_state('chapters')),('Perfiles y aula',self.open_community),
            ('Logros y apariencias',self.open_rewards),('Configuración',self.open_settings),('Créditos',lambda:self.set_state('credits')),('Salir',lambda:setattr(self,'running',False)))
        for i,(label,action) in enumerate(actions):
            self.button(label,(65+i%2*585,220+i//2*116,555,98),action,primary=i==0,arrow=True)

    def mobile_chapters(self):
        s=self.canvas;s.fill((13,27,37));era=self.chapter_era
        if era not in CHAPTER_ORDER:era=7 if self.world.level_id==27 else 9
        position=CHAPTER_ORDER.index(era)
        text(s,'Explora el tiempo',(62,30),39,PAPER,True,serif=True)
        self.button('‹ Época',(65,106,260,88),lambda:setattr(self,'chapter_era',CHAPTER_ORDER[(position-1)%len(CHAPTER_ORDER)]),small=True)
        text(s,ERA_LABELS[era],(640,142),29,CYAN,True,'center')
        self.button('Época ›',(950,106,260,88),lambda:setattr(self,'chapter_era',CHAPTER_ORDER[(position+1)%len(CHAPTER_ORDER)]),small=True)
        for i,level in enumerate(chapter_levels(era)):
            meta=STAGES[level];x=65+i%2*585;y=225+i//2*184
            available=self.save.can_enter(level)
            self.button('',(x,y,555,162),lambda n=level:self.load(*divmod(n,3),restore=True),enabled=available,primary=available,arrow=False)
            color=(18,43,48) if available else MUTED
            text(s,level_label(level)+(' · ENTRAR' if available else ' · POR DESCUBRIR'),(x+22,y+16),19,color,True)
            wrapped(s,meta.name,(x+22,y+60),510,26,color,True,leading=34)
        self.button('Volver al inicio',(65,613,555,87),lambda:self.set_state('menu'),True)
        self.button('Rescates y logros',(650,613,555,87),self.open_rewards)

    def mobile_settings(self):
        s=self.canvas;s.fill((13,27,37));text(s,'Configura tu viaje',(62,30),41,PAPER,True,serif=True)
        text(s,'Preguntas por edad',(65,109),24,CYAN,True)
        for i,label in enumerate(('6–9 años','10–14 años','15+ años')):
            self.button(label,(65+i*390,155,365,82),lambda b=i:self.set_age(b),primary=self.save.data['age_band']==i,arrow=False)
        text(s,'Dificultad de movimiento y combate',(65,267),23,CYAN,True)
        for i,label in enumerate(('Mínima','Media','Alta')):
            self.button(label,(65+i*390,310,365,82),lambda b=i:self.set_motor(b),primary=self.save.combat_band()==i,arrow=False)
        self.button('Lectura y controles',(65,435,555,83),lambda:self.set_state('accessibility'))
        self.button('Cuaderno de campo',(650,435,555,83),lambda:self.open_panel('notebook'))
        self.button('Aula y docentes',(65,539,555,83),lambda:self.open_community('teacher'))
        self.button('Sonido: '+('SÍ' if self.audio.enabled else 'NO'),(650,539,555,83),self.toggle_sound)
        self.button('Volver',(65,640,1140,63),self.close_settings,True)
