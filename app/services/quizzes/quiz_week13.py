"""
Quiz para Semana 13: [Pendiente de definición]
Sistema CIED - Cálculo Integral con Ecuaciones Diferenciales
"""

import random
from typing import List, Dict, Any, Optional

from ..weeks import WeekSpec, register_week


# Templates de quiz para Semana 13 - ESTRUCTURA BÁSICA
QUIZ_TEMPLATES_WEEK13: List[Dict[str, Any]] = [
    # Template básico - reemplazar con contenido real
    {
        "question_latex": r"\int x \, dx",
        "correct_answer": r"\frac{x^2}{2} + C",
        "solution_steps": [
            {
                "text": "Pendiente de implementación específica para semana 13",
                "math": r"\text{Contenido por definir}"
            }
        ],
        "choices_latex": [
            r"\frac{x^2}{2} + C",
            r"x^2 + C",
            r"\frac{x^3}{3} + C",
            r"x + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Error genérico pendiente de definición",
                        "math": r"\text{Error por implementar}"
                    }
                ],
                "error_highlight": "Error pendiente de definición",
                "error_id": "error-pendiente-semana13"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Segundo error pendiente",
                        "math": r"\text{Implementar}"
                    }
                ],
                "error_highlight": "Segundo error pendiente",
                "error_id": "error-pendiente-semana13-2"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Tercer error pendiente",
                        "math": r"\text{Implementar}"
                    }
                ],
                "error_highlight": "Tercer error pendiente",
                "error_id": "error-pendiente-semana13-3"
            }
        ],
        "seed_id": "w13-1",
        "origin_label": "Se"
    }
]


def get_quiz_templates_for_week13() -> List[Dict[str, Any]]:
    """
    Retorna los templates de quiz para la Semana 13.
    
    Returns:
        Lista de templates de quiz
    """
    return QUIZ_TEMPLATES_WEEK13


def generate_dynamic_question(base_question_latex: str) -> Optional[Dict[str, Any]]:
    """
    Genera un ejercicio dinámico basado en configuración de week13 usando LLM.

    Args:
        base_question_latex: LaTeX del ejercicio base (ignorado, usa configuración de semana)

    Returns:
        Dict con la estructura completa del quiz instance generado dinámicamente
        None si no hay LLM disponible o la generación falla
    """
    from ..llm_generator import generate_quiz_instance

    # Usar la nueva función genérica para week13
    result = generate_quiz_instance('week13')

    if result:
        # Añadir campos legacy para compatibilidad
        result["is_dynamic"] = True
        result["source"] = result.get("generated_by", "llm")
        result["origin_label"] = "LLM"

        # Mezclar opciones si existen
        if "options" in result:
            random.shuffle(result["options"])

    return result


def get_random_question(use_dynamic: bool = False, base_question: str = None) -> Dict[str, Any]:
    """
    Retorna una instancia aleatoria del quiz de Semana 13 con opciones mezcladas.

    Args:
        use_dynamic: Si True, genera un ejercicio dinámico usando LLM
        base_question: Enunciado base para generar ejercicio dinámico (requerido si use_dynamic=True)

    Returns:
        Dict con la estructura completa del quiz instance
    """
    if use_dynamic and base_question:
        return generate_dynamic_question(base_question)

    # Switch pedagógico: decidir origen del ejercicio
    origin = choose_exercise_origin()

    # Si el switch elige "llm", intentar generar dinámicamente
    if origin == "llm":
        dynamic_question = generate_dynamic_question("")
        if dynamic_question:
            return dynamic_question

    # Fallback a seed si LLM falla o no está disponible
    quiz_templates = get_quiz_templates_for_week13()
    template = quiz_templates[0].copy()  # Solo hay 1 template por ahora

    # Construir opciones con identificadores únicos
    options = []

    # Opción correcta
    correct_option = {
        "option_id": "A",
        "latex": template["choices_latex"][template["correct_index"]],
        "is_correct": True,
        "solution_steps": template.get("solution_steps", []),
        "final_answer": template.get("correct_answer", "")
    }
    options.append(correct_option)

    # Opciones incorrectas
    for i, (choice_latex, wrong_option) in enumerate(zip(
        [c for j, c in enumerate(template["choices_latex"]) if j != template["correct_index"]],
        template.get("wrong_options", [])
    )):
        incorrect_option = {
            "option_id": chr(66 + i),  # B, C, D
            "latex": choice_latex,
            "is_correct": False,
            "error_id": wrong_option.get("error_id", ""),
            "wrong_steps": wrong_option.get("wrong_steps", []),
            "error_highlight": wrong_option.get("error_highlight", "")
        }
        options.append(incorrect_option)

    # Mezclar opciones
    random.shuffle(options)

    # Construir instancia final
    instance = {
        "question_latex": template["question_latex"],
        "correct_answer": template["correct_answer"],
        "solution_steps": template["solution_steps"],
        "options": options,
        "seed_id": template.get("seed_id"),
        "origin_label": template.get("origin_label", "Se"),
        "week_id": "week13",
        "is_dynamic": False
    }

    return instance


def choose_exercise_origin() -> str:
    """
    Decide pedagógicamente si usar un ejercicio seed o generado por LLM para week13.

    Returns:
        "seed": usar ejercicio basado en plantillas predefinidas
        "llm": generar ejercicio dinámicamente usando LLM
    """
    # Usar la configuración global de ratios
    from ..quizzes.quiz_week01 import SEED_RATIO
    return "seed" if random.random() < SEED_RATIO else "llm"


# Registrar la especificación de la semana
week13_spec = WeekSpec(
    week_id="week13",
    title="Semana 13 - Pendiente de definición",
    subtitle="Contenido por definir",
    temas=["Pendiente"],
    tecnicas=["Pendiente"],
    descripcion="Contenido pendiente de implementación para semana 13",
    quiz_templates=QUIZ_TEMPLATES_WEEK13,
    error_tags=[]
)

register_week("week13", week13_spec)
