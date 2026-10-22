"""Pruebas básicas ejecutables sin una ventana gráfica real."""
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame
import pytest

pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))

import settings
import config
import main
from mundo import Mundo
from cofre import Cofre, generar_operacion
from tienda import Tienda
from player import Player
from game import Game
from boss import Boss
from levels import LevelManager
from sistema_respuestas import SistemaRespuestas
from misiones import SistemaMisiones
from game import GameState


def test_configuration_has_legacy_and_ui_constants():
    assert config.SCREEN_WIDTH > 0
    assert config.SCREEN_HEIGHT > 0
    assert settings.TEXTO_RESPUESTA


def test_all_math_chest_operation_types_return_numeric_answers():
    for kind in ("suma", "resta", "multiplicacion", "division", "potencia", "raiz", "mixta"):
        operation, answer = generar_operacion([kind])
        assert operation
        assert isinstance(answer, int)


def test_chest_uses_original_assets_and_cannot_be_resolved_twice():
    chest = Cofre(96, 96)
    assert chest.rect.size == (settings.TAM, settings.TAM)
    assert chest.img.get_size() == (settings.TAM, settings.TAM)
    assert chest.img_abierto.get_size() == (settings.TAM, settings.TAM)
    assert chest.abrir()
    assert chest.resolver()
    assert not chest.resolver()
    assert chest.puede_reclamar_recompensa()
    assert not chest.puede_reclamar_recompensa()


def test_world_has_valid_bidirectional_routes():
    world = Mundo()
    for area in world.areas.values():
        for destination in area.conexiones:
            assert destination in world.areas
            assert area.id in world.areas[destination].conexiones


def test_shop_can_add_an_item_to_player_inventory():
    player = Player(100, 100)
    player.puntos = 100
    ok, message = Tienda().comprar("pocion_vida", player)
    assert ok, message
    assert player.inventario["pocion_vida"] == 1
    assert player.puntos == 60


def test_legacy_game_can_initialize_with_compatibility_modules():
    manager = LevelManager()
    assert manager.get_current_config()["enemies"] > 0
    game = Game(SCREEN)
    assert game.player.is_alive()
    assert game.enemies
    boss = Boss(300, 200)
    assert boss.is_alive()
    boss.take_damage(50)
    assert boss.hp == boss.max_hp - 50def test_response_ui_initializes():
    ui = SistemaRespuestas(None)
    assert not ui.activo
    assert ui.respuesta_actual == ""


@pytest.fixture(scope="session", autouse=True)
def cleanup_pygame():
    yield
    pygame.quit()


def test_legacy_level_completes_and_victory_can_restart():
    game = Game(SCREEN)
    game.enemies.clear()
    game.update()
    assert game.state == GameState.LEVEL_COMPLETE
    game._handle_level_transition()
    assert game.level_manager.current_level == 2
    game.level_manager.current_level = game.level_manager.total_levels
    game._init_level()
    game.boss.hp = 0
    game.update()
    assert game.state == GameState.LEVEL_COMPLETE
    game._handle_level_transition()
    assert game.state == GameState.BOSS_DEFEATED
    game._handle_level_transition()
    assert game.state == GameState.PLAYING
    assert game.level_manager.current_level == 1


def test_missions_can_be_accepted_and_rewards_claimed_once():
    missions = SistemaMisiones()
    ok, _ = missions.aceptar_mision(1)
    assert ok
    assert len(missions.misiones_activas) == 1
    for _ in range(5):
        messages = missions.actualizar_mision_matando("Básico")
    assert messages
    player = Player(100, 100)
    before = player.puntos
    missions.reclamar_recompensas(player)
    assert player.puntos == before + 100
    missions.reclamar_recompensas(player)
    assert player.puntos == before + 100


def test_every_runtime_module_imports():
    import importlib
    modules = (
        "areas", "bala", "boss", "combat", "combate", "config", "cofre",
        "enemy", "enemigo", "game", "jefe", "jugador", "levels", "main",
        "mapa", "menu", "misiones", "mundo", "niveles", "npc", "player",
        "progresion", "puerta", "settings", "sistema_respuestas", "tienda", "ui",
    )
    for module_name in modules:
        assert importlib.import_module(module_name) is not None, module_namedef test_generated_areas_always_have_a_spawn_tile():
    from mundo import AreaMundo
    for _ in range(12):
        for area in (
            AreaMundo(1, "Bosque", "bosque", (20, 20), 2),
            AreaMundo(2, "Cueva", "cueva", (25, 25), 5),
        ):
            assert any("P" in fila for fila in area.mapa)

def test_main_is_the_official_mathverse_launcher():
    import mathverse
    assert main.ejecutar is mathverse.ejecutar
    assert hasattr(mathverse, "Mathverse")
