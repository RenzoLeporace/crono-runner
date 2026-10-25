# Verificación funcional · beta educativa 0.8

25 de octubre de 2026. Comprobaciones realizadas por el agente principal; no se convocaron subagentes ni se hicieron nuevas auditorías. Los informes 0.7 en docs corresponden únicamente a aquella versión.

## Código y juego

La suite general pasó **124/124 pruebas** en 217,651 segundos. Tras los ajustes de caché e interfaz, las cinco comprobaciones enfocadas de interfaz 0.8 pasaron en 46,568 segundos. Incluyen cámara de 1280, 1600 y 1920 píxeles lógicos, conservación del tamaño del personaje, zonas laterales dibujadas, caché reutilizada, menús, música, currículo y guardado marítimo.

Las tres travesías acuáticas se completaron con simulación de controles reales, recogida de cargas, disparos, errores/reintentos educativos, guardián y muelle. Se comprueba la vuelta al punto de origen tras recargar y la recompensa única. Ningún mapa terrestre puede volver a activar el antiguo barco montable.

Se comprueba el bloqueo del portal sin misión y archivo; los fragmentos solos ya no abren la salida. Las actividades físicas existentes, reducción de anclas, perfiles, editor docente, importación/exportación, puntuaciones, 60 condiciones de logros y salas HTTP locales siguen cubiertos por la suite. Los nueve guardianes originales se derrotaron en simulaciones de mínima con movimiento, salto, descenso y esquiva de marcas, usando el nuevo alcance corto; esto no constituye una campaña humana completa.

## Windows y Android

Windows se genera con PyInstaller incluyendo la música original. El paquete conserva el EXE y `_internal`; no necesita Python instalado. El empaquetador ejecuta las escenas del EXE antes de crear el ZIP y comprueba su integridad y exclusión de partidas personales.

El APK real se generó con SDK 34 y JDK 17, se alineó y se verificó su firma beta v2/v3. Incluye AndroidManifest.xml, classes.dex, CPython WebAssembly, pygame y todos los recursos offline; el intermedio webapp.apk de pygbag no es el APK instalable. Android mínimo 8 (API 26).

El intento de arrancar el APK 0.8 en el emulador aislado se detuvo antes de Android por espacio libre insuficiente para el AVD. Por tanto no se afirma una ejecución del APK 0.8 en emulador; las pruebas instaladas de la versión 0.7 quedan documentadas en sus informes históricos.

## Web experimental para iOS

El motor web arrancó en Edge/Chromium local a 1600×720, con cámara ancha y controles táctiles. La prueba conservó datos Unicode en IndexedDB tras recargar y volvió a iniciar el juego después de cortar la conexión; no hubo excepciones Python/JavaScript ni peticiones fallidas en esa ejecución. La caché offline requiere HTTPS o localhost; una IP de PC mediante HTTP sigue necesitando el servidor conectado.

La muestra de rendimiento web de ese ensayo fue **35,5 FPS** y **29,8 ms de render p95** en Edge headless de esta PC, con juego y tutorial inicial. Es una observación de ese entorno, no un benchmark de teléfonos ni garantía de 60 FPS. La optimización reutiliza escenarios, paneles táctiles y texto, evita dibujos fuera de cámara y reduce efectos ambientales móviles.

La edición iOS es web experimental, no un IPA firmado. No se probó Safari ni un iPhone/iPad físico. La versión web ofrece progreso individual y no cliente de salas LAN; para salas utiliza Windows o el APK Android.

## Límites

No se completó una campaña humana de los 36 mapas ni un piloto escolar. No se verificaron teléfonos físicos o un mando físico. Las misiones y escenas históricas son interpretaciones, y el contenido requiere revisión curricular docente. El juego no cifra las salas HTTP ni impide alteraciones de rankings locales.

Los hashes finales y tamaños se entregan en Entrega/CHECKSUMS.json y permiten identificar exactamente los paquetes distribuidos.

## Paquete Windows final

El ejecutable 0.8 abrió correctamente **36 escenas**, incluidas Historia, Expansiones, travesía marítima, skins, docentes y las rutas bonus. Cada ejecución terminó con código 0 y una captura PNG válida. El ZIP pasó integridad CRC y contiene el lanzador para iPhone y sus recursos públicos. No incluye partidas ni bancos personales.
