"""Week01 quiz seeds (clean implementation).

Provides get_random_question() returning a quiz instance compatible with templates/quiz.html.
"""

import random
from typing import Dict, Any, List

# Compat flags (algunas semanas importan SEED_RATIO desde quiz_week01)
SEED_RATIO = 0.8
LLM_RATIO = 0.2


QUIZ_TEMPLATES: List[Dict[str, Any]] = [
    {
        "question_latex": r"\int x e^{x} \, dx",
        "correct_answer": r"e^{x}(x - 1) + C",
        "solution_steps": [
            {"text": "Aplicamos integración por partes", "math": r"\int u\,dv = uv - \int v\,du"},
            {"text": "Elegimos u = x, dv = e^{x} dx", "math": r"u=x, dv=e^{x}dx"},
            {"text": "Calculamos v = e^{x}, du = dx", "math": r"v=e^{x}, du=dx"},
            {"text": "Aplicamos la fórmula y simplificamos", "math": r"x e^{x} - \int e^{x} dx = x e^{x} - e^{x} + C"},
        ],
        "choices_latex": [
            r"e^{x}(x - 1) + C",
            r"x e^{x} + C",
            r"e^{x}(x + 1) + C",
            r"x e^{x} - e^{x} + C",
        ],
        "correct_index": 0,
        "wrong_options": [
            {"wrong_steps": [{"text": "Elección inapropiada u/dv", "math": r"u=e^{x},dv=x dx"}], "error_highlight": "Elección de u/dv inapropiada", "error_id": "integracion-partes-eleccion-uv"},
            {"wrong_steps": [{"text": "Signo mal aplicado", "math": r"\\int u dv = uv + \\int v du"}], "error_highlight": "Signo incorrecto en la fórmula", "error_id": "integracion-partes-signo-formula"},
            {"wrong_steps": [{"text": "Derivada de u mal calculada", "math": r"du\\neq 2x\\,dx"}], "error_highlight": "Cálculo de derivada incorrecto", "error_id": "integracion-partes-derivada-u"},
        ],
        "source": "seed",
        "seed_id": "w1-1",
        "origin_label": "Se",
    },
    {
        "question_latex": r"\int x \sin(x) \, dx",
        "correct_answer": r"-x\cos x + \sin x + C",
        "solution_steps": [
            {"text": "Integración por partes: u=x, dv=sin x dx", "math": r"u=x, dv=\sin x dx"},
            {"text": "v = -\cos x, du = dx", "math": r"v=-\cos x, du=dx"},
            {"text": "Aplicamos la fórmula y simplificamos", "math": r"-x\cos x + \sin x + C"},
        ],
        "choices_latex": [
            r"-x\cos x + \sin x + C",
            r"x\cos x + C",
            r"\sin x - x\sin x + C",
            r"x(-\cos x) + C",
        ],
        "correct_index": 0,
        "wrong_options": [
            {"wrong_steps": [{"text": "Intercambio u/dv", "math": r"u=\sin x, dv=x dx"}], "error_highlight": "Elección errónea de u/dv", "error_id": "integracion-partes-eleccion-uv"},
            {"wrong_steps": [{"text": "Se olvidó signo en v", "math": r"v=\cos x en lugar de -\cos x"}], "error_highlight": "Signo omitido en antiderivada", "error_id": "integracion-partes-signo-formula"},
            {"wrong_steps": [{"text": "Integral mal resuelta", "math": r"\int\cos x dx != -\sin x"}], "error_highlight": "Integración incorrecta", "error_id": "integracion-partes-innecesaria"},
        ],
        "source": "seed",
        "seed_id": "w1-2",
        "origin_label": "Se",
    },
]

def _build_quiz_instance_from_template(template: Dict[str, Any]) -> Dict[str, Any]:
    t = template.copy()
    options = []
    correct_option = {
        "option_id": "correct",
        "latex": t["choices_latex"][t["correct_index"]],
        "is_correct": True,
        "solution_steps": t.get("solution_steps", []),
        "final_answer": t.get("correct_answer", ""),
    }
    options.append(correct_option)
    wrong_choices = [c for i, c in enumerate(t.get("choices_latex", [])) if i != t.get("correct_index", 0)]
    wrongs = t.get("wrong_options", [])
    for i, (choice, wrong) in enumerate(zip(wrong_choices, wrongs)):
        options.append({
            "option_id": f"incorrect_{i}",
            "latex": choice,
            "is_correct": False,
            "error_id": wrong.get("error_id", ""),
            "wrong_steps": wrong.get("wrong_steps", []),
            "error_highlight": wrong.get("error_highlight", ""),
        })
    random.shuffle(options)
    return {
        "question_latex": t["question_latex"],
        "options": options,
        "solution_steps": t.get("solution_steps", []),
        "correct_answer": t.get("correct_answer", ""),
        "seed_id": t.get("seed_id"),
        "origin_label": t.get("origin_label", "Se"),
    }


def get_random_question() -> Dict[str, Any]:
    tpl = random.choice(QUIZ_TEMPLATES)
    return _build_quiz_instance_from_template(tpl)
