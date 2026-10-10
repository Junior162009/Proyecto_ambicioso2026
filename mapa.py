# mapa.py — Mapa precalculado en una sola capa opaca para acelerar el renderizado
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
        self._paredes_por_celda = {}
        self._capa_mapa = None
        self._construir_paredes()
        self._construir_capa_mapa()

    def _construir_paredes(self):
        self.paredes = []
        self._paredes_por_celda = {}
        for y, fila in enumerate(self.nivel):
            for x, tile in enumerate(fila):
                if tile in TILES_PARED:
                    pared = pygame.Rect(x * TAM, y * TAM, TAM, TAM)
                    self.paredes.append(pared)
                    self._paredes_por_celda[(x, y)] = pared

    def paredes_cercanas(self, rect, margen=1):
        """Devuelve solo paredes de las celdas cercanas a un objeto."""
        x0 = max(0, rect.left // TAM - margen)
        y0 = max(0, rect.top // TAM - margen)
        x1 = min(max((len(fila) for fila in self.nivel), default=1) - 1,
                 rect.right // TAM + margen)
        y1 = min(len(self.nivel) - 1, rect.bottom // TAM + margen)
        return [
            pared
            for y in range(y0, y1 + 1)
            for x in range(x0, x1 + 1)
            if (pared := self._paredes_por_celda.get((x, y))) is not None
        ]

    def _construir_capa_mapa(self):
        """Pre-renderiza suelo y paredes en una sola superficie opaca."""
        alto = max(1, len(self.nivel) * TAM)
        ancho = max(1, max((len(fila) for fila in self.nivel), default=1) * TAM)
        # Sin SRCALPHA: el blit por fotograma no necesita mezclar canales alfa.
        capa = pygame.Surface((ancho, alto)).convert()
        capa.fill((70, 115, 70))

        for y, fila in enumerate(self.nivel):
            for x, tile in enumerate(fila):
                px, py = x * TAM, y * TAM
                if tile in TILES_PARED:
                    capa.blit(self.pared_img, (px, py))
                    pygame.draw.rect(capa, (0, 0, 0), (px, py, TAM, TAM), 1)
                elif tile in TILES_AGUA:
                    pygame.draw.rect(capa, (40, 80, 160), (px, py, TAM, TAM))
                    pygame.draw.rect(capa, (60, 100, 180), (px + 2, py + 2, TAM - 4, TAM - 4))
                elif tile in TILES_TUNEL:
                    pygame.draw.rect(capa, (25, 20, 30), (px, py, TAM, TAM))
                    pygame.draw.rect(capa, (40, 30, 50), (px, py, TAM, TAM), 1)
                else:
                    capa.blit(self.suelo_img, (px, py))
        self._capa_mapa = capa

    def es_tunel(self, tile_x, tile_y):
        return (
            0 <= tile_y < len(self.nivel)
            and 0 <= tile_x < len(self.nivel[tile_y])
            and self.nivel[tile_y][tile_x] in TILES_TUNEL
        )

    def dibujar_suelo(self, superficie, cam_x, cam_y, jugador_pos=None, en_tunel=False):
        # Un solo blit opaco contiene tanto suelo como paredes.
        superficie.blit(self._capa_mapa, (-cam_x, -cam_y))

    def dibujar_paredes(self, superficie, cam_x, cam_y, jugador_pos=None, en_tunel=False):
        # Las paredes ya están incluidas en _capa_mapa; se conserva la API existente.
        return
