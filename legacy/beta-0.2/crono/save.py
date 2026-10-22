"""Portable atomic saves with validation and corruption recovery."""
import json
import os
from pathlib import Path
import sys


def save_path():
    root=Path(sys.executable).parent if getattr(sys,'frozen',False) else Path(__file__).resolve().parents[1]
    return root/'saves'/'progreso.json'


def defaults():
    return dict(version=1,unlocked=0,current=0,started=False,finished=False,
                sound=True,fullscreen=False,progress=None,records={})


class Save:
    def __init__(self,path=None):
        self.path=Path(path) if path else save_path()
        self.data=defaults()
        self.warning=''
        try:
            raw=json.loads(self.path.read_text(encoding='utf-8'))
            if not isinstance(raw,dict) or raw.get('version')!=1:
                raise ValueError('Formato de guardado desconocido')
            for key in ('unlocked','current'):
                value=raw.get(key,0)
                self.data[key]=max(0,min(4,value)) if type(value) is int else 0
            for key in ('started','finished','sound','fullscreen'):
                if type(raw.get(key)) is bool:
                    self.data[key]=raw[key]
            if isinstance(raw.get('records'),dict):
                self.data['records']=raw['records']
            p=raw.get('progress')
            if isinstance(p,dict) and type(p.get('index')) is int and 0<=p['index']<=4:
                self.data['progress']=p
        except FileNotFoundError:
            pass
        except (OSError,ValueError,TypeError):
            self.warning='No se pudo leer el guardado anterior. Puedes empezar un nuevo viaje.'

    def write(self):
        try:
            self.path.parent.mkdir(parents=True,exist_ok=True)
            temporary=self.path.with_suffix('.tmp')
            temporary.write_text(json.dumps(self.data,ensure_ascii=False,indent=2),encoding='utf-8')
            os.replace(temporary,self.path)
            self.warning=''
        except OSError:
            self.warning='No se pudo guardar el progreso en esta carpeta.'

    def capture(self,world):
        self.data.update(started=True,current=world.index)
        self.data['progress']=dict(index=world.index,shards=sorted(world.shards),
            echoes=sorted(world.echoes),checkpoint=world.checkpoint,time=world.time,
            deaths=world.deaths,defeated=[i for i,e in enumerate(world.enemies) if not e.alive])
        self.write()

    def restore(self,world):
        p=self.data.get('progress')
        if not p or p.get('index')!=world.index:
            return
        for key,total in (('shards',3),('echoes',len(world.data['echoes']))):
            values=p.get(key,[])
            if isinstance(values,list):
                setattr(world,key,{i for i in values if type(i) is int and 0<=i<total})
        checkpoint=p.get('checkpoint',-1)
        if type(checkpoint) is int and 0<=checkpoint<len(world.data['checkpoints']):
            world.checkpoint=checkpoint
            x,y=world.data['checkpoints'][checkpoint]
            world.spawn=(x-14,y-64)
            world.player.rect.topleft=world.spawn
        for key in ('time','deaths'):
            value=p.get(key,0)
            if type(value) in (int,float) and 0<=value<1e9:
                setattr(world,key,value)
        defeated=p.get('defeated',[])
        if isinstance(defeated,list):
            for i in defeated:
                if type(i) is int and 0<=i<len(world.enemies):
                    world.enemies[i].alive=False

    def completed(self,world):
        self.data['unlocked']=max(self.data['unlocked'],min(4,world.index+1))
        self.data['current']=min(4,world.index+1)
        self.data['progress']=None
        self.data['finished']=world.index==4 or self.data['finished']
        old=self.data['records'].get(str(world.index),{})
        if not isinstance(old,dict):
            old={}
        previous=old.get('echoes',0)
        previous=previous if type(previous) is int else 0
        self.data['records'][str(world.index)]=dict(echoes=max(previous,len(world.echoes)),
                                                   time=round(world.time,2),deaths=world.deaths)
        self.write()
