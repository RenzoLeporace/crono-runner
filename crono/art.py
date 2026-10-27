"""Original procedural art: layered cut-paper landscapes and animated silhouettes.

No external images or fonts are needed. Geometry and textures are seeded, so the
same location always looks the same, including after a restart.
"""
import math
import random
from functools import lru_cache
import pygame as pg
from .levels import ERAS
from .visuals import palette_for,burnt_tree

W, H = 1280, 720
INK = (15, 23, 33)
PAPER = (238, 236, 217)
MUTED = (158, 176, 178)
CYAN = (116, 237, 219)
GOLD = (242, 189, 112)


def display_alpha(image,rle=False):
    """Prepare cached art once for software blits, preserving every RGBA pixel."""
    screen=pg.display.get_surface()
    if screen and screen.get_bitsize()==32:
        rgb=screen.get_masks()[:3];masks=(*rgb,0xffffffff^(rgb[0]|rgb[1]|rgb[2]))
        if image.get_masks()!=masks:image=image.convert(masks,pg.SRCALPHA)
    image.set_alpha(255,pg.RLEACCEL if rle else 0)
    return image


def mix(a, b, t):
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


def rect(surface, color, box, radius=0, width=0):
    pg.draw.rect(surface, color, pg.Rect(box), width, border_radius=radius)


def line(surface, color, a, b, width=1):
    pg.draw.line(surface, color, a, b, width)


def circle(surface, color, pos, radius, width=0):
    pg.draw.circle(surface, color, (int(pos[0]), int(pos[1])), max(1, int(radius)), width)


def polygon(surface, color, points, width=0):
    pg.draw.polygon(surface, color, [(int(x), int(y)) for x, y in points], width)


@lru_cache(maxsize=120)
def font(size, bold=False, serif=False):
    return pg.font.SysFont('cambria' if serif else 'segoeui', size, bold=bold)


@lru_cache(maxsize=1200)
def rendered_text(value,size,color,bold,serif):
    return display_alpha(font(size,bold,serif).render(value,True,color))

def text(surface, value, pos, size=20, color=PAPER, bold=False, anchor='topleft', serif=False):
    image = rendered_text(str(value),size,tuple(color),bold,serif)
    bounds = image.get_rect(**{anchor: (int(pos[0]), int(pos[1]))})
    surface.blit(image, bounds)
    return bounds


def tracked(surface, value, pos, size=13, color=MUTED, spacing=3):
    x, y = pos
    f = font(size, True)
    for ch in value:
        glyph = rendered_text(ch,size,tuple(color),True,False)
        surface.blit(glyph, (x, y))
        x += glyph.get_width() + spacing
    return x


@lru_cache(maxsize=64)
def glow_image(radius, color):
    size = radius * 2 + 2
    s = pg.Surface((size, size), pg.SRCALPHA)
    for r in range(radius, 0, -3):
        alpha = int(28 * (1 - r / radius) ** 1.3)
        circle(s, (*color, alpha), (radius + 1, radius + 1), r)
    return display_alpha(s)


def glow(surface, pos, radius=60, color=CYAN):
    surface.blit(glow_image(radius, color), (int(pos[0] - radius), int(pos[1] - radius)))


@lru_cache(maxsize=46)
def echo_image(color):
    image=pg.Surface((44,44),pg.SRCALPHA)
    glow(image,(21,21),21,color)
    circle(image,color,(21,21),5,1)
    circle(image,PAPER,(21,21),2)
    return display_alpha(image)


def diamond(surface, pos, size, color, filled=True):
    x, y = pos
    polygon(surface, color, [(x, y-size), (x+size*.65, y), (x, y+size), (x-size*.65, y)], 0 if filled else 1)


def clock_icon(surface, x, y, radius=16, color=CYAN, time=0):
    circle(surface, color, (x, y), radius, 2)
    line(surface, color, (x, y), (x+math.sin(time)*radius*.55, y-math.cos(time)*radius*.55), 2)
    line(surface, color, (x, y), (x-radius*.37, y-radius*.25), 2)
    for angle in range(0, 360, 90):
        a = math.radians(angle)
        line(surface, color, (x+math.cos(a)*(radius-3), y+math.sin(a)*(radius-3)),
             (x+math.cos(a)*(radius-6), y+math.sin(a)*(radius-6)), 1)


def armor_marker(surface,x,y):
    polygon(surface,(20,35,44),[(x-8,y-8),(x+8,y-8),(x+8,y+2),(x,y+10),(x-8,y+2)])
    polygon(surface,GOLD,[(x-8,y-8),(x+8,y-8),(x+8,y+2),(x,y+10),(x-8,y+2)],2)
    line(surface,GOLD,(x-3,y-2),(x+3,y+4),2)
    line(surface,GOLD,(x+3,y-2),(x-3,y+4),2)


def fern(surface, x, y, scale, color, flip=1):
    # Curved stem with alternating cut-paper leaflets.
    tip = (x + 28*scale*flip, y - 87*scale)
    line(surface, color, (x, y), tip, max(1, int(3*scale)))
    for i in range(1, 9):
        t = i/10
        bx = x + 28*scale*flip*t
        by = y - 87*scale*t
        length = 27*scale*math.sin(t*math.pi)
        for side in (-1, 1):
            polygon(surface, color, [(bx, by+4*scale), (bx+side*length, by-16*scale),
                                     (bx+side*length*.6, by-19*scale), (bx, by-3*scale)])


def tree(surface, x, base, height, color, kind='jungle'):
    if kind == 'jungle':
        polygon(surface, color, [(x-10, base), (x+12, base), (x+5, base-height), (x-4, base-height)])
        for side in (-1, 1):
            for j in range(4):
                top = base-height+18+j*18
                reach = (75-j*8)*side
                polygon(surface, color, [(x, top), (x+reach*.7, top-24), (x+reach, top+10),
                                         (x+reach*.6, top-2), (x, top+12)])
    else:
        rect(surface, color, (x-4, base-height*.7, 8, height*.7))
        for j in range(4):
            yy = base-height+j*height*.17
            half = height*(.16+j*.035)
            polygon(surface, color, [(x, yy), (x-half, yy+height*.37), (x+half, yy+height*.37)])


class Artist:
    def __init__(self):
        self.vignette = pg.Surface((W, H), pg.SRCALPHA)
        # Soft edges, without dimming the playable centre.
        for n in range(110):
            alpha=int(42*(1-n/110)**2)
            line(self.vignette,(5,12,20,alpha),(n,0),(n,H))
            line(self.vignette,(5,12,20,alpha),(W-1-n,0),(W-1-n,H))
        for n in range(60):
            line(self.vignette,(5,12,20,int(35*(1-n/60))),(0,H-1-n),(W,H-1-n))
        self.menu_shade = pg.Surface((W, H), pg.SRCALPHA)
        for x in range(W):
            alpha = int(230 * max(0, 1-x/W) ** .55)
            line(self.menu_shade, (8, 17, 25, alpha), (x, 0), (x, H))

    def background(self,surface,index,camera,time,stage=0):
        if index<7:
            from .period_art import background
            background(surface,index,stage,camera,time)
        elif index==7:
            from .argentina_art import background
            background(surface,stage,camera,time)
        elif index==8:
            from .egypt_art import background
            background(surface,stage,camera,time)
        else:
            from .journey_art import background
            background(surface,index,stage,camera,time)

    def platform_image(self,p,index,stage=0):
        args=(stage,int(p.rect.w),int(p.rect.h),int(p.origin),p.moving)
        if index<7:
            from .period_art import tile
            image=tile(index,*args)
        elif index==7:
            from .argentina_art import platform_tile
            image=platform_tile(*args)
        elif index==8:
            from .egypt_art import tile
            image=tile(*args)
        else:
            from .journey_art import tile
            image=tile(index,*args)
        image.set_alpha(255,pg.RLEACCEL)
        return image

    def scenery(self, surface, world, camera, time):
        era = palette_for(world.index,world.stage)
        if world.level_id==0 and not getattr(world,'mobile_render',False):
            for wx,label in ((315,'ESPACIO · MANTÉN PARA SALTAR'),(682,'SHIFT · IMPULSO TEMPORAL')):
                if abs(world.player.rect.centerx-wx)<280:
                    text(surface,label,(wx-camera,351),11,mix(era.accent,PAPER,.3),True,'center')
        # Landmarks live in world space, and never obscure hazards or pickups.
        for p in world.platforms:
            if not p.active:continue
            r=p.rect
            if r.right < camera-20 or r.left > camera+W+20:
                continue
            surface.blit(self.platform_image(p,world.index,world.stage),(int(r.x-camera),int(r.y)))
            if p.moving:
                glow(surface,(r.centerx-camera,r.y+13),40,CYAN)
        for i in range(4):
            a=world.platforms[i].rect
            b=world.platforms[i+1].rect
            midpoint=(a.right+b.left)/2-camera
            if -95<midpoint<W+95:glow(surface,(midpoint,735),95,era.near)
        for n, (wx, wy) in enumerate(world.data['checkpoints']):
            if n not in world.checkpoint_ids:
                continue
            x=wx-camera
            if not -90<x<W+90:continue
            active = n <= world.checkpoint
            color=CYAN if active else era.accent
            rect(surface,era.rock,(x-18,wy-8,36,8))
            rect(surface,mix(era.rock,era.top,.5),(x-6,wy-77,12,70),3)
            circle(surface,color,(x,wy-79),15,2)
            clock_icon(surface,x,wy-79,10,color,time if active else 0)
            if active:
                glow(surface,(x,wy-79),65,CYAN)
            elif abs(world.player.rect.centerx-wx)<160:
                text(surface,'ANCLA TEMPORAL',(x,wy-110),11,color,True,'center')
        for hazard in world.hazards:
            if hazard.right<camera-20 or hazard.left>camera+W+20:continue
            x,y=hazard.x-camera,hazard.y
            icy=world.combat_era==1 or world.level_id in (28,33,48)
            colors=((146,207,230),(225,246,249)) if icy else ((123,128,119),(199,195,159)) if world.combat_era in (4,5,6,7) else ((205,108,105),(243,165,135))
            for xx in range(0,int(hazard.w)-6,13):
                polygon(surface,colors[0],[(x+xx,y+14),(x+xx+6,y-2),(x+xx+13,y+14)])
                line(surface,colors[1],(x+xx+6,y),(x+xx+10,y+10))
        echoes=[];image=echo_image(era.accent)
        for i,(wx,wy) in enumerate(world.data['echoes']):
            if i in world.echoes or not camera-30<wx<camera+surface.get_width()+30:
                continue
            x,y=wx-camera,wy+math.sin(time*2.8+i)*4
            if -25<y<surface.get_height()+25:echoes.append((image,(int(x-21),int(y-21))))
        if echoes:surface.blits(echoes,doreturn=False)
        for i,(wx,wy) in enumerate(world.data['shards']):
            if i in world.shards or not camera-55<wx<camera+surface.get_width()+55:
                continue
            x,y=wx-camera,wy+math.sin(time*2+i)*6
            if -50<x<W+50:
                glow(surface,(x,y),54,CYAN)
                diamond(surface,(x,y),17,CYAN)
                diamond(surface,(x,y),11,(210,255,235))
                line(surface,(31,112,112),(x,y-10),(x,y+10),1)
                for j in range(3):
                    angle=time+j*math.tau/3
                    circle(surface,CYAN,(x+math.cos(angle)*26,y+math.sin(angle)*18),1)
        px,py=world.data['portal']
        if -180<px-camera<W+180:
            self.portal(surface,px-camera,py,time,len(world.shards)==3 and world.story_ready and (not world.boss or not world.boss.alive))
        if abs(world.player.rect.centerx-px)<250:
            text(surface,'AL PRESENTE' if world.level_id in (20,23) else 'SIGUIENTE ÉPOCA' if world.stage==2 else 'SIGUIENTE MAPA',(px-camera,py-166),12,CYAN,True,'center')
            label='Guardián por liberar' if world.boss and world.boss.alive else f'{len(world.shards)} / 3 fragmentos'
            text(surface,label,(px-camera,py-144),13,PAPER,False,'center')

    def portal(self,surface,x,y,time,active=True,scale=1):
        color=CYAN if active else (107,137,138)
        cx,cy=x,y-69*scale
        glow(surface,(cx,cy),int(120*scale),color)
        for side in (-1,1):
            polygon(surface,(34,49,56),[(x+side*43*scale,y),(x+side*57*scale,y-26*scale),
                (x+side*48*scale,y-118*scale),(x+side*28*scale,y-143*scale),
                (x+side*36*scale,y-98*scale),(x+side*32*scale,y)])
            line(surface,color,(x+side*44*scale,y-25*scale),(x+side*39*scale,y-110*scale),max(1,int(2*scale)))
        pg.draw.ellipse(surface,color,pg.Rect(x-34*scale,y-132*scale,68*scale,127*scale),max(1,int(3*scale)))
        pg.draw.ellipse(surface,mix(color,PAPER,.4),pg.Rect(x-28*scale,y-126*scale,56*scale,115*scale),1)
        for j in range(18):
            a=j*math.tau/18+time*.3
            xx=cx+math.cos(a)*25*scale
            yy=cy+math.sin(a)*52*scale
            circle(surface,color,(xx,yy),2*scale)
        if active:
            for i in range(8):
                a=time*.8+i*2.4
                xx=cx+math.sin(a)*19*scale
                yy=cy+math.cos(a*.7)*45*scale
                line(surface,mix(color,PAPER,.2),(xx,yy),(xx,yy+6*scale),1)
        rect(surface,(35,48,53),(x-62*scale,y-7*scale,124*scale,12*scale),3)
        diamond(surface,(x,y-143*scale),9*scale,color)

    def player(self,surface,player,camera,time,scale=1,override=None,ghost=False):
        # The body is drawn in a local 76 x 90 canvas and flipped as a whole.
        s=pg.Surface((82,94),pg.SRCALPHA)
        running=abs(player.vx)>30 and player.grounded
        phase=player.anim*2.4
        bob=math.sin(phase*2)*1.5 if running else math.sin(time*2)*1.0
        jump=not player.grounded
        y=22+bob
        dark=(30,42,53)
        from .skins import SKINS
        coat=next((item['color'] for item in SKINS if item['id']==getattr(player,'skin','crono')),(222,218,189))
        shadow=(156,168,155)
        if ghost:
            coat=CYAN
        # Trailing scarf uses time and velocity, including a soft idle flutter.
        length=32 if abs(player.vx)>100 else 22
        wave=math.sin(time*12)*4
        polygon(s,(197,82,60),[(35,y+14),(21,y+17),(max(0,21-length),y+8+wave),
                              (9,y+23+wave),(32,y+23)])
        polygon(s,(240,137,84),[(33,y+13),(22,y+15),(6,y+11+wave),(19,y+19),(33,y+19)])
        # Backpack, far arm, articulated legs and boots.
        rect(s,(101,101,85),(21,y+21,13,22),4)
        rect(s,(60,74,76),(19,y+23,6,16),2)
        leg_swing=math.sin(phase)*10 if running else 0
        for n,dx in enumerate((-1,1)):
            swing=leg_swing*dx
            knee=(36+dx*6+swing*.6,y+47-(4 if jump else 0))
            foot=(36+dx*7+swing,y+58-(7 if jump and n==0 else 0))
            line(s,dark,(35+dx*5,y+35),knee,8)
            line(s,dark,knee,foot,7)
            rect(s,(44,49,53),(foot[0]-4,foot[1]-3,13,7),2)
            line(s,(134,126,105),(foot[0]-3,foot[1]+3),(foot[0]+8,foot[1]+3),1)
        polygon(s,coat,[(28,y+16),(44,y+17),(48,y+39),(26,y+39)])
        polygon(s,shadow,[(28,y+19),(34,y+21),(32,y+38),(26,y+39)])
        line(s,(115,125,116),(38,y+20),(39,y+34),2)
        rect(s,(78,82,75),(28,y+33,19,5),1)
        rect(s,(214,172,104),(35,y+33,5,5),1)
        # Head / wind-tossed dark hair / visible eye.
        rect(s,(228,178,135),(32,y-3,17,19),5)
        polygon(s,(45,46,49),[(29,y+4),(29,y-5),(34,y-10),(40,y-7),(49,y-9),
                              (51,y-2),(47,y+4),(38,y),(36,y+7),(32,y+8)])
        rect(s,(244,199,150),(46,y+6,5,5),1)
        rect(s,(33,43,48),(45,y+4,3,3))
        rect(s,(236,139,85),(30,y+13,19,6),2)
        handx=49+(6 if player.dash_time>0 else math.sin(phase)*3 if running else 0)
        line(s,coat,(43,y+21),(handx,y+30),8)
        line(s,shadow,(handx,y+30),(handx+2,y+38),7)
        rect(s,(40,87,91),(handx-3,y+30,9,8),2)
        rect(s,CYAN,(handx-2,y+31,7,4),1)
        rect(s,(225,180,137),(handx,y+38,6,6),2)
        from .skins import details
        details(s,player,y)
        if player.facing<0:
            s=pg.transform.flip(s,True,False)
        if ghost:
            s.set_alpha(60)
        elif player.invincible>0 and int(time*14)%2:
            s.set_alpha(100)
        if scale!=1:
            s=pg.transform.scale(s,(int(82*scale),int(94*scale)))
        if override:
            x,by=override
        else:
            x=player.rect.centerx-camera
            by=player.rect.bottom
        surface.blit(s,(int(x-40*scale),int(by-83*scale)))
        if not ghost:
            glow(surface,(x+(14 if player.facing>0 else -14)*scale,by-24*scale),int(23*scale),CYAN)

    def enemy(self,surface,enemy,camera,time,index,stage=0):
        from .enemy_art import draw_enemy
        draw_enemy(surface,enemy,camera,time,enemy.era,enemy.stage if index>=9 else stage)

    def foreground(self,surface,world,camera):
        if not getattr(world,'mobile_render',False) and surface.get_width()==self.vignette.get_width():surface.blit(self.vignette,(0,0))

    def scene(self,surface,world,camera,time):
        from .educational_art import map_features,learning_objects,boss_art,projectiles
        from .visuals import ambient_back,ambient_front
        mobile=getattr(world,'mobile_render',False)
        if mobile:
            from .viewport import mobile_backdrop
            mobile_backdrop(self,surface,world,camera)
        else:
            self.background(surface,world.index,camera,time,world.stage)
            ambient_back(surface,world,camera,time)
            map_features(surface,world,camera,time)
            ambient_front(surface,world,camera,time)
        self.scenery(surface,world,camera,time)
        if world.index==7 and not mobile:
            from .argentina_art import props
            props(surface,world,camera,time)
        elif world.index<7 and not mobile:
            from .period_art import props
            props(surface,world,camera,time)
        learning_objects(surface,world,camera,time)
        from .heritage import draw_sites
        draw_sites(surface,world,camera,time)
        world.mechanic.draw(surface,camera,time)
        world.traits.draw(surface,camera,time)
        from .expansion_ui import draw_missions
        draw_missions(surface,world,camera,time)
        # The walkable rim always remains visible in front of exhibits/tools.
        for platform in world.platforms:
            r=platform.rect
            if platform.active and r.right>=camera and r.left<=camera+surface.get_width():
                line(surface,(187,184,142),(r.left-camera,r.top),(r.right-camera,r.top),3)
        for enemy in world.enemies:
            if world.index==7:
                enemy.show_label=abs(world.player.rect.centerx-enemy.rect.centerx)<240
            self.enemy(surface,enemy,camera,time,world.index,world.stage)
        p=world.player
        original_skin=getattr(p,'skin','crono')
        if world.level_id==44:p.skin='astronauta'
        boss_art(surface,world.boss,camera,time)
        projectiles(surface,world,camera)
        if p.dash_time>0:
            for n in (3,2,1):
                self.player(surface,p,camera+p.facing*n*26,time,ghost=True)
        self.player(surface,p,camera,time)
        if p.shield:
            circle(surface,CYAN,(p.rect.centerx-camera,p.rect.centery),39,1)
            glow(surface,(p.rect.centerx-camera,p.rect.centery),43,CYAN)
        if world.level_id==44:p.skin=original_skin
        world.traits.lighting(surface,camera)
        self.foreground(surface,world,camera)
