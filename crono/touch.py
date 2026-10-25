"""Landscape multitouch controls in logical coordinates, independent fingers."""
import pygame as pg
from functools import lru_cache
from .art import rect,text,line,polygon,CYAN,PAPER

DEFAULT_KEYS=dict(left=pg.K_a,right=pg.K_d,jump=pg.K_SPACE,dash=pg.K_LSHIFT,attack=pg.K_f,interact=pg.K_e,drop=pg.K_s,pause=pg.K_ESCAPE)
KEY_LABELS=dict(left='Izquierda',right='Derecha',jump='Saltar',dash='Impulso',attack='Disparar',interact='Interactuar',drop='Descender',pause='Pausa')
TOUCH_BOXES=dict(left=(22,568,78,78),right=(112,568,78,78),drop=(68,482,66,66),jump=(1178,604,78,78),dash=(1084,604,72,72),attack=(1178,510,72,72),interact=(1084,510,72,72))

@lru_cache(maxsize=8)
def touch_panel(width,height,active):
    panel=pg.Surface((width,height),pg.SRCALPHA)
    pg.draw.circle(panel,(21,51,61,170 if active else 62),(width//2,height//2),min(width,height)//2-2)
    return panel

class TouchUI:
    def init_touch(self):self.fingers={};self.finger_positions={};self.rebind_action=None
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
            if event.type==pg.FINGERUP:self.fingers.pop(key,None);return True
            if event.type==pg.FINGERDOWN:
                for box,action,enabled in self.buttons[:]:
                    if enabled and box.collidepoint(pos):action();return True
            action=next((name for name,box in TOUCH_BOXES.items() if pg.Rect(box).collidepoint(pos)),None)
            previous=self.fingers.get(key);self.fingers[key]=action
            if event.type==pg.FINGERDOWN or action!=previous:
                if action=='jump':self.jump_pending=True
                elif action=='dash':self.dash_pending=True
                elif action=='attack':self.shoot_pending=True
                elif action=='interact' and self.state=='play':self.interact()
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
    def draw_touch(self):
        for name,box in TOUCH_BOXES.items():
            active=self.touch_down(name)
            if self.state=='voyage' and name in ('dash','interact'):continue
            panel=touch_panel(box[2],box[3],active)
            self.canvas.blit(panel,box[:2]);pg.draw.circle(self.canvas,CYAN if active else (166,191,190),pg.Rect(box).center,min(box[2],box[3])//2-2,2 if active else 1)
            label=dict(left='◀',right='▶',drop='↓',jump='SALTO',dash='IMPULSO',attack='PULSO',interact='USAR')[name]
            cx,cy=box[0]+box[2]/2,box[1]+box[3]/2
            if name in ('left','right'):
                sign=-1 if name=='left' else 1
                polygon(self.canvas,PAPER,[(cx+sign*18,cy),(cx-sign*10,cy-18),(cx-sign*10,cy+18)])
            elif name=='drop':polygon(self.canvas,PAPER,[(cx-17,cy-9),(cx+17,cy-9),(cx,cy+17)])
            elif name=='attack':
                pg.draw.circle(self.canvas,PAPER,(cx,cy),11,2)
                line(self.canvas,PAPER,(cx-17,cy),(cx+17,cy),2);line(self.canvas,PAPER,(cx,cy-17),(cx,cy+17),2)
            elif name=='jump':
                line(self.canvas,PAPER,(cx,cy+15),(cx,cy-13),3);polygon(self.canvas,PAPER,[(cx,cy-18),(cx-10,cy-4),(cx+10,cy-4)])
            elif name=='dash':polygon(self.canvas,PAPER,[(cx+4,cy-20),(cx-13,cy+3),(cx-1,cy+3),(cx-5,cy+20),(cx+14,cy-5),(cx+3,cy-5)])
            else:text(self.canvas,'E',(cx,cy),23,PAPER,True,'center')
    def binding_event(self,event):
        if self.state!='accessibility' or not self.rebind_action or event.type!=pg.KEYDOWN:return False
        if event.key==pg.K_ESCAPE:self.rebind_action=None;return True
        if event.key in (pg.K_F11,pg.K_F12,pg.K_m):return True
        if event.key in {self.key_for(a) for a in DEFAULT_KEYS if a!=self.rebind_action} or event.key in (pg.K_UP,pg.K_DOWN,pg.K_LEFT,pg.K_RIGHT,pg.K_u,pg.K_c,pg.K_v,pg.K_r):
            self.access_message='Esa tecla ya tiene otra acción. Elige otra.';return True
        self.save.data['key_bindings'][self.rebind_action]=event.key;self.save.write();self.rebind_action=None;return True
