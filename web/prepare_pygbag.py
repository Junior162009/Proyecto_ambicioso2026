"""Prepara una copia aislada del juego para Pygbag sin tocar la versión de escritorio.

Uso desde la raíz del repositorio:
    python web/prepare_pygbag.py

Genera .pygbag_src/ con el proyecto completo y un main.py adaptado al bucle
asíncrono requerido por Pygbag.
"""
from __future__ import annotations

import ast
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / ".pygbag_src"
EXCLUDE_DIRS = {".git", ".github", ".pytest_cache", ".venv", "venv", "build", "dist", ".pygbag_src"}
EXCLUDE_FILES = {".DS_Store"}


def copy_project() -> None:
    if STAGING.exists():
        shutil.rmtree(STAGING)
    STAGING.mkdir(parents=True)
    for item in ROOT.iterdir():
        if item.name in EXCLUDE_DIRS or item.name in EXCLUDE_FILES or item.name == "web":
            continue
        destination = STAGING / item.name
        if item.is_dir():
            shutil.copytree(item, destination)
        elif item.is_file():
            shutil.copy2(item, destination)


def adapt_main() -> None:
    source_path = STAGING / "main.py"
    source = source_path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    # Si ya está adaptado, no lo vuelvas a envolver.
    if any(isinstance(node, ast.AsyncFunctionDef) and node.name == "main" for node in tree.body):
        if "asyncio.run(main())" in source:
            return

    module_while = next((node for node in tree.body if isinstance(node, ast.While)), None)
    if module_while is None:
        raise RuntimeError(
            "No se encontró el bucle principal while en main.py. "
            "La adaptación automática fue detenida para no alterar el juego."
        )

    lines = source.splitlines()
    start = module_while.lineno - 1
    prefix = lines[:start]
    loop_and_tail = lines[start:]

    while_indent = len(loop_and_tail[0]) - len(loop_and_tail[0].lstrip())
    if while_indent != 0:
        raise RuntimeError("El bucle principal no está al nivel superior del archivo.")
    if not module_while.body:
        raise RuntimeError("El bucle principal no tiene cuerpo.")

    # El yield se ejecuta una vez por frame para devolver el control al navegador.
    first_body_line = module_while.body[0].lineno - module_while.lineno
    insertion = max(1, first_body_line)
    loop_and_tail.insert(insertion, "    await asyncio.sleep(0)")
    loop_and_tail = ["    " + line if line else line for line in loop_and_tail]

    if not any(line.strip() == "import asyncio" for line in prefix):
        import_pos = 0
        for i, line in enumerate(prefix):
            if line.startswith("import ") or line.startswith("from "):
                import_pos = i + 1
        prefix.insert(import_pos, "import asyncio")

    adapted = prefix + ["", "", "async def main():"] + loop_and_tail + ["", "", "asyncio.run(main())", ""]
    source = "\n".join(adapted)

    # En navegador no usamos pygame.FULLSCREEN del escritorio: el canvas de Pygbag
    # se escala al espacio disponible y el navegador conserva su propio fullscreen.
    source = source.replace(
        'PANTALLA = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)',
        'PANTALLA = pygame.display.set_mode((ANCHO, ALTO), pygame.SCALED | pygame.RESIZABLE) if sys.platform == "emscripten" else pygame.display.set_mode((0, 0), pygame.FULLSCREEN)',
    )
    source = source.replace(
        '    if PANTALLA.get_flags() & pygame.FULLSCREEN:\n        PANTALLA = pygame.display.set_mode(_VENTANA_TAM, pygame.RESIZABLE)\n    else:\n        PANTALLA = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)',
        '    if sys.platform == "emscripten":\n        PANTALLA = pygame.display.set_mode((ANCHO, ALTO), pygame.SCALED | pygame.RESIZABLE)\n    elif PANTALLA.get_flags() & pygame.FULLSCREEN:\n        PANTALLA = pygame.display.set_mode(_VENTANA_TAM, pygame.RESIZABLE)\n    else:\n        PANTALLA = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)',
    )
    source_path.write_text(source, encoding="utf-8")


def main() -> None:
    copy_project()
    adapt_main()
    print(f"Proyecto web preparado en: {STAGING}")


if __name__ == "__main__":
    main()
