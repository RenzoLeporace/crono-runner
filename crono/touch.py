"""Landscape multitouch controls in logical coordinates, independent fingers."""
import pygame as pg
from .art import rect,text,line,polygon,CYAN,PAPER

DEFAULT_KEYS=dict(left=pg.K_a,right=pg.K_d,jump=pg.K_SPACE,dash=pg.K_LSHIFT,attack=pg.K_f,interact=pg.K_e,drop=pg.K_s,pause=pg.K_ESCAPE)
KEY_LABELS=dict(left='Izquierda',right='Derecha',jump='Saltar',dash='Impulso',attack='Disparar',interact='Interactuar',drop='Descender',pause='Pausa')
TOUCH_BOXES=dict(left=(28,563,100,105),right=(146,563,100,105),drop=(88,448,100,90),jump=(1128,553,122,118),dash=(996,553,109,118),attack=(1128,422,122,108),interact=(996,422,109,108))

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
        if self.state=='play':
            if event.type==pg.FINGERUP:self.fingers.pop(key,None);return True
            action=next((name for name,box in TOUCH_BOXES.items() if pg.Rect(box).collidepoint(pos)),None)
            previous=self.fingers.get(key);self.fingers[key]=action
            if event.type==pg.FINGERDOWN or action!=previous:
                if action=='jump':self.jump_pending=True
                elif action=='dash':self.dash_pending=True
                elif action=='attack':self.shoot_pending=True
                elif action=='interact':self.interact()
                elif pos[0]>1180 and pos[1]<100:self.set_state('pause')
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
            panel=pg.Surface((box[2],box[3]),pg.SRCALPHA);panel.fill((23,55,65,220) if active else (13,29,41,172))
            self.canvas.blit(panel,box[:2]);pg.draw.rect(self.canvas,CYAN if active else (134,169,174),box,2,border_radius=16)
            label=dict(left='◀',right='▶',drop='↓',jump='SALTO',dash='IMPULSO',attack='PULSO',interact='USAR')[name]
            cx,cy=box[0]+box[2]/2,box[1]+box[3]/2
            if name in ('left','right'):
                sign=-1 if name=='left' else 1
                polygon(self.canvas,PAPER,[(cx+sign*18,cy),(cx-sign*10,cy-18),(cx-sign*10,cy+18)])
            elif name=='drop':polygon(self.canvas,PAPER,[(cx-17,cy-9),(cx+17,cy-9),(cx,cy+17)])
            else:text(self.canvas,label,(cx,cy),17,PAPER,True,'center')
    def binding_event(self,event):
        if self.state!='accessibility' or not self.rebind_action or event.type!=pg.KEYDOWN:return False
        if event.key==pg.K_ESCAPE:self.rebind_action=None;return True
        if event.key in (pg.K_F11,pg.K_F12,pg.K_m):return True
        if event.key in {self.key_for(a) for a in DEFAULT_KEYS if a!=self.rebind_action} or event.key in (pg.K_UP,pg.K_DOWN,pg.K_LEFT,pg.K_RIGHT,pg.K_u,pg.K_c,pg.K_v,pg.K_r):
            self.access_message='Esa tecla ya tiene otra acción. Elige otra.';return True
        self.save.data['key_bindings'][self.rebind_action]=event.key;self.save.write();self.rebind_action=None;return True
