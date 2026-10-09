# levels.py - Gestión de niveles
"""
Define los 10 niveles con dificultad progresiva
"""

# niveles.py - SISTEMA DE NIVELES MEJORADO

class Nivel:
    def __init__(self, numero, enemigos, dificultad, es_jefe=False):
        self.numero = numero
        self.enemigos = enemigos
        self.dificultad = dificultad
        self.es_jefe = es_jefe


class GestorNiveles:
    def __init__(self):
        self.nivel_actual = 1
        self.total_niveles = 10

        self.niveles = self.crear_niveles()

    def crear_niveles(self):
        niveles = {}

        for i in range(1, 11):
            if i == 10:
                niveles[i] = Nivel(
                    numero=i,
                    enemigos=1,
                    dificultad=3.0,
                    es_jefe=True
                )
            else:
                niveles[i] = Nivel(
                    numero=i,
                    enemigos=5 + i * 2,
                    dificultad=1.0 + (i * 0.2),
                    es_jefe=False
                )

        return niveles

    def obtener_nivel_actual(self):
        return self.niveles[self.nivel_actual]

    def es_nivel_jefe(self):
        return self.obtener_nivel_actual().es_jefe

    def siguiente_nivel(self):
        if self.nivel_actual < self.total_niveles:
            self.nivel_actual += 1

    def reiniciar(self):
        self.nivel_actual = 1

    def info(self):
        nivel = self.obtener_nivel_actual()
        if nivel.es_jefe:
            return f"Nivel {nivel.numero} - JEFE FINAL"
        return f"Nivel {nivel.numero} - Enemigos: {nivel.enemigos} - Dificultad x{nivel.dificultad}"
