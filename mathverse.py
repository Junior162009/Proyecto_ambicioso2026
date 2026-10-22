"""Mathverse: El Desafío de los 5 Reinos.
Nueva experiencia competitiva educativa de Pygame, independiente del mundo antiguo de MATEMIA.

Controles: ratón para elegir respuestas/poderes, ESC para salir.
"""
from __future__ import annotations

import json
import math
import random
import time
from pathlib import Path

import pygame

from mathverse_core import atomic_write_json, validate_question_bank, validate_save

WIDTH, HEIGHT = 1280, 720
FPS = 60
MATCH_SECONDS = 360
SAVE_FILE = Path(__file__).with_name("mathverse_save.json")

DOMAINS = [
    ("NUMÉRICO", "Matemáticas", "🧮"),
    ("GLOBAL", "Inglés", "🌐"),
    ("PALABRA", "Español", "📖"),
    ("CIVILIZACIONES", "Historia", "🌎"),
    ("VIDA", "Ciencias", "🧬"),
]

QUESTIONS = {
    0: [
        ("¿Cuánto es 15 × 4?", ["45", "60", "75", "90"], 1),
        ("Completa: 2, 4, 8, 16, ...", ["20", "24", "30", "32"], 3),
        ("¿Cuál es el 25% de 80?", ["10", "15", "20", "25"], 2),
        ("Si x + 7 = 19, ¿cuánto vale x?", ["10", "11", "12", "13"], 2),
    ],
    1: [
        ("What does 'brave' mean?", ["Valiente", "Rápido", "Triste", "Pequeño"], 0),
        ("Choose the correct sentence.", ["She are happy.", "She is happy.", "She am happy.", "She be happy."], 1),
        ("Opposite of 'early'", ["Fast", "Late", "Near", "Easy"], 1),
        ("'Book' as a verb means...", ["Reservar", "Cocinar", "Cerrar", "Pintar"], 0),
    ],
    2: [
        ("¿Cuál palabra está escrita correctamente?", ["Exepción", "Excepción", "Ecepción", "Exsepción"], 1),
        ("Sinónimo de 'rápido'", ["Lento", "Veloz", "Pesado", "Lejano"], 1),
        ("¿Qué expresa una conclusión?", ["Una idea final", "Un saludo", "Un personaje", "Una fecha"], 0),
        ("¿Cuál es un verbo?", ["Montaña", "Azul", "Correr", "Ayer"], 2),
    ],
    3: [
        ("¿En qué continente está Egipto?", ["Asia", "Europa", "África", "Oceanía"], 2),
        ("¿Qué civilización construyó Machu Picchu?", ["Maya", "Inca", "Romana", "Egipcia"], 1),
        ("¿Cuál es la capital de Colombia?", ["Cali", "Medellín", "Cartagena", "Bogotá"], 3),
        ("¿Qué océano está entre América y Europa?", ["Pacífico", "Atlántico", "Índico", "Ártico"], 1),
    ],
    4: [
        ("¿Qué órgano bombea la sangre?", ["Pulmón", "Cerebro", "Corazón", "Riñón"], 2),
        ("¿Qué molécula contiene la información genética?", ["ADN", "Agua", "Glucosa", "Oxígeno"], 0),
        ("En una cadena alimentaria, las plantas son...", ["Productores", "Depredadores", "Descomponedores", "Parásitos"], 0),
        ("¿Cuál es el sistema que permite respirar?", ["Digestivo", "Respiratorio", "Nervioso", "Óseo"], 1),
    ],
}

POWERS = [
    ("NIEBLA MENTAL", 30, "Reduce las opciones del rival"),
    ("CONGELAMIENTO", 45, "Aturde al líder"),
    ("ROBO DE PUNTOS", 55, "Absorbe puntos del rival"),
    ("ESCUDO", 35, "Bloquea el próximo ataque"),
    ("DOBLE O NADA", 40, "Duplica la próxima recompensa"),
]

BOT_NAMES = ["Nova", "Atlas", "Luna", "Pixel", "Vector", "Gaia", "Byte"]


def clamp(value, low, high):
    return max(low, min(high, value))


class Bot:
    def __init__(self, name, index):
        self.name = name
        self.index = index
        self.score = 0
        self.mana = random.randint(15, 45)
        self.level = random.randint(1, 4)
        self.answer_timer = random.uniform(2.0, 9.0)
        self.cooldown = random.uniform(4, 10)
        self.shield = False

    def update(self, dt, game):
        self.answer_timer -= dt
        self.cooldown -= dt
        if self.answer_timer <= 0:
            difficulty = 0.54 + self.level * 0.08
            if random.random() < difficulty:
                gain = random.randint(60, 105)
                self.score += gain
                self.mana = clamp(self.mana + random.randint(8, 20), 0, 100)
            else:
                self.mana = clamp(self.mana + 4, 0, 100)
            self.answer_timer = random.uniform(3.0, 10.0)
        if self.cooldown <= 0 and self.mana >= 30 and random.random() < 0.35:
            self.mana -= random.choice([30, 35, 45, 55])
            self.cooldown = random.uniform(7, 15)
            game.events.append((self.name, random.choice(["NIEBLA MENTAL", "CONGELAMIENTO", "ROBO DE PUNTOS"])))


class Mathverse:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Mathverse — El Desafío de los 5 Reinos")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "menu"
        self.font = pygame.font.Font(None, 28)
        self.big = pygame.font.Font(None, 58)
        self.huge = pygame.font.Font(None, 88)
        self.small = pygame.font.Font(None, 21)
        self.domain = 0
        self.question = None
        self.options = []
        self.correct = 0
        self.question_started = 0.0
        self.question_limit = 12.0
        self.score = 0
        self.mana = 0
        self.xp = 0
        self.brain_coins = 0
        self.combo = 0
        self.round = 0
        self.match_start = 0.0
        self.feedback = ""
        self.feedback_until = 0.0
        self.events = []
        self.bots = []
        self.player_name = "TÚ"
        self.save = self.load_save()
        self.xp = self.save["xp"]
        self.brain_coins = self.save["brain_coins"]
        self.cosmetic = self.save["cosmetic"]
        self.answered = False
        self.match_awarded = False
        self.answer_explanation = ""
        self.question_count = 0
        self.power_cooldowns = {}
        self.shield_active = False
        self.double_or_nothing = False
        errors = validate_question_bank(QUESTIONS)
        if errors:
            raise ValueError("Banco de preguntas inválido: " + "; ".join(errors))

    def load_save(self):
        try:
            return validate_save(json.loads(SAVE_FILE.read_text(encoding="utf-8")))
        except (OSError, ValueError, TypeError):
            return validate_save({})

    def save_game(self):
        data = validate_save({"xp": self.xp, "brain_coins": self.brain_coins,
                              "cosmetic": self.cosmetic,
                              "completed_match_ids": self.save.get("completed_match_ids", [])})
        try:
            atomic_write_json(SAVE_FILE, data)
            self.save = data
        except OSError:
            self.feedback = "No se pudo guardar el progreso local."

    def new_match(self):
        self.state = "match"
        self.score = 0
        self.mana = 0
        self.combo = 0
        self.round = 0
        self.match_start = time.monotonic()
        self.feedback = ""
        self.events.clear()
        self.answered = False
        self.match_awarded = False
        self.question_count = 0
        self.power_cooldowns.clear()
        self.shield_active = False
        self.double_or_nothing = False
        self.bots = [Bot(n, i) for i, n in enumerate(BOT_NAMES[:7])]
        self.next_question()

    def next_question(self):
        self.round += 1
        self.domain = random.randrange(5)
        pool = QUESTIONS[self.domain]
        self.question, self.options, self.correct = random.choice(pool)
        self.question_started = time.monotonic()
        self.answered = False
        self.answer_explanation = ""
        self.question_count += 1
        self.question_limit = 3.0 if self.round % 11 == 0 else random.uniform(10.0, 15.0)
        if self.round % 11 == 0:
            self.feedback = "⚡ RONDA RELÁMPAGO — ¡3 segundos!"
            self.feedback_until = time.monotonic() + 2.0

    def answer(self, index):
        if self.state != "match" or not self.question or self.answered:
            return False
        elapsed = time.monotonic() - self.question_started
        timed_out = elapsed > self.question_limit or index < 0 or index >= len(self.options)
        correct = not timed_out and index == self.correct
        self.answered = True
        if correct:
            speed = max(0.2, 1.0 - elapsed / self.question_limit)
            gain = int(55 + 55 * speed) + self.combo * 8
            if self.round % 11 == 0:
                gain *= 2
            if self.double_or_nothing:
                gain *= 2
            self.score += gain
            self.mana = clamp(self.mana + 16 + int(speed * 12), 0, 100)
            self.xp += 10 + self.combo * 2
            self.combo += 1
            self.feedback = f"✓ ¡Correcto! +{gain} puntos"
        else:
            self.combo = 0
            if self.double_or_nothing:
                self.score = max(0, self.score - min(50, self.score))
            self.mana = clamp(self.mana + 3, 0, 100)
            self.feedback = "⏱ Tiempo agotado" if timed_out else "✗ Respuesta incorrecta"
        self.double_or_nothing = False
        self.answer_explanation = f"Respuesta correcta: {self.options[self.correct]}"
        self.feedback_until = time.monotonic() + 1.6
        return True

    def use_power(self, power_index):
        if self.state != "match" or self.answered or not 0 <= power_index < len(POWERS):
            return False
        now = time.monotonic()
        cooldowns = {0: 12, 1: 15, 2: 18, 3: 12, 4: 15}
        name, cost, _ = POWERS[power_index]
        if now < self.power_cooldowns.get(power_index, 0):
            self.feedback = "Poder en reutilización"
            self.feedback_until = now + 1.2
            return False
        if self.mana < cost:
            self.feedback = "⚡ No tienes suficiente maná"
            self.feedback_until = now + 1.2
            return False
        target = max(self.bots, key=lambda bot: bot.score, default=None)
        if power_index in (3, 4) and ((power_index == 3 and self.shield_active) or (power_index == 4 and self.double_or_nothing)):
            self.feedback = "Ese poder ya está activo"
            self.feedback_until = now + 1.2
            return False
        self.mana -= cost
        if power_index == 0 and target:
            target.answer_timer += 3.0
        elif power_index == 1 and target:
            target.answer_timer += 4.0
        elif power_index == 2 and target:
            stolen = min(80, max(0, target.score))
            target.score -= stolen
            self.score += stolen
        elif power_index == 3:
            self.shield_active = True
        elif power_index == 4:
            self.double_or_nothing = True
        self.power_cooldowns[power_index] = now + cooldowns[power_index]
        self.feedback = f"{name} activado"
        self.feedback_until = now + 1.4
        return True

    def finish(self):
        if self.state != "match" or getattr(self, "match_awarded", False):
            return False
        self.match_awarded = True
        self.state = "result"
        self.brain_coins += max(5, self.score // 80)
        self.xp += self.score // 20
        self.save_game()
        return True

    def draw_text(self, text, pos, size=28, color=(235, 240, 255), center=False):
        f = self.small if size <= 21 else self.font if size <= 32 else self.big if size <= 60 else self.huge
        image = f.render(str(text), True, color)
        rect = image.get_rect()
        if center:
            rect.center = pos
        else:
            rect.topleft = pos
        self.screen.blit(image, rect)

    def button(self, rect, text, active=True, size=25):
        mouse = pygame.mouse.get_pos()
        hover = rect.collidepoint(mouse)
        base = (31, 39, 65) if active else (24, 27, 38)
        if hover and active:
            base = (55, 70, 110)
        pygame.draw.rect(self.screen, base, rect, border_radius=12)
        pygame.draw.rect(self.screen, (93, 112, 165), rect, 2, border_radius=12)
        self.draw_text(text, rect.center, size, center=True)
        return hover

    def draw_menu(self):
        self.screen.fill((9, 12, 25))
        for i in range(18):
            x = (i * 173 + 40) % WIDTH
            y = 80 + ((i * 97) % 550)
            pygame.draw.circle(self.screen, (28, 44, 76), (x, y), 2 + i % 3)
        self.draw_text("MATHVERSE", (WIDTH // 2, 130), 88, (245, 215, 90), True)
        self.draw_text("EL DESAFÍO DE LOS 5 REINOS", (WIDTH // 2, 190), 38, (210, 225, 255), True)
        self.draw_text("Competencia educativa • 5–7 minutos • 8 jugadores", (WIDTH // 2, 232), 24, (150, 170, 205), True)
        self.button(pygame.Rect(WIDTH // 2 - 170, 310, 340, 62), "⚔  JUGAR OFFLINE", True, 30)
        self.button(pygame.Rect(WIDTH // 2 - 170, 390, 340, 62), "✦  PERSONALIZAR AVATAR", True, 26)
        self.button(pygame.Rect(WIDTH // 2 - 170, 470, 340, 62), "◎  SALIR", True, 26)
        self.draw_text(f"Nivel {1 + self.xp // 250}   •   🧠 {self.brain_coins} Brain Coins", (WIDTH // 2, 590), 24, (245, 245, 245), True)

    def draw_avatar_menu(self):
        self.screen.fill((10, 15, 30))
        self.draw_text("PERSONALIZA TU AVATAR", (WIDTH // 2, 90), 48, (245, 215, 90), True)
        cx, cy = WIDTH // 2, 300
        pygame.draw.circle(self.screen, (35, 42, 70), (cx, cy + 20), 120, 3)
        aura = {"aura": (255, 205, 70), "electricidad": (90, 190, 255), "fuego": (255, 100, 70)}.get(self.cosmetic, (255, 205, 70))
        pygame.draw.circle(self.screen, aura, (cx, cy - 20), 62, 5)
        pygame.draw.circle(self.screen, (220, 185, 155), (cx, cy - 20), 40)
        pygame.draw.rect(self.screen, (55, 75, 110), (cx - 45, cy + 15, 90, 95), border_radius=20)
        choices = [("aura", "Aura dorada"), ("electricidad", "Electricidad"), ("fuego", "Fuego")]
        for i, (key, label) in enumerate(choices):
            r = pygame.Rect(WIDTH // 2 - 230 + i * 155, 480, 140, 52)
            self.button(r, label, True, 20)
        self.button(pygame.Rect(30, 30, 130, 48), "← Volver", True, 22)

    def draw_arena(self):
        self.screen.fill((8, 11, 23))
        w, h = self.screen.get_size()
        center = (w // 2, 390)
        radius = min(w, h) // 3
        pts = []
        for i in range(5):
            a = -math.pi / 2 + i * 2 * math.pi / 5
            pts.append((center[0] + math.cos(a) * radius, center[1] + math.sin(a) * radius))
        pygame.draw.polygon(self.screen, (17, 25, 48), pts)
        pygame.draw.polygon(self.screen, (71, 91, 140), pts, 4)
        for i, (name, subject, icon) in enumerate(DOMAINS):
            a = -math.pi / 2 + i * 2 * math.pi / 5
            x = center[0] + math.cos(a) * (radius + 65)
            y = center[1] + math.sin(a) * (radius + 65)
            self.draw_text(f"{icon} {name}", (x, y), 19, (210, 220, 245), True)
        # Players around the pentagon.
        players = [(self.player_name, self.score, True)] + [(b.name, b.score, False) for b in self.bots]
        for i, (name, score, human) in enumerate(players):
            a = -math.pi / 2 + i * 2 * math.pi / len(players)
            px = center[0] + math.cos(a) * (radius - 45)
            py = center[1] + math.sin(a) * (radius - 45)
            col = (245, 210, 70) if human else (100, 155, 235)
            pygame.draw.circle(self.screen, col, (int(px), int(py)), 25)
            pygame.draw.circle(self.screen, (240, 240, 255), (int(px), int(py)), 25, 2)
            self.draw_text(name, (px, py + 34), 18, (235, 240, 255), True)
            self.draw_text(str(score), (px, py), 20, (15, 20, 30), True)
        # Header
        remaining = max(0, MATCH_SECONDS - (time.monotonic() - self.match_start))
        self.draw_text(f"MATHVERSE   {int(remaining)//60:02d}:{int(remaining)%60:02d}", (28, 20), 30, (245, 215, 90))
        self.draw_text(f"PUNTOS {self.score:,}   COMBO x{self.combo}   NIVEL {1 + self.xp // 250}", (28, 55), 21)
        pygame.draw.rect(self.screen, (25, 30, 50), (w - 285, 25, 230, 18), border_radius=9)
        pygame.draw.rect(self.screen, (110, 190, 255), (w - 285, 25, int(230 * self.mana / 100), 18), border_radius=9)
        self.draw_text(f"MANÁ {self.mana}/100", (w - 170, 34), 17, (235, 245, 255), True)
        # Question panel
        panel = pygame.Rect(120, h - 285, w - 240, 120)
        pygame.draw.rect(self.screen, (20, 28, 49), panel, border_radius=18)
        pygame.draw.rect(self.screen, (65, 82, 125), panel, 2, border_radius=18)
        self.draw_text(f"{DOMAINS[self.domain][2]}  {DOMAINS[self.domain][1]}", (panel.x + 18, panel.y + 13), 20, (245, 215, 90))
        self.draw_text(self.question, (w // 2, panel.y + 65), 30, (245, 248, 255), True)
        # Answers
        answer_w = min(300, (w - 180) // 4)
        gap = 15
        total = answer_w * 4 + gap * 3
        start = (w - total) // 2
        for i, option in enumerate(self.options):
            self.button(pygame.Rect(start + i * (answer_w + gap), h - 150, answer_w, 58), f"{i+1}. {option}", True, 21)
        # Powers
        for i, (name, cost, _) in enumerate(POWERS):
            self.button(pygame.Rect(25 + i * 165, h - 78, 155, 48), f"{name} • {cost}", self.mana >= cost, 17)
        if self.feedback and time.monotonic() < self.feedback_until:
            self.draw_text(self.feedback, (w // 2, h - 315), 22, (120, 235, 170), True)
            if self.answered:
                self.draw_text(self.answer_explanation, (w // 2, h - 290), 20, (255, 220, 120), True)

    def draw_result(self):
        self.screen.fill((9, 12, 25))
        self.draw_text("FIN DE LA BATALLA", (WIDTH // 2, 90), 58, (245, 215, 90), True)
        ranking = [(self.player_name, self.score)] + [(b.name, b.score) for b in self.bots]
        ranking.sort(key=lambda x: x[1], reverse=True)
        for i, (name, score) in enumerate(ranking):
            y = 165 + i * 48
            col = (245, 215, 90) if name == self.player_name else (220, 225, 240)
            self.draw_text(f"{i+1:02d}   {name:<10}   {score:,} pts", (WIDTH // 2, y), 27, col, True)
        self.draw_text(f"+{max(5, self.score // 80)} Brain Coins   •   XP total: {self.xp}", (WIDTH // 2, 560), 24, (150, 220, 255), True)
        self.button(pygame.Rect(WIDTH // 2 - 150, 610, 300, 58), "⚔  OTRA PARTIDA", True, 25)

    def click(self, pos):
        x, y = pos
        w, h = self.screen.get_size()
        if self.state == "menu":
            if pygame.Rect(w//2-170, 310, 340, 62).collidepoint(pos): self.new_match()
            elif pygame.Rect(w//2-170, 390, 340, 62).collidepoint(pos): self.state = "avatar"
            elif pygame.Rect(w//2-170, 470, 340, 62).collidepoint(pos): self.running = False
        elif self.state == "avatar":
            if pygame.Rect(30,30,130,48).collidepoint(pos): self.state = "menu"
            for i, key in enumerate(["aura", "electricidad", "fuego"]):
                if pygame.Rect(w//2-230+i*155,480,140,52).collidepoint(pos):
                    self.cosmetic = key
                    self.save_game()
        elif self.state == "match":
            answer_w = min(300, (w - 180) // 4); gap = 15; total = answer_w*4+gap*3; start=(w-total)//2
            for i in range(4):
                if pygame.Rect(start+i*(answer_w+gap), h-150, answer_w, 58).collidepoint(pos): self.answer(i); return
            for i in range(5):
                if pygame.Rect(25+i*165,h-78,155,48).collidepoint(pos): self.use_power(i); return
        elif self.state == "result":
            if pygame.Rect(w//2-150,610,300,58).collidepoint(pos): self.new_match()

    def update(self, dt):
        if self.state != "match": return
        now = time.monotonic()
        if now - self.match_start >= MATCH_SECONDS:
            self.finish()
            return
        if self.answered:
            if now >= self.feedback_until: self.next_question()
            return
        for bot in self.bots: bot.update(dt, self)
        if now - self.question_started >= self.question_limit: self.answer(-1)

    def draw(self):
        if self.state == "menu": self.draw_menu()
        elif self.state == "avatar": self.draw_avatar_menu()
        elif self.state == "match": self.draw_arena()
        else: self.draw_result()
        pygame.display.flip()

    def run(self):
        global WIDTH, HEIGHT
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.running = False
                elif event.type == pygame.VIDEORESIZE:
                    WIDTH, HEIGHT = max(640, event.w), max(480, event.h)
                    self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: self.running = False
                elif event.type == pygame.KEYDOWN and self.state == "match" and pygame.K_1 <= event.key <= pygame.K_4:
                    self.answer(event.key - pygame.K_1)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: self.click(event.pos)
            self.update(dt)
            self.draw()
        self.save_game()
        pygame.quit()


def ejecutar():
    Mathverse().run()


if __name__ == "__main__":
    ejecutar()
