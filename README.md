# CRONO · Ecos del tiempo

**Beta educativa 0.9.1**, creada por **Renzo Leporace**. © 2026 Renzo Leporace. Todos los derechos reservados.

Crono viaja por el pasado para volver al presente. Explorar, comprender archivos y aplicar lo aprendido forman parte del avance: cada salida exige tres fragmentos, una misión contextual completa y al menos un archivo resuelto; en los mapas de cierre también hay que liberar un guardián ficticio.

## Entrega y ejecución

La carpeta **Entrega contiene exactamente Proyecto, Windows y APK**. Esta estructura se mantiene en futuras entregas salvo pedido explícito de Renzo. No hay versión iOS.

Windows: abre `Windows/CRONO - Ecos del tiempo.exe` conservando `_internal` a su lado. Android: instala el APK de `APK`, Android 8 o posterior, en horizontal. El APK incluye su motor y recursos sin requerir Internet al jugar. Los enlaces a fuentes se abren solo cuando los eliges.

Proyecto incluye las fuentes para continuar el desarrollo. Instala `requirements.txt` con Python y ejecuta `Main.py`; `Jugar.bat` también permite iniciar desde fuente. Los datos de alumnos y bancos particulares no se distribuyen.

## Campaña, países y bonus

Hay **46 mapas**: 27 de campaña principal, cuatro rutas principales argentinas, tres bonus argentinos, Farrapos en Brasil, ocho bonus del juego base por rescates y tres grietas históricas. Además existen tres travesías acuáticas separadas, con regreso a su mapa de origen.

Las nueve épocas principales son Primigenio, Deshielo, Egipto, Grecia, Medievo, Industria, Guerras Mundiales, Guerra Fría y Actualidad. Argentina incluye 1810, 1816, Obligado y recuperación democrática; San Martín abre los Andes y Brown su ruta naval. Güemes se habilita al completar 1816. Brasil comienza con la Guerra de los Farrapos, 1835–1845.

Los cinco bonus nuevos del juego base se abren mediante rescates ficticios: bibliotecaria en el templo egipcio → Alejandría; aprendiz en el mercado medieval → Maguncia; aprendiz del equilibrio en Olimpia → Siracusa; guardiana en el molino medieval → Tombuctú; analista en el mapa de refugios de 1939 → Bletchley Park. Estas conexiones del reloj distinguen fechas y regiones; no afirman que el rescate sucediera históricamente.

Cada mapa tiene 48 ecos, dos archivos, tres fragmentos, una curiosidad específica y un trabajo de campo físico. Los nuevos trabajos incluyen transportar provisiones, ordenar un catálogo al regresar, imprimir una página, usar palancas, acompañar una custodia y leer señales con el momento correcto.

La Guerra Fría se integra entre Guerras Mundiales y Actualidad, con Berlín, la Luna y el diálogo de 1989–1991. El mapa lunar no tiene enemigos ni jefe de combate: exige cruzar cráteres de hasta 510 píxeles, usar la baja gravedad y la inercia, recuperar tres piezas y reparar el módulo ficticio de Crono. Conserva los archivos históricos y los fragmentos. Los saltos usan aceleración de 1/6 y un impulso de traje ajustado para jugar, no una simulación física completa.

## Mecánicas de época

| Época | Efecto sobre el juego |
| --- | --- |
| Primigenio | El barro reduce la marcha; saltar y usar pasarelas ayuda. |
| Deshielo | Recoge el abrigo de la primera posta. Sin él, el frío termina quitando energía; los refugios protegen. |
| Egipto | El agua disminuye en el trayecto; pozos y sombra la reponen. |
| Grecia | Los impulsos consumen esfuerzo; el descanso facilita la recuperación. |
| Medievo | La lámpara amplía la zona iluminada y se recarga junto a faroles. La geometría lejana sigue visible. |
| Industria | Rejillas anunciadas expulsan vapor: hay que esperar o rodearlas. |
| Guerras | Las alarmas anticipan impactos; busca los refugios marcados. |
| Guerra Fría | Sincronización de antenas; en la Luna, gravedad reducida, aterrizajes de precisión y reparación sin combate. |
| Actualidad | Las placas energéticas recargan el impulso incluso en el aire. |
| Rutas argentinas y Brasil | Mantener abajo junto a parapetos proporciona cobertura. Las misiones particulares añaden logística, comunicaciones y otras acciones. |

El tutorial enseña cinco acciones. En su última etapa señala un libro abierto y solo pide interactuar al estar cerca. Una caja de preparación y un puesto de registro no son grietas: únicamente la entrada marítima del segundo puesto abre la navegación.

## Aprender, mejorar y personalizar

El banco incluye **1656 preguntas y actividades en 92 archivos**, tres edades y selección aleatoria con respuestas mezcladas. Incluye preguntas factuales y tareas de fuentes, imágenes, razonamiento y cronología; no son 1656 hechos diferentes. Los errores dan explicaciones sin quitar energía. Las primeras respuestas dan saber para **13 mejoras**; la misión y los archivos también suman puntuación y premios únicos.

Los ecos permiten comprar apariencias. Hay **19 skins además de Crono**, contando la de Cronista obtenida por logros. Las 18 comprables se habilitan al terminar su mapa asociado, indicado en cada ficha. No se pierden las compras de partidas anteriores. Seis nuevas visten a Crono como gaúcho, Infernal, arriero, cartógrafo, telegrafista y molinero. Las fichas explican contexto y límites de la representación.

Los **60 logros** conservan el premio final Reloj del Cronista: energía máxima adicional y mayor atracción, desactivable. Las edades 6–9, 10–14 y 15+ ajustan preguntas y dificultad; Accesibilidad permite elegir asistencia motriz por separado. Hay todas las anclas en mínima, cuatro en media y dos en alta. La práctica docente muestra mapas, habilidades y skins sin consumir monedas ni alterar rankings reales.

## Docentes y salas

Configuración → Zona docente permite ver preguntas y respuestas, añadir, editar, duplicar, importar, exportar y seleccionar contenidos. El banco formato 5 conserva las ediciones antiguas al añadir los temas nuevos. Hay perfiles con alias, clase e institución, exportación CSV de respuestas y justificaciones, PIN docente opcional y dos rankings locales: clase e institución.

El docente aloja una sala desde Windows; los dispositivos Windows y Android de la misma LAN/WiFi se unen mediante IP, puerto y código. La red debe permitir comunicación entre dispositivos. El juego no modifica el firewall. La sala usa HTTP en una red de confianza y no tiene ranking global ni protección antitrampas. [Guía docente](docs/GUIA-DOCENTE.md).

## Controles y desarrollo

A/D o flechas: mover; Espacio: salto; Shift: impulso; F: disparo; E: interactuar; abajo: bajar, cubrirse o aplicar herramientas; H: misión histórica; U/C: mejoras/cuaderno; Esc: pausa. En Android hay controles táctiles ampliados aproximadamente un 44%, con iconos mayores, separados entre sí y con margen lateral de 32 píxeles lógicos. El ancho de cámara se adapta mostrando más mapa y conservando proporciones. El cielo y los distintos planos del fondo se desplazan de forma continua, sin reconstrucciones por tramos.

El pulso base tiene alcance corto. Horizonte temporal amplía Crono de 330 a 500 píxeles y la nave de 540 a 800; siguen teniendo límite. El sonido incluye nueve composiciones originales y 17 efectos. La representación visual es original e ilustrativa; las misiones no sustituyen las fuentes.

Pruebas: `python -m unittest discover -s tests`. Windows: `tools/build_beta.py` y `tools/package_beta.py`. Android: `tools/prepare_android.py` y `tools/build_android.py`, con SDK 34 y JDK 17. Entrega: `tools/create_delivery.py`. El contenedor web intermedio no es el APK instalable.

[Novedades de la entrega](docs/CAMBIOS-0.9.1.md) · [Contenido 0.9](docs/CAMBIOS-0.9.md) · [Fuentes](FUENTES.md) · [Verificación](VERIFICACION.md) · [Licencias](LICENCIAS.txt) · [Derechos](COPYRIGHT.txt).
