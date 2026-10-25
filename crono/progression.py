"""Local evidence, fair best-per-map scores and persistent exploration rewards."""
from copy import deepcopy
from datetime import datetime,timezone
import csv
from .campaign import MAIN_LEVEL_IDS,DLC_LEVEL_IDS,BONUS_LEVEL_IDS,RIFT_LEVEL_IDS,is_bonus,is_rift,unlocked

def extra_defaults():
    return dict(coins=0,banked_echoes=[],fragments_by_level={},curiosities_seen=[],rescued_ids=[],
        bonus_unlocked=[],rifts_completed=[],mechanics_completed=[],achievements=[],purchased_skins=[],
        skin_cards_seen=[],skin='crono',master_enabled=True,metrics={},attempts=[],reviews=[],
        bonus_progress={},rift_progress={},active_rift=None,rift_return=None,rift_finished=False,practice=False,
        motor_band=None,reading_size=19,key_bindings={},touch_controls=False,
        practice_records={},lowest_difficulty=1,session_room=None)

def load_extra(raw):
    result=extra_defaults()
    for key,value in result.items():
        candidate=raw.get(key,value)
        if value is None:
            if key in ('active_rift','motor_band'):result[key]=candidate if type(candidate) is int and (candidate in RIFT_LEVEL_IDS if key=='active_rift' else 0<=candidate<=2) else None
            elif candidate is None or isinstance(candidate,dict):result[key]=deepcopy(candidate)
        elif type(candidate) is type(value):result[key]=deepcopy(candidate)
    result['coins']=max(0,min(1000000,result['coins']))
    result['reading_size']=result['reading_size'] if result['reading_size'] in (19,22,25) else 19
    for key in ('banked_echoes','curiosities_seen','rescued_ids','achievements','purchased_skins','skin_cards_seen'):
        result[key]=sorted({v for v in result[key] if isinstance(v,str) and len(v)<100})
    for key,allowed in (('bonus_unlocked',BONUS_LEVEL_IDS),('rifts_completed',RIFT_LEVEL_IDS),('mechanics_completed',range(36))):
        result[key]=sorted({v for v in result[key] if type(v) is int and v in allowed})
    result['attempts']=[v for v in result['attempts'][-10000:] if isinstance(v,dict)]
    for key in ('bonus_progress','rift_progress'):
        result[key]={str(k):v for k,v in result[key].items() if str(k).isdigit() and isinstance(v,dict)}
    result['fragments_by_level']={str(k):[i for i in v if type(i) is int and 0<=i<3] for k,v in result['fragments_by_level'].items() if str(k).isdigit() and isinstance(v,list)}
    metrics={}
    for k,v in result['metrics'].items():
        if not isinstance(k,str):continue
        if k in ('defeated_kinds','defeated_boss_eras'):
            metrics[k]=[i for i in v if type(i) is (str if k=='defeated_kinds' else int)] if isinstance(v,list) else []
        elif type(v) in (int,bool):metrics[k]=max(0,v)
    result['metrics']=metrics
    result['practice_records']={str(k):v for k,v in result['practice_records'].items() if str(k).isdigit() and isinstance(v,dict) and type(v.get('score')) is int}
    return result

def progress_slot(level):
    if is_rift(level):return 'rift_progress'
    if is_bonus(level):return 'bonus_progress'
    return 'dlc_progress' if level in DLC_LEVEL_IDS else 'progress'

def map_score(world):
    defeated=sum(not e.alive for e in world.enemies)
    discoveries=len(getattr(world,'curiosities_this_run',set()))
    mechanics=int(getattr(getattr(world,'mechanic',None),'completed',False))
    rescues=len(getattr(world,'rescues_this_run',set()))
    target=max(30,world.width/310*1.6)
    speed=round(2500*min(1,target/max(1,world.time)))
    exploration=len(world.echoes)*20+len(world.shards)*200+discoveries*350+mechanics*600+rescues*800
    combat=defeated*120+(1000 if world.boss and not world.boss.alive else 0)
    care=max(0,700-world.deaths*140)
    band=getattr(world,'lowest_difficulty',world.difficulty)
    total=round((speed+exploration+combat+care)*(1,1.15,1.3)[band])
    return dict(score=total,speed_points=speed,exploration_points=exploration,combat_points=combat,
        care_points=care,echoes=len(world.echoes),kills=defeated,discoveries=discoveries,
        mechanics=mechanics,rescues=rescues,time=round(world.time,2),deaths=world.deaths,difficulty=band)

class Progression:
    def combat_band(self):
        return self.data['age_band'] if self.data.get('motor_band') is None else self.data['motor_band']

    def effective_upgrades(self):
        from .education import UPGRADES
        result=set(self.data['upgrades'])
        if self.data.get('practice'):
            result.update(u['id'] for u in UPGRADES)
            if self.data.get('master_enabled'):result.add('chronista')
        if len(self.data.get('achievements',[]))>=60 and self.data.get('master_enabled'):result.add('chronista')
        return result

    def can_enter(self,level):
        if self.data.get('practice'):return True
        if is_bonus(level):return level in self.data['bonus_unlocked']
        if is_rift(level):return level==self.data.get('active_rift') or level in self.data['rifts_completed']
        return unlocked(level,self.data['dlc_unlocked'] if level in DLC_LEVEL_IDS else self.data['unlocked'])

    def bank_world(self,world):
        if self.data['practice']:return
        if world.mechanic.completed and world.level_id not in self.data['mechanics_completed']:
            self.data['mechanics_completed'].append(world.level_id);self.data['coins']+=15
        banked=set(self.data['banked_echoes']);keys={f'{world.level_id}:{i}' for i in world.echoes}
        if not self.data['practice']:self.data['coins']+=len(keys-banked)
        self.data['banked_echoes']=sorted(banked|keys)
        previous=set(self.data['fragments_by_level'].get(str(world.level_id),[]))
        self.data['fragments_by_level'][str(world.level_id)]=sorted(previous|world.shards)
        old=getattr(world,'persisted_metrics',{})
        for key,total in getattr(world,'metrics',{}).items():
            if type(total) is int:self.data['metrics'][key]=self.data['metrics'].get(key,0)+max(0,total-old.get(key,0))
        world.persisted_metrics=dict(getattr(world,'metrics',{}))
        kinds=set(self.data['metrics'].get('defeated_kinds',[]) if isinstance(self.data['metrics'].get('defeated_kinds',[]),list) else [])
        kinds.update(e.kind for e in world.enemies if not e.alive)
        self.data['metrics']['defeated_kinds']=sorted(kinds)

    def visit_curiosity(self,key,world):
        if self.data['practice']:
            world.curiosities_this_run.add(key);return
        if key not in self.data['curiosities_seen']:
            self.data['curiosities_seen'].append(key)
            self.data['coins']+=5 if not self.data['practice'] else 0
        if not hasattr(world,'curiosities_this_run'):world.curiosities_this_run=set()
        world.curiosities_this_run.add(key)
        self.refresh_achievements();self.write()

    def rescue(self,key,world):
        from .journeys import RESCUES
        if self.data['practice']:
            world.rescues_this_run.add(key);return True
        if key not in RESCUES or key in self.data['rescued_ids']:return False
        self.data['rescued_ids'].append(key);self.data['bonus_unlocked'].append(RESCUES[key]['bonus'])
        self.data['coins']+=20 if not self.data['practice'] else 0
        world.rescues_this_run.add(key);self.refresh_achievements();self.write();return True

    def record_attempt(self,question,choice,first):
        self.data['attempts'].append(dict(at=datetime.now(timezone.utc).isoformat(timespec='seconds'),
            question=question.id,topic=question.topic,band=self.data['age_band'],type=getattr(question,'kind','choice'),
            choice=choice,selected_text=question.options[choice],correct_text=question.options[question.correct],prompt=question.prompt,
            correct=choice==question.correct,first=first,practice=self.data['practice']))
        self.data['attempts']=self.data['attempts'][-10000:];self.write()

    def export_evidence(self,path,profile=None):
        path.parent.mkdir(parents=True,exist_ok=True);profile=profile or {}
        fields=('alias','classroom','institution','at','question','topic','band','type','prompt','choice','selected_text','correct_text','correct','first','practice','text')
        with path.open('w',encoding='utf-8-sig',newline='') as handle:
            writer=csv.DictWriter(handle,fieldnames=fields,extrasaction='ignore');writer.writeheader()
            for row in self.data['attempts']:writer.writerow(dict(profile,**row))
            for row in self.data['reviews']:
                if isinstance(row,dict):writer.writerow(dict(profile,**row,type='reflection'))
        return path

    def refresh_achievements(self):
        if self.data['practice']:return []
        try:
            from .achievements import earned
        except ImportError:return []
        before=set(self.data['achievements']);self.data['achievements']=sorted(before|earned(self.data))
        return sorted(set(self.data['achievements'])-before)

    def record_map(self,world):
        self.bank_world(world);record=map_score(world)
        key='practice_records' if self.data['practice'] else 'records'
        old=self.data[key].get(str(world.level_id),{})
        old_score=old.get('score',-1)
        if type(old_score) is not int or record['score']>old_score:self.data[key][str(world.level_id)]=record
        if self.data['practice']:return record
        if world.boss and not world.boss.alive:
            bosses=set(self.data['metrics'].get('defeated_boss_eras',[]));bosses.add(world.combat_era)
            self.data['metrics']['defeated_boss_eras']=sorted(bosses)
            topics={world.level_id*2,world.level_id*2+1}
            if topics&world.answered:self.data['metrics']['boss_with_lesson']=True
            if topics<=world.answered:self.data['metrics']['boss_with_two_lessons']=True
            if world.boss_deaths_start is not None and world.deaths==world.boss_deaths_start:self.data['metrics']['boss_without_death']=True
        if world.deaths==0:self.data['metrics']['level_without_death']=True
        self.refresh_achievements();return record
