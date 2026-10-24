"""24 authored elevation itineraries with traversable branches and distinct landmarks.

The geometry is deterministic. Shared construction rules enforce jump reach, but
each map has its own length, elevations, branch placement and return loops.
"""
import random

# 0 = valley floor, 1..4 = successively higher terraces, 64 px per step.
# These are authored routes rather than mirrors or permutations of five maps.
ITINERARIES=(
 '001122321001210', '0123432101232101', '00012123210000010',
 '012212332101210', '0012334321010012', '0123432343210010',
 '0012321012321001', '00010121210001010', '0123234321012100',
 '00012100121210010', '0123210123432101', '01234343212321010',
 '0121232101232100', '00000112100012100', '01234321234321010',
 '00101001212100010', '012321000123210010', '00123210100121000',
 '01234321212343210', '00012123212100010', '01212343212321000',
 '00012101232100010', '01232123210123210', '00123210123210000',
)
ROUTE_NAMES=(
 ('Manglar','Copas enlazadas','Arrecife'),('Estratos','Garganta','Archivo fósil'),('Bosque caído','Cráter','Último refugio'),
 ('Llanura helada','Paso elevado','Cornisa'),('Entrada','Galerías','Hogar del fuego'),('Vestíbulo','Pared de manos','Cámara profunda'),
 ('Pórticos','Terrazas cívicas','Acrópolis'),('Muelles','Almacenes','Faro'),('Entrenamiento','Gradas','Santuario'),
 ('Huertas','Molino','Granero'),('Canales','Tejados','Plaza del mercado'),('Claustro','Contrafuertes','Campanario'),
 ('Calderas','Pasarelas','Turbinas'),('Andenes','Viaducto','Estación'),('Cables','Azoteas','Central'),
 ('Correspondencia','Trincheras vacías','Puesto de socorro'),('Refugios','Ciudad dañada','Evacuación'),('Reconstrucción','Asamblea','Memoria'),
 ('Red local','Servidores','Antenas'),('Agua','Energía solar','Aerogeneradores'),('Laboratorio','Observatorio','Portal a casa'),
 ('Plaza de Mayo','Recova','Cabildo'),('Camino del norte','Patios','Casa de Tucumán'),('Calles','Plaza cívica','Congreso'),
)

def build_route(index,stage,meta):
    level=index*3+stage
    rng=random.Random(5100+level*307)
    itinerary=ITINERARIES[level]
    platforms=[]; main=[]; branches=[]; ferries=[]; links=[]
    def add(x,y,w,h=28,**extra):
        p=dict(x=x,y=y,w=w,h=h,moving=False)
        p.update(extra)
        platforms.append(p)
        return len(platforms)-1
    x=0
    for n,height in enumerate(itinerary):
        y=584-int(height)*64
        width=rng.randrange(540,850,20)
        # Only one-level ascents: a 105 px gap with a 64 px rise is reachable.
        if n and abs(int(height)-int(itinerary[n-1]))>1:
            raise ValueError('The authored itinerary needs an intermediate terrace')
        if n:
            gap=85 if y<main[-1][1] else rng.choice((90,110,130))
            x+=gap
        k=add(x,y,width,220 if height=='0' else 32,oneway=height!='0')
        main.append((x,y,width,k))
        if n:
            links.append((main[-2][3],k))
        x+=width
    # Each optional upper loop has two entrances and a return onto the main route.
    # Its first step is mandatory for a fragment in three separated districts.
    for n,(xx,yy,ww,k) in enumerate(main[1:-1],1):
        if n%2==(level%2) or n in (3,len(main)//2,len(main)-4):
            style=(level+n//3)%4
            # Balconies, stair loops, reversed switchbacks, and split galleries.
            ax,bx,cx=(75,250,440) if style!=2 else (280,105,440)
            by=yy-88 if style==1 else yy-170
            a=add(xx+ax,yy-88,155,24,oneway=True)
            b=add(xx+bx,by,220 if style==1 else 155,24,oneway=True)
            c=add(xx+cx,yy-88,155,24,oneway=True)
            links.extend(((k,a),(a,b),(b,c),(c,k),(c,b),(b,a),(a,k)))
            branches.append((n,a,b,c))
        if n%4==2 and yy<=456:
            # A lower optional gallery, reachable by dropping and stairs back up.
            low=add(xx+80,min(650,yy+130),240,24,oneway=True)
            step=add(xx+350,yy+60,130,24,oneway=True)
            links.extend(((k,low),(low,step),(step,k)))
        if n%3==1:
            ferries.append(add(xx+ww+9,yy+60,75,22,moving=True,amplitude=22,speed=1.1+level*.013))
    targets=[]
    for fraction in (.23,.52,.79):
        target=min(branches,key=lambda b:abs(b[0]/len(main)-fraction))
        # First branch step is 88 px above its base; no upgrade is required.
        p=platforms[target[1]]
        targets.append((p['x']+p['w']/2,p['y']-37))
    checkpoints=[(xx+45,yy) for n,(xx,yy,ww,k) in enumerate(main) if n and n%2==0]
    stations=[(main[0][0]+245,main[0][1],level*2),
              (main[len(main)//2][0]+45,main[len(main)//2][1],level*2+1)]
    safe=[(sx,sy) for sx,sy,*_ in stations]+checkpoints
    enemies=[]; hazards=[]
    roster=('walker','hopper','flyer','sentry','charger','armored')
    for n,(xx,yy,ww,k) in enumerate(main):
        if n:
            for j in range(2 if n%3==1 else 1):
                kind=roster[(n+stage*2+index+j*3)%6]
                ex=xx+ww*(.45+j*.24)
                if all(abs(ex-sx)>145 or abs(yy-sy)>80 for sx,sy in safe):
                    enemies.append(dict(x=ex,y=yy-34,left=xx+165,right=xx+ww-24,kind=kind))
        if n%3==2:
            hx=xx+ww-155
            if all(abs(hx-sx)>155 for sx,sy in safe):
                hazards.append((hx,yy-14,48+stage*8,14))
    # Exactly 48 echoes: each upper route contributes, the remainder marks travel.
    echoes=[(platforms[b]['x']+78,platforms[b]['y']-36) for _,a,b,c in branches]
    for xx,yy,ww,k in main:
        echoes.extend((xx+ww*f,yy-37) for f in (.28,.58,.82))
    echoes=echoes[:48]
    while len(echoes)<48:
        xx,yy,ww,k=main[len(echoes)%len(main)]
        echoes.append((xx+ww*.7+(len(echoes)%3)*25,yy-37))
    last=main[-1]
    # Descending steps lead into an arena whose coordinates derive from map length.
    tail_x=x+90; tail_y=last[1]
    previous=last[3]
    while tail_y<584:
        tail_y=min(584,tail_y+64)
        k=add(tail_x,tail_y,200,28)
        links.append((previous,k));previous=k;tail_x+=280
    arena_left=tail_x if stage==2 else None
    end=add(tail_x,584,1280 if stage==2 else 520,220)
    links.append((previous,end))
    width=tail_x+(1280 if stage==2 else 520)
    if stage==2:
        checkpoints.append((tail_x+70,584))
        add(tail_x+230,488,150,24,oneway=True)
        add(tail_x+1030,488,150,24,oneway=True)
    zones=[(main[int(len(main)*f)][0],name) for f,name in zip((0,.35,.68),ROUTE_NAMES[level])]
    return dict(width=width,platforms=platforms,shards=targets,echoes=echoes,
        checkpoints=checkpoints,stations=stations,enemies=enemies,hazards=hazards,
        spawn=(100,520),portal=(width-160,584),meta=meta,boss=stage==2,
        arena_left=arena_left,arena_right=width-30,route_links=links,
        main_nodes=[m[3] for m in main]+[end],zones=zones,route_name=' / '.join(ROUTE_NAMES[level]),
        layout_version=3)
