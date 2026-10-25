# CRONO 0.8 · iPhone y iPad

Esta entrega es una edición web experimental. No incluye un IPA ni firma de Apple. Compilar una aplicación nativa distribuible requiere el entorno de Apple y la firma correspondiente.

## Desde la misma WiFi que una PC Windows

1. Extrae el ZIP Windows completo, conservando `_internal` e `iOS-Web` junto al EXE.
2. Abre `Abrir en iPhone.bat`. La ventana muestra la dirección local.
3. Desde Safari en el iPhone/iPad abre esa dirección, toca para iniciar y gira el teléfono a horizontal.
4. Mantén la ventana y la PC abiertas mientras juegas. Si Windows solicita permiso de red, usa únicamente la red privada de confianza donde estás jugando.

El servidor comparte los archivos públicos del juego, no la carpeta de partidas ni la configuración docente de la PC. El teléfono tiene su progreso independiente en el almacenamiento del navegador. Usa el mismo origen/dirección para volver a esa partida; cambiar IP, puerto o navegador crea otro espacio de guardado. Borrar datos del sitio también borra ese progreso. Exporta el banco y las evidencias que necesites conservar.

## Instalación como aplicación web

Puedes alojar el contenido del ZIP iOS-Web en un servidor HTTPS. Abre la dirección desde Safari y usa Compartir → Añadir a pantalla de inicio. Tras una primera carga completa, el service worker prepara el motor y los recursos para recargar sin conexión. En una IP local mediante HTTP no se ofrece esa caché offline: requiere la PC conectada. No basta con abrir `index.html` como archivo.

Los controles muestran más mapa para adaptarse al ancho horizontal sin estirar personajes. La versión web permite guardado individual, edición/importación/exportación de preguntas y menús educativos. No incluye cliente LAN para clasificaciones compartidas; utiliza el APK Android o Windows para ese propósito.

## Comprobaciones y límites

El paquete comparte el código del juego Android. Se comprueba el arranque y guardado en un navegador Chromium local; esto no certifica Safari, audio o rendimiento en dispositivos Apple. Safari puede suspender una pestaña en segundo plano o eliminar caché por espacio. No se ha probado en iPhone/iPad físico.

[Apple: convertir un sitio en app en iPhone](https://support.apple.com/en-lamr/guide/iphone/iphea86e5236/ios).
