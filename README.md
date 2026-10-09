# Proyecto Ambicioso 2026 — Matemia

Juego educativo de aventura desarrollado en Python y Pygame. El repositorio conserva los módulos en español y los nombres de compatibilidad en inglés para evitar errores de importación en las partes antiguas del proyecto.

## Requisitos

- Python 3.10 o posterior.
- Pygame 2.6 o posterior.

## Instalación en Linux (incluido antiX)

Desde la carpeta del repositorio:

```bash
python3 -m venv env
source env/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

Si el entorno virtual ya existe, basta con activarlo e instalar las dependencias. No es necesario instalar Android Studio.

## Controles de la aventura

- **WASD** o flechas: mover al personaje.
- **Clic izquierdo**: disparar hacia el cursor.
- **E**: interactuar con cofres, habitantes y salidas.
- **T**: abrir la tienda; usa las teclas **1–7** para comprar.
- **Q**: abrir misiones; usa los números para aceptar una misión.
- **I**: abrir el inventario; usa los números para consumir objetos.
- **M**: consultar el mapa mundial.
- **R**: usar un cargador extra para recuperar 10 balas; después de perder, también reinicia la aventura.
- **Enter**: confirmar la respuesta matemática del cofre.
- **Retroceso**: borrar la respuesta.
- **Esc**: cerrar el panel abierto o salir del juego.

El juego busca recursos en la carpeta `assets/`. Si una imagen no está disponible, usa un recurso gráfico de respaldo para que la ausencia del archivo no cierre el juego.

## Pruebas automáticas

Instala también pytest y ejecuta:

```bash
python -m pip install pytest
python -m pytest -q
```

Las pruebas se ejecutan en modo gráfico ficticio (SDL dummy) y comprueban importaciones, configuración, operaciones matemáticas, rutas del mundo, inventario/tienda, misiones, jefe final y arranque de la aventura. GitHub Actions ejecuta estas pruebas en cada push a `main` y en cada pull request.

## Organización

- `main.py`: aventura principal con exploración, cofres, combate y áreas.
- `mundo.py`, `mapa.py`: generación del mundo, rutas y colisiones.
- `jugador.py`, `enemigo.py`, `boss.py`, `bala.py`: entidades y combate.
- `cofre.py`, `misiones.py`, `progresion.py`, `tienda.py`: sistemas educativos y de progresión.
- `ui.py`, `sistema_respuestas.py`, `menu.py`, `areas.py`: componentes de interfaz.
- `game.py`: modo de combate por niveles mantenido por compatibilidad.
- `config.py`, `player.py`, `enemy.py`, `combat.py`, `levels.py`: adaptadores para nombres usados por el código antiguo.

## Reportar errores

Si el juego muestra un traceback, copia el error completo junto con el comando que ejecutaste. No borres cambios locales ni uses `git reset --hard` para resolver conflictos sin revisar primero los archivos.
