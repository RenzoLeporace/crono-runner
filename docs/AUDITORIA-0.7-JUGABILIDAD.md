# Auditoría independiente de fuentes 0.7 · juego, arte e interfaz

24 de octubre de 2026. Revisión del subagente que auditó también la beta 0.6, retomado expresamente por el usuario. No se modificó código de producción; se generaron pruebas, capturas e informes de auditoría.

## Dictamen

**No encuentro bloqueadores reproducibles pendientes en el código fuente revisado para generar candidatos de Windows y Android y comenzar su validación.** La última suite independiente ejecutó **109 pruebas, todas correctas**, en 29,3 segundos, incluyendo HTTP real en localhost con los permisos necesarios.

Este dictamen permite pasar a compilación y pruebas de artefactos; no certifica todavía el EXE distribuido, una instalación APK ni una campaña humana completa. La revisión de puente nativo, intercambio docente y LAN tiene además un segundo auditor independiente.

## Evidencia realmente obtenida

- Construcción y metadatos de los 36 mapas: 24 principales, cuatro argentinos, cinco bonus y tres grietas. Se conservan los IDs anteriores y el orden principal incluye Egipto entre Deshielo y Grecia.
- Verificación de conexiones mediante física real y, en rondas adicionales, 108 interacciones E con los tres puestos de los 36 mapas. Las posiciones se controlan para comprobar cada sistema; no se simula así una partida humana continua.
- Aplicaciones físicas de las 36 actividades: objetos, balizas, elevadores, pasarelas, acompañamiento, refugios y conducción. Los objetivos se completan en pruebas aisladas y conservan progreso al guardar, cargar y morir.
- Cinco rescates: guardianes vivos bloquean la liberación; después se abre el bonus y la recompensa no se duplica.
- Tres grietas: regreso a la posición exacta del origen, conservación de salud, fragmentos y enemigos derrotados, y premio único de 40 monedas. También se cubre continuar después de cerrar la pantalla de finalización.
- Capturas nuevas de 36 mapas, los nueve jefes adicionales y menús móviles. Se inspeccionaron especialmente modelos romanos y de 1982, arquitectura argentina, barcos, guardarropa, selector 36, accesibilidad, fichas a 25 px, herramientas docentes y HUD de combate.
- Banco de 1296 registros validado por la suite: 72 temas, tres perfiles y seis preguntas por combinación; IDs únicos y opciones válidas. Se revisó además la reescritura de 108 preguntas de los 18 temas de excursiones, con formulaciones específicas de contenido.
- Nueve combates originales completos simulados en mínima sin mejoras ni muertes; reacción a daño confirmado y derrota comprobada en los 18 jefes. Los nuevos encuentros tienen nueve patrones distintos, no solo nombres y dibujos diferentes.
- Pruebas adicionales del logro de duelo: morir antes de la primera activación no impide ganarlo; morir después sí lo impide, y guardar/cargar conserva esa condición.
- La suite final incluye aislamiento de perfiles, práctica sin premios reales, mejores puntuaciones por mapa, banco docente, PIN, CSV con reflexiones, multitouch y regresiones del puente de archivos nativo mediante sustitutos controlados.

La ejecución web offline mostrada por el agente principal arranca en su captura de WASM y los menús resultan legibles. Revisé esa evidencia, pero no la confundo con haber instalado o jugado un APK real.

## Defectos encontrados y corregidos durante las rondas

Los problemas se comunicaron con reproducciones y fueron corregidos por el agente principal. Los más relevantes fueron:

1. **Aislamiento de perfiles:** al cambiar de alumno y cerrar, el mundo anterior podía guardarse en el perfil nuevo. Ahora se guarda primero la sesión anterior y se reinicia el mundo y su contexto al cambiar de perfil.
2. **Práctica y premios únicos:** practicar podía consumir ecos, curiosidades y rescates del progreso real sin conceder sus monedas. La práctica ya mantiene separados los resultados y recompensas reales.
3. **Puestos imposibles de usar:** algunos mapas elegían dos veces la misma ubicación; otros superponían una actividad con un rescate o una grieta que interceptaba E. Los 108 encuentros actuales abren la actividad prevista.
4. **Vehículos:** entrar con un impulso activo podía dejar invulnerabilidad permanente; la orientación del cañón y los temporizadores tampoco se actualizaban correctamente. Se normalizan y la muerte desmonta en un ancla segura.
5. **Guardados parciales inválidos:** valores interiores inesperados en bonus y puntuaciones podían provocar excepciones. Se reforzó la validación y recuperación.
6. **Señales visuales:** humanoides protegidos sin indicador, uniformes heredados de un contexto equivocado, voladores reubicados dentro del suelo y glifos ausentes en controles táctiles. Ahora hay marcadores comunes, variantes históricas y flechas dibujadas.
7. **Mecánicas físicas:** pasarelas dentro de superficies originales, atlas mostrando plataformas inactivas e impactos de campo sin eventos de daño. Se corrigieron posición, visibilidad y reacción audiovisual.
8. **Lectura y HUD:** fichas que ignoraban tamaño 25, desplazamiento heredado entre fichas y progreso de actividad superpuesto a mensajes del jefe. Las capturas finales muestran el contenido separado y la lectura desplazable.
9. **Herramienta docente:** salir por teletransporte de una arena activa devolvía al docente automáticamente al combate. Verifiqué que ahora permanece fuera de la arena y el bloqueo queda desactivado solo en práctica.
10. **Regresión por adaptación móvil:** faltaba importar threading al abrir una sala en escritorio. La suite HTTP real pasó después de corregirlo.

Los registros y reproducciones de trabajo se conservan localmente en `.test-tmp/audit-07-original`, incluidas las rondas intermedias fallidas. Esas ejecuciones no deben presentarse como fallos vigentes después de las correcciones verificadas.

## Valoración visual y educativa

Argentina tiene hitos reconocibles, fachadas con variación y materiales propios. Los escenarios anteriores ya distinguen extinción, cuevas, puertos, mercados, instalaciones industriales y ciudades actuales. Los bonus y grietas añaden paisajes y objetivos identificables. Los modelos de Pompeya y Malvinas se distinguen de sus antiguas bases griegas y de 1914.

Las referencias a Luján, Itatí y Moisés conservan contexto y carácter cultural. El retorno democrático se diferencia de las violencias anteriores; las misiones y rescates ficticios se señalan como tales. La auditoría comprueba ese encuadre en el juego, no una revisión académica independiente de cada afirmación de todas las fuentes.

Las actividades ya exigen una aplicación física además de sus paneles. Las familias reutilizan sistemas compartidos; no se afirma que existan 36 motores mecánicos independientes. El objetivo restante permanece visible para explicar que activar los tres puestos no basta por sí solo.

Las preguntas específicas de excursiones mejoran los primeros borradores basados en prefijos. Las tareas de fuentes, imágenes, razonamiento y cronología amplían la actividad; su presencia y validación formal no demuestran por sí solas eficacia educativa.

## Límites y trabajo posterior necesario

- **Equilibrio:** los controladores genéricos no resolvieron con la misma estrategia todos los nueve encuentros nuevos. Con la política anterior se ganaron seis; Obligado, Faro y Malvinas necesitan una estrategia distinta. Esto no demuestra imposibilidad, pero impide afirmar que los 18 jefes están calibrados para principiantes o que todos se derrotaron sin mejoras y sin muertes. Deben observarse jugadores de 6–9,10–14 y 15+.
- **Partida humana:** no se recorrieron manualmente los 36 mapas de principio a fin. Las pruebas de rutas, combate, interacción y persistencia se preparan por separado y no sustituyen esa sesión.
- **Escuelas:** todavía conviene una revisión curricular docente, observación de accesibilidad y una sesión piloto. Puntuación, rapidez y aciertos deben acompañarse de conversación y explicación; no equivalen automáticamente a aprendizaje ni constituyen evaluación inviolable.
- **Android:** falta verificar APK instalado, reinicio real del proceso, escritura privada, selector nativo de archivos, teclado, orientación, gestos simultáneos, pausado del sistema, LAN y rendimiento en dispositivo. Un puente probado con sustitutos y una captura de WASM no certifican esos aspectos.
- **Distribución:** después de compilar deben probarse el EXE y APK exactos que se entregarán, comprobar dependencias, integridad y exclusión de partidas y bancos personalizados.

Con esas limitaciones explícitas, la fuente revisada está en condiciones de pasar a generación de artefactos candidatos y validación final.


## Verificación independiente del artefacto Windows 0.7

Se verificó el archivo `CRONO-Beta-Educativa-0.7-Windows.zip`: **164 archivos, 20,14 MiB, integridad CRC correcta y sin entradas duplicadas**. Incluye ejecutable, dependencias, licencias, fuentes, guía docente e informes de auditoría. No contiene partidas, perfiles, configuración docente, resultados de salas ni bancos personalizados.

El ejecutable dentro del ZIP es idéntico al ejecutable de raíz. SHA-256: `50d292957eb992c4ab51d3451abb25edc925936a721ddf328bba1596451f2cf9`.

Las 33 capturas generadas por las comprobaciones del ejecutable son PNG válidos de 1280 × 720. Inspeccioné directamente menú 0.7, guardarropa, logros, banco de preguntas y desplazamiento docente: textos y botones resultan legibles y no observé defectos materiales. La generación de esas escenas desde el EXE fue realizada por el empaquetado del agente principal; esta revisión comprueba sus resultados y el contenido del paquete, sin abrir una ventana visible ni modificar partidas.

**Windows queda verificado como paquete beta portátil en el alcance descrito.** No se amplía esta conclusión a una partida humana completa, equilibrio con alumnos o instalación Android. La revisión del APK y del dispositivo sigue siendo independiente y posterior.
