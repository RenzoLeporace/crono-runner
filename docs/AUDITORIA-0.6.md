# Auditoría independiente · CRONO 0.6

24 de octubre de 2026. Informe del subagente `auditoria_beta`, solicitado por el usuario. El agente principal corrigió los dos defectos detectados. Esta revisión corresponde al código fuente y a sus capturas; la validación posterior del ejecutable se detalla en `VERIFICACION.md`.

## Dictamen y alcance

La versión revisada permite una beta jugable y una prueba educativa supervisada. El subagente no encontró fallos P0 o P1 ni otro bloqueo reproducible. Todavía requiere partidas humanas completas para validar equilibrio y sesiones docentes para valorar aprendizaje.

Revisó progresión, guardado, física, combate, banco docente, interfaz, referencias culturales y renderizado. Inspeccionó los montajes de los 21 escenarios renovados, nueve distritos argentinos, Egipto, humanoides y patrimonio, además de capturas individuales de extinción, ciudad medieval, Luján, Moisés y edición docente.

Ejecutó independientemente la suite entonces existente de **86 pruebas**, todas correctas, y después las **11 pruebas de rework** con la nueva regresión de autoguardado, todas correctas: **87 pruebas únicas**. También reprodujo el fallo de autoguardado y realizó sondeos de combate con controles automáticos simplificados. Esos sondeos no certifican equilibrio humano. No jugó la campaña completa ni probó un mando físico.

## Fallos comprobados y corregidos

### P2 · Autoguardado después de completar un mapa

En `Game.update`, completar un mapa cuando el contador de autoguardado superaba 15 segundos hacía que `save.completed` avanzara el mapa, pero una captura posterior volviera a guardar el mundo terminado. Reproducción: entrar al mapa inicial, reunir los fragmentos, colocar a Crono en el portal, poner `autosave=15.01` y actualizar un paso. Se observaba `current=0`, `unlocked=1`, `progress` presente, en lugar de `current=1`, `progress=None`.

**Corregido:** el guardado periódico solo captura cuando el estado sigue siendo `play`. Regresión: `test_autosave_does_not_capture_an_already_completed_map`.

### P2 · Armadura humanoide poco legible

La guía decía “evita sus púas”, pero los humanoides no mostraban esas púas. Egipcios y medievales acorazados eran demasiado similares a los normales, aunque pisarlos daña a Crono.

**Corregido:** explicación explícita de que no se pueden pisar, distintivo de escudo y equipamiento adicional en egipcios, medievales y griegos. El subagente confirmó los cambios en código.

## Evaluación visual

- **Argentina:** Cabildo, Recova, Casa de Tucumán y Congreso son hitos reconocibles. Tejas, rejas, balcones, carteles, macetas y mobiliario aportan variedad más allá del color.
- **Mapas anteriores:** extinción comunica destrucción mediante árboles quemados, humo, meteoros y cráter; el Medievo incorpora entramados, mercado y arquitectura religiosa; Industria presenta instalaciones y materiales propios.
- **Egipto:** se distinguen cultivos y navegación, Guiza y templos. Los textos separan períodos y no presentan todos los monumentos como simultáneos.
- **Humanoides:** equipo y proporciones encajan con Crono. Conservar animales, vehículos y drones mantiene variedad.
- **Patrimonio:** Luján e Itatí tienen representaciones distintas. Moisés es una referencia cultural del relato bíblico, sin fecha arqueológica segura ni papel de enemigo.

Mejoras propuestas: reforzar el contraste entre plataformas y tejados o vigas de luminosidad similar; ofrecer texto ajustable para notebooks y proyectores; incorporar acontecimientos visuales entre hitos para reducir repetición modular. Las figuras son interpretaciones estilizadas, no reconstrucciones documentales exactas.

## Jugabilidad

La secuencia principal `0 → 1 → 8 → 2 → 3 → 4 → 5 → 6` respeta el orden cronológico, mientras Argentina mantiene progreso independiente. Las pruebas verifican Egipto, regreso a Grecia, fronteras de desbloqueo, migraciones y persistencia de campañas separadas.

Los sondeos de salto usan física y colisiones reales. Los humanoides tienen cuerpos más altos con apoyo en la superficie original; el pisotón funciona donde corresponde. Las lecturas y visitas culturales pausan la acción.

Los nueve jefes pasan la prueba de derrota en dificultad mínima sin mejoras. La prueba prepara la arena y aplica una estrategia concreta; no demuestra que un principiante la descubra ni acredita una campaña completa. Los perfiles mayores aún requieren equilibrio con personas.

Prioridades sugeridas:

1. Probar los tres perfiles con personas y registrar muertes, duración, abandono y ataques mal comprendidos.
2. Introducir cada conducta en un encuentro breve antes de mezclar enemigos y precipicios.
3. Alternar exploración, combate y descanso para dar ritmo a las rutas largas.
4. Añadir actividades propias de cada mapa: canales, señales ferroviarias o reconstrucción de archivos.
5. Incorporar momentos narrativos y personajes civiles que den propósito al viaje.

## Uso en instituciones educativas

Antes de una experiencia institucional formal:

- Asociar cada archivo con objetivos del curso y someter contenidos a revisión docente, especialmente dictadura, organizaciones armadas, terrorismo de Estado y tradiciones religiosas.
- Mantener la distinción de 1983 como recuperación democrática y de los enemigos como ecos ficticios del período previo.
- Incorporar tamaño de texto ajustable, controles reasignables y desplazamiento de lecturas con teclado; la rueda del ratón limita algunas configuraciones.
- Separar alumnos mediante perfiles o carpetas: actualmente existe una partida local compartida por instalación.
- Considerar que el editor revela respuestas y permite modificarlas. Sirve para enseñanza supervisada; no garantiza integridad de una evaluación individual.
- Preparar sesiones de 15–25 minutos con objetivos concretos, sin exigir completar la campaña.

Funciones futuras, priorizadas por el subagente:

1. **Evidencia de aprendizaje:** registrar intentos, primera respuesta, correcciones y repasos. “Archivo resuelto” solo demuestra que alguna vez se eligió la respuesta correcta.
2. **Informe docente local:** exportación CSV por alias, tema y sesión, sin cuentas ni conexión.
3. **Variedad por tema:** ampliar las dos preguntas iniciales por perfil y archivo a cinco u ocho, con distractores más plausibles.
4. **Aplicación:** ordenar hechos, contrastar fuentes, interpretar imágenes y justificar decisiones.
5. **Acompañamiento:** separar edad del contenido y asistencia motriz; habilidad lectora y destreza en plataformas no avanzan necesariamente juntas.
6. **Gestión docente:** importar y exportar bancos desde la interfaz, revisar previamente, seleccionar temas y bloquear opcionalmente la edición.
7. **Privacidad:** mantener el funcionamiento local, usar alias y explicar guardado, exportación y eliminación.

Las referencias a Luján, Itatí y Moisés tienen encuadre cultural explícito y visitas opcionales. Una guía pedagógica puede abordarlas desde patrimonio, historia del arte y diversidad de tradiciones.

La inversión siguiente de mayor valor es una prueba humana observada y revisión curricular docente. Las pruebas automáticas no demuestran por sí solas equilibrio, accesibilidad ni eficacia educativa.

## Addendum · Anclas por dificultad

El usuario solicitó posteriormente reducir anclas al aumentar dificultad. El subagente revisó selección, activación, guardado, restauración, dibujo y atlas; ejecutó las **13 pruebas actualizadas de rework**, todas correctas. La suite total pasa a **89 pruebas únicas**.

Comprobó mínima con todas las anclas, media con cuatro y máxima con dos en los 27 mapas; las retiradas no se activan, se conserva la última antes del jefe y el cambio de perfil o restauración selecciona una anterior válida sin mover los IDs. No encontró fallos reproducibles. La repetición de trayectos al morir aumenta; su duración aún requiere pruebas con jugadores.

## Revisión final del ejecutable y paquete

El subagente inspeccionó las capturas generadas por el ejecutable del jefe egipcio, Luján, Itatí, Moisés y el editor egipcio. No observó defectos materiales: los textos y controles caben, Egipto aparece como capítulo 3 y se conserva el contexto de las referencias culturales.

Comprobó un ZIP de 144 archivos y 19,84 MiB, con integridad correcta, ejecutable idéntico al de la raíz, documentación 0.6 y dependencias presentes. Confirmó ausencia de partidas, bancos personalizados y `.git`. La comprobación confirma presentación y empaquetado; no sustituye los ensayos humanos y docentes indicados arriba.
