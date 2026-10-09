import pygame
import os

pygame.init()

# Crear directorio si no existe
os.makedirs("assets/objetos", exist_ok=True)

# Tamaño
TAM = 48

# 1. Cofre cerrado (48x48)
cofre_cerrado = pygame.Surface((TAM, TAM), pygame.SRCALPHA)
cofre_cerrado.fill((160, 120, 80, 255))  # Marrón claro
pygame.draw.rect(cofre_cerrado, (120, 80, 40), (0, 0, TAM, TAM), 3)
pygame.draw.rect(cofre_cerrado, (200, 160, 120), (4, 4, TAM-8, TAM-8), 2)
# Cerradura
pygame.draw.rect(cofre_cerrado, (218, 165, 32), (TAM//2-6, TAM//2-8, 12, 16))
pygame.draw.circle(cofre_cerrado, (255, 215, 0), (TAM//2, TAM//2-2), 4)

# 2. Cofre abierto (48x48)
cofre_abierto = pygame.Surface((TAM, TAM), pygame.SRCALPHA)
cofre_abierto.fill((255, 215, 0, 255))  # Dorado brillante
pygame.draw.rect(cofre_abierto, (184, 134, 11), (0, 0, TAM, TAM), 3)
# Interior marrón
pygame.draw.rect(cofre_abierto, (139, 69, 19), (6, 10, TAM-12, TAM-18))
# Tesoro
for i in range(3):
    for j in range(2):
        pygame.draw.circle(cofre_abierto, (255, 255, 100), 
                          (TAM//4 + i*12, TAM//3 + j*12), 5)

# Guardar
pygame.image.save(cofre_cerrado, "assets/objetos/cofre_cerrado.png")
pygame.image.save(cofre_abierto, "assets/objetos/cofre_abierto.png")

print("✅ Cofres 48x48 creados!")
print("🎮 Ahora ejecuta: python3 main.py")
