import os

ANCHO_PANTALLA = 1080
ALTO_PANTALLA = 640
FPS = 60
TITULO_JUEGO = "CRONO: El Viajero del Tiempo"


GRAVEDAD = 1 
VELOCIDAD_CRONO = 5 
VELOCIDAD_SALTO = -28

ALTURA_CRONO = 60
ANCHURA_CRONO = 50
ESCALA_CRONO = 0.3

mover_izquierda = False
mover_derecha = False
mover_arriba = False
mover_abajo = False

en_suelo = False
SUELO_Y = 500

# --- Nivel / Mundo ---
ANCHO_NIVEL = 3400   # ancho total del nivel (mas grande que la pantalla para poder scrollear)

# --- Camara ---
camara_x = 0

# --- Enemigos / IA ---
VELOCIDAD_ENEMIGO = 2
RANGO_DETECCION_ENEMIGO = 250   # distancia a la que el enemigo detecta y persigue a Crono
VELOCIDAD_PERSECUCION_ENEMIGO = 4
