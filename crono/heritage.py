"""Optional cultural stops: original illustrations, no combat or required belief."""
from functools import lru_cache
import math
import webbrowser
import pygame as pg
from .argentina_art import Painter
from .art import text,rect,line,glow,PAPER,MUTED,GOLD,CYAN,W

ENTRIES={
 'lujan':dict(title='Nuestra Señora de Luján',subtitle='Argentina · patrimonio religioso y cultural',
    body='La devoción a la Virgen de Luján se vincula con una imagen llegada desde Brasil en 1630. La tradición de la carreta relata que la imagen permaneció junto al río Luján. Es patrona de la Argentina y forma parte de su historia religiosa, artística y de peregrinaciones.\n\nEsta hornacina es una ilustración del juego: no sitúa la basílica actual en el Buenos Aires de 1810. El manto celeste, las manos unidas y la corona distinguen esta representación.',
    source='Santuario de Luján · Historia',url='https://santuariodelujan.org.ar/historia/'),
 'itati':dict(title='Nuestra Señora de Itatí',subtitle='Corrientes · devoción y encuentro junto al Paraná',
    body='La Virgen de Itatí es patrona de Corrientes. Su devoción está ligada a la localidad de Itatí, fundada en 1615 junto al Paraná. Su imagen y las peregrinaciones tienen un lugar destacado en la cultura religiosa del nordeste argentino.\n\nEsta representación lleva manto azul, túnica clara, corona y manos unidas. Es una referencia cultural traída por el reloj; no significa que Itatí se encuentre en Tucumán o en Buenos Aires. Su basílica actual es del siglo XX.',
    source='Argentina · Basílica de Itatí',url='https://www.argentina.gob.ar/viaja-por-argentina/que-hacer/visitar-la-basilica-de-la-virgen-de-itati'),
 'moses':dict(title='Moisés y la memoria del Éxodo',subtitle='Tradición bíblica · una referencia cultural',
    body='En la tradición bíblica, Moisés guía la salida de los israelitas de Egipto. La apertura del mar es uno de los episodios del Éxodo representados a lo largo de los siglos en el arte religioso.\n\nEl reloj proyecta aquí una ilustración de ese relato. No es una inscripción egipcia auténtica ni una escena fechada por la arqueología. Las pirámides de Guiza y los templos del Reino Nuevo corresponden a períodos distintos; este recorrido no identifica al faraón del Éxodo con un gobernante concreto.',
    source='British Museum · El paso del mar en el arte',url='https://www.britishmuseum.org/collection/object/P_1875-0710-270'),
}

@lru_cache(maxsize=3)
def illustration(key):
    p=Painter(360,350)
    if key=='moses':
        p.r((24,58,79),(10,10,340,328),12)
        for side in (-1,1):
            x=180+side*135
            p.p((49,136,160),[(x-side*40,303),(x+side*38,303),(x+side*38,45),(x+side*6,68),(x-side*14,134),(x-side*43,203)])
            for yy in (87,127,167,207,247):
                p.a((117,202,205),(x-34,yy,65,47),.2,2.7,3)
        p.p((194,164,115),[(131,315),(230,315),(190,158),(170,158)])
        # Elder figure with a staff; an artistic reference, not an enemy sprite.
        p.p((154,85,57),[(162,204),(197,204),(211,290),(151,290)])
        p.p((220,197,150),[(168,203),(184,215),(191,290),(165,290)])
        p.e((182,137,98),(164,172,31,35));p.e((206,203,186),(162,165,34,23))
        p.p((220,217,200),[(165,191),(195,191),(182,222),(171,213)])
        p.l((192,144,100),(191,215),(216,178),9)
        p.l((119,84,53),(223,140),(223,289),5);p.a((119,84,53),(218,133,17,20),0,3.4,4)
        for n in range(7):
            x=138+n*13;y=240+(n%3)*15
            p.c((179,138,97),(x,y),4);p.p((100+n*9,103,99),[(x-4,y+4),(x+4,y+4),(x+7,y+26),(x-7,y+26)])
        p.label('EL RELATO DEL ÉXODO',61,317,13,(230,213,172))
    else:
        dark=(43,67,80) if key=='lujan' else (34,50,84)
        blue=(109,175,201) if key=='lujan' else (48,86,145)
        gold=(215,176,92);white=(236,221,180)
        # A carved niche with scalloped arch, painted tiles and votive flowers.
        p.r((98,79,64),(34,18,292,312),18);p.r((205,179,134),(41,23,278,301),16)
        p.e((154,127,88),(55,33,250,252));p.r((154,127,88),(55,152,250,160))
        p.e(dark,(65,44,230,230));p.r(dark,(65,151,230,149))
        for n in range(12):
            a=n*math.tau/12;x=180+math.cos(a)*57;y=101+math.sin(a)*57
            p.c(gold,(x,y),2)
        # Crown and aureole.
        p.e(gold,(159,53,43,55),2)
        p.p(gold,[(161,78),(157,62),(167,68),(172,55),(181,67),(190,55),(193,69),(204,62),(198,80)])
        p.r(gold,(160,77,40,7),2);p.c((224,214,167),(181,52),3)
        p.l(gold,(181,42),(181,51),2);p.l(gold,(177,45),(185,45),2)
        p.e((180,133,96),(165,86,32,40))
        p.p(white,[(159,89),(165,83),(194,84),(204,104),(194,120),(190,92),(174,91),(168,116),(157,111)])
        p.l((84,61,51),(175,101),(179,101),1);p.l((84,61,51),(187,101),(190,101),1)
        p.l((127,83,63),(181,110),(187,112),1)
        # Wide embroidered mantle; Itatí and Luján keep distinct outline/color.
        shoulder=143 if key=='lujan' else 135
        p.p(blue,[(162,115),(shoulder,135),(103,270),(257,270),(360-shoulder,135),(197,115)])
        p.p(white,[(171,120),(190,120),(212,269),(149,269)])
        p.p(gold,[(162,115),(shoulder,135),(103,270),(112,270),(shoulder+6,137),(167,120)],1)
        p.p(gold,[(197,115),(360-shoulder,135),(257,270),(248,270),(354-shoulder,137),(192,120)],1)
        for yy in range(150,262,23):
            for xx in (143-(yy-150)*.2,218+(yy-150)*.2):
                p.l(gold,(xx-3,yy),(xx+3,yy),1);p.l(gold,(xx,yy-3),(xx,yy+3),1)
        for x in (158,180,201):p.l((187,174,141),(180+(x-180)*.25,175),(x,260),1)
        p.l((185,139,99),(163,146),(179,160),7);p.l((185,139,99),(198,146),(183,160),7)
        p.l((227,190,142),(178,159),(181,140),5);p.l((227,190,142),(183,159),(181,140),5)
        # Crescent, pedestal, flowers and candles.
        p.a(gold,(142,254,78,33),3.2,6.1,4)
        p.r((169,131,78),(126,281,110,9),3);p.r((115,89,64),(117,290,127,14),3)
        for x in (83,274):
            p.r((202,165,104),(x,284,5,18),1);p.e((246,191,92),(x,275,5,10))
            for j in range(4):
                yy=277-j*7;p.l((94,128,76),(x+13,299),(x+10+j*3,yy),1)
                p.c((181+j*12,114+j*15,119),(x+10+j*3,yy),3)
        p.label('LUJÁN' if key=='lujan' else 'ITATÍ',145,308,16,(71,65,57))
    return p.image()

def near_site(world):
    p=world.player.rect
    return next((site for site in world.data.get('cultural_sites',())
                 if abs(p.centerx-site[0])<83 and abs(p.bottom-site[1])<83),None)

def draw_sites(s,world,camera,t):
    for wx,wy,key in world.data.get('cultural_sites',()):
        x=wx-camera
        if not -140<x<W+140:continue
        img=pg.transform.smoothscale(illustration(key),(139,135))
        s.blit(img,(int(x-69),int(wy-136)))
        rect(s,(83,73,61),(x-64,wy-6,128,6),2)
        if abs(world.player.rect.centerx-wx)<240:
            title='MOISÉS · TRADICIÓN BÍBLICA' if key=='moses' else 'VIRGEN DE '+('LUJÁN' if key=='lujan' else 'ITATÍ')
            text(s,title,(x,wy-160),10,GOLD,True,'center')

def panel(game):
    from .learning_ui import wrapped
    s=game.canvas;game.educational_background()
    item=ENTRIES[game.heritage_key]
    text(s,'PATRIMONIO Y TRADICIONES',(65,32),13,CYAN,True)
    text(s,item['title'],(62,68),38,PAPER,True,serif=True)
    text(s,item['subtitle'],(65,123),16,GOLD)
    for n,key in enumerate(ENTRIES):
        game.button(('Luján','Itatí','Moisés')[n],(65+n*180,169,166,42),lambda k=key:setattr(game,'heritage_key',k),
                    primary=key==game.heritage_key,small=True,arrow=False)
    s.blit(illustration(game.heritage_key),(78,235))
    y=247
    for paragraph in item['body'].split('\n\n'):
        y=wrapped(s,paragraph,(482,y),707,19,PAPER,leading=29)+24
    text(s,'Ilustración original · representación cultural del viaje temporal',(482,570),13,MUTED)
    game.button('Consultar la fuente',(482,610,310,48),lambda:webbrowser.open(item['url']),small=True)
    game.button('Volver al viaje',(65,630,270,48),game.close_panel,True,small=True)
