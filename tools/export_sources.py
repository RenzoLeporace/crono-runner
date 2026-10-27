"""Export the playable curriculum and its source links without duplicating facts."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'.vendor')]
from crono.education import SOURCES,STAGES,LESSONS
from crono.campaign import DISPLAY_LEVEL_IDS,level_label
rows=['# Contenidos y fuentes de la beta educativa 0.9.3','',
      'Las explicaciones son paráfrasis originales. Cada archivo del juego enlaza su fuente en el cuaderno.',
      'Los mapas son escenarios de ficción inspirados en temas concretos, no reconstrucciones exactas ni una historia universal. Los jefes y los enemigos son ficticios.','',
      'El banco inicial contiene 1656 registros para 92 temas y tres edades: 552 preguntas y 1104 tareas de aplicación sobre fuentes, imágenes, razones y cronología. Cada tema y edad tiene seis alternativas; no equivalen a 1656 hechos históricos distintos. Desde Configuración, los docentes pueden consultar todas las respuestas, agregar preguntas y modificar las existentes, incluida su explicación y referencia. Las referencias de esta página corresponden al contenido original; las incorporaciones del docente usan la referencia que este indique. Al abrir un archivo se elige una pregunta al azar y se mezclan las respuestas. Si hay varias, no se repite inmediatamente la anterior del mismo perfil.','',
      'Las preguntas de 6–9 años se centran en reconocer; las de 10–14, en relacionar y explicar; las de 15 en adelante, en inferir y valorar los límites de las evidencias. Son perfiles orientativos, no una evaluación curricular certificada.','']
for level_id in DISPLAY_LEVEL_IDS:
    stage=STAGES[level_id]
    rows.extend([f'## {level_label(level_id)} · {stage.name}','',stage.focus,''])
    for topic in range(level_id*2,level_id*2+2):
        lesson=LESSONS[topic]
        title,url=SOURCES[lesson.source]
        rows.extend([f'- **{lesson.title}**. Fuente: [{title}]({url}).'])
    rows.append('')
rows.extend(['## Campaña y expansión argentina' , '', 'La campaña general tiene 27 mapas. Las dos guerras mundiales se tratan en una época con tres mapas: 1914, 1939 y reconstrucción desde 1945. La Guerra Fría añade Berlín, Luna sin combate y diálogo; la actualidad añade redes, renovables y cooperación científica. Argentina incluye cuatro mapas normales: 1810, 1816, Obligado 1845 y 1983. Hay diez bonus por rescates, Güemes y Farrapos, además de tres grietas, para un total de 46 mapas. Los rescates son ficción del reloj y las grietas devuelven al origen; no alteran los desenlaces históricos. Los adversarios son anomalías ficticias, no poblaciones ni países reales.', '', '## Cómo funciona el aprendizaje','',
             'Cada archivo resuelto por primera vez da dos puntos de conocimiento, compartidos entre los perfiles de edad. Un error muestra la respuesta y una explicación, permite reintentar y no resta energía ni puntos. Los repasos no repiten recompensas. Los archivos descubiertos se pueden consultar en el cuaderno.',
             '', 'En los mapas con jefe, resolver al menos un archivo de ese mapa prolonga 0,8 segundos el período vulnerable del jefe. Ninguna mejora ni respuesta es obligatoria para superar las rutas o los combates.'])
from crono.heritage import ENTRIES
rows.extend(['','## Patrimonio y tradiciones',''])
for entry in ENTRIES.values():
    rows.extend([f'### {entry["title"]}','',entry['body'],'',f'Fuente: [{entry["source"]}]({entry["url"]}).',''])
rows.extend(['## Referencias para la ambientación argentina','',
    'Los realistas son figuras ficticias inspiradas en conflictos del período independentista; los uniformes no reproducen un regimiento concreto. El Cabildo de 1810 y el Congreso de 1816 se presentan como procesos políticos, no como batallas documentadas en esos edificios.', '',
    'En 1983, los militares evocan represión y terrorismo de Estado durante la dictadura; las células terroristas evocan violencia de organizaciones armadas del período previo. No se representa el regreso democrático como una batalla ni se identifican grupos o personas reales. Las fichas distinguen ambas formas de violencia y explican la recuperación institucional.', '',
    '- [Museo del Cabildo](https://www.argentina.gob.ar/node/421639).',
    '- [Casa Histórica de Tucumán](https://www.argentina.gob.ar/node/412295).',
    '- [Museo Histórico Nacional · colección del traje](https://museohistoriconacional.cultura.gob.ar/info/coleccion-del-traje-argentino/).',
    '- [Dirección Nacional Electoral · elecciones de 1983](https://www.argentina.gob.ar/dine/elecciones-1983).',
    '- [Archivo Nacional de la Memoria](https://catalogo.jus.gob.ar/index.php/archivo-nacional-de-la-memoria).',
    '- [Biblioteca Nacional · documentos de la recuperación democrática](https://www.bn.gov.ar/micrositios/admin_assets/issues/files/c6f186381e146bb659027f121d3198f3.pdf).','',
    'Egipto tiene tres mapas que evocan distintos períodos y temas: Nilo, Guiza y templos. Los signos pintados son decorativos, no transcripciones de inscripciones auténticas. La referencia a Moisés se presenta como tradición bíblica y cultural; no se le asigna una fecha arqueológica segura ni un faraón concreto.'])
(ROOT/'FUENTES.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')
