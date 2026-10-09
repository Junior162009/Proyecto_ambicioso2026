"""Adaptador entre game.py y el gestor de niveles en español."""
from settings import LEVEL_CONFIG, TOTAL_LEVELS

class LevelManager:
    def __init__(self):
        self.current_level = 1
        self.total_levels = TOTAL_LEVELS

    def get_current_config(self):
        return LEVEL_CONFIG.get(self.current_level, LEVEL_CONFIG[self.total_levels])

    def is_boss_level(self):
        return bool(self.get_current_config().get("boss", False))

    def next_level(self):
        if self.current_level < self.total_levels:
            self.current_level += 1
        return self.current_level

    def get_level_info(self):
        data = self.get_current_config()
        if self.is_boss_level():
            return f"Nivel {self.current_level} - JEFE FINAL"
        return f"Nivel {self.current_level} - Enemigos: {data['enemies']} - Dificultad x{data['difficulty']:.1f}"
