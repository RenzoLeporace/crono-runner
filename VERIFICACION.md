# Verificación · beta educativa 0.7

24 de octubre de 2026. Windows 11, Python 3.12, pygame-ce 2.5.7.

## Fuente

113 pruebas correctas en la revisión independiente más reciente, con HTTP real sobre localhost. La cobertura de rutas obligatorias, tres fragmentos, dos archivos y reducción de anclas se amplió a los 36 mapas. Se validan 1296 registros únicos en 72 temas y tres edades; seis alternativas por combinación.

Se comprobaron migración de partidas y bancos, aislamiento de perfiles, práctica sin premios ni ranking reales, mejores puntuaciones por mapa, cinco rescates, tres grietas y retorno exacto, 60 condiciones de logros, compras de skins, teclado y multitouch, preguntas y reflexiones exportadas.

Las 36 aplicaciones físicas de actividad se completaron en fixtures con posiciones preparadas, con progreso persistente y premio único. La reacción a daño real y derrota está comprobada en los 18 jefes. Los nueve encuentros originales se vencen en simulaciones de mínima; no se afirma que los nueve nuevos se hayan derrotado sin mejoras o sin muertes.

Un ensayo independiente de 100 ciclos de compras y recarga pasó después de añadir reintentos ante bloqueos breves de OneDrive. La regresión simula además un bloqueo persistente: conserva el archivo anterior, el temporal y el aviso.

## Auditorías previas a compilar

Los dos auditores aprobaron pasar de fuente a generación de candidatos, con límites explícitos. [Informe consolidado](docs/AUDITORIA-0.7.md), [juego y arte](docs/AUDITORIA-0.7-JUGABILIDAD.md), [sistemas y aula](docs/AUDITORIA-0.7-SISTEMAS.md).

## Artefactos

El EXE Windows se compila con PyInstaller y se entrega con _internal. El empaquetado ejecuta 33 escenas del EXE, revisa las capturas, comprueba integridad ZIP y excluye partidas y bancos personales.

Android utiliza el mismo juego Python sobre CPython WebAssembly y pygame-ce offline dentro de una WebView nativa, con controles táctiles y puentes Java para almacenamiento, teclado, documentos y LAN. El APK real contiene AndroidManifest.xml y classes.dex y se alinea y firma con las herramientas SDK 34. No se entrega el archivo web intermedio de pygbag como APK instalable. Firma beta local, minSdk 26 y targetSdk 34.

El arranque WebAssembly en Edge se comprobó bloqueando todas las peticiones externas: sin peticiones fallidas ni excepciones Python. El contenedor móvil compila y el APK pasa integridad y verificación de firma v2/v3. Las comprobaciones de instalación y funcionamiento de los candidatos se registran al final de este documento al completarse.

## Límites

No hubo una campaña humana completa de los 36 mapas ni un piloto con alumnos/docentes. No se verificó un mando físico. Las pruebas automáticas y el emulador no garantizan equilibrio, accesibilidad, eficacia educativa ni rendimiento en todos los equipos/teléfonos. Las misiones, uniformes y escenas son interpretaciones de ficción con fichas y fuentes; no son reconstrucciones exactas.

Las salas usan HTTP en una red local de confianza. No hay nube, ranking global, protección antitrampas ni cifrado de archivos por el PIN. El docente debe gestionar permisos de red y archivos exportados conforme a su institución.



## Comprobación de los paquetes finales

El EXE 0.7 se ejecutó en 33 escenas, con PNG válidos de 1280×720. El ZIP pasó CRC y exclusión de partidas, perfiles y bancos personales. El auditor original inspeccionó además los menús de skins, logros, banco y pruebas docentes.

El APK Android real se instaló en un emulador aislado Android 14 (API 34). Se comprobaron arranque offline, navegación táctil, tres campos con editor nativo, perfiles conservados tras detener y reabrir el proceso, PIN guardado y acceso posterior, importación JSON con BOM/vista previa/respaldo, exportación de banco conservando tildes y CSV con BOM. El cliente Android se unió a una sala Windows y recibió el ranking con otro cliente PC. Una actualización presentó un cierre de conexión intermitente; el candidato final solicita conexiones HTTP independientes para evitar reutilizar conexiones cerradas por el servidor local.

Las pruebas finales de fuente son **113/113 correctas**, incluida una nueva comprobación de las 60 condiciones de logros y del beneficio real de energía. Los controles simultáneos se verificaron mediante eventos de dos dedos en la suite; no se afirma una prueba con dedos físicos. No se completó en Android una campaña ni una grieta de principio a fin. La comprobación LAN usa la red virtual del emulador hacia el host Windows, no varios teléfonos físicos sobre una WiFi escolar.

El emulador de Google APIs sufrió fallos de su proveedor de fuentes; se desactivaron sus servicios de Google únicamente en el entorno aislado de auditoría. El juego no necesita Google Play Services ni Internet. Esto no sustituye la prueba en teléfonos físicos.
