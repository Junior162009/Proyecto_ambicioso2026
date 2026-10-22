"""Reglas puras y verificables de Mathverse, sin dependencias de Pygame."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Any
import json
import os
from pathlib import Path
import tempfile

DOMAIN_NAMES = ("Dominio Numérico", "Dominio Global", "Dominio de la Palabra",
                "Dominio de las Civilizaciones", "Dominio de la Vida")
VALID_COSMETICS = {"aura", "electricidad", "fuego"}
POWER_RULES = {
    0: {"name": "NIEBLA MENTAL", "cost": 30, "duration": 3.0, "cooldown": 12.0},
    1: {"name": "CONGELAMIENTO", "cost": 45, "duration": 3.0, "cooldown": 15.0},
    2: {"name": "ROBO DE PUNTOS", "cost": 55, "duration": 0.0, "cooldown": 18.0},
    3: {"name": "ESCUDO DE SABIDURÍA", "cost": 35, "duration": 10.0, "cooldown": 12.0},
    4: {"name": "DOBLE O NADA", "cost": 40, "duration": 0.0, "cooldown": 15.0},
}

@dataclass(frozen=True)
class Question:
    id: str
    domain: int
    difficulty: str
    age_band: str
    prompt: str
    options: tuple[str, ...]
    correct_index: int
    explanation: str = ""

def validate_question_bank(bank: Mapping[int, Iterable[tuple]]) -> list[str]:
    """Devuelve errores de estructura; lista vacía significa que el banco es válido."""
    errors = []
    seen = set()
    for domain in range(5):
        items = bank.get(domain, ())
        if not items:
            errors.append(f"dominio {domain}: sin preguntas")
        for index, item in enumerate(items):
            if not isinstance(item, (tuple, list)) or len(item) < 3:
                errors.append(f"dominio {domain}, pregunta {index}: formato inválido")
                continue
            prompt, options, correct = item[:3]
            qid = f"realm-{domain + 1}-q-{index + 1:04d}"
            if qid in seen:
                errors.append(f"ID duplicado: {qid}")
            seen.add(qid)
            if not isinstance(prompt, str) or not prompt.strip():
                errors.append(f"{qid}: enunciado vacío")
            if not isinstance(options, (tuple, list)) or len(options) < 2:
                errors.append(f"{qid}: necesita al menos dos opciones")
            elif any(not isinstance(option, str) or not option.strip() for option in options):
                errors.append(f"{qid}: opción vacía o inválida")
            elif len({str(option).strip().casefold() for option in options}) != len(options):
                errors.append(f"{qid}: opciones duplicadas")
            if not isinstance(correct, int) or isinstance(correct, bool) or not isinstance(options, (tuple, list)) or not 0 <= correct < len(options):
                errors.append(f"{qid}: índice de respuesta correcta fuera de opciones")
    return errors

def score_answer(correct: bool, elapsed: float, limit: float, combo: int = 0, multiplier: int = 1) -> int:
    if not correct or limit <= 0 or elapsed > limit:
        return 0
    speed = max(0.2, min(1.0, 1.0 - max(0.0, elapsed) / limit))
    return max(0, int(55 + 55 * speed) + max(0, combo) * 8) * max(1, multiplier)

def apply_power(power_index: int, mana: int, target_score: int, own_score: int,
                shield_active: bool = False, double_or_nothing: bool = False) -> dict[str, Any]:
    """Calcula un efecto validado; el llamador aplica el resultado al estado de juego."""
    if power_index not in POWER_RULES:
        return {"ok": False, "reason": "Poder desconocido"}
    rule = POWER_RULES[power_index]
    if mana < rule["cost"]:
        return {"ok": False, "reason": "Maná insuficiente"}
    if power_index == 3 and shield_active:
        return {"ok": False, "reason": "El escudo ya está activo"}
    if power_index == 4 and double_or_nothing:
        return {"ok": False, "reason": "Ya existe una apuesta activa"}
    new_mana = mana - rule["cost"]
    if power_index == 2:
        stolen = min(80, max(0, target_score))
        return {"ok": True, "mana": new_mana, "target_score": target_score-stolen,
                "own_score": own_score+stolen, "stolen": stolen, "duration": 0.0}
    return {"ok": True, "mana": new_mana, "target_score": target_score,
            "own_score": own_score, "stolen": 0, "duration": rule["duration"]}

def validate_save(data: Any) -> dict[str, Any]:
    """Filtra el progreso persistido y descarta valores corruptos o imposibles."""
    if not isinstance(data, dict):
        data = {}
    def nonnegative_int(key):
        value = data.get(key, 0)
        return max(0, min(10_000_000, value)) if isinstance(value, int) and not isinstance(value, bool) else 0
    cosmetic = data.get("cosmetic", "aura")
    if cosmetic not in VALID_COSMETICS:
        cosmetic = "aura"
    return {"xp": nonnegative_int("xp"), "brain_coins": nonnegative_int("brain_coins"),
            "cosmetic": cosmetic, "completed_match_ids": list(dict.fromkeys(
                x for x in data.get("completed_match_ids", []) if isinstance(x, str)
            ))[:1000] if isinstance(data.get("completed_match_ids", []), list) else []}

def atomic_write_json(path: Path, data: dict[str, Any]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(data, stream, ensure_ascii=False, indent=2)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except OSError:
            pass
        raise
