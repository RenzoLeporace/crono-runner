# Hoja de ruta para retomar CRONO

Actualizada el **27 de octubre de 2026**. Leer este archivo antes de continuar.

> **Punto inmediato de reanudación:** APK de prueba actualizado e instalado en el
> J6; 197 pruebas aprobadas. Se verificó minimizar/volver: sesión conservada,
> pausa al regresar y Continuar funcional. Se liberan controles retenidos,
> también en travesías navales. La vista Android pausa sus temporizadores.
> La composición rápida del HUD y sprites RLE redujeron el primer mapa de
> ~1,3 FPS a 6,6–6,7 FPS (1480×720, sin enemigos visibles): mejora real pero
> **rendimiento todavía insuficiente**, no terminado. Faltan medir jefes y
> escenas con muchas entidades. Priorizar esos escenarios y los costes de
> dibujo/copia; luego portar la guía contextual al HUD de PC y cerrar paquetes.
> La APK vigente coincide con 77 módulos y android/main.py; SHA256 y registros
> en build/verification/0.9.3-desarrollo/APK-CHECK.json. Entrega sigue en 0.9.2.

## Estado exacto al cerrar el punto de trabajo

- Base publicada: **v0.9.2**, commit `d6888e1` en `main` de
  `RenzoLeporace/crono-runner` (repositorio privado).
- Fuentes actuales: **0.9.3 en desarrollo**, con cambios de ayer y del 27 de
  octubre. No hay publicación v0.9.3 ni un Windows recompilado de esta versión.
- **197 pruebas funcionales aprobadas en 50,841 s**. Registro persistente:
  `build/verification/0.9.3-desarrollo/suite-minimize-final.txt`.
- Se generó un APK de prueba firmado: `build/android/CRONO-Beta-Educativa-0.9.3-Android.apk`.
  No presentarlo como entrega final ni confundirlo con `Entrega/APK`.
  Recompilado con `real_dt` corregido; tar y entrada Android coinciden con
  todas las fuentes. Huella y cantidad de módulos: `build/verification/0.9.3-desarrollo/APK-CHECK.json`.
- `Entrega` sigue siendo la entrega anterior y contiene únicamente
  **Proyecto / Windows / APK**. La actualización coordinada de esas tres
  carpetas queda pendiente. No generar iOS ni borrar partidas.
- Renzo pidió primero cerrar las fuentes de ayer y continuar con lo nuevo,
  evitando una compilación intermedia Windows/APK. Luego autorizó pruebas
  Android, descargas de herramientas y subagentes, y conectó un J6.
- Al advertir que quedaba 15 % de uso pidió priorizar una hoja de ruta sólida.
  Después indicó «continua»: continuar a partir de este estado, sin rehacer
  lo terminado ni perder el punto de recuperación.

## Terminado en fuentes y comprobado

### Interfaz dentro del mapa y configuración

- [x] Salto táctil de 156 px; tres acciones de 104 px encima/izquierda;
  controles con margen lateral y captura del dedo al saltar.
- [x] Android: una tarea inmediata, señal de destino y lista corta de pasos
  dentro del mapa; tarjetas educativas grandes y lectura opcional con voz local.
- [ ] **PC: falta portar esa guía simplificada al HUD del mapa**. Sus controles,
  navegación y lectura están corregidos, pero no tiene todavía el mismo HUD
  de una sola tarea. Se aclaró esto expresamente a Renzo.
- [x] E/USAR pulsado abre; mantenido realiza trabajo con barra de progreso.
  S/flecha abajo/BAJAR únicamente desciende por pasarelas delgadas.
- [x] Escape vuelve al panel de origen, partida o pausa. Desbloquear/desactivar
  prueba docente conserva el menú docente y el progreso real.
- [x] Captura de nueva tecla, cancelación y restablecimiento de controles.
  Volumen persistente para música y efectos y cambio real de tamaño de lectura.
- [x] Botón «Equipado» en la apariencia actual. Impulso con recarga efectiva de
  1,15 s, o 0,65 s con mejora; indicador de recarga.
- [x] Selección «Huellas del tiempo» agrupada sin la pared de etiquetas.
  Presentaciones con descripción histórica breve.

### Contenido, mapas y mecánicas

- [x] Primera Guerra: IDs **15, 46, 47** (1914, Verdún, armisticio).
  Segunda Guerra: **16, 48, 17** (Blitz, Stalingrado, Berlín/posguerra).
  **49 = Ypres**, excursión desde el mapa 15. Son 50 mapas y 100 temas.
- [x] La grieta **35** ahora es Chernóbil; mantiene IDs 35/70/71.
  Apolo 11 permanece en el mapa lunar **44**, sin enemigos ni jefe.
- [x] Uniformes humanos en lugar de robots humanoides/insectos mecánicos;
  Berlín sin voladores; diálogo y armisticio sin enemigos.
- [x] Centinela triple más lento, proyectiles contextuales y pinchos de hielo
  o escombros según entorno.
- [x] Frío activo en Deshielo, Andes, Malvinas y Stalingrado; abrigo entre
  15–40 % del recorrido, ralentiza sin dar inmunidad; hogueras y refugios;
  congelarse vuelve al inicio. Luna con oxígeno/tanque, Ypres con filtro/máscara.
- [x] Anclas y objetos separados sobre superficies activas. IDs y orden de
  anclas conservados. Dos balizas lunares pasan a la pasarela que las atravesaba.
- [x] Meteoritos/ceniza/bombardeos con aviso, caída y efecto de impacto.
- [x] Curiosidad situada antes del segundo archivo. Tras leerla, ese archivo
  pregunta sobre su contenido; se conserva la prioridad de los bancos docentes.
- [x] Retiradas las plantillas genéricas que solo cambiaban el título.
  Banco **formato 7**; migración mediante huellas de originales v5/v6 preserva
  ediciones docentes e IDs. Hay **1800 registros**, con reutilización entre
  edades, aproximadamente 600 enunciados distintos: no anunciar 1800 preguntas
  únicas. La banda menor filtra formulaciones originales de bandas superiores.

### Rendimiento medido y límites

- [x] Jefes: caché local recortada de cuerpo/flash, sin superficie de pantalla
  completa ni máscara por golpe. Avisos de ataque siguen en vivo.
- [x] Naves: reutilización de imágenes de reacción al daño.
- [x] Plataformas indexadas por sectores para colisiones de jugador y disparos;
  equivalencia con fuerza bruta en **8250 rectángulos** de 50 mapas/tres fases.
- [x] Caché de enemigos normaliza estados invisibles: **486 combinaciones**
  conservan los mismos píxeles. Caché limitada a 128 imágenes.
- [x] Caché de líneas de texto; evitar consulta al puente Android sin trabajos.
- [x] Separado `real_dt` para telemetría de `dt` acotado para física.
  La primera APK de prueba ocultaba cuadros >100 ms en su contador FPS;
  no usar sus FPS para concluir rendimiento. El p95 de duración no tenía ese error.
- [ ] **Todavía falta demostrar rendimiento suficiente en el J6**, especialmente
  con jefes. Las mejoras nativas y el emulador no cierran esta tarea.
- [ ] Falta recorrido humano completo para ajustar frío/oxígeno, distribución
  de recargas y lectura/dificultad para niños. Las pruebas usan trayectos
  controlados y no demuestran por sí solas buen equilibrio o comodidad infantil.

## Hallazgos de los subagentes y cambios aplicados

Renzo autorizó explícitamente su creación y sus cambios el 27 de octubre.
No hacer una nueva auditoría global por inercia.

- **rendimiento_actual**: corrigió clave de caché en `crono/enemy_art.py`;
  creó `tools/benchmark_enemy_cache.py` y dos regresiones. p95 de render aislado
  con 36 enemigos: Primigenio 2,869→1,987 ms; Medievo 2,676→0,519;
  Actualidad 1,441→0,698; Argentina 3,123→0,629. Son tiempos nativos de PC.
  Después probó Android emulado y detectó el error de delta de telemetría,
  corregido por el agente principal en `android/main.py`.
- **contenido_actual**: fuentes primarias, lecturas específicas del Blitz y
  Berlín, distinción entre respiradores de 1915/1916 y seis regresiones. Advirtió
  mezcla de vocabulario entre edades: se añadió filtrado de originales para
  niños, sin anular una selección deliberada del docente.
- **mecanicas_pruebas**: trece regresiones. Detectó anclas fuera de orden,
  solapamientos lunares, tanque demasiado temprano y anclas atravesadas por
  pasarelas. El agente principal corrigió `interaction_layout.py` y las 27
  comprobaciones integradas de mecánicas/contenido/configuración pasaron.

Notas: `docs/CAMBIOS-2026-10-27.md`,
`docs/COMPROBACIONES-MECANICAS-2026-10-27.md`,
`docs/FUENTES-HISTORIAS-2026-10-27.md`, `docs/PRUEBA-ANDROID-EMULADO.md`.

## Android: situación y siguiente acción prioritaria

### Teléfono real

Samsung **Galaxy J6 SM-J600G**, Android **10**, resolución **720×1480**.
ADB quedó autorizado por Renzo. No registrar su serial en documentación publicada.
`adb -d` selecciona el teléfono físico sin confundirlo con el emulador.

La instalación por streaming quedó detenida. Se detuvo solo ese cliente ADB y
se reintentó `--no-incremental --no-streaming`: el APK se copió a 22,6 MB/s,
pero la instalación no había devuelto éxito. `dumpsys package installs` devolvió
**Can't find service: package**; hay **12 GB libres**, así que no es falta de
espacio. No se borró ninguna partida ni se cambiaron ajustes de seguridad.
**Actualización posterior:** Renzo volvió a autorizar; `service check package`
respondió found, la instalación por copia completa devolvió Success y CRONO
arrancó. Se capturaron menú y primer mapa, sin excepción Python. La telemetría
corregida registró **2,2–2,3 FPS en menú, p95 421,5–450,7 ms**. Es un resultado
muy bajo: la optimización Android continúa abierta, incluso antes de probar
jefes. Capturas/logs en `build/verification/0.9.3-desarrollo/j6`.

El siguiente objetivo es separar tiempo de eventos/actualización/dibujo/
presentación para localizar este coste base y después medir escenas densas y
jefes. Renzo confirmó que le gustó la nueva interfaz y reiteró que entidades y
jefes son las zonas donde más se cae el rendimiento. No confundir una captura
correcta con fluidez aceptable.

1. Comprobar autorización USB: volvió a marcar «unauthorized» después de un
   reinicio del servidor ADB. Renzo recibió la petición de aceptar «Permitir
   siempre desde esta computadora». No diagnosticar el sistema hasta que el
   estado sea `device`. Luego comprobar conexión y servicio del teléfono:

```powershell
$adb = 'C:/Users/renzo/AppData/Local/Android/Sdk/platform-tools/adb.exe'
& $adb devices -l
& $adb -d shell getprop ro.product.model
& $adb -d shell service check package
& $adb -d shell getprop sys.boot_completed
```

2. Si Android sigue sin servicio de instalación, explicar el fallo y pedir a
   Renzo reiniciar manualmente el teléfono; no restablecer, no desinstalar,
   no desactivar verificaciones de seguridad ni reiniciar la PC.
3. Cuando el servicio responda, instalar sin borrar datos:

```powershell
& $adb -d install --no-incremental --no-streaming -r 'build/android/CRONO-Beta-Educativa-0.9.3-Android.apk'
& $adb -d shell am start -W -n org.renzoleporace.crono/.MainActivity --ez crono_performance true
& $adb -d logcat -d -s CRONO:D
```

4. Continuar desde el J6 ya instalado; revisar captura de dedo, salto/impulso, E mantenida,
   lectura, audio, retorno con Atrás, activación de anclas y guardado.
5. Probar un jefe y una escena de entidades; guardar capturas y registros
   `CRONO_FRAME_STATS` con mapa/estado/p95. Medir con telemetría corregida.
6. Si hay caídas, identificar coste de actualización, dibujo, escalado y
   presentación/WebView. No prometer FPS a partir del benchmark nativo ni
   comparar directamente software WebView con hardware de consolas clásicas.

### Emulador

Había un AVD instalado; **no se descargó otro emulador**. Se inició
`Pixel_3a_API_34_extension_level_7_x86_64` con `-read-only -no-snapshot
-no-window -no-audio -no-boot-anim -gpu auto`. Serial `emulator-5554`.
El perfil base del AVD no se modifica. Android 14/API34, x86_64, WebView 113.

Arranque offline y acciones del tutorial comprobados. Usa **Google SwiftShader
por software** y es lento incluso en menú: p95 de cuadro aproximadamente
93–173 ms. El FPS reportado por la primera APK tenía el límite de delta ya
explicado; no usarlo como FPS real. No se llegó a probar un jefe emulado.

`tools/test_android_emulator.py` se bloquea al serial del emulador y comprueba
`ro.kernel.qemu=1`; su opción `--fresh` solo puede limpiar ese perfil temporal,
nunca el J6. No usarla en teléfonos. Ver informe de Android emulado.

## Herramientas y órdenes de construcción

Python del entorno:
`C:/Users/renzo/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`.
Dependencias pygame en `.vendor`. `PYTHONPATH='.vendor;tests'`, `PYTHONUTF8=1`.

```powershell
$py = 'C:/Users/renzo/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$env:PYTHONPATH='.vendor;tests'; $env:PYTHONUTF8='1'
& $py -m unittest discover -s tests
```

Las pruebas de salas HTTP necesitan sockets localhost fuera del sandbox.
No reducir ni eliminar esas pruebas por el bloqueo del sandbox.

Android usa **JDK 17** (no JDK 21, que provoca error D8), SDK 34:

```powershell
$env:JAVA_HOME='C:/Program Files/Eclipse Adoptium/jdk-17.0.20.101-hotspot'
& $py tools/prepare_android.py
& $py tools/build_android.py
```

La preparación necesita acceso a la toolchain/caché de pygbag; no confundir
«assets preparados» con «APK compilado». El constructor verifica alineación,
firma beta v2/v3 e integridad. La clave `.android-build/crono-beta.keystore`
permanece privada y nunca se publica. Conservar la firma para actualizar.

## Pendiente para una entrega final coherente

1. [ ] Resolver el rendimiento bajo medido en J6; segmentar los tiempos del
   cuadro y después probar muchas entidades y jefes. No compilar Windows aún
   como entrega final si Android sigue sin validación.
2. [x] Confirmar que el tar del APK coincide con las fuentes finales, incluida
   la corrección `real_dt` y los últimos cambios de subagentes.
3. [ ] Completar pruebas Android de jefe, audio/voz y reinicio/persistencia.
4. [ ] Recompilar Windows: `tools/build_beta.py` y `tools/package_beta.py`.
   Revisar las capturas del EXE, incluidos mapas 35 y 46–49 y configuración.
5. [ ] Actualizar documentación con resultados efectivos; no heredar afirmaciones
   antiguas de que el frío desaparece con el abrigo o de que hay 46 mapas.
6. [ ] Guardar registros y SHA256 en `build/verification/0.9.3-desarrollo`.
7. [ ] `git add` de fuentes nuevas antes de `tools/create_delivery.py`: el
   copiado de Proyecto se basa en `git ls-files`.
8. [ ] Actualizar juntas las carpetas Proyecto/Windows/APK. El script usa el ZIP
   Windows y APK actuales, por eso no ejecutarlo antes de compilar Windows.
9. [ ] Solo después de verificar paquetes: quitar generados viejos dentro del
   proyecto, conservando perfiles, bancos docentes y clave. No borrar un árbol
   recursivo sin comprobar su ruta absoluta y que está dentro del workspace.
10. [ ] Commit/push y publicación v0.9.3 con ZIP/APK/SHA256. No existe esa release
    todavía. El conector GitHub no sube binarios; puede usarse la API con la
    credencial configurada en memoria, sin imprimir token. Repositorio privado.

Para push sin diálogo de credenciales:
`git -c credential.username=RenzoLeporace push origin main`, con
`GIT_TERMINAL_PROMPT=0` y `GCM_INTERACTIVE=never`. Git puede necesitar escalación.

## Reglas que siguen vigentes

- Entrega tiene solo Proyecto, Windows, APK. Sin iOS.
- Conservar IDs de mapas/preguntas/guardados y las ediciones docentes.
- No empaquetar datos de alumnos, bancos particulares, claves ni temporales.
- No apagar la PC: las instrucciones de apagado antiguas ya fueron atendidas.
- No declarar terminado el rendimiento Android por pruebas de PC/emulación.

## Aclaraciones finales de Renzo

El pedido de interfaz intuitiva abarca Android y PC. Android ya tiene el HUD
nuevo; falta llevar la guía contextual simplificada al HUD de PC. Renzo indicó
que le encantó la interfaz Android y autorizó seguir con rendimiento, sobre
todo con muchas entidades y jefes. No considerar cerrado ese rendimiento.

## Último seguimiento de rendimiento en J6

Checkpoint inicial subido a GitHub: **fcd7e54**. Después se añadieron diagnósticos
por etapas en android/main.py y crono/viewport.py, y una corrección de formato:
la UI usaba BGRA mientras pantalla/mundo usan RGBA. En menú 1480×720 se midió
p95 de eventos0,2ms, actualización0,3ms, render458,9ms, composición360ms,
copia20,4ms y flip11,7ms (percentiles independientes). No era coste de enemigos.

La UI ahora usa los mismos canales que la pantalla y los menús opacos no hacen
mezcla alfa. **12 regresiones de render aprobadas en2,928s** tras el cambio.
Se recompiló y firmó el APK de prueba. Los siguientes registros muestran canales
coincidentes, pero el teléfono se bloqueó y el viewport pasó a960: no presentar
sus8–9FPS como comparación válida con el ensayo anterior a1480.

Para evitar ese problema, MainActivity mantiene la pantalla encendida solo en
primer plano mediante FLAG_KEEP_SCREEN_ON. Renzo recibió una petición para
mantener el J6 desbloqueado durante un minuto; la medición comparable permanece
pendiente. La última APK está verificada y la instalación posterior en el J6 devolvió
Success. Para repetir la instalación usar `adb -d install --no-incremental --no-streaming -r ...`.
La huella vigente está en APK-CHECK.json, no en los informes anteriores.

Prioridad al retomar: (1) instalar esa APK y dejar la pantalla encendida,
(2) capturar métricas a1480×720 en menú/mapa, (3) activar prueba docente y medir
un jefe recibiendo daño/salvas, (4) medir una escena con muchas entidades. Si los
blits de jefes/enemigos/fondos dominan, revisar también los formatos BGRA de
imágenes cached (Painter.image, enemy_picture, body_image) antes de ampliar
cachés. Conservar avisos, feedback de daño, colores y memoria acotada.

La telemetría de diagnóstico toma60cuadros y muestra phases_p95: events,
update,render,compose,display_copy,flip,present; además de entidades visibles,
proyectiles,jefe activo y máscaras de píxel. El modo normal conserva120muestras.
Descartar ventanas de transición, bloqueo o cambio de resolución.

## Actualización posterior: minimizar y dibujo en el J6

Pedido más reciente: comprobar qué pasa al minimizar. Se ensayó HOME durante
8 segundos desde una partida activa y se volvió a la misma Activity: mismo
proceso, pantalla de pausa, partida conservada, sin traceback Python y Continuar
vuelve al mapa. Se repitió tras recompilar/instalar las correcciones. No equivale
a comprobar que Android mate el proceso por falta de memoria; eso sigue pendiente.

MainActivity llama onPause/pauseTimers al salir y onResume/resumeTimers al volver,
y detiene la lectura en voz. El juego atiende pérdida de foco y minimización;
limpia dedos, posiciones, acciones pendientes e impulso/uso de mando, guarda y
pausa. Esto corrige un timón/disparo que podían quedar retenidos al suspender una
travesía naval. Las regresiones verifican que tiempo, posición y disparos no
avanzan durante la pausa. La suite completa pasó 197 pruebas en 50,841 segundos;
16 pruebas focales de navegación y render también pasaron.

El cuello de botella inicial del mapa era mezclar alfa en un HUD de pantalla
completa: p95 de composición ~333 ms, 1,3 FPS. El HUD táctil ahora utiliza recortes
opacos y transparencia por clave; conserva exactamente los píxeles de referencia
en seis mapas consecutivos. Los sprites finales, plataformas y cuerpos de jefes
usan RLE y canales de pantalla; las composiciones intermedias no usan RLE para
conservar los halos. No se aumentaron límites de caché ni se borraron detalles.
El flash móvil de daño se dibuja sobre el mundo y mantiene legible el HUD.

Última medición física comparable del primer mapa a1480×720: 6,6–6,7 FPS,
p95 del cuadro147ms, actualización13,5–13,8ms, render135ms, composición20–23ms,
copia19,6–19,7ms y flip10,5ms. Menú8,3–8,5FPS, cuadro114–117ms. Son registros de
mapa sin enemigos visibles ni jefe: **no cierran el pedido de optimización**.
No confundir las mediciones previas de viewport960 con estas.

Próximo trabajo de rendimiento: activar modo docente sin alterar registros,
abrir tercer mapa de la primera era, usar herramientas para ir al jefe y medir
sus salvas/daño con crono_performance=true. Después escena densa. Examinar copias
de pantalla y dibujo de fondo antes de ampliar cachés; mantener controles, arte,
avisos y formato ancho. Los informes locales conservan fases y entidades visibles.
