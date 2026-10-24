"""Code-native architecture for wars, contemporary cities and Argentina."""
import math
import pygame as pg
from .art import rect,line,circle,polygon,text,mix,PAPER,CYAN,GOLD,W
from .visuals import palette_for

def new_boss(s,b,x,y,t,color,dark,core):
    if b.era==5:
        pg.draw.ellipse(s,dark,(int(x-103),int(y-42),206,45))
        for dx in range(-76,90,29):circle(s,color,(x+dx,y-20),14,3)
        polygon(s,color,[(x-98,y-43),(x-68,y-112),(x+66,y-112),(x+99,y-43)])
        rect(s,dark,(x-35,y-148,72,43),8)
        line(s,color,(x,y-127),(x+b.direction*132,y-127),19)
    elif b.era==6:
        for j in range(6):
            a=t*.7+j*math.tau/6
            xx=x+math.cos(a)*95;yy=y-92+math.sin(a)*76
            line(s,dark,(x,y-78),(xx,yy),9)
            circle(s,color,(xx,yy),19);circle(s,core,(xx,yy),10,3)
        polygon(s,color,[(x-48,y-125),(x+48,y-125),(x+67,y-80),(x+28,y-20),(x-28,y-20),(x-67,y-80)])
    elif b.era==7:
        from .argentina_enemies import draw_carrier
        draw_carrier(s,b,x,y,t)
    else:
        from .egypt_art import sentinel
        sentinel(s,b,x,y,t,core)
