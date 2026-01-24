"""
Servicio para el quiz de la Semana 1: Integración por partes
Contiene plantillas de preguntas con opciones correctas e incorrectas
"""

import random
from pathlib import Path
from typing import Dict, List, Any, Optional
from .weeks import get_quiz_templates_for_week, WeekSpec, register_week
from .llm_generator import generate_week01_exercise


# Configuración pedagógica del switch para mezclar ejercicios seed y LLM
SEED_RATIO = 0.5  # Proporción de ejercicios basados en semillas (0.0 - 1.0)
LLM_RATIO = 0.5   # Proporción de ejercicios generados dinámicamente (0.0 - 1.0)

# Validación: las proporciones deben sumar 1.0
assert SEED_RATIO + LLM_RATIO == 1.0, f"SEED_RATIO ({SEED_RATIO}) + LLM_RATIO ({LLM_RATIO}) must equal 1.0"


# Plantillas de preguntas para el quiz de Semana 1
QUIZ_TEMPLATES = [
    {
        "question_latex": r"\int x e^{x} \, dx",
        "correct_answer": r"e^{x}(x - 1) + C",
        "solution_steps": [
            {
                "text": "Aplicamos integración por partes con la fórmula:",
                "math": r"\int u \, dv = uv - \int v \, du"
            },
            {
                "text": "Elegimos las funciones:",
                "math": r"u = x, \quad dv = e^{x} \, dx"
            },
            {
                "text": "Calculamos las derivadas:",
                "math": r"du = dx, \quad v = e^{x}"
            },
            {
                "text": "Aplicamos la fórmula:",
                "math": r"\int x e^{x} \, dx = x e^{x} - \int e^{x} \, dx"
            },
            {
                "text": "Resolvemos la integral restante:",
                "math": r"\int e^{x} \, dx = e^{x} + C"
            },
            {
                "text": "Sustituimos:",
                "math": r"x e^{x} - (e^{x} + C) = x e^{x} - e^{x} + C"
            },
            {
                "text": "Factorizamos el resultado final:",
                "math": r"e^{x}(x - 1) + C"
            }
        ],
        "choices_latex": [
            r"e^{x}(x - 1) + C",  # Correcta
            r"x e^{x} + C",       # Error: elección incorrecta de u y dv
            r"e^{x}(x + 1) + C",  # Error: signo incorrecto
            r"x e^{x} - e^{x} + C", # Error: derivada incorrecta
            r"\frac{1}{2} x^{2} e^{x} + C", # Error: antiderivada inventada
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Elección incorrecta (regla LIATE):",
                        "math": r"u = e^{x}, \quad dv = x \, dx"
                    },
                    {
                        "text": "Derivadas calculadas:",
                        "math": r"du = e^{x} \, dx, \quad v = \frac{1}{2} x^{2}"
                    },
                    {
                        "text": "Aplicamos la fórmula:",
                        "math": r"e^{x} \cdot \frac{1}{2} x^{2} - \int \frac{1}{2} x^{2} e^{x} \, dx"
                    },
                    {
                        "text": "¡La integral resultante es más complicada!",
                        "math": r"\int x^{2} e^{x} \, dx"
                    }
                ],
                "error_highlight": "Error: mala elección de u y dv (se elige dv como la función más difícil)",
                "error_id": "integracion-partes-eleccion-uv"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Elegimos las funciones correctamente:",
                        "math": r"u = x, \quad dv = e^{x} \, dx"
                    },
                    {
                        "text": "Calculamos las derivadas:",
                        "math": r"du = dx, \quad v = e^{x}"
                    },
                    {
                        "text": "Fórmula incorrecta (signo equivocado):",
                        "math": r"\int u \, dv = uv + \int v \, du"
                    },
                    {
                        "text": "Aplicamos la fórmula errónea:",
                        "math": r"x e^{x} + \int e^{x} \, dx = x e^{x} + e^{x} + C"
                    },
                    {
                        "text": "Resultado incorrecto:",
                        "math": r"e^{x}(x + 1) + C"
                    }
                ],
                "error_highlight": "Error: signo incorrecto en la fórmula (es - ∫v du, no + ∫v du)",
                "error_id": "integracion-partes-signo-formula"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Elegimos las funciones:",
                        "math": r"u = x, \quad dv = e^{x} \, dx"
                    },
                    {
                        "text": "Calculamos las derivadas:",
                        "math": r"du = dx, \quad v = e^{x}"
                    },
                    {
                        "text": "Aplicamos la fórmula:",
                        "math": r"x e^{x} - \int e^{x} \, dx"
                    },
                    {
                        "text": "Error: confusión en el cálculo de la derivada de u",
                        "math": r"\text{(olvida que } du = dx\text{, no } 2x \, dx\text{)}"
                    },
                    {
                        "text": "Resolvemos incorrectamente:",
                        "math": r"x e^{x} - e^{x} + C"
                    }
                ],
                "error_highlight": "Error: cálculo incorrecto de la derivada de u en el proceso",
                "error_id": "integracion-partes-derivada-u"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Antiderivada 'inventada' sin justificación matemática:",
                        "math": r"\int x e^{x} \, dx = \frac{1}{2} x^{2} e^{x} + C"
                    },
                    {
                        "text": "Verificación por derivación:",
                        "math": r"\frac{d}{dx}\left[\frac{1}{2} x^{2} e^{x}\right] = x e^{x} + \frac{1}{2} x^{2} e^{x}"
                    },
                    {
                        "text": "Resultado incorrecto:",
                        "math": r"e^{x}\left(x + \frac{1}{2} x^{2}\right) \neq x e^{x}"
                    }
                ],
                "error_highlight": "Error: antiderivada inventada sin verificación matemática",
                "error_id": "integracion-partes-antiderivada-inventada"
            }
        ],
        "source": "seed",
        "seed_id": "w1-1",
        "origin_label": "Se"
    },
    # ... (el resto de los templates permanecen igual, los omito por brevedad)
]


def _shuffle_llm_question_options(question: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mezcla las opciones de un ejercicio generado por LLM manteniendo
    el seguimiento de cuál es la correcta.

    Args:
        question: Ejercicio generado por LLM

    Returns:
        Ejercicio con opciones mezcladas
    """
    import copy
    question = copy.deepcopy(question)
    
    # Mezclar las opciones
    options = question.get("options", [])
    if options:
        random.shuffle(options)
        question["options"] = options
    
    return question


def generate_dynamic_question(base_question_latex: str) -> Optional[Dict[str, Any]]:
    """
    Genera un ejercicio dinámico basado en un ejercicio semilla usando LLM.

    Args:
        base_question_latex: LaTeX del ejercicio base

    Returns:
        Dict con la estructura completa del quiz instance generado dinámicamente
        None si no hay LLM disponible o la generación falla
    """
    # IMPORTANTE: Para mantener coherencia (enunciado ↔ respuesta ↔ distractores ↔ error_id),
    # el LLM debe generar el ítem COMPLETO, no solo el enunciado.
    from .llm_generator import generate_week01_quiz_instance

    quiz_obj = generate_week01_quiz_instance()
    if quiz_obj is None:
        return None

    # Marcas auxiliares (no rompen el template)
    quiz_obj["week_id"] = "week01"
    quiz_obj["is_dynamic"] = True
    quiz_obj["source"] = "llm"
    
    # ¡MEZCLAR LAS OPCIONES!
    return _shuffle_llm_question_options(quiz_obj)


def is_llm_available() -> bool:
    """
    Verifica si la generación LLM está disponible (API keys configuradas).

    Returns:
        True si se puede generar ejercicios dinámicos, False si debe usar seeds
    """
    try:
        # Verificar configuración local sin llamadas a red
        from .llm_generator import is_any_llm_configured
        return bool(is_any_llm_configured())

    except Exception:
        return False


def choose_exercise_origin() -> str:
    """
    Decide pedagógicamente si usar un ejercicio seed o generado por LLM.
    Respeta reglas pedagógicas: fuerza 'seed' si LLM no está disponible.

    Returns:
        "seed": usar ejercicio basado en plantillas predefinidas
        "llm": generar ejercicio dinámicamente usando LLM
    """
    # Regla pedagógica: si no hay LLM disponible, usar seeds
    if not is_llm_available():
        return "seed"

    # Switch pedagógico basado en ratios configurados
    return "seed" if random.random() < SEED_RATIO else "llm"


def get_another_question(current_question_latex: str) -> Dict[str, Any]:
    """
    Genera otro ejercicio dinámico basado en el ejercicio actual.
    Si no hay LLM disponible, genera un ejercicio seed.

    Args:
        current_question_latex: LaTeX del ejercicio actual

    Returns:
        Dict con nuevo ejercicio generado dinámicamente o seed
    """
    # Intentar generar ejercicio dinámico
    dynamic_question = generate_dynamic_question(current_question_latex)

    # Si la generación LLM falló, fallback a seed
    if dynamic_question is None:
        # Generar ejercicio seed aleatorio (excluyendo el actual si es seed)
        quiz_templates = get_quiz_templates_for_week("week01")
        # Filtrar templates que no coincidan con el ejercicio actual
        available_templates = [t for t in quiz_templates if t["question_latex"] != current_question_latex]
        if not available_templates:
            available_templates = quiz_templates  # Si todos coinciden, usar cualquiera
        template = random.choice(available_templates).copy()
        return _build_quiz_instance_from_template(template)

    return dynamic_question


def get_random_question(use_dynamic: bool = False, base_question: str = None) -> Dict[str, Any]:
    """
    Retorna una instancia aleatoria del quiz de Semana 1 con opciones mezcladas

    Args:
        use_dynamic: Si True, genera un ejercicio dinámico usando LLM
        base_question: Enunciado base para generar ejercicio dinámico (requerido si use_dynamic=True)

    Returns:
        Dict con la estructura completa del quiz instance
    """
    # Si se solicita ejercicio dinámico explícitamente, usar LLM generator
    if use_dynamic and base_question:
        dynamic_question = generate_dynamic_question(base_question)
        if dynamic_question:
            return _shuffle_llm_question_options(dynamic_question)
        # Si falla, continuar con lógica normal

    # Switch pedagógico: decidir origen del ejercicio
    origin = choose_exercise_origin()

    # Si el switch elige "llm", intentar generar dinámicamente
    if origin == "llm":
        # Obtener un template seed aleatorio como base para el LLM
        quiz_templates = get_quiz_templates_for_week("week01")
        base_template = random.choice(quiz_templates)
        base_question_latex = base_template["question_latex"]

        # Generar ejercicio dinámico usando el template como base
        dynamic_question = generate_dynamic_question(base_question_latex)

        # Si la generación LLM falló, fallback silencioso a seed
        if dynamic_question is not None:
            # ¡IMPORTANTE! Mezclar las opciones del ejercicio IA también
            return _shuffle_llm_question_options(dynamic_question)
        # Falló LLM - continuar con lógica seed

    # Origen "seed" o fallback por falla LLM: usar templates predefinidos
    quiz_templates = get_quiz_templates_for_week("week01")
    template = random.choice(quiz_templates)
    return _build_quiz_instance_from_template(template)


def _build_quiz_instance_from_template(template: Dict[str, Any]) -> Dict[str, Any]:
    """
    Construye una instancia del quiz a partir de un template seed.

    Args:
        template: Template del ejercicio seed

    Returns:
        Dict con la instancia completa del quiz
    """
    template = template.copy()

    # Construir opciones con identificadores únicos
    options = []

    # Opción correcta
    correct_option = {
        "option_id": "correct",
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
            "option_id": f"incorrect_{i}",
            "latex": choice_latex,
            "is_correct": False,
            "error_id": wrong_option.get("error_id", ""),
            "wrong_steps": wrong_option.get("wrong_steps", []),
            "error_highlight": wrong_option.get("error_highlight", "")
        }
        options.append(incorrect_option)

    # Mezclar opciones
    random.shuffle(options)

    # Crear instancia del quiz
    quiz_instance = {
        "question_latex": template["question_latex"],
        "options": options,
        "solution_steps": template.get("solution_steps", []),
        "correct_answer": template.get("correct_answer", ""),
        "week_id": "week01",
        "source": template.get("source"),
        "seed_id": template.get("seed_id"),
        "origin_label": template.get("origin_label")
    }

    return quiz_instance


def check_answer(question: Dict[str, Any], selected_index: int) -> Dict[str, Any]:
    """
    Verifica si la respuesta seleccionada es correcta

    Args:
        question: La pregunta del quiz
        selected_index: Índice de la opción seleccionada (0-4)

    Returns:
        Dict con resultado de la verificación
    """
    is_correct = selected_index == question["correct_index"]

    result = {
        "is_correct": is_correct,
        "selected_index": selected_index,
        "correct_index": question["correct_index"],
        "selected_answer": question["choices_latex"][selected_index],
        "correct_answer": question["choices_latex"][question["correct_index"]],
        "solution_steps": question.get("solution_steps", [])
    }

    if not is_correct and selected_index > 0:
        # Obtener información del error correspondiente
        wrong_option_index = selected_index - 1  # Ya que el índice 0 es la respuesta correcta
        if wrong_option_index < len(question.get("wrong_options", [])):
            wrong_option = question["wrong_options"][wrong_option_index]
            result["wrong_steps"] = wrong_option.get("wrong_steps", [])
            result["error_highlight"] = wrong_option.get("error_highlight", "")
            result["error_id"] = wrong_option.get("error_id", "")

    return result


def validate_quiz_templates_week01() -> Dict[str, Any]:
    """
    Función de validación para verificar coherencia en QUIZ_TEMPLATES de Week 01.

    Verifica:
    - correct_answer ∈ choices_latex
    - correct_index apunta al elemento correcto
    - Para integrales definidas, el último step menciona el mismo resultado que correct_answer

    Returns:
        Dict con resultados de validación y lista de errores encontrados
    """
    import re

    errors = []
    warnings = []

    for i, template in enumerate(QUIZ_TEMPLATES):
        question = template.get("question_latex", "")
        correct_answer = template.get("correct_answer", "")
        choices_latex = template.get("choices_latex", [])
        correct_index = template.get("correct_index", -1)
        solution_steps = template.get("solution_steps", [])

        # Verificar que correct_answer esté en choices_latex
        if correct_answer not in choices_latex:
            errors.append(f"Template {i}: correct_answer '{correct_answer}' no está en choices_latex")

        # Verificar que correct_index apunta al elemento correcto
        if 0 <= correct_index < len(choices_latex):
            if choices_latex[correct_index] != correct_answer:
                errors.append(f"Template {i}: correct_index {correct_index} apunta a '{choices_latex[correct_index]}' pero correct_answer es '{correct_answer}'")
        else:
            errors.append(f"Template {i}: correct_index {correct_index} fuera de rango (0-{len(choices_latex)-1})")

        # Para integrales definidas, verificar coherencia con último step
        if r"\int_{" in question and solution_steps:
            last_step = solution_steps[-1]
            last_step_math = last_step.get("math", "")
            last_step_text = last_step.get("text", "")

            # Verificación simple: el último step debe contener el mismo resultado que correct_answer
            # Normalización básica para comparación
            def normalize_math(expr: str) -> str:
                # Remover espacios y algunos símbolos comunes
                return re.sub(r'\s+', '', expr).replace('\\', '').replace('{', '').replace('}', '')

            normalized_correct = normalize_math(correct_answer)
            normalized_last_math = normalize_math(last_step_math)
            normalized_last_text = normalize_math(last_step_text)

            # Verificar si el resultado correcto aparece en el último paso
            if (normalized_correct not in normalized_last_math and
                normalized_correct not in normalized_last_text):
                warnings.append(f"Template {i}: último paso no menciona resultado '{correct_answer}'")

            # Validaciones específicas para integrales impropias
            is_improper = any(keyword in question for keyword in ['x^{-1/2}', 'x^{-1}', '1/(x-1)', '1/x'])
            if is_improper:
                # Verificar que solution_steps mencione explícitamente "límite"
                has_limit_mention = any('lim' in step.get('text', '').lower() or 'límite' in step.get('text', '').lower()
                                      for step in solution_steps)
                if not has_limit_mention:
                    warnings.append(f"Template {i}: integral impropia sin mención explícita de límite en solution_steps")

                # Verificar que se mencione convergencia/divergencia
                has_convergence_mention = any('conver' in step.get('text', '').lower() or 'diver' in step.get('text', '').lower()
                                            for step in solution_steps)
                if not has_convergence_mention:
                    warnings.append(f"Template {i}: integral impropia sin mención de convergencia/divergencia")

        # Verificar que los error_id de wrong_options existan en el repositorio de errores
        wrong_options = template.get("wrong_options", [])
        for j, wrong_option in enumerate(wrong_options):
            error_id = wrong_option.get("error_id", "")
            if error_id:
                # Verificación simple: comprobar que existe archivo JSON correspondiente
                # (en un entorno real usaríamos errors_repo, pero para validación estática esto funciona)
                error_file_path = Path(__file__).parent.parent / "data" / "errors" / f"{error_id}.json"
                if not error_file_path.exists():
                    errors.append(f"Template {i}, wrong_option {j}: error_id '{error_id}' no tiene archivo JSON correspondiente")

    result = {
        "total_templates": len(QUIZ_TEMPLATES),
        "errors": errors,
        "warnings": warnings,
        "is_valid": len(errors) == 0,
        "has_warnings": len(warnings) > 0
    }

    return result


# Registro del WeekSpec para Week 01
# Se ejecuta al importar el módulo, después de que QUIZ_TEMPLATES esté definido

def normalize_week01_seed_metadata():
    """
    Garantiza que TODOS los ejercicios semilla tengan:
    - source = "seed"
    - origin_label = "Se"
    - seed_id = "w1-N"
    """
    for idx, template in enumerate(QUIZ_TEMPLATES, start=1):
        template["source"] = "seed"
        template["origin_label"] = "Se"
        template["seed_id"] = f"w1-{idx}"


normalize_week01_seed_metadata()

week01_spec = WeekSpec(
    week_id="week01",
    title="Semana 1",
    subtitle="Integración por partes",
    temas=[
        "Cálculo Integral",
        "Técnicas de integración",
        "Integración por partes",
        "Integrales impropias"
    ],
    tecnicas=[
        "Fórmula de integración por partes: ∫u dv = uv - ∫v du",
        "Elección de u y dv usando regla LIATE",
        "Cálculo de derivadas du y antiderivadas v",
        "Aplicación de la fórmula paso a paso",
        "Verificación por derivación",
        "Integrales definidas impropias: convergencia y divergencia",
        "Teorema Fundamental del Cálculo para integrales impropias"
    ],
    descripcion="""
    Primera semana del curso enfocada en la técnica fundamental de integración por partes
    y conceptos básicos de integrales impropias. Se cubren casos básicos con funciones elementales,
    aplicaciones a integrales definidas (incluyendo impropias), y resolución de errores comunes
    que cometen los estudiantes en estos temas.
    """,
    quiz_templates=QUIZ_TEMPLATES,
    error_tags=[
        "integracion-partes-eleccion-uv",
        "integracion-partes-signo-formula",
        "integracion-partes-derivada-u",
        "integracion-partes-innecesaria",
        "integracion-partes-antiderivada-inventada"
    ]
)

# Registrar la especificación en el sistema
register_week("week01", week01_spec)