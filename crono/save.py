"""Validated atomic saves, educational progression and migration from beta 0.2."""
import json
import math
import os
from pathlib import Path
import sys
from .education import UPGRADES,LESSONS
from .campaign import MAIN_LEVELS,TOTAL_LEVELS,DLC_START,MAIN_LEVEL_IDS,DLC_LEVEL_IDS,is_dlc,rank,successor,final_level,is_bonus,is_rift
from .progression import Progression,extra_defaults,load_extra,progress_slot
from .storage import atomic_replace


def save_path():
    root=Path(sys.executable).parent if getattr(sys,'frozen',False) else Path(__file__).resolve().parents[1]
    return root/'saves'/'progreso.json'


def defaults():
    result=dict(version=5,unlocked=0,current=0,started=False,finished=False,
                dlc_unlocked=DLC_START,dlc_current=DLC_START,dlc_started=False,dlc_finished=False,dlc_progress=None,
                sound=True,fullscreen=False,progress=None,records={},age_band=1,
                knowledge=0,upgrades=[],solved=[],discovered=[])
    result.update(extra_defaults())
    return result


def valid_ids(values,total):
    return sorted({i for i in values if type(i) is int and 0<=i<total}) if isinstance(values,list) else []


class Save(Progression):
    def __init__(self,path=None):
        self.path=Path(path) if path else save_path()
        self.data=defaults()
        self.warning=''
        self.legacy_bytes=None
        try:
            from .mobile import ensure_file
            ensure_file(self.path)
            raw_bytes=self.path.read_bytes()
            raw=json.loads(raw_bytes.decode('utf-8-sig'))
            if not isinstance(raw,dict) or raw.get('version') not in (1,2,3,4,5):
                raise ValueError('Formato de guardado desconocido')
            legacy=raw.get('version')==1
            self.data.update(load_extra(raw))
            if raw.get('version') in (1,2,3,4):
                self.legacy_bytes=raw_bytes
            for key in ('unlocked','current'):
                value=raw.get(key,0)
                candidate=value*(3 if legacy else 1) if type(value) is int else 0
                self.data[key]=candidate if candidate in MAIN_LEVEL_IDS else 0
            for key in ('dlc_unlocked','dlc_current'):
                value=raw.get(key,DLC_START)
                self.data[key]=value if type(value) is int and value in DLC_LEVEL_IDS else DLC_START
            for key in ('started','finished','sound','fullscreen','dlc_started','dlc_finished'):
                if type(raw.get(key)) is bool:
                    self.data[key]=raw[key]
            if legacy:
                self.data['finished']=False
            if raw.get('version')==2 and raw.get('finished'):
                self.data.update(finished=False,current=15,unlocked=max(15,self.data['unlocked']))
            age=raw.get('age_band',1)
            self.data['age_band']=age if type(age) is int and 0<=age<3 else 1
            for key in ('solved','discovered'):
                self.data[key]=valid_ids(raw.get(key,[]),len(LESSONS))
            knowledge=raw.get('knowledge',0)
            self.data['knowledge']=max(0,min(len(LESSONS)*2,knowledge)) if type(knowledge) is int else 0
            upgrades=raw.get('upgrades',[])
            if isinstance(upgrades,list):
                self.data['upgrades']=[u['id'] for u in UPGRADES if u['id'] in upgrades]
            if 'vitality2' in self.data['upgrades'] and 'vitality' not in self.data['upgrades']:
                self.data['upgrades'].remove('vitality2')
            records=raw.get('records',{})
            if isinstance(records,dict):
                self.data['records']={str(int(k)*3 if legacy else int(k)):v for k,v in records.items()
                                      if str(k).isdigit() and 0<=int(k)<(5 if legacy else TOTAL_LEVELS) and isinstance(v,dict)}
            p=raw.get('progress')
            if isinstance(p,dict) and type(p.get('index')) is int and p['index'] in (0,1,2,3,4,5,6,8):
                self.data['progress']=dict(p)
                stage=p.get('stage',0)
                self.data['progress']['stage']=stage if type(stage) is int and 0<=stage<3 else 0
            p=raw.get('dlc_progress')
            if isinstance(p,dict) and type(p.get('index')) is int and type(p.get('stage')) is int and p['index']*3+p['stage'] in DLC_LEVEL_IDS and 0<=p['stage']<3:
                self.data['dlc_progress']=dict(p)
        except FileNotFoundError:
            pass
        except (OSError,ValueError,TypeError):
            self.warning='No se pudo leer el guardado anterior. Puedes empezar un nuevo viaje.'

    def write(self):
        try:
            self.path.parent.mkdir(parents=True,exist_ok=True)
            if self.legacy_bytes is not None:
                version=json.loads(self.legacy_bytes.decode('utf-8-sig')).get('version',1)
                backup=self.path.with_name(self.path.stem+f'-v{version}-respaldo.json')
                if not backup.exists():
                    backup.write_bytes(self.legacy_bytes)
                    from .mobile import persist
                    persist(backup)
                self.legacy_bytes=None
            temporary=self.path.with_suffix('.tmp')
            temporary.write_text(json.dumps(self.data,ensure_ascii=False,indent=2),encoding='utf-8')
            atomic_replace(temporary,self.path)
            from .mobile import persist
            persist(self.path)
            self.warning=''
        except OSError:
            self.warning='No se pudo guardar el progreso en esta carpeta.'

    def discover(self,topic):
        if self.data['practice']:return
        if topic not in self.data['discovered']:
            self.data['discovered'].append(topic)
            self.write()

    def answer(self,topic):
        if self.data['practice']:return False
        if type(topic) is not int or not 0<=topic<len(LESSONS) or topic in self.data['solved']:
            return False
        self.data['solved'].append(topic)
        if topic not in self.data['discovered']:
            self.data['discovered'].append(topic)
        self.data['knowledge']+=2
        self.write()
        return True

    def buy(self,upgrade_id):
        if self.data['practice']:return False
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
        if self.data['practice']:return
        self.bank_world(world)
        dlc=is_dlc(world.level_id)
        if not is_bonus(world.level_id) and not is_rift(world.level_id):
            self.data.update(**({'dlc_started':True,'dlc_current':world.level_id} if dlc else {'started':True,'current':world.level_id}))
        from .education import UPGRADES
        self.data['upgrades']=sorted(world.upgrades&{u['id'] for u in UPGRADES})
        self.data['solved']=sorted(world.answered|set(self.data['solved']))
        progress=dict(layout_version=world.data['layout_version'],index=world.index,stage=world.stage,shards=sorted(world.shards),
            echoes=sorted(world.echoes),checkpoint=world.checkpoint,time=world.time,
            deaths=world.deaths,boss_deaths_start=world.boss_deaths_start,defeated=[i for i,e in enumerate(world.enemies) if not e.alive],
            enemy_hp=[e.hp if e.alive else 0 for e in world.enemies],boss_hp=world.boss.hp if world.boss else None,
            mechanics=getattr(getattr(world,'mechanic',None),'state',{}),
            curiosities=sorted(getattr(world,'curiosities_this_run',set())),
            rescues=sorted(getattr(world,'rescues_this_run',set())),lowest_difficulty=getattr(world,'lowest_difficulty',world.difficulty))
        slot=progress_slot(world.level_id)
        if slot in ('bonus_progress','rift_progress'):self.data[slot][str(world.level_id)]=progress
        else:self.data[slot]=progress
        self.refresh_achievements()
        self.write()

    def restore(self,world):
        world.upgrades=self.effective_upgrades()
        world.answered=set(self.data['solved'])
        world.player.configure(world.upgrades,True)
        slot=progress_slot(world.level_id);p=self.data.get(slot)
        if slot in ('bonus_progress','rift_progress'):p=p.get(str(world.level_id)) if isinstance(p,dict) else None
        if not isinstance(p,dict) or p.get('index')!=world.index or p.get('stage',0)!=world.stage:
            return
        world.curiosities_this_run=set(v for v in p.get('curiosities',[]) if isinstance(v,str)) if isinstance(p.get('curiosities',[]),list) else set()
        world.rescues_this_run=set(v for v in p.get('rescues',[]) if isinstance(v,str)) if isinstance(p.get('rescues',[]),list) else set()
        lowest=p.get('lowest_difficulty',world.difficulty)
        world.lowest_difficulty=min(world.difficulty,lowest) if type(lowest) is int and 0<=lowest<=2 else world.difficulty
        if hasattr(world,'mechanic') and isinstance(p.get('mechanics'),dict):world.mechanic.restore(p['mechanics'])
        if p.get('layout_version')!=world.data['layout_version']:
            # Checkpoint/enemy IDs belonged to a different route. Keep learning,
            # upgrades and the three already collected fragments, restart safely.
            world.shards=set(valid_ids(p.get('shards',[]),3))
            world.echoes=set(valid_ids(p.get('echoes',[]),len(world.data['echoes'])))
            world.say('Ruta renovada: conservas fragmentos, ecos y mejoras. Recorre las nuevas anclas.')
            return
        for key,total in (('shards',3),('echoes',len(world.data['echoes']))):
            setattr(world,key,set(valid_ids(p.get(key,[]),total)))
        checkpoint=p.get('checkpoint',-1)
        if type(checkpoint) is int and 0<=checkpoint<len(world.data['checkpoints']):
            world.select_checkpoint(checkpoint)
            world.player.rect.topleft=world.spawn
        for key in ('time','deaths'):
            value=p.get(key,0)
            if type(value) in (int,float) and math.isfinite(value) and 0<=value<1e9:
                setattr(world,key,value)
        start=p.get('boss_deaths_start')
        world.boss_deaths_start=start if type(start) is int and 0<=start<=world.deaths else None
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
        self.record_map(world)
        if self.data['practice']:self.write();return
        if is_bonus(world.level_id):
            self.data['bonus_progress'].pop(str(world.level_id),None);self.write();return
        if is_rift(world.level_id):
            self.data['rift_finished']=True
            if world.level_id not in self.data['rifts_completed']:
                self.data['rifts_completed'].append(world.level_id)
                if not self.data['practice']:self.data['coins']+=40
            self.data['rift_progress'].pop(str(world.level_id),None)
            self.refresh_achievements();self.write();return
        prefix='dlc_' if is_dlc(world.level_id) else ''
        following=successor(world.level_id)
        frontier=self.data[prefix+'unlocked']
        self.data[prefix+'unlocked']=max((frontier,following),key=rank)
        self.data[prefix+'current']=following
        self.data[prefix+'started']=True
        self.data[prefix+'progress']=None
        self.data[prefix+'finished']=final_level(world.level_id) or self.data[prefix+'finished']
        self.write()
