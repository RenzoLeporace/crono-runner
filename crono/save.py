"""Validated atomic saves, educational progression and migration from beta 0.2."""
import json
import math
import os
from pathlib import Path
import sys
from .education import UPGRADES


def save_path():
    root=Path(sys.executable).parent if getattr(sys,'frozen',False) else Path(__file__).resolve().parents[1]
    return root/'saves'/'progreso.json'


def defaults():
    return dict(version=2,unlocked=0,current=0,started=False,finished=False,
                sound=True,fullscreen=False,progress=None,records={},age_band=1,
                knowledge=0,upgrades=[],solved=[],discovered=[])


def valid_ids(values,total):
    return sorted({i for i in values if type(i) is int and 0<=i<total}) if isinstance(values,list) else []


class Save:
    def __init__(self,path=None):
        self.path=Path(path) if path else save_path()
        self.data=defaults()
        self.warning=''
        self.legacy_bytes=None
        try:
            raw_bytes=self.path.read_bytes()
            raw=json.loads(raw_bytes.decode('utf-8-sig'))
            if not isinstance(raw,dict) or raw.get('version') not in (1,2):
                raise ValueError('Formato de guardado desconocido')
            legacy=raw.get('version')==1
            if legacy:
                self.legacy_bytes=raw_bytes
            for key in ('unlocked','current'):
                value=raw.get(key,0)
                self.data[key]=max(0,min(14,value*(3 if legacy else 1))) if type(value) is int else 0
            for key in ('started','finished','sound','fullscreen'):
                if type(raw.get(key)) is bool:
                    self.data[key]=raw[key]
            if legacy:
                self.data['finished']=False
            age=raw.get('age_band',1)
            self.data['age_band']=age if type(age) is int and 0<=age<3 else 1
            for key in ('solved','discovered'):
                self.data[key]=valid_ids(raw.get(key,[]),30)
            knowledge=raw.get('knowledge',0)
            self.data['knowledge']=max(0,min(60,knowledge)) if type(knowledge) is int else 0
            upgrades=raw.get('upgrades',[])
            if isinstance(upgrades,list):
                self.data['upgrades']=[u['id'] for u in UPGRADES if u['id'] in upgrades]
            if 'vitality2' in self.data['upgrades'] and 'vitality' not in self.data['upgrades']:
                self.data['upgrades'].remove('vitality2')
            records=raw.get('records',{})
            if isinstance(records,dict):
                self.data['records']={str(int(k)*3 if legacy else int(k)):v for k,v in records.items()
                                      if str(k).isdigit() and 0<=int(k)<(5 if legacy else 15) and isinstance(v,dict)}
            p=raw.get('progress')
            if isinstance(p,dict) and type(p.get('index')) is int and 0<=p['index']<=4:
                self.data['progress']=dict(p)
                stage=p.get('stage',0)
                self.data['progress']['stage']=stage if type(stage) is int and 0<=stage<3 else 0
        except FileNotFoundError:
            pass
        except (OSError,ValueError,TypeError):
            self.warning='No se pudo leer el guardado anterior. Puedes empezar un nuevo viaje.'

    def write(self):
        try:
            self.path.parent.mkdir(parents=True,exist_ok=True)
            if self.legacy_bytes is not None:
                backup=self.path.with_name(self.path.stem+'-v1-respaldo.json')
                if not backup.exists():
                    backup.write_bytes(self.legacy_bytes)
                self.legacy_bytes=None
            temporary=self.path.with_suffix('.tmp')
            temporary.write_text(json.dumps(self.data,ensure_ascii=False,indent=2),encoding='utf-8')
            os.replace(temporary,self.path)
            self.warning=''
        except OSError:
            self.warning='No se pudo guardar el progreso en esta carpeta.'

    def discover(self,topic):
        if topic not in self.data['discovered']:
            self.data['discovered'].append(topic)
            self.write()

    def answer(self,topic):
        if type(topic) is not int or not 0<=topic<30 or topic in self.data['solved']:
            return False
        self.data['solved'].append(topic)
        if topic not in self.data['discovered']:
            self.data['discovered'].append(topic)
        self.data['knowledge']+=2
        self.write()
        return True

    def buy(self,upgrade_id):
        item=next((u for u in UPGRADES if u['id']==upgrade_id),None)
        if not item or upgrade_id in self.data['upgrades'] or self.data['knowledge']<item['cost']:
            return False
        if item['requires'] and item['requires'] not in self.data['upgrades']:
            return False
        self.data['knowledge']-=item['cost']
        self.data['upgrades'].append(upgrade_id)
        self.write()
        return True

    def capture(self,world):
        self.data.update(started=True,current=world.level_id)
        self.data['upgrades']=sorted(world.upgrades)
        self.data['solved']=sorted(world.answered|set(self.data['solved']))
        self.data['progress']=dict(index=world.index,stage=world.stage,shards=sorted(world.shards),
            echoes=sorted(world.echoes),checkpoint=world.checkpoint,time=world.time,
            deaths=world.deaths,defeated=[i for i,e in enumerate(world.enemies) if not e.alive],
            enemy_hp=[e.hp if e.alive else 0 for e in world.enemies],boss_hp=world.boss.hp if world.boss else None)
        self.write()

    def restore(self,world):
        world.upgrades=set(self.data['upgrades'])
        world.answered=set(self.data['solved'])
        world.player.configure(world.upgrades,True)
        p=self.data.get('progress')
        if not p or p.get('index')!=world.index or p.get('stage',0)!=world.stage:
            return
        for key,total in (('shards',3),('echoes',len(world.data['echoes']))):
            setattr(world,key,set(valid_ids(p.get(key,[]),total)))
        checkpoint=p.get('checkpoint',-1)
        if type(checkpoint) is int and 0<=checkpoint<len(world.data['checkpoints']):
            world.checkpoint=checkpoint
            x,y=world.data['checkpoints'][checkpoint]
            world.spawn=(x-14,y-64)
            world.player.rect.topleft=world.spawn
        for key in ('time','deaths'):
            value=p.get(key,0)
            if type(value) in (int,float) and math.isfinite(value) and 0<=value<1e9:
                setattr(world,key,value)
        for i in valid_ids(p.get('defeated',[]),len(world.enemies)):
            world.enemies[i].alive=False
            world.enemies[i].hp=0
        health=p.get('enemy_hp',[])
        if isinstance(health,list):
            for e,hp in zip(world.enemies,health):
                if type(hp) is int:
                    e.hp=max(0,min(e.max_hp,hp))
                    e.alive=e.hp>0
        if world.boss and type(p.get('boss_hp')) is int:
            world.boss.hp=max(0,min(world.boss.max_hp,p['boss_hp']))
            world.boss.alive=world.boss.hp>0

    def completed(self,world):
        self.data['unlocked']=max(self.data['unlocked'],min(14,world.level_id+1))
        self.data['current']=min(14,world.level_id+1)
        self.data['started']=True
        self.data['progress']=None
        self.data['finished']=world.level_id==14 or self.data['finished']
        old=self.data['records'].get(str(world.level_id),{})
        previous=old.get('echoes',0)
        previous=previous if type(previous) is int else 0
        self.data['records'][str(world.level_id)]=dict(echoes=max(previous,len(world.echoes)),
                                                   time=round(world.time,2),deaths=world.deaths)
        self.write()
