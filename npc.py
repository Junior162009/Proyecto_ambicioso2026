# npc.py - SISTEMA DE NPCs
import pygame
from settings import *

class NPC:
    def __init__(self, x, y, tipo, nombre, dialogo, misiones=None):
        self.rect = pygame.Rect(x, y, TAM, TAM)
        self.tipo = tipo  # "aldeano", "profesor", "comerciante", "explorador"
        self.nombre = nombre
        self.dialogo = dialogo
        self.misiones = misiones or []
        self.hablando = False
        self.dialogo_actual = 0

        # Crear sprite según tipo
        self.sprite = self.crear_sprite()

    def crear_sprite(self):
        """Crea un sprite visual para el NPC"""
        sprite = pygame.Surface((TAM, TAM), pygame.SRCALPHA)

        if self.tipo == "profesor":
            pygame.draw.circle(sprite, (100, 100, 255), (TAM//2, TAM//2), TAM//2 - 4)
            pygame.draw.circle(sprite, (255, 255, 255), (TAM//2 - 8, TAM//2 - 5), 6)
            pygame.draw.circle(sprite, (255, 255, 255), (TAM//2 + 8, TAM//2 - 5), 6)
            pygame.draw.rect(sprite, (0, 0, 0), (TAM//2 - 15, TAM//2 + 10, 30, 4))
        elif self.tipo == "aldeano":
            pygame.draw.circle(sprite, (255, 200, 150), (TAM//2, TAM//2), TAM//2 - 4)
            pygame.draw.circle(sprite, (100, 50, 0), (TAM//2 - 8, TAM//2 - 5), 6)
            pygame.draw.circle(sprite, (100, 50, 0), (TAM//2 + 8, TAM//2 - 5), 6)
            pygame.draw.arc(sprite, (0, 0, 0), (TAM//2 - 10, TAM//2 + 5, 20, 10), 0, 3.14, 3)
        elif self.tipo == "comerciante":
            pygame.draw.circle(sprite, (255, 220, 100), (TAM//2, TAM//2), TAM//2 - 4)
            pygame.draw.circle(sprite, (0, 100, 0), (TAM//2 - 8, TAM//2 - 5), 6)
            pygame.draw.circle(sprite, (0, 100, 0), (TAM//2 + 8, TAM//2 - 5), 6)
            pygame.draw.circle(sprite, (200, 0, 0), (TAM//2, TAM//2 + 8), 8)
        elif self.tipo == "explorador":
            pygame.draw.circle(sprite, (150, 255, 150), (TAM//2, TAM//2), TAM//2 - 4)
            pygame.draw.circle(sprite, (50, 100, 50), (TAM//2 - 8, TAM//2 - 5), 6)
            pygame.draw.circle(sprite, (50, 100, 50), (TAM//2 + 8, TAM//2 - 5), 6)
            pygame.draw.rect(sprite, (100, 50, 0), (TAM//2 - 12, TAM//2 + 5, 24, 8))
        elif self.tipo == "guerrero":
            pygame.draw.circle(sprite, (200, 100, 100), (TAM//2, TAM//2), TAM//2 - 4)
            pygame.draw.circle(sprite, (50, 50, 50), (TAM//2 - 8, TAM//2 - 5), 6)
            pygame.draw.circle(sprite, (50, 50, 50), (TAM//2 + 8, TAM//2 - 5), 6)
            pygame.draw.rect(sprite, (100, 0, 0), (TAM//2 - 10, TAM//2 + 5, 20, 6))
        elif self.tipo == "mago":
            pygame.draw.circle(sprite, (200, 100, 255), (TAM//2, TAM//2), TAM//2 - 4)
            pygame.draw.circle(sprite, (255, 255, 255), (TAM//2 - 8, TAM//2 - 5), 6)
            pygame.draw.circle(sprite, (255, 255, 255), (TAM//2 + 8, TAM//2 - 5), 6)
            pygame.draw.polygon(sprite, (100, 50, 200), [(TAM//2 - 5, TAM//2 + 10),
                                                         (TAM//2 + 5, TAM//2 + 10),
                                                         (TAM//2, TAM//2 + 20)])
        else:  # curandero por defecto
            pygame.draw.circle(sprite, (150, 255, 200), (TAM//2, TAM//2), TAM//2 - 4)
            pygame.draw.circle(sprite, (50, 150, 100), (TAM//2 - 8, TAM//2 - 5), 6)
            pygame.draw.circle(sprite, (50, 150, 100), (TAM//2 + 8, TAM//2 - 5), 6)
            pygame.draw.circle(sprite, (255, 100, 100), (TAM//2, TAM//2 + 8), 8)

        return sprite

    def hablar(self, jugador, sistema_misiones):
        """Inicia conversación con el NPC"""
        self.hablando = True
        self.dialogo_actual = 0

        # Si tiene misiones, agregarlas al sistema
        if self.misiones:
            for mision_id in self.misiones:
                # Solo agregar misiones que no estén ya disponibles
                misiones_disponibles_ids = [m.id for m in sistema_misiones.misiones_disponibles]
                if mision_id not in misiones_disponibles_ids:
                    # Buscar la misión en las misiones base
                    for mision_base in sistema_misiones.cargar_misiones_base():
                        if mision_base.id == mision_id:
                            sistema_misiones.misiones_disponibles.append(mision_base)
                            break

        return self.dialogo[self.dialogo_actual]

    def siguiente_dialogo(self):
        """Avanza al siguiente diálogo"""
        if self.dialogo_actual < len(self.dialogo) - 1:
            self.dialogo_actual += 1
            return self.dialogo[self.dialogo_actual]
        else:
            self.hablando = False
            return None

    def tiene_misiones(self):
        """Verifica si el NPC tiene misiones"""
        return len(self.misiones) > 0

    def dibujar(self, pantalla, cam_x, cam_y):
        """Dibuja el NPC"""
        pantalla.blit(self.sprite, (self.rect.x - cam_x, self.rect.y - cam_y))

        # Indicador de misión disponible
        if self.tiene_misiones():
            pygame.draw.circle(pantalla, (255, 255, 0),
                             (self.rect.centerx - cam_x, self.rect.top - cam_y - 5), 5)
