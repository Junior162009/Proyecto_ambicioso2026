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


def test_configuration_has_legacy_and_ui_constants():
    assert config.SCREEN_WIDTH > 0
    assert config.SCREEN_HEIGHT > 0
    assert settings.TEXTO_RESPUESTA


def test_all_math_chest_operation_types_return_numeric_answers():
    for kind in ("suma", "resta", "multiplicacion", "division", "potencia", "raiz", "mixta"):
        operation, answer = generar_operacion([kind])
        assert operation
        assert isinstance(answer, int)


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
    assert boss.hp == boss.max_hp - 50


def test_main_adventure_initializes_and_has_playable_area():
    game = main.Juego()
    assert game.mundo.area_actual.id == 1
    assert game.mapa.nivel
    assert game.jugador.vida > 0
    assert game.mapa.paredes


def test_response_ui_initializes():
    ui = SistemaRespuestas(None)
    assert not ui.activo
    assert ui.respuesta_actual == ""


@pytest.fixture(scope="session", autouse=True)
def cleanup_pygame():
    yield
    pygame.quit()
