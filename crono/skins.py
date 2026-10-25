"""Earnable outfits with original details and a sourced historical card."""
SKINS=(
 dict(id='granadero',name='Granadero de los Andes',cost=60,color=(42,70,102),
  history='El Regimiento de Granaderos a Caballo fue creado por José de San Martín en 1812. Participó en la campaña de independencia. Esta apariencia combina rasgos de uniforme de manera ilustrativa; no reproduce un uniforme de museo exacto.',url='https://sanmartiniano.cultura.gob.ar/noticia/cronologia-sanmartiniana/'),
 dict(id='marinero',name='Marinero del Río de la Plata',cost=90,color=(207,213,190),
  history='Guillermo Brown comandó fuerzas navales rioplatenses durante la independencia y la guerra con el Imperio del Brasil de 1825–1828. Tripulantes de distintos orígenes trabajaban en maniobras, artillería y mantenimiento.',url='https://www.argentina.gob.ar/armada/historia-naval/heroes-navales/almirante-guillermo-brown'),
 dict(id='escriba',name='Aprendiz de escriba',cost=120,color=(221,204,158),
  history='Los escribas del antiguo Egipto registraban información de administración, religión y vida cotidiana. Aprendían a leer y escribir distintos sistemas sobre soportes como papiro, piedra y fragmentos de cerámica.',url='https://www.metmuseum.org/essays/egyptian-art'),
 dict(id='ingeniera',name='Ingeniera del ferrocarril',cost=150,color=(100,114,121),
  history='La expansión ferroviaria del siglo XIX requirió trabajadores de vía, señalización, talleres y conducción. Esta ropa de trabajo es una interpretación ficticia que reconoce esos oficios y a quienes hoy los estudian.',url='https://www.railwaymuseum.org.uk/objects-and-stories'),
 dict(id='sanitaria',name='Asistencia humanitaria',cost=180,color=(203,215,193),
  history='La asistencia humanitaria protege la vida y la dignidad de personas afectadas por conflictos. Esta apariencia representa cuidado civil, con un distintivo ficticio de Crono y sin utilizar emblemas protegidos.',url='https://www.icrc.org/es/quienes-somos'),
 dict(id='astronauta',name='Explorador lunar',cost=220,color=(225,224,201),
  history='En julio de 1969 Apolo 11 llevó a Armstrong y Aldrin a la superficie lunar, mientras Collins permanecía en órbita. El traje del juego es una interpretación del equipo de exploración, no una réplica técnica.',url='https://www.nasa.gov/mission/apollo-11/'),
 dict(id='cronista',name='Cronista del tiempo',cost=0,color=(161,130,76),
  history='Un atuendo ficticio para quien reúne los 60 logros. Su Reloj del Cronista añade una unidad de energía máxima y 60 píxeles de alcance de atracción. Puedes desactivar ese beneficio conservando la apariencia.',url=''),
)

SKINS += (
 dict(id='paleontologo',name='Explorador de fósiles',cost=75,color=(181,164,113),history='La paleontología estudia la vida del pasado mediante fósiles y su contexto. Este equipo de campo es moderno: las personas no convivieron con los dinosaurios del Cretácico; Crono llega allí por ficción temporal.',url='https://www.nhm.ac.uk/discover/dino-directory.html'),
 dict(id='glacial',name='Abrigo del deshielo',cost=85,color=(135,115,91),history='Las poblaciones de regiones frías utilizaron recursos locales para protegerse y construir refugios. El atuendo ilustra aislamiento y abrigo; no reproduce una vestimenta única de todas las sociedades paleolíticas.',url='https://www.britishmuseum.org/collection'),
 dict(id='agora',name='Mensajero del ágora',cost=100,color=(210,199,162),history='El ágora era un espacio de encuentro, intercambio y vida cívica de la polis. Esta túnica es una interpretación ilustrativa; la ciudadanía ateniense excluía a mujeres, esclavos y extranjeros residentes.',url='https://www.metmuseum.org/essays/ancient-greece'),
 dict(id='copista',name='Copista medieval',cost=110,color=(111,80,86),history='Los manuscritos se copiaban y decoraban a mano. Bibliotecas y talleres conservaron y transformaron conocimientos. Esta capucha y su cuaderno aluden a esos oficios, sin representar a una persona concreta.',url='https://www.bl.uk/medieval-literature'),
 dict(id='corresponsal',name='Correo entre refugios',cost=125,color=(119,133,108),history='Las cartas conservadas permiten estudiar experiencias de guerra, vínculos y vida cotidiana. Un testimonio aporta una perspectiva y debe contrastarse con otras fuentes. La ropa del juego representa un correo ficticio.',url='https://www.iwm.org.uk/history/first-world-war'),
 dict(id='cientifica',name='Ciencia del presente',cost=135,color=(218,225,216),history='Investigar implica registrar, comparar evidencias y revisar explicaciones. El traje reconoce el trabajo cooperativo en ciencia; su cuaderno y sus gafas son elementos ilustrativos del viaje.',url='https://www.nasa.gov/learning-resources/'),
)

def buy_skin(save,key):
    item=next((s for s in SKINS if s['id']==key),None)
    if not item or key=='cronista' or key in save.data['purchased_skins'] or save.data['coins']<item['cost'] or save.data['practice']:return False
    save.data['coins']-=item['cost'];save.data['purchased_skins'].append(key)
    save.refresh_achievements();save.write();return True

def available(save,key):
    return key=='crono' or save.data['practice'] or key in save.data['purchased_skins'] or key=='cronista' and len(save.data['achievements'])==60

def details(s,player,y):
    """Small silhouette changes keep outfits readable at gameplay size."""
    from .art import rect,line,circle,polygon,CYAN,GOLD
    key=getattr(player,'skin','crono')
    if key=='granadero':
        rect(s,(31,43,61),(30,y-23,22,21),2);rect(s,(27,33,44),(28,y-4,27,4));line(s,(186,57,45),(31,y-18),(27,y-30),4)
        line(s,(217,196,145),(30,y+19),(44,y+32),3);line(s,(217,196,145),(44,y+19),(30,y+32),3)
        for yy in range(20,34,5):circle(s,GOLD,(37,y+yy),1)
    elif key=='marinero':
        rect(s,(223,222,195),(29,y-13,25,9),3);rect(s,(47,67,89),(28,y-5,28,4))
        for yy in (22,28,34):line(s,(49,78,100),(29,y+yy),(44,y+yy),2)
    elif key=='escriba':
        rect(s,(40,48,53),(29,y-8,23,7),2);line(s,GOLD,(28,y-1),(50,y-1),3)
        polygon(s,(204,180,119),[(27,y+18),(47,y+18),(43,y+25),(31,y+25)])
        rect(s,(224,204,148),(22,y+21,6,23),2)
    elif key=='ingeniera':
        polygon(s,(201,155,65),[(28,y-4),(30,y-16),(48,y-16),(53,y-4)])
        line(s,(236,201,111),(27,y-3),(55,y-3),3)
        for xx in (31,42):line(s,(46,69,87),(xx,y+18),(xx,y+36),4)
    elif key=='sanitaria':
        rect(s,(214,222,202),(29,y-11,23,9),2);diamond_points=[(39,y-9),(43,y-6),(39,y-3),(35,y-6)]
        polygon(s,CYAN,diamond_points);rect(s,(70,105,99),(20,y+22,13,18),3)
    elif key=='astronauta':
        circle(s,(221,219,194),(41,y+3),19,4);circle(s,(87,116,126),(41,y+3),16,2)
        rect(s,(216,211,184),(18,y+14,13,29),3);line(s,(174,162,102),(23,y+19),(23,y+37),2)
    elif key=='cronista':
        polygon(s,(99,64,95),[(28,y+16),(20,y+45),(32,y+39),(42,y+17)])
        circle(s,GOLD,(38,y+24),8,2);line(s,CYAN,(38,y+24),(38,y+18),2)
    elif key=='paleontologo':
        rect(s,(162,133,77),(28,y-14,24,13),3);rect(s,(205,177,115),(20,y-3,42,5),2)
        line(s,(104,74,54),(29,y+18),(44,y+39),5);rect(s,(125,95,58),(43,y+25,12,15),2)
    elif key=='glacial':
        circle(s,(212,201,170),(40,y+3),20,6);rect(s,(176,157,123),(27,y+15,25,10),4)
        for xx in (29,45):line(s,(214,205,180),(xx,y+28),(xx,y+44),4)
    elif key=='agora':
        polygon(s,(239,225,184),[(26,y+15),(47,y+17),(53,y+42),(28,y+42)])
        line(s,(143,102,76),(28,y+17),(48,y+36),4);circle(s,GOLD,(31,y+19),4)
        rect(s,(213,196,142),(19,y+22,7,21),2)
    elif key=='copista':
        polygon(s,(88,56,65),[(23,y+9),(28,y-22),(45,y-18),(58,y+11),(46,y+7),(40,y-5),(31,y+7)])
        polygon(s,(87,58,73),[(28,y+15),(18,y+48),(52,y+48),(47,y+16)])
        rect(s,(211,193,142),(18,y+26,14,17),2)
    elif key=='corresponsal':
        rect(s,(81,99,78),(27,y-11,26,12),4);line(s,(51,65,55),(25,y+2),(55,y+2),4)
        line(s,(93,72,51),(30,y+18),(49,y+39),5);rect(s,(137,105,64),(43,y+32,16,16),2)
        rect(s,(222,213,184),(46,y+35,10,6),1)
    elif key=='cientifica':
        for xx in (35,45):circle(s,CYAN,(xx,y+3),5,2)
        line(s,CYAN,(35,y+3),(45,y+3),2);polygon(s,(239,238,220),[(27,y+18),(25,y+45),(38,y+42),(50,y+45),(47,y+18)])
        line(s,(107,129,136),(38,y+23),(38,y+40),2);rect(s,(65,125,125),(20,y+29,11,16),1)
