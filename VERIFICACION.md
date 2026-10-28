# Verificación funcional · desarrollo 0.9.3

El último cierre completo de fuentes aprobó **197 pruebas en 50,841 segundos**.
Registro: `build/verification/0.9.3-desarrollo/suite-minimize-final.txt`.
Las pruebas incluyen los 50 mapas y recorridos con física real, misiones,
configuración, retornos con Escape, migraciones de banco y guardado, redes LAN,
exposición, skins, logros y feedback de daño.

No es una auditoría global nueva ni una campaña humana completa. Renzo autorizó
subagentes el 27 de octubre para las comprobaciones y cambios focales de esta
sesión. Los hallazgos y cambios están en docs/HOJA-DE-RUTA.md y en las notas de
contenido, mecánicas y Android.

Actualización de idiomas: **204 comprobaciones verificadas**. La ejecución
general pasó203/204 en51,122s; únicamente la prueba HTTP de salas encontró el
bloqueo de socket del aislamiento. Esa misma prueba, sin modificarla, pasó
fuera del aislamiento en0,708s. Registros: suite-localization.txt y
localization-lan-test.txt en build/verification/0.9.3-desarrollo.
Incluyen cobertura de cada pregunta/respuesta original en portugués, fechas,
opciones diferentes, conservación de IDs y banco, guardado de idioma, editor
bilingüe y pantallas PC/táctiles en ambos idiomas.

## Fuentes y compatibilidad

Hay 50 mapas, 100 temas y 1800 registros de preguntas. Hay reutilización entre
bandas: ese número no representa 1800 preguntas distintas. Se retiraron las
plantillas genéricas originales. Los IDs anteriores se conservan; el banco7
migra solo preguntas originales cuyo contenido coincide con una huella v5/v6.
Las modificaciones y adiciones docentes permanecen. Se conservan compras,
logros, mapas y guardados; las nuevas rutas usan IDs46–49.

Las pruebas de colisiones locales coinciden con fuerza bruta en 8250 rectángulos
sobre 50 mapas y tres fases. La caché de enemigos conserva exactamente los
píxeles en 486 combinaciones. Se verifican los avisos, reacciones, refugios,
recargas y congelación. Las posiciones de interacción se separan sin modificar
las superficies de los mapas; dos anclas lunares pasan a la pasarela que antes
las atravesaba.

## Rendimiento

Los benchmarks reproducibles son tests/boss_stress.py, tests/frame_stress.py,
tests/render_stress.py y tools/benchmark_enemy_cache.py. Las mediciones nativas
están en build/verification/0.9.3-desarrollo y las notas de cambios. No son FPS
de Android. El emulador utiliza SwiftShader por software y es demasiado lento
incluso en el menú para inferir rendimiento del J6.

La primera telemetría Android limitaba el delta de diagnóstico a100ms. Se
corrigió separando tiempo real y delta físico; no usar los FPS anteriores como
medida real. Los percentiles de duración del cuadro anteriores sí se midieron
sin ese límite. La próxima comprobación debe incluir un jefe en Android real.

## Paquetes y dispositivos

Se compiló y verificó un **APK de prueba0.9.3**, SDK34/JDK17, versionCode12,
firma beta v2/v3. Su integridad ZIP pasó. La clave de firma no se distribuye.
El emulador API34/x86_64 arrancó offline sin errores fatales y permitió menú,
primer mapa, desplazamiento, orbes, salto, impulso y disparo. Más resultados en
docs/PRUEBA-ANDROID-EMULADO.md. No equivale a haber jugado toda la campaña.

Renzo conectó un Samsung Galaxy J6 SM-J600G, Android10,720×1480. ADB quedó
autorizado, pero la instalación todavía no terminó; una consulta devolvió
«Can't find service: package». Hay12GB libres. No se borraron datos ni se
modificaron ajustes de seguridad. Después de repetir la autorización, el servicio respondió y la instalación
terminó correctamente. El menú y primer mapa se dibujaron sin excepción Python.
La primera métrica física corregida dio 2,2–2,3 FPS en menú y p95 421,5–450,7ms;
es muy baja y no cierra la optimización. Aún faltan jefe y escena densa.

**Windows no se recompiló en esta sesión. Entrega y la publicación de GitHub
siguen siendo0.9.2.** El APK de prueba vive en build/android, todavía no es una
entrega final. Próximos pasos exactos en docs/HOJA-DE-RUTA.md.

Lo anterior registra el punto previo a los idiomas: posteriormente se recompiló
Windows y el APK con español/portugués de Brasil. La publicación GitHub continúa
en0.9.2; las compilaciones0.9.3 locales siguen en desarrollo.

## Seguimiento físico: pausa y composición

La APK de prueba más reciente se instaló correctamente en el J6, sin borrar datos.
Minimizar ocho segundos y volver conservó el proceso y regresó en pausa;
Continuar reanudó la partida, sin traceback Python. MainActivity suspende los
temporizadores de WebView; pérdida de foco/minimización también libera controles
retenidos en plataforma y navegación. No se ensayó muerte del proceso por Android.

Tras retirar la mezcla alfa de pantalla completa del HUD táctil y preparar sprites
RLE, el primer mapa a1480×720 subió de~1,3 a6,6–6,7FPS; composición p95 bajó de
~333 a20–23ms. Sigue siendo insuficiente y todavía no se midieron jefe/escena densa.
La regresión de píxeles del HUD pasa en seis mapas consecutivos; 197 pruebas totales.
La APK coincide con77módulos y la entrada Android. Huella vigente: APK-CHECK.json.
Entrega y Windows permanecen en0.9.2; esto es una compilación de prueba.

## Idiomas y paquetes locales posteriores

El EXE y el APK0.9.3 se recompilaron con el catálogo offline es/pt-BR. El modelo
de traducción y sus herramientas no forman parte del runtime. Se conservaron
24 capturas desde fuentes: menús, selector, mapa, pregunta, banco y editor,
en dos idiomas y dos modos de entrada. La suite funcional se completó con
la prueba LAN repetida fuera del aislamiento, como se detalla arriba.

El intento de instalar esta última compilación en el J6 devolvió «no devices
found»; no presentar la instalación previa como prueba física de los idiomas.
La lectura en voz selecciona es o pt-BR si existe una voz offline del idioma;
no se confirmó una voz portuguesa instalada en un dispositivo real.

El empaquetado Windows comprobó36 capturas del EXE, incluidas preguntas en
español/portugués, selector de idioma, dos modos de entrada y rutas de las
guerras mundiales. ZIP íntegro y catálogo incluido.26 pruebas focales de
idiomas/editor aprobaron después del último ajuste de nombres propios.
Entrega local0.9.3 mantiene exactamente Proyecto/Windows/APK. Es una entrega
de desarrollo; la publicación de GitHub continúa en0.9.2 y la optimización
Android con jefes sigue abierta.
