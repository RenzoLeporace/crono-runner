# Beta 0.9.3 · guía dentro del mapa e historia real

## Jugar desde el celular

El salto pasa de 112 a 156 píxeles lógicos. PULSO, RAYO y USAR conservan sus
104 píxeles y forman un arco por arriba y por la izquierda del salto. Todos
tienen icono, nombre y margen del borde. El encuadre deja espacio para los
pulgares al comienzo y final del recorrido, sin mover plataformas ni cambiar
las colisiones.

Dentro del mapa se muestra una sola tarea inmediata. La señal indica el puesto,
objeto, libro, cristal o salida que corresponde al progreso real. Si queda fuera
de la zona visible libre de controles, una flecha indica la dirección. Las manos
y libros señalados también admiten toque directo. La ayuda muestra una lista
breve de pasos, con marcas al completarlos.

**Tocar E/USAR** abre un libro o puesto. **Mantener E/USAR** aplica herramientas,
entrega cargas, coordina cadenas o repara la nave. Una barra y un anillo muestran
el avance; soltar o alejarse interrumpe la pulsación. **Abajo/BAJAR** vuelve a
servir únicamente para bajar por pasarelas, sin combinación con salto. Las
teclas personalizadas se conservan.

Los puestos, la lectura y las respuestas usan tarjetas grandes. Los textos
largos se dividen en páginas. La primera lectura muestra el contenido histórico
del tema; una explicación personalizada por un docente tiene prioridad. Los
mensajes de misión ya no exigen leer a la vez el plano, varios contadores y
descripciones pequeñas. Se conservan aula, mejoras, cuaderno y demás funciones.

Un altavoz permite escuchar el objetivo, la lectura o las opciones de una
pregunta. Usa una voz española instalada y disponible sin red en Android. El
motor se inicia al solicitarlo; no descarga voces. Si no hay una voz compatible,
se mantienen el texto y los pictogramas. Esta función aún necesita prueba en un
teléfono físico.

## Rendimiento de jefes

Se eliminó la capa de pantalla completa y su máscara, que se generaban cada
cuadro al golpear un jefe. Los cuerpos y destellos usan imágenes locales
recortadas, con caché limitada a 128 entradas. Reacciones, retroceso, daño,
derrota y avisos de ataque se conservan. Los avisos se dibujan por separado para
que no queden congelados. También se reutilizan los efectos de las naves.

`python tests/boss_stress.py --output resultado.json` mide solo el render del
jefe, con 60 cuadros de calentamiento y 180 muestras por caso a 1600×720:

| Jefe recibiendo daño · p95 | Antes | Después |
| --- | ---: | ---: |
| Primigenio | 7,178 ms | 0,104 ms |
| Medievo | 7,298 ms | 1,401 ms |
| Argentina | 6,852 ms | 0,107 ms |
| Egipto | 8,781 ms | 0,086 ms |
| Brown | 7,296 ms | 0,152 ms |
| Guerra Fría | 6,798 ms | 1,681 ms |

Son mediciones de SDL nativo en la PC de desarrollo, no FPS de Android ni del
juego completo. No garantizan una frecuencia mínima en todos los celulares.

## Contenido educativo

Se revisaron las 1656 preguntas y actividades originales, las decisiones
marítimas y las fichas culturales e históricas de apariencias. Se sustituyeron
preguntas sobre Crono, rescates inventados, pantallas o mecánicas por preguntas
de historia, ciencias y análisis de fuentes. Las lecturas no presentan la
aventura como evidencia histórica. Los objetos tienen nombres reconocibles,
como ánfora, papiro, motor de Newcomen o muestra lunar.

Las referencias religiosas se estudian como patrimonio y tradición cultural.
Por ejemplo, el episodio de Moisés se relaciona con el relato bíblico y su
representación artística documentada, sin convertirlo en una inscripción
egipcia ni asignarle una fecha arqueológica demostrada.

El banco usa formato 6. Las preguntas originales sin editar se actualizan
mediante sus huellas de contenido; las modificadas o añadidas por docentes se
conservan. No cambian IDs, compras, logros ni partidas.

Entre las fuentes contrastadas están [NASA · Apollo 11](https://www.nasa.gov/mission/apollo-11/),
[British Museum · estampa de 1533](https://www.britishmuseum.org/collection/object/P_1875-0710-270),
[Dirección Nacional Electoral · 1983](https://www.argentina.gob.ar/dine/elecciones-1983),
[Gobierno de Mendoza · Ejército de los Andes](https://www.mendoza.gov.ar/prensa/se-conmemoro-el-dia-de-la-bandera-provincial/)
y [UNESCO · Tombuctú](https://whc.unesco.org/en/list/119/). El catálogo por tema
está en FUENTES.md.

La entrega mantiene exclusivamente Proyecto / Windows / APK. © 2026 Renzo Leporace.
