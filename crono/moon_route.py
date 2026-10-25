"""A traversal-only lunar level, authored for 1/6 gravity and suit-controlled jumps."""
from .physics_constants import LUNAR_GRAVITY,LUNAR_JUMP_SCALE

def build(meta):
    platforms=[];main=[];links=[]
    heights=(584,540,490,570,440,520,420,510,460,584,470,530,420,500,570,480,540,584)
    x=0
    for n,y in enumerate(heights):
        width=650 if n==0 else 650 if n==17 else (185,240,165,280)[n%4]
        if n:x+=(330,430,510,380)[n%4]
        k=len(platforms);p=dict(x=x,y=y,w=width,h=180 if n in (0,17) else 28,moving=False,oneway=n not in (0,17))
        platforms.append(p);main.append(k)
        if n:links.append((main[-2],k))
        x+=width
    shards=[];parts=[]
    for n in (4,9,14):
        base=platforms[main[n]];a=len(platforms)
        platforms.append(dict(x=base['x']+30,y=base['y']-88,w=135,h=20,moving=False,oneway=True))
        links.extend(((main[n],a),(a,main[n])))
        shards.append((base['x']+97,base['y']-125))
        parts.append((base['x']+97,base['y']-108))
    # Moving stepping stones offer alternatives but do not replace the main route.
    for n in (3,7,11,15):
        base=platforms[main[n]];platforms.append(dict(x=base['x']-180,y=base['y']+48,w=100,h=18,moving=True,oneway=True,amplitude=40,speed=.8))
    checkpoints=[(platforms[main[n]]['x']+32,heights[n]) for n in range(2,18,2)]
    stations=[(245,584,88),(platforms[main[8]]['x']+70,heights[8],89)]
    echoes=[]
    for n in range(16):
        p=platforms[main[n]]
        for f in (.2,.5,.8):echoes.append((p['x']+p['w']*f,p['y']-35))
    last=platforms[main[-1]];width=x
    return dict(gravity=LUNAR_GRAVITY,jump_scale=LUNAR_JUMP_SCALE,width=width,platforms=platforms,main_nodes=main,route_links=links,shards=shards,echoes=echoes,
                checkpoints=checkpoints,stations=stations,enemies=[],hazards=[],spawn=(100,520),portal=(width-110,584),
                boss=False,arena_left=None,arena_right=width-30,meta=meta,layout_version=4,
                cultural_sites=[(last['x']+90,584,'lunar_boot')],repair_parts=parts,repair_ship=(width-340,584),
                zones=[(0,'El módulo dañado'),(platforms[main[6]]['x'],'Cornisas de baja gravedad'),(platforms[main[12]]['x'],'El camino de regreso')],
                route_name='Cráteres / cornisas de inercia / reparación del módulo')
