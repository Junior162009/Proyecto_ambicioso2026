# player.py - Lógica del jugador
"""
Gestiona movimiento, vida, ataque y colisiones del jugador
"""

import pygame
import config


class Player(pygame.sprite.Sprite):
    """Clase que representa al jugador"""

    def __init__(self, x, y):
        """
        Inicializa el jugador

        Args:
            x (int): Posición X inicial
            y (int): Posición Y inicial
        """
        super().__init__()
        self.image = pygame.Surface((config.PLAYER_SIZE, config.PLAYER_SIZE))
        self.image.fill(config.COLOR_BLUE)
        self.rect = self.image.get_rect(center=(x, y))

        # Salud
        self.max_hp = config.PLAYER_MAX_HP
        self.hp = config.PLAYER_INITIAL_HP

        # Movimiento
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = config.PLAYER_SPEED

        # Combate
        self.attack_cooldown = 0
        self.attack_damage = config.ATTACK_DAMAGE

        # Inventario y progresión usados por tienda.py y progresion.py.
        self.inventario = {}
        self.experiencia = 0
        self.nivel = 1

    def handle_input(self, keys):
        """
        Procesa entrada del teclado

        Args:
            keys (dict): Estados de teclas
        """
        self.velocity_x = 0
        self.velocity_y = 0

        if keys[pygame.K_w]:
            self.velocity_y = -self.speed
        if keys[pygame.K_s]:
            self.velocity_y = self.speed
        if keys[pygame.K_a]:
            self.velocity_x = -self.speed
        if keys[pygame.K_d]:
            self.velocity_x = self.speed

    def update(self):
        """Actualiza al jugador"""
        # Mover
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # Limitar dentro de pantalla
        self.rect.x = max(0, min(self.rect.x, config.SCREEN_WIDTH - config.PLAYER_SIZE))
        self.rect.y = max(0, min(self.rect.y, config.SCREEN_HEIGHT - config.PLAYER_SIZE))

        # Cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def take_damage(self, damage):
        """Recibe daño"""
        self.hp = max(0, self.hp - damage)

    def is_alive(self):
        """¿Está vivo?"""
        return self.hp > 0

    def agregar_item(self, item_id, cantidad=1):
        """Añade un artículo al inventario del jugador."""
        self.inventario[item_id] = self.inventario.get(item_id, 0) + max(1, int(cantidad))
        return self.inventario[item_id]

    def ganar_experiencia(self, cantidad):
        """Suma experiencia y actualiza el nivel sin bajar nunca de nivel 1."""
        self.experiencia = max(0, self.experiencia + int(cantidad))
        self.nivel = 1 + self.experiencia // 100
        return self.nivel

    def draw(self, surface):
        """Dibuja el jugador"""
        surface.blit(self.image, self.rect)
        self._draw_health_bar(surface)

    def _draw_health_bar(self, surface):
        """Dibuja barra de vida"""
        bar_width = config.PLAYER_SIZE
        bar_height = 5
        bar_x = self.rect.x
        bar_y = self.rect.y - 10

        pygame.draw.rect(surface, config.COLOR_RED, (bar_x, bar_y, bar_width, bar_height))
        health_percentage = self.hp / self.max_hp
        pygame.draw.rect(surface, config.COLOR_GREEN, (bar_x, bar_y, bar_width * health_percentage, bar_height))
