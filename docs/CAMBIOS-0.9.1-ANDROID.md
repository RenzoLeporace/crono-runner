# CRONO Android 0.9.1

El fondo conserva el cielo fijo y el desplazamiento propio de cada plano. Se
eliminó la captura panorámica que se reconstruía cada tramo de cámara: provocaba
saltos visuales e invalidaba las cachés gráficas. Cielos, edificios y vegetación
se reutilizan como recursos independientes. La cámara y las plataformas conservan
su escala; los escenarios se dibujan hasta el ancho real de la pantalla.

Los botones principales pasan de 78 a 112 píxeles lógicos; las acciones, de 72
a 104, y descenso, de 66 a 96. Los iconos también son mayores. Conservan margen
lateral de 32 píxeles, separación entre botones y uso simultáneo con varios dedos.

Los cambios de tamaño de pantalla se estabilizan antes de recrear superficies;
una proporción que alcanza el límite de ancho no dispara recreaciones repetidas.

La actualización conserva el identificador de aplicación y la clave de firma.
Se instala encima de la versión anterior sin desinstalarla para conservar datos.
No se modifican IDs, preguntas, guardados ni ediciones docentes.
