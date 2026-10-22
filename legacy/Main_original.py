import pygame
import os
from lib.Core import Crono, Plataforma, Enemigo, Portal
import lib.Var
pygame.init()

# ------------------------------------------------------------------
# Carga de recursos
# ------------------------------------------------------------------

#escalar la imagen
def escalar_img(image, scale):
    width = image.get_width()
    height = image.get_height()
    new_size = (int(width * scale), int(height * scale))
    return pygame.transform.scale(image, new_size)

#Contar elementos
def contar_elementos_carpeta(ruta):
    try:
        elementos = os.listdir(ruta)
        return len(elementos)
    except FileNotFoundError:
        print("La ruta especificada no existe.")
        return 0

#Nombre de la carpeta
def obtener_nombre_carpeta(ruta):
    return os.path.basename(os.path.normpath(ruta))

# --- Plataformas ---
plataforma_img = pygame.image.load("Sprite/Obstaculos/hielo.jpg")
plataforma_img = pygame.transform.scale(plataforma_img, (200, 20))

plataformas = [
    Plataforma(200, 400, 200, 20, plataforma_img),
    Plataforma(600, 300, 200, 20, plataforma_img, dx=2, limite_izq=500, limite_der=800),
    Plataforma(1000, 420, 200, 20, plataforma_img),
    Plataforma(1300, 320, 200, 20, plataforma_img, dx=2, limite_izq=1250, limite_der=1550),
    Plataforma(1650, 430, 200, 20, plataforma_img),
    Plataforma(1950, 340, 200, 20, plataforma_img),
    Plataforma(2250, 420, 200, 20, plataforma_img, dx=3, limite_izq=2200, limite_der=2500),
    Plataforma(2600, 340, 200, 20, plataforma_img),
    Plataforma(2900, 420, 200, 40, plataforma_img),
    Plataforma(lib.Var.ANCHO_NIVEL - 220, 440, 200, 40, plataforma_img),  # plataforma final del portal
]

# --- Animaciones del jugador ---
animaciones = []
for i in range(4):
    img = pygame.image.load(f"Sprite/Personaje/crono_idle{i}.png")
    img = escalar_img(img, lib.Var.ESCALA_CRONO)
    animaciones.append(img)

# --- Animaciones de enemigos ---
lista_enemigos = ["Dino", "Tigre"]
CarpetaEnemigos = "Sprite/Enemigos"
animaciones_enemigos = {}
for enemigo in lista_enemigos:
    lista_temporal = []
    ruta_temporal = f"Sprite/Enemigos/{enemigo}"
    archivos = sorted(os.listdir(ruta_temporal))
    for archivo in archivos:
        img = pygame.image.load(f"{ruta_temporal}/{archivo}")
        img = escalar_img(img, lib.Var.ESCALA_CRONO)
        lista_temporal.append(img)
    animaciones_enemigos[enemigo] = lista_temporal

# --- Jugador ---
jugador = Crono(100, 500, animaciones)

# --- Configuracion ventana ---
ventana = pygame.display.set_mode((lib.Var.ANCHO_PANTALLA, lib.Var.ALTO_PANTALLA))
pygame.display.set_caption(lib.Var.TITULO_JUEGO)

# --- Lista de enemigos con zonas de patrulla ---
enemigos = [
    Enemigo(400, 480, animaciones_enemigos["Dino"], limite_izq=320, limite_der=520),
    Enemigo(1100, 390, animaciones_enemigos["Tigre"], limite_izq=1020, limite_der=1250),
    Enemigo(1750, 400, animaciones_enemigos["Dino"], limite_izq=1680, limite_der=1900),
    Enemigo(2050, 310, animaciones_enemigos["Tigre"], limite_izq=1980, limite_der=2200),
    Enemigo(2700, 310, animaciones_enemigos["Dino"], limite_izq=2620, limite_der=2850),
]

# --- Fondo (se repite a lo largo del nivel) ---
background_img = pygame.image.load("Sprite/Fondos/hielo.jpg")
background_img = pygame.transform.scale(background_img, (lib.Var.ANCHO_PANTALLA, lib.Var.ALTO_PANTALLA))
ancho_fondo = background_img.get_width()
num_fondos = (lib.Var.ANCHO_NIVEL // ancho_fondo) + 2

# --- Portal de fin de nivel ---
portal_img = pygame.image.load("Sprite/Objetos/Power.png").convert_alpha()
plataforma_final = plataformas[-1]
portal = Portal(plataforma_final.rect.centerx, plataforma_final.rect.top, portal_img, ancho=110, alto=110)

velocidad_y = 0
run = True
nivel_completado = False

reloj = pygame.time.Clock()

while run:
    reloj.tick(lib.Var.FPS)
    delta_x = 0
    delta_y = 0
    prev_bottom = jugador.forma.bottom

    # --- Actualizar plataformas ---
    for plat in plataformas:
        plat.mover()

    # --- Movimiento horizontal ---
    if lib.Var.mover_derecha:
        delta_x = lib.Var.VELOCIDAD_CRONO
    if lib.Var.mover_izquierda:
        delta_x = -lib.Var.VELOCIDAD_CRONO

    # --- Movimiento vertical (salto y gravedad) ---
    if lib.Var.mover_arriba and lib.Var.en_suelo:
        velocidad_y = lib.Var.VELOCIDAD_SALTO
        lib.Var.en_suelo = False
    velocidad_y += lib.Var.GRAVEDAD
    delta_y = velocidad_y

    # --- Movimiento horizontal y colision horizontal ---
    jugador.movimiento(delta_x, 0)
    for plat in plataformas:
        if jugador.forma.colliderect(plat.rect):
            if delta_x > 0:
                jugador.forma.right = plat.rect.left
            elif delta_x < 0:
                jugador.forma.left = plat.rect.right

    # --- Movimiento vertical y colision vertical ---
    jugador.movimiento(0, delta_y)
    lib.Var.en_suelo = False
    for plat in plataformas:
        if jugador.forma.colliderect(plat.rect):
            if velocidad_y > 0:  # Cayendo
                jugador.forma.bottom = plat.rect.top
                velocidad_y = 0
                lib.Var.en_suelo = True
            elif velocidad_y < 0:
                jugador.forma.top = plat.rect.bottom
                velocidad_y = 0

    # --- Suelo ---
    if jugador.forma.bottom >= lib.Var.SUELO_Y:
        jugador.forma.bottom = lib.Var.SUELO_Y
        velocidad_y = 0
        lib.Var.en_suelo = True

    # --- Limitar bordes del NIVEL (no de la pantalla) ---
    if jugador.forma.left < 0:
        jugador.forma.left = 0
    if jugador.forma.right > lib.Var.ANCHO_NIVEL:
        jugador.forma.right = lib.Var.ANCHO_NIVEL
    if jugador.forma.top < 0:
        jugador.forma.top = 0

    jugador.actualizar_animacion()

    # --- Camara: sigue a Crono, centrado en pantalla ---
    camara_x = jugador.forma.centerx - lib.Var.ANCHO_PANTALLA // 2
    camara_x = max(0, min(camara_x, lib.Var.ANCHO_NIVEL - lib.Var.ANCHO_PANTALLA))
    lib.Var.camara_x = camara_x

    # --- IA de enemigos ---
    for ene in enemigos:
        ene.actualizar_ia(jugador)
        ene.actualizar_animacion()

    # --- Colisiones jugador-enemigos ---
    enemigos_restantes = []
    crono_murio = False
    for ene in enemigos:
        if jugador.forma.colliderect(ene.forma):
            mask_jugador = pygame.mask.from_surface(jugador.image)
            mask_enemigo = pygame.mask.from_surface(ene.image)
            offset = (ene.forma.x - jugador.forma.x, ene.forma.y - jugador.forma.y)
            if mask_jugador.overlap(mask_enemigo, offset):
                if prev_bottom <= ene.forma.top + 10 and jugador.forma.bottom >= ene.forma.top and velocidad_y > 0:
                    print("¡Enemigo derrotado!")
                    velocidad_y = lib.Var.VELOCIDAD_SALTO
                    continue  # el enemigo no se agrega a la lista -> eliminado
                else:
                    print("¡Crono ha muerto!")
                    crono_murio = True
                    break
            else:
                enemigos_restantes.append(ene)
        else:
            enemigos_restantes.append(ene)

    if crono_murio:
        run = False
        break

    enemigos = enemigos_restantes

    # --- Colision con el portal (fin de nivel) ---
    if not nivel_completado and jugador.forma.colliderect(portal.rect):
        nivel_completado = True

    # ------------------------------------------------------------------
    # DIBUJADO
    # ------------------------------------------------------------------
    ventana.fill((0, 0, 0))

    # Fondo repetido a lo largo del nivel, con efecto parallax leve
    fondo_offset = int(camara_x * 0.5) % ancho_fondo
    for i in range(num_fondos):
        ventana.blit(background_img, (i * ancho_fondo - fondo_offset, 0))

    for plat in plataformas:
        plat.dibujar(ventana, camara_x)

    portal.dibujar(ventana, camara_x)

    jugador.dibujar(ventana, camara_x)

    for ene in enemigos:
        ene.dibujar(ventana, camara_x)

    if nivel_completado:
        fuente = pygame.font.SysFont(None, 60)
        texto = fuente.render("¡Nivel completado!", True, (255, 255, 0))
        rect_texto = texto.get_rect(center=(lib.Var.ANCHO_PANTALLA // 2, lib.Var.ALTO_PANTALLA // 2))
        ventana.blit(texto, rect_texto)
        pygame.display.update()
        pygame.time.delay(2000)
        run = False
        break

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                lib.Var.mover_derecha = True
            if event.key == pygame.K_LEFT:
                lib.Var.mover_izquierda = True
            if event.key == pygame.K_UP:
                lib.Var.mover_arriba = True
            if event.key == pygame.K_DOWN:
                lib.Var.mover_abajo = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                lib.Var.mover_derecha = False
            if event.key == pygame.K_LEFT:
                lib.Var.mover_izquierda = False
            if event.key == pygame.K_UP:
                lib.Var.mover_arriba = False
            if event.key == pygame.K_DOWN:
                lib.Var.mover_abajo = False

pygame.quit()
