# cofre.py — Cofres con operaciones matemáticas
import pygame
import random
from settings import TAM, TEXTO_TITULO, TEXTO_OPERACION

OPERACIONES_POR_TIPO = {
    "suma":           lambda: ("+",  random.randint(1, 20),  random.randint(1, 20)),
    "resta":          lambda: ("-",  random.randint(10, 30), random.randint(1, 10)),
    "multiplicacion": lambda: ("×",  random.randint(2, 9),   random.randint(2, 9)),
    "division":       lambda: ("÷",  None, None),   # generada aparte
    "potencia":       lambda: ("^",  random.randint(2, 5),   random.randint(2, 3)),
    "raiz":           lambda: ("√",  None, None),   # generada aparte
    "mixta":          lambda: None,                  # generada aparte
}

def generar_operacion(tipos=None):
    if tipos is None:
        tipos = ["suma", "resta"]

    tipo = random.choice(tipos)

    if tipo == "suma":
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        return f"{a} + {b}", a + b

    elif tipo == "resta":
        a = random.randint(10, 30)
        b = random.randint(1, a)
        return f"{a} - {b}", a - b

    elif tipo == "multiplicacion":
        a = random.randint(2, 9)
        b = random.randint(2, 9)
        return f"{a} × {b}", a * b

    elif tipo == "division":
        b = random.randint(2, 9)
        resultado = random.randint(2, 9)
        a = b * resultado
        return f"{a} ÷ {b}", resultado

    elif tipo == "potencia":
        base = random.randint(2, 5)
        exp  = random.randint(2, 3)
        return f"{base} ^ {exp}", base ** exp

    elif tipo == "raiz":
        resultado = random.randint(2, 9)
        a = resultado ** 2
        return f"√{a}", resultado

    elif tipo == "mixta":
        a = random.randint(2, 9)
        b = random.randint(2, 5)
        c = random.randint(1, 10)
        return f"{a} × {b} + {c}", a * b + c

    # fallback
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    return f"{a} + {b}", a + b


class Cofre:
    def __init__(self, x, y, tipos_ops=None):
        self.rect       = pygame.Rect(x, y, TAM, TAM)
        self.abierto    = False
        self.resuelto   = False
        self.operacion_resuelta = False
        self.operacion, self.respuesta_correcta = generar_operacion(tipos_ops)

        # Sprite simple
        self.img = pygame.Surface((TAM, TAM), pygame.SRCALPHA)
        self._dibujar_sprite_cerrado()
        self.img_abierto = pygame.Surface((TAM, TAM), pygame.SRCALPHA)
        self._dibujar_sprite_abierto()

    def _dibujar_sprite_cerrado(self):
        s = self.img
        pygame.draw.rect(s, (139, 90, 43),  (2,  10, TAM-4, TAM-14), border_radius=4)
        pygame.draw.rect(s, (101, 67, 33),  (2,  10, TAM-4, TAM-14), 2, border_radius=4)
        pygame.draw.rect(s, (180, 140, 60), (4,  4,  TAM-8, 14),     border_radius=3)
        pygame.draw.rect(s, (101, 67, 33),  (4,  4,  TAM-8, 14),     2, border_radius=3)
        pygame.draw.circle(s, (255, 215, 0), (TAM//2, 17), 5)
        pygame.draw.circle(s, (180, 150, 0),(TAM//2, 17), 5, 2)

    def _dibujar_sprite_abierto(self):
        s = self.img_abierto
        pygame.draw.rect(s, (80,  50, 20),  (2, 18, TAM-4, TAM-22), border_radius=4)
        pygame.draw.rect(s, (60,  35, 10),  (2, 18, TAM-4, TAM-22), 2, border_radius=4)
        pygame.draw.rect(s, (100, 70, 30),  (4,  4, TAM-8, 16),     border_radius=3)
        pygame.draw.rect(s, (60,  35, 10),  (4,  4, TAM-8, 16),     2, border_radius=3)
        # Brillo interior
        pygame.draw.ellipse(s, (255, 215, 0, 160), (8, 14, TAM-16, 10))

    def abrir(self):
        self.abierto = True

    def obtener_texto_operacion(self):
        return f"{self.operacion} = ?"

    def dibujar(self, superficie, cam_x=0, cam_y=0):
        rx = self.rect.x - cam_x
        ry = self.rect.y - cam_y

        if self.resuelto:
            superficie.blit(self.img_abierto, (rx, ry))
            # Brillo dorado
            fuente = pygame.font.Font(None, 18)
            txt = fuente.render("✓", True, (255, 215, 0))
            superficie.blit(txt, (rx + TAM//2 - 5, ry - 14))
        else:
            superficie.blit(self.img, (rx, ry))
            if not self.abierto:
                # Señal de que hay un acertijo
                fuente = pygame.font.Font(None, 18)
                txt = fuente.render("?", True, TEXTO_TITULO)
                superficie.blit(txt, (rx + TAM//2 - 4, ry - 14))
