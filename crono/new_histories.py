"""Seven additional routes with stable IDs and contextual, sourced learning."""
NEW_MAPS=(
 dict(name='Brasil · la Guerra de los Farrapos',focus='Rio Grande do Sul, 1835–1845: conflicto, recursos y desigualdades.',landmark='farrapos',combat=7,date='Brasil meridional · 1835–1845',
      source='Marinha do Brasil · Revoltas',url='https://www.marinha.mil.br/comemch/revoltas',
      topics=(('Un conflicto del Brasil imperial','La Guerra de los Farrapos o Revolución Farroupilha ocurrió entre 1835 y 1845, principalmente en Rio Grande do Sul y también en Santa Catarina. Enfrentó a rebeldes y fuerzas del Imperio del Brasil. No fue la guerra naval de Brown de 1825–1828.',
               ('¿Dónde comenzó la Guerra de los Farrapos?','Rio Grande do Sul','Egipto','Inglaterra'),('¿Qué fechas corresponden a este conflicto?','1835–1845','1914–1918','1810–1816')),
              ('No todos vivieron la misma guerra','El conflicto involucró intereses políticos y económicos y a personas con posiciones sociales distintas. Los Lanceiros Negros incluyeron hombres esclavizados que combatieron con expectativas de libertad. Una bandera rebelde no demuestra que existiera igualdad para toda la población.',
               ('¿Qué expectativa tuvieron muchos Lanceiros Negros?','Obtener la libertad','Viajar a la Luna','Construir pirámides'),('¿Qué evita una visión simplificada de la guerra?','Reconocer desigualdades y experiencias distintas','Suponer igualdad por llevar una bandera','Ignorar a las personas esclavizadas'))),
      curiosity=('lanceiros','Los Lanceiros Negros','Un regimiento permite preguntar quién luchó, bajo qué condiciones y qué significaba la libertad.'),
      mechanic=('Los caminos del abastecimiento','supply','Reúne tres cargas y entrégalas en el campamento.',('Reconocer el camino','Asegurar los suministros','Organizar la entrega'),'El reparto de recursos y sus consecuencias sociales importan tanto como una batalla. El convoy del reloj es ficticio.')),
 dict(name='Güemes · la Guerra Gaucha',focus='Salta y Jujuy: territorio, redes de apoyo y defensa del norte.',landmark='guemes',combat=7,date='Salta y Jujuy · 1814–1821',
      source='Argentina · Güemes y el Plan Continental',url='https://www.argentina.gob.ar/noticias/el-general-guemes-y-el-plan-continental-sanmartiniano',
      topics=(('La defensa del norte','Martín Miguel de Güemes organizó la resistencia en Salta y Jujuy durante las guerras de independencia. La Guerra Gaucha combinó conocimiento del terreno, movilidad, milicias y apoyo de la población. Güemes murió el 17 de junio de 1821.',
               ('¿Qué región defendieron Güemes y sus fuerzas?','El norte de las actuales provincias argentinas','El valle del Nilo','La costa de Inglaterra'),('¿Qué ayudaba a las partidas gauchas?','Conocer el terreno y coordinarse','Ignorar los caminos','Usar aviones modernos')),
              ('Una estrategia continental','La defensa del norte ayudó a sostener la estrategia independentista mientras San Martín preparaba y desarrollaba su campaña por los Andes. También participaron fuerzas de línea, como los Infernales. Las familias y los recursos de la región soportaron costos y conflictos.',
               ('¿Qué fuerza se vincula con Güemes?','Los Infernales','Los astronautas de Apolo','Los caballeros de una leyenda medieval'),('¿Cómo se relacionaban las campañas del norte y de los Andes?','Formaban parte de una estrategia más amplia','Ocurrieron en la Segunda Guerra Mundial','No tuvieron ningún contexto compartido'))),
      curiosity=('poncho_guemes','Un poncho y muchas historias','El poncho salteño remite a identidad y memoria; no reemplaza el estudio de las personas y redes que sostuvieron la campaña.'),
      mechanic=('Correos de la quebrada','courier','Recupera comunicaciones entre tres postas del norte.',('Reconocer la posta','Proteger los mensajes','Coordinar la llegada'),'La red de información y el conocimiento de los caminos ayudaban a la movilidad. El correo que rescata Crono pertenece a la ficción.')),
 dict(name='Alejandría · custodiar el conocimiento',focus='Bibliotecas, copias y transmisión de textos en el mundo antiguo.',landmark='library',combat=2,date='Alejandría · mundo helenístico',
      source='Bibliotheca Alexandrina · preguntas frecuentes',url='https://www.bibalex.org/fr/page/faq',
      topics=(('Una biblioteca también trabaja','La antigua biblioteca de Alejandría reunió textos y personas dedicadas al estudio en el mundo helenístico. Copiar, ordenar y comparar escritos ayudaba a transmitir conocimientos. Un rollo conservado y su interpretación actual no son la misma cosa.',
               ('¿Qué se reunía en una biblioteca antigua?','Textos para estudiar y conservar','Solo armas','Motores eléctricos'),('¿Qué tarea ayuda a encontrar y conservar textos?','Catalogar y copiar','Quitar sus referencias','Mezclar todas sus fechas')),
              ('La memoria no desaparece en un solo dibujo','La pérdida de la biblioteca se vincula con un proceso de daños y cambios a lo largo del tiempo; no se explica con certeza mediante una única escena de incendio. Algunos textos antiguos se transmitieron gracias a copias y traducciones en otros lugares.',
               ('¿Cómo pudieron transmitirse algunos textos antiguos?','Mediante copias y traducciones','Solamente por un rumor sin evidencias','Sin personas que los conservaran'),('¿Qué conviene evitar al explicar la pérdida de la biblioteca?','Afirmar que una imagen de incendio explica todo','Comparar fuentes','Reconocer lo que no sabemos'))),
      curiosity=('catalogue_roll','Las pistas de un catálogo','Un catálogo registra y organiza: también permite investigar qué se conserva y qué falta.'),
      mechanic=('El catálogo perdido','catalogue','Recupera tres fichas y vuelve al primer escritorio para ordenarlas manteniendo E.',('Preparar el catálogo','Comparar las fichas','Conservar las referencias'),'Conservar no es solo reunir objetos: importa registrar procedencia, título y contexto.')),
 dict(name='Maguncia · la imprenta transforma los textos',focus='Hacia 1450: tipos móviles, corrección y circulación de libros.',landmark='printing',combat=3,date='Maguncia · hacia 1450',
      source='Biblioteca Nacional Alemana · Gutenberg',url='https://mediengeschichte.dnb.de/DBSMZBN/Content/EN/Printing/04-gutenberg-johannes-en.html',
      topics=(('Letras que pueden volver a usarse','Hacia mediados del siglo XV, Gutenberg desarrolló en Maguncia un sistema europeo de impresión con tipos móviles metálicos. Componer, entintar y prensar permitía reproducir páginas. Gutenberg no inventó la escritura ni fue la primera persona de la historia en imprimir.',
               ('¿Dónde trabajó Gutenberg en su sistema de impresión?','Maguncia','Tucumán','La superficie lunar'),('¿Qué podía reorganizarse para componer páginas?','Los tipos móviles','Las estrellas','Los huesos fósiles')),
              ('Innovar tiene una historia','En China y Corea existieron técnicas de impresión y tipos móviles anteriores al sistema de Gutenberg. La difusión de libros también dependió de papel, oficios, comercio y lectores. Poder imprimir no significó que todas las personas supieran leer.',
               ('¿Existió impresión anterior a Gutenberg en Asia?','Sí, en China y Corea','No existía ninguna escritura','Solo en el siglo XX'),('¿Por qué imprimir más libros no equivale a alfabetización universal?','El acceso y la lectura también dependen de condiciones sociales','Porque los libros nunca circulan','Porque todas las personas ya sabían leer'))),
      curiosity=('movable_type','Una letra puede volver a imprimirse','Un tipo móvil es una pieza reutilizable: la tecnología también necesita trabajo y revisión.'),
      mechanic=('Componer, revisar, imprimir','printing','Recoge tres cajas de tipos y mantén E en la prensa final para imprimir.',('Preparar las cajas de letras','Revisar la composición','Preparar la tirada'),'La prensa del reloj simplifica un taller. Corregir antes de multiplicar una página es parte del aprendizaje.')),
 dict(name='Siracusa · el taller de las palancas',focus='Arquímedes, equilibrio e investigación mediante modelos.',landmark='lever',combat=2,date='Siracusa · siglo III a. C.',
      source='Museo Galileo · ciencia del equilibrio',url='https://catalogue.museogalileo.it/section/ScienceOfEquilibrium.html',
      topics=(('Una palanca cambia el esfuerzo','Arquímedes estudió problemas de equilibrio y geometría. Una palanca permite relacionar fuerza, distancia y punto de apoyo: no produce energía de la nada. Sus obras se estudian mediante textos, modelos y análisis de sus principios mecánicos.',
               ('¿Qué elemento es esencial en una palanca?','Un punto de apoyo','Un motor eléctrico obligatorio','Una antena de radio'),('¿Qué se relaciona al estudiar una palanca?','Fuerza y distancia respecto del apoyo','Solo el color del objeto','La fecha de una elección')),
              ('Un modelo no es una prueba de todo','Probar un modelo, medir y comparar resultados ayuda a explicar un mecanismo. Las leyendas atribuidas a un personaje deben distinguirse de las obras y evidencias disponibles. Atribuir un invento a una persona exige contrastar las fuentes.',
               ('¿Qué ayuda a comprobar una explicación mecánica?','Medir y comparar pruebas','Aceptar cualquier leyenda','Cambiar los datos para que coincidan'),('¿Qué debe distinguirse al estudiar a Arquímedes?','Evidencia y relatos legendarios','El color de dos enemigos','Solo el tamaño del dibujo'))),
      curiosity=('balance_arm','El punto de apoyo importa','Mover el apoyo cambia las distancias y el esfuerzo necesario: experimenta antes de concluir.'),
      mechanic=('Dos brazos, un equilibrio','lever','Acciona las palancas y usa dos plataformas elevadoras.',('Fijar el punto de apoyo','Comparar las cargas','Probar el equilibrio'),'Una máquina simple modifica cómo aplicamos la fuerza; no elimina el trabajo que hace falta.')),
 dict(name='Tombuctú · las rutas del manuscrito',focus='África occidental: comercio, estudio y conservación de documentos.',landmark='timbuktu',combat=3,date='Tombuctú · tradiciones de estudio',
      source='Library of Congress · manuscritos de Mali',url='https://www.loc.gov/exhibits/mali/mali-overview.html',
      topics=(('Una ciudad de intercambio y estudio','Tombuctú, en el actual Mali, fue un importante centro de comercio y aprendizaje. Sus manuscritos tratan temas como derecho, astronomía, medicina e historia. El conocimiento del pasado no se produjo únicamente en Europa.',
               ('¿En qué región está Tombuctú?','África occidental','La Antártida','El Río de la Plata'),('¿Qué temas pueden aparecer en sus manuscritos?','Astronomía, derecho e historia','Solo resultados deportivos actuales','Únicamente planos de aviones')),
              ('Custodiar también es producir historia','Familias, bibliotecas y especialistas han conservado manuscritos de Tombuctú. Registrar, proteger y estudiar esas colecciones permite revisar relatos históricos. Estas colecciones contienen documentos de distintas épocas.',
               ('¿Quiénes contribuyen a conservar colecciones?','Familias, bibliotecas y especialistas','Solo nombres sin documentos','Nadie necesita cuidarlas'),('¿Por qué importa conservar la procedencia de un manuscrito?','Permite investigar su contexto','Borra su historia','Hace innecesario leerlo'))),
      curiosity=('manuscript_box','Una biblioteca también puede ser familiar','Las colecciones familiares ayudan a comprender redes de aprendizaje y memoria en África occidental.'),
      mechanic=('Un camino para los manuscritos','manuscripts','Recupera tres manuscritos y acompaña a su guardiana hasta el depósito.',('Preparar cajas protectoras','Registrar la procedencia','Acordar la entrega'),'La protección del patrimonio implica personas, materiales y cooperación; no solo monumentos.')),
 dict(name='Bletchley Park · mensajes y cooperación',focus='Segunda Guerra Mundial: criptografía y trabajo colectivo.',landmark='bletchley',combat=5,date='Inglaterra · década de 1940',
      source='The National Museum of Computing · Bombe',url='https://www.tnmoc.org/bombe',
      topics=(('Leer un mensaje cifrado','En Bletchley Park se trabajó para descifrar comunicaciones durante la Segunda Guerra Mundial. La Bombe ayudó en el análisis de Enigma. Matemáticas, ingeniería, personal de operación e información previa participaron en ese trabajo colectivo.',
               ('¿Con qué se relaciona Bletchley Park?','El análisis de mensajes cifrados','La construcción de pirámides','La Revolución de Mayo'),('¿Qué máquina ayudó a analizar Enigma?','La Bombe','Una locomotora Rocket','El módulo lunar')),
              ('No fue una persona trabajando sola','Los equipos incluyeron numerosas mujeres y personas con oficios distintos; también existieron aportes polacos previos contra Enigma. Bombe y Colossus fueron máquinas diferentes. Los documentos permiten distinguir el cometido de cada máquina.',
               ('¿Qué explica mejor el trabajo de descifrado?','La cooperación de muchos equipos y aportes','Una sola persona sin colaboradores','Un invento sin contexto'),('¿Qué conviene distinguir?','Bombe y Colossus, porque no eran la misma máquina','Todas las máquinas como si fueran iguales','Todas las máquinas como un único invento'))),
      curiosity=('cipher_rotor','Un rotor no trabaja solo','Personas, máquinas y procedimientos formaban una red de trabajo: una cifra no se interpreta sin contexto.'),
      mechanic=('La secuencia de señales','cipher','Observa tres paneles y mantén E cuando su señal esté encendida.',('Registrar la primera señal','Contrastar la secuencia','Comprobar el resultado'),'Este ejercicio de atención es una simplificación de ficción, no una simulación de Enigma.')),
)

from .coldwar_content import COLD_WAR
NEW_MAPS+=COLD_WAR
from .world_wars import WAR_MAPS
NEW_MAPS+=WAR_MAPS

HISTORY_QUESTIONS={
 'Un conflicto del Brasil imperial':('¿En qué territorio comenzó la Guerra de los Farrapos?','Río Grande del Sur','Mendoza','Buenos Aires'),
 'No todos vivieron la misma guerra':('¿Qué grupo formó parte de los Lanceiros Negros?','Hombres negros esclavizados y libertos','Legionarios romanos','Escribas egipcios'),
 'La defensa del norte':('¿Qué fuerzas se asocian con Güemes?','Milicias gauchas','La escuadra de Brown','La tripulación del Apolo 11'),
 'Una estrategia continental':('¿Qué permitía el abastecimiento durante una campaña?','Sostener a las tropas durante la marcha','Prescindir de alimentos','Eliminar la necesidad de rutas'),
 'Una biblioteca también trabaja':('¿En qué ciudad se encontraba la célebre biblioteca helenística?','Alejandría','Londres','Berlín'),
 'La memoria no desaparece en un solo dibujo':('¿Cómo se investiga la historia de una biblioteca antigua?','Comparando textos, restos e investigaciones','Tomando un rumor como certeza','Suponiendo que todos sus documentos se conservaron'),
 'Letras que pueden volver a usarse':('¿Qué se reutiliza en la impresión con tipos móviles?','Las piezas con letras','La tinta ya seca de una página','Los márgenes de un libro encuadernado'),
 'Innovar tiene una historia':('¿Por qué se investigan los antecedentes de una técnica?','Permiten comprender cómo cambió con el tiempo','Demuestran que todo se inventó en un día','Hacen innecesarias las fechas'),
 'Una palanca cambia el esfuerzo':('¿Qué necesita una palanca para girar?','Un punto de apoyo','Una caldera de vapor','Una antena'),
 'Un modelo no es una prueba de todo':('¿Qué relaciona el estudio de las palancas?','Fuerza, distancia y punto de apoyo','Solo el color de los materiales','Únicamente la edad de una herramienta'),
 'Una ciudad de intercambio y estudio':('¿En qué país actual se encuentra Tombuctú?','Mali','Egipto','Grecia'),
 'Custodiar también es producir historia':('¿Quiénes contribuyeron a conservar manuscritos de Tombuctú?','Familias, bibliotecas y especialistas','Solo navegantes del Río de la Plata','Únicamente tripulaciones espaciales'),
 'Leer un mensaje cifrado':('¿Qué máquina ayudó a analizar mensajes de Enigma?','La Bombe','La locomotora Rocket','El motor de Newcomen'),
 'No fue una persona trabajando sola':('¿Qué caracterizó el trabajo de descifrado en Bletchley Park?','La cooperación de equipos y distintas especialidades','La tarea de una sola persona sin antecedentes','La ausencia de matemáticas'),
 'Un mundo en tensión':('¿Qué países encabezaron los principales bloques de la Guerra Fría?','Estados Unidos y la Unión Soviética','Grecia y Egipto','Argentina y el Imperio del Brasil'),
 'Berlín y sus habitantes':('¿En qué año se abrieron los pasos del muro de Berlín?','1989','1961','1817'),
 'La gravedad no desaparece':('¿Cómo es la gravedad en la superficie lunar respecto de la terrestre?','Aproximadamente una sexta parte','Exactamente igual','Seis veces mayor'),
 'Explorar requiere preparación':('¿Quién permaneció en órbita durante el alunizaje del Apolo 11?','Michael Collins','Neil Armstrong','Buzz Aldrin'),
 'Cambios que no ocurren en un solo día':('¿Qué ocurrió con la Unión Soviética en 1991?','Se disolvió','Se fundó el Imperio del Brasil','Comenzó la Revolución de Mayo'),
 'Investigar también exige escuchar':('¿Por qué se comparan testimonios sobre un mismo proceso?','Aportan experiencias y perspectivas diferentes','Todos describen exactamente lo mismo','La comparación reemplaza las fechas'),
}


def extend_new(Stage,lesson,stages,lessons,sources):
    for row in NEW_MAPS:
        stages.append(Stage(row['name'],row['focus'],row['landmark']))
        source=len(sources);sources.append((row['source'],row['url']))
        for topic in row['topics']:
            title,fact,q1,q2=topic[:4]
            if title=='No todos vivieron la misma guerra':
                source=len(sources);sources.append(('Senado Federal · Lanceiros Negros','https://www12.senado.leg.br/noticias/materias/2023/03/15/paim-fala-sobre-aprovacao-de-lanceiros-negros-no-livro-dos-herois-da-patria'))
            if title=='Explorar requiere preparación':
                source=len(sources);sources.append(('NASA · Apollo 11','https://www.nasa.gov/mission/apollo-11/'))
            if len(topic)==8:questions=topic[2:]
            else:
                from .specific_questions import EXTRA
                extra=EXTRA[title]
                questions=(q1,q2,extra[0],HISTORY_QUESTIONS[title],extra[1],extra[2])
            lessons.append(lesson(title,fact,source,*questions))
