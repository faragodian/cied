"""
Servicio de especificaciones de semanas para el sistema de quiz CIED.

Este módulo define la estructura WeekSpec que permite extender el sistema
a múltiples semanas manteniendo consistencia y reusabilidad.
"""

from typing import Dict, List, Any, Optional


class WeekSpec:
    """
    Especificación canónica para una semana del curso.

    Define la estructura completa necesaria para implementar un quiz semanal:
    - Metadata de la semana
    - Lista de ejercicios con sus templates
    - Configuración pedagógica
    """

    def __init__(
        self,
        week_id: str,
        title: str,
        subtitle: str,
        temas: List[str],
        tecnicas: List[str],
        descripcion: str,
        quiz_templates: List[Dict[str, Any]],
        error_tags: Optional[List[str]] = None
    ):
        self.week_id = week_id
        self.title = title
        self.subtitle = subtitle
        self.temas = temas
        self.tecnicas = tecnicas
        self.descripcion = descripcion
        self.quiz_templates = quiz_templates
        self.error_tags = error_tags or []


# Definición de especificaciones de semanas
# Las semanas se registran mediante llamadas explícitas a register_week_spec()
# para evitar imports circulares

WEEK_SPECS: Dict[str, WeekSpec] = {}


def register_week_spec(spec: WeekSpec) -> None:
    """
    Registra una especificación de semana en el sistema.

    Args:
        spec: Especificación de semana completa
    """
    WEEK_SPECS[spec.week_id] = spec


def register_week(week_id: str, spec: WeekSpec) -> None:
    """
    Registra una especificación de semana con ID explícito.

    Args:
        week_id: ID de la semana (debe coincidir con spec.week_id)
        spec: Especificación de semana
    """
    if spec.week_id != week_id:
        raise ValueError(f"WeekSpec week_id '{spec.week_id}' no coincide con parámetro '{week_id}'")
    register_week_spec(spec)


def get_week_spec(week_id: str) -> Optional[WeekSpec]:
    """
    Obtiene la especificación de una semana por su ID.

    Args:
        week_id: Identificador de la semana (ej: "week01")

    Returns:
        WeekSpec si existe, None si no se encuentra
    """
    return WEEK_SPECS.get(week_id)


def get_quiz_templates_for_week(week_id: str) -> List[Dict[str, Any]]:
    """
    Obtiene los templates de quiz para una semana específica.

    Args:
        week_id: Identificador de la semana

    Returns:
        Lista de templates de quiz, o lista vacía si la semana no existe
    """
    spec = get_week_spec(week_id)

    # Si es week01 y no está registrado, importar el módulo para registrarlo
    if not spec and week_id == "week01":
        try:
            # Importar quiz_week01 para que se registre automáticamente
            import app.services.quiz_week01  # noqa: F401
            spec = get_week_spec(week_id)
        except ImportError:
            pass  # Si falla el import, continuar

    if spec:
        return spec.quiz_templates
    return []


def get_available_weeks() -> List[str]:
    """
    Lista los IDs de semanas disponibles.

    Returns:
        Lista de week_ids disponibles
    """
    return list(WEEK_SPECS.keys())


def validate_week_spec(week_id: str) -> bool:
    """
    Valida que una especificación de semana tenga todos los campos requeridos.

    Args:
        week_id: ID de la semana a validar

    Returns:
        True si la especificación es válida, False en caso contrario
    """
    spec = get_week_spec(week_id)
    if not spec:
        return False

    # Validaciones básicas
    required_fields = ['week_id', 'title', 'quiz_templates']
    for field in required_fields:
        if not hasattr(spec, field) or not getattr(spec, field):
            return False

    # Validar que tenga al menos un template
    if not spec.quiz_templates or len(spec.quiz_templates) == 0:
        return False

    return True
