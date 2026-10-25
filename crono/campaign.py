"""Stable campaign boundaries; Argentina is independent of the main journey."""
MAIN_ERA_IDS=(0,1,8,2,3,4,5,6)
MAIN_ERAS=len(MAIN_ERA_IDS)
TOTAL_ERAS=12
MAIN_LEVELS=MAIN_ERAS*3
TOTAL_LEVELS=36
DLC_START=21  # Stable IDs: existing maps and teachers' questions never move.
MAIN_LEVEL_IDS=tuple(e*3+s for e in MAIN_ERA_IDS for s in range(3))
DLC_LEVEL_IDS=(21,22,27,23)
BONUS_LEVEL_IDS=(28,29,30,31,32)
RIFT_LEVEL_IDS=(33,34,35)
CHAPTER_ORDER=MAIN_ERA_IDS+(7,9,10,11)
DISPLAY_LEVEL_IDS=MAIN_LEVEL_IDS+DLC_LEVEL_IDS+BONUS_LEVEL_IDS+RIFT_LEVEL_IDS
ERA_LABELS=('Primigenio','Deshielo','Grecia','Medievo','Industria','Guerras mundiales','Actualidad','Argentina · DLC','Antiguo Egipto','Argentina · bonus','Otros rescates','Grietas históricas')
DIFFICULTIES=('Explorador · mínima','Aventurero · media','Experto · alta')

def is_dlc(level):
    return level in DLC_LEVEL_IDS or level in (28,29)

def is_bonus(level):return level in BONUS_LEVEL_IDS
def is_rift(level):return level in RIFT_LEVEL_IDS
def sequence_for(level):
    if is_bonus(level) or is_rift(level):return (level,)
    return DLC_LEVEL_IDS if is_dlc(level) else MAIN_LEVEL_IDS

def rank(level):
    return sequence_for(level).index(level)

def successor(level):
    sequence=sequence_for(level)
    return sequence[min(len(sequence)-1,sequence.index(level)+1)]

def final_level(level):
    return level==sequence_for(level)[-1]

def unlocked(level,frontier):
    if is_bonus(level) or is_rift(level):return False
    return is_dlc(level)==is_dlc(frontier) and rank(level)<=rank(frontier)

def level_label(level):
    era,stage=divmod(level,3)
    if level in DLC_LEVEL_IDS:return f'AR.{DLC_LEVEL_IDS.index(level)+1}'
    if is_bonus(level):return f'B.{BONUS_LEVEL_IDS.index(level)+1}'
    if is_rift(level):return f'G.{RIFT_LEVEL_IDS.index(level)+1}'
    return f'{MAIN_ERA_IDS.index(era)+1}.{stage+1}'

def chapter_levels(era):
    if era==7:return DLC_LEVEL_IDS
    if era==9:return (28,29)
    if era==10:return (30,31,32)
    if era==11:return RIFT_LEVEL_IDS
    return tuple(era*3+s for s in range(3))
