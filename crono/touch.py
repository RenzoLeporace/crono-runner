"""Landscape multitouch controls in logical coordinates, independent fingers."""
import pygame as pg
import math
from functools import lru_cache
from .art import rect,text,line,polygon,CYAN,PAPER

DEFAULT_KEYS=dict(left=pg.K_a,right=pg.K_d,jump=pg.K_SPACE,dash=pg.K_LSHIFT,attack=pg.K_f,interact=pg.K_e,drop=pg.K_s,pause=pg.K_ESCAPE)
KEY_LABELS=dict(left='Izquierda',right='Derecha',jump='Saltar',dash='Impulso',attack='Disparar',interact='Usar / mantener para trabajar',drop='Bajar',pause='Pausa')


def boxes_for_width(width):
    # Anchor to the real viewport, with breathing room for thumbs and screen edges.
    pad=32;right=width-pad-156
    return dict(left=(pad,552,112,112),right=(pad+126,552,112,112),drop=(pad+71,442,96,96),
                jump=(right,532,156,156),dash=(width-294,417,104,104),
                attack=(width-162,365,104,104),interact=(width-344,558,104,104))


TOUCH_BOXES=boxes_for_width(1280)

@lru_cache(maxsize=8)
def touch_panel(width,height,active):
    panel=pg.Surface((width,height),pg.SRCALPHA)
    pg.draw.circle(panel,(21,51,61,170 if active else 62),(width//2,height//2),min(width,height)//2-2)
    return panel

@lru_cache(maxsize=32)
def control_image(name,size,active,ready):
    from .child_ui import pictogram
    image=pg.Surface((size,size),pg.SRCALPHA);cx=size/2;cy=size/2-9
    primary=name=='jump';color=CYAN if primary or active else PAPER if ready else (128,151,156)
    pg.draw.circle(image,(24,81,89,195 if active else 140) if primary else (21,51,61,175 if active else 115),(size//2,size//2),size//2-3)
    pg.draw.circle(image,color,(size//2,size//2),size//2-3,3 if primary or active else 2)
    if name in ('left','right'):
        sign=-1 if name=='left' else 1
        polygon(image,color,[(cx+sign*25,size/2),(cx-sign*14,size/2-25),(cx-sign*14,size/2+25)])
    elif name=='drop':polygon(image,color,[(cx-22,cy-11),(cx+22,cy-11),(cx,cy+21)])
    elif name=='attack':
        pg.draw.circle(image,color,(cx,cy),16,2)
        line(image,color,(cx-23,cy),(cx+23,cy),3);line(image,color,(cx,cy-23),(cx,cy+23),3)
    elif name=='jump':
        line(image,color,(cx,cy+25),(cx,cy-22),5);polygon(image,color,[(cx,cy-34),(cx-20,cy-9),(cx+20,cy-9)])
    elif name=='dash':polygon(image,color,[(cx+6,cy-25),(cx-17,cy+3),(cx-1,cy+3),(cx-6,cy+25),(cx+18,cy-6),(cx+4,cy-6)])
    else:image.blit(pg.transform.scale(pictogram('hand',color),(45,45)),(round(cx-22),round(cy-25)))
    if name not in ('left','right'):
        label=dict(drop='BAJAR',jump='SALTAR',attack='PULSO',dash='RAYO',interact='USAR')[name]
        text(image,label,(cx,cy+(45 if primary else 32)),22 if primary else 13,color,True,'center')
    from .art import display_alpha
    return display_alpha(image,True)


class TouchUI:
    def init_touch(self):
        self.fingers={};self.finger_positions={};self.rebind_action=None
        self.work_lock=False;self.joy_work=False
    def press_interact(self):
        if self.work_lock:return
        self.work_lock=True
        if self.world.mechanic.field.work_target():return
        self.interact()
    def key_for(self,action):
        value=self.save.data['key_bindings'].get(action,DEFAULT_KEYS[action])
        return value if type(value) is int else DEFAULT_KEYS[action]
    def touch_enabled(self):return bool(self.save.data['touch_controls'])
    def touch_down(self,action):return action in self.fingers.values()
    def touch_event(self,event):
        if event.type not in (pg.FINGERDOWN,pg.FINGERMOTION,pg.FINGERUP):return False
        self.save.data['touch_controls']=True
        dw,dh=self.display.get_size();pos=self.logical_mouse((event.x*dw,event.y*dh));key=event.finger_id
        previous_pos=self.finger_positions.get(key,pos);self.finger_positions[key]=pos
        if event.type==pg.FINGERUP:self.finger_positions.pop(key,None)
        if self.state in ('play','voyage'):
            if event.type==pg.FINGERUP:
                self.fingers.pop(key,None)
                if not self.touch_down('interact'):self.work_lock=False
                return True
            if event.type==pg.FINGERDOWN:
                for box,action,enabled in self.buttons[:]:
                    if enabled and box.collidepoint(pos):action();return True
            control_pos=(pos[0]*self.ui_scale+self.ui_offset[0],pos[1]*self.ui_scale+self.ui_offset[1])
            action=next((name for name,box in boxes_for_width(self.viewport_width).items() if pg.Rect(box).collidepoint(control_pos)),None)
            if action is None and self.state=='play' and any(box.collidepoint(control_pos) for box in getattr(self,'world_action_hotspots',[])):action='interact'
            previous=self.fingers.get(key);self.fingers[key]=action
            # Keep the jump captured while a thumb drifts across its rim.
            if event.type==pg.FINGERMOTION and previous=='jump':action='jump';self.fingers[key]=action
            if previous=='interact' and action!='interact':self.work_lock=False
            if event.type==pg.FINGERDOWN or action!=previous:
                if action=='jump':self.jump_pending=True
                elif action=='dash':self.dash_pending=True
                elif action=='attack':self.shoot_pending=True
                elif action=='interact' and self.state=='play':self.press_interact()
                elif pos[0]>1180 and pos[1]<100:
                    if self.state=='voyage':self.voyage.paused=True
                    else:self.set_state('pause')
            return True
        if event.type==pg.FINGERDOWN:
            self.mouse=pos
            # Reuse text fields and button actions without synthesizing a second click.
            synthetic=pg.event.Event(pg.MOUSEBUTTONDOWN,button=1,pos=(event.x*dw,event.y*dh))
            if self.handle_community_event(synthetic) or self.handle_school_event(synthetic) or self.handle_teacher_event(synthetic):return True
            for box,action,enabled in self.buttons[:]:
                if enabled and box.collidepoint(pos):action();break
        elif event.type==pg.FINGERMOTION and self.state=='quiz':
            delta=previous_pos[1]-pos[1]
            if pos[0]<520:self.quiz_scroll=max(0,min(max(0,self.quiz_fact_height-self.quiz_fact_view_height),self.quiz_scroll+delta))
            else:self.quiz_feedback_scroll=max(0,min(max(0,self.quiz_feedback_height-265),self.quiz_feedback_scroll+delta))
        elif event.type==pg.FINGERMOTION and self.state=='heritage':
            self.heritage_scroll=max(0,min(max(0,self.heritage_height-295),self.heritage_scroll+previous_pos[1]-pos[1]))
        return True
    def touch_action_ready(self):
        from .heritage import near_site
        w=self.world;p=w.player.rect
        if w.mechanic.field.work_target() or w.traits.can_work() or w.near_station() or w.mechanic.near() is not None or near_site(w):return True
        return any(site and abs(p.centerx-site[0])<100 and abs(p.bottom-site[1])<110 for site in (w.rift_site,w.rescue_site))

    def draw_touch(self):
        s=self.world_canvas;work=self.world.mechanic.field.work_target()
        for name,box in boxes_for_width(self.viewport_width).items():
            if self.state=='voyage' and name in ('dash','interact'):continue
            active=self.touch_down(name)
            ready=self.world.player.dash_ready and self.world.player.cooldown<=0 if name=='dash' else self.touch_action_ready() if name=='interact' else True
            s.blit(control_image(name,box[2],active,ready),box[:2])
            if name=='dash' and self.world.player.cooldown>0:
                duration=.65 if 'dash' in self.world.player.upgrades else 1.15
                pg.draw.arc(s,(242,189,112),pg.Rect(box).inflate(-8,-8),-math.pi/2,-math.pi/2+math.tau*(1-min(1,self.world.player.cooldown/duration)),5)
            tutorial=getattr(self,'tutorial_active',False)
            target=('left','jump','dash','attack','interact')[self.tutorial_step] if tutorial else None
            if name==target or target=='left' and name=='right':
                pg.draw.circle(s,(242,189,112),pg.Rect(box).center,box[2]//2-1,4)
            if name=='interact' and work and work['progress']:
                pg.draw.arc(s,(242,189,112),pg.Rect(box).inflate(-7,-7),-math.pi/2,-math.pi/2+math.tau*work['progress'],5)
    def binding_event(self,event):
        if self.state!='accessibility' or not self.rebind_action or event.type!=pg.KEYDOWN:return False
        if event.key==pg.K_ESCAPE:self.rebind_action=None;self.access_message='Cambio cancelado.';return True
        if event.key in (pg.K_F11,pg.K_F12,pg.K_m):return True
        if event.key in {self.key_for(a) for a in DEFAULT_KEYS if a!=self.rebind_action} or event.key in (pg.K_UP,pg.K_DOWN,pg.K_LEFT,pg.K_RIGHT,pg.K_u,pg.K_c,pg.K_v,pg.K_r):
            self.access_message='Esa tecla ya tiene otra acción. Elige otra.';return True
        action=self.rebind_action
        self.save.data['key_bindings'][action]=event.key;self.save.write();self.rebind_action=None
        self.access_message=KEY_LABELS[action]+': '+pg.key.name(event.key)+'. Guardado.';return True

    def begin_rebind(self,action):
        self.rebind_action=action;self.access_message='Pulsa una tecla para '+KEY_LABELS[action].lower()+'. Esc cancela.'

    def reset_keys(self):
        self.save.data['key_bindings']={};self.rebind_action=None;self.save.write()
        self.access_message='Controles restablecidos: A/D, Espacio, Shift, F, E y S o flecha abajo.'
