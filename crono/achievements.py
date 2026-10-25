"""Explicit predicates, no executable conditions read from saves or content."""
from collections import Counter
from .achievement_catalog import CATALOG
from .campaign import MAIN_LEVEL_IDS,DLC_LEVEL_IDS,MAIN_ERA_IDS
from .curiosities import MAP_CURIOSITIES
from .education import UPGRADES

def earned(data):
    if data.get('practice'):return set()
    levels={int(k) for k in data.get('records',{}) if str(k).isdigit()}
    fragments=data.get('fragments_by_level',{});complete=sum(len(v)==3 for v in fragments.values() if isinstance(v,list))
    curiosities=set(data.get('curiosities_seen',[]));echoes=data.get('banked_echoes',[])
    echo_counts=Counter(v.split(':')[0] for v in echoes if isinstance(v,str))
    m=data.get('metrics',{});kinds=set(m.get('defeated_kinds',[]) if isinstance(m.get('defeated_kinds',[]),list) else [])
    bosses=set(m.get('defeated_boss_eras',[]) if isinstance(m.get('defeated_boss_eras',[]),list) else [])
    solved=set(data.get('solved',[]));upgrades=set(data.get('upgrades',[]));rescues=set(data.get('rescued_ids',[]))
    rifts=set(data.get('rifts_completed',[]));mechanics=set(data.get('mechanics_completed',[]));skins=set(data.get('purchased_skins',[]))
    checks=[bool(levels),0 in levels,
        *[set(e*3+s for s in range(3))<=levels for e in (0,1,8,2,3,4,5,6)],
        set(MAIN_LEVEL_IDS)<=levels,21 in levels,22 in levels,27 in levels,23 in levels,set(DLC_LEVEL_IDS)<=levels,
        set(MAIN_LEVEL_IDS+DLC_LEVEL_IDS)<=levels,
        any(bool(v) for v in fragments.values()),complete>=1,complete>=5,
        bool(curiosities),len(curiosities)>=8,{MAP_CURIOSITIES[i] for i in MAIN_LEVEL_IDS}<=curiosities,
        {MAP_CURIOSITIES[i] for i in DLC_LEVEL_IDS}<=curiosities,{'moses','lujan','itati'}<=curiosities,
        max(echo_counts.values(),default=0)>=12,max(echo_counts.values(),default=0)>=36,len(echoes)>=300,
        sum(m.get(k,0) for k in ('stomp_kills','dash_kills','shot_kills'))>=1,
        {'walker','hopper','flyer','sentry','charger','armored'}<=kinds,
        m.get('stomp_kills',0)>=5,m.get('dash_kills',0)>=5,m.get('shot_kills',0)>=10,
        bool(bosses),{0,1,8,2,3,4,5,6,7}<=bosses,bool(m.get('boss_with_lesson')),bool(m.get('boss_with_two_lessons')),
        bool(m.get('level_without_death')),bool(m.get('boss_without_death')),
        bool(solved),len(solved)>=10,len(solved)>=30,{i*2+s for i in MAIN_LEVEL_IDS for s in (0,1)}<=solved,
        all(any(i in solved for i in range(e*6,e*6+6)) for e in MAIN_ERA_IDS),
        bool(upgrades),len(upgrades)>=4,{u['id'] for u in UPGRADES}<=upgrades,
        bool(rescues),'san_martin' in rescues and 28 in data.get('bonus_unlocked',[]),
        'brown' in rescues and 29 in data.get('bonus_unlocked',[]),28 in levels,29 in levels,len(rescues)>=3,
        bool(rifts),33 in rifts,len(rifts)>=3,len(mechanics)>=8,bool(skins),len(skins&set(data.get('skin_cards_seen',[])))>=3,
        all(any(i in mechanics for i in range(e*3,e*3+3)) for e in MAIN_ERA_IDS)]
    assert len(checks)==len(CATALOG)==60
    return {row['id'] for row,ok in zip(CATALOG,checks) if ok}
