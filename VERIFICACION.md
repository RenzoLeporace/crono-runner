# Verificación funcional · desarrollo 0.9.3

El último cierre completo de fuentes aprobó **194 pruebas en 69,228 segundos**.
Registro: `build/verification/0.9.3-desarrollo/suite-ready-android.txt`.
Las pruebas incluyen los 50 mapas y recorridos con física real, misiones,
configuración, retornos con Escape, migraciones de banco y guardado, redes LAN,
exposición, skins, logros y feedback de daño.

No es una auditoría global nueva ni una campaña humana completa. Renzo autorizó
subagentes el 27 de octubre para las comprobaciones y cambios focales de esta
sesión. Los hallazgos y cambios están en docs/HOJA-DE-RUTA.md y en las notas de
contenido, mecánicas y Android.

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
