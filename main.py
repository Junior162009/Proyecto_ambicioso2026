import pygame
import sys
import random

from mundo import Mundo
from niveles import GestorNiveles
from npc import NPC
from mapa import Mapa

# ===============================
# CONFIG
# ===============================
ANCHO = 800
ALTO = 600
TAM = 32

pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego Mundo Abierto")
clock = pygame.time.Clock()

# ===============================
# CLASE JUGADOR
# ===============================
class Jugador:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TAM, TAM)
        self.vel = 4

    def mover(self, teclas, paredes):
        dx, dy = 0, 0

        if teclas[pygame.K_w]: dy = -self.vel
        if teclas[pygame.K_s]: dy = self.vel
        if teclas[pygame.K_a]: dx = -self.vel
        if teclas[pygame.K_d]: dx = self.vel

        # mover X
        self.rect.x += dx
        for p in paredes:
            if self.rect.colliderect(p):
                if dx > 0:
                    self.rect.right = p.left
                if dx < 0:
                    self.rect.left = p.right

        # mover Y
        self.rect.y += dy
        for p in paredes:
            if self.rect.colliderect(p):
                if dy > 0:
                    self.rect.bottom = p.top
                if dy < 0:
                    self.rect.top = p.bottom

    def dibujar(self, superficie, cam_x, cam_y):
        pygame.draw.rect(superficie, (0, 255, 0),
                         (self.rect.x - cam_x, self.rect.y - cam_y, TAM, TAM))


# ===============================
# ENEMIGO SIMPLE
# ===============================
class Enemigo:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TAM, TAM)
        self.vida = 10
        self.vel = 2

    def update(self, jugador):
        if jugador.rect.x > self.rect.x:
            self.rect.x += self.vel
        if jugador.rect.x < self.rect.x:
            self.rect.x -= self.vel
        if jugador.rect.y > self.rect.y:
            self.rect.y += self.vel
        if jugador.rect.y < self.rect.y:
            self.rect.y -= self.vel

    def dibujar(self, superficie, cam_x, cam_y):
        pygame.draw.rect(superficie, (255, 0, 0),
                         (self.rect.x - cam_x, self.rect.y - cam_y, TAM, TAM))


# ===============================
# JUEGO
# ===============================
class Juego:
    def __init__(self):
        self.mundo = Mundo()
        self.niveles = SistemaNiveles()

        self.jugador = Jugador(100, 100)

        self.enemigos = []
        self.npcs = []

        self.cargar_area()

    # ===============================
    # CARGAR ÁREA
    # ===============================
    def cargar_area(self):
        self.enemigos.clear()
        self.npcs.clear()

        mapa_data = self.mundo.area_actual.mapa

        self.mapa = Mapa(
            mapa_data,
            pygame.Surface((TAM, TAM)),
            pygame.Surface((TAM, TAM))
        )

        for y, fila in enumerate(mapa_data):
            for x, tile in enumerate(fila):

                px = x * TAM
                py = y * TAM

                if tile == "P":
                    self.jugador.rect.topleft = (px, py)

                elif tile == "E" and not self.mundo.area_actual.es_segura:
                    enemigo = Enemigo(px, py)

                    # aplicar dificultad
                    mult = self.niveles.obtener_multiplicador()
                    enemigo.vida = int(enemigo.vida * mult)
                    enemigo.vel *= mult

                    self.enemigos.append(enemigo)

                elif tile == "N" and self.mundo.area_actual.tipo in ["pueblo", "aldea"]:
                    npc = NPC(px, py, "aldeano", "NPC", ["Hola aventurero"])
                    self.npcs.append(npc)

    # ===============================
    # UPDATE
    # ===============================
    def update(self):
        teclas = pygame.key.get_pressed()

        self.jugador.mover(teclas, self.mapa.paredes)

        for enemigo in self.enemigos:
            enemigo.update(self.jugador)

        # subir nivel si no hay enemigos
        if len(self.enemigos) == 0:
            self.niveles.subir_nivel()

    # ===============================
    # DIBUJO
    # ===============================
    def draw(self):
        pantalla.fill((20, 20, 20))

        cam_x = self.jugador.rect.x - ANCHO // 2
        cam_y = self.jugador.rect.y - ALTO // 2

        self.mapa.dibujar_suelo(pantalla, cam_x, cam_y)
        self.mapa.dibujar_paredes(pantalla, cam_x, cam_y)

        for npc in self.npcs:
            npc.dibujar(pantalla, cam_x, cam_y)

        for enemigo in self.enemigos:
            enemigo.dibujar(pantalla, cam_x, cam_y)

        self.jugador.dibujar(pantalla, cam_x, cam_y)

        pygame.display.flip()

    # ===============================
    # LOOP
    # ===============================
    def run(self):
        while True:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        # cambiar área (debug)
                        for a in self.mundo.area_actual.conexiones:
                            self.mundo.cambiar_area(a)
                            self.cargar_area()
                            break

            self.update()
            self.draw()


# ===============================
# RUN
# ===============================
if __name__ == "__main__":
    juego = Juego()
    juego.run()
