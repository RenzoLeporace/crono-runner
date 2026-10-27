"""Large landscape entry menus for touch screens; shares the campaign state."""
import pygame as pg
from .art import text,tracked,rect,line,PAPER,CYAN,GOLD,MUTED
from .campaign import CHAPTER_ORDER,ERA_LABELS,chapter_levels,level_label
from .education import STAGES
from .learning_ui import wrapped
from .child_ui import ChildUI

class MobileUI(ChildUI):
    def mobile_menu(self):
        return self.child_menu()

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
        self.button('Volver',(65,613,555,87),self.go_back,True)
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
        self.button('Música y sonidos',(650,539,555,83),lambda:self.set_state('sound_settings'))
        self.button('Volver',(65,640,1140,63),self.close_settings,True)
