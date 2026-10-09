"""Compatibilidad con los módulos antiguos que importan `config`.

La configuración oficial vive en settings.py. Este archivo evita errores
ModuleNotFoundError sin duplicar los valores de configuración.
"""
from settings import *  # noqa: F401,F403
