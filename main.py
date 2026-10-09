"""Juego principal de Matemia: exploración, combate, cofres y transición de áreas.

Ejecutar con: python main.py
Requiere pygame (pip install pygame).
"""
import math
import random
import sys
from pathlib import Path

import pygame

from mundo import Mundo
from mapa import Mapa
from npc import NPC
from bala import Bala
from cofre import Cofre, generar_operacion
from tienda import Tienda
from misiones import SistemaMisiones
from progresion import ProgresionHistoria
from settings import ANCHO, ALTO, TAM, FPS, TITLE, TEXTO_TITULO, TEXTO_NORMAL

BASE_DIR = Path(__file__).resolve().parent
ASSETS = BASE_DIR / "assets"

pygame.init()
pygame.display.set_caption(TITLE)
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
RELOJ = pygame.time.Clock()


_CACHE_IMAGENES = {}

def cargar_imagen(ruta, tamaño, color_respaldo):
    """Carga y escala cada recurso una sola vez para evitar tirones."""
    clave = (str(ruta), tamaño, color_respaldo)
    if clave in _CACHE_IMAGENES:
        return _CACHE_IMAGENES[clave]
    try:
        imagen = pygame.image.load(str(ruta)).convert_alpha()
        imagen = pygame.transform.smoothscale(imagen, tamaño)
    except (pygame.error, OSError):
        imagen = pygame.Surface(tamaño, pygame.SRCALPHA)
        imagen.fill(color_respaldo)
        pygame.draw.rect(imagen, (245, 225, 170), imagen.get_rect(), 2)
    _CACHE_IMAGENES[clave] = imagen
    return imagen


def texto(superficie, mensaje, x, y, fuente, color=TEXTO_NORMAL):
    imagen = fuente.render(str(mensaje), True, color)
    superficie.blit(imagen, (x, y))


class Jugador:
    def __init__(self):
        self.rect = pygame.Rect(64, 64, TAM - 4, TAM - 4)
        self.velocidad = 4
        self.vida_maxima = 100
        self.vida = self.vida_maxima
        self.puntos = 0
        self.experiencia = 0
        self.enemigos_eliminados = 0
        self.operaciones = []
        self.inventario = {}
        self.municion = 30
        self.daño_disparo = 25
        self.efectos_activos = {}
        self.cooldown_disparo = 0
        self.invulnerable = 0
        self.sprite = cargar_imagen(ASSETS / "sprites" / "jugador.png", (TAM, TAM), (55, 125, 245))

    def mover(self, teclas, paredes):
        ahora = pygame.time.get_ticks()
        self.velocidad = 6 if self.efectos_activos.get("velocidad", 0) > ahora else 4
        self.daño_disparo = 38 if self.efectos_activos.get("fuerza", 0) > ahora else 25
        for efecto, fin in list(self.efectos_activos.items()):
            if fin <= ahora:
                self.efectos_activos.pop(efecto, None)
        dx = (int(teclas[pygame.K_d] or teclas[pygame.K_RIGHT]) -
              int(teclas[pygame.K_a] or teclas[pygame.K_LEFT])) * self.velocidad
        dy = (int(teclas[pygame.K_s] or teclas[pygame.K_DOWN]) -
              int(teclas[pygame.K_w] or teclas[pygame.K_UP])) * self.velocidad
        if dx and dy:
            dx = int(dx * 0.7071)
            dy = int(dy * 0.7071)
        self.rect.x += dx
        for pared in paredes:
            if self.rect.colliderect(pared):
                if dx > 0:
                    self.rect.right = pared.left
                elif dx < 0:
                    self.rect.left = pared.right
        self.rect.y += dy
        for pared in paredes:
            if self.rect.colliderect(pared):
                if dy > 0:
                    self.rect.bottom = pared.top
                elif dy < 0:
                    self.rect.top = pared.bottom
        self.rect.x = max(0, self.rect.x)
        self.rect.y = max(0, self.rect.y)
        if self.cooldown_disparo > 0:
            self.cooldown_disparo -= 1
        if self.invulnerable > 0:
            self.invulnerable -= 1

    @property
    def nivel(self):
        return 1 + self.experiencia // 100

    def agregar_item(self, item_id, cantidad=1):
        self.inventario[item_id] = self.inventario.get(item_id, 0) + max(1, int(cantidad))
        return self.inventario[item_id]

    def usar_item(self, item_id):
        if self.inventario.get(item_id, 0) <= 0:
            return False, "No tienes ese objeto."
        ahora = pygame.time.get_ticks()
        if item_id == "pocion_vida":
            self.vida = min(self.vida_maxima, self.vida + 35)
        elif item_id == "balas_extra":
            self.municion += 10
        elif item_id in ("pocion_velocidad", "pocion_fuerza", "pocion_defensa"):
            efecto = {"pocion_velocidad": "velocidad", "pocion_fuerza": "fuerza",
                      "pocion_defensa": "defensa"}[item_id]
            self.efectos_activos[efecto] = ahora + 30000
        elif item_id in ("mapa", "llave"):
            return True, "El objeto está en el inventario; las salidas actuales no requieren llave."
        self.inventario[item_id] -= 1
        if self.inventario[item_id] <= 0:
            del self.inventario[item_id]
        return True, f"Usaste {item_id.replace('_', ' ')}."

    def recibir_daño(self, cantidad):
        if self.efectos_activos.get("defensa", 0) > pygame.time.get_ticks():
            cantidad = max(1, cantidad // 2)
        if self.invulnerable <= 0:
            self.vida = max(0, self.vida - cantidad)
            self.invulnerable = 45

    def dibujar(self, pantalla, cam_x, cam_y):
        destino = (self.rect.x - cam_x - 2, self.rect.y - cam_y - 2)
        if self.invulnerable and self.invulnerable // 4 % 2:
            return
        pantalla.blit(self.sprite, destino)


class Enemigo:
    def __init__(self, x, y, dificultad=1.0, jefe=False):
        self.jefe = jefe
        tamaño = 64 if jefe else 28
        self.rect = pygame.Rect(x, y, tamaño, tamaño)
        self.vida_maxima = int((180 if jefe else 35) * dificultad)
        self.vida = self.vida_maxima
        self.velocidad = 1.35 if jefe else random.uniform(1.0, 1.7) * min(dificultad, 1.6)
        self.daño = 18 if jefe else 8
        self.cooldown = 0
        self.color = (150, 55, 205) if jefe else random.choice([(205, 55, 60), (220, 105, 45), (90, 180, 75)])

    def actualizar(self, jugador, paredes):
        dx = jugador.rect.centerx - self.rect.centerx
        dy = jugador.rect.centery - self.rect.centery
        distancia = math.hypot(dx, dy)
        if distancia > 1:
            paso_x = round(dx / distancia * self.velocidad)
            paso_y = round(dy / distancia * self.velocidad)
            self.rect.x += paso_x
            for pared in paredes:
                if self.rect.colliderect(pared):
                    self.rect.x -= paso_x
                    break
            self.rect.y += paso_y
            for pared in paredes:
                if self.rect.colliderect(pared):
                    self.rect.y -= paso_y
                    break
        if self.cooldown > 0:
            self.cooldown -= 1
        if self.rect.colliderect(jugador.rect) and self.cooldown <= 0:
            jugador.recibir_daño(self.daño)
            self.cooldown = 50

    def dibujar(self, pantalla, cam_x, cam_y):
        r = self.rect.move(-cam_x, -cam_y)
        pygame.draw.ellipse(pantalla, self.color, r)
        pygame.draw.ellipse(pantalla, (35, 25, 35), r, 2)
        ancho = r.width
        pygame.draw.rect(pantalla, (50, 20, 25), (r.x, r.y - 8, ancho, 5))
        pygame.draw.rect(pantalla, (70, 220, 90), (r.x, r.y - 8, int(ancho * max(0, self.vida / self.vida_maxima)), 5))


class Juego:
    def __init__(self):
        self.mundo = Mundo()
        self.jugador = Jugador()
        self.fuente = pygame.font.Font(None, 25)
        self.fuente_grande = pygame.font.Font(None, 38)
        self.estado = "jugando"
        self.mensaje = "Explora Matemia. WASD mover · clic disparar · E interactuar"
        self.mensaje_hasta = pygame.time.get_ticks() + 5000
        self.balas = []
        self.cofres = []
        self.puertas = []
        self.npcs = []
        self.enemigos = []
        self.cofre_activo = None
        self.respuesta = ""
        self.area_visitada = set()
        self.area_anterior_id = None
        self.nivel = 1
        self.tienda = Tienda()
        self.misiones = SistemaMisiones()
        self.progresion = ProgresionHistoria()
        self.panel = None
        self.cargar_area(inicial=True)

    def avisar(self, mensaje, duracion=2600):
        self.mensaje = mensaje
        self.mensaje_hasta = pygame.time.get_ticks() + duracion

    def cargar_area(self, inicial=False):
        area = self.mundo.area_actual
        mapa_data = area.mapa
        suelo = cargar_imagen(ASSETS / "tiles" / "suelo.png", (TAM, TAM), (70, 115, 70))
        pared = cargar_imagen(ASSETS / "tiles" / "pared.png", (TAM, TAM), (80, 80, 95))
        self.mapa = Mapa(mapa_data, suelo, pared)
        self.cofres, self.puertas, self.npcs, self.enemigos, self.balas = [], [], [], [], []
        self.area_visitada.add(area.id)

        for y, fila in enumerate(mapa_data):
            for x, tile in enumerate(fila):
                px, py = x * TAM, y * TAM
                if tile == "P":
                    self.jugador.rect.topleft = (px, py)
                elif tile == "C":
                    self.cofres.append(Cofre(px, py))
                elif tile == "D":
                    self.puertas.append(pygame.Rect(px, py, TAM, TAM))
                elif tile == "N" and area.tipo in ("pueblo", "aldea"):
                    self.npcs.append(NPC(px, py, "aldeano", "Habitante de Matemia",
                                         ["¡Bienvenido, aventurero!", "Derrota criaturas y resuelve cofres para conseguir puntos."]))
                elif tile == "E" and not area.es_segura:
                    self.enemigos.append(Enemigo(px + 2, py + 2, 1 + area.peligrosidad * 0.08))

        if not inicial:
            self.jugador.rect.x = max(TAM, min(self.jugador.rect.x, (len(mapa_data[0]) - 2) * TAM))
            self.jugador.rect.y = max(TAM, min(self.jugador.rect.y, (len(mapa_data) - 2) * TAM))
        if not area.es_segura and not self.enemigos:
            # Las áreas peligrosas deben tener al menos algunos enemigos.
            for _ in range(max(2, area.peligrosidad)):
                for intento in range(80):
                    x = random.randint(1, len(mapa_data[0]) - 2) * TAM
                    y = random.randint(1, len(mapa_data) - 2) * TAM
                    rect = pygame.Rect(x, y, 28, 28)
                    if not any(rect.colliderect(p) for p in self.mapa.paredes) and math.hypot(rect.centerx - self.jugador.rect.centerx, rect.centery - self.jugador.rect.centery) > 150:
                        self.enemigos.append(Enemigo(x, y, 1 + area.peligrosidad * 0.08))
                        break
        if area.id == 5 and not area.es_segura:
            # Buscar una celda despejada para que el jefe no aparezca dentro de una pared.
            jefe_creado = False
            for y in range(1, len(mapa_data) - 2):
                for x in range(1, len(mapa_data[y]) - 2):
                    rect_jefe = pygame.Rect(x * TAM, y * TAM, 64, 64)
                    if (not any(rect_jefe.colliderect(p) for p in self.mapa.paredes)
                            and math.hypot(rect_jefe.centerx - self.jugador.rect.centerx,
                                           rect_jefe.centery - self.jugador.rect.centery) > 180):
                        self.enemigos.append(Enemigo(rect_jefe.x, rect_jefe.y, 2.0, jefe=True))
                        jefe_creado = True
                        break
                if jefe_creado:
                    break
        self.avisar(f"{area.nombre} — {len(self.enemigos)} enemigos")

    def disparar(self, destino):
        if self.jugador.cooldown_disparo > 0 or self.estado != "jugando":
            return
        if self.jugador.municion <= 0:
            self.avisar("Sin munición. Compra cargadores en la tienda (T) y usa R para recargar.")
            return
        sx, sy = self.jugador.rect.center
        self.balas.append(Bala(sx, sy, destino[0], destino[1], velocidad=11))
        self.jugador.municion -= 1
        self.jugador.cooldown_disparo = 12

    def gestionar_panel(self, evento):
        """Procesa las opciones de tienda, inventario y misiones."""
        atajos = {"tienda": pygame.K_t, "inventario": pygame.K_i,
                  "misiones": pygame.K_q, "mapa": pygame.K_m}
        if evento.key == pygame.K_ESCAPE or evento.key == atajos.get(self.panel):
            self.panel = None
            return
        teclas_numero = (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                         pygame.K_5, pygame.K_6, pygame.K_7)
        indice = next((i for i, tecla in enumerate(teclas_numero) if evento.key == tecla), None)
        if indice is None:
            return
        if self.panel == "tienda":
            catalogo = self.tienda.obtener_items_compra()
            if indice < len(catalogo):
                _, mensaje = self.tienda.comprar(catalogo[indice]["id"], self.jugador)
                self.avisar(mensaje)
        elif self.panel == "inventario":
            objetos = list(self.jugador.inventario)
            if indice < len(objetos):
                _, mensaje = self.jugador.usar_item(objetos[indice])
                self.avisar(mensaje)
        elif self.panel == "misiones":
            disponibles = self.misiones.misiones_disponibles
            if indice < len(disponibles):
                _, mensaje = self.misiones.aceptar_mision(disponibles[indice].id)
                self.avisar(mensaje)

    def interactuar(self):
        if self.cofre_activo:
            return
        cerca = self.jugador.rect.inflate(36, 36)
        for cofre in self.cofres:
            if cerca.colliderect(cofre.rect) and not cofre.resuelto:
                cofre.abierto = True
                self.cofre_activo = cofre
                self.respuesta = ""
                self.avisar("Resuelve la operación y pulsa ENTER", 5000)
                return
        for npc in self.npcs:
            if cerca.colliderect(npc.rect):
                npc.hablando = True
                npc.dialogo_actual = (npc.dialogo_actual + 1) % max(1, len(npc.dialogo))
                self.avisar(f"{npc.nombre}: {npc.dialogo[npc.dialogo_actual]}")
                return
        for puerta in self.puertas:
            if cerca.colliderect(puerta):
                conexiones = self.mundo.area_actual.conexiones
                if conexiones:
                    # Las conexiones están definidas en mundo.py; usar solo destinos válidos.
                    opciones = [i for i in conexiones if i in self.mundo.areas]
                    destino = next((i for i in opciones if i != self.area_anterior_id), opciones[0] if opciones else None)
                    if destino is not None:
                        area_anterior = self.mundo.area_actual.id
                        if self.mundo.cambiar_area(destino):
                            self.area_anterior_id = area_anterior
                            self.nivel = min(10, self.nivel + 1)
                            self.cargar_area()
                            mensajes = self.misiones.actualizar_mision_explorando()
                            if mensajes:
                                self.misiones.reclamar_recompensas(self.jugador)
                                self.avisar(" ".join(mensajes))
                            return
        # En ausencia de una puerta marcada en el mapa, E cerca del borde permite viajar.
        area = self.mundo.area_actual
        if conexiones := area.conexiones:
            borde = (self.jugador.rect.left <= TAM + 3 or self.jugador.rect.top <= TAM + 3 or
                     self.jugador.rect.right >= len(area.mapa[0]) * TAM - TAM - 3 or
                     self.jugador.rect.bottom >= len(area.mapa) * TAM - TAM - 3)
            if borde:
                opciones = [i for i in conexiones if i in self.mundo.areas]
                if opciones:
                    destino = next((i for i in opciones if i != self.area_anterior_id), opciones[0])
                    area_anterior = self.mundo.area_actual.id
                    if self.mundo.cambiar_area(destino):
                        self.area_anterior_id = area_anterior
                        self.nivel = min(10, self.nivel + 1)
                        self.cargar_area()
                        mensajes = self.misiones.actualizar_mision_explorando()
                        if mensajes:
                            self.misiones.reclamar_recompensas(self.jugador)
                            self.avisar(" ".join(mensajes))
                        return
        self.avisar("Acércate a un cofre, habitante o salida para interactuar.")

    def comprobar_respuesta(self, evento):
        if not self.cofre_activo or evento.type != pygame.KEYDOWN:
            return
        if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            try:
                valor = int(self.respuesta)
            except ValueError:
                self.avisar("Escribe una respuesta numérica.")
                return
            if valor == self.cofre_activo.respuesta_correcta:
                self.cofre_activo.resuelto = True
                self.jugador.puntos += 30
                self.jugador.experiencia += 20
                self.jugador.operaciones.append(self.cofre_activo.operacion)
                mensajes_mision = self.misiones.actualizar_mision_cofre()
                if mensajes_mision:
                    self.misiones.reclamar_recompensas(self.jugador)
                self.cofre_activo = None
                self.respuesta = ""
                self.avisar("¡Correcto! +30 puntos y +20 experiencia" + (" · " + " ".join(mensajes_mision) if mensajes_mision else ""))
            else:
                self.respuesta = ""
                self.avisar("Respuesta incorrecta. Inténtalo de nuevo.")
        elif evento.key == pygame.K_BACKSPACE:
            self.respuesta = self.respuesta[:-1]
        elif evento.unicode.isdigit() and len(self.respuesta) < 7:
            self.respuesta += evento.unicode

    def actualizar(self):
        if self.estado != "jugando" or self.panel is not None:
            return
        teclas = pygame.key.get_pressed()
        self.jugador.mover(teclas, self.mapa.paredes)

        for enemigo in self.enemigos[:]:
            enemigo.actualizar(self.jugador, self.mapa.paredes)
        for bala in self.balas[:]:
            bala.mover()
            if (bala.rect.right < 0 or bala.rect.left > len(self.mapa.nivel[0]) * TAM or
                    bala.rect.bottom < 0 or bala.rect.top > len(self.mapa.nivel) * TAM):
                self.balas.remove(bala)
                continue
            if any(bala.rect.colliderect(p) for p in self.mapa.paredes):
                self.balas.remove(bala)
                continue
            golpeado = next((e for e in self.enemigos if bala.rect.colliderect(e.rect)), None)
            if golpeado:
                golpeado.vida -= self.jugador.daño_disparo
                if bala in self.balas:
                    self.balas.remove(bala)
                if golpeado.vida <= 0:
                    self.enemigos.remove(golpeado)
                    self.jugador.puntos += 15
                    self.jugador.experiencia += 10
                    self.jugador.enemigos_eliminados += 1
                    mensajes_mision = self.misiones.actualizar_mision_matando("Básico")
                    if mensajes_mision:
                        self.misiones.reclamar_recompensas(self.jugador)
                        self.avisar(" ".join(mensajes_mision))
                    else:
                        self.avisar("Enemigo derrotado: +15 puntos")
        for mensaje_progreso in self.progresion.verificar_progreso(self.jugador, self.mundo):
            self.avisar(mensaje_progreso)
        self.misiones.actualizar_mision_nivel(self.jugador.nivel)
        if self.jugador.vida <= 0:
            self.estado = "game_over"

    def dibujar(self):
        PANTALLA.fill((18, 25, 30))
        ancho_mundo = len(self.mapa.nivel[0]) * TAM
        alto_mundo = len(self.mapa.nivel) * TAM
        cam_x = max(0, min(self.jugador.rect.centerx - ANCHO // 2, ancho_mundo - ANCHO))
        cam_y = max(0, min(self.jugador.rect.centery - ALTO // 2, alto_mundo - ALTO))
        self.mapa.dibujar_suelo(PANTALLA, cam_x, cam_y)
        self.mapa.dibujar_paredes(PANTALLA, cam_x, cam_y)

        for puerta in self.puertas:
            pygame.draw.rect(PANTALLA, (145, 90, 45), puerta.move(-cam_x, -cam_y))
            pygame.draw.rect(PANTALLA, (240, 190, 75), puerta.move(-cam_x, -cam_y), 2)
        for cofre in self.cofres:
            r = cofre.rect.move(-cam_x, -cam_y)
            img_path = ASSETS / "objetos" / ("cofre_abierto.png" if cofre.resuelto else "cofre_cerrado.png")
            img = cargar_imagen(img_path, (TAM, TAM), (170, 115, 45))
            PANTALLA.blit(img, r)
        for npc in self.npcs:
            npc.dibujar(PANTALLA, cam_x, cam_y)
        for bala in self.balas:
            bala.dibujar(PANTALLA, cam_x, cam_y)
        for enemigo in self.enemigos:
            enemigo.dibujar(PANTALLA, cam_x, cam_y)
        self.jugador.dibujar(PANTALLA, cam_x, cam_y)

        # HUD
        pygame.draw.rect(PANTALLA, (35, 30, 42), (12, 12, 330, 78), border_radius=10)
        pygame.draw.rect(PANTALLA, (90, 35, 45), (24, 24, 210, 18), border_radius=5)
        pygame.draw.rect(PANTALLA, (55, 210, 95), (24, 24, int(210 * self.jugador.vida / self.jugador.vida_maxima), 18), border_radius=5)
        texto(PANTALLA, f"VIDA {self.jugador.vida}/{self.jugador.vida_maxima}", 244, 23, self.fuente)
        texto(PANTALLA, f"⭐ {self.jugador.puntos}   XP {self.jugador.experiencia}", 24, 53, self.fuente)
        texto(PANTALLA, f"{self.mundo.area_actual.nombre}  |  Enemigos: {len(self.enemigos)}", 18, ALTO - 34, self.fuente)
        texto(PANTALLA, f"WASD mover · clic disparar · E interactuar · T tienda · Q misiones · I inventario · M mapa · Munición {self.jugador.municion}", 360, 16, self.fuente)

        if pygame.time.get_ticks() < self.mensaje_hasta:
            panel = pygame.Surface((ANCHO - 100, 42), pygame.SRCALPHA)
            panel.fill((15, 18, 25, 220))
            PANTALLA.blit(panel, (50, ALTO - 82))
            texto(PANTALLA, self.mensaje, 65, ALTO - 72, self.fuente, TEXTO_TITULO)

        if self.cofre_activo:
            panel = pygame.Surface((520, 180), pygame.SRCALPHA)
            panel.fill((18, 22, 34, 245))
            pygame.draw.rect(panel, (210, 170, 80), panel.get_rect(), 3, border_radius=12)
            PANTALLA.blit(panel, (ANCHO // 2 - 260, ALTO // 2 - 90))
            texto(PANTALLA, "COFRE MATEMÁTICO", ANCHO // 2 - 225, ALTO // 2 - 70, self.fuente_grande, TEXTO_TITULO)
            texto(PANTALLA, f"{self.cofre_activo.operacion} = ?", ANCHO // 2 - 200, ALTO // 2 - 25, self.fuente_grande)
            texto(PANTALLA, f"Respuesta: {self.respuesta}_", ANCHO // 2 - 200, ALTO // 2 + 20, self.fuente)
            texto(PANTALLA, "ENTER confirmar · BACKSPACE borrar", ANCHO // 2 - 200, ALTO // 2 + 55, self.fuente)

        if self.panel is not None:
            overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            overlay.fill((8, 10, 18, 220))
            PANTALLA.blit(overlay, (0, 0))
            pygame.draw.rect(PANTALLA, (210, 170, 80), (ANCHO // 2 - 300, 80, 600, ALTO - 160), 3, border_radius=12)
            titulos = {"tienda": "TIENDA · pulsa 1-7 para comprar",
                       "inventario": "INVENTARIO · pulsa un número para usar",
                       "misiones": "MISIONES · pulsa un número para aceptar",
                       "mapa": "MAPA DEL MUNDO"}
            texto(PANTALLA, titulos.get(self.panel, "PANEL"), ANCHO // 2 - 270, 105, self.fuente_grande, TEXTO_TITULO)
            lineas = []
            if self.panel == "tienda":
                lineas = [f"{i+1}. {item['nombre']} — {item['precio']} puntos ({item['efecto']})"
                          for i, item in enumerate(self.tienda.obtener_items_compra())]
                lineas.append(f"Puntos disponibles: {self.jugador.puntos}")
            elif self.panel == "inventario":
                lineas = [f"{i+1}. {item} × {cantidad}" for i, (item, cantidad) in enumerate(self.jugador.inventario.items())]
                lineas.append(f"Munición actual: {self.jugador.municion}")
                if not self.jugador.inventario:
                    lineas.append("Inventario vacío. Pulsa T para comprar objetos.")
            elif self.panel == "misiones":
                lineas = [f"{i+1}. {m.titulo} — {m.progreso}/{m.cantidad}"
                          for i, m in enumerate(self.misiones.misiones_disponibles)]
                lineas.append("Activas: " + (", ".join(m.titulo for m in self.misiones.misiones_activas) or "ninguna"))
                if not self.misiones.misiones_disponibles:
                    lineas.append("No quedan misiones disponibles.")
            elif self.panel == "mapa":
                lineas = [f"{area.id}. {area.nombre} — {'visitada' if area.explorada else 'sin explorar'}"
                          for area in self.mundo.areas.values()]
                lineas.append("Acércate a una salida y pulsa E para viajar.")
            for i, linea in enumerate(lineas[:12]):
                texto(PANTALLA, linea, ANCHO // 2 - 270, 155 + i * 32, self.fuente)
            texto(PANTALLA, "Pulsa la misma tecla o ESC para cerrar", ANCHO // 2 - 200, ALTO - 110, self.fuente, TEXTO_TITULO)

        if self.estado == "game_over":
            overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            overlay.fill((10, 0, 0, 200))
            PANTALLA.blit(overlay, (0, 0))
            texto(PANTALLA, "HAS CAÍDO EN MATEMIA", ANCHO // 2 - 190, ALTO // 2 - 40, self.fuente_grande, (255, 100, 100))
            texto(PANTALLA, "Pulsa R para volver a intentarlo · ESC salir", ANCHO // 2 - 220, ALTO // 2 + 12, self.fuente)

        pygame.display.flip()

    def ejecutar(self):
        ejecutando = True
        while ejecutando:
            RELOJ.tick(FPS)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        ejecutando = False
                    elif self.estado == "game_over" and evento.key == pygame.K_r:
                        self.jugador = Jugador()
                        self.estado = "jugando"
                        self.cargar_area(inicial=True)
                    elif self.cofre_activo:
                        self.comprobar_respuesta(evento)
                    elif self.panel is not None:
                        self.gestionar_panel(evento)
                    elif evento.key == pygame.K_e:
                        self.interactuar()
                    elif evento.key == pygame.K_t:
                        self.panel = "tienda"
                    elif evento.key == pygame.K_i:
                        self.panel = "inventario"
                    elif evento.key == pygame.K_q:
                        self.panel = "misiones"
                    elif evento.key == pygame.K_m:
                        self.panel = "mapa"
                    elif evento.key == pygame.K_r:
                        ok, mensaje = self.jugador.usar_item("balas_extra")
                        self.avisar(mensaje if ok else "No tienes cargadores extra. Compra uno en la tienda (T).")
                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if not self.cofre_activo and self.estado == "jugando":
                        mouse = pygame.mouse.get_pos()
                        ancho_mundo = len(self.mapa.nivel[0]) * TAM
                        alto_mundo = len(self.mapa.nivel) * TAM
                        cam_x = max(0, min(self.jugador.rect.centerx - ANCHO // 2, ancho_mundo - ANCHO))
                        cam_y = max(0, min(self.jugador.rect.centery - ALTO // 2, alto_mundo - ALTO))
                        self.disparar((mouse[0] + cam_x, mouse[1] + cam_y))
            self.actualizar()
            self.dibujar()
        pygame.quit()


if __name__ == "__main__":
    Juego().ejecutar()
