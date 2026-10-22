"""Punto de entrada oficial de Mathverse.

En escritorio usa el bucle tradicional; en navegador, Pygbag necesita un
bucle asíncrono para ceder el control al navegador en cada fotograma.
El juego anterior de MATEMIA se conserva en backups/matemia_main_2026-10-21.py.
"""
import asyncio
import sys

from mathverse import Mathverse, ejecutar


if __name__ == "__main__":
    if sys.platform == "emscripten":
        asyncio.run(Mathverse().run_web())
    else:
        ejecutar()
