"""Servicio mínimo Weeks: define WeekSpec y registro de semanas.

Proporciona las funciones necesarias para que los módulos quiz_weekNN
puedan registrar sus WeekSpec sin importar el orden de importación.
"""
from typing import Dict, Any, List, Optional


class WeekSpec:
    def __init__(self, week_id: str, title: str, subtitle: str, temas: List[str], tecnicas: List[str], descripcion: str, quiz_templates: List[Dict[str, Any]], error_tags: Optional[List[str]] = None):
        self.week_id = week_id
        self.title = title
        self.subtitle = subtitle
        self.temas = temas
        self.tecnicas = tecnicas
        self.descripcion = descripcion
        self.quiz_templates = quiz_templates
        self.error_tags = error_tags or []


WEEK_SPECS: Dict[str, WeekSpec] = {}


def register_week(week_id: str, spec: WeekSpec) -> None:
    if spec.week_id != week_id:
        raise ValueError("week_id mismatch")
    WEEK_SPECS[week_id] = spec


def get_week_spec(week_id: str) -> Optional[WeekSpec]:
    return WEEK_SPECS.get(week_id)


def get_quiz_templates_for_week(week_id: str) -> List[Dict[str, Any]]:
    spec = get_week_spec(week_id)
    if spec and getattr(spec, 'quiz_templates', None):
        return spec.quiz_templates
    return []
