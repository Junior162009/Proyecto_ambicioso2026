# game.py - Gestión principal del juego
"""
Controla el flujo del juego, estados y lógica
"""

import pygame
import random
import config
from player import Player
from enemy import Enemy
from boss import Boss
from levels import LevelManager
from combat import CombatSystem


class GameState:
    """Estados del juego"""
    PLAYING = "playing"
    LEVEL_COMPLETE = "level_complete"
    GAME_OVER = "game_over"
    BOSS_DEFEATED = "boss_defeated"


class Game:
    """Clase principal del juego"""

    def __init__(self, screen):
        """
        Inicializa el juego
        
        Args:
            screen: Superficie de Pygame
        """
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        self.running = True
        self.state = GameState.PLAYING

        self.level_manager = LevelManager()
        self.combat_system = CombatSystem()

        self._init_level()

    def _init_level(self):
        """Inicializa un nivel nuevo"""
        self.enemies = []
        self.boss = None
        self.enemy_spawn_timer = 0

        self.player = Player(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)

        config_data = self.level_manager.get_current_config()

        if self.level_manager.is_boss_level():
            self.boss = Boss(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 4)
        else:
            enemy_count = config_data['enemies']
            for _ in range(enemy_count):
                enemy = Enemy(
                    random.randint(config.ENEMY_SIZE, config.SCREEN_WIDTH - config.ENEMY_SIZE),
                    random.randint(config.ENEMY_SIZE, config.SCREEN_HEIGHT - config.ENEMY_SIZE),
                    hp=int(config_data['enemy_hp'] * config_data['difficulty'])
                )
                self.enemies.append(enemy)

    def handle_input(self):
        """Procesa entrada del usuario"""
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)

        if pygame.mouse.get_pressed()[0]:
            self.combat_system.handle_player_attack(self.player, self.enemies, self.boss)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.state != GameState.PLAYING:
                        self._handle_level_transition()

    def _handle_level_transition(self):
        """Maneja transición entre niveles"""
        if self.state == GameState.LEVEL_COMPLETE:
            if self.level_manager.current_level < self.level_manager.total_levels:
                self.level_manager.next_level()
                self.state = GameState.PLAYING
                self._init_level()
            else:
                self.state = GameState.BOSS_DEFEATED

        elif self.state == GameState.GAME_OVER:
            self.level_manager.current_level = 1
            self.player.hp = self.player.max_hp
            self.state = GameState.PLAYING
            self._init_level()

    def update(self):
        """Actualiza la lógica del juego"""
        if self.state != GameState.PLAYING:
            return

        self.player.update()

        for enemy in self.enemies[:]:
            enemy.update(self.player.rect)

            damage = self.combat_system.handle_enemy_attacks([enemy], self.player)
            if damage > 0:
                self.player.take_damage(damage)

        if self.boss:
            self.boss.update(self.player.rect)

            damage = self.combat_system.handle_boss_attack(self.boss, self.player)
            if damage > 0:
                self.player.take_damage(damage)

        if not self.player.is_alive():
            self.state = GameState.GAME_OVER

        if self.level_manager.is_boss_level():
            if self.boss and not self.boss.is_alive():
                self.state = GameState.LEVEL_COMPLETE
        else:
            if len(self.enemies) == 0:
                if self.enemy_spawn_timer <= 0:
                    config_data = self.level_manager.get_current_config()
                    for _ in range(2):
                        enemy = Enemy(
                            random.randint(config.ENEMY_SIZE, config.SCREEN_WIDTH - config.ENEMY_SIZE),
                            random.randint(config.ENEMY_SIZE, config.SCREEN_HEIGHT - config.ENEMY_SIZE),
                            hp=int(config_data['enemy_hp'] * config_data['difficulty'])
                        )
                        self.enemies.append(enemy)
                    self.enemy_spawn_timer = 120
                self.enemy_spawn_timer -= 1

    def render(self):
        """Dibuja todo en pantalla"""
        self.screen.fill(config.COLOR_BLACK)

        self.player.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        if self.boss:
            self.boss.draw(self.screen)

        self._draw_ui()

        if self.state == GameState.LEVEL_COMPLETE:
            self._draw_level_complete()
        elif self.state == GameState.GAME_OVER:
            self._draw_game_over()
        elif self.state == GameState.BOSS_DEFEATED:
            self._draw_victory()

        pygame.display.flip()

    def _draw_ui(self):
        """Dibuja la UI"""
        player_info = f"HP: {self.player.hp}/{self.player.max_hp}"
        player_text = self.font.render(player_info, True, config.COLOR_WHITE)
        self.screen.blit(player_text, (10, 10))

        level_info = self.level_manager.get_level_info()
        level_text = self.small_font.render(level_info, True, config.COLOR_YELLOW)
        self.screen.blit(level_text, (config.SCREEN_WIDTH // 2 - level_text.get_width() // 2, 10))

        if not self.level_manager.is_boss_level():
            enemy_count = f"Enemies: {len(self.enemies)}"
            enemy_text = self.small_font.render(enemy_count, True, config.COLOR_RED)
            self.screen.blit(enemy_text, (config.SCREEN_WIDTH - enemy_text.get_width() - 10, 10))

    def _draw_level_complete(self):
        """Dibuja mensaje de nivel completado"""
        text = self.font.render("LEVEL COMPLETE!", True, config.COLOR_GREEN)
        subtext = self.small_font.render("Press SPACE to continue", True, config.COLOR_WHITE)

        x = config.SCREEN_WIDTH // 2 - text.get_width() // 2
        y = config.SCREEN_HEIGHT // 2 - 30

        self.screen.blit(text, (x, y))
        self.screen.blit(subtext, (config.SCREEN_WIDTH // 2 - subtext.get_width() // 2, y + 50))

    def _draw_game_over(self):
        """Dibuja mensaje de game over"""
        text = self.font.render("GAME OVER", True, config.COLOR_RED)
        subtext = self.small_font.render("Press SPACE to restart", True, config.COLOR_WHITE)

        x = config.SCREEN_WIDTH // 2 - text.get_width() // 2
        y = config.SCREEN_HEIGHT // 2 - 30

        self.screen.blit(text, (x, y))
        self.screen.blit(subtext, (config.SCREEN_WIDTH // 2 - subtext.get_width() // 2, y + 50))

    def _draw_victory(self):
        """Dibuja mensaje de victoria"""
        text = self.font.render("YOU WIN!", True, config.COLOR_GREEN)
        subtext = self.small_font.render("Press SPACE to play again", True, config.COLOR_WHITE)

        x = config.SCREEN_WIDTH // 2 - text.get_width() // 2
        y = config.SCREEN_HEIGHT // 2 - 30

        self.screen.blit(text, (x, y))
        self.screen.blit(subtext, (config.SCREEN_WIDTH // 2 - subtext.get_width() // 2, y + 50))

    def run(self):
        """Ejecuta el bucle principal del juego"""
        while self.running:
            self.handle_input()
            self.update()
            self.render()
            self.clock.tick(config.FPS)
