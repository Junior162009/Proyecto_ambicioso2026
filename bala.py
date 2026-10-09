# bala.py — Balas del jugador y enemigas
import pygame
import math

TAM_BALA = 8

class Bala:
    def __init__(self, x, y, destino_x, destino_y, velocidad=10):
        self.rect = pygame.Rect(x - TAM_BALA//2, y - TAM_BALA//2, TAM_BALA, TAM_BALA)
        dist = max(1, math.hypot(destino_x - x, destino_y - y))
        self.dx = (destino_x - x) / dist * velocidad
        self.dy = (destino_y - y) / dist * velocidad

    def mover(self):
        self.rect.x += int(self.dx)
        self.rect.y += int(self.dy)

    def dibujar(self, superficie, cam_x=0, cam_y=0):
        rx = self.rect.x - cam_x
        ry = self.rect.y - cam_y
        pygame.draw.circle(superficie, (255, 255, 100), (rx + TAM_BALA//2, ry + TAM_BALA//2), TAM_BALA//2)
        pygame.draw.circle(superficie, (255, 200, 0),   (rx + TAM_BALA//2, ry + TAM_BALA//2), TAM_BALA//2, 2)


class BalaEnemiga:
    def __init__(self, x, y, destino_x, destino_y, tipo="Básico", velocidad=5):
        self.rect = pygame.Rect(x - 5, y - 5, 10, 10)
        dist = max(1, math.hypot(destino_x - x, destino_y - y))
        self.dx = (destino_x - x) / dist * velocidad
        self.dy = (destino_y - y) / dist * velocidad
        self.tipo = tipo
        colores = {"Básico": (255,80,80), "Camuflado": (80,255,80), "Disparador": (80,80,255)}
        self.color = colores.get(tipo, (200,200,200))

    def mover(self):
        self.rect.x += int(self.dx)
        self.rect.y += int(self.dy)

    def dibujar(self, superficie, cam_x=0, cam_y=0):
        rx = self.rect.x - cam_x
        ry = self.rect.y - cam_y
        pygame.draw.circle(superficie, self.color, (rx+5, ry+5), 5)
        pygame.draw.circle(superficie, (255,255,255), (rx+5, ry+5), 2)
