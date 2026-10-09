# settings.py - Configuración centralizada y compatibilidad
"""Configuración centralizada del juego MindMath 2026."""

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
ANCHO = SCREEN_WIDTH
ALTO = SCREEN_HEIGHT
FPS = 60
TITLE = "Mundo Libre Matemático — Matemia"

TAM = 32
OSCURIDAD_TUNEL_ALPHA = 170
LUZ_RADIO_TUNEL = 96
LUZ_RADIO_NORMAL = 180

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (220, 55, 55)
COLOR_GREEN = (55, 205, 95)
COLOR_BLUE = (70, 130, 240)
COLOR_GRAY = (128, 128, 128)
COLOR_YELLOW = (255, 220, 70)
COLOR_PURPLE = (155, 90, 220)

NEGRO, BLANCO, ROJO, VERDE = COLOR_BLACK, COLOR_WHITE, COLOR_RED, COLOR_GREEN
AZUL, GRIS, AMARILLO, MORADO = COLOR_BLUE, COLOR_GRAY, COLOR_YELLOW, COLOR_PURPLE

# Colores y fuentes de texto usados por la interfaz existente.
TEXTO_TITULO = (255, 225, 140)
TEXTO_OPERACION = (255, 220, 100)
TEXTO_RESPUESTA = (255, 255, 255)
TEXTO_NORMAL = (245, 240, 225)
TEXTO_SECUNDARIO = (180, 195, 210)
COLOR_FONDO_UI = (24, 29, 42)

PLAYER_SPEED = 5
PLAYER_SIZE = 40
PLAYER_MAX_HP = 100
PLAYER_INITIAL_HP = 100

ENEMY_SPEED = 2
ENEMY_SIZE = 35
ENEMY_MAX_HP = 30
ENEMY_DAMAGE = 10

BOSS_SIZE = 80
BOSS_MAX_HP = 300
BOSS_SPEED = 2.5
BOSS_DAMAGE = 25
BOSS_ATTACK_COOLDOWN = 60

ATTACK_DAMAGE = 20
ATTACK_COOLDOWN = 18

TOTAL_LEVELS = 10
BOSS_LEVEL = 10
LEVEL_CONFIG = {
    1: {"enemies": 3, "enemy_hp": 20, "difficulty": 1.0},
    2: {"enemies": 4, "enemy_hp": 25, "difficulty": 1.1},
    3: {"enemies": 5, "enemy_hp": 30, "difficulty": 1.2},
    4: {"enemies": 6, "enemy_hp": 35, "difficulty": 1.3},
    5: {"enemies": 7, "enemy_hp": 40, "difficulty": 1.4},
    6: {"enemies": 8, "enemy_hp": 45, "difficulty": 1.5},
    7: {"enemies": 9, "enemy_hp": 50, "difficulty": 1.6},
    8: {"enemies": 10, "enemy_hp": 55, "difficulty": 1.7},
    9: {"enemies": 11, "enemy_hp": 60, "difficulty": 1.8},
    10: {"enemies": 0, "enemy_hp": 0, "difficulty": 2.0, "boss": True},
}

# Tienda: precios coherentes con la economía de puntos.
PRECIOS_TIENDA = {
    "pocion_vida": 40,
    "balas_extra": 25,
    "pocion_velocidad": 50,
    "pocion_fuerza": 60,
    "pocion_defensa": 60,
    "mapa": 20,
    "llave": 75,
}
