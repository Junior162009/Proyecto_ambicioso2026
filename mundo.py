# mundo.py - MUNDO MEJORADO (PUEBLO FIJO + SIN NPCs EN MAZMORRAS)
import random


class AreaMundo:
    def __init__(self, id_area, nombre, tipo, tamaño, peligrosidad, es_segura=False):
        self.id = id_area
        self.nombre = nombre
        self.tipo = tipo
        self.tamaño = tamaño
        self.peligrosidad = peligrosidad
        self.es_segura = es_segura

        self.explorada = False
        self.conexiones = []
        self.mapa = self.generar_mapa()

    # ===============================
    # GENERAR MAPA SEGÚN TIPO
    # ===============================
    def generar_mapa(self):
        if self.tipo in ["pueblo", "aldea"]:
            return self.mapa_pueblo()

        elif self.tipo in ["cueva", "mazmorra", "ruinas"]:
            return self.mapa_mazmorra()

        else:
            return self.mapa_naturaleza()

    # ===============================
    # 🌳 NATURALEZA
    # ===============================
    def mapa_naturaleza(self):
        ancho, alto = self.tamaño
        mapa = []

        for y in range(alto):
            fila = ""
            for x in range(ancho):

                if x == 0 or y == 0 or x == ancho-1 or y == alto-1:
                    fila += "1"

                elif random.random() < 0.15:
                    fila += "1"

                elif random.random() < 0.05 and not self.es_segura:
                    fila += "E"

                elif random.random() < 0.03:
                    fila += "C"

                elif random.random() < 0.02:
                    fila += "D"

                else:
                    fila += "0"

            mapa.append(fila)

        return self.colocar_spawn(mapa)

    # ===============================
    # 🏘️ PUEBLO FIJO (NPCs ORGANIZADOS)
    # ===============================
    def mapa_pueblo(self):
        return [
            "11111111111111111111",
            "1P      N      N   1",
            "1   111111111       1",
            "1   1      1   N    1",
            "1   1      1        1",
            "1   11111111   N    1",
            "1                  1",
            "1   N       N      1",
            "1                  1",
            "11111111111111111111",
        ]

    # ===============================
    # ⚔️ MAZMORRAS (SIN NPCs)
    # ===============================
    def mapa_mazmorra(self):
        ancho, alto = self.tamaño
        mapa = []

        for y in range(alto):
            fila = ""
            for x in range(ancho):

                if x == 0 or y == 0 or x == ancho-1 or y == alto-1:
                    fila += "#"

                elif random.random() < 0.35:
                    fila += "#"

                elif random.random() < 0.20:
                    fila += "E"

                elif random.random() < 0.08:
                    fila += "C"

                elif random.random() < 0.03:
                    fila += "D"

                else:
                    fila += "0"

            mapa.append(fila)

        return self.colocar_spawn(mapa)

    # ===============================
    # 📍 SPAWN DEL JUGADOR
    # ===============================
    def colocar_spawn(self, mapa):
        alto = len(mapa)
        ancho = len(mapa[0])

        for _ in range(50):
            x = random.randint(1, ancho - 2)
            y = random.randint(1, alto - 2)

            if mapa[y][x] in ["0", " "]:
                fila = list(mapa[y])
                fila[x] = "P"
                mapa[y] = "".join(fila)
                break

        return mapa


# ===================================
# 🌍 MUNDO GLOBAL
# ===================================

class Mundo:
    def __init__(self):
        self.areas = {}
        self.area_actual = None

        self.crear_mundo()

    def crear_mundo(self):
        # 🌳 NATURALEZA
        self.areas[1] = AreaMundo(1, "Bosque", "bosque", (20, 20), 2)
        self.areas[2] = AreaMundo(2, "Lago", "lago", (18, 18), 1, True)

        # 🏘️ PUEBLO (SEGURO)
        self.areas[3] = AreaMundo(3, "Aldea", "aldea", (20, 10), 1, True)

        # ⚔️ MAZMORRAS
        self.areas[4] = AreaMundo(4, "Cueva", "cueva", (25, 25), 5)
        self.areas[5] = AreaMundo(5, "Mazmorra", "mazmorra", (30, 30), 8)

        # 🔗 CONEXIONES
        self.areas[1].conexiones = [2, 3]
        self.areas[2].conexiones = [1]
        self.areas[3].conexiones = [1, 4]
        self.areas[4].conexiones = [3, 5]
        self.areas[5].conexiones = [4]

        # 📍 INICIO
        self.area_actual = self.areas[1]
        self.area_actual.explorada = True

    @property
    def progreso(self):
        """Cantidad de áreas nuevas descubiertas tras la zona inicial."""
        return max(0, sum(1 for area in self.areas.values() if area.explorada) - 1)

    # ===============================
    # CAMBIAR ÁREA
    # ===============================
    def cambiar_area(self, id_area):
        if id_area in self.areas and id_area in self.area_actual.conexiones:
            self.area_actual = self.areas[id_area]
            self.area_actual.explorada = True
            return True
        return False

    # ===============================
    # ÁREAS DISPONIBLES
    # ===============================
    def obtener_areas_conectadas(self):
        return [self.areas[i] for i in self.area_actual.conexiones]
