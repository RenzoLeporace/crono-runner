from .campaign import TOTAL_LEVELS
"""Offline aliases, isolated progress, optional teacher PIN and fair rankings."""
import hashlib
import hmac
import json
import os
from pathlib import Path
import secrets
from .save import Save,save_path
from .storage import atomic_replace
from .i18n import literal

def atomic_json(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
    atomic_replace(temporary,path)
    from .mobile import persist
    persist(path)

def clean_label(value,limit=48):
    return literal(' '.join(str(value).split())[:limit])

def valid_records(records):
    result={}
    if not isinstance(records,dict):return result
    for key,value in records.items():
        if str(key).isdigit() and 0<=int(key)<TOTAL_LEVELS and isinstance(value,dict) and type(value.get('score')) is int and 0<=value['score']<=100000:
            canonical=str(int(key))
            if value['score']>result.get(canonical,{}).get('score',-1):result[canonical]=dict(value)
    return result

def rankings(rows,classroom=None,institution=None):
    """Each alias contributes only its best verified local score per map."""
    result=[]
    for row in rows:
        if row.get('role')=='teacher':continue
        if classroom is not None and row.get('classroom')!=classroom:continue
        if institution is not None and row.get('institution')!=institution:continue
        records=valid_records(row.get('records',{}))
        normalized={}
        for key,r in records.items():
            if str(key).isdigit() and 0<=int(key)<TOTAL_LEVELS and isinstance(r,dict) and type(r.get('score')) is int and 0<=r['score']<=100000:
                normalized[str(int(key))]=max(normalized.get(str(int(key)),0),r['score'])
        scores=list(normalized.values())
        result.append(dict(alias=clean_label(row.get('alias','Explorador')),classroom=clean_label(row.get('classroom','')),
            institution=clean_label(row.get('institution','')),score=sum(scores),maps=len(scores)))
    return sorted(result,key=lambda r:(-r['score'],-r['maps'],r['alias'].casefold()))

class School:
    def __init__(self,root=None):
        self.root=Path(root) if root else save_path().parent
        self.path=self.root/'perfiles.json';self.config_path=self.root/'docente.json'
        self.data=dict(active='legacy',profiles=[dict(id='legacy',alias='Explorador',classroom='Mi clase',institution='Mi institución',role='student')])
        self.config=dict(pin=None,topics=[])
        for path,target in ((self.path,self.data),(self.config_path,self.config)):
            try:
                raw=json.loads(path.read_text(encoding='utf-8'))
                if isinstance(raw,dict):target.update(raw)
            except (OSError,ValueError):pass
        profiles=self.data.get('profiles',[])
        self.data['profiles']=[];used=set()
        for p in profiles if isinstance(profiles,list) else []:
            if not isinstance(p,dict):continue
            key=p.get('id')
            if not isinstance(key,str) or key in used or not (key=='legacy' or len(key)==24 and all(c in '0123456789abcdef' for c in key)):continue
            used.add(key)
            self.data['profiles'].append(dict(id=key,alias=clean_label(p.get('alias','Explorador')) or 'Explorador',
                classroom=clean_label(p.get('classroom','Mi clase')),institution=clean_label(p.get('institution','Mi institución')),
                role='teacher' if p.get('role')=='teacher' else 'student'))
        if not self.data['profiles']:self.data['profiles']=[dict(id='legacy',alias='Explorador',classroom='Mi clase',institution='Mi institución',role='student')]
        if not isinstance(self.data.get('active'),str) or self.data['active'] not in {p['id'] for p in self.data['profiles']}:self.data['active']=self.data['profiles'][0]['id']
        topics=self.config.get('topics',[])
        self.config['topics']=sorted({i for i in topics if type(i) is int and 0<=i<72}) if isinstance(topics,list) else []

    @property
    def active(self):return next(p for p in self.data['profiles'] if p['id']==self.data['active'])
    def progress_path(self,key):return self.root/'progreso.json' if key=='legacy' else self.root/'perfiles'/key/'progreso.json'
    def save(self):atomic_json(self.path,self.data)
    def create(self,alias,classroom,institution,role='student'):
        alias=clean_label(alias)
        if not alias:raise ValueError('Escribe un alias.')
        profile=dict(id=secrets.token_hex(12),alias=alias,classroom=clean_label(classroom),institution=clean_label(institution),role='teacher' if role=='teacher' else 'student')
        self.data['profiles'].append(profile);self.data['active']=profile['id'];self.save();return profile
    def select(self,key):
        if key not in {p['id'] for p in self.data['profiles']}:raise ValueError('Perfil desconocido.')
        self.data['active']=key;self.save();return Save(self.progress_path(key))
    def delete(self,key):
        from .mobile import delete
        delete(self.progress_path(key))
        if key=='legacy':
            Save(self.progress_path(key)).path.unlink(missing_ok=True)
        else:
            self.progress_path(key).unlink(missing_ok=True)
        self.data['profiles']=[p for p in self.data['profiles'] if p['id']!=key]
        if not self.data['profiles']:
            self.data['profiles']=[dict(id='legacy',alias='Explorador',classroom='Mi clase',institution='Mi institución',role='student')]
        self.data['active']=self.data['profiles'][0]['id'];self.save()
    def rows(self):
        return [dict(p,records=Save(self.progress_path(p['id'])).data['records']) for p in self.data['profiles'] if p.get('role')!='teacher']
    def set_pin(self,pin):
        if pin and (len(pin)<4 or len(pin)>64):raise ValueError('El PIN debe tener entre 4 y 64 caracteres.')
        salt=secrets.token_hex(16)
        self.config['pin']=dict(salt=salt,digest=hashlib.pbkdf2_hmac('sha256',pin.encode(),bytes.fromhex(salt),180000).hex()) if pin else None
        atomic_json(self.config_path,self.config)
    def check_pin(self,pin):
        saved=self.config.get('pin')
        if not saved:return True
        try:return hmac.compare_digest(saved['digest'],hashlib.pbkdf2_hmac('sha256',pin.encode(),bytes.fromhex(saved['salt']),180000).hex())
        except (ValueError,TypeError,KeyError):return False
