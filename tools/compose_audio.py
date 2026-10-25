"""Compose original looping music and tactile effects. © Renzo Leporace."""
from array import array
import math
from pathlib import Path
import random
import wave

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets'/'audio';RATE=22050

def save(name,values):
    OUT.mkdir(parents=True,exist_ok=True)
    pcm=array('h',(round(max(-.94,min(.94,v))*32767) for v in values))
    with wave.open(str(OUT/(name+'.wav')),'wb') as file:file.setparams((1,2,RATE,0,'NONE','not compressed'));file.writeframes(pcm.tobytes())

def tone(buffer,start,length,freq,volume,voice='pluck'):
    first=int(start*RATE);count=int(length*RATE)
    for i in range(count):
        if first+i>=len(buffer):break
        t=i/RATE;attack=min(1,t/.018);release=min(1,(count-i)/(RATE*.08))
        envelope=attack*release*(math.exp(-t*4) if voice=='pluck' else .65+.35*math.sin(math.pi*i/count))
        value=math.sin(math.tau*freq*t)+(.2 if voice=='flute' else .32)*math.sin(math.tau*freq*2*t)
        buffer[first+i]+=volume*envelope*value

def main():
    scale=(0,2,3,5,7,10,12,14);pattern=(0,2,4,3,1,2,5,4,2,3,6,4,3,1,2,0)
    for era,root in enumerate((146.83,130.81,164.81,146.83,110.,123.47,164.81,146.83,138.59)):
        beat=.375;duration=beat*32;buffer=[0.]*(round(duration*RATE));rng=random.Random(40+era)
        for n in range(32):
            chord=(0,5,3,7)[n//8%4];degree=pattern[(n+era*2)%16]
            melody=root*2**(scale[degree]/12)
            tone(buffer,n*beat,beat*.87,melody,.075,'flute' if era in (1,2,7,8) else 'pluck')
            if n%2==0:tone(buffer,n*beat,beat*1.7,root*.5*2**(chord/12),.065)
            if n%4==0:
                tone(buffer,n*beat,.14,55,.07)
            if n%4==2:
                start=round(n*beat*RATE)
                for i in range(round(.065*RATE)):buffer[start+i]+=rng.uniform(-1,1)*.025*(1-i/(.065*RATE))**2
        save('era-'+str(era),buffer)
    effects={'jump':(390,570),'dash':(150,80),'echo':(880,1175),'shard':(523,659,784,1046),
             'checkpoint':(392,523,784),'hurt':(130,90),'death':(220,165,110),'stomp':(160,280),
             'ui':(620,),'portal':(262,330,392,523),'shot':(490,220),'shield':(690,440),
             'block':(180,270),'boss':(392,523,659,784),'heal':(440,554,659),'field_complete':(523,784,1046),'cannon':(70,42)}
    for name,notes in effects.items():
        buffer=[0.]*(round((len(notes)*.075+.14)*RATE))
        for i,note in enumerate(notes):tone(buffer,i*.075,.16,note,.18)
        save(name,buffer)
    (OUT/'LEEME.txt').write_text('Música y efectos originales generados por tools/compose_audio.py. © 2026 Renzo Leporace. Inspiración contemporánea; no reconstrucción de música antigua.\n',encoding='utf-8')
    print('9 composiciones originales y 17 efectos preparados.')

if __name__=='__main__':main()
