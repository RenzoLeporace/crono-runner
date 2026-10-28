"""Collect bundled text and build the offline locale with an optional local model.

The model/toolchain stays in ignored .android-build/localization, never in a game
package. Only our text catalog is shipped. No teacher banks or saves are read.
"""
import argparse
import ast
from collections import Counter
import json
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'assets'/'locales'/'pt-BR.json'
FIELD=re.compile(r'\{\d+\}')


def display_text(value):
    if not value or len(value)>1600 or not any(c.isalpha() for c in value):return False
    if value.startswith(('http','C:/','C:\\','<!','<html','\n<style>')):return False
    if '\n' in value or re.fullmatch(r'[\w./\\:-]+',value) and value.islower():return False
    return len(value)>1 and (' ' in value or any(c.isupper() or c in 'áéíóúñ¿¡' for c in value))


def collect():
    messages=set();templates=set()
    for p in sorted((ROOT/'crono').glob('*.py')):
        if p.stem.startswith(('curriculum_','i18n')):continue
        tree=ast.parse(p.read_text(encoding='utf8'))
        parents={id(child):node for node in ast.walk(tree) for child in ast.iter_child_nodes(node)}
        for node in ast.walk(tree):
            parent=parents.get(id(node))
            if isinstance(node,ast.Constant) and isinstance(node.value,str):
                if isinstance(parent,(ast.Expr,ast.JoinedStr)):continue
                if isinstance(parent,ast.Dict) and node in parent.keys:continue
                if display_text(node.value):messages.add(node.value)
            elif isinstance(node,ast.JoinedStr):
                parts=[];index=0
                for part in node.values:
                    if isinstance(part,ast.Constant):parts.append(part.value)
                    else:parts.append('{'+str(index)+'}');index+=1
                value=''.join(parts)
                if index and display_text(FIELD.sub('',value)):templates.add(value)
            elif isinstance(node,ast.BinOp) and isinstance(node.op,ast.Add):
                if isinstance(parent,ast.BinOp) and isinstance(parent.op,ast.Add):continue
                def flatten(v):
                    if isinstance(v,ast.BinOp) and isinstance(v.op,ast.Add):return flatten(v.left)+flatten(v.right)
                    return [v]
                parts=[];index=0
                for part in flatten(node):
                    if isinstance(part,ast.Constant) and isinstance(part.value,str):parts.append(part.value)
                    else:parts.append('{'+str(index)+'}');index+=1
                value=''.join(parts)
                if index and display_text(FIELD.sub('',value)):templates.add(value)
    sys.path[:0]=[str(ROOT),str(ROOT/'.vendor')]
    from crono.question_bank import builtin_records
    from crono.education import fact_for,LESSONS
    for q in builtin_records():
        messages.update(v for v in [q['prompt'],*q['options'],q['explanation'],q['source']] if v)
    for topic in range(len(LESSONS)):
        for band in range(3):messages.add(fact_for(topic,band))
    return sorted(messages),sorted(templates)


def generate(refine=False):
    root=ROOT/'.android-build'/'localization'
    sys.path.insert(0,str(root/'toolchain'))
    import ctranslate2
    import sentencepiece
    package=root/'model'/'translate-es_pt-1_0'
    tokenizer=sentencepiece.SentencePieceProcessor(model_file=str(package/'sentencepiece.model'))
    model=ctranslate2.Translator(str(package/'model'),device='cpu',compute_type='int8',intra_threads=6)
    catalog=json.loads(DEST.read_text(encoding='utf8')) if DEST.exists() else dict(language='pt-BR',messages={},templates={})
    messages,templates=collect()
    if refine:
        # Sentence-trained models can silently omit the second paragraph.
        # Translate each sentence separately, keeping original separators.
        todo=[];layouts={}
        for source in messages:
            if source.startswith(('http://','https://')):continue
            parts=re.split(r'(\n+|(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÑ¿¡]))',source)
            if len(parts)>1:
                layouts[source]=parts
                todo.extend(v for i,v in enumerate(parts) if i%2==0 and v.strip())
        units=list(dict.fromkeys(todo));translated={}
        for start in range(0,len(units),32):
            batch=units[start:start+32]
            results=model.translate_batch([tokenizer.encode(v,out_type=str) for v in batch],beam_size=4,max_decoding_length=512)
            translated.update((source,tokenizer.decode(result.hypotheses[0])) for source,result in zip(batch,results))
            print('sentences',min(start+32,len(units)),'/',len(units),flush=True)
        for source,parts in layouts.items():catalog['messages'][source]=''.join(translated.get(v,v) if i%2==0 else v for i,v in enumerate(parts))
    for kind,values in (('messages',messages),('templates',templates)):
        missing=[v for v in values if v not in catalog[kind]]
        for start in range(0,len(missing),32):
            batch=missing[start:start+32]
            results=model.translate_batch([tokenizer.encode(v,out_type=str) for v in batch],beam_size=4,max_decoding_length=512)
            for source,result in zip(batch,results):
                target=tokenizer.decode(result.hypotheses[0])
                # Numbers and interpolation slots carry historical/game data.
                if Counter(FIELD.findall(source))!=Counter(FIELD.findall(target)):
                    pieces=re.split(r'(\{\d+\})',source)
                    for i,piece in enumerate(pieces):
                        if piece.strip() and not FIELD.fullmatch(piece):
                            translated=model.translate_batch([tokenizer.encode(piece.strip(),out_type=str)],beam_size=4,max_decoding_length=512)[0]
                            pieces[i]=(' ' if piece.startswith(' ') else '')+tokenizer.decode(translated.hypotheses[0])+(' ' if piece.endswith(' ') else '')
                    target=''.join(pieces)
                catalog[kind][source]=target
            DEST.parent.mkdir(parents=True,exist_ok=True)
            DEST.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
            print(kind,min(start+32,len(missing)),'/',len(missing),flush=True)
    review=json.loads((ROOT/'tools'/'pt_BR_review.json').read_text(encoding='utf8'))
    for kind in ('messages','templates'):
        for source,target in catalog[kind].items():
            if source.startswith(('http://','https://')):target=source
            else:
                target=target.replace('¿','').replace('¡','')
                for old,new in review['replacements'].items():target=re.sub(r'(?<!\w)'+re.escape(old)+r'(?!\w)',lambda _:new,target)
                target=source[:len(source)-len(source.lstrip())]+target.strip()+source[len(source.rstrip()):]
            catalog[kind][source]=target
        catalog[kind].update(review[kind])
    DEST.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('Catalog written:',DEST)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--generate',action='store_true');parser.add_argument('--refine',action='store_true');args=parser.parse_args()
    if args.generate or args.refine:generate(args.refine)
    else:
        messages,templates=collect();print(json.dumps(dict(messages=len(messages),templates=len(templates),characters=sum(map(len,messages+templates)))))
