"""Stub LLM generator minimal API.

Proporciona `is_any_llm_configured()` requerido por módulos de week.
En este entorno devolvemos False para forzar uso de seeds cuando no haya
configuración real de LLMs.
"""
import os
from typing import Any, Dict, Optional


def is_any_llm_configured() -> bool:
    """Indica si hay alguna LLM configurada por variables de entorno.

    Esta implementación mínima consulta las variables estándar y retorna
    True si detecta alguna clave; en caso contrario False.
    """
    return bool(os.environ.get("OPENAI_API_KEY") or os.environ.get("GEMINI_API_KEY") or os.environ.get("OPENROUTER_API_KEY") or os.environ.get("DEEPSEEK_API_KEY"))


def generate_quiz_instance(week_id: str) -> Optional[Dict[str, Any]]:
    """Placeholder: no genera nada en este stub."""
    return None


def generate_exercise(week_id: str) -> Optional[Dict[str, Any]]:
    return None
