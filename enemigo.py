# enemy.py - Lógica de enemigos
"""
Gestiona movimiento, IA y combate de enemigos
"""

import pygame
import random
import math
import config


class Enemy(pygame.sprite.Sprite):
    """Clase que representa un enemigo"""

    def __init__(self, x, y, hp=config.ENEMY_MAX_HP):
        """
        Inicializa un enemigo

        Args:
            x (int): Posición X
            y (int): Posición Y
            hp (int): Puntos de vida
        """
        super().__init__()
        self.image = pygame.Surface((config.ENEMY_SIZE, config.ENEMY_SIZE))
        self.image.fill(config.COLOR_RED)
        self.rect = self.image.get_rect(center=(x, y))

        self.max_hp = hp
        self.hp = hp

        self.velocity_x = random.uniform(-config.ENEMY_SPEED, config.ENEMY_SPEED)
        self.velocity_y = random.uniform(-config.ENEMY_SPEED, config.ENEMY_SPEED)
        self.speed = config.ENEMY_SPEED

        self.damage = config.ENEMY_DAMAGE
        self.attack_cooldown = 0

        self.direction_change_timer = 0

    def update(self, player_rect):
        """Actualiza enemigo"""
        self.direction_change_timer -= 1
        if self.direction_change_timer <= 0:
            self._change_direction(player_rect)
            self.direction_change_timer = random.randint(60, 180)

        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # Rebotar en límites
        if self.rect.left < 0 or self.rect.right > config.SCREEN_WIDTH:
            self.velocity_x *= -1
        if self.rect.top < 0 or self.rect.bottom > config.SCREEN_HEIGHT:
            self.velocity_y *= -1

        self.rect.x = max(0, min(self.rect.x, config.SCREEN_WIDTH - config.ENEMY_SIZE))
        self.rect.y = max(0, min(self.rect.y, config.SCREEN_HEIGHT - config.ENEMY_SIZE))

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def _change_direction(self, player_rect):
        """IA simple: perseguir al jugador"""
        if random.random() < 0.7:
            dx = player_rect.centerx - self.rect.centerx
            dy = player_rect.centery - self.rect.centery
            distance = math.sqrt(dx**2 + dy**2)

            if distance > 0:
                self.velocity_x = (dx / distance) * self.speed
                self.velocity_y = (dy / distance) * self.speed
        else:
            angle = random.uniform(0, 2 * math.pi)
            self.velocity_x = math.cos(angle) * self.speed
            self.velocity_y = math.sin(angle) * self.speed

    def take_damage(self, damage):
        """Recibe daño"""
        self.hp = max(0, self.hp - damage)

    def is_alive(self):
        """¿Está vivo?"""
        return self.hp > 0

    def draw(self, surface):
        """Dibuja el enemigo"""
        surface.blit(self.image, self.rect)
        self._draw_health_bar(surface)

    def _draw_health_bar(self, surface):
        """Dibuja barra de vida"""
        bar_width = config.ENEMY_SIZE
        bar_height = 4
        bar_x = self.rect.x
        bar_y = self.rect.y - 8

        pygame.draw.rect(surface, config.COLOR_RED, (bar_x, bar_y, bar_width, bar_height))
        health_percentage = self.hp / self.max_hp
        pygame.draw.rect(surface, config.COLOR_GREEN, (bar_x, bar_y, bar_width * health_percentage, bar_height))
