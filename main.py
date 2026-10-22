"""Punto de entrada oficial de Mathverse.

En escritorio conserva el bucle tradicional. En Pygbag se crea Pygame dentro
de la corrutina principal para que el runtime web ya esté activo al inicializar
la ventana y el bucle ceda el control al navegador en cada fotograma.
El juego anterior de MATEMIA se conserva en backups/matemia_main_2026-10-21.py.
"""
import asyncio
import sys

import pygame

from mathverse import Mathverse, ejecutar


async def main_web():
    """Inicializa y ejecuta el juego dentro del event loop de Pygbag."""
    game = None
    try:
        game = Mathverse()
        await game.run_web()
    finally:
        if game is not None:
            game.save_game()
        pygame.quit()


if __name__ == "__main__":
    if sys.platform == "emscripten":
        asyncio.run(main_web())
    else:
        ejecutar()
