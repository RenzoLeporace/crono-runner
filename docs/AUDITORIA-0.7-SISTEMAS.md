# Auditoría de sistemas y aula — CRONO 0.7

Auditor independiente: `auditoria_exigente`, segundo subagente solicitado por el usuario. Esta revisión complementa la auditoría visual y jugable de `auditoria_beta`. El agente principal implementó las correcciones; este auditor reprodujo fallos y verificó cambios sin modificar las fuentes del producto.

## Dictamen y alcance

**La fuente revisada es apta para generar y verificar candidatos de distribución. No quedan bloqueos reproducidos de esta auditoría pendientes de corregir.** La validación del APK instalado y sus funciones nativas constituye una etapa posterior, a cargo del agente principal. Este documento distingue las pruebas de fuente de las comprobaciones realizadas en Android.

Se revisaron campañas, guardados, preguntas, perfiles, práctica docente, puntuación, rankings, salas LAN, actividades, recompensas y el puente Android. Se utilizaron eventos Pygame, física real, llamadas de interfaz y conexiones HTTP locales. Algunos ensayos preparan posiciones, retiran enemigos o sustituyen el puente nativo por un simulador para aislar una condición; no representan partidas humanas completas.

## Progreso y persistencia: fallos corregidos

| Problema reproducido | Efecto | Corrección verificada |
| --- | --- | --- |
| La práctica consumía orbes, curiosidades y rescates del progreso normal. | El alumno perdía recompensas después de una prueba docente; también avanzaban fronteras de campaña. | Práctica separa registros y excluye monedas, desbloqueos, aprendizaje permanente y logros normales. |
| Salir de práctica conservaba un bonus bloqueado o una apariencia sin comprar. | La siguiente partida podía puntuar en un mapa aún inaccesible. | Se restaura un mapa permitido y la apariencia válida. El docente puede probar también el beneficio del Cronista. |
| Cambiar o eliminar un perfil dejaba un mundo anterior activo al cerrar. | Podía copiarse progreso entre alumnos. | Activar un perfil reinicia mundo y sesión; borrar y cerrar conserva el reemplazo y los otros perfiles. |
| Completar una grieta y volver al menú reiniciaba la excursión. | Había que repetirla para regresar al origen. | La finalización pendiente se conserva y continuar vuelve al origen, también desde el DLC. |
| Una repetición inferior alteraba los orbes del mejor registro. | Puntaje, tiempo y desglose dejaban de describir una misma partida. | El mejor registro se mantiene completo; los acumulados tienen almacenamiento independiente. |
| El logro del duelo contaba muertes anteriores al jefe o reiniciaba su referencia al morir. | No coincidía con su descripción. | Se conserva la referencia de la primera activación del encuentro, incluso tras reaparecer y guardar/cargar. |
| Valores anidados malformados provocaban excepciones. | Un archivo de progreso, perfiles o sala parcialmente inválido podía cerrar el juego. | Se normalizan contadores, listas, subprogresos, registros y metadatos con valores predeterminados. |

La suite de 109 pruebas encontró una compra que devolvía éxito pero no sobrevivía a recarga. Un ensayo independiente reprodujo una pérdida en 100 ciclos y registró `PermissionError(13, Acceso denegado)` en `os.replace`, dentro de esta carpeta OneDrive. El disco conservaba únicamente `vitality` y 17 puntos, aunque la memoria ya tenía `vitality2`.

La corrección `storage.atomic_replace` reintenta brevemente solo ante ese error. Se aplica a progreso, perfiles, banco e importación. Si el bloqueo persiste, conserva el archivo anterior y el temporal y comunica la advertencia. Después del cambio, los 100 ciclos de compra y recarga fueron correctos. Hay regresiones para bloqueo transitorio y persistente.

## Aula y salas: fallos corregidos

| Problema reproducido | Corrección verificada |
| --- | --- |
| El banco anterior quedaba ignorado al añadir temas. | La migración conserva personalizaciones e incorpora el currículo nuevo sin sustituir sus identificadores. |
| Reingresar añadía otra fila para el mismo alumno. | Se conserva el token por perfil y dirección; reconectar mantiene el mismo miembro. |
| Una conexión iniciada por A podía terminar aplicada al perfil B. | El trabajo de red no modifica el juego desde el hilo secundario; el resultado solo se aplica al perfil que lo inició. |
| Banco y temario de una sala quedaban activos en otro perfil. | Cambiar de alumno limpia cliente, preguntas, temas e información compartida anteriores. |
| La selección docente o las ediciones no llegaban al alumno. | La sala actualiza preguntas y temas; sincronizar recupera la actividad y se aplica al cargar el mapa. |
| Restaurar una sala ignoraba el temario local mientras llegaba la red. | Se distingue temario desconocido de “todos”; se usa el local como respaldo y se actualiza la sesión de forma asíncrona. |
| El anfitrión veía solo perfiles locales. | Consulta miembros de su sala mediante una copia protegida frente a escrituras concurrentes. |
| Los IDs `0`, `00` y `000` sumaban un mapa tres veces. | Se normalizan identificadores y se rechazan duplicados. |
| Un código no ASCII cortaba la conexión. | Se valida el código y se devuelve un error legible. |
| Cuentas docentes aparecían en rankings de alumnos. | El rol docente queda excluido del envío puntuable y de los rankings locales y LAN. |
| La práctica consumía el primer intento educativo del alumno. | Primera respuesta se calcula por separado para práctica y modo normal. |
| El informe guardaba solo el índice de una respuesta barajada. | Conserva pregunta, texto elegido y correcto, contexto de práctica y reflexiones; el CSV permite reconstruir el intento. |

La prueba HTTP utilizó cuatro alumnos concurrentes, dos clases y dos instituciones. Se comprobaron filtros, mejores registros, exclusión de práctica, reconexión y reinicio del servidor. Una prueba con `Game` real recuperó al arrancar una pregunta personalizada y recibió después una segunda versión del banco y otro temario. Una cuenta docente fue rechazada al enviar puntuación y no apareció en el ranking.

El PIN limita acceso a menús; no cifra los archivos del equipo. Los rankings acompañan el trabajo del aula y no constituyen por sí solos una evaluación certificada.

## Actividades, controles y recompensas

- Las 36 actividades se ejercitaron con `World.update`: objetos, elevadores y pasarelas, acompañamiento, refugios, balizas y vehículos. Las 36 guardan y restauran su finalización y no repiten recompensa al guardar otra vez.
- Se comprobó retorno de una grieta a coordenadas y energía exactas, conservando fragmentos, orbes, enemigo derrotado y actividad del origen. Repetirla no duplica su premio.
- Dirección y salto funcionan con dos dedos independientes; soltar dirección conserva salto. La reasignación rechaza teclas ocupadas.
- La navegación cambia orientación y disparo. Montar un vehículo no deja un impulso congelado.
- Las pantallas y el bestiario de los 36 mapas se generan sin las excepciones de índices detectadas inicialmente. El selector docente se adaptó al número de mapas.
- El catálogo contiene 60 logros. El premio final añade una unidad de energía máxima y 60 píxeles de alcance de atracción y puede desactivarse. Las apariencias incluyen fichas históricas.
- El banco contiene 1.296 ítems: 72 temas, tres perfiles de edad y seis variantes por combinación, con actividades factuales, de fuentes, imagen, razonamiento y cronología. La variedad de formato no demuestra por sí sola eficacia pedagógica.

## Puente Android y hallazgos del APK candidato

Se revisaron `mobile.py`, la entrada asíncrona, `MainActivity.java` y el manifest. El wrapper sirve juego y runtime desde assets empaquetados, acota archivos privados por prefijo y ruta canónica y abre fuentes externas mediante el sistema. Android se une a una sala creada en la PC docente.

La revisión encontró archivos docentes que solo existían en el sistema virtual. Se incorporó persistencia de respaldos y selección nativa de documentos para importar bancos y exportar banco/CSV. También se corrigieron:

- Importación con BOM UTF-8 y conservación del BOM del CSV exportado.
- Descarte de la vista previa anterior si la siguiente importación falla o se cancela; límite de 10.000 preguntas.
- Límites coherentes en bytes para lectura y escritura. Los archivos privados admiten hasta 32 MiB; al arrancar se cargan metadatos y los perfiles/bancos se recuperan bajo demanda, sin reconstruir todos los respaldos.
- Respuestas de sala de hasta 8 MB para bancos personalizados admitidos; las peticiones siguen acotadas a 2 MB.

Durante la verificación del APK real, el agente principal encontró un defecto que los simuladores anteriores no reprodujeron: el transporte Python–Java deformaba caracteres. Por ejemplo, “institución” se convertía en “instituciÃ³n”, y sucesivas cargas podían repetir la corrupción.

El parche transporta contenido de archivos, texto inicial del editor, exportaciones y URLs como UTF-8 codificado en Base64 ASCII. Los JSON de respuestas y metadatos utilizan escapes ASCII y conservan también caracteres suplementarios como emoji. Se añadió una regresión con transporte deliberadamente alterado como Latin-1. Los simuladores independientes se actualizaron al contrato y siguieron pasando.

El principal encontró además que un toque abría dos editores nativos: SDL emitía un evento de ratón adicional y este llegaba a los campos antes de filtrarse. El segundo editor sustituía el trabajo pendiente, dejando campos vacíos o un diálogo que reaparecía. Ahora el filtro de eventos de ratón generados por toque se ejecuta primero y `request_text` conserva un único trabajo pendiente. La regresión publica `FINGERDOWN` y `MOUSEBUTTONDOWN` con `touch=True` y exige una sola solicitud de editor.

El teclado nativo recibe foco explícito al abrirse. La confirmación manual de estos arreglos sobre el APK reconstruido corresponde a la verificación de artefactos del principal. Este auditor no operó el emulador.

## Evidencia de cierre

| Comprobación | Resultado |
| --- | --- |
| Suite independiente tras Unicode y la corrección de doble evento | 112 pruebas correctas, en 34,934 segundos. |
| Compras y recarga tras el arreglo atómico | 100 ciclos correctos de 100. |
| Puente con nativo simulado | Diez comprobaciones correctas, incluidas URL Unicode y editor pendiente único. |
| Herramientas docentes nativas simuladas | Diez comprobaciones correctas. |
| Actividades físicas preparadas y persistencia | 36 mapas correctos de 36. |
| Sintaxis del wrapper contra Android 34 | Compilación Java correcta; avisos de API/source 8 obsoletos. |
| Duelo después de muerte y recarga | Referencia inicial conservada y condición respetada. |

Los registros y scripts se conservaron localmente en `.test-tmp/audit-07-new/`, separados por rondas y cierre. No contienen datos de alumnos reales. La comprobación de los ejecutables, capturas y hashes se documenta en `VERIFICACION.md`.

## Límites de la conclusión

Esta auditoría habilita la compilación y revisión de candidatos. Las pruebas preparadas no equivalen a recorrer con una persona todos los mapas ni a una experiencia docente observada. Equilibrio, accesibilidad efectiva y objetivos curriculares requieren esas sesiones.

En Android deben comprobarse sobre el artefacto instalado: arranque sin Internet, teclado y controles simultáneos, PIN, perfiles, guardado tras cerrar/reabrir, documentos nativos, Unicode y conexión LAN con la PC docente. Solo deben darse por realizadas las pruebas manuales documentadas expresamente. Los cambios funcionales posteriores requieren repetir las comprobaciones afectadas.
