"""Specific factual questions retain the old application IDs, without generic templates."""

def curiosity_question(level):
    from .education import LESSONS
    from .curiosities import ROWS,MAP_CURIOSITIES
    special={
        'lujan':('¿De qué país llegó en 1630 la imagen vinculada con la devoción de Luján?','Brasil','Francia','Japón'),
        'itati':('¿De qué provincia argentina es patrona la Virgen de Itatí?','Corrientes','Mendoza','Salta'),
        'moses':('¿Qué episodio bíblico representa la estampa de Sebald Beham de 1533?','El paso del mar del relato del Éxodo','La fundación de Roma','La batalla de Obligado'),
        'andes_route':('¿Qué advocación fue proclamada Patrona del Ejército de los Andes en enero de 1817?','La Virgen del Carmen de Cuyo','La Virgen de Itatí','La Virgen de Luján'),
    }
    key=MAP_CURIOSITIES[level]
    return special.get(key) or LESSONS[ROWS[level][2]].questions[0]

def records():
    from .education import LESSONS,SOURCES,fact_for
    from .curiosities import MAP_CURIOSITIES
    from .heritage import ENTRIES
    result=[]
    for topic,lesson in enumerate(LESSONS):
        entry=ENTRIES[MAP_CURIOSITIES[topic//2]]
        for band in range(3):
            remaining=[q for i,q in enumerate(lesson.questions) if i//2!=band]
            # Four previously generic IDs are now concrete questions on this topic.
            for variant,q in enumerate(remaining[:2]+[curiosity_question(topic//2)]+remaining[2:3]):
                is_curiosity=variant==2
                result.append(dict(id=(5000000+topic*9+band*3+variant if variant<3 else 6000000+topic*3+band),
                    topic=topic,band=band,kind='curiosity' if is_curiosity else 'choice',prompt=q[0],options=list(q[1:]),correct=0,
                    explanation=entry['body'][:700] if is_curiosity else fact_for(topic,band),
                    source=entry['url'] if is_curiosity else SOURCES[lesson.source][1]))
    return result
