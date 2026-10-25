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
