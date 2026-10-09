import pygame
from settings import *

class Menu:
    def __init__(self):
        self.fuente_titulo = pygame.font.Font(None, 72)
        self.fuente_opciones = pygame.font.Font(None, 48)
        self.opciones = ["Jugar", "Instrucciones", "Salir"]
        self.seleccionado = 0
    
    def dibujar(self, pantalla):
        pantalla.fill((50, 50, 100))
        
        # Título
        titulo = self.fuente_titulo.render("Mazmorra Matemática", True, (255, 255, 0))
        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 100))
        
        # Opciones
        for i, opcion in enumerate(self.opciones):
            color = (0, 255, 0) if i == self.seleccionado else (255, 255, 255)
            texto = self.fuente_opciones.render(opcion, True, color)
            pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, 250 + i * 60))
    
    def manejar_eventos(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                self.seleccionado = (self.seleccionado - 1) % len(self.opciones)
            elif evento.key == pygame.K_DOWN:
                self.seleccionado = (self.seleccionado + 1) % len(self.opciones)
            elif evento.key == pygame.K_RETURN:
                return self.seleccionado
        return None