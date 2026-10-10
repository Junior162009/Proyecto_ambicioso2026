# 🌐 Proyecto Ambicioso 2026 en navegador

El juego de escritorio sigue usando `main.py` normalmente. La versión web se prepara automáticamente en una copia temporal para no alterar la versión de PC.

## Requisitos para desarrollo local

- Python 3.12 recomendado para Pygbag 0.9.3.
- Pygbag 0.9.3.
- Navegador moderno, preferiblemente Chrome/Chromium.

## Probar localmente

Desde la raíz del repositorio:

```bash
python -m pip install --upgrade pygbag==0.9.3
python web/prepare_pygbag.py
python -m pygbag .pygbag_src
```

Después abre `http://localhost:8000`.

Para depuración de Pygbag se puede usar `http://localhost:8000/#debug`.

## Qué hace la preparación

- Copia módulos, imágenes, fuentes y demás recursos al staging `.pygbag_src/`.
- Conserva `main.py` de escritorio sin modificar.
- Convierte automáticamente el bucle principal de la copia web a `async def main()` y añade `await asyncio.sleep(0)` por frame.
- Usa un canvas escalable en navegador en vez del `pygame.FULLSCREEN` del escritorio.
- Mantiene la lógica del juego, mapas, cofres, enemigos, preguntas, combate, progresión y recursos originales.

## Publicación

El workflow `.github/workflows/pygbag-pages.yml` prepara la copia, ejecuta Pygbag 0.9.3, verifica `build/web/index.html` y publica el resultado mediante GitHub Pages.

La publicación se activa automáticamente con cada push a `main` y también puede lanzarse manualmente desde GitHub Actions.

## Limitaciones web conocidas

El navegador no tiene el mismo acceso al sistema de archivos que Windows/Linux. Las partidas que dependan de archivos locales deberán migrarse a almacenamiento del navegador si el proyecto usa guardado persistente en disco.

El audio del navegador puede requerir una primera interacción del usuario por las políticas de reproducción automática.
