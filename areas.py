import pygame
from settings import *

class GestorAreas:
    def __init__(self):
        # Verificar si estamos en modo de desarrollo (pantalla más pequeña)
        self.modo_desarrollo = False
        
        if self.modo_desarrollo:
            self.ANCHO = 1024
            self.ALTO = 768
        else:
            # Usar pantalla completa
            info = pygame.display.Info()
            self.ANCHO = info.current_w
            self.ALTO = info.current_h
        
        # Definir áreas proporcionales
        self.definir_areas()
        
    def definir_areas(self):
        """Define las áreas proporcionales de la pantalla"""
        # Área del menú superior (15%)
        self.menu_alto = int(self.ALTO * 0.15)
        self.menu_rect = pygame.Rect(0, 0, self.ANCHO, self.menu_alto)
        
        # Área principal de juego (70% del ancho, 70% del alto restante)
        self.juego_ancho = int(self.ANCHO * 0.7)
        self.juego_alto = int((self.ALTO - self.menu_alto) * 0.7)
        self.juego_rect = pygame.Rect(0, self.menu_alto, self.juego_ancho, self.juego_alto)
        
        # Área de inventario (70% del ancho, 30% del alto restante)
        self.inv_alto = (self.ALTO - self.menu_alto) - self.juego_alto
        self.inv_rect = pygame.Rect(0, self.menu_alto + self.juego_alto, 
                                   self.juego_ancho, self.inv_alto)
        
        # Área de UI derecha (30% del ancho total, todo el alto restante)
        self.ui_ancho = self.ANCHO - self.juego_ancho
        self.ui_rect = pygame.Rect(self.juego_ancho, self.menu_alto, 
                                  self.ui_ancho, self.ALTO - self.menu_alto)
        
        # Colores de fondo para cada área
        self.color_menu = (40, 40, 60, 255)
        self.color_juego = (20, 20, 30, 255)
        self.color_inventario = (50, 40, 60, 255)
        self.color_ui = (30, 30, 40, 255)
    
    def crear_superficies(self):
        """Crea superficies para cada área"""
        self.superficie_menu = pygame.Surface((self.menu_rect.width, self.menu_rect.height), pygame.SRCALPHA)
        self.superficie_juego = pygame.Surface((self.juego_rect.width, self.juego_rect.height), pygame.SRCALPHA)
        self.superficie_inventario = pygame.Surface((self.inv_rect.width, self.inv_rect.height), pygame.SRCALPHA)
        self.superficie_ui = pygame.Surface((self.ui_rect.width, self.ui_rect.height), pygame.SRCALPHA)
        
        # Rellenar con colores base
        self.superficie_menu.fill(self.color_menu)
        self.superficie_juego.fill(self.color_juego)
        self.superficie_inventario.fill(self.color_inventario)
        self.superficie_ui.fill(self.color_ui)
    
    def obtener_posicion_relativa(self, pos_absoluta, area):
        """Convierte posición absoluta de pantalla a relativa dentro de un área"""
        if area == "menu":
            return (pos_absoluta[0] - self.menu_rect.x, pos_absoluta[1] - self.menu_rect.y)
        elif area == "juego":
            return (pos_absoluta[0] - self.juego_rect.x, pos_absoluta[1] - self.juego_rect.y)
        elif area == "inventario":
            return (pos_absoluta[0] - self.inv_rect.x, pos_absoluta[1] - self.inv_rect.y)
        elif area == "ui":
            return (pos_absoluta[0] - self.ui_rect.x, pos_absoluta[1] - self.ui_rect.y)
        return pos_absoluta
    
    def esta_en_area(self, pos, area):
        """Verifica si una posición está dentro de un área específica"""
        if area == "menu":
            return self.menu_rect.collidepoint(pos)
        elif area == "juego":
            return self.juego_rect.collidepoint(pos)
        elif area == "inventario":
            return self.inv_rect.collidepoint(pos)
        elif area == "ui":
            return self.ui_rect.collidepoint(pos)
        return False
    
    def dibujar_bordes(self, pantalla):
        """Dibuja bordes entre las áreas para mejor visualización"""
        # Borde entre menú y áreas inferiores
        pygame.draw.line(pantalla, (100, 100, 100), 
                        (0, self.menu_alto), 
                        (self.ANCHO, self.menu_alto), 3)
        
        # Borde vertical entre juego y UI
        pygame.draw.line(pantalla, (100, 100, 100),
                        (self.juego_ancho, self.menu_alto),
                        (self.juego_ancho, self.ALTO), 3)
        
        # Borde horizontal entre juego e inventario
        pygame.draw.line(pantalla, (100, 100, 100),
                        (0, self.menu_alto + self.juego_alto),
                        (self.juego_ancho, self.menu_alto + self.juego_alto), 3)
        
        # Bordes internos sutiles
        for rect, color in [(self.menu_rect, (80, 80, 100)),
                          (self.juego_rect, (60, 60, 80)),
                          (self.inv_rect, (90, 80, 100)),
                          (self.ui_rect, (70, 70, 90))]:
            pygame.draw.rect(pantalla, color, rect, 1)
