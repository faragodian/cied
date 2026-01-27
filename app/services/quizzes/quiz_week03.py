"""
Quiz para Semana 3: Fracciones Parciales e Integrales Impropias
Sistema CIED - Cálculo Integral con Ecuaciones Diferenciales
"""

import random
from typing import List, Dict, Any, Optional

from ..weeks import WeekSpec, register_week


# Templates de quiz para Semana 3
QUIZ_TEMPLATES_WEEK03: List[Dict[str, Any]] = [
    # Template 1: Fracciones parciales con factores cuadráticos
    {
        "question_latex": r"\int \frac{x^2 + 1}{(x^2 + 2x + 2)^2} \, dx",
        "correct_answer": r"\frac{1}{2} \arctan(x + 1) + \frac{1}{2} \cdot \frac{x + 1}{(x^2 + 2x + 2)^2} + C",
        "solution_steps": [
            {
                "text": "Observar que el numerador es casi igual al denominador",
                "math": r"\frac{x^2 + 1}{(x^2 + 2x + 2)^2} = \frac{(x^2 + 2x + 2) - 2x - 1}{(x^2 + 2x + 2)^2}"
            },
            {
                "text": "Descomponer en fracciones parciales",
                "math": r"= \frac{1}{x^2 + 2x + 2} - \frac{2x + 1}{(x^2 + 2x + 2)^2}"
            },
            {
                "text": "Completar el cuadrado en el primer término",
                "math": r"\frac{1}{x^2 + 2x + 2} = \frac{1}{(x+1)^2 + 1}"
            },
            {
                "text": "Integrar cada término",
                "math": r"\int \frac{1}{(x+1)^2 + 1} dx - \int \frac{2x + 1}{(x^2 + 2x + 2)^2} dx"
            },
            {
                "text": "Resultado de la integración",
                "math": r"= \arctan(x + 1) - \frac{1}{2} \cdot \frac{x + 1}{(x^2 + 2x + 2)} + C"
            }
        ],
        "choices_latex": [
            r"\frac{1}{2} \arctan(x + 1) + \frac{1}{2} \cdot \frac{x + 1}{(x^2 + 2x + 2)^2} + C",
            r"\arctan(x + 1) - \frac{x + 1}{x^2 + 2x + 2} + C",
            r"\ln|x^2 + 2x + 2| - \frac{1}{x^2 + 2x + 2} + C",
            r"\frac{x^3}{3} + x + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Error: no reconocer el patrón de descomposición",
                        "math": r"\frac{x^2 + 1}{(x^2 + 2x + 2)^2} = \frac{Ax + B}{x^2 + 2x + 2} + \frac{Cx + D}{(x^2 + 2x + 2)^2}"
                    }
                ],
                "error_highlight": "Error: descomposición incorrecta para caso especial",
                "error_id": "fracciones-parciales-descomposicion-lineal"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Error: olvidar completar el cuadrado",
                        "math": r"\frac{1}{x^2 + 2x + 2} \neq \arctan(x + 1)"
                    }
                ],
                "error_highlight": "Error: integración incorrecta de forma cuadrática",
                "error_id": "fracciones-parciales-sin-simplificar"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Integrar directamente sin descomponer",
                        "math": r"\int \frac{x^2 + 1}{(x^2 + 2x + 2)^2} dx = \frac{x^3}{3} + x + C"
                    }
                ],
                "error_highlight": "Error: no aplicar método de fracciones parciales",
                "error_id": "fracciones-parciales-sin-simplificar"
            }
        ],
        "seed_id": "w3-1",
        "origin_label": "Se"
    },

    # Template 2: Integrales impropias - intervalo infinito
    {
        "question_latex": r"\int_{1}^{\infty} \frac{1}{x^2} \, dx",
        "correct_answer": r"1",
        "solution_steps": [
            {
                "text": "Identificar como integral impropia de tipo I (límite superior infinito)",
                "math": r"\lim_{b \to \infty} \int_{1}^{b} \frac{1}{x^2} \, dx"
            },
            {
                "text": "Calcular la integral indefinida",
                "math": r"\int \frac{1}{x^2} dx = -\frac{1}{x} + C"
            },
            {
                "text": "Evaluar el límite",
                "math": r"\lim_{b \to \infty} \left[ -\frac{1}{x} \right]_{1}^{b} = \lim_{b \to \infty} \left( -\frac{1}{b} - \left( -\frac{1}{1} \right) \right)"
            },
            {
                "text": "Calcular el límite",
                "math": r"= \lim_{b \to \infty} \left( -\frac{1}{b} + 1 \right) = 0 + 1 = 1"
            },
            {
                "text": "Conclusión: la integral converge",
                "math": r"\int_{1}^{\infty} \frac{1}{x^2} \, dx = 1"
            }
        ],
        "choices_latex": [
            r"1",
            r"\infty",
            r"0",
            r"-\frac{1}{x} \bigg|_{1}^{\infty}"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Error: evaluar sin límite",
                        "math": r"\int_{1}^{\infty} \frac{1}{x^2} dx = \left[ -\frac{1}{x} \right]_{1}^{\infty} = \infty"
                    }
                ],
                "error_highlight": "Error: no aplicar concepto de límite en integrales impropias",
                "error_id": "integrales-impropias-ignora-impropiedad"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Evaluar incorrectamente el límite",
                        "math": r"\lim_{b \to \infty} \left( -\frac{1}{b} \right) = -\infty"
                    }
                ],
                "error_highlight": "Error: cálculo incorrecto del límite",
                "error_id": "integrales-impropias-planteo-limite-incorrecto"
            },
            {
                "wrong_steps": [
                    {
                        "text": "No evaluar los límites",
                        "math": r"\int \frac{1}{x^2} dx = -\frac{1}{x} + C"
                    }
                ],
                "error_highlight": "Error: olvidar evaluar los límites de integración",
                "error_id": "integral-definida-sin-evaluar-limites"
            }
        ],
        "seed_id": "w3-2",
        "origin_label": "Se"
    },

    # Template 3: Integrales impropias - discontinuidad
    {
        "question_latex": r"\int_{0}^{1} \frac{1}{\sqrt{x}} \, dx",
        "correct_answer": r"2",
        "solution_steps": [
            {
                "text": "Identificar discontinuidad en x = 0 (punto extremo del intervalo)",
                "math": r"f(x) = \frac{1}{\sqrt{x}} \to \infty \text{ cuando } x \to 0^+"
            },
            {
                "text": "Convertir a integral impropia de tipo II",
                "math": r"\lim_{a \to 0^+} \int_{a}^{1} \frac{1}{\sqrt{x}} \, dx"
            },
            {
                "text": "Calcular la integral indefinida",
                "math": r"\int \frac{1}{\sqrt{x}} dx = 2\sqrt{x} + C"
            },
            {
                "text": "Evaluar el límite",
                "math": r"\lim_{a \to 0^+} \left[ 2\sqrt{x} \right]_{a}^{1} = \lim_{a \to 0^+} \left( 2\sqrt{1} - 2\sqrt{a} \right)"
            },
            {
                "text": "Calcular el límite",
                "math": r"= \lim_{a \to 0^+} \left( 2 - 2\sqrt{a} \right) = 2 - 0 = 2"
            }
        ],
        "choices_latex": [
            r"2",
            r"\infty",
            r"0",
            r"2\sqrt{x} \bigg|_{0}^{1}"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Error: integrar sin considerar la discontinuidad",
                        "math": r"\int_{0}^{1} \frac{1}{\sqrt{x}} dx = \left[ 2\sqrt{x} \right]_{0}^{1} = 2 - 0 = 2"
                    }
                ],
                "error_highlight": "Error: no reconocer que es integral impropia",
                "error_id": "integrales-impropias-ignora-impropiedad"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Evaluar directamente sin límite",
                        "math": r"\left[ 2\sqrt{x} \right]_{0}^{1} = 2\sqrt{1} - 2\sqrt{0} = \infty"
                    }
                ],
                "error_highlight": "Error: evaluación incorrecta en punto de discontinuidad",
                "error_id": "integrales-impropias-planteo-limite-incorrecto"
            },
            {
                "wrong_steps": [
                    {
                        "text": "No evaluar límites",
                        "math": r"\int \frac{1}{\sqrt{x}} dx = 2\sqrt{x} + C"
                    }
                ],
                "error_highlight": "Error: olvidar aplicar concepto de límite",
                "error_id": "integral-definida-sin-evaluar-limites"
            }
        ],
        "seed_id": "w3-3",
        "origin_label": "Se"
    }
]


def get_quiz_templates_for_week03() -> List[Dict[str, Any]]:
    """
    Retorna los templates de quiz para la Semana 3.

    Returns:
        Lista de templates de quiz
    """
    return QUIZ_TEMPLATES_WEEK03


def generate_dynamic_question(base_question_latex: str) -> Optional[Dict[str, Any]]:
    """
    Genera un ejercicio dinámico basado en configuración de week03 usando LLM.

    Args:
        base_question_latex: LaTeX del ejercicio base (ignorado, usa configuración de semana)

    Returns:
        Dict con la estructura completa del quiz instance generado dinámicamente
        None si no hay LLM disponible o la generación falla
    """
    from ..llm_generator import generate_quiz_instance

    # Usar la nueva función genérica para week03
    result = generate_quiz_instance('week03')

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
    Retorna una instancia aleatoria del quiz de Semana 3 con opciones mezcladas.

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
    quiz_templates = get_quiz_templates_for_week03()
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
        "week_id": "week03",
        "is_dynamic": False
    }

    return instance


def choose_exercise_origin() -> str:
    """
    Decide pedagógicamente si usar un ejercicio seed o generado por LLM para week03.

    Returns:
        "seed": usar ejercicio basado en plantillas predefinidas
        "llm": generar ejercicio dinámicamente usando LLM
    """
    # Usar la configuración global de ratios
    from ..quizzes.quiz_week01 import SEED_RATIO
    return "seed" if random.random() < SEED_RATIO else "llm"


# Registrar la especificación de la semana
week03_spec = WeekSpec(
    week_id="week03",
    title="Fracciones parciales e integrales impropias",
    subtitle="Técnicas avanzadas de integración",
    temas=[
        "Fracciones parciales avanzadas",
        "Factores cuadráticos",
        "Integrales impropias",
        "Convergencia de integrales"
    ],
    tecnicas=[
        "Descomposición con factores repetidos",
        "Integrales impropias tipo I y II",
        "Análisis de convergencia",
        "Evaluación mediante límites"
    ],
    descripcion="Técnicas finales de integración y análisis de convergencia",
    quiz_templates=QUIZ_TEMPLATES_WEEK03,
    error_tags=["fracciones-parciales", "integrales-impropias"]
)

register_week("week03", week03_spec)