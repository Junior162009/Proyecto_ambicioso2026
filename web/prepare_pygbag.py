"""Prepara una copia aislada del juego para Pygbag sin tocar la versión de escritorio.

Uso desde la raíz del repositorio:
    python web/prepare_pygbag.py

Genera .pygbag_src/ con el proyecto completo y adapta Juego.ejecutar()
a una corrutina que cede el control al navegador en cada fotograma.
"""
from __future__ import annotations

import ast
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / ".pygbag_src"
EXCLUDE_DIRS = {".git", ".github", ".pytest_cache", ".venv", "venv", "build", "dist", ".pygbag_src", "__pycache__"}
EXCLUDE_FILES = {".DS_Store", ".gitignore.respaldo"}


def copy_project() -> None:
    if STAGING.exists():
        shutil.rmtree(STAGING)
    STAGING.mkdir(parents=True)
    for item in ROOT.iterdir():
        if item.name in EXCLUDE_DIRS or item.name in EXCLUDE_FILES or item.name == "web":
            continue
        destination = STAGING / item.name
        if item.is_dir():
            shutil.copytree(item, destination, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache"))
        elif item.is_file():
            shutil.copy2(item, destination)


def adapt_main() -> None:
    source_path = STAGING / "main.py"
    source = source_path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    lines = source.splitlines()

    # El bucle principal está dentro de Juego.ejecutar(), no al nivel superior.
    juego = next(
        (node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "Juego"),
        None,
    )
    if juego is None:
        raise RuntimeError("No se encontró la clase Juego; no se modificó la copia.")

    ejecutar = next(
        (node for node in juego.body
         if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "ejecutar"),
        None,
    )
    if ejecutar is None:
        raise RuntimeError("No se encontró Juego.ejecutar(); no se modificó la copia.")

    bucle = next((node for node in ast.walk(ejecutar) if isinstance(node, ast.While)), None)
    if bucle is None or not bucle.body:
        raise RuntimeError("No se encontró el bucle principal; no se modificó la copia.")

    # Convierte el método en asíncrono, únicamente en la copia web.
    if isinstance(ejecutar, ast.FunctionDef):
        idx = ejecutar.lineno - 1
        lines[idx] = lines[idx].replace("def ejecutar(", "async def ejecutar(", 1)

    # Cede el control al navegador una vez por fotograma.
    if "await asyncio.sleep(0)" not in source:
        tick_node = next(
            (node for node in ast.walk(bucle)
             if isinstance(node, ast.Expr)
             and isinstance(node.value, ast.Call)
             and isinstance(node.value.func, ast.Attribute)
             and node.value.func.attr == "tick"),
            None,
        )
        if tick_node is not None:
            lines.insert(tick_node.end_lineno, " " * tick_node.col_offset + "await asyncio.sleep(0)")
        else:
            first = bucle.body[0]
            lines.insert(first.lineno - 1, " " * first.col_offset + "await asyncio.sleep(0)")

    source = "\n".join(lines) + "\n"
    if "import asyncio" not in source:
        source = source.replace("import math\n", "import asyncio\nimport math\n", 1)

    # El punto de entrada debe esperar la corrutina.
    source = source.replace("Juego().ejecutar()", "asyncio.run(Juego().ejecutar())")

    # En navegador se utiliza un canvas escalado, no fullscreen exclusivo.
    source = source.replace(
        "PANTALLA = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)",
        'PANTALLA = pygame.display.set_mode((960, 540)) if sys.platform == "emscripten" else pygame.display.set_mode((0, 0), pygame.FULLSCREEN)',
        1,
    )
    source = source.replace(
        "    if PANTALLA.get_flags() & pygame.FULLSCREEN:\n"
        "        PANTALLA = pygame.display.set_mode(_VENTANA_TAM, pygame.RESIZABLE)\n"
        "    else:\n"
        "        PANTALLA = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)",
        "    if sys.platform == \"emscripten\":\n"
        "        PANTALLA = pygame.display.set_mode((960, 540))\n"
        "    elif PANTALLA.get_flags() & pygame.FULLSCREEN:\n"
        "        PANTALLA = pygame.display.set_mode(_VENTANA_TAM, pygame.RESIZABLE)\n"
        "    else:\n"
        "        PANTALLA = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)",
        1,
    )

    # Comprueba sintaxis antes de escribir la copia preparada.
    ast.parse(source)
    source_path.write_text(source, encoding="utf-8")


def main() -> None:
    copy_project()
    adapt_main()
    print(f"Proyecto web preparado en: {STAGING}")


if __name__ == "__main__":
    main()
