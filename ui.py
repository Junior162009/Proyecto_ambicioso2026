# ui.py — Elementos de UI: FranjaTexto y Pergamino
import pygame
from settings import TEXTO_TITULO, TEXTO_NORMAL, TEXTO_SECUNDARIO, ANCHO, ALTO

class FranjaTexto:
    """Banda de texto que aparece en la parte inferior de la pantalla."""

    def __init__(self, imagen=None):
        self.imagen  = imagen
        self.mensaje = ""
        self.activa  = False
        self.fin     = 0
        self.font    = pygame.font.Font(None, 32)

    def mostrar(self, texto, duracion=2.0):
        self.mensaje = texto
        self.activa  = True
        self.fin     = pygame.time.get_ticks() + int(duracion * 1000)

    def actualizar(self):
        if self.activa and pygame.time.get_ticks() > self.fin:
            self.activa = False

    def dibujar(self, pantalla):
        if not self.activa:
            return

        ancho = pantalla.get_width()
        alto  = pantalla.get_height()

        franja_alto = 50
        franja_y    = alto - franja_alto - 10

        if self.imagen:
            img = pygame.transform.scale(self.imagen, (ancho - 100, franja_alto))
            pantalla.blit(img, (50, franja_y))
        else:
            fondo = pygame.Surface((ancho - 100, franja_alto), pygame.SRCALPHA)
            fondo.fill((0, 0, 0, 210))
            pantalla.blit(fondo, (50, franja_y))
            pygame.draw.rect(pantalla, (139, 69, 19), (50, franja_y, ancho - 100, franja_alto), 3)

        txt = self.font.render(self.mensaje, True, TEXTO_TITULO)
        pantalla.blit(txt, (ancho // 2 - txt.get_width() // 2, franja_y + (franja_alto - txt.get_height()) // 2))


class Pergamino:
    """Pergamino flotante con texto informativo."""

    def __init__(self, imagen=None):
        self.imagen  = imagen
        self.mensaje = ""
        self.activa  = False
        self.fin     = 0
        self.font    = pygame.font.Font(None, 26)

    def mostrar(self, texto, duracion=3.0):
        self.mensaje = texto
        self.activa  = True
        self.fin     = pygame.time.get_ticks() + int(duracion * 1000)

    def actualizar(self):
        if self.activa and pygame.time.get_ticks() > self.fin:
            self.activa = False

    def dibujar(self, pantalla):
        if not self.activa:
            return

        ancho_p = 400
        alto_p  = 120
        x = pantalla.get_width() - ancho_p - 20
        y = 80

        if self.imagen:
            img = pygame.transform.scale(self.imagen, (ancho_p, alto_p))
            pantalla.blit(img, (x, y))
        else:
            fondo = pygame.Surface((ancho_p, alto_p), pygame.SRCALPHA)
            fondo.fill((240, 220, 180, 230))
            pantalla.blit(fondo, (x, y))
            pygame.draw.rect(pantalla, (180, 140, 80), (x, y, ancho_p, alto_p), 3)

        # Dividir texto en líneas
        palabras = self.mensaje.split()
        lineas, linea = [], ""
        for p in palabras:
            prueba = linea + " " + p if linea else p
            if self.font.size(prueba)[0] < ancho_p - 20:
                linea = prueba
            else:
                lineas.append(linea)
                linea = p
        if linea:
            lineas.append(linea)

        for i, l in enumerate(lineas[:4]):
            txt = self.font.render(l, True, (80, 50, 20))
            pantalla.blit(txt, (x + 15, y + 15 + i * 24))
