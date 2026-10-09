# tienda.py — Sistema de Tienda
from settings import *

class Tienda:
    def __init__(self):
        self.catalogo = [
            {"id": "pocion_vida",      "nombre": "Poción de Vida",      "precio": PRECIOS_TIENDA["pocion_vida"],      "efecto": "Restaura hasta 35 puntos de vida"},
            {"id": "balas_extra",      "nombre": "Cargador Extra",       "precio": PRECIOS_TIENDA["balas_extra"],      "efecto": "+10 balas al usarlo"},
            {"id": "pocion_velocidad", "nombre": "Poción de Velocidad",  "precio": PRECIOS_TIENDA["pocion_velocidad"], "efecto": "+2 velocidad por 30s"},
            {"id": "pocion_fuerza",    "nombre": "Poción de Fuerza",     "precio": PRECIOS_TIENDA["pocion_fuerza"],    "efecto": "+50% daño por 30s"},
            {"id": "pocion_defensa",   "nombre": "Escudo Mágico",        "precio": PRECIOS_TIENDA["pocion_defensa"],   "efecto": "-50% daño recibido por 30s"},
            {"id": "mapa",             "nombre": "Mapa del Área",        "precio": PRECIOS_TIENDA["mapa"],             "efecto": "Abre el mapa mundial"},
            {"id": "llave",            "nombre": "Llave Maestra",        "precio": PRECIOS_TIENDA["llave"],            "efecto": "Viaja a un área conectada"},
        ]

    def obtener_items_compra(self):
        return self.catalogo

    def comprar(self, item_id, jugador):
        for item in self.catalogo:
            if item["id"] == item_id:
                if jugador.puntos >= item["precio"]:
                    jugador.puntos -= item["precio"]
                    jugador.agregar_item(item_id)
                    return True, f"¡Compraste {item['nombre']}!"
                else:
                    return False, "No tienes suficientes puntos."
        return False, "Item no encontrado."
