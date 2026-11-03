# CRONO · Ecos del tiempo

<img src="tools/crono.png" alt="Ícono de CRONO, un reloj turquesa" width="112" height="112">

**Beta educativa 0.9.3 en preparación**, creada por **Renzo Leporace**. © 2026 Renzo Leporace. Todos los derechos reservados.

**CRONO** es un juego educativo de plataformas en 2D, desarrollado en Python con pygame-ce para Windows y Android. Para volver al presente, Crono debe explorar distintas épocas históricas, completar misiones y resolver archivos con preguntas sobre lo aprendido.

- **Campaña histórica** · Niveles con mecánicas propias de cada época y rutas dedicadas a Argentina y Brasil.
- **Aprendizaje adaptable** · Preguntas por edades, explicaciones de las respuestas y herramientas para que docentes editen y seleccionen contenidos.
- **Modalidades de juego** · Campaña sin conexión y salas docentes en una red local.

La publicación de GitHub sigue en **0.9.2**. La **0.9.3** está en preparación y sus compilaciones locales son de prueba. Consultá la [hoja de ruta](docs/HOJA-DE-RUTA.md) y los [cambios de la beta](docs/CAMBIOS-0.9.3.md).

**Idiomas:** Configuración → Idioma permite elegir **Español** o **Português (Brasil)** en PC y Android, sin Internet. Incluye menús, tutorial, preguntas, explicaciones, curiosidades, skins y logros. Las preguntas propias del docente conservan su texto; el editor permite guardar traducciones independientes sin reemplazar la versión española. Más información en [Idiomas](docs/IDIOMAS.md).

## Entrega y ejecución

La carpeta **Entrega contiene exactamente Proyecto, Windows y APK**. Esta estructura se mantiene en futuras entregas salvo pedido explícito de Renzo. No hay versión iOS.

Windows: abre `Windows/CRONO - Ecos del tiempo.exe` conservando `_internal` a su lado. Android: instala el APK de `APK`, Android 8 o posterior, en horizontal. El APK incluye su motor y recursos sin requerir Internet al jugar. Los enlaces a fuentes se abren solo cuando los eliges.

### Ejecutar desde el código fuente

Desde la raíz del repositorio o la carpeta `Proyecto` de una entrega:

```sh
python -m pip install -r requirements.txt
python Main.py
```

En Windows también podés usar `Jugar.bat`. Los datos de alumnos y los bancos particulares quedan fuera de las entregas.

## Campaña, países y bonus

Hay **50 mapas**: 30 de campaña principal, cuatro rutas principales argentinas, tres bonus argentinos, Farrapos en Brasil, ocho bonus del juego base por rescates y cuatro grietas históricas. Además existen tres travesías acuáticas separadas, con regreso a su mapa de origen.

Las diez épocas principales son Primigenio, Deshielo, Egipto, Grecia, Medievo, Industria, Primera Guerra Mundial, Segunda Guerra Mundial, Guerra Fría y Actualidad. Argentina incluye 1810, 1816, Obligado y recuperación democrática; San Martín abre los Andes y Brown su ruta naval. Güemes se habilita al completar 1816. Brasil comienza con la Guerra de los Farrapos, 1835–1845.

Los cinco bonus nuevos del juego base se abren mediante rescates ficticios: bibliotecaria en el templo egipcio → Alejandría; aprendiz en el mercado medieval → Maguncia; aprendiz del equilibrio en Olimpia → Siracusa; guardiana en el molino medieval → Tombuctú; analista en el mapa londinense del Blitz → Bletchley Park. Estas conexiones del reloj distinguen fechas y regiones; no afirman que el rescate sucediera históricamente.

Cada mapa tiene 48 ecos, dos archivos, tres fragmentos, una curiosidad específica y un trabajo de campo físico. Los nuevos trabajos incluyen transportar provisiones, ordenar un catálogo al regresar, imprimir una página, usar palancas, acompañar una custodia y leer señales con el momento correcto.

La Guerra Fría se integra entre Guerras Mundiales y Actualidad, con Berlín, la Luna y el diálogo de 1989–1991. El mapa lunar no tiene enemigos ni jefe de combate: exige cruzar cráteres de hasta 510 píxeles, usar la baja gravedad y la inercia, recuperar tres piezas y reparar el módulo ficticio de Crono. Conserva los archivos históricos y los fragmentos. Los saltos usan aceleración de 1/6 y un impulso de traje ajustado para jugar, no una simulación física completa.

## Mecánicas de época

| Época | Efecto sobre el juego |
| --- | --- |
| Primigenio | El barro reduce la marcha; saltar y usar pasarelas ayuda. |
| Deshielo | El frío llena una barra y puede congelarte. El abrigo se encuentra más adelante y ralentiza la pérdida de calor; las hogueras y refugios permiten recuperarlo. |
| Egipto | El agua disminuye en el trayecto; pozos y sombra la reponen. |
| Grecia | Los impulsos consumen esfuerzo; el descanso facilita la recuperación. |
| Medievo | La lámpara amplía la zona iluminada y se recarga junto a faroles. La geometría lejana sigue visible. |
| Industria | Rejillas anunciadas expulsan vapor: hay que esperar o rodearlas. |
| Guerras | Las alarmas anticipan impactos; busca los refugios marcados. |
| Guerra Fría | Sincronización de antenas; en la Luna, gravedad reducida, aterrizajes de precisión y reparación sin combate. |
| Actualidad | Las placas energéticas recargan el impulso incluso en el aire. |
| Rutas argentinas y Brasil | Mantener E junto a parapetos proporciona cobertura. Las misiones particulares añaden logística, comunicaciones y otras acciones. |

El tutorial enseña cinco acciones. En su última etapa señala un libro abierto y solo pide interactuar al estar cerca. Una caja de preparación y un puesto de registro no son grietas: únicamente la entrada marítima del segundo puesto abre la navegación.

## Aprender, mejorar y personalizar

El banco incluye **1800 registros de preguntas en 100 archivos**, tres edades y selección aleatoria con respuestas mezcladas. Las preguntas tratan contenidos concretos, sin plantillas que cambian únicamente el título. El total incluye reutilización entre edades: no son 1800 preguntas ni hechos diferentes. Se filtra el vocabulario original avanzado para la banda menor y se conservan las elecciones docentes. Una curiosidad leída se pregunta en el segundo archivo, más adelante. Los errores dan explicaciones sin quitar energía. Las primeras respuestas dan saber para **13 mejoras**; la misión y los archivos también suman puntuación y premios únicos.

Los ecos permiten comprar apariencias. Hay **19 skins además de Crono**, contando la de Cronista obtenida por logros. Las 18 comprables se habilitan al terminar su mapa asociado, indicado en cada ficha. No se pierden las compras de partidas anteriores. Seis nuevas visten a Crono como gaúcho, Infernal, arriero, cartógrafo, telegrafista y molinero. Las fichas explican contexto y límites de la representación.

Los **60 logros** conservan el premio final Reloj del Cronista: energía máxima adicional y mayor atracción, desactivable. Las edades 6–9, 10–14 y 15+ ajustan preguntas y dificultad; Accesibilidad permite elegir asistencia motriz por separado. Hay todas las anclas en mínima, cuatro en media y dos en alta. La práctica docente muestra mapas, habilidades y skins sin consumir monedas ni alterar rankings reales.

## Docentes y salas

Configuración → Zona docente permite ver preguntas y respuestas, añadir, editar, duplicar, importar, exportar y seleccionar contenidos. El banco formato 7 conserva las ediciones antiguas al añadir los temas nuevos. Hay perfiles con alias, clase e institución, exportación CSV de respuestas y justificaciones, PIN docente opcional y dos rankings locales: clase e institución.

El docente aloja una sala desde Windows; los dispositivos Windows y Android de la misma LAN/WiFi se unen mediante IP, puerto y código. La red debe permitir comunicación entre dispositivos. El juego no modifica el firewall. La sala usa HTTP en una red de confianza y no tiene ranking global ni protección antitrampas. [Guía docente](docs/GUIA-DOCENTE.md).

## Controles y desarrollo

A/D o flechas: mover; Espacio: salto; Shift: impulso; F: disparo; tocar E: abrir libros y puestos; mantener E: herramientas, cobertura y trabajo de la misión; abajo: bajar por pasarelas; H: ayuda; U/C: mejoras/cuaderno; Esc: pausa. En Android, SALTAR es el botón principal de 156 píxeles. PULSO, RAYO y USAR mantienen su tamaño y orbitan por arriba y por la izquierda. BAJAR sirve solo para bajar.

El mapa muestra una sola tarea inmediata, una señal hacia su destino y progreso visible al mantener USAR. El altavoz lee objetivos y preguntas si Android dispone de una voz española instalada sin red. La lectura y las respuestas usan tarjetas grandes. Los jefes reutilizan imágenes locales y conservan sus avisos y reacciones de daño. [Detalle de interfaz, contenido y mediciones](docs/CAMBIOS-0.9.3.md).

El pulso base tiene alcance corto. Horizonte temporal amplía Crono de 330 a 500 píxeles y la nave de 540 a 800; siguen teniendo límite. El sonido incluye nueve composiciones originales y 17 efectos. La representación visual es original e ilustrativa; las misiones no sustituyen las fuentes.

Pruebas: `python -m unittest discover -s tests`. Windows: `tools/build_beta.py` y `tools/package_beta.py`. Android: `tools/prepare_android.py` y `tools/build_android.py`, con SDK 34 y JDK 17. Entrega: `tools/create_delivery.py`. El contenedor web intermedio no es el APK instalable.

[Novedades de la entrega](docs/CAMBIOS-0.9.3.md) · [Contenido 0.9](docs/CAMBIOS-0.9.md) · [Fuentes](FUENTES.md) · [Verificación](VERIFICACION.md) · [Licencias](LICENCIAS.txt) · [Derechos](COPYRIGHT.txt).

Cambios del 27 de octubre: Primera Guerra (1914, Verdún, armisticio), Segunda Guerra (Blitz, Stalingrado, Berlín/posguerra), excursión química de Ypres y Chernóbil en lugar de repetir Apolo 11. Luna conserva su mapa propio y ahora incorpora oxígeno y tanque de reserva. Frío y abrigo también aparecen en Andes, Malvinas y Stalingrado. [Detalle](docs/CAMBIOS-2026-10-27.md).
