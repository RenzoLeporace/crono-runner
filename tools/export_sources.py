"""Export the playable curriculum and its source links without duplicating facts."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from crono.education import SOURCES,STAGES,LESSONS
rows=['# Contenidos y fuentes de la beta educativa 0.4','',
      'Las explicaciones son paráfrasis originales. Cada archivo del juego enlaza su fuente en el cuaderno.',
      'Los mapas son escenarios de ficción inspirados en temas concretos, no reconstrucciones exactas ni una historia universal. Los jefes y los enemigos son ficticios.','',
      'El banco inicial contiene 180 preguntas escritas: 60 por perfil de edad, con dos variantes por archivo y perfil. Desde Configuración, los docentes pueden consultar todas las respuestas, agregar preguntas y modificar las existentes, incluida su explicación y referencia. Las referencias de esta página corresponden al contenido original; las incorporaciones del docente usan la referencia que este indique. Al abrir un archivo se elige una pregunta al azar y se mezclan las respuestas. Si hay varias, no se repite inmediatamente la anterior del mismo perfil.','',
      'Las preguntas de 6–9 años se centran en reconocer; las de 10–14, en relacionar y explicar; las de 15 en adelante, en inferir y valorar los límites de las evidencias. Son perfiles orientativos, no una evaluación curricular certificada.','']
for level_id,stage in enumerate(STAGES):
    rows.extend([f'## {level_id//3+1}.{level_id%3+1} · {stage.name}','',stage.focus,''])
    for topic in range(level_id*2,level_id*2+2):
        lesson=LESSONS[topic]
        title,url=SOURCES[lesson.source]
        rows.extend([f'- **{lesson.title}**. Fuente: [{title}]({url}).'])
    rows.append('')
rows.extend(['## Cómo funciona el aprendizaje','',
             'Cada archivo resuelto por primera vez da dos puntos de conocimiento, compartidos entre los perfiles de edad. Un error muestra la respuesta y una explicación, permite reintentar y no resta energía ni puntos. Los repasos no repiten recompensas. Los archivos descubiertos se pueden consultar en el cuaderno.',
             '', 'En los terceros mapas, resolver al menos un archivo de ese mapa prolonga 0,8 segundos el período vulnerable del jefe. Ninguna mejora ni respuesta es obligatoria para superar las rutas o los combates.'])
(ROOT/'FUENTES.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')
