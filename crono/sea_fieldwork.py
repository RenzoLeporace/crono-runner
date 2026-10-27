"""Different shore decisions; only the middle station is a maritime rift."""
QUESTIONS={
 'tide':(
 ('¿Cuándo terminó el Cretácico?',('Hace unos 66 millones de años','Hace unos 200 años','En 1816')),
 ('¿Cómo se investigan los animales del Cretácico?',('Solo con relatos sin evidencias','Con fósiles y contexto geológico','Solo con documentos navales del siglo XIX')),
 ('¿Qué relación tienen las aves con los dinosaurios?',('Ninguna relación','Las aves aparecieron en 1810','Las aves descienden de dinosaurios'))),
 'canal':(
 ('¿Qué prepara un transporte por el Nilo?',('Agua, carga y una ruta observada','Un motor eléctrico antiguo','Un mapa sin relación con el río')),
 ('¿Qué necesitaban los canales para la agricultura?',('Abandonar la distribución del agua','Organización y mantenimiento del riego','Eliminar los cultivos')),
 ('¿Qué explica la organización de los canales?',('Que no hacía falta cooperación','Que el río era un adorno','La coordinación del agua, los cultivos y el transporte'))),
 'naval':(
 ('¿Qué sostiene al convoy de Brown antes de zarpar?',('Provisiones y coordinación de las tripulaciones','Solo tener una bandera','Navegar sin conocer el estuario')),
 ('¿Qué condicionaba la navegación por el estuario?',('Que todos los barcos tuvieran el mismo calado','Los canales, la profundidad y los bancos de arena','La altura de los pasos cordilleranos')),
 ('¿Qué fuentes permiten estudiar la guerra naval?',('Solo el color de una pintura','Una narración sin fechas','Documentos y testimonios situados en el conflicto'))),
}

SEA_QUESTIONS={
 'canal':(('¿Por qué el Nilo fue clave para el abastecimiento?',('Permitía transportar personas y productos','Egipto no necesitaba cultivar alimentos','Todas las ciudades estaban junto al mar')),
          ('¿Cómo se aprovechaban las crecidas?',('Observando el río y organizando cultivos y canales','Usando locomotoras eléctricas','Evitando el trabajo colectivo')),
          ('¿Qué relaciona el estudio del Nilo?',('Agua, transporte y organización social','Que solo había una actividad económica','Que todos los egipcios tenían los mismos recursos'))),
 'tide':(('¿Qué ocurrió al final del Cretácico?',('Se extinguieron los dinosaurios no avianos y otros grupos','Desapareció toda la vida terrestre','Solo desapareció una especie de pez')),
         ('¿Cómo estudiamos los ambientes del Cretácico?',('Relacionando fósiles, rocas y otras evidencias','Suponiendo que todos los fósiles son iguales','Suponiendo que el clima nunca cambió')),
         ('¿Qué es una extinción masiva?',('Una gran pérdida de biodiversidad en un intervalo geológico','La desaparición de toda forma de vida','El desplazamiento de una sola especie'))),
 'naval':(('¿Por qué era importante el abastecimiento de una escuadra?',('Sostenía el viaje y el cuidado de las tripulaciones','Solo servía para decorar los barcos','Evitaba organizar las provisiones')),
          ('¿Contra quién combatió Brown en 1826–1827?',('Contra fuerzas del Imperio del Brasil','Contra una escuadra realista de la independencia','Contra una escuadra de la Segunda Guerra Mundial')),
          ('¿Por qué importaban los canales y bancos del Río de la Plata?',('Condicionaban el calado, las rutas y las decisiones navales','Permitían navegar sin conocer el río','Hacían innecesaria la coordinación')))
}

def shore_question(kind,index):return QUESTIONS[kind][index]
