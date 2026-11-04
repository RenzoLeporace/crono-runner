# Hoja de ruta para retomar CRONO

Actualizada el **4 de noviembre de 2026**. Leer este archivo antes de continuar.

## Estado actual

- Última publicación en GitHub: **v0.9.2** (pre-release). El repositorio es público.
- Fuentes en `main`: **0.9.3 en desarrollo**. No existe todavía la release v0.9.3.
- **215 pruebas** pasan con `python -m unittest discover -s tests`.
- Hay un APK de prueba firmado en `build/android/CRONO-Beta-Educativa-0.9.3-Android.apk`
  (local, no versionado). No presentarlo como entrega final. La huella vigente está en
  `build/verification/0.9.3-desarrollo/APK-CHECK.json`.
- `Entrega` contiene la entrega anterior (Proyecto / Windows / APK). Actualizar las tres
  carpetas juntas cuando se cierre la 0.9.3.
- Los cambios de la 0.9.3 están resumidos en [CHANGELOG.md](../CHANGELOG.md).

## Prioridades

1. [ ] **Rendimiento en el J6 con jefes y escenas densas.** Es el bloqueo principal de la
   0.9.3. Las mejoras medidas en PC y en el emulador no cierran esta tarea.
2. [ ] **Balance con recorridos humanos completos:** frío y oxígeno, distribución de
   recargas, lectura y dificultad para niños. Las pruebas automáticas usan trayectos
   controlados y no demuestran por sí solas un buen equilibrio.
3. [ ] Pruebas Android de jefe, audio y voz, y reinicio con persistencia (incluido que
   Android cierre el proceso por falta de memoria).
4. [ ] Probar en Windows la guía de una tarea del HUD de PC.

## Rendimiento en el J6

Teléfono: Samsung **Galaxy J6 SM-J600G**, Android 10, 720×1480. No registrar su serial en
documentación publicada. `adb -d` selecciona el teléfono físico y no el emulador.

Última medición comparable del primer mapa a 1480×720, sin enemigos visibles ni jefe:
**6,6–6,7 FPS**, p95 del cuadro 147 ms (actualización 13,5–13,8 ms, render 135 ms,
composición 20–23 ms, copia 19,6–19,7 ms, flip 10,5 ms). Menú: 8,3–8,5 FPS, cuadro
114–117 ms. Las mediciones con viewport 960 no son comparables con estas.

**4 de noviembre · pendiente de medir en el J6.** En esa medición, composición (20–23 ms) y
copia (19,6 ms) eran pasadas de pantalla completa. Ahora, en partida, la interfaz táctil se
dibuja directo sobre el mundo y el mundo directo en la ventana, así que la composición y la
copia deberían ser casi cero. Además, las piezas de arte se preparan de a una antes de entrar
en pantalla. En la PC de desarrollo el render en Android bajó un 58 % en la mediana y un 59 %
en el p99 (ver CHANGELOG.md). Hay que confirmarlo en el teléfono con `crono_performance=true`.
Si `display_copy` no baja a cero, el formato de la ventana en pygbag no coincide con el del
mundo y `world_fits_display()` lo está descartando.

Lo que ya se corrigió y no hay que rehacer:

- El HUD táctil usa recortes opacos y transparencia por clave en lugar de mezclar alfa a
  pantalla completa (antes: composición p95 ~333 ms, 1,3 FPS).
- La UI usa los mismos canales RGBA que la pantalla; los menús opacos no mezclan alfa.
- Sprites, plataformas y cuerpos de jefes usan RLE y el formato de pantalla.
- `real_dt` separa la telemetría del `dt` acotado de la física. Los FPS de la primera APK de
  prueba ocultaban cuadros de más de 100 ms: no usarlos como referencia.
- MainActivity mantiene la pantalla encendida en primer plano (`FLAG_KEEP_SCREEN_ON`) y
  pausa y reanuda temporizadores y voz al minimizar.

Siguiente medición:

1. Instalar la APK sin borrar datos y dejar la pantalla encendida.
2. Capturar métricas a 1480×720 en menú y mapa.
3. Activar la prueba docente y medir un jefe recibiendo daño y lanzando salvas.
4. Medir una escena con muchas entidades.
5. Si dominan los blits de jefes, enemigos o fondos, revisar el formato de las imágenes en
   caché (`Painter.image`, `enemy_picture`, `body_image`) antes de ampliar cachés.
   Conservar avisos, feedback de daño, colores y memoria acotada.

La telemetría de diagnóstico toma 60 cuadros y muestra `phases_p95` (events, update,
render, compose, display_copy, flip, present), entidades visibles, proyectiles, jefe activo
y máscaras de píxel. Descartar ventanas de transición, bloqueo o cambio de resolución.

```powershell
$adb = 'C:/Users/renzo/AppData/Local/Android/Sdk/platform-tools/adb.exe'
& $adb devices -l                       # debe decir "device", no "unauthorized"
& $adb -d shell service check package   # debe responder "found"
& $adb -d install --no-incremental --no-streaming -r 'build/android/CRONO-Beta-Educativa-0.9.3-Android.apk'
& $adb -d shell am start -W -n org.renzoleporace.crono/.MainActivity --ez crono_performance true
& $adb -d logcat -d -s CRONO:D
```

Si aparece «unauthorized», aceptar «Permitir siempre desde esta computadora» en el
teléfono. Si Android no tiene servicio de instalación, reiniciar el teléfono a mano; no
restablecer, desinstalar ni desactivar verificaciones de seguridad.

### Emulador

AVD `Pixel_3a_API_34_extension_level_7_x86_64` (Android 14, x86_64), iniciado con
`-read-only -no-snapshot -no-window -no-audio -no-boot-anim -gpu auto`, serial
`emulator-5554`. Usa SwiftShader por software y es lento incluso en el menú (p95
~93–173 ms), así que sirve para probar funciones, no rendimiento.
`tools/test_android_emulator.py` solo actúa sobre el emulador (`ro.kernel.qemu=1`); su
opción `--fresh` nunca debe usarse con el teléfono.

## Construcción

```powershell
$py = 'C:/Users/renzo/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$env:PYTHONPATH='.vendor;tests'; $env:PYTHONUTF8='1'
& $py -m unittest discover -s tests
```

Las pruebas de salas HTTP necesitan sockets localhost; no eliminarlas si un sandbox las
bloquea.

Android usa **JDK 17** (JDK 21 provoca un error de D8) y SDK 34:

```powershell
$env:JAVA_HOME='C:/Program Files/Eclipse Adoptium/jdk-17.0.20.101-hotspot'
& $py tools/prepare_android.py
& $py tools/build_android.py
```

La preparación necesita la toolchain de pygbag; «assets preparados» no es lo mismo que
«APK compilado». El constructor verifica alineación, firma v2/v3 e integridad. La clave
`.android-build/crono-beta.keystore` es privada y nunca se publica; conservarla para poder
actualizar la app instalada.

## Pasos para publicar la 0.9.3

1. [ ] Cerrar el rendimiento en el J6 (prioridad 1).
2. [ ] Recompilar Windows con `tools/build_beta.py` y `tools/package_beta.py`, y revisar
   capturas del EXE, incluidos los mapas 35 y 46–49 y la configuración.
3. [ ] Recompilar el APK con las fuentes finales.
4. [ ] Guardar registros y SHA256 en `build/verification/0.9.3-desarrollo`.
5. [ ] `git add` de las fuentes nuevas antes de `tools/create_delivery.py`: la copia de
   Proyecto se basa en `git ls-files`.
6. [ ] Actualizar juntas las carpetas Proyecto / Windows / APK. El script usa el ZIP de
   Windows y el APK actuales, así que se ejecuta después de compilar.
7. [ ] Quitar generados viejos del proyecto, conservando perfiles, bancos docentes y la
   clave. No borrar carpetas recursivamente sin comprobar su ruta.
8. [ ] Publicar la release v0.9.3 con ZIP, APK y SHA256, y actualizar CHANGELOG.md.

## Reglas

- La entrega tiene solo Proyecto, Windows y APK. Sin iOS.
- Conservar IDs de mapas, preguntas y guardados, y las ediciones docentes.
- No empaquetar datos de alumnos, bancos particulares, claves ni temporales.
- No declarar terminado el rendimiento Android a partir de pruebas en PC o emulador.
- No anunciar 1800 preguntas únicas: son 1800 registros con unos 600 enunciados distintos.
- IDs de mapas recientes: Primera Guerra **15, 46, 47**; Segunda Guerra **16, 48, 17**;
  Ypres **49** (excursión desde el 15); Chernóbil **35** (IDs 35/70/71); Luna **44**.
