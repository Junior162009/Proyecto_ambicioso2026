import pygame
from settings import *

class Puerta:
    def __init__(self, x, y):
        try:
            self.img = pygame.image.load("assets/objetos/puerta.png").convert_alpha()
            self.img = pygame.transform.scale(self.img, (TAM, TAM))
        except:
            # Crear puerta temporal
            self.img = pygame.Surface((TAM, TAM))
            self.img.fill((160, 120, 80))
            pygame.draw.rect(self.img, (100, 70, 40), (0, 0, TAM, TAM), 3)
            pygame.draw.rect(self.img, (200, 150, 100), (TAM//4, TAM//4, TAM//2, TAM//2))
        
        self.rect = self.img.get_rect(topleft=(x, y))
        self.abierta = False
    
    def dibujar(self, pantalla, cam_x=0, cam_y=0):
        pantalla.blit(self.img, (self.rect.x - cam_x, self.rect.y - cam_y))