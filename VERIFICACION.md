# Verificación funcional · beta 0.9.2

Estas son comprobaciones funcionales de la entrega. Renzo solicitó un subagente para optimizar escenas densas; su intervención se limitó a render, medición y regresiones visuales.

## Juego y datos

152 pruebas aprobadas en una ejecución de 29,235 segundos con acceso a sockets locales para las salas HTTP. Cubren progresión y portales, misiones físicas, colisiones reales y ruta lunar, recompensas únicas, alcance de disparos, feedback de daño marítimo, rescates, skins, perfiles, migración de preguntas docentes y rankings/salas. Los IDs anteriores y las compras existentes se conservan.

Hay 46 mapas, 92 archivos, 1656 preguntas y actividades, 19 skins además de Crono y 13 mejoras. No son 1656 hechos históricos diferentes. Se comprueba el recorrido lunar con baja gravedad, tres piezas y reparación sin enemigos ni jefe. Se verifican el frío sin abrigo, la protección al recogerlo, agua/sombra, energía y persistencia del equipo.

## Pantalla ancha y controles

Los 46 mapas se renderizaron al inicio y al final a 1600 píxeles lógicos de ancho, además de la navegación marítima. Cinco regresiones específicas comprueban que el cielo no se desliza ni salta al avanzar o retroceder por antiguos límites del fondo, que la cámara conserva sus cachés y el ancho real, que los botones mayores no se superponen, que el multitáctil responde en otra resolución física y que un ancho sin cambios no recrea superficies.

El fondo conserva el cielo y el desplazamiento de cada plano, sin reconstruir capturas panorámicas. Se reutilizan cielos, edificios, palmeras y cultivos. Los botones principales miden 112 píxeles, las acciones 104 y descenso 96, con iconos mayores y margen lateral 32. Se midió el render nativo para detectar picos de reconstrucción; no equivale a una medición de FPS en Android.

## Paquetes

Windows 0.9.2 se compila con PyInstaller desde las fuentes finales. El empaquetador ejecuta19 escenas del EXE en modo táctil y panorámico, incluidas las rutas nuevas, Guerra Fría, Luna, navegación, guardarropa y docentes. Cada escena debe producir PNG válido y salida 0. Se comprueba integridad ZIP y se excluyen perfiles, bancos particulares y archivos temporales.

El APK 0.9.2 usa SDK 34 y JDK 17, versionCode 11. Se alinea y verifica su firma beta y la integridad ZIP; se comprueba que su tar coincide con las fuentes finales. El contenedor web redundante y el módulo iOS retirado no están presentes. La clave de firma es la misma que la beta anterior, de modo que puede instalarse encima sin desinstalar. Tamaño aproximado 14,3 MiB; esto no es una promesa de FPS. Los archivos SHA256 de la entrega y publicación permiten comprobar los paquetes.

La estructura final de Entrega contiene exclusivamente Proyecto, Windows y APK. Proyecto conserva fuentes, herramientas y documentación; Windows conserva EXE/runtime; APK conserva el instalador Android.

## Corrección de campo y escenas densas

Abajo conserva herramientas y cobertura; solo abajo + salto atraviesa una pasarela. Se comprobaron teclado, dos dedos en Android, una entrega sobre superficie delgada, una batería de Obligado, descenso sin consumir salto doble y las 48 recogidas simultáneas con partículas decorativas limitadas. La prueba de conexiones usa la intención explícita de descenso y la física real.

El subagente comprobó 2955 estados de enemigos de los 46 mapas. Su caché está limitada a 128 imágenes y conserva variantes, facciones, avisos, salud, orientación y daño. Cinco regresiones comprueban esos estados, el descarte fuera de pantalla y el aspecto de los orbes.

El benchmark reproducible está en tests/render_stress.py: 36 enemigos, 96 orbes y 36 proyectiles a 1600×720, 60 cuadros de calentamiento y 300 muestras. En la ruta de render móvil, el p95 nativo fue 17,501→3,497 ms en Primigenio, 17,701→2,883 ms en Grecia y 18,491→2,849 ms en Argentina. Las cifras completas constan en docs/CAMBIOS-0.9.2.md. No son FPS de un teléfono ni tiempos del juego completo.

## Límites

No se ha probado esta versión en un teléfono físico ni se ha realizado un piloto escolar, una campaña humana completa o prueba de mando físico. Las comprobaciones automáticas no garantizan equilibrio o rendimiento en todos los dispositivos.

Las misiones, criaturas y uniformes son ilustraciones de ficción contextualizada. Las fuentes y fichas distinguen los hechos de las licencias del juego. El profesorado debe revisar su adecuación curricular. Las salas usan HTTP sobre una red local de confianza, sin ranking global ni protección antitrampas. No hay versión iOS.
