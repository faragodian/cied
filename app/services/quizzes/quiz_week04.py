"""
Quiz para Semana 4: Parcial 1 y Números Complejos
Sistema CIED - Cálculo Integral con Ecuaciones Diferenciales
"""

import random
from typing import List, Dict, Any, Optional

from ..weeks import WeekSpec, register_week


# Templates de quiz para Semana 4
QUIZ_TEMPLATES_WEEK04: List[Dict[str, Any]] = [
    # Template 1: Repaso de integración por partes
    {
        "question_latex": r"\int x e^{2x} \, dx",
        "correct_answer": r"\frac{1}{2} x e^{2x} - \frac{1}{4} e^{2x} + C",
        "solution_steps": [
            {
                "text": "Aplicar integración por partes: u = x, dv = e^{2x} dx",
                "math": r"u = x, \quad dv = e^{2x} \, dx"
            },
            {
                "text": "Calcular du y v",
                "math": r"du = dx, \quad v = \frac{1}{2} e^{2x}"
            },
            {
                "text": "Aplicar la fórmula: ∫ u dv = u v - ∫ v du",
                "math": r"= x \cdot \frac{1}{2} e^{2x} - \int \frac{1}{2} e^{2x} \, dx"
            },
            {
                "text": "Resolver la integral restante",
                "math": r"= \frac{1}{2} x e^{2x} - \frac{1}{2} \cdot \frac{1}{2} e^{2x} + C"
            },
            {
                "text": "Simplificar",
                "math": r"= \frac{1}{2} x e^{2x} - \frac{1}{4} e^{2x} + C"
            }
        ],
        "choices_latex": [
            r"\frac{1}{2} x e^{2x} - \frac{1}{4} e^{2x} + C",
            r"x e^{2x} - \frac{1}{2} e^{2x} + C",
            r"\frac{1}{2} e^{2x} + C",
            r"x^2 e^{2x} + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Error: olvidar la constante en v",
                        "math": r"v = e^{2x} \quad (\text{incorrecto, debería ser } \frac{1}{2} e^{2x})"
                    }
                ],
                "error_highlight": "Error: cálculo incorrecto de la integral de dv",
                "error_id": "integracion-partes-derivada-u"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Aplicar fórmula con signo incorrecto",
                        "math": r"\int u dv = uv + \int v du \quad (\text{incorrecto})"
                    }
                ],
                "error_highlight": "Error: fórmula incorrecta de integración por partes",
                "error_id": "integracion-partes-signo-formula"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Integrar directamente sin método",
                        "math": r"\int x e^{2x} dx = x^2 e^{2x} + C \quad (\text{incorrecto})"
                    }
                ],
                "error_highlight": "Error: no reconocer necesidad de integración por partes",
                "error_id": "integracion-partes-innecesaria"
            }
        ],
        "seed_id": "w4-1",
        "origin_label": "Se"
    },

    # Template 2: Números complejos - operaciones básicas
    {
        "question_latex": r"\text{Calcular } (3 + 2i) + (1 - 4i)",
        "correct_answer": r"4 - 2i",
        "solution_steps": [
            {
                "text": "Separar partes real e imaginaria",
                "math": r"(3 + 2i) + (1 - 4i) = (3 + 1) + (2i - 4i)"
            },
            {
                "text": "Sumar las partes reales",
                "math": r"3 + 1 = 4"
            },
            {
                "text": "Sumar las partes imaginarias",
                "math": r"2i + (-4i) = -2i"
            },
            {
                "text": "Resultado final",
                "math": r"4 + (-2i) = 4 - 2i"
            }
        ],
        "choices_latex": [
            r"4 - 2i",
            r"4 + 2i",
            r"2 - 4i",
            r"5 - 2i"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Error: sumar real con imaginario",
                        "math": r"3 + 2i + 1 - 4i = 4 + (-2i) \to 4 - 2i \quad (\text{correcto, pero confusión conceptual})"
                    }
                ],
                "error_highlight": "Error conceptual: no distinguir partes real e imaginaria",
                "error_id": "numeros-complejos-parte-real-imaginaria"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Error de signo en la parte imaginaria",
                        "math": r"2i + (-4i) = -2i \to +2i \quad (\text{incorrecto})"
                    }
                ],
                "error_highlight": "Error: signo incorrecto en parte imaginaria",
                "error_id": "numeros-complejos-operaciones"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Sumar todas las partes como números reales",
                        "math": r"3 + 2 + 1 - 4 = 2 \to 2 + 0i \quad (\text{incorrecto})"
                    }
                ],
                "error_highlight": "Error: tratar números complejos como reales",
                "error_id": "numeros-complejos-parte-real-imaginaria"
            }
        ],
        "seed_id": "w4-2",
        "origin_label": "Se"
    },

    # Template 3: Números complejos - multiplicación
    {
        "question_latex": r"\text{Calcular } (1 + 2i)(3 - i)",
        "correct_answer": r"3 + 6i - i - 2i^2 = 5 + 5i",
        "solution_steps": [
            {
                "text": "Aplicar propiedad distributiva",
                "math": r"(1 + 2i)(3 - i) = 1 \cdot 3 + 1 \cdot (-i) + 2i \cdot 3 + 2i \cdot (-i)"
            },
            {
                "text": "Multiplicar cada término",
                "math": r"= 3 - i + 6i - 2i^2"
            },
            {
                "text": "Recordar que i² = -1",
                "math": r"= 3 - i + 6i - 2(-1)"
            },
            {
                "text": "Simplificar términos",
                "math": r"= 3 + 2 + (-i + 6i)"
            },
            {
                "text": "Agrupar partes real e imaginaria",
                "math": r"= 5 + 5i"
            }
        ],
        "choices_latex": [
            r"5 + 5i",
            r"3 + 5i",
            r"5 + 3i",
            r"-1 + 5i"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Error: olvidar que i² = -1",
                        "math": r"-2i^2 = -2i^2 \to -2i^2 \quad (\text{no simplificado})"
                    }
                ],
                "error_highlight": "Error: no simplificar i² a -1",
                "error_id": "numeros-complejos-operaciones"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Error en distribución de términos",
                        "math": r"1 \cdot 3 + 2i \cdot (-i) = 3 - 2i^2 \to 3 + 2 \quad (\text{falta } 1 \cdot (-i) + 2i \cdot 3)"
                    }
                ],
                "error_highlight": "Error: distribución incompleta en multiplicación",
                "error_id": "numeros-complejos-operaciones"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Tratar como binomios sin considerar i",
                        "math": r"(1 + 2)(3 - 1) = 3 - 1 + 6 - 2 = 6 \to 6 + 0i \quad (\text{incorrecto})"
                    }
                ],
                "error_highlight": "Error: ignorar naturaleza compleja de i",
                "error_id": "numeros-complejos-parte-real-imaginaria"
            }
        ],
        "seed_id": "w4-3",
        "origin_label": "Se"
    }
]


def get_quiz_templates_for_week04() -> List[Dict[str, Any]]:
    """
    Retorna los templates de quiz para la Semana 4.

    Returns:
        Lista de templates de quiz
    """
    return QUIZ_TEMPLATES_WEEK04


def generate_dynamic_question(base_question_latex: str) -> Optional[Dict[str, Any]]:
    """
    Genera un ejercicio dinámico basado en configuración de week04 usando LLM.

    Args:
        base_question_latex: LaTeX del ejercicio base (ignorado, usa configuración de semana)

    Returns:
        Dict con la estructura completa del quiz instance generado dinámicamente
        None si no hay LLM disponible o la generación falla
    """
    from ..llm_generator import generate_quiz_instance

    # Usar la nueva función genérica para week04
    result = generate_quiz_instance('week04')

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
    Retorna una instancia aleatoria del quiz de Semana 4 con opciones mezcladas.

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
    quiz_templates = get_quiz_templates_for_week04()
    template = random.choice(quiz_templates).copy()

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
        "week_id": "week04",
        "is_dynamic": False
    }

    return instance


def choose_exercise_origin() -> str:
    """
    Decide pedagógicamente si usar un ejercicio seed o generado por LLM para week04.

    Returns:
        "seed": usar ejercicio basado en plantillas predefinidas
        "llm": generar ejercicio dinámicamente usando LLM
    """
    # Usar la configuración global de ratios
    from ..quizzes.quiz_week01 import SEED_RATIO
    return "seed" if random.random() < SEED_RATIO else "llm"


# Registrar la especificación de la semana
week04_spec = WeekSpec(
    week_id="week04",
    title="Parcial 1 y números complejos",
    subtitle="Repaso y fundamentos complejos",
    temas=[
        "Repaso integral completo",
        "Números complejos",
        "Operaciones complejas",
        "Interpretación geométrica"
    ],
    tecnicas=[
        "Todas las técnicas de integración",
        "Operaciones con números complejos",
        "Representación en plano complejo",
        "Forma algebraica vs geométrica"
    ],
    descripcion="Consolidación de conocimientos y preparación para temas avanzados",
    quiz_templates=QUIZ_TEMPLATES_WEEK04,
    error_tags=["repaso-integral", "numeros-complejos"]
)

register_week("week04", week04_spec)