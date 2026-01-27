"""
Configuración centralizada para todas las semanas del sistema CIED.

Este módulo define la configuración canónica para las 16 semanas del curso,
basado en el syllabus oficial y los objetivos pedagógicos.
"""

from typing import Dict, List, Any

# Pedagogical switch: ratio of seed exercises vs. LLM-generated exercises
SEED_RATIO = 0.8  # 80% ejercicios basados en semillas (más estable)
LLM_RATIO = 0.2   # 20% ejercicios generados por LLM (menos errores)
assert SEED_RATIO + LLM_RATIO == 1.0, f"SEED_RATIO ({SEED_RATIO}) + LLM_RATIO ({LLM_RATIO}) must equal 1.0"

# Configuración de semanas existentes (con syllabus)
WEEK_CONFIGS: Dict[str, Dict[str, Any]] = {
    "week01": {
        "week_id": "week01",
        "title": "Integración por partes e integrales trigonométricas",
        "subtitle": "Técnicas básicas de integración",
        "curso": "Cálculo Integral",
        "tema_principal": "Técnicas de Integración",
        "temas": [
            "Integración por partes",
            "Integrales trigonométricas",
            "Identidades trigonométricas"
        ],
        "tecnicas": [
            "Regla de integración por partes",
            "Identidades trigonométricas básicas"
        ],
        "descripcion": "Introducción a técnicas avanzadas de integración",
        "allowed_error_ids": [],
        "ejemplos_entrada": [],
        "nivel": "universitario",
        "error_tags": ["integracion-partes", "integrales-trig"],
        "status": "implementado"
    },

    "week02": {
        "week_id": "week02",
        "title": "Sustitución Trigonométrica y Fracciones Parciales",
        "subtitle": "Técnicas de Integración Avanzadas",
        "curso": "Cálculo Integral",
        "tema_principal": "Técnicas de Integración Avanzadas",
        "temas": [
            "7.3: Sustitución trigonométrica",
            "7.4: Fracciones parciales",
            "Casos de sustitución trigonométrica",
            "Descomposición en fracciones parciales"
        ],
        "tecnicas": [
            "Identificación de patrones: √(a²-x²), √(x²+a²), √(x²-a²)",
            "Sustitución adecuada: x = a sinθ, x = a tanθ, x = a secθ",
            "Descomposición en fracciones parciales: casos lineal, cuadrático, repetido",
            "Resolución de sistemas de ecuaciones para coeficientes"
        ],
        "descripcion": "Segunda semana: técnicas avanzadas de integración. Sustitución trigonométrica para integrales con raíces cuadradas y fracciones parciales para funciones racionales.",
        "allowed_error_ids": [
            "sustitucion-trigonometrica-caso-incorrecto",
            "sustitucion-trigonometrica-no-retorno",
            "sustitucion-trigonometrica-eleccion-caso",
            "sustitucion-trig-identidad-mal",
            "sustitucion-trig-limites-olvidados",
            "fracciones-parciales-descomposicion-lineal",
            "fracciones-parciales-sin-simplificar",
            "fracciones-parciales-coeficientes-mal",
            "fracciones-parciales-integracion-error",
            "fracciones-parciales-denominador-incompleto"
        ],
        "ejemplos_entrada": [
            "\\int \\frac{x^3}{\\sqrt{x^2 + 9}} \\, dx",
            "\\int \\frac{dx}{\\sqrt{x^2 + 4}^2}",
            "\\int \\frac{x+1}{x^2 + 2x} \\, dx",
            "\\int \\frac{3x-2}{x^3 + 3x^2 + 2x} \\, dx"
        ],
        "nivel": "universitario",
        "error_tags": [
            "sustitucion-trigonometrica",
            "fracciones-parciales",
            "integracion-avanzada"
        ],
        "status": "completa"
    },

    "week03": {
        "week_id": "week03",
        "title": "Fracciones parciales e integrales impropias",
        "subtitle": "Completando técnicas de integración",
        "curso": "Cálculo Integral",
        "tema_principal": "Técnicas de Integración Finales",
        "temas": [
            "Fracciones parciales avanzadas",
            "Integrales impropias",
            "Convergencia de integrales"
        ],
        "tecnicas": [
            "Factores cuadráticos",
            "Integrales impropias tipo I y II",
            "Criterios de convergencia"
        ],
        "descripcion": "Técnicas finales de integración",
        "allowed_error_ids": [],
        "ejemplos_entrada": [],
        "nivel": "universitario",
        "error_tags": ["fracciones-parciales", "integrales-impropias"],
        "status": "planificado"
    },

    "week04": {
        "week_id": "week04",
        "title": "Parcial 1 y números complejos",
        "subtitle": "Repaso y fundamentos complejos",
        "curso": "Cálculo Integral",
        "tema_principal": "Consolidación y Transición",
        "temas": [
            "Repaso integral",
            "Números complejos",
            "Funciones complejas"
        ],
        "tecnicas": [
            "Todas las técnicas de integración",
            "Operaciones con números complejos",
            "Representación gráfica"
        ],
        "descripcion": "Consolidación de conocimientos y preparación para temas avanzados",
        "allowed_error_ids": [],
        "ejemplos_entrada": [],
        "nivel": "universitario",
        "error_tags": ["repaso-integral", "numeros-complejos"],
        "status": "planificado"
    }
}


def get_week_config(week_id: str) -> Dict[str, Any]:
    """
    Obtiene la configuración de una semana específica.

    Args:
        week_id: Identificador de la semana (ej: "week01")

    Returns:
        Dict con la configuración de la semana

    Raises:
        KeyError: Si la semana no existe
    """
    if week_id not in WEEK_CONFIGS:
        raise KeyError(f"Configuración para {week_id} no encontrada")
    return WEEK_CONFIGS[week_id]


def get_available_weeks() -> List[str]:
    """
    Lista todas las semanas configuradas.

    Returns:
        Lista de week_ids disponibles
    """
    return list(WEEK_CONFIGS.keys())


def get_weeks_by_status(status: str) -> List[str]:
    """
    Obtiene semanas por estado de implementación.

    Args:
        status: Estado deseado ("implementado", "estructurado", "planificado", "completa", "pendiente")

    Returns:
        Lista de week_ids con ese estado
    """
    return [week_id for week_id, config in WEEK_CONFIGS.items()
            if config.get("status") == status]


def validate_week_config(week_id: str) -> bool:
    """
    Valida que una configuración de semana tenga todos los campos requeridos.

    Args:
        week_id: ID de la semana a validar

    Returns:
        True si es válida, False en caso contrario
    """
    try:
        config = get_week_config(week_id)
        required_fields = ["week_id", "title", "subtitle", "curso", "tema_principal", 
                          "temas", "tecnicas", "descripcion", "allowed_error_ids", 
                          "ejemplos_entrada", "nivel", "error_tags", "status"]
        return all(field in config for field in required_fields)
    except KeyError:
        return False


# Configuraciones adicionales para semanas futuras (placeholders)
def create_week_placeholder(week_num: int) -> Dict[str, Any]:
    """Crea configuración placeholder para semanas futuras."""
    return {
        "week_id": f"week{week_num}",
        "title": f"Semana {week_num}",
        "subtitle": "Pendiente de definición",
        "curso": "Cálculo Integral",
        "tema_principal": "Pendiente",
        "temas": ["Pendiente"],
        "tecnicas": ["Pendiente"],
        "descripcion": f"Contenido pendiente para Semana {week_num}",
        "allowed_error_ids": [],
        "ejemplos_entrada": [],
        "nivel": "universitario",
        "error_tags": [],
        "status": "pendiente"
    }


# Extender configuraciones para semanas 5-16 (placeholders)
for week_num in range(5, 17):
    week_id = f"week{week_num:02d}"
    WEEK_CONFIGS[week_id] = create_week_placeholder(week_num)
