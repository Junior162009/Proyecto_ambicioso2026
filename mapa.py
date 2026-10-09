# mapa.py — Mapa de tiles con soporte de túneles y visión
import pygame
import math
from settings import TAM, OSCURIDAD_TUNEL_ALPHA, LUZ_RADIO_TUNEL, LUZ_RADIO_NORMAL

TILES_PARED   = {"1", "#"}
TILES_TUNEL   = {"T"}
TILES_AGUA    = {" "}

class Mapa:
    def __init__(self, nivel, suelo_img, pared_img):
        self.nivel    = nivel
        self.suelo_img = suelo_img
        self.pared_img = pared_img
        self.paredes  = []
        self._construir_paredes()

    def _construir_paredes(self):
        self.paredes = []
        for y, fila in enumerate(self.nivel):
            for x, tile in enumerate(fila):
                if tile in TILES_PARED:
                    self.paredes.append(pygame.Rect(x * TAM, y * TAM, TAM, TAM))

    def es_tunel(self, tile_x, tile_y):
        try:
            return self.nivel[tile_y][tile_x] in TILES_TUNEL
        except IndexError:
            return False

    def dibujar_suelo(self, superficie, cam_x, cam_y, jugador_pos=None, en_tunel=False):
        for y, fila in enumerate(self.nivel):
            for x, tile in enumerate(fila):
                rx = x * TAM - cam_x
                ry = y * TAM - cam_y

                # Culling: no dibujar si está fuera de pantalla
                if rx < -TAM or ry < -TAM or rx > superficie.get_width() + TAM or ry > superficie.get_height() + TAM:
                    continue

                if tile in TILES_PARED:
                    continue

                if tile in TILES_AGUA:
                    pygame.draw.rect(superficie, (40, 80, 160), (rx, ry, TAM, TAM))
                    pygame.draw.rect(superficie, (60, 100, 180), (rx+2, ry+2, TAM-4, TAM-4))
                elif tile in TILES_TUNEL:
                    pygame.draw.rect(superficie, (25, 20, 30), (rx, ry, TAM, TAM))
                    pygame.draw.rect(superficie, (40, 30, 50), (rx, ry, TAM, TAM), 1)
                else:
                    superficie.blit(self.suelo_img, (rx, ry))

    def dibujar_paredes(self, superficie, cam_x, cam_y, jugador_pos=None, en_tunel=False):
        for y, fila in enumerate(self.nivel):
            for x, tile in enumerate(fila):
                rx = x * TAM - cam_x
                ry = y * TAM - cam_y

                if rx < -TAM or ry < -TAM or rx > superficie.get_width() + TAM or ry > superficie.get_height() + TAM:
                    continue

                if tile in TILES_PARED:
                    superficie.blit(self.pared_img, (rx, ry))
                    # Borde sutil
                    pygame.draw.rect(superficie, (0, 0, 0), (rx, ry, TAM, TAM), 1)
