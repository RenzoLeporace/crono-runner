"""Stable campaign boundaries; Argentina is independent of the main journey."""
MAIN_ERA_IDS=(0,1,8,2,3,4,5,16,15,6)
WW1_LEVEL_IDS=(15,46,47)
WW2_LEVEL_IDS=(16,48,17)
COLD_WAR_LEVEL_IDS=(43,44,45)
MAIN_ERAS=len(MAIN_ERA_IDS)
TOTAL_ERAS=17
MAIN_LEVELS=MAIN_ERAS*3
TOTAL_LEVELS=50
DLC_START=21  # Stable IDs: existing maps and teachers' questions never move.
MAIN_LEVEL_IDS=tuple(n for e in MAIN_ERA_IDS for n in (WW1_LEVEL_IDS if e==5 else WW2_LEVEL_IDS if e==16 else COLD_WAR_LEVEL_IDS if e==15 else tuple(e*3+s for s in range(3))))
DLC_LEVEL_IDS=(21,22,27,23)
BONUS_LEVEL_IDS=(28,29,30,31,32,36,37,38,39,40,41,42)
RIFT_LEVEL_IDS=(33,34,35,49)
CHAPTER_ORDER=MAIN_ERA_IDS+(7,9,10,11,12,13,14)
DISPLAY_LEVEL_IDS=MAIN_LEVEL_IDS+DLC_LEVEL_IDS+BONUS_LEVEL_IDS+RIFT_LEVEL_IDS
ERA_LABELS=('Primigenio','Deshielo','Grecia','Medievo','Industria','Primera Guerra Mundial','Actualidad','Argentina · DLC','Antiguo Egipto','Argentina · bonus','Otros rescates','Grietas históricas','Brasil · DLC','Nuevas historias','Saberes y cooperación','Guerra Fría','Segunda Guerra Mundial')
DIFFICULTIES=('Explorador · mínima','Aventurero · media','Experto · alta')

def is_dlc(level):
    return level in DLC_LEVEL_IDS or level in (28,29,36,37)

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
    if level in WW1_LEVEL_IDS:return f'7.{WW1_LEVEL_IDS.index(level)+1}'
    if level in WW2_LEVEL_IDS:return f'8.{WW2_LEVEL_IDS.index(level)+1}'
    if level in COLD_WAR_LEVEL_IDS:return f'9.{COLD_WAR_LEVEL_IDS.index(level)+1}'
    if level==36:return 'BR.1'
    if level==37:return 'AR.B3'
    if level in DLC_LEVEL_IDS:return f'AR.{DLC_LEVEL_IDS.index(level)+1}'
    if is_bonus(level):return f'B.{BONUS_LEVEL_IDS.index(level)+1}'
    if is_rift(level):return f'G.{RIFT_LEVEL_IDS.index(level)+1}'
    return f'{MAIN_ERA_IDS.index(era)+1}.{stage+1}'

def chapter_for_level(level):
    if level in WW1_LEVEL_IDS:return 5
    if level in WW2_LEVEL_IDS:return 16
    if level in COLD_WAR_LEVEL_IDS:return 15
    if level in DLC_LEVEL_IDS:return 7
    if level in (28,29,37):return 9
    if level in (30,31,32):return 10
    if level in RIFT_LEVEL_IDS:return 11
    if level==36:return 12
    if level in (38,39,40):return 13
    if level in (41,42):return 14
    return level//3

def chapter_levels(era):
    if era==5:return WW1_LEVEL_IDS
    if era==16:return WW2_LEVEL_IDS
    if era==15:return COLD_WAR_LEVEL_IDS
    if era==7:return DLC_LEVEL_IDS
    if era==9:return (28,29,37)
    if era==12:return (36,)
    if era==13:return (38,39,40)
    if era==14:return (41,42)
    if era==10:return (30,31,32)
    if era==11:return RIFT_LEVEL_IDS
    return tuple(era*3+s for s in range(3))
