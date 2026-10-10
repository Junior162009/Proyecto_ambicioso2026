# cofre.py — Cofres con operaciones matemáticas
from pathlib import Path
import random

import pygame

from settings import TAM, TEXTO_TITULO, TEXTO_OPERACION

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets" / "objetos"

OPERACIONES_POR_TIPO = {
    "suma": lambda: ("+", random.randint(1, 20), random.randint(1, 20)),
    "resta": lambda: ("-", random.randint(10, 30), random.randint(1, 10)),
    "multiplicacion": lambda: ("×", random.randint(2, 9), random.randint(2, 9)),
    "division": lambda: ("÷", None, None),
    "potencia": lambda: ("^", random.randint(2, 5), random.randint(2, 3)),
    "raiz": lambda: ("√", None, None),
    "mixta": lambda: None,
}


def generar_operacion(tipos=None):
    if tipos is None:
        tipos = ["suma", "resta"]

    tipo = random.choice(tipos)
    if tipo == "suma":
        a, b = random.randint(1, 20), random.randint(1, 20)
        return f"{a} + {b}", a + b
    if tipo == "resta":
        a = random.randint(10, 30)
        b = random.randint(1, a)
        return f"{a} - {b}", a - b
    if tipo == "multiplicacion":
        a, b = random.randint(2, 9), random.randint(2, 9)
        return f"{a} × {b}", a * b
    if tipo == "division":
        b, resultado = random.randint(2, 9), random.randint(2, 9)
        return f"{b * resultado} ÷ {b}", resultado
    if tipo == "potencia":
        base, exp = random.randint(2, 5), random.randint(2, 3)
        return f"{base} ^ {exp}", base ** exp
    if tipo == "raiz":
        resultado = random.randint(2, 9)
        return f"√{resultado ** 2}", resultado
    if tipo == "mixta":
        a, b, c = random.randint(2, 9), random.randint(2, 5), random.randint(1, 10)
        return f"{a} × {b} + {c}", a * b + c

    a, b = random.randint(1, 10), random.randint(1, 10)
    return f"{a} + {b}", a + b


def _cargar_sprite(nombre, respaldo):
    """Carga el recurso desde la raíz del proyecto y deja un respaldo si falta."""
    ruta = ASSETS_DIR / nombre
    try:
        imagen = pygame.image.load(str(ruta)).convert_alpha()
        return pygame.transform.smoothscale(imagen, (TAM, TAM))
    except (pygame.error, OSError):
        imagen = pygame.Surface((TAM, TAM), pygame.SRCALPHA)
        imagen.fill(respaldo)
        pygame.draw.rect(imagen, (245, 225, 170), imagen.get_rect(), 2, border_radius=4)
        return imagen


class Cofre:
    def __init__(self, x, y, tipos_ops=None):
        self.rect = pygame.Rect(x, y, TAM, TAM)
        self.abierto = False
        self.resuelto = False
        self.operacion_resuelta = False
        self.recompensa_entregada = False
        self.operacion, self.respuesta_correcta = generar_operacion(tipos_ops)

        # Se conservan los sprites originales del repositorio cuando existen.
        self.img = _cargar_sprite("cofre_cerrado.png", (139, 90, 43))
        self.img_abierto = _cargar_sprite("cofre_abierto.png", (80, 50, 20))

    def _dibujar_sprite_cerrado(self):
        # Compatibilidad con versiones antiguas que llamaban este método.
        self.img = _cargar_sprite("cofre_cerrado.png", (139, 90, 43))

    def _dibujar_sprite_abierto(self):
        # Compatibilidad con versiones antiguas que llamaban este método.
        self.img_abierto = _cargar_sprite("cofre_abierto.png", (80, 50, 20))

    def abrir(self):
        if self.resuelto:
            return False
        self.abierto = True
        return True

    def resolver(self):
        """Marca el acertijo como resuelto sin entregar dos veces la recompensa."""
        if self.resuelto:
            return False
        self.abierto = True
        self.resuelto = True
        self.operacion_resuelta = True
        return True

    def puede_reclamar_recompensa(self):
        if not self.resuelto or self.recompensa_entregada:
            return False
        self.recompensa_entregada = True
        return True

    def obtener_texto_operacion(self):
        return f"{self.operacion} = ?"

    def dibujar(self, superficie, cam_x=0, cam_y=0):
        rx, ry = self.rect.x - cam_x, self.rect.y - cam_y
        superficie.blit(self.img_abierto if self.resuelto else self.img, (rx, ry))
        fuente = pygame.font.Font(None, 18)
        if self.resuelto:
            txt = fuente.render("✓", True, (255, 215, 0))
            superficie.blit(txt, (rx + TAM // 2 - 5, ry - 14))
        elif not self.abierto:
            txt = fuente.render("?", True, TEXTO_TITULO)
            superficie.blit(txt, (rx + TAM // 2 - 4, ry - 14))
