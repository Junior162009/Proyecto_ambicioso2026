# settings.py - Configuración centralizada y compatibilidad
"""Configuración centralizada del juego MindMath 2026."""

# Pantalla
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
ANCHO = SCREEN_WIDTH
ALTO = SCREEN_HEIGHT
FPS = 60
TITLE = "MindMath 2026 - Batalla Matemática"

# Tamaño base de tiles y constantes de iluminación usadas por mapa.py / npc.py
TAM = 32
OSCURIDAD_TUNEL_ALPHA = 170
LUZ_RADIO_TUNEL = 96
LUZ_RADIO_NORMAL = 180

# Colores
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_GRAY = (128, 128, 128)
COLOR_YELLOW = (255, 255, 0)
COLOR_PURPLE = (128, 0, 128)

# Alias de nombres utilizados por módulos antiguos
NEGRO = COLOR_BLACK
BLANCO = COLOR_WHITE
ROJO = COLOR_RED
VERDE = COLOR_GREEN
AZUL = COLOR_BLUE
GRIS = COLOR_GRAY
AMARILLO = COLOR_YELLOW
MORADO = COLOR_PURPLE

# Jugador
PLAYER_SPEED = 5
PLAYER_SIZE = 40
PLAYER_MAX_HP = 100
PLAYER_INITIAL_HP = 100

# Enemigos
ENEMY_SPEED = 2
ENEMY_SIZE = 35
ENEMY_MAX_HP = 30
ENEMY_DAMAGE = 10

# Jefe
BOSS_SIZE = 80
BOSS_MAX_HP = 300
BOSS_SPEED = 2.5
BOSS_DAMAGE = 25
BOSS_ATTACK_COOLDOWN = 60

# Combate
ATTACK_DAMAGE = 20
ATTACK_COOLDOWN = 30

# Niveles
TOTAL_LEVELS = 10
BOSS_LEVEL = 10
LEVEL_CONFIG = {
    1: {"enemies": 2, "enemy_hp": 20, "difficulty": 1.0},
    2: {"enemies": 3, "enemy_hp": 25, "difficulty": 1.1},
    3: {"enemies": 4, "enemy_hp": 30, "difficulty": 1.2},
    4: {"enemies": 5, "enemy_hp": 35, "difficulty": 1.3},
    5: {"enemies": 6, "enemy_hp": 40, "difficulty": 1.4},
    6: {"enemies": 7, "enemy_hp": 45, "difficulty": 1.5},
    7: {"enemies": 8, "enemy_hp": 50, "difficulty": 1.6},
    8: {"enemies": 9, "enemy_hp": 55, "difficulty": 1.7},
    9: {"enemies": 10, "enemy_hp": 60, "difficulty": 1.8},
    10: {"enemies": 0, "enemy_hp": 0, "difficulty": 2.0, "boss": True},
}
