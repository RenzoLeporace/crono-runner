"""Append-only maps: Verdun (46), armistice (47), Stalingrad (48), Ypres (49)."""
VERDUN='https://www.defense.gouv.fr/chemins-memoire/histoire-memoires/ressources-historiques/premiere-guerre-mondiale/combattre-combats/fronts-32'
ARMISTICE='https://www.nam.ac.uk/explore/1918-victory'
STALINGRAD='https://encyclopedia.ushmm.org/content/en/article/the-soviet-union-and-the-eastern-front'
YPRES='https://www.theworldwar.org/learn/about-wwi/spotlight-first-usage-poison-gas'
RESPIRATOR='https://www.awm.gov.au/3dtreasures/items/small-box-respirator/'
BLITZ='https://www.londonmuseum.org.uk/collections/london-stories/londons-blitz-a-city-at-war/'
HOME_FRONT='https://www.rafmuseum.org.uk/research/online-exhibitions/history-of-the-battle-of-britain/the-home-front/'
BERLIN='https://www.archives.gov/milestone-documents/surrender-of-germany'

def topic(title,fact,*questions):
    assert len(questions)==6
    return (title,fact,*questions)

WAR_MAPS=(
 dict(name='Verdún · sostener la ruta de ayuda',focus='Francia, 1916: desgaste, fortificaciones y abastecimiento.',landmark='verdun',combat=5,date='Verdún · 1916',source='Ministerio de las Fuerzas Armadas de Francia · 1916',url=VERDUN,
 topics=(topic('Verdún, una batalla de desgaste','La batalla de Verdún enfrentó a los ejércitos alemán y francés en 1916. Comenzó el 21 de febrero y se prolongó durante meses. Los fuertes de Douaumont y Vaux formaron parte de los combates.',
 ('¿En qué país se encuentra Verdún?','Francia','Egipto','Brasil'),('¿En qué año ocurrió esta batalla?','1916','1939','1989'),('¿Qué ejércitos se enfrentaron en Verdún?','El alemán y el francés','El romano y el griego','El brasileño y el argentino'),('¿Cuándo comenzó la batalla de Verdún?','El 21 de febrero de 1916','El 9 de julio de 1816','El 20 de julio de 1969'),('¿Qué fortificaciones formaron parte de los combates?','Douaumont y Vaux','El Cabildo y la Casa de Tucumán','Las pirámides de Guiza'),('¿Qué significa describir Verdún como una batalla de desgaste?','Que meses de combate agotaron personas y recursos','Que fue un encuentro deportivo','Que no requirió abastecimiento')),
 topic('La Somme y el cambio técnico','La ofensiva de la Somme comenzó el 1 de julio de 1916. En septiembre se emplearon por primera vez carros de combate en esta batalla. El nuevo equipo no eliminó las dificultades de la guerra de trincheras.',
 ('¿Qué batalla comenzó en julio de 1916?','La Somme','Stalingrado','Obligado'),('¿Qué vehículo nuevo se empleó allí en septiembre?','El carro de combate','El módulo lunar','El avión a reacción'),('¿En qué guerra ocurrió la Somme?','La Primera Guerra Mundial','La Segunda Guerra Mundial','La Guerra Fría'),('¿Qué fecha corresponde al inicio de la Somme?','1 de julio de 1916','11 de noviembre de 1918','26 de abril de 1986'),('¿Los primeros carros acabaron inmediatamente con todas las trincheras?','No; persistieron grandes dificultades','Sí; no hubo más combate','Sí; se terminó la guerra ese día'),('¿Qué batallas coincidieron en 1916?','Verdún y la Somme','Stalingrado y el Blitz','Obligado y las Termópilas'))),
 curiosity=('verdun_fort','Douaumont y Vaux','Los fuertes de Douaumont y Vaux permiten localizar lugares concretos de la batalla de Verdún.'),
 mechanic=('Abastecer entre bombardeos','supply','Recupera tres cajas y entrégalas al puesto de ayuda; busca refugios ante los avisos.',('Identificar las cargas','Señalar la ruta protegida','Organizar la entrega'),'Abastecimiento y protección en una ruta ficticia situada en el contexto de Verdún.')),
 dict(name='1918 · llevar la noticia del armisticio',focus='Compiègne y frente occidental: cese del fuego, asistencia y posguerra.',landmark='armistice',combat=5,date='Francia · 11 de noviembre de 1918',source='National Army Museum · 1918',url=ARMISTICE,
 topics=(topic('La hora del cese del fuego','El armisticio con Alemania se firmó en un vagón de ferrocarril en Compiègne, Francia, el 11 de noviembre de 1918. El cese del fuego entró en vigor a las once de la mañana en el frente occidental.',
 ('¿Dónde se firmó el armisticio?','En un vagón de ferrocarril','En un módulo lunar','En una pirámide'),('¿En qué año se firmó?','1918','1945','1810'),('¿En qué país está Compiègne?','Francia','Argentina','Japón'),('¿Cuándo entró en vigor el cese del fuego?','A las once de la mañana del 11 de noviembre','El 1 de enero a medianoche','El 20 de julio de 1969'),('¿Con qué país firmaron el armisticio los aliados?','Alemania','El Imperio romano','El Egipto faraónico'),('¿Qué se detuvo con el armisticio en el frente occidental?','Los combates','El paso del tiempo','Todas las tareas de asistencia')),
 topic('El armisticio no resolvió todo','El fin de los combates no borró las pérdidas, heridas y destrucción. El Tratado de Versalles se firmó en junio de 1919. El armisticio de 1918 y el tratado de paz fueron documentos distintos.',
 ('¿Desaparecieron las heridas al anunciarse el armisticio?','No; continuaron necesidades de atención','Sí; inmediatamente','No hubo personas heridas'),('¿Qué tratado se firmó después de la guerra?','Versalles','El Acta de Tucumán','La Carta de Mayo'),('¿En qué año se firmó Versalles?','1919','1914','1961'),('¿Armisticio y tratado de paz son el mismo documento?','No; tienen funciones y fechas distintas','Sí; son dos nombres idénticos','Sí; ambos se firmaron en 1816'),('¿Qué tarea continuó tras el cese del fuego?','Atender heridas y reconstruir comunidades','Preparar la misión Apolo 11','Construir pirámides faraónicas'),('¿Qué ocurrió primero?','El armisticio de 1918','El tratado de 1919','La apertura del muro de 1989'))),
 curiosity=('armistice_carriage','El vagón de Compiègne','El armisticio se firmó en un vagón de ferrocarril; su firma y la entrada en vigor no ocurrieron a la misma hora.'),
 mechanic=('Una ruta para la asistencia','escort','Prepara el puesto de ayuda y acompaña a quienes necesitan atención.',('Confirmar el mensaje fechado','Preparar la asistencia','Acompañar el traslado'),'La noticia no suprimió las necesidades de asistencia y reconstrucción.')),
 dict(name='Stalingrado · sobrevivir al invierno',focus='Frente oriental, 1942–1943: cerco, abastecimiento y coste humano.',landmark='stalingrad',combat=5,date='Stalingrado · 1942–1943',source='United States Holocaust Memorial Museum · Frente oriental',url=STALINGRAD,
 topics=(topic('La ciudad junto al Volga','La batalla de Stalingrado se desarrolló en 1942–1943 en el frente oriental de la Segunda Guerra Mundial. La ciudad, hoy Volgogrado, está junto al río Volga. Los combates causaron enorme destrucción y sufrimiento.',
 ('¿Junto a qué río está Stalingrado?','El Volga','El Paraná','El Nilo'),('¿Cómo se llama hoy esa ciudad?','Volgogrado','Alejandría','Maguncia'),('¿A qué guerra corresponde Stalingrado?','A la Segunda Guerra Mundial','A la Primera Guerra Mundial','A las guerras napoleónicas'),('¿En qué período ocurrió la batalla?','1942–1943','1914–1918','1982–1983'),('¿En qué frente se encontraba?','En el frente oriental','En el Río de la Plata','En el frente lunar'),('¿Qué consecuencia tuvieron los combates en la ciudad?','Destrucción y sufrimiento de soldados y civiles','La desaparición de toda necesidad de refugios','La construcción del muro de Berlín')),
 topic('El cerco y el abastecimiento','La contraofensiva soviética de noviembre de 1942 cercó fuerzas alemanas y aliadas en Stalingrado. La derrota alemana se completó en febrero de 1943. El frío, la falta de suministros y los combates agravaron las condiciones humanas.',
 ('¿Qué dificultó sobrevivir durante el cerco?','El frío y la falta de suministros','La gravedad lunar','Las crecidas del Nilo'),('¿Cuándo terminó la derrota alemana en Stalingrado?','En febrero de 1943','En julio de 1969','En mayo de 1810'),('¿Qué fuerza lanzó la contraofensiva de noviembre de 1942?','El ejército soviético','Las milicias de Güemes','La escuadra de Brown'),('¿Qué significa que un ejército quede cercado?','Que sus rutas terrestres quedan rodeadas por fuerzas enemigas','Que recibe provisiones sin límite','Que desaparece toda oposición'),('¿Qué elemento seguía siendo esencial incluso con armamento?','Alimentos, refugio y abrigo','Un reloj sin fecha','Una antena lunar'),('¿Qué efecto tuvo Stalingrado en el frente oriental?','Contribuyó al cambio de iniciativa a favor soviético','Terminó toda guerra en 1942','Comenzó la Primera Guerra Mundial'))),
 curiosity=('volga_supply','El Volga y los suministros','La ubicación junto al Volga ayuda a comprender la importancia de las rutas y los suministros de la ciudad.'),
 mechanic=('Provisiones entre las ruinas','supply','Busca el abrigo, recupérate en refugios y entrega tres cajas de suministros.',('Preparar la posta','Comprobar la ruta','Entregar los víveres'),'Los recursos y el clima condicionaron las posibilidades de sobrevivir.')),
 dict(name='Ypres · la amenaza de los gases',focus='Bélgica, 1915: guerra química y protección de las personas.',landmark='ypres',combat=5,date='Ypres · abril de 1915',source='National WWI Museum · Uso de gases',url=YPRES,
 topics=(topic('Una nueva amenaza en Ypres','El 22 de abril de 1915, fuerzas alemanas liberaron cloro a gran escala cerca de Ypres, Bélgica. El gas causó graves daños a quienes estaban expuestos. Los ataques químicos se convirtieron en una amenaza en las trincheras.',
 ('¿En qué país se encuentra Ypres?','Bélgica','Brasil','Egipto'),('¿Qué sustancia se liberó allí en abril de 1915?','Cloro','Oxígeno lunar','Vapor de agua potable'),('¿En qué guerra ocurrió este ataque?','La Primera Guerra Mundial','La Guerra Fría','La guerra de Malvinas'),('¿Qué fecha corresponde al gran ataque de cloro en Ypres?','22 de abril de 1915','9 de julio de 1816','11 de noviembre de 1989'),('¿Por qué era peligrosa una nube de cloro?','Porque dañaba la respiración y podía causar la muerte','Porque daba oxígeno puro','Porque curaba heridas'),('¿De dónde procedía el gas liberado en este ataque?','De cilindros preparados por las tropas','De un volcán belga','De una nave espacial')),
 topic('Protección frente a la guerra química','La protección respiratoria cambió durante la Primera Guerra Mundial: hubo recursos improvisados en 1915 y el ejército británico introdujo el respirador de caja pequeña en 1916. Los modelos no fueron todos iguales ni eliminaron el peligro. La asistencia a las personas expuestas siguió siendo esencial.',
 ('¿Para qué servían los respiradores de guerra?','Para reducir la exposición a gases','Para fabricar gas','Para volar sobre trincheras'),('¿Una máscara hacía desaparecer el peligro?','No; la protección tenía límites','Sí; cualquier máscara anulaba todo riesgo','Sí; no necesitaba ajustarse'),('¿Qué parte del cuerpo buscaban proteger los respiradores?','Las vías respiratorias','Las ruedas de un tanque','Las velas de un barco'),('¿Qué motivó mejorar la protección respiratoria?','Los ataques químicos','El comercio de ánforas','La imprenta de Gutenberg'),('¿Por qué era importante el ajuste de una máscara?','Porque las entradas de aire sin filtrar reducían su protección','Porque cambiaba la fecha del ataque','Porque eliminaba el viento'),('¿Qué necesitaban las personas expuestas además de protección?','Asistencia y traslado fuera del peligro','Más exposición al gas','Continuar sin ayuda'))),
 curiosity=('gas_respirator','Los primeros respiradores','La protección respiratoria cambió durante la guerra; las máscaras no eliminaron el peligro químico.'),
 mechanic=('Avisar y evacuar','siren','Consigue una máscara, evita nubes y acompaña al grupo por las zonas de resguardo.',('Reconocer el aviso','Preparar la protección','Acompañar la evacuación'),'La exposición y la máscara son una simplificación de juego, no instrucciones de seguridad reales.')),
)

def apply_existing(Stage,Lesson,stages,lessons,sources):
    stages[15]=Stage('1914 · el frente y sus cartas','Inicio de la Primera Guerra Mundial, trincheras y vida civil.','trenches')
    stages[16]=Stage('Londres · protegerse del Blitz','Bombardeos de 1940–1941, refugios y población civil.','shelter')
    stages[17]=Stage('1945 · de Berlín a la reconstrucción','El final de la guerra en Europa, cooperación y derechos humanos.','peace')
    sources.append(('National Army Museum · Paz y conmemoración','https://www.nam.ac.uk/explore/peace-and-commemoration'))
    item=lessons[95]
    lessons[95]=Lesson(item.title,item.fact,len(sources)-1,item.questions)
    sources.append(('Australian War Memorial · Respiradores de la Primera Guerra',RESPIRATOR))
    item=lessons[99]
    lessons[99]=Lesson(item.title,item.fact,len(sources)-1,item.questions)
    rows=(
      (32,'Londres durante el Blitz',
       'El 7 de septiembre de 1940 comenzó una intensa campaña de bombardeos alemanes sobre Londres. El Blitz afectó también a otras ciudades británicas y se prolongó hasta 1941. Las viviendas, el transporte y la vida de la población civil sufrieron sus efectos.',
       'London Museum · El Blitz',BLITZ,
       ('¿Qué ciudad británica sufrió el Blitz?','Londres','París','Roma'),
       ('¿Los bombardeos afectaron también a personas civiles?','Sí; afectaron viviendas y vidas cotidianas','No; solo había soldados','No; las ciudades estaban vacías'),
       ('¿En qué guerra ocurrió el Blitz?','En la Segunda Guerra Mundial','En la Primera Guerra Mundial','En la Guerra de los Farrapos'),
       ('¿Cuándo comenzó la campaña intensa contra Londres?','El 7 de septiembre de 1940','El 21 de febrero de 1916','El 11 de noviembre de 1918'),
       ('¿El Blitz afectó únicamente a Londres?','No; también a otras ciudades británicas','Sí; ninguna otra ciudad fue atacada','No; se limitó a ciudades de América'),
       ('¿Qué muestra la destrucción de viviendas durante el Blitz?','Que la guerra alcanzó la vida civil además de los frentes','Que solo afectó a los ejércitos','Que el transporte siguió siempre sin alteraciones')),
      (33,'Sirenas, refugios y ayuda civil',
       'Durante los ataques aéreos, las sirenas advertían del peligro. En Londres se utilizaron distintos refugios, incluidas estaciones del metro y estructuras Anderson. Bomberos, servicios de emergencia y comunidades participaron en la protección y asistencia.',
       'RAF Museum · El frente interno',HOME_FRONT,
       ('¿Para qué sonaban las sirenas de alarma aérea?','Para avisar del peligro','Para anunciar un mercado','Para iniciar un partido'),
       ('¿Qué lugar se utilizó también como refugio en Londres?','Estaciones del metro','La superficie de la Luna','Templos de Olimpia'),
       ('¿Cómo se llamaba un tipo de refugio doméstico usado en Gran Bretaña?','Anderson','Eagle','Rocket'),
       ('¿Qué servicio combatía los incendios provocados por los bombardeos?','Los bomberos','Los escribas del Nilo','Los arrieros de los Andes'),
       ('¿Hubo un único tipo de refugio durante el Blitz?','No; se utilizaron varios tipos de resguardo','Sí; toda la población usó el mismo edificio','No hubo refugios'),
       ('¿Qué relación hubo entre ataques aéreos y organización civil?','Se necesitaron avisos, refugios y servicios de asistencia','Los ataques volvieron innecesarios los servicios públicos','Solo los pilotos tuvieron tareas que realizar')),
      (34,'Berlín y el final de la guerra en Europa',
       'En la primavera de 1945 las fuerzas soviéticas tomaron Berlín. La rendición militar alemana se firmó en Reims el 7 de mayo y en Berlín el 8 de mayo; dispuso el cese de las operaciones el 8 de mayo. Esto marcó el final de la guerra en Europa, no el de todos los combates en el mundo.',
       'National Archives · Rendición de Alemania',BERLIN,
       ('¿Qué ciudad era la capital alemana tomada en 1945?','Berlín','Londres','Tucumán'),
       ('¿Qué fuerzas tomaron Berlín al final de la guerra?','Las fuerzas soviéticas','Las milicias de Güemes','La escuadra de Brown'),
       ('¿En qué año se rindió Alemania en la Segunda Guerra Mundial?','1945','1918','1989'),
       ('¿Qué ciudad fue sede de la firma del 7 de mayo de 1945?','Reims','Compiègne','Versalles'),
       ('¿Qué dispuso la rendición militar alemana?','El cese de las operaciones de sus fuerzas','La continuación de todos los ataques','La construcción del muro de Berlín'),
       ('¿Por qué se distingue el final europeo del final mundial de la guerra?','Porque en mayo de 1945 aún continuaba la guerra contra Japón','Porque la guerra mundial terminó en 1918','Porque Berlín estaba fuera de Europa')),
    )
    for index,title,fact,label,url,*questions in rows:
        sources.append((label,url))
        lessons[index]=Lesson(title,fact,len(sources)-1,tuple(questions))
