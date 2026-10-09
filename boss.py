"""Jefe final compatible con el sistema de combate existente."""
import math
import pygame
import config

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((config.BOSS_SIZE, config.BOSS_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, config.COLOR_PURPLE, (config.BOSS_SIZE // 2, config.BOSS_SIZE // 2), config.BOSS_SIZE // 2 - 2)
        pygame.draw.circle(self.image, config.COLOR_YELLOW, (config.BOSS_SIZE // 2, config.BOSS_SIZE // 2), config.BOSS_SIZE // 2 - 8, 4)
        self.rect = self.image.get_rect(center=(x, y))
        self.max_hp = config.BOSS_MAX_HP
        self.hp = self.max_hp
        self.speed = config.BOSS_SPEED
        self.damage = config.BOSS_DAMAGE
        self.attack_cooldown = 0

    def update(self, player_rect):
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist > 1:
            self.rect.x += round(dx / dist * self.speed)
            self.rect.y += round(dy / dist * self.speed)
        self.rect.clamp_ip(pygame.Rect(0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def can_attack(self):
        return self.attack_cooldown <= 0

    def prepare_attack(self):
        self.attack_cooldown = config.BOSS_ATTACK_COOLDOWN

    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)

    def is_alive(self):
        return self.hp > 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, config.COLOR_RED, (self.rect.x, self.rect.y - 10, self.rect.width, 6))
        width = int(self.rect.width * self.hp / self.max_hp)
        pygame.draw.rect(surface, config.COLOR_GREEN, (self.rect.x, self.rect.y - 10, width, 6))
