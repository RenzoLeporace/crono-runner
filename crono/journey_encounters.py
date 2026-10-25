"""Contextual attack patterns for fictional guardians of historical excursions."""
import math
from .combat import Projectile
HINTS=dict(battery='Salta la onda y abandona las columnas marcadas.',andes='Busca abrigo y esquiva las rocas anunciadas.',
    naval='Gobierna el barco entre salvas; dispara al núcleo abierto.',lighthouse='Cruza los huecos del abanico de luz.',
    train='Salta las ondas y evita la locomotora en marcha.',hospital='Protege el recorrido y evita las marcas de la sirena.',
    malvinas='Alterna altura y movimiento entre las ráfagas.',volcano='Busca los huecos entre las columnas de ceniza.',
    lunar='Aprovecha la gravedad menor entre proyectiles radiales.')
HINTS.update(frontier='Salta las salvas y usa la cobertura entre ataques.',archive='Evita las columnas marcadas y devuelve los pulsos al núcleo.',
             press='Cruza entre los golpes de la prensa y ataca al detenerse.',lever='Salta la onda y busca el núcleo durante el equilibrio.',
             manuscript='Alterna movimiento y refugio; protege el recorrido.',cipher='Observa las marcas antes de moverte hacia el núcleo.')

def begin(b,w):
    variant=getattr(b,'variant','')
    if not variant:return False
    b.phase='attack';b.attack_time=0.;b.timer=dict(battery=1.1,andes=1.,naval=1.3,lighthouse=1.1,train=1.25,hospital=1.2,malvinas=1.3,volcano=1.25,lunar=1.4).get(variant,1.2)
    x,y=b.rect.center;rate=(1.,1.15,1.3)[b.difficulty];p=w.player.rect
    b.direction=1 if p.centerx>x else -1
    if variant in ('frontier','press','lever','archive','manuscript','cipher'):
        if variant in ('frontier','press','lever'):
            for side in (-1,1):w.projectiles.append(Projectile(x,570,side*240*rate,kind='wave'))
        if variant in ('archive','press','manuscript','cipher'):
            offsets=(-160,160) if variant=='manuscript' else (-140,0,140)
            for dx in offsets:b.telegraphs.append([max(b.left+70,min(b.right-70,p.centerx+dx)),1.2])
        if variant=='frontier':w.projectiles.append(Projectile(x,520,b.direction*270*rate,kind='musket'))
    elif variant=='battery':
        for dx in (-190,0,190):b.telegraphs.append([max(b.left+70,min(b.right-70,p.centerx+dx)),1.05])
        for side in (-1,1):w.projectiles.append(Projectile(x,570,side*220*rate,kind='wave'))
    elif variant=='andes':
        for offset in (-150,150):b.telegraphs.append([max(b.left+65,min(b.right-65,p.centerx+offset)),1.2])
        w.projectiles.append(Projectile(x,570,b.direction*240*rate,kind='wave'))
    elif variant=='naval':
        # Cannon salvos cross the navigable height; a boat can steer between them.
        for vy in (-105,0,105):w.projectiles.append(Projectile(x,y,b.direction*260*rate,vy))
        if b.difficulty:b.telegraphs.append([p.centerx,1.15])
    elif variant=='lighthouse':
        for n in range(5):
            angle=-.5+n*.25;w.projectiles.append(Projectile(x,y,b.direction*215*rate*math.cos(angle),215*rate*math.sin(angle)))
    elif variant=='train':
        for side in (-1,1):w.projectiles.append(Projectile(x,570,side*190*rate,kind='wave'))
    elif variant=='hospital':
        # The antagonist is a temporal siren, never a wounded person or medic.
        for dx in (-230,0,230):b.telegraphs.append([max(b.left+70,min(b.right-70,p.centerx+dx)),1.25])
    elif variant=='malvinas':
        for n in range(3):w.projectiles.append(Projectile(x,410+n*55,b.direction*(200+n*25)*rate,15))
        b.telegraphs.append([p.centerx,1.2])
    elif variant=='volcano':
        for n in range(4+b.difficulty):b.telegraphs.append([b.left+130+n*(b.right-b.left-260)/(3+b.difficulty),1.15+n*.08])
    elif variant=='lunar':
        for n in range(6):
            angle=math.tau*n/6;w.projectiles.append(Projectile(x,y,math.cos(angle)*170*rate,math.sin(angle)*170*rate))
    return True

def movement(b,dt,w):
    if getattr(b,'variant','')=='train' and b.phase=='attack':b.rect.x+=b.direction*(300+b.difficulty*40)*dt
    elif getattr(b,'variant','')=='naval' and b.phase=='attack':b.rect.x+=math.sin(b.attack_time*2)*75*dt
