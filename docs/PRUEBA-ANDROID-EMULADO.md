# Prueba Android en emulador · preparación

Destino exclusivo: `emulator-5554`, emulador temporal de Android 14/API 34,
modelo `sdk_gphone64_x86_64`. No se usa el teléfono conectado ni sus perfiles.
El estado físico inicial informado por `wm size` es 1080×2220; las capturas
determinarán el tamaño efectivo cuando la actividad quede en horizontal.

Herramienta: `tools/test_android_emulator.py`. Rechaza destinos que no informen
ser un emulador; todos los comandos incluyen el serial fijo. Permite instalar
un APK indicado expresamente, reiniciar solo sus datos de prueba, desconectar
la red del emulador, lanzar el juego con métricas, tocar controles y guardar
capturas y Logcat. Ninguna de estas acciones afecta un teléfono físico.

Secuencia prevista, pendiente del APK final de trabajo:

1. Registrar versión de Android, WebView, ABI, tamaño y huella de la imagen.
2. Instalar el APK 0.9.3, guardar su SHA256 e iniciar un perfil de prueba limpio.
3. Activar modo avión, deshabilitar WiFi/datos y lanzar sin red.
4. Comprobar menú, carga y entrada al primer mapa mediante capturas y estado.
5. Probar desplazamiento, salto, disparo, pausa, lectura, misiones y retorno.
6. Revisar volumen, tamaño de lectura y pruebas docentes sin abandonar su menú.
7. Entrar a una escena con jefe y proyectiles; guardar muestras de 120 cuadros
   de `CRONO_FRAME_STATS`, con estado, mapa, viewport y proyectiles.
8. Revisar errores de Python, Java, memoria y arranque en Logcat.

Los gestos ADB de un dedo no prueban la comodidad real de los pulgares ni el
multitáctil. Las métricas de un emulador x86_64 en una PC no se presentarán como
FPS de un Samsung J6 ni como garantía para equipos Android de baja potencia.
La lectura por voz depende de una voz española instalada; no se descarga una
voz para esta prueba sin autorización.

## Resultado de la ejecución del 27 de octubre

Se instaló el APK de prueba y arrancó sin red, sin excepción fatal Java/Python.
Se comprobaron menú, entrada al primer mapa, caminar, recoger orbes, salto,
impulso y disparo, avanzando en el tutorial. Se guardaron capturas de libro,
historia y retornos; no se completó una campaña ni se llegó a un jefe.

El renderer fue Google SwiftShader por software. Los percentiles de duración
fueron aproximadamente 93–173 ms, ya lentos en menú. Los FPS registrados por
esa primera APK tienen un piso artificial de 10 porque usaban delta acotado;
no deben citarse como FPS reales. El agente principal corrigió la telemetría y
recompiló después; no se repitió esta prueba emulada con la corrección.

Los registros/capturas están en build/verification/0.9.3-desarrollo/android-emulator.
La última APK verificada tiene SHA256
42753d09201efb51839e3b173df6cab91c5e7fd51d1c6df3ea5f9e08e4e09377;
sus 77 módulos y entrada Android coinciden con las fuentes.

El emulador ya no aparecía en ADB al cerrar estas pruebas. No se apagó la PC,
no se modificó el perfil base del AVD y el J6 se manejó por separado.

