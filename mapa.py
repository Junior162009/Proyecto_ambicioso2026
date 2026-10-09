# mapa.py — Renderizado de tiles con colisiones y culling
import pygame
from settings import TAM, OSCURIDAD_TUNEL_ALPHA, LUZ_RADIO_TUNEL, LUZ_RADIO_NORMAL

TILES_PARED = {"1", "#"}
TILES_TUNEL = {"T"}
# Los espacios son caminos transitables del pueblo, no agua.
TILES_AGUA = {"~"}


class Mapa:
    def __init__(self, nivel, suelo_img, pared_img):
        self.nivel = nivel
        self.suelo_img = suelo_img
        self.pared_img = pared_img
        self.paredes = []
        self._construir_paredes()

    def _construir_paredes(self):
        self.paredes = [
            pygame.Rect(x * TAM, y * TAM, TAM, TAM)
            for y, fila in enumerate(self.nivel)
            for x, tile in enumerate(fila)
            if tile in TILES_PARED
        ]

    def es_tunel(self, tile_x, tile_y):
        return (
            0 <= tile_y < len(self.nivel)
            and 0 <= tile_x < len(self.nivel[tile_y])
            and self.nivel[tile_y][tile_x] in TILES_TUNEL
        )

    def dibujar_suelo(self, superficie, cam_x, cam_y, jugador_pos=None, en_tunel=False):
        alto, ancho = superficie.get_height(), superficie.get_width()
        for y, fila in enumerate(self.nivel):
            ry = y * TAM - cam_y
            if ry < -TAM or ry > alto + TAM:
                continue
            for x, tile in enumerate(fila):
                rx = x * TAM - cam_x
                if rx < -TAM or rx > ancho + TAM or tile in TILES_PARED:
                    continue
                rect = (rx, ry, TAM, TAM)
                if tile in TILES_AGUA:
                    pygame.draw.rect(superficie, (40, 80, 160), rect)
                    pygame.draw.rect(superficie, (60, 100, 180), (rx + 2, ry + 2, TAM - 4, TAM - 4))
                elif tile in TILES_TUNEL:
                    pygame.draw.rect(superficie, (25, 20, 30), rect)
                    pygame.draw.rect(superficie, (40, 30, 50), rect, 1)
                else:
                    superficie.blit(self.suelo_img, (rx, ry))

    def dibujar_paredes(self, superficie, cam_x, cam_y, jugador_pos=None, en_tunel=False):
        alto, ancho = superficie.get_height(), superficie.get_width()
        for y, fila in enumerate(self.nivel):
            ry = y * TAM - cam_y
            if ry < -TAM or ry > alto + TAM:
                continue
            for x, tile in enumerate(fila):
                rx = x * TAM - cam_x
                if rx < -TAM or rx > ancho + TAM:
                    continue
                if tile in TILES_PARED:
                    superficie.blit(self.pared_img, (rx, ry))
                    pygame.draw.rect(superficie, (0, 0, 0), (rx, ry, TAM, TAM), 1)
