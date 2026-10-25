"""The current Argentine flag; historical scenes choose when it is appropriate."""
import math
from .art import rect,line,circle

def argentina(s,box):
    x,y,w,h=box
    for i,c in enumerate(((112,191,219),(241,237,211),(112,191,219))):rect(s,c,(x,y+h*i/3,w,h/3+1))
    cx,cy=x+w/2,y+h/2;r=h*.095
    for i in range(16):
        a=i*math.tau/16;line(s,(209,151,49),(cx+math.cos(a)*r,cy+math.sin(a)*r),(cx+math.cos(a)*r*1.7,cy+math.sin(a)*r*1.7),1)
    circle(s,(237,182,66),(cx,cy),r);circle(s,(174,124,44),(cx,cy),r,1)
