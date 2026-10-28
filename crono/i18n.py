"""Small offline presentation catalog. Stored game/content IDs stay in Spanish.

Only bundled text is translated; Verbatim protects teacher/student input. The
catalog is loaded lazily and all per-frame lookup caches have fixed limits.
"""
from functools import lru_cache
import json
from pathlib import Path
import re
import sys

LANGUAGES=(('es','Español'),('pt-BR','Português (Brasil)'))
_language='es'
_catalog=None
_patterns=None
_FIELD=re.compile(r'\{(\d+)\}')


class Verbatim(str):
    """Text authored by a person, not an instruction to translate its words."""


class Localized(str):
    """Already translated and measured; never translate individual wrapped rows."""


class Authored(str):
    """Original question text plus optional teacher-authored language variants."""
    def __new__(cls,value,variants=None,bundled=False):
        obj=super().__new__(cls,value);obj.variants=variants or {};obj.bundled=bundled
        return obj


def language():return _language


def set_language(code):
    global _language
    code=code if code in dict(LANGUAGES) else 'es'
    if code==_language:return
    _language=code;_translate.cache_clear()
    # Some cached pictures contain labels (buttons, monuments, landmarks).
    # Invalidate on the explicit setting change, never during normal rendering.
    seen=set()
    for name,module in tuple(sys.modules.items()):
        if not name.startswith('crono.') or name=='crono.i18n':continue
        for value in tuple(vars(module).values()):
            if callable(value) and hasattr(value,'cache_clear') and id(value) not in seen:
                seen.add(id(value));value.cache_clear()


def catalog():
    global _catalog
    if _catalog is None:
        root=Path(getattr(sys,'_MEIPASS',Path(__file__).resolve().parents[1]))
        _catalog=json.loads((root/'assets'/'locales'/'pt-BR.json').read_text(encoding='utf8'))
    return _catalog


def patterns():
    global _patterns
    if _patterns is None:
        groups={}
        for source,target in catalog()['templates'].items():
            fields=_FIELD.findall(source)
            if sorted(fields)!=sorted(_FIELD.findall(target)):continue
            parts=_FIELD.split(source);regex='';names=[]
            for i,part in enumerate(parts):
                if i%2:regex+='(.+?)';names.append(part)
                else:regex+=re.escape(part)
            first=parts[0][:1] if parts[0] else ''
            groups.setdefault(first,[]).append((sum(map(len,parts[::2])),re.compile('^'+regex+'$',re.DOTALL),target,names))
        _patterns={key:sorted(rows,key=lambda v:v[0],reverse=True) for key,rows in groups.items()}
    return _patterns


@lru_cache(maxsize=1)
def uppercase_messages():return {source.upper():target.upper() for source,target in catalog()['messages'].items()}


@lru_cache(maxsize=2048)
def _translate(value):
    messages=catalog()['messages']
    if value in messages:return Localized(messages[value])
    if value.isupper() and value in uppercase_messages():return Localized(uppercase_messages()[value])
    stripped=value.strip()
    if stripped in messages:
        return Localized(value[:len(value)-len(value.lstrip())]+messages[stripped]+value[len(value.rstrip()):])
    groups=patterns()
    for _,regex,target,names in (*groups.get(value[:1],()),*groups.get('',())):
        match=regex.fullmatch(value)
        if match:
            args={name:str(tr(part)) for name,part in zip(names,match.groups())}
            return Localized(_FIELD.sub(lambda m:args[m[1]],target))
    parts=re.split(r'(\n+| · )',value)
    if len(parts)>1:return Localized(''.join(str(tr(part)) if i%2==0 else part for i,part in enumerate(parts)))
    return Localized(value)


def tr(value):
    if isinstance(value,Authored):
        if _language in value.variants:return Verbatim(value.variants[_language])
        return tr(str(value)) if value.bundled else Verbatim(value)
    if isinstance(value,(Verbatim,Localized)):return value
    value=str(value)
    if value.startswith(('https://','http://')):return Verbatim(value)
    if _language=='es' or not value or not any(c.isalpha() for c in value):return value
    return _translate(value)


def literal(value):return Verbatim(value)
