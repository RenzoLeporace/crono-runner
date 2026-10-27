# Comprobaciones funcionales de exposición y objetos · 27/10/2026

Trabajo focal solicitado por Renzo y delegado por el agente principal. No es
una auditoría completa ni una prueba en un teléfono físico. No se compilaron
paquetes desde este subtrabajo.

Las regresiones están en `tests/test_environment_followup.py`. Se ejecutan con
Python y pygame-ce locales, vídeo y audio SDL `dummy`:

```powershell
$env:PYTHONPATH='.vendor;tests'
$env:PYTHONUTF8='1'
python -m unittest test_environment_followup
```

## Qué comprueban

1. El frío consume calor en los tres mapas de hielo, Andes, Malvinas y
   Stalingrado. El abrigo reduce el consumo pero no lo elimina. Se usan
   actualizaciones de la física real, sobre superficies existentes.
2. Agotar calor reinicia al comienzo incluso habiendo activado un ancla.
3. Abrigo, tanque y máscara se recogen en una superficie alcanzable entre el
   15 % y el 40 % del trayecto, y no vuelven inmune al ambiente.
4. Refugios y recargas recuperan calor, oxígeno o filtro al permanecer cerca.
5. Agotar oxígeno o filtro devuelve al ancla conservada, sin duplicar muertes.
6. Equipo y recurso restante se guardan y restauran en los cinco contextos.
7. Las anclas de los 50 mapas mantienen orden y el punto anterior al jefe.
8. Archivos, curiosidades, puestos, recogibles, refugios, anclas y equipo están
   apoyados en superficies activas existentes.
9. Las balizas no atraviesan pasarelas superiores en su volumen visible.
10. Ningún par de esos objetos ocupa a la vez la misma región de 100 × 80 px.
    Es una comprobación geométrica de los objetos, no de todos sus rótulos.
11. La curiosidad aparece antes del segundo archivo en los 50 mapas.
12. Meteoritos, ceniza y bombardeos primero muestran aviso, después generan
    impacto y modifican píxeles visibles. Incluye mapas 2, 15, 16, 34, 46,
    48 y 49.
13. Las consultas de colisión por cercanía coinciden con el recorrido completo
    de plataformas, en 8250 rectángulos de prueba sobre los 50 mapas y tres
    fases de movimiento. Incluye plataformas activadas/desactivadas y cambio
    de lista de superficies, conservando el orden de resolución.

## Errores encontrados y corregidos

La primera disposición podía invertir dos anclas del primer mapa de hielo y
solapar objetos de la Luna: archivo/ancla, pieza/tanque, pieza/refugio y
refugios/anclas. El agente principal corrigió la colocación tomando las
anclas como reservas y admitiendo superficies activas más pequeñas, sin
cambiar IDs.

El tanque lunar quedaba en el 4 % del trayecto en lugar de más adelante.
Ahora su colocación se reserva en la franja del 15–40 % antes de situar
otros objetos automáticos. Dos anclas lunares estaban atravesadas por
pasarelas situadas 88 px encima (anclas 1 y 6); sus puntos se apoyan ahora
en esas pasarelas. Conservan sus IDs, orden y superficie real de aparición.

## Resultado

Las 13 pruebas de este archivo pasaron después de esas correcciones. La
ejecución integrada junto con las pruebas de contenido específico y
configuración/navegación aprobó 27 pruebas en 6,608 segundos. Registro local:
`.test-tmp/integrated-followups.txt`. Este resultado verifica las fuentes;
no valida por sí solo una compilación entregable.

## Límites

No mide FPS Android, uso de memoria de un teléfono ni comodidad para niños.
Las pruebas de exposición usan recorridos controlados y posiciones reales de
apoyo; no equivalen a completar manualmente toda la campaña. La separación
geométrica no sustituye una revisión visual de todos los textos y decorados.
