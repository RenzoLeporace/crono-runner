# Registro de cambios

Todas las versiones de CRONO · Ecos del tiempo, de la más reciente a la más antigua.
Las mediciones de rendimiento son de render SDL nativo en la PC de desarrollo: no son
FPS de Android ni garantizan una frecuencia mínima en todos los dispositivos.

- [0.9.3 · en desarrollo](#093--en-desarrollo)
- [0.9.2 · misiones y rendimiento](#092--misiones-y-rendimiento)
- [0.9.1 · contenido educativo y Android](#091--contenido-educativo-y-android)
- [0.9 · épocas, rutas y skins](#09--épocas-rutas-y-skins)

---

## 0.9.3 · en desarrollo

### Guía dentro del mapa

- **Una sola tarea inmediata** en pantalla, con una señal sobre el puesto, objeto, libro,
  cristal o salida que corresponde al progreso real. Si el destino queda fuera de la vista,
  una flecha indica la dirección. La ayuda muestra una lista breve de pasos con marcas al
  completarlos.
- **PC:** el HUD del mapa usa la misma guía que Android con las teclas configuradas
  («Visita el puesto 1 · pulsa E»), marca dorada sobre el destino y barra de progreso al
  mantener E. La ayuda inicial de controles ya no queda tapada por el botón Historia.
- **Tocar E/USAR** abre un libro o puesto; **mantener E/USAR** aplica herramientas, entrega
  cargas, coordina cadenas o repara la nave, con barra y anillo de avance. **Abajo/BAJAR**
  sirve únicamente para bajar por pasarelas.
- Tarjetas grandes para puestos, lecturas y respuestas, con paginación de textos largos.
- **Lectura en voz alta** del objetivo, la lectura o las opciones, con una voz española
  instalada y sin red en Android. Si no hay voz compatible se mantienen texto y pictogramas.

### Controles y configuración

- Android: salto de 156 píxeles lógicos; PULSO, RAYO y USAR de 104 forman un arco por
  arriba y a la izquierda. El encuadre deja espacio para los pulgares sin mover plataformas.
- Escape vuelve al panel de origen y de ahí a la partida o pausa.
- Reasignar controles muestra la captura, los conflictos y la confirmación.
- Volumen persistente de música y efectos, y cambio real del tamaño de lectura.
- Impulso con recarga visible de 1,15 s, o 0,65 s con Impulso afinado.
- Las apariencias muestran «Equipado».

### Historia y exploración

- Primera Guerra (1914, Verdún, armisticio) y Segunda Guerra (Blitz, Stalingrado,
  Berlín/posguerra) en tres mapas cada una; excursión química de Ypres. **50 mapas.**
- Chernóbil reemplaza la excursión Apolo 35; la Luna (44) sigue siendo el mapa del alunizaje.
- Adversarios con uniformes humanos en épocas modernas; Berlín sin voladores; diálogo y
  armisticio sin enemigos.
- Frío activo en Deshielo, Andes, Malvinas y Stalingrado: el abrigo da autonomía, las
  hogueras y refugios recuperan calor y congelarse vuelve al inicio. La Luna usa oxígeno y
  tanque; Ypres, filtro y máscara. Son reglas de juego, no simulaciones.
- Meteoritos, ceniza y bombardeos con aviso, caída y efecto de impacto.

### Contenido educativo

- Revisión de las 1656 preguntas y actividades originales: se reemplazaron preguntas sobre
  mecánicas o rescates inventados por preguntas de historia, ciencias y análisis de fuentes.
- Banco 7 con preguntas concretas por tema y 1800 registros, conservando IDs y ediciones
  docentes. La banda menor no recibe el vocabulario de bandas superiores.
- Las referencias religiosas se tratan como patrimonio y tradición cultural.
- **Idiomas:** español y portugués de Brasil sin conexión, con variantes docentes
  independientes. Ver [docs/IDIOMAS.md](docs/IDIOMAS.md).
- Fuentes contrastadas, entre otras, de NASA, British Museum, Dirección Nacional Electoral,
  Gobierno de Mendoza y UNESCO. Catálogo completo en [FUENTES.md](FUENTES.md).

### Rendimiento

**Cuadro más liviano en Android y PC**, con los mismos píxeles: 1050 cuadros de los 50
mapas (PC 1280, Android 1281 y 1480) son idénticos a la versión anterior.

- **Interfaz táctil dibujada directamente sobre el mundo.** Antes cada cuadro borraba una capa
  de 1280×720, la componía con color clave y copiaba el mundo a la pantalla. Como sus paneles
  son opacos, ahora se dibuja encima del mundo en el orden correcto.
- **El mundo se dibuja directo en la ventana** cuando tienen el mismo tamaño y formato, lo que
  ahorra una copia de pantalla completa por cuadro en Android y en PC. La pantalla solo se
  limpia si hay franjas negras.
- **Preparación adelantada:** las plataformas, casas, módulos y monumentos que están por
  aparecer se construyen de a una por cuadro, empezando por lo más cercano, y también durante
  la presentación del mapa. Antes se construían todas juntas al entrar en una zona nueva: en
  Maguncia se encadenaban cuadros de 150, 57 y 54 ms.
- Los edificios del horizonte en los mapas argentinos son imágenes en caché: unos 500
  rectángulos por cuadro pasan a ser 12 copias.

Recorrido de 12 mapas caminando, 900 cuadros por mapa, tiempo del render en la PC de
desarrollo (no son FPS del teléfono):

| | Mediana | p95 | p99 |
| --- | ---: | ---: | ---: |
| Android 1480×720 | 3,96 → 1,65 ms (−58 %) | 8,71 → 3,56 ms (−59 %) | 18,59 → 5,06 ms (−73 %) |
| PC 1280×720 | 4,57 → 3,80 ms (−17 %) | 7,96 → 6,67 ms (−16 %) | 15,59 → 9,55 ms (−39 %) |

Jefes recibiendo daño, p95 del render a 1600×720 (`python tests/boss_stress.py`):

| Jefe | Antes | Después |
| --- | ---: | ---: |
| Primigenio | 7,178 ms | 0,104 ms |
| Medievo | 7,298 ms | 1,401 ms |
| Argentina | 6,852 ms | 0,107 ms |
| Egipto | 8,781 ms | 0,086 ms |
| Brown | 7,296 ms | 0,152 ms |
| Guerra Fría | 6,798 ms | 1,681 ms |

- Se eliminó la capa de pantalla completa que se generaba en cada cuadro al golpear un jefe.
- Plataformas indexadas por sectores para las colisiones: una escena con muchos proyectiles
  pasaba por más de 1,3 millones de comprobaciones en 240 cuadros.
- Estados invisibles de enemigos normalizados en la caché: con 36 enemigos, el p95 bajó de
  2,869 a 1,987 ms (Primigenio), 2,676 a 0,519 ms (Medievo), 1,441 a 0,698 ms (Actualidad) y
  3,123 a 0,629 ms (Argentina), con píxeles idénticos en 486 combinaciones.
- El rendimiento en teléfonos con jefes y escenas densas sigue pendiente de medición.

---

## 0.9.2 · misiones y rendimiento

- Abajo aplica herramientas y cobertura sin hacer caer a Crono de una pasarela delgada;
  para atravesarla se usa **abajo + salto**. Los saltos dobles no se consumen al bajar.
- Caché compartida de hasta 128 imágenes de enemigos, con claves por fase, salud, daño,
  aviso, dirección, facción y variante. Orbes y pulsos reutilizables y descarte de
  elementos fuera de pantalla, sin retirar enemigos ni objetos.
- Menos asignaciones al comprobar recogidas; partículas limitadas a 120 con controles
  táctiles y 240 con teclado.

Escena de 36 enemigos, 96 orbes y 36 proyectiles a 1600×720, p95 del render
(`python tests/render_stress.py`):

| Escena · ruta móvil | Antes | Después |
| --- | ---: | ---: |
| Primigenio | 17,501 ms | 3,497 ms |
| Grecia | 17,701 ms | 2,883 ms |
| Argentina | 18,491 ms | 2,849 ms |

En la ruta de escritorio: 18,767→3,117 ms, 17,142→2,843 ms y 19,544→4,142 ms.

---

## 0.9.1 · contenido educativo y Android

- **46 mapas**, nueve épocas principales y 27 mapas en su recorrido. Guerra Fría añade
  Berlín, la Luna y el diálogo de 1989–1991. La Luna no tiene enemigos ni jefe: baja
  gravedad, cráteres, tres piezas y reparación del módulo.
- Brasil incorpora la Guerra de los Farrapos; Argentina, el bonus de Güemes y la Guerra
  Gaucha. Cinco rescates abren Alejandría, Maguncia, Siracusa, Tombuctú y Bletchley Park.
- Mecánicas de época: frío y abrigo, agua y sombra, barro, esfuerzo, iluminación, vapor,
  alarmas y refugios, energía, cobertura y sincronización.
- 19 skins además de Crono, con fichas históricas, y 13 mejoras, incluida Horizonte temporal.
- Banco de 1656 preguntas y actividades en 92 archivos, con selección por edad y migración
  que conserva las ediciones docentes. Perfiles, salas LAN/WiFi y rankings de clase.
- **Android:** botones principales de 78 a 112 píxeles lógicos y acciones de 72 a 104, con
  margen lateral de 32; fondo continuo con caché por plano y redimensionado estable. Se
  instala encima de la versión anterior y conserva los datos.

---

## 0.9 · épocas, rutas y skins

- Nueva época principal **Guerra Fría** con tres mapas, incluido un desafío lunar de
  gravedad 1/6 sin enemigos.
- Siete mapas con rutas propias, dos archivos, curiosidad, aplicación física, jefe y fuentes.
- Seis skins nuevas: vestimenta gaúcha, Infernales, arriero, cartógrafo, telegrafista y
  molinero. Las comprables exigen completar su mapa.
- Horizonte temporal amplía el alcance de los disparos de 330 a 500 píxeles (nave: 540 a 800).
- Naves, reptiles marinos y víveres más detallados, dibujados a doble resolución; daño
  marítimo con sacudida, salpicaduras y protección temporal.
- Tutorial contextual que guía hasta un libro real.
- Bandera argentina con Sol de Mayo solo en contextos posteriores a su adopción.
- Banco docente en formato 5, sin sobrescribir preguntas editadas.
- Android carga únicamente el paquete necesario, con menos consultas al puente JavaScript.
- Se retira la versión iOS. Entrega fija: Proyecto, Windows y APK.

---

© 2026 Renzo Leporace. Todos los derechos reservados.
