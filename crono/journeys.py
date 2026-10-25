"""Stable IDs for historical excursions, rescues and their actual contexts."""
COMBAT_ERAS=(7,7,7,2,4,5,5,2,6)
DATES=('20 de noviembre de 1845','Enero de 1817','1825–1828','Alejandría · época helenística','Ferrocarril · siglo XIX','Europa · siglo XX','Malvinas · 1982','Pompeya · año 79','Apolo 11 · julio de 1969')
BOSSES=('El bloqueo del Paraná','El guardián del paso','La fragata del tiempo','La sombra del faro','La locomotora sin rumbo','La sirena del último refugio','La tormenta del Atlántico','El frente de ceniza','El ruido de la órbita')
VARIANTS=('battery','andes','naval','lighthouse','train','hospital','malvinas','volcano','lunar')
RESCUES={
 'san_martin':dict(level=22,bonus=28,name='José de San Martín',date='Cuyo · 1816',
   text='El reloj aisló un eco de San Martín en su campamento de Cuyo. Este rescate es una misión de ficción: no representa un secuestro histórico en Tucumán. La preparación del Ejército de los Andes tuvo lugar en Mendoza antes del cruce de 1817.'),
 'brown':dict(level=21,bonus=29,name='Guillermo Brown',date='Eco naval · 1825–1828',
   text='Una grieta enlaza el puerto de 1810 con un eco posterior de Brown. Libera su señal para explorar la guerra naval contra el Imperio del Brasil. El encuentro y el rescate pertenecen a la ficción del reloj.'),
 'cartographer':dict(level=7,bonus=30,name='La cartógrafa',date='Personaje ficticio · Mediterráneo',
   text='Una viajera de las rutas marítimas quedó atrapada en una rama del reloj. Su mapa abre un viaje a la Alejandría helenística, un contexto posterior al Ágora de Atenas de la campaña.'),
 'engineer':dict(level=13,bonus=31,name='La técnica ferroviaria',date='Personaje ficticio · siglo XIX',
   text='La técnica intenta restablecer las señales del ferrocarril. Recupera su equipo en la pasarela elevada y te mostrará el acceso al expreso nocturno.'),
 'medic':dict(level=16,bonus=32,name='La médica del refugio',date='Personaje ficticio · población civil',
   text='La médica necesita una ruta segura para evacuar heridos. Su misión se centra en proteger vidas y abre un hospital de campaña ficticio inspirado en la atención durante la guerra.'),
}
RIFTS={23:33,11:34,20:35}

def combat_era(index,stage=0):return COMBAT_ERAS[index*3+stage-27] if index>=9 else index
def date_for(level):
    if level>=27:return DATES[level-27]
    from .levels import ERAS
    return ERAS[level//3].date

def rescue_for(level):return next(((key,value) for key,value in RESCUES.items() if value['level']==level),None)
