import os
import pygame

# Inicializar pygame para cargar imágenes
pygame.init()

# Rutas a verificar
rutas = [
    "assets/objetos/cofre_cerrado.png",
    "assets/objetos/cofre_abierto.png",
    "assets/objetos/puerta.png",
    "assets/sprites/jugador.png",
    "assets/tiles/suelo.png",
    "assets/tiles/pared.png"
]

print("=== VERIFICANDO ARCHIVOS DE IMÁGENES ===")
for ruta in rutas:
    if os.path.exists(ruta):
        print(f"✓ EXISTE: {ruta}")
        try:
            # Intentar cargar con pygame
            img = pygame.image.load(ruta)
            print(f"  Tamaño: {img.get_size()}")
        except Exception as e:
            print(f"  ERROR al cargar: {e}")
    else:
        print(f"✗ NO EXISTE: {ruta}")
