# Verificación de la beta educativa 0.4

Fecha: 22 de octubre de 2026. Windows 11, Python 3.12 y pygame-ce 2.5.7.

## Pruebas automáticas

**61 pruebas aprobadas**: 23 en `tests/test_game.py`, 19 en `tests/test_education.py` y 19 en `tests/test_teacher.py`.

- Simulación de saltos con la física real para comprobar los fragmentos y la salida de los 15 mapas, sin mejoras ni impulso obligatorios.
- Progresión ordenada de los 15 mapas, cinco épocas y desenlace; bloqueo de portales por fragmentos y guardianes.
- Salto variable, tolerancia al borde, memoria de salto, impulso, paredes, plataformas móviles, combate y reaparición.
- Banco de 180 preguntas: dos variantes por archivo y perfil, selección por edad, no repetición inmediata y mezcla de posiciones correctas.
- Respuesta errónea sin penalización, recompensa única, compras con requisitos y saldo, persistencia y prevención de recompensas duplicadas al cambiar de edad.
- Segundo salto, escudo, energía mejorada, resistencia de enemigos acorazados y daño del pulso amplificado.
- Seis comportamientos de enemigo y mezclas de al menos tres tipos en cada mapa.
- Combates completos simulados de los cinco guardianes con equipo básico, sin muertes en las pruebas. Duraciones de los escenarios de combate: aproximadamente 12, 18, 18, 25 y 30 segundos.
- Núcleos protegidos, vulnerabilidad ampliada por aprendizaje, entrada de arena y reinicio del jefe al morir.
- Migración de partidas 0.2 con respaldo, conservación de fragmentos y anclas, tolerancia a guardados dañados.
- Navegación por teclado desde un archivo hasta responder y volver a la partida; selector de edad mediante clic y persistencia.
- Render de los 15 escenarios, pantallas educativas, 30 archivos en los tres perfiles y las cuatro fases de la pregunta; todas las páginas del cuaderno.
- Consulta de las 180 preguntas sin desbloqueos; altas, duplicación y modificación de pregunta, respuestas, opción correcta, explicación, referencia, archivo, mapa y edad.
- Uso inmediato del banco editado en el sorteo real, mezcla de respuestas conservando la correcta, persistencia al recargar, respaldos exactos y rechazo de datos inválidos sin escritura parcial.
- Conservación del archivo dañado, advertencia y recuperación mediante guardado explícito con respaldo; protección del último contenido de cada archivo y edad.
- Eventos de ratón y teclado en configuración y editor, entrada Unicode, atajos de texto, cambios sin guardar, selector de mapa y textos largos con desplazamiento.
- Quince ambientes distintos y galería de escenarios sin modificar la partida.

## Revisión visual y ejecutable

Capturas revisadas en `capturas/educativa-0.4/`: menú, preguntas, explicaciones, taller, cuaderno, configuración, banco docente, editor, selector de mapa del editor, galería, 15 paisajes y cinco guardianes. Se revisaron las respuestas señaladas y el escenario de extinción con terreno quemado, meteoros, humo, incendios y cenizas. Los efectos ambientales son visuales y no modifican las colisiones.

Medición orientativa del render fuera de pantalla a 1280 × 720: aproximadamente 6,4 ms por cuadro, unos 157 cuadros por segundo en esta máquina. No es una garantía de rendimiento en otras computadoras.

El ejecutable se construye con PyInstaller en formato portable, con sus bibliotecas en `_internal`. Se eligió este formato después de observar una demora de arranque en la variante de archivo único. La comprobación de distribución genera capturas del banco docente, del editor y del escenario de extinción desde el propio ejecutable, y comprueba que terminen sin errores.

La partida existente permanece en formato 2, compatible con la beta 0.3. El banco docente usa su propio archivo, independiente del progreso del alumno. Los ensayos de edición usan archivos temporales y no modifican los contenidos del usuario.

## Límites

No hubo una sesión completa de juego humano de toda la campaña, pruebas con alumnos ni validación docente. Tampoco se verificó hardware físico de mando. La simulación comprueba rutas y reglas; el equilibrio y la adecuación pedagógica necesitan pruebas con personas.
