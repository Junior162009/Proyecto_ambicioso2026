import pygame
import sys

from mundo import Mundo
from niveles import GestorNiveles
from npc import NPC
from mapa import Mapa
from settings import ANCHO, ALTO, TAM, FPS

pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("MindMath 2026 - Batalla Matemática")
clock = pygame.time.Clock()


class Jugador:
    """Jugador básico del modo mundo abierto, con colisiones por eje."""

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TAM, TAM)
        self.vel = 4

    def mover(self, teclas, paredes):
        dx = (int(teclas[pygame.K_d]) - int(teclas[pygame.K_a])) * self.vel
        dy = (int(teclas[pygame.K_s]) - int(teclas[pygame.K_w])) * self.vel

        self.rect.x += dx
        for pared in paredes:
            if self.rect.colliderect(pared):
                if dx > 0:
                    self.rect.right = pared.left
                elif dx < 0:
                    self.rect.left = pared.right

        self.rect.y += dy
        for pared in paredes:
            if self.rect.colliderect(pared):
                if dy > 0:
                    self.rect.bottom = pared.top
                elif dy < 0:
                    self.rect.top = pared.bottom

    def dibujar(self, superficie, cam_x, cam_y):
        pygame.draw.rect(
            superficie,
            (0, 255, 0),
            (self.rect.x - cam_x, self.rect.y - cam_y, self.rect.width, self.rect.height),
        )


class Enemigo:
    """Enemigo básico que persigue al jugador."""

    def __init__(self, x, y, multiplicador=1.0):
        self.rect = pygame.Rect(x, y, TAM, TAM)
        self.vida = max(1, int(10 * multiplicador))
        self.vel = max(1, int(2 * multiplicador))

    def update(self, jugador):
        # Evita que el enemigo se mueva en diagonal más rápido que en recta.
        dx = jugador.rect.centerx - self.rect.centerx
        dy = jugador.rect.centery - self.rect.centery
        if dx:
            self.rect.x += min(self.vel, dx) if dx > 0 else max(-self.vel, dx)
        if dy:
            self.rect.y += min(self.vel, dy) if dy > 0 else max(-self.vel, dy)

    def dibujar(self, superficie, cam_x, cam_y):
        pygame.draw.rect(
            superficie,
            (255, 0, 0),
            (self.rect.x - cam_x, self.rect.y - cam_y, self.rect.width, self.rect.height),
        )


class Juego:
    def __init__(self):
        self.mundo = Mundo()
        self.niveles = GestorNiveles()
        self.jugador = Jugador(100, 100)
        self.enemigos = []
        self.npcs = []
        self.mapa = None
        self.cargar_area()

    def cargar_area(self):
        self.enemigos.clear()
        self.npcs.clear()
        mapa_data = self.mundo.area_actual.mapa

        # Superficies visibles para que el mapa no dependa de superficies vacías.
        suelo = pygame.Surface((TAM, TAM))
        suelo.fill((70, 110, 70))
        pared = pygame.Surface((TAM, TAM))
        pared.fill((75, 75, 85))
        self.mapa = Mapa(mapa_data, suelo, pared)

        for y, fila in enumerate(mapa_data):
            for x, tile in enumerate(fila):
                px, py = x * TAM, y * TAM
                if tile == "P":
                    self.jugador.rect.topleft = (px, py)
                elif tile == "E" and not self.mundo.area_actual.es_segura:
                    self.enemigos.append(Enemigo(px, py))
                elif tile == "N" and self.mundo.area_actual.tipo in ("pueblo", "aldea"):
                    self.npcs.append(
                        NPC(px, py, "aldeano", "NPC", ["Hola aventurero"])
                    )

    def update(self):
        teclas = pygame.key.get_pressed()
        self.jugador.mover(teclas, self.mapa.paredes)

        for enemigo in self.enemigos[:]:
            enemigo.update(self.jugador)

        # No se sube de nivel automáticamente cada fotograma. La progresión debe
        # activarse mediante un evento explícito al completar el nivel.

    def draw(self):
        pantalla.fill((20, 20, 20))
        cam_x = max(0, self.jugador.rect.centerx - ANCHO // 2)
        cam_y = max(0, self.jugador.rect.centery - ALTO // 2)

        self.mapa.dibujar_suelo(pantalla, cam_x, cam_y)
        self.mapa.dibujar_paredes(pantalla, cam_x, cam_y)

        for npc in self.npcs:
            npc.dibujar(pantalla, cam_x, cam_y)
        for enemigo in self.enemigos:
            enemigo.dibujar(pantalla, cam_x, cam_y)
        self.jugador.dibujar(pantalla, cam_x, cam_y)
        pygame.display.flip()

    def run(self):
        ejecutando = True
        while ejecutando:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ejecutando = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    conexiones = self.mundo.area_actual.conexiones
                    if conexiones:
                        siguiente_area = conexiones[0]
                        if self.mundo.cambiar_area(siguiente_area):
                            self.cargar_area()

            self.update()
            self.draw()

        pygame.quit()


if __name__ == "__main__":
    Juego().run()
