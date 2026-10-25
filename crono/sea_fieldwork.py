"""Different shore decisions; only the middle station is a maritime rift."""
QUESTIONS={
 'tide':(
 ('Antes de navegar, ¿qué necesita conocer Crono?',('Observar las mareas y preparar el equipo','Suponer que el agua está siempre quieta','Buscar personas del Cretácico')),
 ('El agua está subiendo. ¿Qué decisión abre la travesía?',('Cerrar todas las rutas sin observar','Aprovechar la pleamar y entrar con el esquife','Caminar con el barco por las plataformas')),
 ('Al volver, ¿qué debe registrar para comparar las mareas?',('Solo el color del esquife','Una fecha inventada','Los cambios observados y las condiciones del recorrido'))),
 'canal':(
 ('¿Qué prepara un transporte por el Nilo?',('Agua, carga y una ruta observada','Un motor eléctrico antiguo','Un mapa sin relación con el río')),
 ('¿Cómo continúa el viaje fluvial?',('Transportando el barco por los tejados','Entrando en el canal desde la grieta señalada','Ignorando el nivel del agua')),
 ('¿Qué explica la organización de los canales?',('Que no hacía falta cooperación','Que el río era un adorno','La coordinación del agua, los cultivos y el transporte'))),
 'naval':(
 ('¿Qué sostiene al convoy de Brown antes de zarpar?',('Provisiones y coordinación de las tripulaciones','Solo tener una bandera','Navegar sin conocer el estuario')),
 ('¿Qué permite iniciar una ruta segura por el estuario?',('Suponer que todos los barcos tienen el mismo calado','Reconocer el canal y entrar por la grieta marítima','Pasar por encima de las plataformas terrestres')),
 ('¿Qué debe contrastarse después del viaje?',('Solo el número de disparos del juego','Una historia sin fechas','Las decisiones de navegación con fuentes del conflicto'))),
}

def shore_question(kind,index):return QUESTIONS[kind][index]
