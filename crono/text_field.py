"""Pygame text editing with Unicode, selection, clipboard, wrapping and scrolling."""
import pygame as pg
from .art import font,rect,text,line,PAPER,MUTED,CYAN
from .i18n import literal


class TextField:
    def __init__(self,value='',limit=220,multiline=False):
        self.value=value
        self.limit=limit
        self.multiline=multiline
        self.cursor=len(value)
        self.anchor=self.cursor
        self.box=pg.Rect(0,0,1,1)
        self.focused=False
        self.scroll=0
        self.dragging=False
        self.size=17
        self.password=False
        self.lines=[(0,len(value))]

    def set_value(self,value):
        self.value=value
        self.cursor=len(value)
        self.anchor=self.cursor
        self.scroll=0

    def replace_selection(self,value):
        value=value.replace('\r\n','\n').replace('\r','\n')
        if not self.multiline:
            value=value.replace('\n',' ')
        a,b=sorted((self.cursor,self.anchor))
        capacity=self.limit-len(self.value)+(b-a)
        value=value[:max(0,capacity)]
        self.value=self.value[:a]+value+self.value[b:]
        self.cursor=a+len(value)
        self.anchor=self.cursor

    def move(self,target,select=False):
        self.cursor=max(0,min(len(self.value),target))
        if not select:
            self.anchor=self.cursor

    def layout(self):
        f=font(self.size)
        width=max(20,self.box.w-26)
        lines=[]
        start=0
        while start<len(self.value):
            end=start
            last_space=-1
            while end<len(self.value) and self.value[end]!='\n' and f.size(self.value[start:end+1])[0]<=width:
                if self.value[end]==' ':
                    last_space=end
                end+=1
            if end==len(self.value):
                lines.append((start,end))
                start=end
            elif self.value[end]=='\n':
                lines.append((start,end))
                start=end+1
            else:
                if last_space>=start:
                    end=last_space+1
                end=max(start+1,end)
                lines.append((start,end))
                start=end
        if not lines or self.value.endswith('\n'):
            lines.append((len(self.value),len(self.value)))
        self.lines=lines

    def row_for(self,index):
        for row,(a,b) in enumerate(self.lines):
            if a<=index<b or (a<=index<=b and row==len(self.lines)-1):
                return row
            if index==b and b<len(self.value) and self.value[b]=='\n':
                return row
        return len(self.lines)-1

    def index_at(self,pos):
        row=max(0,min(len(self.lines)-1,int((pos[1]-self.box.y-10)/24)+self.scroll))
        a,b=self.lines[row]
        x=pos[0]-self.box.x-12
        return min(range(a,b+1),key=lambda i:abs(font(self.size).size(self.value[a:i])[0]-x))

    def handle(self,event):
        if event.type==pg.MOUSEBUTTONDOWN and event.button==1 and self.box.collidepoint(event.pos):
            from .mobile import request_text
            request_text(self)
            self.focused=True
            self.layout()
            self.move(self.index_at(event.pos),bool(pg.key.get_mods()&pg.KMOD_SHIFT))
            self.dragging=True
            return True
        if event.type==pg.MOUSEBUTTONUP and event.button==1:
            self.dragging=False
        if event.type==pg.MOUSEMOTION and self.dragging:
            self.cursor=self.index_at(event.pos)
            return True
        if not self.focused:
            return False
        if event.type==pg.TEXTINPUT:
            self.replace_selection(event.text)
            return True
        if event.type!=pg.KEYDOWN:
            return False
        key=event.key
        mods=getattr(event,'mod',pg.key.get_mods())
        ctrl=bool(mods&pg.KMOD_CTRL)
        shift=bool(mods&pg.KMOD_SHIFT)
        if ctrl and key==pg.K_a:
            self.anchor=0
            self.cursor=len(self.value)
        elif ctrl and key in (pg.K_c,pg.K_x):
            try:
                a,b=sorted((self.cursor,self.anchor))
                pg.scrap.put_text(self.value[a:b])
                if key==pg.K_x:
                    self.replace_selection('')
            except pg.error:
                pass
        elif ctrl and key==pg.K_v:
            try:
                self.replace_selection(pg.scrap.get_text() or '')
            except pg.error:
                pass
        elif key in (pg.K_BACKSPACE,pg.K_DELETE):
            if self.cursor==self.anchor:
                if key==pg.K_BACKSPACE:
                    self.anchor=max(0,self.cursor-1)
                else:
                    self.anchor=min(len(self.value),self.cursor+1)
            self.replace_selection('')
        elif key in (pg.K_LEFT,pg.K_RIGHT):
            if not shift and self.anchor!=self.cursor:
                self.move(min(self.anchor,self.cursor) if key==pg.K_LEFT else max(self.anchor,self.cursor))
            else:
                self.move(self.cursor+(-1 if key==pg.K_LEFT else 1),shift)
        elif key in (pg.K_HOME,pg.K_END):
            self.layout()
            a,b=self.lines[self.row_for(self.cursor)]
            self.move((0 if key==pg.K_HOME else len(self.value)) if ctrl else (a if key==pg.K_HOME else b),shift)
        elif key in (pg.K_UP,pg.K_DOWN):
            self.layout()
            row=self.row_for(self.cursor)
            x=font(self.size).size(self.value[self.lines[row][0]:self.cursor])[0]
            dest=max(0,min(len(self.lines)-1,row+(-1 if key==pg.K_UP else 1)))
            a,b=self.lines[dest]
            self.move(min(range(a,b+1),key=lambda i:abs(font(self.size).size(self.value[a:i])[0]-x)),shift)
        elif key in (pg.K_RETURN,pg.K_KP_ENTER) and self.multiline and not ctrl:
            self.replace_selection('\n')
        return True

    def draw(self,surface,box,placeholder='',size=17):
        self.box=pg.Rect(box)
        self.size=size
        rect(surface,(24,41,51),self.box,5)
        pg.draw.rect(surface,CYAN if self.focused else (61,84,94),self.box,2 if self.focused else 1,border_radius=5)
        self.layout()
        rows=max(1,(self.box.h-17)//24)
        caret_row=self.row_for(self.cursor)
        if self.focused:
            self.scroll=max(0,min(self.scroll,caret_row))
            if caret_row>=self.scroll+rows:
                self.scroll=caret_row-rows+1
        self.scroll=min(self.scroll,max(0,len(self.lines)-rows))
        old_clip=surface.get_clip()
        surface.set_clip(self.box.inflate(-16,-8))
        a,b=sorted((self.cursor,self.anchor))
        if not self.value:
            text(surface,placeholder,(self.box.x+12,self.box.y+10),size,MUTED)
        for row in range(self.scroll,min(len(self.lines),self.scroll+rows)):
            start,end=self.lines[row]
            y=self.box.y+10+(row-self.scroll)*24
            if self.focused and a<b and b>start and a<end:
                left=max(start,a)
                right=min(end,b)
                xx=self.box.x+12+font(size).size(self.value[start:left])[0]
                ww=font(size).size(self.value[left:right])[0]
                rect(surface,(54,105,111),(xx,y,ww,23))
            text(surface,literal('*'*(end-start) if self.password else self.value[start:end]),(self.box.x+12,y),size,PAPER)
            if self.focused and row==caret_row and pg.time.get_ticks()%1000<650:
                xx=self.box.x+12+font(size).size(self.value[start:self.cursor])[0]
                line(surface,CYAN,(xx,y),(xx,y+21),2)
        surface.set_clip(old_clip)
        if len(self.lines)>rows:
            text(surface,f'{self.scroll+1}/{len(self.lines)}',(self.box.right-5,self.box.bottom-2),9,MUTED,False,'bottomright')
