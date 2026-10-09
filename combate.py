# combat.py - Sistema de combate
"""
Maneja colisiones, daño y mecánicas de combate
"""

import config


class CombatSystem:
    """Sistema de combate del juego"""

    def __init__(self):
        """Inicializa el sistema de combate"""
        pass

    def handle_player_attack(self, player, enemies, boss=None):
        """
        Maneja ataque del jugador
        
        Args:
            player: Objeto del jugador
            enemies: Lista de enemigos
            boss: Objeto del boss (opcional)
        
        Returns:
            int: Daño total
        """
        if player.attack_cooldown > 0:
            return 0

        total_damage = 0
        attack_range = 100

        for enemy in enemies[:]:
            distance = self._distance(player.rect.center, enemy.rect.center)
            if distance < attack_range:
                enemy.take_damage(player.attack_damage)
                total_damage += player.attack_damage

                if not enemy.is_alive():
                    enemies.remove(enemy)

        if boss and boss.is_alive():
            distance = self._distance(player.rect.center, boss.rect.center)
            if distance < attack_range + 30:
                boss.take_damage(player.attack_damage)
                total_damage += player.attack_damage

        if total_damage > 0:
            player.attack_cooldown = config.ATTACK_COOLDOWN

        return total_damage

    def handle_enemy_attacks(self, enemies, player):
        """
        Maneja ataques de enemigos
        
        Args:
            enemies: Lista de enemigos
            player: Objeto del jugador
        
        Returns:
            int: Daño total recibido
        """
        total_damage = 0
        collision_distance = config.PLAYER_SIZE + config.ENEMY_SIZE

        for enemy in enemies:
            distance = self._distance(player.rect.center, enemy.rect.center)
            if distance < collision_distance:
                if enemy.attack_cooldown <= 0:
                    total_damage += enemy.damage
                    enemy.attack_cooldown = config.ATTACK_COOLDOWN

        return total_damage

    def handle_boss_attack(self, boss, player):
        """
        Maneja ataque del boss
        
        Args:
            boss: Objeto del boss
            player: Objeto del jugador
        
        Returns:
            int: Daño infligido
        """
        total_damage = 0
        collision_distance = config.PLAYER_SIZE + config.BOSS_SIZE

        distance = self._distance(player.rect.center, boss.rect.center)
        if distance < collision_distance and boss.can_attack():
            total_damage = boss.damage
            boss.prepare_attack()

        return total_damage

    @staticmethod
    def _distance(pos1, pos2):
        """Calcula distancia entre dos posiciones"""
        return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5
