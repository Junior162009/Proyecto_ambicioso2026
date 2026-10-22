# MATEMIA — Mundo Libre Matemático

Juego educativo de aventura creado con Python y Pygame. Explora áreas, combate enemigos, abre cofres matemáticos, conversa con NPC, completa misiones y mejora tu inventario.

## Ejecutar en escritorio (Linux/antiX)

Requiere Python 3.10 o posterior y Pygame.

```bash
python3 -m venv env
source env/bin/activate
python -m pip install --upgrade pip
python -m pip install pygame-ce pytest pygbag
python main.py
```

Si ya tienes un entorno virtual preparado, actívalo y ejecuta `python main.py`.

## Jugar desde el navegador

La versión web se construye con Pygbag a partir del juego original, usando una copia de preparación para navegador. El archivo `main.py` de escritorio se conserva sin convertir su bucle principal.

1. Abre la pestaña **Actions** del repositorio y entra en **MATEMIA Web (Pygbag)**.
2. Espera a que terminen los trabajos **build** y **deploy**.
3. Cuando finalice correctamente, abre: https://junior162009.github.io/Proyecto_ambicioso2026/

La primera carga puede tardar porque el navegador descarga Pygame y los recursos gráficos. Si la acción falla, abre su registro y revisa el paso de compilación.

Para probar localmente el paquete web:

```bash
python web/prepare_pygbag.py
cd .pygbag_src
python -m pygbag .
```

## Controles

- **WASD o flechas:** mover al personaje.
- **Clic en el mundo:** disparar.
- **E:** interactuar / abrir cofres.
- **T:** tienda.
- **I:** inventario.
- **Q:** misiones.
- **M:** mapa.
- **F11:** alternar pantalla en escritorio.
- **+ / -:** ajustar zoom.
- **ESC:** cerrar un panel o salir.

## Pruebas

```bash
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy python -m pytest -q
```

## Archivos principales

- `main.py`: juego original MATEMIA para escritorio.
- `web/prepare_pygbag.py`: crea una copia compatible con el bucle asíncrono del navegador.
- `assets/`: gráficos del jugador, terreno, cofres y UI.
- `backups/matemia_main_2026-10-21.py`: copia de respaldo del punto de entrada original.

## Alcance

La versión de navegador permite jugar la aventura localmente dentro del navegador; no representa un modo multijugador en línea. La compatibilidad final debe confirmarse con la compilación de GitHub Actions y una prueba real en el navegador.
