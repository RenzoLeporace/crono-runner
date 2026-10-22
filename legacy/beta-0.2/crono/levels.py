"""Hand-authored routes. All coordinates are world pixels; Y grows downward."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Era:
    name: str
    date: str
    subtitle: str
    story: str
    sky: tuple
    horizon: tuple
    far: tuple
    near: tuple
    rock: tuple
    top: tuple
    accent: tuple
    kind: str


ERAS = [
    Era("EL MUNDO PRIMIGENIO", "66 millones de años atrás", "Donde todo comienza",
        "El salto salió mal. Tu reloj se rompió en el tiempo.\nReúne los tres fragmentos de cada época para abrir el siguiente umbral.",
        (13, 29, 43), (102, 164, 148), (38, 80, 82), (21, 59, 62), (30, 48, 49), (119, 174, 116), (242, 184, 100), "jungle"),
    Era("EL ÚLTIMO DESHIELO", "12.000 años atrás", "El silencio bajo el hielo",
        "El reloj vuelve a latir, pero aún no reconoce tu hogar.\nSigue las luces entre los glaciares. El frío no puede detenerte.",
        (22, 30, 61), (129, 161, 191), (65, 89, 126), (38, 60, 93), (40, 57, 82), (190, 223, 230), (133, 218, 245), "ice"),
    Era("LA CIUDAD DEL SOL", "2.500 años atrás", "La memoria de la piedra",
        "Alguien talló el mismo símbolo de tu reloj en estas ruinas.\nQuizá no seas la primera persona que se perdió en el tiempo.",
        (62, 44, 65), (222, 159, 109), (146, 94, 91), (101, 65, 76), (88, 63, 65), (225, 176, 115), (255, 211, 126), "ruins"),
    Era("LA EDAD DE LAS TORRES", "Año 1380", "Un reino entre la niebla",
        "Las campanas anuncian una tormenta que ya has escuchado.\nCada fragmento acerca tu pulso al presente. No mires atrás.",
        (25, 28, 53), (136, 115, 150), (72, 67, 103), (43, 45, 75), (49, 47, 65), (146, 155, 161), (210, 178, 240), "castle"),
    Era("LA HORA DE LAS MÁQUINAS", "Año 1889", "La última chispa",
        "Entre vapor y engranajes, el reloj encuentra tu señal.\nUn último umbral. Esta vez, al otro lado, está tu hogar.",
        (28, 33, 47), (178, 123, 98), (98, 80, 83), (54, 53, 65), (54, 51, 55), (185, 137, 93), (255, 173, 105), "factory"),
]

# Ground islands deliberately keep every required gap below the normal jump range.
# (x, top, width, height); side routes reward exploration but are never mandatory.
GROUND = [(0, 584, 680, 220), (815, 584, 700, 220), (1685, 584, 660, 220),
          (2500, 584, 690, 220), (3370, 584, 1180, 220)]
LEDGES = [(320, 488, 150, 28), (530, 410, 135, 28),
          (930, 490, 230, 34), (1210, 406, 170, 28),
          (1770, 490, 140, 28), (1960, 418, 175, 28), (2180, 490, 125, 28),
          (2580, 488, 155, 28), (2800, 408, 190, 28),
          (3470, 490, 240, 34), (3780, 405, 180, 28), (4030, 482, 130, 28)]


def level_data(index):
    """Small route changes give each chapter its own rhythm without blind jumps."""
    ground,ledges=GROUND,LEDGES
    shards = [(1040, 452), (2040, 380), (3590, 452)]
    checkpoints=[(1460,584),(3080,584)]
    hazards=[(1350,570,65,14),(2920,570,75,14),(3980,570,70,14)]
    enemies=[(1190,550,1175,1470),(1950,550,1780,2290),(2720,550,2550,3130),(3870,550,3750,4190)]
    if index==1:
        ground=[(0,584,560,220),(700,584,620,220),(1480,584,700,220),(2350,584,710,220),(3240,584,1310,220)]
        ledges=[(230,492,160,28),(430,414,120,28),(760,494,180,30),(1050,420,150,28),
                (1510,494,160,28),(1740,414,200,30),(2010,486,140,28),(2420,494,160,28),
                (2630,414,170,28),(2900,484,120,28),(3320,494,150,28),(3540,414,200,30),(3950,488,150,28)]
        shards=[(850,456),(1840,376),(3640,376)]
        checkpoints=[(1280,584),(3010,584)]
        hazards=[(1170,570,65,14),(2770,570,75,14),(4160,570,80,14)]
        enemies=[(980,550,950,1140),(1640,550,1500,2120),(2500,550,2390,2720),(3860,550,3760,4080)]
    elif index==2:
        ground=[(0,584,760,220),(910,584,720,220),(1780,584,680,220),(2640,584,650,220),(3430,584,1120,220)]
        ledges=[(280,492,160,28),(500,408,160,28),(1000,492,220,30),(1320,408,170,28),
                (1830,492,150,28),(2040,412,210,30),(2310,490,125,28),(2690,492,150,28),
                (2900,408,150,28),(3490,492,150,28),(3710,412,220,30),(4040,488,140,28)]
        shards=[(1100,454),(2140,374),(3820,374)]
        checkpoints=[(1570,584),(3220,584)]
        hazards=[(1450,570,75,14),(3090,570,65,14),(4120,570,70,14)]
        enemies=[(1250,550,1230,1420),(1920,550,1800,2370),(2800,550,2680,3040),(3980,550,3950,4080)]
    elif index==3:
        ground=[(0,584,650,220),(800,584,680,220),(1650,584,620,220),(2440,584,710,220),(3320,584,1230,220)]
        ledges=[(250,490,140,28),(460,405,130,28),(890,490,220,30),(1200,406,150,28),
                (1690,492,130,28),(1860,413,180,30),(2110,488,130,28),(2500,490,155,28),
                (2720,410,160,28),(2980,490,110,28),(3380,492,140,28),(3570,413,170,30),(3990,488,160,28)]
        shards=[(1000,452),(1950,375),(3650,375)]
        checkpoints=[(1410,584),(3070,584)]
        hazards=[(1300,570,65,14),(2910,570,60,14),(4180,570,70,14)]
        enemies=[(1130,550,1120,1280),(1820,550,1680,2200),(2660,550,2480,2860),(3860,550,3770,4100)]
    elif index==4:
        ground=[(0,584,590,220),(750,584,670,220),(1590,584,620,220),(2390,584,700,220),(3270,584,1280,220)]
        ledges=[(200,490,140,28),(400,408,130,28),(790,492,140,28),(990,410,200,30),
                (1240,490,130,28),(1640,492,130,28),(1830,410,180,30),(2070,490,110,28),
                (2450,490,150,28),(2660,408,160,28),(2900,490,120,28),(3330,490,150,28),
                (3540,408,200,30),(3890,490,160,28)]
        shards=[(1090,372),(1920,372),(3640,370)]
        checkpoints=[(1360,584),(3020,584)]
        hazards=[(1190,570,70,14),(2815,570,75,14),(4140,570,90,14)]
        enemies=[(950,550,780,1160),(1760,550,1630,2110),(2590,550,2420,2770),(3880,550,3780,4090)]
    ledges=[(x,min(y,490) if y>492 else y,w,h) for x,y,w,h in ledges]
    platforms = [dict(x=x, y=y, w=w, h=h, moving=False) for x, y, w, h in ground]
    for x, y, w, h in ledges:
        platforms.append(dict(x=x, y=y, w=w, h=h, moving=False))
    # Optional ferries below the jump arc, safely separated from permanent ground.
    for i in range(len(ground)-1):
        end=ground[i][0]+ground[i][2]
        x=(end+ground[i+1][0])/2-50
        platforms.append(dict(x=x, y=526, w=100, h=22, moving=True,
                              amplitude=36, speed=1.0 + index * .12))
    echoes = [(370, 451), (575, 373), (650, 548), (860, 548),
              (1250, 369), (1330, 369), (1440, 548), (1740, 548),
              (1830, 453), (2240, 453), (2560, 548), (2850, 371),
              (2940, 371), (3420, 548), (3830, 368), (3910, 368), (4085, 445)]
    if index:
        echoes=[(x+w*.4,y-37) for x,y,w,h in ledges]
        echoes += [(x+w-38,y-37) for x,y,w,h in ground[:4]]
        echoes=echoes[:17]
        while len(echoes)<17:
            echoes.append((ground[len(echoes)%len(ground)][0]+90,547))
    return dict(width=4550, platforms=platforms, shards=shards, echoes=echoes,
                enemies=enemies, hazards=hazards, checkpoints=checkpoints,
                spawn=(100, 520), portal=(4360, 584))
