"""Editable local curriculum, separate from student progress and bundled code."""
from collections import Counter
from copy import deepcopy
from datetime import datetime
import json
import hashlib
import os
from pathlib import Path
import random
import sys
from .education import LESSONS, SOURCES, Question, fact_for
from .storage import atomic_replace
from .i18n import Authored,tr,literal


def content_path():
    root=Path(sys.executable).parent if getattr(sys,'frozen',False) else Path(__file__).resolve().parents[1]
    return root/'contenido'/'preguntas.json'


def builtin_records():
    base=[dict(id=(topic*6 if topic<30 else 10000+(topic-30)*6 if topic<48 else 2000000+(topic-48)*6)+variant,topic=topic,band=variant//2,prompt=q[0],
                 options=list(q[1:]),correct=0,explanation=fact_for(topic,variant//2),
                 source=SOURCES[lesson.source][1])
            for topic,lesson in enumerate(LESSONS) for variant,q in enumerate(lesson.questions)]
    from .application_questions import records
    return base+records()


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
    record['kind']=value.get('kind','choice') if value.get('kind','choice') in ('choice','source','image','reason','chronology','curiosity') else 'choice'
    # Optional additions preserve the exact old record shape/fingerprints.
    language=value.get('language')
    if language is not None:
        if language not in ('es','pt-BR'):raise ValueError('Idioma de pregunta no válido.')
        record['language']=language
    translations=value.get('translations',{})
    if not isinstance(translations,dict) or any(code not in ('es','pt-BR') for code in translations):
        raise ValueError('Idioma de traducción no válido.')
    if translations:
        record['translations']={}
        for code,translated in translations.items():
            if not isinstance(translated,dict):raise ValueError('Traducción de pregunta no válida.')
            translated=validate_record(dict(record,id=record['id'],translations={},**{k:translated.get(k,record[k]) for k in ('prompt','options','explanation','source')}))
            record['translations'][code]={k:translated[k] for k in ('prompt','options','explanation','source')}
    return record


class QuestionBank:
    def __init__(self,path=None):
        self.path=Path(path) if path else content_path()
        self.records=builtin_records()
        self.original_explanations={q['id']:q['explanation'] for q in self.records}
        self.original_records={q['id']:validate_record(q) for q in self.records}
        self.warning=''
        try:
            from .mobile import ensure_file
            ensure_file(self.path)
            document=json.loads(self.path.read_text(encoding='utf-8-sig'))
            if not isinstance(document,dict) or document.get('version') not in (1,2,3,4,5,6,7) or not isinstance(document.get('questions'),list):
                raise ValueError('Formato de banco desconocido.')
            records=[validate_record(q) for q in document['questions']]
            records=self.migrate(records,document['version'])
            if len({r['id'] for r in records})!=len(records):
                raise ValueError('Hay identificadores de pregunta repetidos.')
            self.validate_pools(records)
            self.records=records
        except FileNotFoundError:
            pass
        except (OSError,ValueError,TypeError) as error:
            self.warning=f'No se pudo cargar el banco local: {error} Se usan las preguntas originales; el archivo se conserva.'

    @staticmethod
    def migrate(records,version):
        if version not in (1,2,3,4,5,6):return records
        first={1:30,2:48,3:54,4:72,5:92,6:92}[version]
        records=deepcopy(records);used={q['id']:q for q in records}
        for q in builtin_records():
            if q['topic']<first and not (version<4 and q['id']>=5000000):continue
            if q['id'] in used:
                if used[q['id']]['topic']==q['topic']:continue
                q['id']=max(used)+1
            used[q['id']]=q;records.append(q)
        from .curriculum_migration import V5_HASHES
        from .curriculum_v6 import V6_HASHES
        current={q['id']:q for q in builtin_records()}
        for i,q in enumerate(records):
            digest=hashlib.sha256(json.dumps(validate_record(q),sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
            if digest in (V5_HASHES.get(q['id']),V6_HASHES.get(q['id'])) and q['id'] in current:records[i]=deepcopy(current[q['id']])
        return records

    @staticmethod
    def validate_pools(records):
        counts=Counter((q['topic'],q['band']) for q in records)
        if any(counts[(topic,band)]<1 for topic in range(len(LESSONS)) for band in range(3)):
            raise ValueError('Cada archivo y edad debe conservar al menos una pregunta. Agrega un reemplazo antes de cambiar esta asignación.')

    def get(self,question_id):
        return deepcopy(next(q for q in self.records if q['id']==question_id))

    def display_record(self,record):
        """Localize a view, never the editable/persisted canonical bank."""
        result=deepcopy(record)
        bundled=validate_record(record)==self.original_records.get(record['id'])
        variants=record.get('translations',{});source_language=record.get('language','es')
        def field(key,value,index=None):
            choices={code:(v[key][index] if index is not None else v[key]) for code,v in variants.items()}
            choices.setdefault(source_language,value)
            return Authored(value,choices,bundled)
        for key in ('prompt','explanation','source'):result[key]=field(key,record[key])
        result['options']=[field('options',v,i) for i,v in enumerate(record['options'])]
        return result

    def question(self,record,order):
        view=self.display_record(record)
        return Question(record['id'],record['topic'],view['prompt'],tuple(view['options'][i] for i in order),
                        order.index(record['correct']),view['explanation'],view['source'],record.get('kind','choice'))

    def filtered(self,era=-1,stage=-1,band=-1,query=''):
        query=query.casefold().strip()
        from .campaign import chapter_for_level,chapter_levels
        return [deepcopy(q) for q in sorted(self.records,key=lambda r:(r['topic'],r['band'],r['id']))
                if (era<0 or chapter_for_level(q['topic']//2)==era)
                and (stage<0 or chapter_levels(chapter_for_level(q['topic']//2)).index(q['topic']//2)==stage)
                and (band<0 or q['band']==band)
                and (not query or query in ' '.join([q['prompt'],*q['options'],q['explanation'],*[str(tr(v)) for v in self.display_record(q)['options']],str(tr(self.display_record(q)['prompt']))]).casefold())]

    def choose(self,topic,band,rng=None,previous=None):
        rng=rng or random
        pool=[q for q in self.records if q['topic']==topic and q['band']==band]
        complete_pool=pool
        if band<2:
            authored={q[0] for q in LESSONS[topic].questions[:(band+1)*2]}
            # Original supplementary IDs must not expose six-year-olds to the
            # oldest band's wording. Teacher-authored edits retain priority.
            pool=[q for q in pool if q.get('kind')=='curiosity' or q['prompt'] in authored or validate_record(q)!=self.original_records.get(q['id'])]
            if not pool:pool=complete_pool  # A teacher may deliberately keep one replacement only.
        pool=list({(q['prompt'],tuple(q['options']),q['correct']):q for q in pool}.values())
        if len(pool)>1:
            pool=[q for q in pool if q['id']!=previous]
        record=rng.choice(pool)
        order=list(range(3))
        rng.shuffle(order)
        return self.question(record,order)

    def backup(self):
        folder=self.path.parent/'respaldos'
        folder.mkdir(parents=True,exist_ok=True)
        target=folder/f'preguntas-{datetime.now():%Y%m%d-%H%M%S-%f}.json'
        content=self.path.read_bytes() if self.path.exists() else self.serialise(self.records).encode('utf-8')
        target.write_bytes(content)
        from .mobile import persist
        persist(target)
        return target

    @staticmethod
    def serialise(records):
        return json.dumps(dict(version=7,questions=records),ensure_ascii=False,indent=2)+'\n'

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
        atomic_replace(temporary,self.path)
        from .mobile import persist
        persist(self.path)
        self.records=records
        self.warning=''
        return candidate['id']
