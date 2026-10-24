# Verificación · beta educativa 0.5

24 de octubre de 2026. Windows 11, Python 3.12, pygame-ce 2.5.7.

## Pruebas automáticas

**76 pruebas**: 23 de juego, 19 educativas, 19 del editor y 15 de la expansión.

- Las 24 rutas tienen geometrías distintas, más de 12.000 píxeles, tres zonas, 48 ecos, anclas y fragmentos en ramales.
- Saltos y descensos con controlador y colisiones reales para verificar conexiones obligatorias, tres fragmentos y archivos de cada mapa, sin mejoras ni plataformas móviles. Se comprueban conexiones; no se simula una partida humana continua.
- Salto variable, tolerancia al borde, impulso, paredes, plataformas móviles, descenso de pasarelas, daño y reaparición.
- Progresión de 21 mapas principales, final en actualidad y bloqueo por fragmentos/jefes. Argentina conserva su progreso y comparte mejoras y aprendizaje.
- Ocho combates completos simulados en dificultad mínima sin mejoras ni muertes. Los perfiles mayores se comprueban por velocidad, salud, frecuencia, salvas, marcas de caída y ventanas de vulnerabilidad; no se afirma una campaña completa automatizada en alta.
- Cambio de edad aplicado al mundo activo sin revivir derrotados. Ocho familias con siluetas distintas incluso al quitar el color.
- 288 preguntas en 48 archivos y tres edades: sorteo, mezcla, no repetición inmediata, recompensa única y errores sin castigo.
- Editor docente completo, validación, escritura atómica, respaldos, búsqueda, Unicode, selección, textos largos y protección de cambios.
- Migración de bancos con preguntas propias desde ID 180: se conservan contenidos y se agregan nuevos temas con IDs independientes.
- Migración de partidas con respaldo, inventario y aprendizaje; entrada segura por cambio de geometría; apertura de guerras si se había completado la beta 0.4.
- Render de mapas, jefes, modelos, perfiles, planos y zona docente. V pausa en el plano y Esc vuelve al estado anterior.

## Visuales y distribución

Capturas en `capturas/educativa-0.5`: 24 escenarios, ocho guardianes, familias de enemigos, plano, menú, épocas, configuración y editor. Se revisan trincheras, refugios, reconstrucción, redes, renovables, observatorio, Cabildo, Tucumán y plaza cívica.

Medición orientativa fuera de pantalla a 1280 × 720: unos 6,4 ms por cuadro en esta máquina. No garantiza rendimiento en otros equipos.

El ejecutable PyInstaller se distribuye con `_internal`. El empaquetado comprueba ocho escenas: configuración, banco, editor, galería argentina, pregunta argentina, jefe actual, plano de guerras y mapa de Tucumán. También comprueba la integridad del ZIP y que no contenga partidas ni bancos docentes personalizados.

## Límites

No se realizó una partida humana completa de los 24 mapas ni sesiones con alumnos o docentes. El equilibrio de media y alta requiere esas pruebas. Tampoco se verificó un mando físico. Referencias en `FUENTES.md`; escenarios y adversarios son ficción.
