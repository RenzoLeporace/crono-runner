import pygame
import lib.Var as Var

class Crono():
    def __init__(self, x, y, animaciones):
        self.flip = False
        self.animaciones = animaciones  
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = animaciones[self.frame_index]
        self.forma = pygame.Rect(0, 0, Var.ALTURA_CRONO, Var.ANCHURA_CRONO)
        self.forma.center = (x, y)
    def movimiento(self, delta_x, delta_y):
        if delta_x < 0:
            self.flip = True
        if delta_x > 0:
            self.flip = False
        self.forma.x = self.forma.x + delta_x
        self.forma.y = self.forma.y + delta_y    
    def actualizar_animacion(self):
        ANIMACION_COOLDOWN = 100
        self.image = self.animaciones[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMACION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animaciones):
            self.frame_index = 0
    def dibujar(self, ventana, camara_x=0):
        imagen_flip = pygame.transform.flip(self.image, self.flip, flip_y= False)
        rect_pantalla = self.forma.move(-camara_x, 0)
        ventana.blit(imagen_flip, rect_pantalla)
        #pygame.draw.rect(ventana, (255, 0, 0), rect_pantalla)


class Plataforma:
    def __init__(self, x, y, w, h, imagen=None, dx=0, dy=0, limite_izq=None, limite_der=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.imagen = imagen  # Surface o None
        self.dx = dx  # velocidad horizontal
        self.dy = dy  # velocidad vertical
        # limites de movimiento en coordenadas del MUNDO (si no se especifican, no se mueve)
        self.limite_izq = limite_izq if limite_izq is not None else self.rect.x
        self.limite_der = limite_der if limite_der is not None else self.rect.x

    def mover(self):
        if self.dx != 0:
            self.rect.x += self.dx
            if self.rect.x <= self.limite_izq or self.rect.x >= self.limite_der:
                self.dx *= -1

    def dibujar(self, ventana, camara_x=0):
        rect_pantalla = self.rect.move(-camara_x, 0)
        if self.imagen:
            ventana.blit(self.imagen, rect_pantalla)
        else:
            pygame.draw.rect(ventana, (150, 75, 0), rect_pantalla)


class Enemigo:
    """Enemigo con IA basica: patrulla de un lado a otro de su plataforma/zona
    y persigue a Crono cuando este se encuentra dentro de su rango de deteccion."""

    def __init__(self, x, y, animaciones, limite_izq=None, limite_der=None, velocidad=None):
        self.flip = False
        self.animaciones = animaciones
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = animaciones[self.frame_index]
        ancho_img = self.image.get_width()
        alto_img = self.image.get_height()
        self.forma = pygame.Rect(0, 0, ancho_img, alto_img)
        self.forma.center = (x, y)

        self.velocidad_patrulla = velocidad if velocidad is not None else Var.VELOCIDAD_ENEMIGO
        self.direccion = 1  # 1 = derecha, -1 = izquierda
        # Zona de patrulla en coordenadas del mundo
        self.limite_izq = limite_izq if limite_izq is not None else self.forma.x - 100
        self.limite_der = limite_der if limite_der is not None else self.forma.x + 100
        self.vivo = True
        self.estado = "patrulla"  # "patrulla" o "persecucion"

    def actualizar_ia(self, jugador):
        if not self.vivo:
            return

        distancia_x = jugador.forma.centerx - self.forma.centerx
        distancia = abs(distancia_x)

        if distancia <= Var.RANGO_DETECCION_ENEMIGO:
            # --- Modo persecucion ---
            self.estado = "persecucion"
            if distancia_x > 0:
                self.direccion = 1
            else:
                self.direccion = -1
            velocidad_actual = Var.VELOCIDAD_PERSECUCION_ENEMIGO
        else:
            # --- Modo patrulla ---
            self.estado = "patrulla"
            velocidad_actual = self.velocidad_patrulla
            if self.forma.x <= self.limite_izq:
                self.direccion = 1
            elif self.forma.x >= self.limite_der:
                self.direccion = -1

        self.forma.x += velocidad_actual * self.direccion
        self.flip = self.direccion < 0

        # No dejar que el enemigo se salga demasiado de su zona cuando persigue
        if self.estado == "persecucion":
            margen = 60
            if self.forma.x < self.limite_izq - margen:
                self.forma.x = self.limite_izq - margen
            if self.forma.x > self.limite_der + margen:
                self.forma.x = self.limite_der + margen

    def actualizar_animacion(self):
        ANIMACION_COOLDOWN = 150
        self.image = self.animaciones[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMACION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animaciones):
            self.frame_index = 0

    def dibujar(self, ventana, camara_x=0):
        if not self.vivo:
            return
        imagen_flip = pygame.transform.flip(self.image, self.flip, flip_y=False)
        rect_pantalla = self.forma.move(-camara_x, 0)
        ventana.blit(imagen_flip, rect_pantalla)
        #pygame.draw.rect(ventana, (255, 0, 0), rect_pantalla)


class Portal:
    """Portal de fin de nivel. Al colisionar con Crono, el nivel se completa."""

    def __init__(self, x, y, imagen, ancho=90, alto=90):
        self.imagen = pygame.transform.scale(imagen, (ancho, alto))
        self.rect = self.imagen.get_rect()
        self.rect.midbottom = (x, y)
        self.frame = 0

    def dibujar(self, ventana, camara_x=0):
        rect_pantalla = self.rect.move(-camara_x, 0)
        ventana.blit(self.imagen, rect_pantalla)
