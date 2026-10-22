# Mathverse en navegador

El punto de entrada de la versión actual es `main.py` y el juego principal es `mathverse.py`. Pygbag empaqueta directamente esta versión; no uses el antiguo script `web/prepare_pygbag.py`, que fue creado para el juego anterior y busca una clase `Juego` que ya no es el punto de entrada actual.

## Probar en tu equipo

Desde la raíz del repositorio, con Python 3.11 recomendado:

```bash
python -m pip install --upgrade pygbag==0.9.3 pygame-ce
python -m pygbag .
```

Cuando termine la preparación, abre la dirección local que indique Pygbag (normalmente `http://localhost:8000`). La primera carga puede tardar porque el navegador descarga el runtime de WebAssembly.

## Publicación de prueba en GitHub

El workflow `.github/workflows/pygbag-pages.yml` compila Mathverse en cada push a `main` y `mathverse-finalizacion`. En cualquier rama, descarga el artefacto `mathverse-web-build` desde la ejecución de Actions. Solo la rama `main` activa la publicación de GitHub Pages, para evitar publicar cambios de prueba antes de integrar la rama.

## Limitaciones que deben comprobarse

- El bucle del navegador usa `asyncio.sleep(0)` para ceder el control a WebAssembly.
- La partida offline con bots no es multijugador en Internet.
- El progreso guardado en archivos locales podría no persistir entre sesiones del navegador.
- El paquete generado debe probarse en un navegador real; que Pygbag compile no demuestra por sí solo que toda la partida sea compatible.
