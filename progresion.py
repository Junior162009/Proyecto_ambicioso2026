# progresion.py — Sistema de Progresión de Historia
from settings import *

class ProgresionHistoria:
    def __init__(self):
        self.hitos_alcanzados = set()
        self.fase_actual = "inicio"

    def verificar_progreso(self, jugador, mundo):
        """Verifica si se alcanzaron nuevos hitos y devuelve mensajes."""
        mensajes = []

        # Hito: primer enemigo eliminado
        if jugador.enemigos_eliminados >= 1 and "primer_enemigo" not in self.hitos_alcanzados:
            self.hitos_alcanzados.add("primer_enemigo")
            mensajes.append("¡Primer enemigo derrotado! El Liche te observa...")

        # Hito: primer cofre resuelto
        if len(jugador.operaciones) >= 1 and "primer_cofre" not in self.hitos_alcanzados:
            self.hitos_alcanzados.add("primer_cofre")
            mensajes.append("¡Cofre resuelto! La magia matemática fluye en ti.")

        # Hito: nivel 3 de experiencia
        if jugador.nivel >= 3 and "nivel_3" not in self.hitos_alcanzados:
            self.hitos_alcanzados.add("nivel_3")
            mensajes.append("¡Nivel 3 alcanzado! Eres un aventurero experimentado.")

        # Hito: llegar a mazmorras
        if mundo.progreso >= 2 and "mazmorras" not in self.hitos_alcanzados:
            self.hitos_alcanzados.add("mazmorras")
            mensajes.append("¡Has llegado a las mazmorras! El Liche está cerca.")

        # Hito: llegar al reino
        if mundo.progreso >= 3 and "reino" not in self.hitos_alcanzados:
            self.hitos_alcanzados.add("reino")
            mensajes.append("¡El reino te da la bienvenida! La batalla final se acerca.")

        return mensajes
