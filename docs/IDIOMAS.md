# Español y português do Brasil

Configuración → Idioma permite elegir Español o Português (Brasil). La
preferencia se guarda por perfil y se conserva al comenzar otra partida.
El selector funciona también desde la configuración abierta durante una partida.

Menús, tutorial, objetivos, controles, preguntas originales, explicaciones,
curiosidades, fichas de skins y logros usan el catálogo incluido. No se necesita
Internet para cambiar de idioma. Los identificadores internos, nombres de mapas
en los guardados, respuestas correctas y puntuaciones permanecen iguales.

Los nombres escritos por alumnos y los campos de texto se muestran literalmente.
Una pregunta propia del docente conserva su idioma original. El editor indica
el idioma activo: al editar en portugués una pregunta cuya base es española,
guarda una variante independiente; no reemplaza el texto español. Exportar,
importar y compartir el banco en una sala conserva ambas versiones. Una pregunta
nueva se guarda con el idioma que estaba elegido al crearla. Alumnos de una sala
pueden usar distintos idiomas sin cambiar el banco del profesor.

La lectura en voz Android usa una voz española o portuguesa de Brasil instalada
y sin conexión. Si no existe una voz del idioma elegido, se muestra un aviso y
siguen disponibles los textos y señales visuales.

## Mantenimiento del catálogo

El catálogo desplegado es `assets/locales/pt-BR.json`; el español es el texto
original de las fuentes. `crono/i18n.py` traduce únicamente la presentación y
mantiene cachés acotadas. Los textos se traducen antes de medirlos y dividirlos
en renglones. Cambiar idioma invalida imágenes con etiquetas para que los
controles y carteles no conserven el idioma anterior.

La base portuguesa se preparó localmente con el modelo abierto Argos es→pt1.0;
se revisaron términos de interfaz, vocabulario de Brasil, fechas, numeración,
marcadores y opciones de respuesta. No es una revisión editorial integral por
un docente brasileño. El editor permite corregir o ampliar las traducciones.
Se tradujeron por separado las oraciones para evitar omisiones de párrafos.
Modelo: https://argos-net.com/v1/translate-es_pt-1_0.argosmodel
Documentación: https://argos-translate.readthedocs.io/en/latest/

`tools/pt_BR_review.json` conserva decisiones de vocabulario y traducciones
revisadas. `tools/localization_catalog.py --generate` recoge texto de las fuentes
y del banco original, añade entradas faltantes y aplica esas correcciones.
`--refine` vuelve a traducir párrafos por oración. El modelo, SentencePiece y
CTranslate2 son herramientas de desarrollo en `.android-build/localization`;
no se distribuyen con el juego. Nunca se leen bancos particulares ni datos de
alumnos para generar el catálogo.

La opción de captura `--language es` / `--language pt-BR` permite comprobar el
ejecutable sin cambiar el idioma guardado del usuario.

Los registros de pregunta existentes conservan su forma original. Los campos
opcionales nuevos son `language` y `translations`, con claves `es`/`pt-BR`;
cada variante contiene prompt/options/explanation/source y usa el mismo orden
de opciones y el mismo índice correcto. El formato de banco sigue aceptando
versiones1–7. Las traducciones nunca sobrescriben personalizaciones al migrar.
