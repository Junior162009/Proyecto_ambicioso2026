# Mathverse — El Desafío de los 5 Reinos

Juego educativo competitivo en Python y Pygame. El punto de entrada oficial es Mathverse; el código anterior de MATEMIA queda respaldado en `backups/matemia_main_2026-10-21.py`.

## Requisitos

- Python 3.10 o posterior.
- Pygame 2.6.1 o posterior.
- pytest para las pruebas automatizadas.

## Instalación y ejecución (Linux/antiX)

```bash
python3 -m venv env
source env/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

También se puede ejecutar con `python mathverse.py`. Ambos comandos llaman a la misma implementación.

## Controles

- Ratón o teclas 1–4: seleccionar respuestas.
- En el menú, elige partidas de 5, 6 o 7 minutos.
- Clic en los botones inferiores: usar poderes cuando el maná alcance el coste.
- ESC: salir.

## Pruebas

```bash
python -m pip install pytest
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy python -m pytest -q
```

Las pruebas cubren el banco de preguntas, cálculo de puntos, reglas de poderes, validación y escritura atómica del progreso y prevención de recompensas duplicadas. Ejecuta el juego en una sesión gráfica para comprobar visualmente la ventana y los controles.

## Estado funcional conocido

- Modo offline con bots: implementado en el cliente Pygame.
- Cinco reinos: banco inicial de 30 preguntas, con identificador estable, dificultad y explicación; se puede ampliar desde `QUESTIONS`.
- Eventos offline: rondas relámpago de 3 segundos, muerte súbita y bonificación de Jefe del Dominio.
- Bots: cinco personalidades con precisión, preferencias y frecuencia de poderes diferentes.
- Poderes: niebla reduce temporalmente la precisión del bot; congelamiento retrasa su respuesta; robo transfiere puntos de su próxima respuesta; el escudo bloquea un ataque; doble o nada apuesta la próxima ganancia.
- Perfil local: guardado JSON con validación y escritura atómica.
- Online: no se anuncia como funcional. Este repositorio no contiene aún un servidor autoritativo, emparejamiento ni sincronización WebSocket verificados. Para habilitarlo hace falta desplegar y probar esa infraestructura.
- Navegador/Pygbag: no declarado compatible ni probado en esta entrega.

## Organización

- `main.py`: lanzador oficial.
- `mathverse.py`: ventana, menús, partida y renderizado Pygame.
- `mathverse_core.py`: validación de preguntas, puntuación, reglas de poderes y persistencia segura.
- `tests/test_mathverse.py`: pruebas automatizadas.
- `backups/`: respaldo del punto de entrada de MATEMIA previo a la migración.

## Versión web de prueba

Mathverse usa Pygbag para empaquetar Pygame en WebAssembly. El flujo `.github/workflows/mathverse-web.yml` construye una versión de navegador en cada cambio a `main` o `mathverse-finalizacion`.

- En la pestaña **Actions**, abre **Mathverse Web (Pygbag)** y descarga el artefacto `mathverse-web-build` para revisar el paquete generado.
- La publicación automática en GitHub Pages está configurada solo para `main`, para no publicar cambios de una rama de trabajo antes de integrarlos.
- El bucle del navegador es asíncrono y cede el control con `await asyncio.sleep(0)`, como requiere Pygbag.
- El modo de escritorio sigue usando `python main.py`.
- Esta configuración no convierte el juego en multijugador en línea. El guardado persistente del navegador y la compatibilidad visual todavía deben comprobarse en un navegador real.

Para probar localmente: instala Pygbag (`python -m pip install pygbag pygame-ce`) y ejecuta `python -m pygbag .`; luego abre la dirección local que muestre el servidor de Pygbag.
