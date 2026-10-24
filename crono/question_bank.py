"""Editable local curriculum, separate from student progress and bundled code."""
from collections import Counter
from copy import deepcopy
from datetime import datetime
import json
import os
from pathlib import Path
import random
import sys
from .education import LESSONS, SOURCES, Question, fact_for


def content_path():
    root=Path(sys.executable).parent if getattr(sys,'frozen',False) else Path(__file__).resolve().parents[1]
    return root/'contenido'/'preguntas.json'


def builtin_records():
    return [dict(id=(topic*6 if topic<30 else 10000+(topic-30)*6)+variant,topic=topic,band=variant//2,prompt=q[0],
                 options=list(q[1:]),correct=0,explanation=fact_for(topic,variant//2),
                 source=SOURCES[lesson.source][1])
            for topic,lesson in enumerate(LESSONS) for variant,q in enumerate(lesson.questions)]


def validate_record(value):
    if not isinstance(value,dict):
        raise ValueError('La pregunta no tiene un formato válido.')
    record={}
    for key,minimum,maximum in (('id',0,10**9),('topic',0,len(LESSONS)-1),('band',0,2),('correct',0,2)):
        item=value.get(key)
        if type(item) is not int or not minimum<=item<=maximum:
            raise ValueError(f'El campo {key} no es válido.')
        record[key]=item
    for key,limit,required in (('prompt',220,True),('explanation',700,True),('source',300,False)):
        item=value.get(key,'')
        if not isinstance(item,str) or len(item.strip())>limit or (required and not item.strip()):
            name=dict(prompt='pregunta',explanation='explicación',source='fuente')[key]
            raise ValueError(f'Revisa {name}: '+(f'es obligatoria y admite hasta {limit} caracteres.' if required else f'admite hasta {limit} caracteres.'))
        record[key]=item.strip()
    options=value.get('options')
    if not isinstance(options,list) or len(options)!=3 or any(not isinstance(o,str) or not o.strip() or len(o.strip())>180 for o in options):
        raise ValueError('Completa las tres respuestas; cada una admite hasta 180 caracteres.')
    if len({o.strip().casefold() for o in options})!=3:
        raise ValueError('Las tres respuestas deben ser diferentes.')
    record['options']=[o.strip() for o in options]
    return record


class QuestionBank:
    def __init__(self,path=None):
        self.path=Path(path) if path else content_path()
        self.records=builtin_records()
        self.warning=''
        try:
            document=json.loads(self.path.read_text(encoding='utf-8-sig'))
            if not isinstance(document,dict) or document.get('version') not in (1,2) or not isinstance(document.get('questions'),list):
                raise ValueError('Formato de banco desconocido.')
            records=[validate_record(q) for q in document['questions']]
            if document['version']==1:
                # Old teacher IDs >=180 remain intact; new official IDs use 10000+.
                records.extend(q for q in builtin_records() if q['topic']>=30)
            if len({r['id'] for r in records})!=len(records):
                raise ValueError('Hay identificadores de pregunta repetidos.')
            self.validate_pools(records)
            self.records=records
        except FileNotFoundError:
            pass
        except (OSError,ValueError,TypeError) as error:
            self.warning=f'No se pudo cargar el banco local: {error} Se usan las preguntas originales; el archivo se conserva.'

    @staticmethod
    def validate_pools(records):
        counts=Counter((q['topic'],q['band']) for q in records)
        if any(counts[(topic,band)]<1 for topic in range(len(LESSONS)) for band in range(3)):
            raise ValueError('Cada archivo y edad debe conservar al menos una pregunta. Agrega un reemplazo antes de cambiar esta asignación.')

    def get(self,question_id):
        return deepcopy(next(q for q in self.records if q['id']==question_id))

    def filtered(self,era=-1,stage=-1,band=-1,query=''):
        query=query.casefold().strip()
        return [deepcopy(q) for q in sorted(self.records,key=lambda r:(r['topic'],r['band'],r['id']))
                if (era<0 or q['topic']//6==era)
                and (stage<0 or q['topic']//2%3==stage)
                and (band<0 or q['band']==band)
                and (not query or query in ' '.join([q['prompt'],*q['options'],q['explanation']]).casefold())]

    def choose(self,topic,band,rng=None,previous=None):
        rng=rng or random
        pool=[q for q in self.records if q['topic']==topic and q['band']==band]
        if len(pool)>1:
            pool=[q for q in pool if q['id']!=previous]
        record=rng.choice(pool)
        order=list(range(3))
        rng.shuffle(order)
        return Question(record['id'],topic,record['prompt'],tuple(record['options'][i] for i in order),
                        order.index(record['correct']),record['explanation'],record['source'])

    def backup(self):
        folder=self.path.parent/'respaldos'
        folder.mkdir(parents=True,exist_ok=True)
        target=folder/f'preguntas-{datetime.now():%Y%m%d-%H%M%S-%f}.json'
        content=self.path.read_bytes() if self.path.exists() else self.serialise(self.records).encode('utf-8')
        target.write_bytes(content)
        return target

    @staticmethod
    def serialise(records):
        return json.dumps(dict(version=2,questions=records),ensure_ascii=False,indent=2)+'\n'

    def upsert(self,draft):
        candidate=deepcopy(draft)
        if candidate.get('id') is None:
            candidate['id']=max((q['id'] for q in self.records),default=179)+1
        candidate=validate_record(candidate)
        records=[deepcopy(q) for q in self.records if q['id']!=candidate['id']]+[candidate]
        self.validate_pools(records)
        self.path.parent.mkdir(parents=True,exist_ok=True)
        if self.path.exists():
            self.backup()
        temporary=self.path.with_suffix('.tmp')
        temporary.write_text(self.serialise(records),encoding='utf-8')
        os.replace(temporary,self.path)
        self.records=records
        self.warning=''
        return candidate['id']
