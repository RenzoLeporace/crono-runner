"""Stable campaign boundaries; Argentina is independent of the main journey."""
MAIN_ERA_IDS=(0,1,8,2,3,4,5,6)
MAIN_ERAS=len(MAIN_ERA_IDS)
TOTAL_ERAS=9
MAIN_LEVELS=MAIN_ERAS*3
TOTAL_LEVELS=TOTAL_ERAS*3
DLC_START=21  # Stable IDs: existing maps and teachers' questions never move.
MAIN_LEVEL_IDS=tuple(e*3+s for e in MAIN_ERA_IDS for s in range(3))
DLC_LEVEL_IDS=(21,22,23)
CHAPTER_ORDER=MAIN_ERA_IDS+(7,)
ERA_LABELS=('Primigenio','Deshielo','Grecia','Medievo','Industria','Guerras mundiales','Actualidad','Argentina · DLC','Antiguo Egipto')
DIFFICULTIES=('Explorador · mínima','Aventurero · media','Experto · alta')

def is_dlc(level):
    return level in DLC_LEVEL_IDS

def rank(level):
    return (DLC_LEVEL_IDS if is_dlc(level) else MAIN_LEVEL_IDS).index(level)

def successor(level):
    sequence=DLC_LEVEL_IDS if is_dlc(level) else MAIN_LEVEL_IDS
    return sequence[min(len(sequence)-1,sequence.index(level)+1)]

def final_level(level):
    return level==(DLC_LEVEL_IDS[-1] if is_dlc(level) else MAIN_LEVEL_IDS[-1])

def unlocked(level,frontier):
    return is_dlc(level)==is_dlc(frontier) and rank(level)<=rank(frontier)

def level_label(level):
    era,stage=divmod(level,3)
    return f'{"AR" if era==7 else MAIN_ERA_IDS.index(era)+1}.{stage+1}'
