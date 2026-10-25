"""Pauseable route overview for long maps, with all branch geometry visible."""
from .art import rect,line,circle,diamond,text,tracked,PAPER,MUTED,CYAN,GOLD,W
from .campaign import DIFFICULTIES

class AtlasUI:
    def open_atlas(self):
        self.atlas_return=self.state
        self.set_state('atlas')

    def atlas(self):
        s=self.canvas;w=self.world
        self.artist.scene(s,w,self.camera,self.time)
        self.dim(238)
        tracked(s,'EXPLORA · EL TIEMPO ESTÁ EN PAUSA',(60,36),11,CYAN,3)
        text(s,w.data['meta'].name,(57,75),37,PAPER,True,serif=True)
        text(s,f'Tres zonas conectadas · {DIFFICULTIES[w.difficulty]}',(60,132),16,GOLD)
        text(s,'Cada línea es una superficie real. Las galerías superiores tienen entradas y retornos.',(60,178),17,MUTED)
        scale=1140/w.width
        def point(x,y):return (60+x*scale,262+(y-130)*.57)
        for p in w.platforms:
            if not p.active:continue
            x,y=point(p.rect.x,p.rect.y)
            line(s,(67,100,114) if p.oneway else (157,184,184),(x,y),(x+max(3,p.rect.w*scale),y),3 if p.oneway else 5)
        for n,(x,y) in enumerate(w.data['shards']):diamond(s,point(x,y-16),8,CYAN if n in w.shards else GOLD,n in w.shards)
        for x,y,topic in w.data['stations']:
            px,py=point(x,y-65);rect(s,CYAN,(px-4,py-4,8,8))
        for i in w.checkpoint_ids:
            x,y=w.data['checkpoints'][i];circle(s,(180,185,210),point(x,y-20),3)
        for x,name in w.data['zones']:
            px,_=point(x,0)
            text(s,name,(px,231),13,GOLD,True)
        circle(s,PAPER,point(w.player.rect.centerx,w.player.rect.bottom-25),6)
        x,y=point(*w.data['portal']);circle(s,CYAN,(x,y-12),9,2)
        text(s,'Blanco: Crono    Dorado: fragmento pendiente    Turquesa: archivo y portal    Gris: ancla',(60,591),16,PAPER)
        self.button('Volver al viaje',(60,642,270,47),lambda:self.set_state(self.atlas_return),True,small=True)
        text(s,'V abre el plano · S / abajo permite bajar por las pasarelas.',(1210,665),13,MUTED,False,'midright')
