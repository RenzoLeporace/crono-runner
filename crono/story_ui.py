"""Playable onboarding, mandatory historical objectives and expansion entry."""
from .art import text,rect,PAPER,CYAN,GOLD,MUTED
from .learning_ui import wrapped

TUTORIAL=('Camina hacia la primera señal: usa la cruceta o A/D.',
          'Salta sobre el primer desnivel: toca salto o Espacio.',
          'Prueba el impulso: toca el botón de la flecha o Shift.',
          'Dispara un pulso corto: toca el objetivo o F.',
          'Acércate al archivo luminoso, usa E o la mano y resuelve su pregunta.')

class StoryUI:
    def init_story(self):
        self.tutorial_active=False;self.tutorial_step=0;self.workshop_page=0;self.skin_page=0
        self.sea_origin=None;self.voyage=None

    def start_tutorial(self):
        self.load(0);self.begin();self.tutorial_active=True;self.tutorial_step=0

    def tutorial_progress(self,events):
        if not self.tutorial_active:return
        step=self.tutorial_step
        passed=(self.world.player.rect.x>self.world.data['spawn'][0]+85 if step==0 else
                'jump' in events if step==1 else 'dash' in events if step==2 else
                'shot' in events if step==3 else bool({0,1}&self.world.answered))
        if passed:
            self.tutorial_step+=1;self.audio.play('checkpoint')
            if self.tutorial_step==5:
                self.tutorial_active=False;self.save.data['tutorial_done']=True;self.save.write()
                self.world.say('¡Ya sabes explorar! Ahora completa la misión del mapa. H abre tu historia.')

    def story_hud(self):
        w=self.world;m=w.mechanic
        if self.tutorial_active:
            rect(self.canvas,(16,39,46),(245,204,790,70),8)
            wrapped(self.canvas,f'TUTORIAL {self.tutorial_step+1}/5 · '+TUTORIAL[self.tutorial_step],(265,217),750,18,CYAN,leading=25)
        else:
            learned=bool({w.level_id*2,w.level_id*2+1}&w.answered)
            self.button(('✓' if w.story_ready else 'H')+' · Historia',(565,665,205,42),lambda:self.set_state('story'),small=True,arrow=False)
            if not (w.boss and w.boss.active and w.boss.alive):
                text(self.canvas,f'Historia: {m.state["step"]}/3 puestos · aplicación '+('✓' if m.field.done else 'pendiente')+' · archivo '+('✓' if learned else 'pendiente'),(36,111),14,CYAN if w.story_ready else GOLD)

    def story_panel(self):
        s=self.canvas;s.fill((13,28,38));w=self.world;m=w.mechanic
        text(s,'Tu misión en esta historia',(62,35),40,PAPER,True,serif=True)
        text(s,w.data['meta'].name,(65,106),26,GOLD,True)
        wrapped(s,m.note,(65,164),1120,self.save.data['reading_size']+2,PAPER,leading=32)
        learned=bool({w.level_id*2,w.level_id*2+1}&w.answered)
        rows=[(len(w.shards)==3,f'Recuperar los tres fragmentos · {len(w.shards)}/3'),
              (learned,'Comprender al menos un archivo de este mapa'),
              (m.state['step']>=3,'Aplicar las tres decisiones: '+m.title),
              (m.field.done,m.field.description()),
              (not w.boss or not w.boss.alive,'Liberar al guardián' if w.boss else 'Alcanzar el portal de regreso')]
        for i,(done,label) in enumerate(rows):
            rect(s,(22,43,50),(65,289+i*53,1140,45),5)
            wrapped(s,('HECHO · ' if done else 'PENDIENTE · ')+label,(82,298+i*53),1100,18,CYAN if done else PAPER)
        text(s,'Las respuestas dan saber para habilidades; la misión abre el portal. Los errores tienen pistas, no castigos.',(65,580),16,GOLD)
        self.button('Seguir mi historia',(65,632,350,60),lambda:self.set_state('play'),True)
        self.button('Ver lugares en el plano',(445,632,350,60),self.open_atlas,small=True)

    def dlc_menu(self):
        s=self.canvas;s.fill((13,28,38));text(s,'Historias de nuestros países',(62,54),43,PAPER,True,serif=True)
        rect(s,(29,65,77),(65,172,555,380),12);rect(s,(38,70,50),(650,172,555,380),12)
        for y,col in ((202,(127,203,225)),(258,(236,232,209)),(314,(127,203,225))):rect(s,col,(95,y,240,55))
        from .art import polygon,circle
        rect(s,(50,118,64),(680,202,240,167));polygon(s,(231,188,76),[(800,214),(901,285),(800,353),(697,285)]);circle(s,(42,75,124),(800,285),37)
        text(s,'Argentina',(95,397),32,PAPER,True)
        text(s,'Brasil',(680,397),32,PAPER,True)
        wrapped(s,'Cuatro mapas históricos y excursiones por descubrir.',(95,449),480,22,CYAN)
        wrapped(s,'Próximo DLC · el menú está preparado. Sus mapas se incorporarán más adelante.',(680,449),480,22,GOLD)
        self.button('Entrar a Argentina',(95,572,495,72),self.continue_dlc,True)
        self.button('Brasil · próximamente',(680,572,495,72),lambda:None,enabled=False)
        self.button('Volver',(65,659,250,45),lambda:self.set_state('menu'),small=True)
