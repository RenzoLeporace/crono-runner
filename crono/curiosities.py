"""One distinct, optional discovery for each map, using the cited curriculum."""
MAP_CURIOSITIES=(
 'wing','footprint','feather','mammoth_ears','flint','pigments',
 'assembly','amphora','olympiad','wool','charter','rose_window',
 'pump','rocket','lightbulb','letter','civilian_archive','rights',
 'network','solar','science','lujan','itati','ballot','papyrus','stonework','moses',
 'river_chain','andes_route','naval_compass','pharos','rail_signal','field_medicine','field_radio','roman_mosaic','lunar_sample',
)
ROWS=(
 ('Un dedo convertido en ala','El ala de un pterosaurio no era igual a la de un ave: observa el dedo que sostiene la membrana.',0),
 ('Una pisada también cuenta','Un fósil no tiene que ser un hueso. Una huella puede conservar una actividad del pasado.',3),
 ('Dinosaurios que siguen aquí','La extinción no acabó con toda la vida: las aves conservan una conexión con aquel mundo.',5),
 ('Orejas pequeñas contra el frío','El pelo no era la única adaptación del mamut lanudo. Mira también el tamaño de sus orejas.',6),
 ('Una piedra se vuelve herramienta','Una herramienta tallada es una pista sobre las actividades de las personas.',8),
 ('Una pared guarda una mirada','Las pinturas permiten estudiar cómo las personas representaban su entorno. Este pequeño panel es una interpretación artística.',10),
 ('¿Quién podía tomar la palabra?','El objeto recuerda una pregunta esencial del ágora: quién tenía derecho a participar y quién quedaba fuera.',13),
 ('Una vasija puede viajar muy lejos','La cerámica conservada ayuda a conocer intercambios entre ciudades mediterráneas.',15),
 ('Cuatro años de espera','El calendario del encuentro de Olimpia tenía un ritmo propio: observa los cuatro tramos del círculo.',16),
 ('La lana también sostenía abadías','Una madeja puede contar historia económica. En Byland, criar ovejas y vender lana aportaba ingresos.',18),
 ('Un permiso para celebrar el mercado','Un documento puede revelar cómo se organizaban los encuentros comerciales.',20),
 ('La luz atraviesa el color','El pequeño rosetón muestra cómo el vidrio transforma la luz que entra en un edificio.',23),
 ('Una máquina para sacar agua','Este modelo recuerda el problema de las minas que ayudó a resolver el motor de Newcomen.',24),
 ('La locomotora puesta a prueba','Una innovación también se conoce por las pruebas y documentos que la acompañan.',26),
 ('La luz no llegó de golpe','Que exista un invento no significa que todas las casas puedan usarlo al mismo tiempo.',28),
 ('La guerra también tiene vida civil','Esta carta es una representación de los documentos que permiten estudiar experiencias fuera del combate.',31),
 ('Un archivo detrás del refugio','Conservar documentos cotidianos ayuda a investigar cómo cambian el trabajo y la organización social.',33),
 ('Un documento para todas las personas','La reconstrucción también incluyó acuerdos sobre derechos y dignidad.',35),
 ('Conectar es más que tender cables','Una red puede unir equipos; para que las personas la aprovechen también necesitan acceso y conocimientos.',36),
 ('Energía que vuelve a llegar','El modelo solar invita a distinguir una fuente de energía de los dispositivos que la transforman.',39),
 ('La ciencia cruza fronteras','El pequeño laboratorio recuerda que afrontar problemas de salud requiere cooperación.',41),
 None,None,
 ('La urna devuelve la palabra','Las elecciones del 30 de octubre de 1983 marcaron el retorno del voto democrático antes de la asunción del 10 de diciembre.',46),
 ('Un soporte nacido de una planta','Antes del papel industrial, en Egipto se escribía también sobre papiro.',52),
 ('Una obra de muchas tareas','Una piedra colocada en una pirámide pasó antes por extracción y transporte: la obra exigía organización.',51),
 None,
 ('Las cadenas del Paraná','Una cadena en un río puede ser parte de una estrategia; también es una pista para investigar el conflicto de Obligado.',54),
 ('La ruta antes de la montaña','Reconocer caminos y reunir provisiones formaba parte de la preparación de la expedición.',57),
 ('Una brújula no decide sola','Orientarse y coordinar una escuadra requería recursos y decisiones además de instrumentos.',59),
 ('Una luz para encontrar el puerto','El Faro de Alejandría pertenece al mundo helenístico; este modelo no reproduce sus dimensiones exactas.',60),
 ('El valor de una señal','Organizar el ferrocarril también significa coordinar la circulación y comprobar nuevas tecnologías.',63),
 ('La ayuda deja documentos','Los objetos y testimonios de atención médica permiten estudiar experiencias de la guerra.',65),
 ('La voz que busca contacto','Este equipo de radio representa la importancia de comunicar y ayudar en un conflicto. La misión de rescate es ficticia.',66),
 ('Una ciudad debajo de la ceniza','Un fragmento de decoración invita a estudiar la vida cotidiana y los cambios de una ciudad romana.',69),
 ('Una muestra de otro mundo','Recoger, registrar y estudiar muestras forma parte de la investigación; los planes e imágenes de Apolo 11 son fuentes de su misión.',71),
)

from .new_histories import NEW_MAPS
MAP_CURIOSITIES+=tuple(row['curiosity'][0] for row in NEW_MAPS)
ROWS+=tuple((row['curiosity'][1],row['curiosity'][2],72+i*2) for i,row in enumerate(NEW_MAPS))

def extend_entries(entries):
    from .education import LESSONS,SOURCES,STAGES
    from .campaign import DISPLAY_LEVEL_IDS,level_label
    for level,key in enumerate(MAP_CURIOSITIES):
        row=ROWS[level]
        if row:
            title,intro,topic=row;lesson=LESSONS[topic];source,url=SOURCES[lesson.source]
            if key=='ballot':source,url='Dirección Nacional Electoral · 1983','https://www.argentina.gob.ar/dine/elecciones-1983'
            entries[key]=dict(title=title,subtitle=f'{level_label(level)} · {STAGES[level].name}',
                body=intro+'\n\n'+lesson.fact,source=source,url=url)
        entries[key]['level']=level
    return {MAP_CURIOSITIES[level]:entries[MAP_CURIOSITIES[level]] for level in DISPLAY_LEVEL_IDS}

def place_site(index,stage,main,stations,enemies):
    """A single grounded stop, away from lessons, with a clear approach."""
    key=MAP_CURIOSITIES[index*3+stage]
    fraction=.35 if key=='lujan' else .58 if key=='itati' else .38+stage*.12
    candidates=[m for n,m in enumerate(main) if 1<n<len(main)-2
                and all(abs(m[0]+175-sx)>180 for sx,sy,topic in stations)]
    grounded=[m for m in candidates if m[1]==584]
    xx,yy,ww,k=min(grounded or candidates,key=lambda m:abs(m[0]/main[-1][0]-fraction))
    x=xx+175
    for spec in enemies:
        if xx<=spec['x']<=xx+ww and abs(spec['y']+34-yy)<3:
            spec['left']=max(spec['left'],x+145)
            spec['x']=max(spec['x'],spec['left'])
    return [(x,yy,key)]
