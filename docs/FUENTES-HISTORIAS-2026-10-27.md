# Contenidos históricos revisados · 27 de octubre de 2026

Esta comprobación se limita a las preguntas específicas añadidas y a las rutas
de las guerras mundiales y Chernóbil. No es una auditoría completa del juego ni
una validación curricular de aula. Los textos son paráfrasis; las misiones y
reglas de protección pertenecen al diseño del juego.

## Cambios concretos

Los mapas 46–49 añaden Verdún/Somme, armisticio, Stalingrado e Ypres, sin mover
los IDs anteriores. Los temas 32–34 enseñan ahora el Blitz, la protección civil
y la rendición alemana: antes sus textos generales no coincidían con los nuevos
nombres de los mapas de Londres y Berlín. El tema 35 conserva los derechos
humanos de 1948. Los temas 70–71 pasan de la excursión lunar duplicada a
Chernóbil; Apolo 11 permanece en el mapa lunar de Guerra Fría.

Se distingue el armisticio de 1918 del tratado de 1919, el final europeo de la
guerra de su final mundial y los primeros recursos respiratorios de 1915 de
modelos de 1916. Las preguntas nuevas sobre Enigma, Tombuctú, Gutenberg, Güemes,
Berlín y Apolo 11 nombran hechos, objetos o lugares concretos, sin la plantilla
que solo cambiaba el título de una lección.

El total de registros del banco incluye distintas bandas e IDs de compatibilidad:
no equivale al mismo número de preguntas o hechos históricos diferentes. No se
reemplazan automáticamente los registros originales modificados por docentes.

## Fuentes contrastadas

| Contenido | Fuente institucional y alcance |
| --- | --- |
| Verdún y Somme | [Ministerio de las Fuerzas Armadas de Francia](https://www.defense.gouv.fr/chemins-memoire/histoire-memoires/ressources-historiques/premiere-guerre-mondiale/combattre-combats/fronts-32): cronología de 1916, Douaumont, Vaux y empleo de carros. |
| Armisticio | [National Army Museum · 1918](https://www.nam.ac.uk/explore/1918-victory): Compiègne y entrada en vigor del cese del fuego. |
| Posguerra de 1918 | [National Army Museum · Paz y conmemoración](https://www.nam.ac.uk/explore/peace-and-commemoration): Versalles, desmovilización y necesidades posteriores. |
| Stalingrado | [USHMM · Frente oriental](https://encyclopedia.ushmm.org/content/en/article/the-soviet-union-and-the-eastern-front): Volga, contraofensiva de noviembre de 1942 y rendición de 1943. |
| Ypres | [National WWI Museum](https://www.theworldwar.org/learn/about-wwi/spotlight-first-usage-poison-gas): ataque de cloro de abril de 1915 y evolución de la guerra química. |
| Respiradores | [Australian War Memorial](https://www.awm.gov.au/3dtreasures/items/small-box-respirator/): primeras protecciones y respirador de caja pequeña británico de 1916. |
| Blitz | [London Museum](https://www.londonmuseum.org.uk/collections/london-stories/londons-blitz-a-city-at-war/): campaña de 1940–1941, efectos civiles y otras ciudades atacadas. |
| Protección civil | [RAF Museum](https://www.rafmuseum.org.uk/research/online-exhibitions/history-of-the-battle-of-britain/the-home-front/): refugios, metro, Anderson y bomberos. |
| Berlín y rendición | [National Archives · Alemania](https://www.archives.gov/milestone-documents/surrender-of-germany) y [USHMM · Rendición](https://encyclopedia.ushmm.org/content/en/timeline-event/holocaust/1942-1945/german-forces-surrender-to-the-allies): documentos, ciudades y fechas diferentes. |
| Final mundial de 1945 | [National Archives · Japón](https://www.archives.gov/milestone-documents/surrender-of-japan): el instrumento japonés es posterior a la rendición alemana. |
| Chernóbil | [Central de Chornóbil](https://www.chnpp.gov.ua/en/about/history-of-the-chnpp/accident-of-1986): reactor 4 y accidente durante pruebas en abril de 1986. |
| Estudios posteriores | [OIEA · documento de contexto](https://www.iaea.org/sites/default/files/21/04/iaea-background-document-chornobyl.pdf): revisiones, investigaciones y cooperación después del accidente. |
| Enigma y Bombe | [The National Museum of Computing](https://www.tnmoc.org/bombe): carácter electromecánico de la Bombe, antecedentes polacos y trabajo colectivo. |
| Tombuctú | [Library of Congress · introducción](https://www.loc.gov/exhibits/mali/mali-overview.html) y [objetos de la exposición](https://www.loc.gov/exhibits/mali/mali-exhibit.html): rutas, colecciones y diversidad de manuscritos. |
| Güemes | [Argentina · Plan Continental](https://www.argentina.gob.ar/noticias/el-general-guemes-y-el-plan-continental-sanmartiniano): defensa del norte y relación con la campaña independentista. |
| Lanceiros Negros | [Senado Federal de Brasil](https://www12.senado.leg.br/noticias/materias/2023/03/15/paim-fala-sobre-aprovacao-de-lanceiros-negros-no-livro-dos-herois-da-patria): participación y desigualdad durante la Guerra de los Farrapos. |
| Berlín, 1961–1989 | [Landesdenkmalamt de Berlín](https://www.berlin.de/landesdenkmalamt/denkmale/highlight-berliner-mauer/aufbau-und-entwicklung/): desarrollo del sistema fronterizo y fechas del muro. |
| Apolo 11 | [NASA · misión](https://www.nasa.gov/history/apollo-11-mission-overview/) y [NASA · regreso de Eagle](https://science.nasa.gov/resource/eagles-return/): tripulación, módulos y órbita. |

La página de la Biblioteca Nacional Alemana sobre Gutenberg y la descarga de
«Fallas do Throno» del Senado brasileño no pudieron recuperarse completas con
el lector web durante esta comprobación. Se conservaron las formulaciones
históricas prudentes; no se presenta ese acceso fallido como una lectura completa.
El catálogo general del proyecto conserva las demás referencias por tema.

## Comprobaciones reproducibles

`python -m unittest discover -s tests -p test_specific_history.py` verifica IDs
anteriores, incorporación de temas, formato de registros, ausencia de las
plantillas retiradas, coherencia de los episodios y migración de un registro
original de formato 6 conservando una edición docente.
