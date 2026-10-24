# Verificación · beta educativa 0.6

24 de octubre de 2026. Windows 11, Python 3.12, pygame-ce 2.5.7.

## Pruebas automáticas

**89 pruebas:** 23 de juego, 19 educativas, 19 del editor, 15 de la expansión y 13 del rework.

- Las 27 rutas tienen geometrías distintas, más de 12.000 píxeles, tres zonas, 48 ecos, archivos y fragmentos en ramales.
- Saltos y descensos con controles y colisiones reales verifican conexiones obligatorias, fragmentos y archivos, sin mejoras ni dependencia de plataformas móviles. No se simula una partida humana continua.
- Progresión de 24 mapas principales con Egipto entre Deshielo y Grecia; final en actualidad. Los tres mapas argentinos mantienen progreso independiente.
- Nueve combates completos simulados en mínima sin mejoras ni muertes. Egipto: 35,2 segundos en la estrategia del test. Media y alta se comprueban por velocidad, resistencia, salvas, marcas y ventanas; no se afirma una campaña automatizada en alta.
- Todas las anclas en mínima, cuatro en media y dos en máxima, con última antes del jefe. Las deshabilitadas no se activan ni aparecen; cambiar edad o cargar una retirada vuelve a una anterior válida.
- Nueve familias con siluetas distintas; humanoides con colisiones más altas sobre el mismo suelo, pisotón y variantes protegidas señalizadas.
- 324 preguntas en 54 archivos y tres edades: sorteo, mezcla, recompensa única y errores sin castigo.
- Editor docente, validación, escritura atómica, respaldos, búsqueda, Unicode, selección, textos largos y protección de cambios. El selector incluye los 27 mapas en orden cronológico.
- Bancos antiguos ampliados sin reemplazar modificaciones o preguntas propias; las preguntas nuevas egipcias usan IDs independientes.
- Partidas 0.5 conservan mapas, anclas habilitadas, fragmentos, daño a enemigos, mejoras y aprendizaje. Formato 4 con respaldo del archivo anterior. Las partidas 0.4 conservan la migración por geometría renovada.
- Las visitas a Luján, Itatí y Moisés pausan y regresan al juego sin recompensas duplicadas. Los hitos culturales se apoyan en superficies transitables fuera de arenas.
- Regresión del autoguardado: completar un mapa no vuelve a capturar el mundo terminado ni retrocede el mapa de continuación.

## Revisión visual

Capturas actuales: `capturas/rework-0.6` contiene 63 vistas de los tres distritos de los 21 mapas anteriores; `capturas/argentina-0.6` contiene nueve distritos, introducciones, guías y adversarios; `capturas/novedades-0.6`, Egipto, humanoides y patrimonio; `capturas/educativa-0.6`, los 27 mapas, nueve jefes y pantallas docentes.

Se inspeccionaron los montajes y vistas individuales de arquitectura, materiales, hitos, modelos, museo cultural y editor. El arte se genera por código a doble resolución donde corresponde. Las superficies transitables y los elementos del fondo mantienen colisiones separadas.

Mediciones orientativas fuera de pantalla a 1280 × 720: medianas de 3,3–5,4 ms en los 21 mapas renovados; p95 máximo observado 6,6 ms. Argentina: mediana 5,2 ms y p95 6,5 ms. Egipto: mediana 4,1 ms y p95 5,2 ms. Son mediciones de esta máquina, no garantías de FPS en otros equipos.

## Distribución y auditoría

El ejecutable PyInstaller se distribuye con `_internal`. El empaquetado comprueba dieciséis escenas del ejecutable: menú, épocas, configuración, banco, editor egipcio, galería argentina, pregunta egipcia, dos jefes, plano, Tucumán, dos mapas egipcios y las tres fichas culturales. Comprueba salida correcta, PNG generado, integridad del ZIP y ausencia de partidas o bancos personalizados.

El informe independiente solicitado está en [docs/AUDITORIA-0.6.md](docs/AUDITORIA-0.6.md). El subagente ejecutó las pruebas de su revisión, identificó dos defectos y comprobó sus correcciones. Añadió revisión específica del último cambio de anclas. El agente principal realiza la verificación del ejecutable después de compilar.

## Límites

No se realizó una partida humana completa de los 27 mapas ni sesiones con alumnos o docentes. El equilibrio de media y alta, la duración entre anclas, la accesibilidad y la eficacia educativa requieren esas pruebas. No se verificó un mando físico. Fuentes en `FUENTES.md`; arquitectura, uniformes y adversarios son interpretaciones de ficción. Moisés se presenta como tradición bíblica; Luján e Itatí, como patrimonio religioso y cultural.
