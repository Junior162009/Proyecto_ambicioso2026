"""Compatibilidad para el jefe final y el nombre antiguo Enemy."""
from boss import Boss
from enemigo import Enemy

class Jefe(Boss):
    """Nombre en español para el jefe final."""
    pass

__all__ = ["Jefe", "Boss", "Enemy"]
