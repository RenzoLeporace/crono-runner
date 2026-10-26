# Beta 0.9.2 · misiones y rendimiento

Abajo sigue aplicando herramientas y cobertura. Ya no hace caer a Crono por una
pasarela delgada mientras prepara una batería, entrega materiales o repara la
nave. Para atravesar una pasarela se necesita **abajo + salto**, con teclado o
con dos dedos en Android. El botón táctil ahora indica ACCIÓN. Los saltos dobles
no se consumen ni se activan accidentalmente al bajar. Se conservan las teclas
personalizadas y los guardados.

El subagente de rendimiento solicitado encontró que los enemigos reconstruían
su imagen, máscara y doce capas de contorno a la vez, doce veces por segundo.
Aplicó una caché compartida de hasta 128 imágenes recortadas, con claves para
fase, salud, daño, aviso de ataque, dirección, facción y variante. También creó
imágenes reutilizables para orbes y pulsos y descartó elementos fuera de pantalla
antes de dibujarlos. No se retiraron enemigos ni objetos para obtener la mejora.

Se redujeron además las asignaciones de rectángulos al comprobar recogidas y el
trabajo sobre plataformas inmóviles. El panel superior se reutiliza. Los efectos
decorativos quedan limitados a 120 partículas con controles táctiles y 240 con
teclado; se conservan todos los orbes recogidos, premios y sonidos.

## Medición reproducible

`python tests/render_stress.py --output resultado.json` construye una escena de
1600×720 con 36 enemigos, 96 orbes y 36 proyectiles. Tras 60 cuadros de
calentamiento mide otros 300. Estos son los picos p95 de tiempo de render:

| Escena con ruta de render móvil | Antes | Después |
| --- | ---: | ---: |
| Primigenio | 17,501 ms | 3,497 ms |
| Grecia | 17,701 ms | 2,883 ms |
| Argentina | 18,491 ms | 2,849 ms |

En la ruta de escritorio, los p95 fueron respectivamente 18,767→3,117 ms,
17,142→2,843 ms y 19,544→4,142 ms. Se comprobaron además 2955 estados visuales
de enemigos a través de los 46 mapas, y cinco regresiones de caché/render.

**Son mediciones de render SDL nativo en la PC de desarrollo, no FPS de un
teléfono ni tiempos del juego completo.** La mejora puede variar según el equipo.
No se ha probado esta versión en un teléfono físico. Los resultados no prometen
un FPS mínimo en todos los dispositivos.

Se añaden regresiones de teclado y multitáctil, trabajo de campo en una pasarela,
batería de Obligado sin caídas, descenso con salto doble y recogidas densas con
partículas limitadas. Se mantiene la entrega Proyecto / Windows / APK, sin iOS.

© 2026 Renzo Leporace. Todos los derechos reservados.
