# Auditoría 0.7 · conclusiones y cambios

24 de octubre de 2026. Se retomó al auditor original y se añadió un segundo auditor exigente antes de compilar EXE y APK, como pidió Renzo Leporace. Un tercer subagente había jugado sesiones programáticas y propuesto los 60 logros.

## Dictámenes de fuente

Ambos auditores concluyeron que no quedaban bloqueos reproducibles de sus revisiones para pasar a compilar candidatos. La última batería del principal pasó **113/113 pruebas**; los auditores independientes cerraron sus rondas con 109 y 112 pruebas y el ensayo de compras, guardado y recarga pasó **100/100 ciclos**.

- [Juego, arte, rutas e interfaz](AUDITORIA-0.7-JUGABILIDAD.md).
- [Aula, persistencia, salas y puente Android](AUDITORIA-0.7-SISTEMAS.md).
- [Comprobaciones de los artefactos distribuidos y límites](../VERIFICACION.md).

## Qué sugirieron y qué se hizo

| Propuesta | Cambio incorporado |
| --- | --- |
| Rutas legibles con detalle y descanso | Rework de 21 mapas anteriores, hitos propios, bordes transitables contrastados, introducción de dispositivos en zonas seguras y enemigos reubicados fuera del primer contacto. |
| Enemigos y jefes reconocibles y más expresivos | Modelos humanoides contextuales, Cruz de Borgoña realista, variantes navales/romanas/de clima frío, señal de protección y daño visible en los 18 jefes. Ataques adicionales anticipados en media/alta. |
| Dar significado a explorar | Una curiosidad por mapa, cinco rescates que abren bonus, tres grietas con retorno exacto y recompensa única, actividades físicas contextualizadas y ecos como moneda para skins. |
| Reconocer distintas formas de jugar | 60 logros con condiciones explícitas de exploración, combate y aprendizaje. Todos conceden un beneficio real al completar la colección: Reloj del Cronista. |
| Mejor accesibilidad | Texto 19/22/25, desplazamiento con teclado y tacto, reasignación de controles, asistencia motriz separada de edad y controles multitouch. |
| Aprendizaje más amplio que memorizar | Banco 1296 registros con preguntas factuales y tareas de fuentes, imágenes, razonamiento y cronología; explicación tras error, repaso y justificación escrita. |
| Herramientas de aula | Perfiles aislados, intentos y correcciones, CSV reconstruible, PIN opcional, selección de temas, importación/exportación con vista previa y respaldos, guía de 15–25 minutos. |
| Probar todo sin interferir con alumnos | Práctica docente con todos los mapas, mejoras y skins; desplazamientos por mapa y resultados separados de los rankings reales. |
| Trabajo entre dispositivos | Salas Windows por IP y código, clientes Windows/Android, banco y temas compartidos, rankings por clase e institución dentro de la sala. |

## Bugs concretos encontrados y corregidos

Las rondas detectaron mezcla de progreso al cambiar de perfil y cerrar, premios consumidos durante práctica, puestos duplicados o tapados por otra interacción, invulnerabilidad heredada al subir a un vehículo, orientación de cañón incorrecta y guardados interiores mal formados.

Se corrigieron también el retorno de grietas tras cerrar/continuar, puntuaciones duplicadas por IDs no canónicos, docentes que aparecían como alumnos, tareas de red que podían aplicar resultados a otro perfil, lectura de fichas a 25 píxeles, glifos táctiles, plataformas inactivas visibles, señales de daño y superposición del HUD.

En la última ronda se corrigieron el bloqueo de arena al teletransportar al docente, importaciones Android con BOM, previsualización antigua después de cancelar o fallar, CSV sin BOM, carga masiva de respaldos al iniciar, límites de respuesta LAN insuficientes para bancos grandes y un import de threading perdido. Un bloqueo transitorio de OneDrive reproducido durante compras motivó reintentos acotados de escritura atómica, con conservación del archivo anterior y aviso si persiste.

## Alcance real

Se probaron sistemas y física real mediante escenarios preparados, capturas y sesiones programáticas. Las 36 actividades se completaron aisladamente; esto no equivale a recorrer 36 mapas a mano. Los 18 jefes tienen feedback comprobado; no se afirma que todos se hayan derrotado sin mejoras y sin muertes. Algunas estrategias automáticas no resolvieron tres encuentros nuevos, sin demostrar que sean imposibles.

La auditoría no sustituye sesiones humanas, calibración con las tres edades, revisión curricular ni un piloto escolar. Los rankings incluyen destreza y velocidad y no deben convertirse por sí solos en una nota de aprendizaje. Los informes de fuente anteceden a las comprobaciones de paquetes descritas en VERIFICACION.md.
