import json
from pathlib import Path

import mathverse_core as core
from mathverse import QUESTIONS, Bot, Mathverse


def test_five_domains_have_valid_questions():
    assert core.validate_question_bank(QUESTIONS) == []
    assert set(QUESTIONS) == set(range(5))
    assert all(QUESTIONS[domain] for domain in range(5))


def test_score_correctness_speed_and_timeout():
    assert core.score_answer(True, 0, 10) == 110
    assert core.score_answer(True, 9, 10) > 0
    assert core.score_answer(False, 1, 10) == 0
    assert core.score_answer(True, 11, 10) == 0


def test_power_costs_and_point_theft_are_bounded():
    assert core.apply_power(0, 29, 50, 10)["ok"] is False
    result = core.apply_power(2, 55, 30, 10)
    assert result["ok"] and result["stolen"] == 30
    assert result["target_score"] == 0 and result["own_score"] == 40
    assert core.apply_power(99, 100, 0, 0)["ok"] is False


def test_save_validation_rejects_corrupt_values():
    assert core.validate_save(None)["xp"] == 0
    result = core.validate_save({"xp": -7, "brain_coins": "infinito", "cosmetic": "../bad"})
    assert result == {"xp": 0, "brain_coins": 0, "cosmetic": "aura", "completed_match_ids": []}


def test_atomic_save_round_trip(tmp_path):
    path = tmp_path / "profile.json"
    data = core.validate_save({"xp": 42, "brain_coins": 7, "cosmetic": "fuego"})
    core.atomic_write_json(path, data)
    assert json.loads(path.read_text(encoding="utf-8")) == data


def test_match_finish_is_idempotent(monkeypatch, tmp_path):
    monkeypatch.setattr("mathverse.SAVE_FILE", tmp_path / "save.json")
    game = Mathverse.__new__(Mathverse)
    game.state = "match"
    game.score = 160
    game.brain_coins = 0
    game.xp = 0
    game.cosmetic = "aura"
    game.save = {"completed_match_ids": []}
    game.finish()
    first = (game.brain_coins, game.xp)
    game.finish()
    assert (game.brain_coins, game.xp) == first
    assert (tmp_path / "save.json").exists()


def test_bot_personality_and_timing_values_are_bounded():
    bot = Bot("Prueba", 0)
    assert 0 <= bot.mana <= 100
    assert bot.answer_timer > 0
