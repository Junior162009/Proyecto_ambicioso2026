# misiones.py — Sistema de Misiones
import random
from settings import *

class Mision:
    def __init__(self, id_, titulo, descripcion, tipo, objetivo, cantidad, npc="???", recompensa=100):
        self.id          = id_
        self.titulo      = titulo
        self.descripcion = descripcion
        self.tipo        = tipo       # "matar", "cofre", "explorar"
        self.objetivo    = objetivo   # tipo de enemigo o acción
        self.cantidad    = cantidad
        self.progreso    = 0
        self.completada  = False
        self.npc         = npc
        self.recompensa  = recompensa

    def actualizar(self, cantidad=1):
        if not self.completada:
            self.progreso = min(self.progreso + cantidad, self.cantidad)
            if self.progreso >= self.cantidad:
                self.completada = True
                return True
        return False

    def info(self):
        return {
            "titulo":      self.titulo,
            "descripcion": self.descripcion,
            "progreso":    f"{self.progreso}/{self.cantidad}",
            "completada":  self.completada,
            "npc":         self.npc,
        }


class SistemaMisiones:
    def __init__(self):
        self.misiones_disponibles  = []
        self.misiones_activas      = []
        self.misiones_completadas  = []
        self._cargar_misiones_iniciales()

    def _cargar_misiones_iniciales(self):
        base = self.cargar_misiones_base()
        self.misiones_disponibles = base[:3]

    def cargar_misiones_base(self):
        return [
            Mision(1,  "Cazador Novato",        "Elimina 5 enemigos básicos.",           "matar",   "Básico",       5,  "Anciano",  100),
            Mision(2,  "Descifrador",            "Abre 3 cofres resolviendo operaciones.","cofre",   "cofre",        3,  "Mago",     150),
            Mision(3,  "Explorador",             "Explora 3 áreas del mundo.",            "explorar","area",         3,  "Explorador",80),
            Mision(4,  "Cazador de Sombras",     "Elimina 3 enemigos camuflados.",        "matar",   "Camuflado",    3,  "Guerrero", 200),
            Mision(5,  "Tirador",                "Elimina 2 enemigos disparadores.",      "matar",   "Disparador",   2,  "Guerrero", 250),
            Mision(6,  "Coleccionista",          "Abre 10 cofres en total.",              "cofre",   "cofre",       10,  "Comerciante",300),
            Mision(7,  "Exterminador",           "Elimina 20 enemigos.",                  "matar",   "cualquier",   20,  "Rey",      500),
            Mision(8,  "Matemático",             "Resuelve 10 cofres correctos.",         "cofre",   "cofre",       10,  "Mago",     400),
            Mision(9,  "Preparado para el Jefe", "Llega al nivel 5 de experiencia.",      "nivel",   "nivel",        5,  "Anciano",  600),
            Mision(10, "Héroe del Reino",        "Derrota al Liche Matemático.",          "boss",    "Liche",        1,  "Rey",     2000),
        ]

    def obtener_misiones_activas(self):
        return [m.info() for m in self.misiones_activas if not m.completada]

    def obtener_misiones_disponibles(self):
        return [m.info() for m in self.misiones_disponibles]

    def actualizar_mision_matando(self, tipo_enemigo):
        mensajes = []
        for mision in self.misiones_activas:
            if mision.tipo == "matar" and not mision.completada:
                if mision.objetivo in ("cualquier", tipo_enemigo):
                    if mision.actualizar():
                        mensajes.append(f"✅ Misión completada: {mision.titulo} (+{mision.recompensa} pts)")
                        self.misiones_completadas.append(mision)
        return mensajes

    def actualizar_mision_cofre(self):
        mensajes = []
        for mision in self.misiones_activas:
            if mision.tipo == "cofre" and not mision.completada:
                if mision.actualizar():
                    mensajes.append(f"✅ Misión completada: {mision.titulo} (+{mision.recompensa} pts)")
                    self.misiones_completadas.append(mision)
        return mensajes

    def actualizar_mision_boss(self):
        mensajes = []
        for mision in self.misiones_activas:
            if mision.tipo == "boss" and not mision.completada:
                if mision.actualizar():
                    mensajes.append(f"🏆 ¡MISIÓN ÉPICA COMPLETADA: {mision.titulo}! (+{mision.recompensa} pts)")
                    self.misiones_completadas.append(mision)
        return mensajes
