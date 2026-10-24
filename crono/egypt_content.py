"""Museum-based Egypt curriculum; religious narratives are explicitly identified."""

def extend_egypt(Stage,lesson,stages,lessons,sources):
    stages.extend(Stage(*row) for row in (
        ('Los canales del Nilo','Crecidas, cultivos y navegación en el Antiguo Egipto.','nile'),
        ('La meseta de Guiza','Pirámides del Reino Antiguo, canteras y trabajo organizado.','giza'),
        ('El templo de la memoria','Escritura, templos del Reino Nuevo y la tradición de Moisés.','temple'),
    ))
    base=len(sources)
    sources.extend((
        ('British Museum · Explorar Egipto','https://www.britishmuseum.org/sites/default/files/2024-06/Museum_explorers_Ancient_Egypt.pdf'),
        ('UNESCO · Menfis y su necrópolis','https://whc.unesco.org/en/list/86/'),
        ('Fitzwilliam Museum · Escritura egipcia','https://fitzmuseum.cam.ac.uk/explore-our-collection/highlights/context/tradition-and-change/egyptian-writing'),
        ('British Museum · Moisés y el Éxodo en el arte','https://www.britishmuseum.org/collection/object/P_1875-0710-270'),
    ))
    rows=(
      ('El río que alimenta',
       'El Nilo aportaba agua y las crecidas depositaban sedimentos fértiles. Las comunidades organizaban canales y cultivos; el río también conectaba poblaciones mediante barcos.',0,(
        ('¿Qué río atraviesa Egipto?','El Nilo','El Paraná','El Támesis'),
        ('¿Para qué servía el agua de los canales?','Regar cultivos','Cargar teléfonos','Enfriar trenes'),
        ('¿Qué dejaban las crecidas en las tierras?','Sedimentos fértiles','Plástico industrial','Nieve permanente'),
        ('¿Qué conectaba poblaciones por el río?','La navegación','El ferrocarril eléctrico','Aviones de pasajeros'),
        ('¿Qué relación ayuda a explicar los asentamientos?','Agua, cultivos y transporte','Solo la forma de las coronas','La presencia de fábricas de vapor'),
        ('¿Qué requiere una red de canales?','Organización y mantenimiento','Que el agua corra siempre cuesta arriba','Que nunca haya trabajo humano'))),
      ('Mirar la vida cotidiana',
       'Las sociedades egipcias incluían agricultores, artesanos y escribas, además de gobernantes. Herramientas, imágenes y objetos permiten investigar sus actividades; una sola imagen no representa toda la sociedad.',0,(
        ('¿Quién cultivaba los alimentos?','Agricultores','Solo faraones','Solo astronautas'),
        ('¿Qué hacía un artesano?','Fabricaba objetos','Pilotaba aviones','Programaba robots'),
        ('¿Qué sirve para investigar el trabajo antiguo?','Herramientas y representaciones','Un rumor sin evidencias','Solo un nombre de película'),
        ('¿Toda la población tenía la misma ocupación?','No, había distintos trabajos','Sí, todos eran reyes','Sí, todos escribían libros'),
        ('¿Qué límite tiene una escena pintada?','Selecciona lo que representa','Cuenta necesariamente todas las vidas','Sustituye toda otra evidencia'),
        ('¿Qué investigación es más sólida?','Comparar objetos, imágenes y contexto','Generalizar desde un solo detalle','Ignorar cuándo se produjo cada objeto'))),
      ('Piedra para la memoria',
       'Las pirámides de Guiza se construyeron como tumbas reales durante el Reino Antiguo, en el tercer milenio a. C. Sus complejos incluían otros edificios. No pertenecen al mismo momento que todos los templos egipcios.',1,(
        ('¿Qué forma tienen las grandes construcciones de Guiza?','Pirámides','Rascacielos de vidrio','Torres de televisión'),
        ('¿Para qué se construyeron las grandes pirámides de Guiza?','Como tumbas reales','Como estaciones de tren','Como fábricas de autos'),
        ('¿En qué período se construyeron?','En el Reino Antiguo','Durante las guerras mundiales','En el siglo XIX'),
        ('¿Qué integraba un complejo piramidal?','La pirámide y otros edificios','Solo una piedra suelta','Una autopista moderna'),
        ('¿Por qué evitar mezclar todos los monumentos en una fecha?','Egipto tuvo una historia de milenios','Todos se hicieron en un solo año','No se puede estudiar su antigüedad'),
        ('¿Qué dato sitúa a Guiza en el tiempo?','El tercer milenio antes de nuestra era','El año 1816','El siglo de las máquinas de vapor'))),
      ('Construir en equipo',
       'Levantar un complejo monumental exigía extraer, transportar y colocar piedra, organizar trabajadores y abastecerlos. Las construcciones y sus contextos arqueológicos ofrecen evidencias para estudiar ese trabajo.',1,(
        ('¿Con qué material se levantaron las pirámides de Guiza?','Piedra','Plástico','Hielo'),
        ('¿Una obra grande necesita organizar tareas?','Sí','No, nunca','Solo si llueve'),
        ('¿Qué tarea ocurría antes de colocar un bloque?','Extraerlo y transportarlo','Instalar un motor eléctrico','Fabricar una pantalla'),
        ('¿Qué necesitaban quienes trabajaban?','Alimentos y abastecimiento','Únicamente una corona','Ningún recurso'),
        ('¿Qué explica mejor una obra monumental?','Recursos, organización y técnicas','Una sola persona trabajando un día','Atribuirlo todo a tecnología actual'),
        ('¿Cómo evaluar una hipótesis de construcción?','Contrastar evidencias arqueológicas','Elegir la explicación más espectacular','Ignorar las herramientas conocidas'))),
      ('Escribir para conservar',
       'La escritura egipcia empleaba signos con funciones distintas, incluidos sonidos. Los escribas registraban información. El papiro se elaboraba con una planta; las inscripciones monumentales también se tallaban en piedra.',2,(
        ('¿Cómo llamamos a los signos de muchas inscripciones egipcias?','Jeroglíficos','Emojis de teléfono','Notas de un piano'),
        ('¿De qué se hacía el papiro?','De una planta','De vidrio','De hierro'),
        ('¿Qué trabajo realizaba un escriba?','Registrar información','Conducir locomotoras','Reparar satélites'),
        ('¿Dónde se tallaban inscripciones monumentales?','En piedra','Solo en pantallas','Solo en plástico'),
        ('¿Por qué los jeroglíficos no son simples dibujos decorativos?','Sus signos también representan sonidos','No transmitían información','Todos significan exactamente lo mismo'),
        ('¿Qué distingue soporte y sistema de escritura?','Papiro es material; jeroglíficos son signos','Ambos son nombres de faraones','El papiro es un idioma moderno'))),
      ('Moisés y los relatos del Éxodo',
       'En la tradición bíblica, Moisés guía la salida de los israelitas de Egipto. El relato del Éxodo tiene importancia religiosa y cultural. No permite fijar por sí solo una fecha histórica; este juego no identifica a su faraón con un gobernante concreto.',3,(
        ('¿Quién guía la salida de Egipto en el relato bíblico?','Moisés','Un astronauta','Un caballero medieval'),
        ('¿Cómo se llama ese relato de salida?','Éxodo','Revolución industrial','Edad del hielo'),
        ('¿Qué tipo de referencia es Moisés en este mapa?','Una tradición religiosa y cultural','Un jefe que debes atacar','Una máquina histórica'),
        ('¿Cómo presenta el juego la escena del mar?','Como representación del relato bíblico','Como una filmación de la época','Como una fecha arqueológica segura'),
        ('¿Qué debe distinguir el estudio histórico?','Tradición religiosa y evidencia arqueológica','Toda narración y una prueba concluyente','Un personaje bíblico y un robot'),
        ('¿Qué conclusión evita este mapa?','Identificar sin pruebas a un faraón concreto','Reconocer el valor cultural del Éxodo','Explicar que se trata de una tradición'))),
    )
    for title,fact,source,questions in rows:
        lessons.append(lesson(title,fact,base+source,*questions))
