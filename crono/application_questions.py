"""Source, illustration and reasoning tasks supplement authored factual items."""
def records():
    from .education import LESSONS,SOURCES,STAGES,fact_for
    from .curiosities import MAP_CURIOSITIES
    from .heritage import ENTRIES
    result=[]
    sequences={
        0:('El proceso de un fósil','Enterramiento → conservación en la roca → investigación del fósil','La investigación ocurre después de la formación del fósil; los restos no se conservan siempre.'),
        1:('Estudiar una pintura paleolítica','Creación de la pintura → conservación del sitio → estudio actual','Los estudios actuales interpretan evidencias antiguas; no fueron escritos por quienes pintaron la cueva.'),
        2:('Dos contextos del Mediterráneo','Atenas clásica → Alejandría helenística → investigación actual','La Alejandría de los Ptolomeos es posterior a la Atenas clásica del recorrido.'),
        3:('La historia de una fuente medieval','Creación del documento medieval → conservación en un archivo → consulta actual','La fecha de creación del documento y la fecha en que lo consultamos son distintas.'),
        4:('Innovaciones y pruebas','Motor de Newcomen (1712) → Rainhill (1829) → lámparas prácticas hacia 1880','Estos hitos no sucedieron simultáneamente ni bastan para explicar toda la industrialización.'),
        5:('Tres hitos del siglo XX','Inicio de la Primera Guerra (1914) → inicio de la Segunda (1939) → Declaración Universal (1948)','Las dos guerras y la Declaración Universal pertenecen a momentos distintos.'),
        6:('Una misión y sus evidencias','Planificar Apolo 11 → alunizar en 1969 → estudiar sus registros','Los registros de una misión permiten investigar sus decisiones y resultados después.'),
        7:('Procesos de la historia argentina','Revolución de Mayo (1810) → Independencia (1816) → recuperación democrática (1983)','Son procesos distintos; la recuperación democrática no ocurrió durante las guerras de independencia.'),
        8:('Investigar un papiro','Escritura antigua → conservación del soporte → interpretación actual','El objeto y su interpretación pertenecen a momentos distintos. Moisés no tiene una fecha arqueológica establecida en este archivo.'),
        9:('Independencia y conflictos posteriores','Preparación en Cuyo (1816) → Cruce de los Andes (1817) → Obligado (1845)','El cruce precedió a la Vuelta de Obligado. La guerra naval con Brasil corresponde a 1825–1828.'),
        10:('Cuidado e investigación','Registrar una experiencia → conservar el testimonio → contrastarlo con otras fuentes','Esta secuencia organiza el trabajo con fuentes; no inventa una fecha para la misión ficticia.'),
        11:('Tres episodios del pasado','Erupción de Pompeya (79) → Apolo 11 (1969) → guerra de Malvinas (1982)','Las grietas reúnen episodios muy distantes. El orden del menú no determina la fecha de un hecho.'),
    }
    for topic,lesson in enumerate(LESSONS):
        level=topic//2;entry=ENTRIES[MAP_CURIOSITIES[level]]
        others=[i for i in range(level//3*3,level//3*3+3) if i!=level]
        image_options=[entry['title']]+[ENTRIES[MAP_CURIOSITIES[i]]['title'] for i in others]
        source_label=SOURCES[lesson.source][0]
        other_sources=list(dict.fromkeys(label for label,url in SOURCES if label!=source_label))
        source_options=[source_label,other_sources[(lesson.source+3)%len(other_sources)],other_sources[(lesson.source+8)%len(other_sources)]]
        for band in range(3):
            source_prompt=(f'¿Qué fuente aparece citada en «{lesson.title}»?',f'Vas a comprobar «{lesson.title}». ¿Qué institución o colección está citada?',f'Identifica la procedencia de la información en «{lesson.title}». ¿Qué fuente corresponde al archivo?')[band]
            image_prompt=(f'Mira la ilustración. ¿Qué curiosidad representa en «{STAGES[level].name}»?',f'Observa la ilustración del hallazgo de «{STAGES[level].name}». ¿Qué referencia permite identificar?',f'Identifica el hallazgo ilustrado de «{STAGES[level].name}» antes de interpretar su contexto.')[band]
            reason_prompt=(f'Aprendiste sobre «{lesson.title}». ¿Cómo puedes comprobar lo que cuenta el juego?',f'Quieres investigar más sobre «{lesson.title}». ¿Qué procedimiento aporta mejor evidencia?',f'Debes justificar una afirmación sobre «{lesson.title}». ¿Qué procedimiento evita una generalización sin evidencia?')[band]
            reason_options=(('Consultar la fuente y buscar otra pista','Usar solamente lo que imagino','Decidir por el color de los enemigos'),('Comparar el archivo con la fuente citada y otras evidencias','Tomar un solo objeto como prueba de toda una época','Suponer que el mapa reproduce todos los hechos'),('Contrastar procedencia, fecha y alcance de varias evidencias','Usar un caso documentado como explicación universal del período','Considerar el diseño del juego una prueba histórica independiente'))[band]
            for variant,(kind,prompt,options,explanation) in enumerate((
                ('source',source_prompt,source_options,'La procedencia permite localizar y revisar la información. La fuente citada es '+source_label+'. '+fact_for(topic,band)),
                ('image',image_prompt,image_options,'El hallazgo es «'+entry['title']+'». Es una ilustración original, no una fotografía de un objeto histórico. '+entry['body'].split('\n\n')[0]),
                ('reason',reason_prompt,reason_options,'Una conclusión debe sostenerse en evidencias situadas en su contexto. El juego combina aprendizaje y ficción; consultar y comparar fuentes ayuda a distinguirlos.'),
            )):
                result.append(dict(id=5000000+topic*9+band*3+variant,topic=topic,band=band,kind=kind,prompt=prompt,options=list(options),correct=0,explanation=explanation[:700],source=SOURCES[lesson.source][1]))
            title,sequence,explanation=sequences[level//3]
            parts=sequence.split(' → ')
            result.append(dict(id=6000000+topic*3+band,topic=topic,band=band,kind='chronology',
                prompt=('Ordena los pasos: ' if band==0 else '¿Qué secuencia temporal es coherente? ' if band==1 else 'Distingue creación, contexto e investigación. Identifica el orden correcto: ')+title+'.',
                options=[sequence,' → '.join((parts[1],parts[0],parts[2])),' → '.join(reversed(parts))],correct=0,explanation=explanation,source=SOURCES[lesson.source][1]))
    return result
