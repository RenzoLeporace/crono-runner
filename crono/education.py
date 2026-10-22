"""Original age-graded question bank. Facts are paraphrased from cited museums.

Each of 30 topics has six authored questions: two per age band, 180 total.
The correct answer's position is randomised at runtime, never encoded in the UI.
"""
from dataclasses import dataclass
import random

AGE_BANDS=('6–9 años','10–14 años','15 años en adelante')
SOURCES=[
 ('Natural History Museum · Pterosaurios','https://www.nhm.ac.uk/discover/the-truth-about-pterosaurs.html'),
 ('Natural History Museum · Fósiles','https://www.nhm.ac.uk/discover/how-are-fossils-formed.html'),
 ('Natural History Museum · Extinción','https://www.nhm.ac.uk/discover/dinosaur-extinction.html'),
 ('Natural History Museum · Mamuts','https://www.nhm.ac.uk/discover/were-all-mammoths-woolly.html'),
 ('Smithsonian · Herramientas y alimento','https://humanorigins.si.edu/human-characteristics/tools-food'),
 ('UNESCO · Cuevas del Vézère','https://whc.unesco.org/en/list/85/'),
 ('British Museum · Atenas y ciudadanía','https://www.britishmuseum.org/sites/default/files/2023-04/Luxury_and_power_large_print_guide.pdf'),
 ('British Museum · Atenas y el Mediterráneo','https://www.britishmuseum.org/collection/galleries/greece-athens-and-lycia'),
 ('UNESCO · Olimpia','https://whc.unesco.org/en/list/517/'),
 ('English Heritage · Byland Abbey','https://www.english-heritage.org.uk/visit/places/byland-abbey/history/'),
 ('The National Archives · Mercados y ferias','https://www.nationalarchives.gov.uk/help-with-your-research/research-guides/markets-fairs'),
 ('Victoria and Albert Museum · El gótico','https://www.vam.ac.uk/articles/the-gothic-style-an-introduction'),
 ('National Museums Scotland · Motor de Newcomen','https://www.nms.ac.uk/discover-catalogue/the-newcomen-engine-and-its-role-in-britains-industrial-revolution'),
 ('Science Museum Group · Rocket','https://collection.sciencemuseumgroup.org.uk/objects/co26704'),
 ('London Museum · Electricidad','https://www.londonmuseum.org.uk/collections/london-stories/when-did-london-get-electricity/'),
]


@dataclass(frozen=True)
class Stage:
    name: str
    focus: str
    landmark: str


STAGES=[
 Stage('La costa de los gigantes','Dinosaurios, aves y reptiles voladores.','coast'),
 Stage('El valle de los fósiles','Cómo las rocas conservan señales de vida.','fossils'),
 Stage('El cielo que cambió el mundo','Extinción, supervivencia y cambios ambientales.','crater'),
 Stage('La estepa del mamut','Adaptaciones de los animales al frío.','mammoth'),
 Stage('El refugio del fuego','Herramientas y preparación de los alimentos.','cave'),
 Stage('La cueva de las manos','Arte paleolítico y evidencias del pasado.','paintings'),
 Stage('El ágora de Atenas','Participación política y exclusiones en la Grecia clásica.','agora'),
 Stage('Las rutas del Mediterráneo','Cerámica, navegación e intercambio.','harbor'),
 Stage('El santuario de Olimpia','Juegos, arquitectura y encuentros entre ciudades.','stadium'),
 Stage('Los campos de la abadía','Ganadería y economía de un monasterio inglés.','fields'),
 Stage('La ciudad de los mercaderes','Mercados y documentos medievales de Inglaterra y Gales.','market'),
 Stage('Las torres de luz','Arcos, vidrieras y construcción gótica europea.','cathedral'),
 Stage('La fuerza del vapor','Máquinas, minas y transformación de energía.','engine'),
 Stage('El camino de hierro','Ferrocarril y pruebas de nuevas tecnologías.','railway'),
 Stage('La ciudad eléctrica','Innovación y adopción gradual de la electricidad.','electric'),
]


@dataclass(frozen=True)
class Lesson:
    title: str
    fact: str
    source: int
    questions: tuple


def lesson(title,fact,source,*questions):
    assert len(questions)==6
    return Lesson(title,fact,source,questions)


# Every question tuple contains prompt, correct answer, and two distractors.
LESSONS=[
 lesson('Alas que no son de dinosaurio',
  'Los pterosaurios eran reptiles voladores, distintos de los dinosaurios. Sus alas tenían una membrana sostenida por un dedo muy alargado.',0,
  ('¿Qué eran los pterosaurios?','Reptiles voladores','Peces gigantes','Mamíferos con pelo'),
  ('¿Qué sostenía su ala?','Un dedo alargado','Una aleta de pez','Una rama de árbol'),
  ('¿Por qué tener alas no basta para ser dinosaurio?','Distintos grupos pueden volar','Todo animal volador es dinosaurio','Las alas solo existen en aves'),
  ('¿Qué cubierta formaba el ala del pterosaurio?','Una membrana','Una concha rígida','Una hoja de planta'),
  ('¿Qué comparación anatómica es pertinente?','La estructura que sostiene cada ala','Solo el tamaño de los animales','Solo el lugar donde se encontró el fósil'),
  ('¿Qué afirmación confunde grupos diferentes?','Todos los reptiles voladores eran dinosaurios','Los pterosaurios tenían alas de membrana','No todo reptil mesozoico era dinosaurio')),
 lesson('Comparar para conocer',
  'Las alas de las aves están cubiertas de plumas; las de los pterosaurios tenían membranas. Comparar huesos y alas permite distinguir estos grupos.',0,
  ('¿Qué cubre las alas de un ave?','Plumas','Escamas de pescado','Hojas verdes'),
  ('¿Qué podemos comparar en dos fósiles?','Sus huesos','Su comida favorita exacta','Sus nombres inventados'),
  ('¿Qué diferencia ayuda a distinguir estas alas?','Plumas frente a membrana','Que ambas permiten volar','Que ambas pertenecen a animales'),
  ('¿Cómo investigarías un ala fósil?','Observando su estructura','Suponiendo que todo volador es igual','Mirando solo su color actual'),
  ('¿Qué dato apoya mejor una clasificación?','Rasgos anatómicos comparables','El apodo popular del ejemplar','La fama de la especie'),
  ('¿Qué es una conclusión prudente?','Volar no implica pertenecer al mismo grupo','Dos alas prueban que son la misma especie','Todo fósil de ala pertenece a un ave')),
 lesson('Del sedimento a la roca',
  'El enterramiento por sedimentos puede proteger restos. Con mucho tiempo, los minerales pueden conservar o reemplazar partes de esos restos; fosilizarse es poco frecuente.',1,
  ('¿Qué puede cubrir y proteger unos restos?','Sedimentos','Un paraguas moderno','Una manta de tela'),
  ('¿Se fosilizan todos los animales?','No, es poco frecuente','Sí, siempre','Solo si son gigantes'),
  ('¿Qué favorece conservar un resto?','Quedar cubierto por sedimentos','Quedar expuesto para siempre','Moverlo cada día'),
  ('¿Qué puede ocurrir durante la fosilización?','Intervienen minerales','El animal revive','El hueso se vuelve plástico'),
  ('¿Por qué el registro fósil es incompleto?','La fosilización es poco frecuente','Todos los restos se conservan igual','Nunca hubo animales pequeños'),
  ('¿Qué conclusión sería incorrecta?','Si no hay fósil, esa especie nunca existió','El enterramiento puede proteger restos','Los minerales pueden intervenir en su conservación')),
 lesson('Huellas de una vida',
  'Huesos y dientes son restos del cuerpo. Huellas y otras señales de actividad también pueden fosilizarse: cuentan algo de lo que un organismo hizo.',1,
  ('¿Cuál es un resto del cuerpo?','Un diente','Una pisada','Una sombra actual'),
  ('¿Qué puede mostrar una huella?','Que un animal pisó allí','Su nombre exacto','Que llevaba un reloj'),
  ('¿Cuál es una señal de actividad?','Un rastro de pisadas','Un hueso de la pata','Un diente de la mandíbula'),
  ('¿Qué diferencia hay entre hueso y huella?','Uno es corporal; la otra registra actividad','Ambos son órganos vivos','La huella es siempre una pintura'),
  ('¿Qué pregunta se estudia mejor con pisadas?','Cómo se desplazaba un organismo','Cuál era su nombre individual','Qué sonido emitió exactamente'),
  ('¿Por qué conviene estudiar restos y rastros?','Aportan evidencias distintas','Son pruebas idénticas','Las huellas nunca aportan información')),
 lesson('Un impacto y sus consecuencias',
  'Hace unos 66 millones de años, un gran asteroide impactó la Tierra. El evento alteró el ambiente y está relacionado con una extinción masiva.',2,
  ('¿Qué chocó con la Tierra?','Un asteroide','Un tren','Un barco'),
  ('¿Hace cuánto ocurrió este impacto?','Unos 66 millones de años','Hace 66 días','En el año 1889'),
  ('¿Qué cambió tras el impacto?','Las condiciones ambientales','La existencia de la gravedad','La forma de todos los átomos'),
  ('¿Qué significa una extinción masiva?','Desaparecen muchas especies','Se esconde un solo animal','Todos los seres se vuelven más grandes'),
  ('¿Cómo puede un impacto afectar a muchas especies?','Al alterar los ambientes de los que dependen','Solo golpeando directamente a cada individuo','Eliminando la necesidad de alimento'),
  ('¿Qué relación respalda la evidencia estudiada?','Impacto, cambio ambiental y extinción','Impacto y nacimiento de la humanidad','Impacto y comienzo del ferrocarril')),
 lesson('Un mundo con supervivientes',
  'La extinción del final del Cretácico no eliminó toda la vida. Desaparecieron los dinosaurios no avianos; las aves son dinosaurios que sobrevivieron.',2,
  ('¿Qué dinosaurios siguen existiendo hoy?','Las aves','Los automóviles','Los mamuts'),
  ('¿Desapareció toda la vida?','No','Sí, toda','Solo quedaron piedras sin vida'),
  ('¿Cuál es una forma precisa de decirlo?','Se extinguieron los dinosaurios no avianos','No sobrevivió ningún dinosaurio','Las aves aparecieron como máquinas'),
  ('¿Qué grupo actual conecta con los dinosaurios?','Los pájaros','Los peces de colores','Los caracoles'),
  ('¿Qué error contiene decir que murieron todos los dinosaurios?','Ignora a las aves supervivientes','Confunde aves con plantas','Supone que nunca hubo extinciones'),
  ('¿Qué conclusión permite la supervivencia de las aves?','Los efectos de una extinción no son iguales para todos','Todas las especies se extinguen juntas','Nada cambió en los ecosistemas')),
 lesson('Abrigo para la estepa',
  'El mamut lanudo tenía pelaje y orejas pequeñas, rasgos relacionados con la vida en ambientes fríos. Sus parientes no tenían todos el mismo aspecto.',3,
  ('¿Qué ayudaba a abrigar al mamut lanudo?','Su pelaje','Unas plumas de metal','Un paraguas'),
  ('¿Cómo eran sus orejas frente a las de elefantes actuales?','Pequeñas','Como velas de barco','No tenía cabeza'),
  ('¿Qué combinación encaja con el frío?','Pelaje y orejas pequeñas','Ausencia de abrigo y grandes orejas','Aletas y branquias'),
  ('¿Qué es una adaptación en este contexto?','Un rasgo relacionado con vivir en un ambiente','Un objeto comprado por un animal','Un cambio elegido cada mañana'),
  ('¿Qué lectura evita atribuir intención al animal?','Sus rasgos se relacionan con adaptación al frío','Decidió fabricar orejas pequeñas','Diseñó su propio pelaje de repente'),
  ('¿Qué dato compararías para estudiar adaptación?','Rasgos de distintos mamuts y sus ambientes','Solo el nombre de cada museo','La longitud del cartel del fósil')),
 lesson('No todos los mamuts eran iguales',
  'Hubo distintas especies de mamut. El mamut lanudo es una de ellas: no debemos imaginar que todos los mamuts tuvieron siempre un pelaje idéntico.',3,
  ('¿Hubo un solo tipo de mamut?','No, hubo varias especies','Sí, uno solo','Todos eran aves'),
  ('¿Cuál de estos nombres corresponde a un mamut?','Mamut lanudo','Locomotora lanuda','Pez de hierro'),
  ('¿Qué generalización hay que evitar?','Todos los mamuts eran idénticos','Existieron especies distintas','El lanudo era un mamut'),
  ('¿Qué conviene estudiar además de un ejemplar?','Otros mamuts y sus diferencias','Solo una película de ficción','Solo un dibujo inventado'),
  ('¿Por qué un ejemplar no representa toda la diversidad?','El grupo incluía distintas especies','Toda variación es imposible','Todos vivieron en el mismo instante'),
  ('¿Qué afirmación es más rigurosa?','Los rasgos pueden variar entre especies de mamut','Todo mamut era un clon del lanudo','El nombre mamut describe una sola apariencia')),
 lesson('Piedra que se vuelve herramienta',
  'Los humanos y sus antepasados fabricaron herramientas de piedra mucho antes de las ciudades. Los filos podían servir para cortar y procesar alimentos.',4,
  ('¿Qué material usaban para estas herramientas?','Piedra','Plástico','Pantallas táctiles'),
  ('¿Para qué sirve un filo?','Para cortar','Para iluminar eléctricamente','Para volar'),
  ('¿Qué actividad podía facilitar una herramienta?','Procesar alimento','Enviar correos electrónicos','Construir ferrocarriles modernos'),
  ('¿Qué es más antiguo que las ciudades?','El uso de herramientas de piedra','La iluminación eléctrica','El motor de vapor industrial'),
  ('¿Qué evidencia se puede comparar con un filo?','Marcas de corte en restos animales','El color de un cartel moderno','La forma de una nube actual'),
  ('¿Qué conclusión evita una idea equivocada?','La tecnología no empezó con las máquinas industriales','No hubo tecnología antes del metal','Toda herramienta necesita electricidad')),
 lesson('Cocinar transforma',
  'Controlar el fuego permitió cocinar. Preparar así los alimentos puede facilitar su digestión y cambiar cómo se aprovechan sus nutrientes.',4,
  ('¿Qué permite cocinar sin electricidad?','El fuego','Una piedra fría por sí sola','Una sombra'),
  ('¿Qué se puede preparar con el fuego?','Alimentos','Mensajes por Internet','Billetes de tren'),
  ('¿Qué cambió con la cocción?','La preparación y digestión de alimentos','La necesidad de alimentarse desapareció','Todos los alimentos se volvieron iguales'),
  ('¿Qué uso del fuego explica este panel?','Cocinar','Fabricar teléfonos','Crear hielo sin enfriamiento'),
  ('¿Por qué controlar el fuego fue un cambio tecnológico?','Permitió transformar alimentos','No alteró ninguna actividad','Sustituyó todos los recursos naturales'),
  ('¿Qué afirmación es prudente sobre la cocción?','Puede facilitar el aprovechamiento de alimentos','Hace comestible cualquier sustancia','Elimina toda necesidad de nutrientes')),
 lesson('Pintar en una cueva',
  'En el valle del Vézère, en Francia, hay cuevas con arte paleolítico. En Lascaux se representaron animales: estas imágenes son evidencias de actividad humana.',5,
  ('¿Dónde están estas pinturas?','En cuevas','En pantallas antiguas','En vagones eléctricos'),
  ('¿Qué aparece representado en Lascaux?','Animales','Automóviles','Aviones modernos'),
  ('¿Qué tipo de evidencia son las pinturas?','Evidencia de actividad humana','Una fotografía tomada por dinosaurios','Prueba de electricidad prehistórica'),
  ('¿En qué país está Lascaux?','Francia','Japón','Australia'),
  ('¿Qué podemos afirmar directamente al estudiar estas imágenes?','Que hubo representaciones realizadas por humanos','El significado exacto de cada imagen sin investigar','El nombre de todos sus autores'),
  ('¿Qué distingue observación de interpretación?','Ver animales pintados no revela por sí solo toda su intención','Toda interpretación es una observación directa','Una pintura explica toda una sociedad')),
 lesson('Cuidar las evidencias',
  'Las cuevas decoradas del Vézère forman parte del Patrimonio Mundial. Conservar estos lugares protege testimonios que permiten investigar el pasado.',5,
  ('¿Qué conviene hacer con una pintura antigua?','Protegerla','Rayarla','Pintar encima'),
  ('¿Qué nos ayuda a conocer?','El pasado humano','La contraseña de Crono','El futuro exacto'),
  ('¿Por qué conservar una cueva decorada?','Para proteger evidencias','Para borrar sus dibujos','Para sustituirla por una copia sin registro'),
  ('¿Qué reconoce la UNESCO en estos sitios?','Su valor como patrimonio','Que sean parques de máquinas','Que todos sus dibujos sean modernos'),
  ('¿Qué se pierde si destruimos una evidencia?','Información difícil o imposible de recuperar','Solo una decoración reemplazable sin pérdida','La necesidad de investigar'),
  ('¿Qué decisión favorece investigar a largo plazo?','Conservar y documentar el sitio','Alterarlo sin registrar cambios','Elegir una interpretación y borrar las otras')),
 lesson('Decidir en Atenas',
  'En la democracia ateniense, los ciudadanos varones adultos participaban en las decisiones políticas. La participación no se extendía a toda la población.',6,
  ('¿Qué ciudad estudiamos aquí?','Atenas','Londres industrial','Una estación espacial'),
  ('¿Qué hacían los ciudadanos con derechos políticos?','Participaban en decisiones','Conducían trenes eléctricos','Elegían dinosaurios'),
  ('¿Quiénes participaban en estas decisiones?','Ciudadanos varones adultos','Toda persona sin excepción','Solo turistas extranjeros'),
  ('¿Por qué no era participación universal?','Había grupos excluidos','Todos tenían exactamente los mismos derechos','No había decisiones colectivas'),
  ('¿Qué comparación con el presente exige cuidado?','La palabra democracia no implica iguales derechos en toda época','Toda democracia histórica fue idéntica','La ciudadanía nunca cambió'),
  ('¿Qué pregunta permite examinar un sistema político?','Quién puede participar y quién queda excluido','Solo el tamaño de sus edificios','Solo la cantidad de cerámica')),
 lesson('Las personas que quedaban fuera',
  'En Atenas, las mujeres, los residentes extranjeros y las personas esclavizadas estaban excluidos de la participación política descrita en este sistema.',6,
  ('¿Todas las personas podían participar políticamente?','No','Sí, sin excepción','Solo los animales'),
  ('¿Qué grupo estaba excluido?','Las personas esclavizadas','Todos los varones ciudadanos adultos','Los relojes'),
  ('¿Qué muestra esta exclusión?','Que los derechos eran desiguales','Que todas las personas votaban','Que no había población extranjera'),
  ('¿Quiénes tampoco accedían a esa participación?','Las mujeres y los residentes extranjeros','Todos los ciudadanos varones adultos','Ningún grupo humano'),
  ('¿Qué afirmación es compatible con estas evidencias?','Un sistema puede ser llamado democrático y mantener exclusiones','El nombre democrático elimina toda desigualdad','La esclavitud otorgaba iguales derechos políticos'),
  ('¿Qué enfoque mejora una explicación histórica?','Examinar también a los grupos excluidos','Describir solo a quienes tenían poder','Suponer que el pasado tenía las reglas actuales')),
 lesson('Barcos que conectan ciudades',
  'La Atenas clásica tuvo un poderoso imperio marítimo. Las rutas del Mediterráneo conectaban ciudades y favorecían la circulación de bienes.',7,
  ('¿Por dónde viajaban estos barcos?','Por el mar','Por vías de tren','Por la Luna'),
  ('¿Qué mar aparece en este mapa?','El Mediterráneo','Un océano de lava','Un mar de plástico'),
  ('¿Qué permitían las rutas marítimas?','Conectar ciudades y mover bienes','Aislar para siempre todos los puertos','Eliminar todos los intercambios'),
  ('¿Qué significa marítimo?','Relacionado con el mar','Relacionado con trenes','Relacionado con volcanes solamente'),
  ('¿Por qué estudiar rutas además de ciudades?','Permite analizar sus conexiones','Cada ciudad existía sin contactos','Las rutas solo son decoración'),
  ('¿Qué sería una conclusión exagerada?','El comercio hizo iguales a todas las sociedades','Las ciudades mantuvieron contactos','Los barcos transportaban bienes')),
 lesson('La cerámica también viaja',
  'La cerámica pintada de Atenas se exportó por el Mediterráneo. Los objetos de una colección pueden ayudar a estudiar producción, comercio y relaciones entre comunidades.',7,
  ('¿Qué objeto viajaba desde Atenas?','Cerámica pintada','Computadoras','Locomotoras'),
  ('¿Qué material forma una vasija de cerámica?','Arcilla cocida','Hielo puro','Cables eléctricos'),
  ('¿Qué puede indicar una vasija lejos de su lugar de producción?','Circulación de objetos','Que las ciudades nunca se conectaron','Que la vasija volaba sola'),
  ('¿Qué quiere decir exportar?','Enviar productos a otros lugares','Esconderlos para siempre','Fabricar solo para destruir'),
  ('¿Por qué el contexto de hallazgo importa?','Ayuda a interpretar la circulación del objeto','La ubicación nunca aporta información','Todo objeto hallado fue fabricado allí'),
  ('¿Qué afirmación evita una inferencia automática?','Un objeto ateniense no convierte su lugar de hallazgo en Atenas','Toda vasija prueba una conquista militar','Un único objeto cuenta toda la historia del comercio')),
 lesson('Encuentro en Olimpia',
  'Los juegos de la antigua Olimpia se celebraban cada cuatro años. El lugar era un santuario con espacios de culto y de competición.',8,
  ('¿Dónde se celebraban estos juegos?','En Olimpia','En una fábrica','En el espacio'),
  ('¿Cada cuántos años se celebraban?','Cada cuatro años','Cada cuatro días','Cada cien años'),
  ('¿Qué combinaba el sitio de Olimpia?','Culto y competiciones','Minas y centrales eléctricas','Aeropuertos y autopistas'),
  ('¿Qué significa una celebración cada cuatro años?','Hay cuatro años entre celebraciones','Hay cuatro celebraciones al día','Ocurre una sola vez'),
  ('¿Por qué sería incompleto describir Olimpia solo como estadio?','También era un santuario','Nunca se practicó deporte allí','Solo tuvo edificios modernos'),
  ('¿Qué ayuda a comprender el lugar históricamente?','Relacionar sus funciones religiosas y deportivas','Aplicar sin cambios las reglas del deporte actual','Estudiar solo su nombre moderno')),
 lesson('Piedras con distintas funciones',
  'En el sitio arqueológico de Olimpia se conservan restos de templos y estructuras deportivas. Su distribución ayuda a comprender las actividades del santuario.',8,
  ('¿Qué edificio se relaciona con el culto?','Un templo','Una locomotora','Un poste eléctrico'),
  ('¿Qué espacio sirve para competir?','Un estadio','Una chimenea','Un motor de vapor'),
  ('¿Qué estudia un sitio arqueológico?','Restos materiales y sus relaciones','Solo relatos inventados','Únicamente edificios actuales'),
  ('¿Qué aporta ubicar templos y espacios deportivos?','Entender funciones del conjunto','Demostrar que todo era una vivienda','Borrar diferencias entre actividades'),
  ('¿Qué evidencia apoya funciones múltiples en Olimpia?','La presencia de templos y estructuras deportivas','Solo un nombre en un mapa actual','Una única piedra sin contexto'),
  ('¿Cómo evitar interpretar mal una ruina?','Combinar ubicación, estructura y otras evidencias','Adivinar solo por su tamaño','Asignar a todos los edificios la misma función')),
 lesson('Ovejas y lana',
  'La abadía inglesa de Byland obtenía ingresos de criar ovejas y vender lana. Un monasterio podía participar en actividades económicas además de religiosas.',9,
  ('¿Qué animal aportaba lana?','La oveja','Un pez','Un pterosaurio'),
  ('¿Qué vendía Byland según este ejemplo?','Lana','Teléfonos','Motores eléctricos'),
  ('¿Qué muestra el caso de Byland?','La conexión entre monasterios y economía','Que los monasterios nunca producían bienes','Que la lana se fabricaba con vapor'),
  ('¿Qué actividad era ganadera?','Criar ovejas','Construir un tren','Pintar una vidriera'),
  ('¿Qué generalización refuta este ejemplo?','Los monasterios estaban separados de toda actividad económica','Hubo comercio de lana','Las instituciones tenían varias funciones'),
  ('¿Qué conviene investigar para comprender la abadía?','Sus ingresos y actividades además de sus edificios','Solo la altura de una torre','Solo leyendas sin contrastar')),
 lesson('Un caso no es toda una época',
  'Byland es un ejemplo concreto de economía monástica en Inglaterra. Su historia ayuda a estudiar la Edad Media, pero no representa a todas las comunidades del mundo.',9,
  ('¿Dónde está el ejemplo estudiado?','En Inglaterra','En la Luna','Bajo el océano'),
  ('¿Todas las comunidades vivían igual?','No','Sí, sin diferencias','No había personas'),
  ('¿Qué alcance tiene este ejemplo?','Una abadía y su contexto','Todo el planeta sin excepciones','Solo el futuro de Crono'),
  ('¿Qué hace falta para comparar comunidades?','Estudiar más casos','Suponer que todas eran idénticas','Ignorar sus diferencias'),
  ('¿Por qué hay que indicar lugar y contexto?','Para no convertir un caso en una regla universal','Porque todas las regiones eran iguales','Porque la evidencia no necesita ubicación'),
  ('¿Qué conclusión es defendible?','Algunos monasterios ingleses obtuvieron ingresos de la lana','Toda sociedad medieval dependía de Byland','Toda institución tenía el mismo ingreso')),
 lesson('Un lugar para intercambiar',
  'En la Inglaterra y el Gales medievales existían mercados y ferias. Sus concesiones podían quedar registradas en documentos reales.',10,
  ('¿Qué se hacía en un mercado?','Intercambiar y vender bienes','Pilotar aviones','Fabricar dinosaurios'),
  ('¿Qué podía autorizar un documento real?','Un mercado o una feria','Un viaje espacial','Una red de Internet'),
  ('¿Qué conecta un mercado con el campo?','La circulación de productos','La desaparición de todos los caminos','Que no se intercambiaba nada'),
  ('¿Qué evidencia ayuda a estudiar una feria medieval?','Documentos de concesión','Un anuncio de televisión actual','Una novela sin fuentes'),
  ('¿Qué permite estudiar una concesión real?','Aspectos de la autorización de un mercado','Cada venta que ocurrió durante siglos','La identidad de todos sus visitantes'),
  ('¿Qué cautela es importante con estas fuentes?','Una autorización no describe toda la vida del mercado','Un documento contiene toda la historia','Si hay un mercado, no existen leyes')),
 lesson('Los archivos guardan pistas',
  'The National Archives conserva registros útiles para investigar mercados y ferias. Los documentos no siempre indican todos los detalles, como su ubicación exacta o sus normas.',10,
  ('¿Qué guarda un archivo histórico?','Documentos','Solo juguetes','Únicamente plantas'),
  ('¿Un documento cuenta todos los detalles?','No siempre','Sí, siempre','Nunca cuenta nada'),
  ('¿Qué hacer si falta un dato?','Buscar y comparar otras evidencias','Inventarlo y darlo por cierto','Ignorar todos los documentos'),
  ('¿Qué detalle puede faltar en los registros?','La ubicación exacta del mercado','El hecho de que son documentos','Que tienen información escrita'),
  ('¿Qué distingue ausencia de dato de ausencia del hecho?','Que un registro no lo mencione no prueba que no ocurriera','Todo silencio documental prueba inexistencia','Un archivo es una copia completa del pasado'),
  ('¿Qué práctica mejora una investigación?','Reconocer límites y contrastar fuentes','Ocultar lo que no sabemos','Tratar cada documento como verdad completa')),
 lesson('Arcos que apuntan al cielo',
  'La arquitectura gótica empleó arcos apuntados, bóvedas de crucería y arbotantes. Estas soluciones ayudaban a construir edificios altos y a gestionar las cargas.',11,
  ('¿Qué forma tiene un arco apuntado?','Termina en punta','Es una línea plana','Es un cuadrado cerrado'),
  ('¿Qué construcciones estudiamos aquí?','Edificios góticos','Estaciones espaciales','Fábricas de plástico'),
  ('¿Para qué servían los arbotantes?','Para ayudar a sostener las cargas','Para impulsar trenes','Para cocinar alimentos'),
  ('¿Qué rasgo pertenece al gótico?','La bóveda de crucería','El motor eléctrico','El ala de un pterosaurio'),
  ('¿Qué relación explica estas soluciones?','Forma constructiva y distribución de fuerzas','La altura depende solo de decoración','La piedra no ejerce peso'),
  ('¿Por qué conviene estudiar varios elementos a la vez?','Trabajan como un sistema estructural','Cada elemento elimina la gravedad','La estructura no influye en el edificio')),
 lesson('Luz de colores',
  'Las grandes vidrieras y los rosetones son rasgos del arte gótico. Los marcos de piedra y las soluciones estructurales hicieron posibles ventanas más amplias.',11,
  ('¿Qué deja pasar una vidriera?','Luz','Trenes','Rocas gigantes'),
  ('¿Qué es un rosetón en este contexto?','Una ventana circular decorada','Una flor del jardín solamente','Un tipo de locomotora'),
  ('¿Qué relación había entre estructura y ventanas?','Las soluciones constructivas permitían abrir más espacio','Las ventanas no requerían sostén','El vidrio soportaba solo todo el techo'),
  ('¿Qué aportaban las vidrieras al interior?','Luz y color','Vapor para mover motores','Aire acondicionado eléctrico'),
  ('¿Por qué no basta describir una catedral por su decoración?','La estructura condiciona los espacios y la luz','La decoración elimina las cargas','Toda ventana es independiente del edificio'),
  ('¿Qué explicación integra arte y técnica?','La construcción permite espacios para vidrieras','El color reemplaza todo soporte','El tamaño de una ventana no tiene límites físicos')),
 lesson('La máquina que sacaba agua',
  'Newcomen desarrolló en 1712 un motor empleado para bombear agua de minas. El vapor y su condensación intervenían en su funcionamiento.',12,
  ('¿Qué sacaba este motor de las minas?','Agua','Plumas','Cuadernos de Crono'),
  ('¿Qué material produce vapor al calentarse?','Agua','Una piedra seca por sí sola','Un cable sin energía'),
  ('¿Qué problema ayudó a resolver?','La acumulación de agua en minas','La falta de juegos deportivos','La ausencia de cerámica griega'),
  ('¿En qué año se desarrolló este tipo de motor?','1712','66 millones de años atrás','El año pasado'),
  ('¿Qué muestra el origen de esta máquina?','Una innovación puede responder a un problema concreto','Toda máquina surgió para mover trenes','El vapor no tuvo aplicaciones mineras'),
  ('¿Qué proceso forma parte del motor estudiado?','La condensación del vapor','La creación de energía de la nada','La desaparición de la presión atmosférica')),
 lesson('Energía para transformar',
  'El carbón fue importante en la industrialización británica. Los motores y la extracción de minerales se relacionaron con un aumento de la producción mediante máquinas.',12,
  ('¿Qué combustible se usó mucho?','Carbón','Cubitos de hielo','Pintura de cueva'),
  ('¿Qué aumentó con la mecanización?','La producción con máquinas','La cantidad de dinosaurios','La duración de los días'),
  ('¿Qué conexión se observa entre minas e industria?','Las minas aportaban recursos para la producción','Las minas solo eran decoración','No existía relación económica'),
  ('¿Las máquinas crean energía de la nada?','No, transforman energía','Sí, siempre','Solo cuando son grandes'),
  ('¿Qué afirmación evita atribuir todo a un único invento?','Máquinas, recursos y producción se relacionaban','Un solo motor explica toda la historia mundial','El carbón no tuvo usos industriales'),
  ('¿Qué hay que considerar al estudiar mecanización?','La energía y los recursos que requiere','Solo la forma exterior del motor','Que no necesita ninguna fuente de energía')),
 lesson('Una locomotora a prueba',
  'La locomotora Rocket ganó las pruebas de Rainhill de 1829. El concurso buscaba elegir la fuerza motriz para el ferrocarril Liverpool–Manchester.',13,
  ('¿Qué era Rocket?','Una locomotora','Un dinosaurio','Una vasija'),
  ('¿Sobre qué avanza una locomotora?','Sobre vías','Sobre alas','Sobre hojas de árbol'),
  ('¿Para qué se realizaron las pruebas de Rainhill?','Para elegir locomotoras para un ferrocarril','Para pintar una catedral','Para estudiar cuevas paleolíticas'),
  ('¿Cuándo ganó Rocket estas pruebas?','En 1829','En la Grecia clásica','Hace 66 millones de años'),
  ('¿Qué aporta probar una tecnología antes de elegirla?','Permite comparar su funcionamiento','Garantiza perfección eterna','Hace innecesario observar resultados'),
  ('¿Qué afirmación está apoyada por esta evidencia?','Rocket ganó un concurso concreto en 1829','Rocket fue toda la historia del ferrocarril','Todas las locomotoras posteriores eran idénticas')),
 lesson('Objetos que cuentan tecnología',
  'Rocket se conserva en una colección del Science Museum Group. Estudiar una máquina junto a sus registros permite investigar su diseño y su trayectoria.',13,
  ('¿Dónde se puede conservar una máquina histórica?','En un museo','Solo en un cuento','Solo en una nube'),
  ('¿Qué ayuda a conocer su historia?','El objeto y sus registros','Solo su apodo','Una suposición sin pruebas'),
  ('¿Por qué conservar una locomotora?','Para estudiar tecnología del pasado','Para demostrar que todo tren es igual','Para borrar sus modificaciones'),
  ('¿Qué conviene comparar con una máquina?','Documentos sobre su uso y diseño','Únicamente dibujos inventados','El clima de hoy solamente'),
  ('¿Qué evita tratar un objeto como si explicara todo?','Combinar su estudio con otras fuentes','Ignorar dónde se conservó','Suponer que nunca tuvo cambios'),
  ('¿Qué puede investigar un museo con una máquina histórica?','Diseño, materiales y trayectoria','El futuro exacto de todos los trenes','Las ideas privadas de cada pasajero')),
 lesson('La luz llega poco a poco',
  'Londres tuvo iluminación eléctrica en el siglo XIX, pero no se volvió común de inmediato. La adopción de una tecnología puede tardar décadas.',14,
  ('¿Qué iluminaba calles y edificios?','Lámparas eléctricas','Fósiles luminosos','Ovejas brillantes'),
  ('¿Llegó a todas las casas en un mismo día?','No','Sí','Las casas no existían'),
  ('¿Qué diferencia hay entre inventar y adoptar?','Una tecnología puede existir antes de difundirse','Son siempre el mismo momento','Adoptar significa destruir el invento'),
  ('¿Qué pasó con la luz eléctrica en Londres?','Se difundió de forma gradual','Todos la usaron desde el primer instante','Solo existió antes de los dinosaurios'),
  ('¿Qué error evita distinguir invención y difusión?','Suponer acceso universal inmediato','Reconocer diferencias de acceso','Estudiar varias décadas'),
  ('¿Qué pregunta completa la historia de una innovación?','Quién pudo usarla y cuándo','Solo quién recibió más fama','Solo qué aspecto tiene el invento')),
 lesson('Inventar también es colaborar',
  'Las lámparas prácticas de Edison y Swan aparecieron alrededor de 1880. La historia de la iluminación incluye a varias personas y distintas etapas de desarrollo.',14,
  ('¿Cuántas personas aparecen en este ejemplo?','Dos: Edison y Swan','Solo Crono','Ninguna'),
  ('¿Para qué sirve una lámpara?','Para iluminar','Para fosilizar huesos','Para criar ovejas'),
  ('¿Qué muestra mencionar a Edison y a Swan?','Que participaron distintas personas','Que una sola persona hizo todo','Que nunca hubo mejoras'),
  ('¿Alrededor de qué año aparecieron estas lámparas?','1880','1380','Hace 12.000 años'),
  ('¿Por qué conviene evitar el relato de un inventor único?','Puede ocultar contribuciones y etapas','Porque nadie inventa nada','Porque todas las tecnologías son iguales'),
  ('¿Qué enfoque explica mejor el cambio tecnológico?','Examinar personas, mejoras y difusión','Atribuir todo a un momento aislado','Ignorar el uso real de la tecnología')),
]


@dataclass(frozen=True)
class Question:
    id: int
    topic: int
    prompt: str
    options: tuple
    correct: int
    explanation: str = ''
    source: str = ''


def choose_question(topic,band,rng=None,previous=None):
    rng=rng or random
    pool=[band*2,band*2+1]
    if previous is not None and previous%6 in pool:
        pool.remove(previous%6)
    variant=rng.choice(pool)
    prompt,*answers=LESSONS[topic].questions[variant]
    order=list(range(3))
    rng.shuffle(order)
    return Question(topic*6+variant,topic,prompt,tuple(answers[i] for i in order),order.index(0))


UPGRADES=[
 dict(id='vitality',name='Corazón del viajero',cost=3,description='Una unidad adicional de energía máxima.',requires=None),
 dict(id='double_jump',name='Segundo salto',cost=4,description='Un salto adicional en el aire antes de aterrizar.',requires=None),
 dict(id='magnet',name='Imán de ecos',cost=3,description='Recoge ecos y fragmentos a mayor distancia.',requires=None),
 dict(id='dash',name='Impulso afinado',cost=4,description='Un impulso más largo y una recarga más rápida.',requires=None),
 dict(id='shield',name='Escudo de memoria',cost=5,description='Absorbe un golpe. Se recupera en anclas y al reaparecer.',requires=None),
 dict(id='pulse',name='Pulso amplificado',cost=6,description='Duplica el daño de los disparos temporales.',requires=None),
 dict(id='boots',name='Botas del explorador',cost=4,description='Aumenta la velocidad de carrera y el control en el aire.',requires=None),
 dict(id='vitality2',name='Núcleo resistente',cost=6,description='Otra unidad de energía máxima, hasta cinco.',requires='vitality'),
]


def next_level(era,stage):
    return min(14,era*3+stage+1)


assert len(LESSONS)==30 and sum(len(x.questions) for x in LESSONS)==180

EASY_FACTS=(
 'Los pterosaurios eran reptiles que volaban. Su ala era una membrana sostenida por un dedo largo. No eran dinosaurios.',
 'Las aves tienen plumas en las alas. Los pterosaurios tenían membranas. Mirar sus huesos ayuda a distinguirlos.',
 'La arena y el barro pueden cubrir restos. Con muchísimo tiempo, algunos se conservan en las rocas. No todos forman fósiles.',
 'Un diente fósil es parte de un cuerpo. Una pisada fósil es una señal de lo que hizo un animal.',
 'Un gran asteroide chocó con la Tierra hace unos 66 millones de años. Cambió el ambiente y desaparecieron muchas especies.',
 'No desapareció toda la vida. Las aves sobrevivieron: ¡también son dinosaurios!',
 'El mamut lanudo vivía en lugares fríos. Tenía mucho pelo y orejas pequeñas.',
 'Hubo varias especies de mamut. No todos eran iguales al mamut lanudo.',
 'Mucho antes de las ciudades, las personas hacían herramientas de piedra. Sus bordes afilados servían para cortar comida.',
 'El fuego permite cocinar. Cocinar puede ayudar a que el cuerpo aproveche los alimentos.',
 'En Lascaux, una cueva de Francia, las personas pintaron animales hace muchísimo tiempo.',
 'Las pinturas antiguas nos ayudan a conocer el pasado. Protegerlas permite que otras personas puedan estudiarlas.',
 'En la antigua Atenas, algunos hombres adultos podían participar en las decisiones. No todas las personas tenían ese derecho.',
 'Las mujeres, las personas extranjeras residentes y las personas esclavizadas no podían participar en esas decisiones políticas de Atenas.',
 'Los barcos del mar Mediterráneo conectaban ciudades. Llevaban productos de un puerto a otro.',
 'La cerámica se hace con arcilla cocida. Desde Atenas viajaban vasijas pintadas a otros lugares.',
 'En Olimpia había juegos cada cuatro años. También era un lugar de culto, con templos.',
 'En Olimpia quedan restos de templos y de espacios para competir. Cada edificio tenía sus funciones.',
 'En la abadía de Byland, en Inglaterra, se criaban ovejas y se vendía lana para obtener ingresos.',
 'Byland es un ejemplo de Inglaterra. No todas las personas de la Edad Media vivían de la misma manera.',
 'En Inglaterra y Gales había mercados y ferias medievales. Algunos documentos del rey daban permiso para celebrarlos.',
 'Los archivos guardan documentos antiguos. No cuentan todos los detalles: a veces debemos buscar más pistas.',
 'Los edificios góticos tenían arcos que terminaban en punta. Diferentes apoyos ayudaban a sostener su peso.',
 'Las vidrieras dejan pasar luz de colores. Un rosetón es una gran ventana circular decorada.',
 'En 1712, Newcomen desarrolló un motor que ayudaba a sacar agua de las minas. Usaba vapor y su enfriamiento.',
 'El carbón fue muy importante para la industria británica. Las máquinas necesitan energía: no la crean de la nada.',
 'Rocket era una locomotora que iba por vías. Ganó unas pruebas para un ferrocarril en 1829.',
 'Los museos conservan máquinas antiguas. Podemos estudiar el objeto y sus documentos para conocer su historia.',
 'Londres tuvo luz eléctrica en el siglo XIX. No llegó a todas las casas a la vez: se extendió poco a poco.',
 'Edison y Swan hicieron lámparas eléctricas prácticas alrededor de 1880. Varias personas ayudaron a desarrollar esta tecnología.',
)


def fact_for(topic,band):
    return EASY_FACTS[topic] if band==0 else LESSONS[topic].fact
