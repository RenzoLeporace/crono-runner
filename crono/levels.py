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
        "El salto salió mal. Tu reloj se rompió en el tiempo.\nReúne los tres fragmentos de cada mapa para abrir el siguiente umbral.",
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
    Era("LA HORA DE LAS MÁQUINAS", "Año 1889", "El pulso de las máquinas",
        "Entre vapor y engranajes, el reloj encuentra tu señal.\nLa señal atraviesa otro siglo: todavía queda camino hasta casa.",
        (28, 33, 47), (178, 123, 98), (98, 80, 83), (54, 53, 65), (54, 51, 55), (185, 137, 93), (255, 173, 105), "factory"),
]

ERAS.extend([
    Era('EL SIGLO DE LAS GUERRAS','1914–1948','Memoria y reconstrucción',
        'Cruza archivos, refugios y ciudades en reconstrucción.\nRecupera la memoria y supera los ecos del conflicto.',
        (28,36,47),(142,148,137),(76,89,89),(43,56,64),(42,46,47),(146,151,133),(238,186,109),'war'),
    Era('EL MUNDO CONECTADO','Era actual','Un presente por construir',
        'Redes, ciencia y energía conectan tu señal con casa.\nRepara el último umbral y piensa qué futuro queremos construir.',
        (13,30,57),(106,165,188),(48,92,121),(26,57,86),(31,48,65),(146,203,207),(99,239,219),'modern'),
    Era('ARGENTINA · HISTORIAS DE UN PAÍS','1810 · 1816 · 1983','Expansión incluida',
        'Recorre tres momentos de la historia argentina.\nConserva sus archivos y libera al guardián de la memoria.',
        (39,61,82),(207,194,161),(126,137,139),(68,94,109),(67,70,70),(211,198,165),(135,216,245),'argentina'),
])

ERAS.append(Era('EL REINO DEL NILO','Antiguo Egipto','Entre el río y la memoria',
    'El reloj despierta entre canales, piedra y papiros.\nExplora siglos distintos de Egipto y distingue las evidencias de las tradiciones.',
    (44,77,102),(242,192,117),(180,134,86),(105,83,66),(94,72,51),(223,181,109),(96,221,206),'egypt'))

ERAS.extend([
    Era('ARGENTINA · RUTAS DE LA MEMORIA','1845 · 1817 · 1825–1828','Defensa y travesías',
        'Recupera documentos y protege las rutas del reloj.\nDistingue las misiones de ficción de los hechos históricos.',
        (34,59,78),(181,188,167),(96,124,127),(49,80,94),(61,78,80),(183,180,145),(126,219,233),'journey'),
    Era('LOS CAMINOS RESCATADOS','Viajes desbloqueables','Personas que abren caminos',
        'Cada rescate conserva una historia y abre otra ruta.\nLa cooperación también puede cambiar el viaje.',
        (40,57,81),(187,172,138),(111,122,124),(61,79,96),(62,73,83),(185,180,153),(235,193,118),'journey'),
    Era('GRIETAS AL PASADO','Excursiones históricas','Volver con memoria',
        'Una grieta conduce a otro episodio del pasado.\nCompleta la excursión y regresa al lugar de origen con tu recompensa.',
        (24,42,68),(139,162,171),(84,108,128),(44,65,89),(53,66,80),(166,190,192),(126,226,219),'journey'),
])


for title in ('PAÍSES Y MEMORIAS','EL SABER EN MOVIMIENTO','REDES DE COOPERACIÓN','GUERRA FRÍA'):
    ERAS.append(Era(title,'Nuevas rutas históricas','Historias para investigar',
        'Recupera fuentes, contrasta relatos y completa una misión contextual.',
        (41,62,79),(198,185,146),(108,130,122),(54,82,86),(66,74,69),(191,177,135),(239,195,111),'journey'))


def level_data(index,stage=0):
    from .education import STAGES
    from .routes import build_route
    if not 0<=index<len(ERAS) or not 0<=stage<3 or index*3+stage>=len(STAGES):
        raise ValueError('Época o mapa fuera de rango')
    return build_route(index,stage,STAGES[index*3+stage])
