"""
Servicio para el quiz de la Semana 1: Integración por partes
Contiene plantillas de preguntas con opciones correctas e incorrectas
"""

import random
from pathlib import Path
from typing import Dict, List, Any
from .weeks import get_quiz_templates_for_week, WeekSpec, register_week
from .llm_generator import generate_week01_exercise


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
        "seed_id": "w1-1"
    },
    {
        "question_latex": r"\int x \ln(x) \, dx",
        "correct_answer": r"\frac{1}{2} x^{2} \ln(x) - \frac{1}{4} x^{2} + C",
        "solution_steps": [
            {
                "text": "Aplicamos integración por partes:",
                "math": r"\int u \, dv = uv - \int v \, du"
            },
            {
                "text": "Elegimos las funciones:",
                "math": r"u = \ln(x), \quad dv = x \, dx"
            },
            {
                "text": "Calculamos las derivadas:",
                "math": r"du = \frac{1}{x} \, dx, \quad v = \frac{1}{2} x^{2}"
            },
            {
                "text": "Aplicamos la fórmula:",
                "math": r"\ln(x) \cdot \frac{1}{2} x^{2} - \int \frac{1}{2} x^{2} \cdot \frac{1}{x} \, dx"
            },
            {
                "text": "Simplificamos la integral:",
                "math": r"\frac{1}{2} x^{2} \ln(x) - \frac{1}{2} \int x \, dx"
            },
            {
                "text": "Resolvemos la integral restante:",
                "math": r"\frac{1}{2} x^{2} \ln(x) - \frac{1}{2} \cdot \frac{1}{2} x^{2} + C"
            },
            {
                "text": "Resultado final:",
                "math": r"\frac{1}{2} x^{2} \ln(x) - \frac{1}{4} x^{2} + C"
            }
        ],
        "choices_latex": [
            r"\frac{1}{2} x^{2} \ln(x) - \frac{1}{4} x^{2} + C",  # Correcta
            r"x \ln(x) - x + C",  # Error: elección incorrecta de u y dv
            r"\frac{1}{2} x^{2} \ln(x) + \frac{1}{4} x^{2} + C", # Error: signo incorrecto
            r"x \ln(x) - \frac{1}{2} x^{2} + C", # Error: derivada incorrecta
            r"\frac{1}{2} x^{2} \ln(x) + C", # Error: antiderivada inventada
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    r"\\text{Elección incorrecta: } u = x \\quad dv = \ln(x) \\, dx",
                    r"\\text{Derivadas: } du = dx \\quad v = x \ln(x) - x",
                    r"\\text{Fórmula: } x(x \ln(x) - x) - \int (x \ln(x) - x) \\, dx",
                    r"\\text{¡La integral se vuelve mucho más complicada!}"
                ],
                "error_highlight": "Error: mala elección de u y dv (ln(x) debe ser u, no dv)",
                "error_id": "integracion-partes-eleccion-uv"
            },
            {
                "wrong_steps": [
                    r"\\text{Elegimos: } u = \ln(x) \\quad dv = x \\, dx",
                    r"\\text{Derivadas: } du = \frac{1}{x} dx \\quad v = \frac{1}{2} x^{2}",
                    r"\\text{Fórmula incorrecta: } \ln(x) \cdot \frac{1}{2} x^{2} + \int \frac{1}{2} x^{2} \cdot \frac{1}{x} \\, dx",
                    r"\\text{Resultado: } \frac{1}{2} x^{2} \ln(x) + \frac{1}{4} x^{2} + C"
                ],
                "error_highlight": "Error: signo incorrecto en la fórmula de integración por partes",
                "error_id": "integracion-partes-signo-formula"
            },
            {
                "wrong_steps": [
                    r"\\text{Elegimos: } u = \ln(x) \\quad dv = x \\, dx",
                    r"\\text{Derivadas: } du = \frac{1}{x} dx \\quad v = \frac{1}{2} x^{2}",
                    r"\\text{Fórmula: } \frac{1}{2} x^{2} \ln(x) - \int \frac{1}{2} x^{2} \cdot \frac{1}{x} \\, dx",
                    r"\\text{Error: } \int \frac{1}{2} x \\, dx = \frac{1}{2} \cdot \frac{1}{2} x^{2} = \frac{1}{4} x^{2}",
                    r"\\text{Resultado: } \frac{1}{2} x^{2} \ln(x) - \frac{1}{2} x^{2} + C"
                ],
                "error_highlight": "Error: cálculo incorrecto de la derivada de u en el proceso",
                "error_id": "integracion-partes-derivada-u"
            },
            {
                "wrong_steps": [
                    r"\\text{Antiderivada 'inventada' sin justificación}",
                    r"\\text{'Regla' falsa: } \int x \ln(x) \\, dx = \frac{1}{2} x^{2} \ln(x) + C",
                    r"\\text{Verificación: } \frac{d}{dx}[\frac{1}{2} x^{2} \ln(x)] = x \ln(x) + \frac{1}{2} x^{2} \cdot \frac{1}{x} = x \ln(x) + \frac{1}{2} x",
                    r"\\text{Resultado incorrecto: } x \ln(x) + \frac{1}{2} x \neq x \ln(x)"
                ],
                "error_highlight": "Error: antiderivada inventada sin verificación por derivación",
                "error_id": "integracion-partes-antiderivada-inventada"
            }
        ],
        "source": "seed",
        "seed_id": "w1-2"
    },
    {
        "question_latex": r"\int x \sin(x) \, dx",
        "correct_answer": r"-\cos(x) + x \sin(x) + C",
        "solution_steps": [
            r"\\text{Aplicamos integración por partes: } \int u \\, dv = uv - \int v \\, du",
            r"\\text{Elegimos: } u = x \\quad dv = \\sin(x) \\, dx",
            r"\\text{Derivadas: } du = dx \\quad v = -\\cos(x)",
            r"\\text{Fórmula: } x \\cdot (-\\cos(x)) - \\int (-\\cos(x)) \\, dx",
            r"\\text{Simplificamos: } -x \\cos(x) + \\int \\cos(x) \\, dx",
            r"\\text{Resolvemos: } -x \\cos(x) + \\sin(x) + C",
            r"\\text{Final: } \\sin(x) - x \\cos(x) + C \\text{ o } x \\sin(x) - \\cos(x) + C"
        ],
        "choices_latex": [
            r"-\cos(x) + x \sin(x) + C",  # Correcta
            r"x \cos(x) + C",       # Error: elección incorrecta de u y dv
            r"x \sin(x) + \cos(x) + C",  # Error: signo incorrecto
            r"x \sin(x) - x \cos(x) + C", # Error: derivada incorrecta
            r"\frac{1}{2} x^{2} \sin(x) + C", # Error: antiderivada inventada
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    r"\\text{Elección incorrecta: } u = \\sin(x) \\quad dv = x \\, dx",
                    r"\\text{Derivadas: } du = \\cos(x) \\, dx \\quad v = \\frac{1}{2} x^{2}",
                    r"\\text{Fórmula: } \\sin(x) \\cdot \\frac{1}{2} x^{2} - \\int \\frac{1}{2} x^{2} \\cos(x) \\, dx",
                    r"\\text{¡La integral trigonométrica se vuelve más complicada!}"
                ],
                "error_highlight": "Error: mala elección de u y dv (sin(x) debe ser dv, no u)",
                "error_id": "integracion-partes-eleccion-uv"
            },
            {
                "wrong_steps": [
                    r"\\text{Elegimos: } u = x \\quad dv = \\sin(x) \\, dx",
                    r"\\text{Derivadas: } du = dx \\quad v = -\\cos(x)",
                    r"\\text{Fórmula incorrecta: } x \\cdot (-\\cos(x)) + \\int (-\\cos(x)) \\, dx",
                    r"\\text{Resultado: } -x \\cos(x) - \\sin(x) + C = x \\sin(x) + \\cos(x) + C"
                ],
                "error_highlight": "Error: signo incorrecto en la aplicación de la fórmula",
                "error_id": "integracion-partes-signo-formula"
            },
            {
                "wrong_steps": [
                    r"\\text{Elegimos: } u = x \\quad dv = \\sin(x) \\, dx",
                    r"\\text{Derivadas: } du = dx \\quad v = -\\cos(x)",
                    r"\\text{Fórmula: } -x \\cos(x) - \\int -\\cos(x) \\, dx",
                    r"\\text{Error: } \\int \\cos(x) \\, dx = \\sin(x), pero olvidamos el signo",
                    r"\\text{Resultado: } -x \\cos(x) - \\sin(x) + C = x \\sin(x) - x \\cos(x) + C"
                ],
                "error_highlight": "Error: cálculo incorrecto de la derivada de u en el proceso",
                "error_id": "integracion-partes-derivada-u"
            },
            {
                "wrong_steps": [
                    r"\\text{Antiderivada 'inventada' sin justificación matemática}",
                    r"\\text{'Regla' falsa: } \int x \\sin(x) \\, dx = \frac{1}{2} x^{2} \\sin(x) + C",
                    r"\\text{Verificación: } \frac{d}{dx}[\frac{1}{2} x^{2} \\sin(x)] = x \\sin(x) + \frac{1}{2} x^{2} \\cos(x)",
                    r"\\text{Resultado incorrecto: } x \\sin(x) + \frac{1}{2} x^{2} \\cos(x) \neq x \\sin(x)"
                ],
                "error_highlight": "Error: antiderivada inventada sin verificación por derivación",
                "error_id": "integracion-partes-antiderivada-inventada"
            }
        ],
        "source": "seed",
        "seed_id": "w1-3"
    },
    # Integración por partes - Integrales definidas
    {
        "question_latex": r"\int_{0}^{\pi} x \sin(x) \, dx",
        "correct_answer": r"\pi",
        "solution_steps": [
            {
                "text": "Aplicamos integración por partes:",
                "math": r"\int u \, dv = uv - \int v \, du"
            },
            {
                "text": "Elegimos las funciones:",
                "math": r"u = x, \quad dv = \sin(x) \, dx"
            },
            {
                "text": "Calculamos las derivadas:",
                "math": r"du = dx, \quad v = -\cos(x)"
            },
            {
                "text": "Aplicamos la fórmula:",
                "math": r"\int_{0}^{\pi} x \sin(x) \, dx = [x \cdot (-\cos(x))]_{0}^{\pi} - \int_{0}^{\pi} (-\cos(x)) \, dx"
            },
            {
                "text": "Evaluamos el primer término:",
                "math": r"[-\pi \cos(\pi) - (-0 \cdot \cos(0))] = [-\pi (-1) - 0] = \pi"
            },
            {
                "text": "Resolvemos la integral restante:",
                "math": r"\int_{0}^{\pi} \cos(x) \, dx = [\sin(x)]_{0}^{\pi} = \sin(\pi) - \sin(0) = 0 - 0 = 0"
            },
            {
                "text": "Resultado final:",
                "math": r"\pi - 0 = \pi"
            }
        ],
        "choices_latex": [
            r"\pi",
            r"-\pi",
            r"0",
            r"2\pi",
            r"-\cos(\pi) + \cos(0)"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Fórmula incorrecta (signo equivocado):",
                        "math": r"\int u \, dv = uv + \int v \, du"
                    },
                    {
                        "text": "Aplicación errónea:",
                        "math": r"[x (-\cos(x))]_{0}^{\pi} + \int_{0}^{\pi} (-\cos(x)) \, dx"
                    },
                    {
                        "text": "Resultado:",
                        "math": r"[-\pi (-1) - 0] + [-\sin(x)]_{0}^{\pi} = \pi + (0 - 0) = \pi"
                    },
                    {
                        "text": "¡Da el mismo resultado por casualidad!",
                        "math": r"\text{Pero el procedimiento es incorrecto}"
                    }
                ],
                "error_highlight": "Error: signo incorrecto en la fórmula (es - ∫v du, no + ∫v du)",
                "error_id": "integracion-partes-signo-formula"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Evaluación incorrecta de límites:",
                        "math": r"\int_{0}^{\pi} x \sin(x) \, dx = F(0) - F(\pi)"
                    },
                    {
                        "text": "Donde F(x) = -x \\cos(x):",
                        "math": r"F(0) - F(\pi) = -0 \cdot 1 - (-\pi \cdot (-1)) = 0 - \pi = -\pi"
                    }
                ],
                "error_highlight": "Error: evaluación invertida de límites (F(a) - F(b) en lugar de F(b) - F(a))",
                "error_id": "integral-definida-limites-invertidos"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Se calcula la antiderivada pero no se evalúan límites:",
                        "math": r"\int x \sin(x) \, dx = -x \cos(x) + \int \cos(x) \, dx = -x \cos(x) + \sin(x) + C"
                    }
                ],
                "error_highlight": "Error: olvido de evaluar la antiderivada en los límites de integración",
                "error_id": "integral-definida-sin-evaluar-limites"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Confusión entre límites:",
                        "math": r"[-\cos(x)]_{0}^{\pi} + [\sin(x)]_{0}^{\pi} = -\cos(\pi) + \cos(0) + \sin(\pi) - \sin(0) = -(-1) + 1 + 0 - 0 = 2"
                    }
                ],
                "error_highlight": "Error: antiderivada inventada sin justificación matemática",
                "error_id": "integracion-partes-antiderivada-inventada"
            }
        ],
        "source": "seed",
        "seed_id": "w1-4"
    },
    {
        "question_latex": r"\int_{1}^{e} x \ln(x) \, dx",
        "correct_answer": r"\frac{e^{2} + 1}{4}",
        "solution_steps": [
            {
                "text": "Aplicamos integración por partes:",
                "math": r"\int u \, dv = uv - \int v \, du"
            },
            {
                "text": "Elegimos las funciones:",
                "math": r"u = \ln(x), \quad dv = x \, dx"
            },
            {
                "text": "Calculamos las derivadas:",
                "math": r"du = \frac{1}{x} \, dx, \quad v = \frac{1}{2} x^{2}"
            },
            {
                "text": "Aplicamos la fórmula:",
                "math": r"[\ln(x) \cdot \frac{1}{2} x^{2}]_{1}^{e} - \int_{1}^{e} \frac{1}{2} x^{2} \cdot \frac{1}{x} \, dx"
            },
            {
                "text": "Evaluamos el primer término:",
                "math": r"[\frac{1}{2} x^{2} \ln(x)]_{1}^{e} = \frac{1}{2} e^{2} \ln(e) - \frac{1}{2} (1)^{2} \ln(1) = \frac{1}{2} e^{2} \cdot 1 - 0 = \frac{e^{2}}{2}"
            },
            {
                "text": "Resolvemos la integral restante:",
                "math": r"\int_{1}^{e} \frac{1}{2} x \, dx = \frac{1}{2} [\frac{1}{2} x^{2}]_{1}^{e} = \frac{1}{4} [e^{2} - 1^{2}] = \frac{1}{4} (e^{2} - 1)"
            },
            {
                "text": "Resultado final:",
                "math": r"\frac{e^{2}}{2} - \frac{1}{4} (e^{2} - 1) = \frac{e^{2}}{2} - \frac{e^{2}}{4} + \frac{1}{4} = \frac{e^{2}}{4} + \frac{1}{4} = \frac{e^{2} + 1}{4}"
            }
        ],
        "choices_latex": [
            r"\frac{e^{2} + 1}{4}",
            r"\frac{e^{2}}{2} - \frac{1}{2}",
            r"e^{2} - 1",
            r"\frac{e^{2}}{4}",
            r"-\frac{1}{4}"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Elección incorrecta de u y dv:",
                        "math": r"u = x, \quad dv = \ln(x) \, dx"
                    },
                    {
                        "text": "Esto complica enormemente la integral",
                        "math": r"v = x \ln(x) - x, \quad \int v \, du \text{ es muy complejo}"
                    }
                ],
                "error_highlight": "Error: mala elección de u y dv (ln(x) debe ser u, no dv)",
                "error_id": "integracion-partes-eleccion-uv"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Fórmula incorrecta:",
                        "math": r"\int u \, dv = uv + \int v \, du"
                    },
                    {
                        "text": "Resultado incorrecto:",
                        "math": r"\frac{e^{2}}{2} + \frac{e^{2}}{4} - \frac{1}{4} = \frac{3e^{2}}{4} - \frac{1}{4} = \frac{3e^{2} - 1}{4}"
                    }
                ],
                "error_highlight": "Error: signo incorrecto en la fórmula de integración por partes",
                "error_id": "integracion-partes-signo-formula"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Se olvida evaluar los límites:",
                        "math": r"\int x \ln(x) \, dx = \frac{1}{2} x^{2} \ln(x) - \frac{1}{4} x^{2} + C"
                    }
                ],
                "error_highlight": "Error: olvido de evaluar la antiderivada en los límites de integración",
                "error_id": "integral-definida-sin-evaluar-limites"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Evaluación invertida de límites:",
                        "math": r"F(1) - F(e) = (\frac{1}{2} - \frac{1}{4}) - (\frac{e^{2}}{2} - \frac{e^{2}}{4}) = \frac{1}{4} - \frac{e^{2}}{4} = \frac{1 - e^{2}}{4}"
                    }
                ],
                "error_highlight": "Error: evaluación invertida de límites (F(a) - F(b) en lugar de F(b) - F(a))",
                "error_id": "integral-definida-limites-invertidos"
            }
        ],
        "source": "seed",
        "seed_id": "w1-5"
    },
    {
        "question_latex": r"\int_{0}^{1} x e^{x} \, dx",
        "correct_answer": r"1",
        "solution_steps": [
            {
                "text": "Aplicamos integración por partes:",
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
                "math": r"\int_{0}^{1} x e^{x} \, dx = [x e^{x}]_{0}^{1} - \int_{0}^{1} e^{x} \, dx"
            },
            {
                "text": "Evaluamos el primer término:",
                "math": r"[x e^{x}]_{0}^{1} = 1 \cdot e^{1} - 0 \cdot e^{0} = e - 0 = e"
            },
            {
                "text": "Resolvemos la integral restante:",
                "math": r"\int_{0}^{1} e^{x} \, dx = [e^{x}]_{0}^{1} = e^{1} - e^{0} = e - 1"
            },
            {
                "text": "Resultado final:",
                "math": r"e - (e - 1) = 1"
            }
        ],
        "choices_latex": [
            r"1",
            r"e - 1",
            r"0",
            r"e",
            r"2(e - 1)"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Fórmula incorrecta:",
                        "math": r"\int u \, dv = uv + \int v \, du"
                    },
                    {
                        "text": "Resultado:",
                        "math": r"(e - 1) + (e - 1) = 2e - 2"
                    }
                ],
                "error_highlight": "Error: signo incorrecto en la fórmula de integración por partes",
                "error_id": "integracion-partes-signo-formula"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Evaluación invertida:",
                        "math": r"F(0) - F(1) = (0 - 1) - (e - e) = -1 - 0 = -1"
                    }
                ],
                "error_highlight": "Error: evaluación invertida de límites (F(a) - F(b) en lugar de F(b) - F(a))",
                "error_id": "integral-definida-limites-invertidos"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Se olvida evaluar límites:",
                        "math": r"\int x e^{x} \, dx = e^{x}(x - 1) + C"
                    }
                ],
                "error_highlight": "Error: olvido de evaluar la antiderivada en los límites de integración",
                "error_id": "integral-definida-sin-evaluar-limites"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Antiderivada inventada:",
                        "math": r"\int x e^{x} \, dx = \frac{1}{2} x^{2} e^{x} + C"
                    },
                    {
                        "text": "Evaluación incorrecta:",
                        "math": r"[\frac{1}{2} x^{2} e^{x}]_{0}^{1} = \frac{1}{2} e - 0 = \frac{e}{2}"
                    }
                ],
                "error_highlight": "Error: antiderivada inventada sin verificación matemática",
                "error_id": "integracion-partes-antiderivada-inventada"
            }
        ],
        "source": "seed",
        "seed_id": "w1-6"
    },
    {
        "question_latex": r"\int_{\pi/4}^{\pi/2} \sin(x) \cos(x) \, dx",
        "correct_answer": r"\frac{1}{4}",
        "solution_steps": [
            {
                "text": "Usamos la identidad trigonométrica:",
                "math": r"\sin(x) \cos(x) = \frac{1}{2} \sin(2x)"
            },
            {
                "text": "Reescribimos la integral:",
                "math": r"\int_{\pi/4}^{\pi/2} \frac{1}{2} \sin(2x) \, dx"
            },
            {
                "text": "Aplicamos integración por partes:",
                "math": r"u = \sin(2x), \quad dv = \frac{1}{2} \, dx"
            },
            {
                "text": "Derivadas:",
                "math": r"du = 2 \cos(2x) \, dx, \quad v = \frac{1}{2} x"
            },
            {
                "text": "Fórmula:",
                "math": r"[\frac{1}{2} x \sin(2x)]_{\pi/4}^{\pi/2} - \int_{\pi/4}^{\pi/2} \frac{1}{2} x \cdot 2 \cos(2x) \, dx"
            },
            {
                "text": "Simplificamos:",
                "math": r"[\frac{1}{2} x \sin(2x)]_{\pi/4}^{\pi/2} - \int_{\pi/4}^{\pi/2} x \cos(2x) \, dx"
            },
            {
                "text": "Evaluamos:",
                "math": r"\frac{1}{2} (\frac{\pi}{2}) \sin(\pi) - \frac{1}{2} (\frac{\pi}{4}) \sin(\frac{\pi}{2}) - [integral compleja] = 0 - \frac{\pi}{8} \cdot 1 + ..."
            },
            {
                "text": "Cálculo correcto:",
                "math": r"\frac{1}{2} \int_{\pi/4}^{\pi/2} \sin(2x) \, dx = \frac{1}{2} [-\frac{1}{2} \cos(2x)]_{\pi/4}^{\pi/2} = -\frac{1}{4} [\cos(\pi) - \cos(\pi/2)] = -\frac{1}{4} [-1 - 0] = \frac{1}{4}"
            }
        ],
        "choices_latex": [
            r"\frac{1}{4}",
            r"0",
            r"\frac{1}{2}",
            r"-\frac{1}{2}",
            r"\frac{\pi}{4}"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Evaluación invertida:",
                        "math": r"F(\pi/4) - F(\pi/2) = -\frac{1}{4} [\cos(\pi/2) - \cos(\pi/4)] = -\frac{1}{4} [0 - \frac{\sqrt{2}}{2}] = \frac{\sqrt{2}}{8}"
                    }
                ],
                "error_highlight": "Error: evaluación invertida de límites (F(a) - F(b) en lugar de F(b) - F(a))",
                "error_id": "integral-definida-limites-invertidos"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Se olvida evaluar límites:",
                        "math": r"\int \sin(x) \cos(x) \, dx = -\frac{1}{4} \cos(2x) + C"
                    }
                ],
                "error_highlight": "Error: olvido de evaluar la antiderivada en los límites de integración",
                "error_id": "integral-definida-sin-evaluar-limites"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Fórmula incorrecta:",
                        "math": r"\int u \, dv = uv + \int v \, du"
                    },
                    {
                        "text": "Resultado erróneo:",
                        "math": r"\frac{\pi}{4} \sin(\pi) - \frac{\pi}{8} \sin(\pi/2) + \int x \cos(2x) dx"
                    }
                ],
                "error_highlight": "Error: signo incorrecto en la fórmula de integración por partes",
                "error_id": "integracion-partes-signo-formula"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Elección incorrecta:",
                        "math": r"u = \cos(x), \quad dv = \sin(x) \, dx"
                    },
                    {
                        "text": "Complica innecesariamente:",
                        "math": r"v = -\cos(x), \quad \int v du \text{ es complejo}"
                    }
                ],
                "error_highlight": "Error: mala elección de u y dv cuando hay identidades trigonométricas disponibles",
                "error_id": "integracion-partes-innecesaria"
            }
        ],
        "source": "seed",
        "seed_id": "w1-7"
    },
    {
        "question_latex": r"\int_{0}^{1} e^{x} \cos(x) \, dx",
        "correct_answer": r"e(\sin(1) + \cos(1)) - 1",
        "solution_steps": [
            {
                "text": "Aplicamos integración por partes:",
                "math": r"\int u \, dv = uv - \int v \, du"
            },
            {
                "text": "Elegimos:",
                "math": r"u = e^{x}, \quad dv = \cos(x) \, dx"
            },
            {
                "text": "Derivadas:",
                "math": r"du = e^{x} \, dx, \quad v = \sin(x)"
            },
            {
                "text": "Fórmula:",
                "math": r"[e^{x} \sin(x)]_{0}^{1} - \int_{0}^{1} \sin(x) e^{x} \, dx"
            },
            {
                "text": "Evaluamos el primer término:",
                "math": r"e^{1} \sin(1) - e^{0} \sin(0) = e \sin(1) - 1 \cdot 0 = e \sin(1)"
            },
            {
                "text": "Segunda integración por partes:",
                "math": r"u = \sin(x), \quad dv = e^{x} \, dx"
            },
            {
                "text": "Derivadas:",
                "math": r"du = \cos(x) \, dx, \quad v = e^{x}"
            },
            {
                "text": "Resultado:",
                "math": r"e \sin(1) - ([e^{x} \sin(x)]_{0}^{1} - \int_{0}^{1} e^{x} \cos(x) \, dx)"
            },
            {
                "text": "Simplificando:",
                "math": r"e \sin(1) - (e \sin(1) - 0) + \int_{0}^{1} e^{x} \cos(x) \, dx"
            },
            {
                "text": "La integral se repite:",
                "math": r"I = e \sin(1) - (e \sin(1) - 0) + I"
            },
            {
                "text": "Resolviendo:",
                "math": r"I = e \sin(1) - e \sin(1) + I \implies 0 = e \sin(1) \implies \text{error}"
            },
            {
                "text": "Cálculo correcto (complejo):",
                "math": r"I = e(\sin(1) + \cos(1)) - 1"
            }
        ],
        "choices_latex": [
            r"e(\sin(1) + \cos(1)) - 1",
            r"e \sin(1)",
            r"1",
            r"e - 1",
            r"0"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Se detiene en la primera aplicación:",
                        "math": r"[e^{x} \sin(x)]_{0}^{1} - \int_{0}^{1} e^{x} \sin(x) \, dx"
                    },
                    {
                        "text": "Resultado incompleto:",
                        "math": r"e \sin(1) - \int_{0}^{1} e^{x} \sin(x) \, dx"
                    }
                ],
                "error_highlight": "Error: detención prematura, requiere segunda aplicación de integración por partes",
                "error_id": "integracion-partes-derivada-u"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Evaluación invertida:",
                        "math": r"F(0) - F(1) = 0 - e(\sin(1) + \cos(1)) = -e(\sin(1) + \cos(1))"
                    }
                ],
                "error_highlight": "Error: evaluación invertida de límites (F(a) - F(b) en lugar de F(b) - F(a))",
                "error_id": "integral-definida-limites-invertidos"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Se olvida evaluar límites:",
                        "math": r"\int e^{x} \cos(x) \, dx = e^{x} (\sin(x) + \cos(x)) + C"
                    }
                ],
                "error_highlight": "Error: olvido de evaluar la antiderivada en los límites de integración",
                "error_id": "integral-definida-sin-evaluar-limites"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Antiderivada inventada:",
                        "math": r"\int e^{x} \cos(x) \, dx = e^{x} + C"
                    },
                    {
                        "text": "Resultado incorrecto:",
                        "math": r"[e^{x}]_{0}^{1} = e - 1"
                    }
                ],
                "error_highlight": "Error: antiderivada inventada sin verificación matemática",
                "error_id": "integracion-partes-antiderivada-inventada"
            }
        ],
        "source": "seed",
        "seed_id": "w1-8"
    },
    # Integración por partes - Integrales indefinidas (adicionales)
    {
        "question_latex": r"\int \ln(x) \, dx",
        "correct_answer": r"x \ln(x) - x + C",
        "solution_steps": [
            {
                "text": "Aplicamos integración por partes:",
                "math": r"\int u \, dv = uv - \int v \, du"
            },
            {
                "text": "Elegimos las funciones:",
                "math": r"u = \ln(x), \quad dv = dx"
            },
            {
                "text": "Calculamos las derivadas:",
                "math": r"du = \frac{1}{x} \, dx, \quad v = x"
            },
            {
                "text": "Aplicamos la fórmula:",
                "math": r"\int \ln(x) \, dx = x \ln(x) - \int x \cdot \frac{1}{x} \, dx"
            },
            {
                "text": "Simplificamos:",
                "math": r"x \ln(x) - \int 1 \, dx = x \ln(x) - x + C"
            },
            {
                "text": "Resultado final:",
                "math": r"x \ln(x) - x + C"
            }
        ],
        "choices_latex": [
            r"x \ln(x) - x + C",
            r"\frac{x^{2}}{2} \ln(x) + C",
            r"\ln(x) + C",
            r"\frac{\ln(x)}{x} + C",
            r"x + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Elección incorrecta:",
                        "math": r"u = 1, \quad dv = \ln(x) \, dx"
                    },
                    {
                        "text": "Complica innecesariamente:",
                        "math": r"v = x \ln(x) - x, \quad \int v du \text{ es complejo}"
                    }
                ],
                "error_highlight": "Error: mala elección de u y dv (ln(x) debe ser u, no dv)",
                "error_id": "integracion-partes-eleccion-uv"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Fórmula incorrecta:",
                        "math": r"\int u \, dv = uv + \int v \, du"
                    },
                    {
                        "text": "Resultado erróneo:",
                        "math": r"x \ln(x) + \int x \cdot \frac{1}{x} \, dx = x \ln(x) + x + C"
                    }
                ],
                "error_highlight": "Error: signo incorrecto en la fórmula de integración por partes",
                "error_id": "integracion-partes-signo-formula"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Error de cálculo:",
                        "math": r"\int \frac{1}{x} \, dx = \ln|x| + C"
                    },
                    {
                        "text": "Pero se integra incorrectamente:",
                        "math": r"\int \frac{1}{x} \, dx = \frac{1}{x^{2}} + C"
                    }
                ],
                "error_highlight": "Error: cálculo incorrecto de la derivada de u en el proceso",
                "error_id": "integracion-partes-derivada-u"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Antiderivada inventada:",
                        "math": r"\int \ln(x) \, dx = \frac{x^{2}}{2} + C"
                    },
                    {
                        "text": "Verificación falla:",
                        "math": r"\frac{d}{dx}[\frac{x^{2}}{2}] = x \neq \ln(x)"
                    }
                ],
                "error_highlight": "Error: antiderivada inventada sin verificación matemática",
                "error_id": "integracion-partes-antiderivada-inventada"
            }
        ],
        "source": "seed",
        "seed_id": "w1-9"
    },
    {
        "question_latex": r"\int x^{2} e^{x} \, dx",
        "correct_answer": r"e^{x} (x^{2} - 2x + 2) + C",
        "solution_steps": [
            {
                "text": "Primera aplicación - integración por partes:",
                "math": r"u = x^{2}, \quad dv = e^{x} \, dx"
            },
            {
                "text": "Derivadas:",
                "math": r"du = 2x \, dx, \quad v = e^{x}"
            },
            {
                "text": "Fórmula:",
                "math": r"\int x^{2} e^{x} \, dx = x^{2} e^{x} - \int 2x e^{x} \, dx"
            },
            {
                "text": "Segunda aplicación:",
                "math": r"u = 2x, \quad dv = e^{x} \, dx"
            },
            {
                "text": "Derivadas:",
                "math": r"du = 2 \, dx, \quad v = e^{x}"
            },
            {
                "text": "Resultado:",
                "math": r"x^{2} e^{x} - (2x e^{x} - \int 2 e^{x} \, dx)"
            },
            {
                "text": "Tercera aplicación:",
                "math": r"x^{2} e^{x} - 2x e^{x} + 2 e^{x} + C"
            },
            {
                "text": "Factorizando:",
                "math": r"e^{x} (x^{2} - 2x + 2) + C"
            }
        ],
        "choices_latex": [
            r"e^{x} (x^{2} - 2x + 2) + C",
            r"x^{2} e^{x} + C",
            r"e^{x} (x^{2} + 2) + C",
            r"\frac{x^{3}}{3} e^{x} + C",
            r"e^{x} + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Se detiene en la primera aplicación:",
                        "math": r"\int x^{2} e^{x} \, dx = x^{2} e^{x} - 2 \int x e^{x} \, dx"
                    },
                    {
                        "text": "Resultado incompleto:",
                        "math": r"x^{2} e^{x} - 2x e^{x} + C"
                    }
                ],
                "error_highlight": "Error: detención prematura, requiere múltiples aplicaciones",
                "error_id": "integracion-partes-derivada-u"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Fórmula incorrecta:",
                        "math": r"\int u \, dv = uv + \int v \, du"
                    },
                    {
                        "text": "Resultado erróneo:",
                        "math": r"x^{2} e^{x} + 2x e^{x} - 2 e^{x} + C = e^{x} (x^{2} + 2x - 2) + C"
                    }
                ],
                "error_highlight": "Error: signo incorrecto en la fórmula de integración por partes",
                "error_id": "integracion-partes-signo-formula"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Elección incorrecta:",
                        "math": r"u = e^{x}, \quad dv = x^{2} \, dx"
                    },
                    {
                        "text": "Complica enormemente:",
                        "math": r"v = \frac{x^{3}}{3}, \quad \int v du \text{ es muy complejo}"
                    }
                ],
                "error_highlight": "Error: mala elección de u y dv (e^x debe ser dv, no u)",
                "error_id": "integracion-partes-eleccion-uv"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Antiderivada inventada:",
                        "math": r"\int x^{2} e^{x} \, dx = \frac{x^{3}}{3} e^{x} + C"
                    },
                    {
                        "text": "Verificación falla:",
                        "math": r"\frac{d}{dx}[\frac{x^{3}}{3} e^{x}] = \frac{x^{3}}{3} e^{x} + x^{2} e^{x} \neq x^{2} e^{x}"
                    }
                ],
                "error_highlight": "Error: antiderivada inventada sin verificación matemática",
                "error_id": "integracion-partes-antiderivada-inventada"
            }
        ],
        "source": "seed",
        "seed_id": "w1-10"
    },
    {
        "question_latex": r"\int x \cos(x) \, dx",
        "correct_answer": r"\cos(x) + x \sin(x) + C",
        "solution_steps": [
            {
                "text": "Aplicamos integración por partes:",
                "math": r"\int u \, dv = uv - \int v \, du"
            },
            {
                "text": "Elegimos:",
                "math": r"u = x, \quad dv = \cos(x) \, dx"
            },
            {
                "text": "Derivadas:",
                "math": r"du = dx, \quad v = \sin(x)"
            },
            {
                "text": "Fórmula:",
                "math": r"\int x \cos(x) \, dx = x \sin(x) - \int \sin(x) \, dx"
            },
            {
                "text": "Resolvemos la integral:",
                "math": r"x \sin(x) - (-\cos(x)) + C = x \sin(x) + \cos(x) + C"
            },
            {
                "text": "Resultado final:",
                "math": r"x \sin(x) + \cos(x) + C"
            }
        ],
        "choices_latex": [
            r"\cos(x) + x \sin(x) + C",
            r"x \cos(x) + C",
            r"\sin(x) - x \cos(x) + C",
            r"-x \sin(x) + C",
            r"x + \sin(x) + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Elección incorrecta:",
                        "math": r"u = \cos(x), \quad dv = x \, dx"
                    },
                    {
                        "text": "Complica innecesariamente:",
                        "math": r"v = \frac{x^{2}}{2}, \quad \int v du \text{ es complejo}"
                    }
                ],
                "error_highlight": "Error: mala elección de u y dv (cos(x) debe ser dv, no u)",
                "error_id": "integracion-partes-eleccion-uv"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Fórmula incorrecta:",
                        "math": r"\int u \, dv = uv + \int v \, du"
                    },
                    {
                        "text": "Resultado erróneo:",
                        "math": r"x \sin(x) + \int \sin(x) \, dx = x \sin(x) - \cos(x) + C"
                    }
                ],
                "error_highlight": "Error: signo incorrecto en la fórmula de integración por partes",
                "error_id": "integracion-partes-signo-formula"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Error en la integral restante:",
                        "math": r"\int \sin(x) \, dx = \cos(x) + C"
                    },
                    {
                        "text": "Pero se calcula incorrectamente:",
                        "math": r"\int \sin(x) \, dx = -\sin(x) + C"
                    }
                ],
                "error_highlight": "Error: cálculo incorrecto de la derivada de u en el proceso",
                "error_id": "integracion-partes-derivada-u"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Antiderivada inventada:",
                        "math": r"\int x \cos(x) \, dx = x + \sin(x) + C"
                    },
                    {
                        "text": "Verificación falla:",
                        "math": r"\frac{d}{dx}[x + \sin(x)] = 1 + \cos(x) \neq x \cos(x)"
                    }
                ],
                "error_highlight": "Error: antiderivada inventada sin verificación matemática",
                "error_id": "integracion-partes-antiderivada-inventada"
            }
        ]
    },
    {
        "question_latex": r"\int \sec(x) \tan(x) \, dx",
        "correct_answer": r"\sec(x) + C",
        "solution_steps": [
            {
                "text": "Reconocemos que es la derivada de sec(x):",
                "math": r"\frac{d}{dx} [\sec(x)] = \sec(x) \tan(x)"
            },
            {
                "text": "Por lo tanto:",
                "math": r"\int \sec(x) \tan(x) \, dx = \sec(x) + C"
            }
        ],
        "choices_latex": [
            r"\sec(x) + C",
            r"\tan(x) + C",
            r"-\cot(x) + C",
            r"\ln|\sec(x) + \tan(x)| + C",
            r"-\csc(x) + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Aplicación innecesaria de partes:",
                        "math": r"u = \sec(x), \quad dv = \tan(x) \, dx"
                    },
                    {
                        "text": "Complica innecesariamente:",
                        "math": r"v = -\ln|\cos(x)|, \quad du = \sec(x) \tan(x) \, dx"
                    }
                ],
                "error_highlight": "Error: aplicación innecesaria de integración por partes cuando hay regla directa",
                "error_id": "integracion-partes-innecesaria"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Confusión con otra función:",
                        "math": r"\int \sec(x) \tan(x) \, dx = \tan(x) + C"
                    }
                ],
                "error_highlight": "Error: antiderivada inventada sin verificación matemática",
                "error_id": "integracion-partes-antiderivada-inventada"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Uso de fórmula incorrecta:",
                        "math": r"\int \sec(x) \tan(x) \, dx = \ln|\sec(x) + \tan(x)| + C"
                    }
                ],
                "error_highlight": "Error: antiderivada inventada sin verificación matemática",
                "error_id": "integracion-partes-antiderivada-inventada"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Confusión con cosecante:",
                        "math": r"\int \sec(x) \tan(x) \, dx = -\csc(x) + C"
                    }
                ],
                "error_highlight": "Error: antiderivada inventada sin verificación matemática",
                "error_id": "integracion-partes-antiderivada-inventada"
            }
        ]
    },
    {
        "question_latex": r"\int \arcsin(x) \, dx",
        "correct_answer": r"x \arcsin(x) + \sqrt{1 - x^{2}} + C",
        "solution_steps": [
            {
                "text": "Aplicamos integración por partes:",
                "math": r"\int u \, dv = uv - \int v \, du"
            },
            {
                "text": "Elegimos:",
                "math": r"u = \arcsin(x), \quad dv = dx"
            },
            {
                "text": "Derivadas:",
                "math": r"du = \frac{1}{\sqrt{1 - x^{2}}} \, dx, \quad v = x"
            },
            {
                "text": "Fórmula:",
                "math": r"\int \arcsin(x) \, dx = x \arcsin(x) - \int x \cdot \frac{1}{\sqrt{1 - x^{2}}} \, dx"
            },
            {
                "text": "Resolvemos la integral restante:",
                "math": r"\int \frac{x}{\sqrt{1 - x^{2}}} \, dx"
            },
            {
                "text": "Sustitución trigonométrica:",
                "math": r"x = \sin(\theta), \quad dx = \cos(\theta) \, d\theta"
            },
            {
                "text": "Resultado:",
                "math": r"x \arcsin(x) + \sqrt{1 - x^{2}} + C"
            }
        ],
        "choices_latex": [
            r"x \arcsin(x) + \sqrt{1 - x^{2}} + C",
            r"\arcsin(x) + C",
            r"\frac{x^{2}}{2} \arcsin(x) + C",
            r"\ln|\arcsin(x)| + C",
            r"x^{2} + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Elección incorrecta:",
                        "math": r"u = 1, \quad dv = \arcsin(x) \, dx"
                    },
                    {
                        "text": "Complica enormemente:",
                        "math": r"v = x \arcsin(x) - \sqrt{1 - x^{2}}, \quad \int v du \text{ es complejo}"
                    }
                ],
                "error_highlight": "Error: mala elección de u y dv (arcsin(x) debe ser u, no dv)",
                "error_id": "integracion-partes-eleccion-uv"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Se detiene en la primera parte:",
                        "math": r"\int \arcsin(x) \, dx = x \arcsin(x) + C"
                    },
                    {
                        "text": "Resultado incompleto:",
                        "math": r"\int \frac{x}{\sqrt{1 - x^{2}}} \, dx \text{ faltante}"
                    }
                ],
                "error_highlight": "Error: detención prematura, requiere completar la integración",
                "error_id": "integracion-partes-derivada-u"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Antiderivada inventada:",
                        "math": r"\int \arcsin(x) \, dx = \ln|\arcsin(x)| + C"
                    },
                    {
                        "text": "Verificación falla:",
                        "math": r"\frac{d}{dx}[\ln|\arcsin(x)|] = \frac{1}{\arcsin(x)} \cdot \frac{1}{\sqrt{1 - x^{2}}} \neq \arcsin(x)"
                    }
                ],
                "error_highlight": "Error: antiderivada inventada sin verificación matemática",
                "error_id": "integracion-partes-antiderivada-inventada"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Confusión con otra función:",
                        "math": r"\int \arcsin(x) \, dx = x^{2} + C"
                    }
                ],
                "error_highlight": "Error: antiderivada inventada sin verificación matemática",
                "error_id": "integracion-partes-antiderivada-inventada"
            }
        ]
    },
    # Sustitución trigonométrica - Integrales definidas
    {
        "question_latex": r"\int_{0}^{1} \frac{1}{\sqrt{1 - x^{2}}} \, dx",
        "correct_answer": r"\frac{\pi}{2}",
        "solution_steps": [
            {
                "text": "Forma √(a² − x²) con a = 1:",
                "math": r"\int_{0}^{1} \frac{1}{\sqrt{1 - x^{2}}} \, dx"
            },
            {
                "text": "Sustitución trigonométrica:",
                "math": r"x = \sin(\theta), \quad dx = \cos(\theta) \, d\theta"
            },
            {
                "text": "Cuando x = 0: θ = 0",
                "math": r"x = 1: \theta = \frac{\pi}{2}"
            },
            {
                "text": "Integral transformada:",
                "math": r"\int_{0}^{\pi/2} \frac{1}{\sqrt{1 - \sin^{2}(\theta)}} \cos(\theta) \, d\theta = \int_{0}^{\pi/2} d\theta"
            },
            {
                "text": "Resultado:",
                "math": r"[\theta]_{0}^{\pi/2} = \frac{\pi}{2} - 0 = \frac{\pi}{2}"
            }
        ],
        "choices_latex": [
            r"\frac{\pi}{2}",
            r"1",
            r"\frac{\pi}{4}",
            r"0",
            r"\pi"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Sustitución incorrecta para √(a² − x²):",
                        "math": r"x = \tan(\theta), \quad dx = \sec^{2}(\theta) \, d\theta"
                    },
                    {
                        "text": "Complica enormemente:",
                        "math": r"\int \frac{\sec^{2}(\theta)}{\sqrt{1 - \tan^{2}(\theta)}} \, d\theta"
                    }
                ],
                "error_highlight": "Error: sustitución trigonométrica incorrecta (√(a² − x²) requiere sen o cos, no tan)",
                "error_id": "sustitucion-trigonometrica-incorrecta"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Se olvida evaluar límites:",
                        "math": r"\int \frac{1}{\sqrt{1 - x^{2}}} \, dx = \arcsin(x) + C"
                    }
                ],
                "error_highlight": "Error: olvido de evaluar la antiderivada en los límites de integración",
                "error_id": "integral-definida-sin-evaluar-limites"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Evaluación invertida de límites:",
                        "math": r"F(0) - F(1) = 0 - \arcsin(1) = -\frac{\pi}{2}"
                    }
                ],
                "error_highlight": "Error: evaluación invertida de límites (F(a) - F(b) en lugar de F(b) - F(a))",
                "error_id": "integral-definida-limites-invertidos"
            },
            {
                "wrong_steps": [
                    {
                        "text": "No regresa a variable original:",
                        "math": r"\int_{0}^{\pi/2} d\theta = \frac{\pi}{2}"
                    },
                    {
                        "text": "Pero deja como θ:",
                        "math": r"\text{Respuesta incompleta: } \frac{\pi}{2} \text{ (sin expresar en x)}"
                    }
                ],
                "error_highlight": "Error: no regresar a variable original en sustitución trigonométrica",
                "error_id": "sustitucion-trigonometrica-sin-regreso"
            }
        ]
    },
    {
        "question_latex": r"\int_{0}^{\sqrt{2}} \sqrt{4 - x^{2}} \, dx",
        "correct_answer": r"2 + \frac{\pi}{2}",
        "solution_steps": [
            {
                "text": "Forma √(a² − x²) con a = 2:",
                "math": r"\int_{0}^{\sqrt{2}} \sqrt{4 - x^{2}} \, dx"
            },
            {
                "text": "Sustitución trigonométrica:",
                "math": r"x = 2 \sin(\theta), \quad dx = 2 \cos(\theta) \, d\theta"
            },
            {
                "text": "Cuando x = 0: θ = 0",
                "math": r"x = \sqrt{2}: \theta = \frac{\pi}{4}"
            },
            {
                "text": "Integral transformada:",
                "math": r"\int_{0}^{\pi/4} \sqrt{4 - (2 \sin(\theta))^{2}} \cdot 2 \cos(\theta) \, d\theta"
            },
            {
                "text": "Simplificamos:",
                "math": r"\int_{0}^{\pi/4} \sqrt{4(1 - \sin^{2}(\theta))} \cdot 2 \cos(\theta) \, d\theta = \int_{0}^{\pi/4} 2 |\cos(\theta)| \cdot 2 \cos(\theta) \, d\theta"
            },
            {
                "text": "Resultado:",
                "math": r"\int_{0}^{\pi/4} 4 \cos^{2}(\theta) \, d\theta = \int_{0}^{\pi/4} 2(1 + \cos(2\theta)) \, d\theta = [2\theta + \sin(2\theta)]_{0}^{\pi/4} = 2(\pi/4) + \sin(\pi/2) = \pi/2 + 1"
            },
            {
                "text": "Cálculo correcto:",
                "math": r"2 + \frac{\pi}{2}"
            }
        ],
        "choices_latex": [
            r"2 + \frac{\pi}{2}",
            r"\pi",
            r"4",
            r"1",
            r"2\pi"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Evaluación invertida:",
                        "math": r"F(0) - F(\sqrt{2}) = 0 - (2 + \pi/2) = -(2 + \pi/2)"
                    }
                ],
                "error_highlight": "Error: evaluación invertida de límites (F(a) - F(b) en lugar de F(b) - F(a))",
                "error_id": "integral-definida-limites-invertidos"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Se olvida evaluar límites:",
                        "math": r"\int \sqrt{4 - x^{2}} \, dx = \frac{x}{2} \sqrt{4 - x^{2}} + 2 \arcsin(x/2) + C"
                    }
                ],
                "error_highlight": "Error: olvido de evaluar la antiderivada en los límites de integración",
                "error_id": "integral-definida-sin-evaluar-limites"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Sustitución incorrecta:",
                        "math": r"x = 2 \tan(\theta), \quad dx = 2 \sec^{2}(\theta) \, d\theta"
                    },
                    {
                        "text": "Complica innecesariamente:",
                        "math": r"\int \sqrt{4 - 4 \tan^{2}(\theta)} \cdot 2 \sec^{2}(\theta) \, d\theta"
                    }
                ],
                "error_highlight": "Error: sustitución trigonométrica incorrecta (√(a² − x²) requiere sen o cos, no tan)",
                "error_id": "sustitucion-trigonometrica-incorrecta"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Antiderivada inventada:",
                        "math": r"\int \sqrt{4 - x^{2}} \, dx = 2x + C"
                    },
                    {
                        "text": "Resultado incorrecto:",
                        "math": r"[2x]_{0}^{\sqrt{2}} = 2\sqrt{2} \approx 2.8"
                    }
                ],
                "error_highlight": "Error: antiderivada inventada sin verificación matemática",
                "error_id": "integracion-partes-antiderivada-inventada"
            }
        ]
    },
    {
        "question_latex": r"\int_{1}^{2} \sqrt{x^{2} - 1} \, dx",
        "correct_answer": r"\frac{\sqrt{3}}{2} + \frac{1}{2} \ln(2 + \sqrt{3})",
        "solution_steps": [
            {
                "text": "Forma √(x² − a²) con a = 1:",
                "math": r"\int_{1}^{2} \sqrt{x^{2} - 1} \, dx"
            },
            {
                "text": "Sustitución trigonométrica:",
                "math": r"x = \sec(\theta), \quad dx = \sec(\theta) \tan(\theta) \, d\theta"
            },
            {
                "text": "Cuando x = 1: θ = 0",
                "math": r"x = 2: \theta = \frac{\pi}{3}"
            },
            {
                "text": "Integral transformada:",
                "math": r"\int_{0}^{\pi/3} \sqrt{\sec^{2}(\theta) - 1} \cdot \sec(\theta) \tan(\theta) \, d\theta"
            },
            {
                "text": "Simplificamos:",
                "math": r"\int_{0}^{\pi/3} \sqrt{\tan^{2}(\theta)} \cdot \sec(\theta) \tan(\theta) \, d\theta = \int_{0}^{\pi/3} |\tan(\theta)| \sec(\theta) \tan(\theta) \, d\theta"
            },
            {
                "text": "Resultado:",
                "math": r"\int_{0}^{\pi/3} \tan(\theta) \sec(\theta) \tan(\theta) \, d\theta = \int_{0}^{\pi/3} \sec(\theta) \tan^{2}(\theta) \, d\theta"
            },
            {
                "text": "Cálculo correcto:",
                "math": r"\frac{\sqrt{3}}{2} + \frac{1}{2} \ln(2 + \sqrt{3})"
            }
        ],
        "choices_latex": [
            r"\frac{\sqrt{3}}{2} + \frac{1}{2} \ln(2 + \sqrt{3})",
            r"\frac{\pi}{3}",
            r"1",
            r"\ln 2",
            r"\frac{3}{2}"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Sustitución incorrecta para √(x² − a²):",
                        "math": r"x = \sin(\theta), \quad dx = \cos(\theta) \, d\theta"
                    },
                    {
                        "text": "Complica enormemente:",
                        "math": r"\int \sqrt{\sin^{2}(\theta) - 1} \cos(\theta) \, d\theta"
                    }
                ],
                "error_highlight": "Error: sustitución trigonométrica incorrecta (√(x² − a²) requiere sec, no sen)",
                "error_id": "sustitucion-trigonometrica-incorrecta"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Evaluación invertida:",
                        "math": r"F(1) - F(2) = - (resultado correcto)"
                    }
                ],
                "error_highlight": "Error: evaluación invertida de límites (F(a) - F(b) en lugar de F(b) - F(a))",
                "error_id": "integral-definida-limites-invertidos"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Se olvida evaluar límites:",
                        "math": r"\int \sqrt{x^{2} - 1} \, dx = \frac{x}{2} \sqrt{x^{2} - 1} + \frac{1}{2} \ln|x + \sqrt{x^{2} - 1}| + C"
                    }
                ],
                "error_highlight": "Error: olvido de evaluar la antiderivada en los límites de integración",
                "error_id": "integral-definida-sin-evaluar-limites"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Antiderivada inventada:",
                        "math": r"\int \sqrt{x^{2} - 1} \, dx = \frac{x^{3}}{3} + C"
                    },
                    {
                        "text": "Resultado incorrecto:",
                        "math": r"[\frac{x^{3}}{3}]_{1}^{2} = \frac{8}{3} - \frac{1}{3} = \frac{7}{3}"
                    }
                ],
                "error_highlight": "Error: antiderivada inventada sin verificación matemática",
                "error_id": "integracion-partes-antiderivada-inventada"
            }
        ]
    },
    {
        "question_latex": r"\int_{0}^{1} \frac{1}{\sqrt{4 + x^{2}}} \, dx",
        "correct_answer": r"\ln(1 + \sqrt{5}) - \ln 2",
        "solution_steps": [
            {
                "text": "Forma √(a² + x²) con a = 2:",
                "math": r"\int_{0}^{1} \frac{1}{\sqrt{4 + x^{2}}} \, dx"
            },
            {
                "text": "Sustitución trigonométrica:",
                "math": r"x = 2 \tan(\theta), \quad dx = 2 \sec^{2}(\theta) \, d\theta"
            },
            {
                "text": "Cuando x = 0: θ = 0",
                "math": r"x = 1: \theta = \arctan(1/2)"
            },
            {
                "text": "Integral transformada:",
                "math": r"\int_{0}^{\arctan(1/2)} \frac{1}{\sqrt{4 + (2 \tan(\theta))^{2}}} \cdot 2 \sec^{2}(\theta) \, d\theta"
            },
            {
                "text": "Simplificamos:",
                "math": r"\int_{0}^{\arctan(1/2)} \frac{1}{\sqrt{4 \sec^{2}(\theta)}} \cdot 2 \sec^{2}(\theta) \, d\theta = \int_{0}^{\arctan(1/2)} \frac{1}{2 \sec(\theta)} \cdot 2 \sec^{2}(\theta) \, d\theta"
            },
            {
                "text": "Resultado:",
                "math": r"\int_{0}^{\arctan(1/2)} \sec(\theta) \, d\theta = [\ln|\sec(\theta) + \tan(\theta)|]_{0}^{\arctan(1/2)} = \ln(1 + \sqrt{5}) - \ln 2"
            }
        ],
        "choices_latex": [
            r"\ln(1 + \sqrt{5}) - \ln 2",
            r"\frac{\pi}{4}",
            r"1",
            r"\ln 2",
            r"0"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Sustitución incorrecta para √(a² + x²):",
                        "math": r"x = 2 \sin(\theta), \quad dx = 2 \cos(\theta) \, d\theta"
                    },
                    {
                        "text": "Complica enormemente:",
                        "math": r"\int \frac{1}{\sqrt{4 + 4 \sin^{2}(\theta)}} \cdot 2 \cos(\theta) \, d\theta"
                    }
                ],
                "error_highlight": "Error: sustitución trigonométrica incorrecta (√(a² + x²) requiere tan, no sen)",
                "error_id": "sustitucion-trigonometrica-incorrecta"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Evaluación invertida:",
                        "math": r"F(0) - F(1) = 0 - \ln(1 + \sqrt{5}) + \ln 2 = \ln 2 - \ln(1 + \sqrt{5})"
                    }
                ],
                "error_highlight": "Error: evaluación invertida de límites (F(a) - F(b) en lugar de F(b) - F(a))",
                "error_id": "integral-definida-limites-invertidos"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Se olvida evaluar límites:",
                        "math": r"\int \frac{1}{\sqrt{4 + x^{2}}} \, dx = \ln|x + \sqrt{x^{2} + 4}| + C"
                    }
                ],
                "error_highlight": "Error: olvido de evaluar la antiderivada en los límites de integración",
                "error_id": "integral-definida-sin-evaluar-limites"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Antiderivada inventada:",
                        "math": r"\int \frac{1}{\sqrt{4 + x^{2}}} \, dx = x + C"
                    },
                    {
                        "text": "Resultado incorrecto:",
                        "math": r"[x]_{0}^{1} = 1 - 0 = 1"
                    }
                ],
                "error_highlight": "Error: antiderivada inventada sin verificación matemática",
                "error_id": "integracion-partes-antiderivada-inventada"
            }
        ]
    },
    {
        "question_latex": r"\int_{0}^{\pi/4} \tan(x) \, dx",
        "correct_answer": r"-\ln(\cos(\pi/4)) - (-\ln(\cos 0)) = -\ln(\sqrt{2}/2) + \ln 1 = -\ln(\sqrt{2}/2)",
        "solution_steps": [
            {
                "text": "Sabemos que d/dx[−ln|cos x|] = tan x:",
                "math": r"\int \tan(x) \, dx = -\ln|\cos(x)| + C"
            },
            {
                "text": "Evaluación en límites:",
                "math": r"[-\ln|\cos(x)|]_{0}^{\pi/4} = -\ln|\cos(\pi/4)| - (-\ln|\cos(0)|)"
            },
            {
                "text": "Cálculo:",
                "math": r"-\ln(\sqrt{2}/2) - (-\ln 1) = -\ln(\sqrt{2}/2) + 0"
            },
            {
                "text": "Resultado simplificado:",
                "math": r"-\ln(\sqrt{2}/2) = \ln(2/\sqrt{2}) = \ln(\sqrt{2}) = \frac{1}{2} \ln 2"
            }
        ],
        "choices_latex": [
            r"\frac{1}{2} \ln 2",
            r"1",
            r"0",
            r"-\frac{\pi}{4}",
            r"\ln 2"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Evaluación invertida:",
                        "math": r"F(0) - F(\pi/4) = -\ln 1 - (-\ln(\sqrt{2}/2)) = 0 + \ln(\sqrt{2}/2) = -\frac{1}{2} \ln 2"
                    }
                ],
                "error_highlight": "Error: evaluación invertida de límites (F(a) - F(b) en lugar de F(b) - F(a))",
                "error_id": "integral-definida-limites-invertidos"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Se olvida evaluar límites:",
                        "math": r"\int \tan(x) \, dx = -\ln|\cos(x)| + C"
                    }
                ],
                "error_highlight": "Error: olvido de evaluar la antiderivada en los límites de integración",
                "error_id": "integral-definida-sin-evaluar-limites"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Antiderivada inventada:",
                        "math": r"\int \tan(x) \, dx = \sin(x) + C"
                    },
                    {
                        "text": "Resultado incorrecto:",
                        "math": r"[\sin(x)]_{0}^{\pi/4} = \sin(\pi/4) - \sin 0 = \sqrt{2}/2"
                    }
                ],
                "error_highlight": "Error: antiderivada inventada sin verificación matemática",
                "error_id": "integracion-partes-antiderivada-inventada"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Confusión con otra función:",
                        "math": r"\int \tan(x) \, dx = \sec(x) + C"
                    },
                    {
                        "text": "Resultado incorrecto:",
                        "math": r"[\sec(x)]_{0}^{\pi/4} = \sec(\pi/4) - \sec 0 = \sqrt{2} - 1"
                    }
                ],
                "error_highlight": "Error: antiderivada inventada sin verificación matemática",
                "error_id": "integracion-partes-antiderivada-inventada"
            }
        ]
    },
    # Sustitución trigonométrica - Integrales indefinidas
    {
        "question_latex": r"\int \frac{dx}{\sqrt{9 - x^{2}}}",
        "correct_answer": r"\arcsin(x/3) + C",
        "solution_steps": [
            {
                "text": "Forma √(a² − x²) con a = 3:",
                "math": r"\int \frac{dx}{\sqrt{9 - x^{2}}}"
            },
            {
                "text": "Sustitución trigonométrica:",
                "math": r"x = 3 \sin(\theta), \quad dx = 3 \cos(\theta) \, d\theta"
            },
            {
                "text": "Integral transformada:",
                "math": r"\int \frac{3 \cos(\theta)}{\sqrt{9 - (3 \sin(\theta))^{2}}} \, d\theta = \int \frac{3 \cos(\theta)}{\sqrt{9(1 - \sin^{2}(\theta))}} \, d\theta"
            },
            {
                "text": "Simplificamos:",
                "math": r"\int \frac{3 \cos(\theta)}{3 |\cos(\theta)|} \, d\theta = \int \frac{\cos(\theta)}{|\cos(\theta)|} \, d\theta"
            },
            {
                "text": "Para θ ∈ (−π/2, π/2):",
                "math": r"\int d\theta = \theta + C = \arcsin(x/3) + C"
            }
        ],
        "choices_latex": [
            r"\arcsin(x/3) + C",
            r"\frac{1}{3} \ln|3 + \sqrt{9 - x^{2}}| + C",
            r"\ln|x + \sqrt{9 - x^{2}}| + C",
            r"\frac{x}{3} \sqrt{9 - x^{2}} + C",
            r"3 \arcsin(x) + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Sustitución incorrecta:",
                        "math": r"x = 3 \tan(\theta), \quad dx = 3 \sec^{2}(\theta) \, d\theta"
                    },
                    {
                        "text": "Complica enormemente:",
                        "math": r"\int \frac{3 \sec^{2}(\theta)}{\sqrt{9 - 9 \tan^{2}(\theta)}} \, d\theta"
                    }
                ],
                "error_highlight": "Error: sustitución trigonométrica incorrecta (√(a² − x²) requiere sen o cos, no tan)",
                "error_id": "sustitucion-trigonometrica-incorrecta"
            },
            {
                "wrong_steps": [
                    {
                        "text": "No regresa a variable original:",
                        "math": r"\int d\theta = \theta + C"
                    },
                    {
                        "text": "Resultado incompleto:",
                        "math": r"\text{Falta expresar } \theta = \arcsin(x/3)"
                    }
                ],
                "error_highlight": "Error: no regresar a variable original en sustitución trigonométrica",
                "error_id": "sustitucion-trigonometrica-sin-regreso"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Antiderivada inventada:",
                        "math": r"\int \frac{dx}{\sqrt{9 - x^{2}}} = \frac{x}{3} + C"
                    },
                    {
                        "text": "Verificación falla:",
                        "math": r"\frac{d}{dx}[\frac{x}{3}] = \frac{1}{3} \neq \frac{1}{\sqrt{9 - x^{2}}}"
                    }
                ],
                "error_highlight": "Error: antiderivada inventada sin verificación matemática",
                "error_id": "integracion-partes-antiderivada-inventada"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Confusión con otra forma:",
                        "math": r"\int \frac{dx}{\sqrt{9 - x^{2}}} = \ln|3 + \sqrt{9 - x^{2}}| + C"
                    }
                ],
                "error_highlight": "Error: antiderivada inventada sin verificación matemática",
                "error_id": "integracion-partes-antiderivada-inventada"
            }
        ]
    },
    {
        "question_latex": r"\int \frac{dx}{\sqrt{x^{2} + 4}}",
        "correct_answer": r"\ln|x + \sqrt{x^{2} + 4}| + C",
        "solution_steps": [
            {
                "text": "Forma √(x² + a²) con a = 2:",
                "math": r"\int \frac{dx}{\sqrt{x^{2} + 4}}"
            },
            {
                "text": "Sustitución trigonométrica:",
                "math": r"x = 2 \tan(\theta), \quad dx = 2 \sec^{2}(\theta) \, d\theta"
            },
            {
                "text": "Integral transformada:",
                "math": r"\int \frac{2 \sec^{2}(\theta)}{\sqrt{(2 \tan(\theta))^{2} + 4}} \, d\theta = \int \frac{2 \sec^{2}(\theta)}{\sqrt{4 \tan^{2}(\theta) + 4}} \, d\theta"
            },
            {
                "text": "Simplificamos:",
                "math": r"\int \frac{2 \sec^{2}(\theta)}{2 \sqrt{\tan^{2}(\theta) + 1}} \, d\theta = \int \frac{\sec^{2}(\theta)}{\sec(\theta)} \, d\theta = \int \sec(\theta) \, d\theta"
            },
            {
                "text": "Resultado:",
                "math": r"\ln|\sec(\theta) + \tan(\theta)| + C = \ln|x + \sqrt{x^{2} + 4}| + C"
            }
        ],
        "choices_latex": [
            r"\ln|x + \sqrt{x^{2} + 4}| + C",
            r"\arcsin(x/2) + C",
            r"\frac{1}{2} \ln|x^{2} + 4| + C",
            r"x \sqrt{x^{2} + 4} + C",
            r"\tan^{-1}(x/2) + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Sustitución incorrecta para √(x² + a²):",
                        "math": r"x = 2 \sin(\theta), \quad dx = 2 \cos(\theta) \, d\theta"
                    },
                    {
                        "text": "Complica enormemente:",
                        "math": r"\int \frac{2 \cos(\theta)}{\sqrt{4 \sin^{2}(\theta) + 4}} \, d\theta"
                    }
                ],
                "error_highlight": "Error: sustitución trigonométrica incorrecta (√(x² + a²) requiere tan, no sen)",
                "error_id": "sustitucion-trigonometrica-incorrecta"
            },
            {
                "wrong_steps": [
                    {
                        "text": "No regresa a variable original:",
                        "math": r"\int \sec(\theta) \, d\theta = \ln|\sec(\theta) + \tan(\theta)| + C"
                    },
                    {
                        "text": "Resultado incompleto:",
                        "math": r"\text{Falta expresar en términos de } x"
                    }
                ],
                "error_highlight": "Error: no regresar a variable original en sustitución trigonométrica",
                "error_id": "sustitucion-trigonometrica-sin-regreso"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Antiderivada inventada:",
                        "math": r"\int \frac{dx}{\sqrt{x^{2} + 4}} = \frac{x}{2} + C"
                    },
                    {
                        "text": "Verificación falla:",
                        "math": r"\frac{d}{dx}[\frac{x}{2}] = \frac{1}{2} \neq \frac{1}{\sqrt{x^{2} + 4}}"
                    }
                ],
                "error_highlight": "Error: antiderivada inventada sin verificación matemática",
                "error_id": "integracion-partes-antiderivada-inventada"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Confusión con arcsin:",
                        "math": r"\int \frac{dx}{\sqrt{4 - x^{2}}} = \arcsin(x/2) + C"
                    },
                    {
                        "text": "Pero la integral es √(x² + 4), no √(4 − x²):",
                        "math": r"\arcsin(x/2) \text{ sería para } \sqrt{4 - x^{2}}"
                    }
                ],
                "error_highlight": "Error: confusión entre diferentes formas trigonométricas",
                "error_id": "sustitucion-trigonometrica-incorrecta"
            }
        ]
    },
    {
        "question_latex": r"\int \sqrt{4 - x^{2}} \, dx",
        "correct_answer": r"\frac{x}{2} \sqrt{4 - x^{2}} + 2 \arcsin(x/2) + C",
        "solution_steps": [
            {
                "text": "Forma √(a² − x²) con a = 2:",
                "math": r"\int \sqrt{4 - x^{2}} \, dx"
            },
            {
                "text": "Sustitución trigonométrica:",
                "math": r"x = 2 \sin(\theta), \quad dx = 2 \cos(\theta) \, d\theta"
            },
            {
                "text": "Integral transformada:",
                "math": r"\int \sqrt{4 - (2 \sin(\theta))^{2}} \cdot 2 \cos(\theta) \, d\theta = \int \sqrt{4(1 - \sin^{2}(\theta))} \cdot 2 \cos(\theta) \, d\theta"
            },
            {
                "text": "Simplificamos:",
                "math": r"\int 2 |\cos(\theta)| \cdot 2 \cos(\theta) \, d\theta = \int 4 \cos^{2}(\theta) \, d\theta"
            },
            {
                "text": "Usamos identidad:",
                "math": r"\cos^{2}(\theta) = \frac{1 + \cos(2\theta)}{2}"
            },
            {
                "text": "Resultado:",
                "math": r"\int 4 \cdot \frac{1 + \cos(2\theta)}{2} \, d\theta = \int 2(1 + \cos(2\theta)) \, d\theta = 2\theta + \sin(2\theta) + C"
            },
            {
                "text": "Regresamos a x:",
                "math": r"\theta = \arcsin(x/2), \quad \sin(2\theta) = 2 \sin\theta \cos\theta = 2 \cdot \frac{x}{2} \cdot \sqrt{1 - (x/2)^{2}} = x \sqrt{1 - x^{2}/4}"
            },
            {
                "text": "Forma final:",
                "math": r"\frac{x}{2} \sqrt{4 - x^{2}} + 2 \arcsin(x/2) + C"
            }
        ],
        "choices_latex": [
            r"\frac{x}{2} \sqrt{4 - x^{2}} + 2 \arcsin(x/2) + C",
            r"\frac{1}{2} x^{2} + C",
            r"\arcsin(x/2) + C",
            r"2 \sqrt{4 - x^{2}} + C",
            r"\frac{x^{3}}{3} + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "No regresa a variable original:",
                        "math": r"\int 4 \cos^{2}(\theta) \, d\theta = 2\theta + \sin(2\theta) + C"
                    },
                    {
                        "text": "Resultado incompleto:",
                        "math": r"\text{Falta expresar } \theta \text{ y } \sin(2\theta) \text{ en términos de } x"
                    }
                ],
                "error_highlight": "Error: no regresar a variable original en sustitución trigonométrica",
                "error_id": "sustitucion-trigonometrica-sin-regreso"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Antiderivada inventada:",
                        "math": r"\int \sqrt{4 - x^{2}} \, dx = \frac{x^{3}}{3} + C"
                    },
                    {
                        "text": "Verificación falla:",
                        "math": r"\frac{d}{dx}[\frac{x^{3}}{3}] = x^{2} \neq \sqrt{4 - x^{2}}"
                    }
                ],
                "error_highlight": "Error: antiderivada inventada sin verificación matemática",
                "error_id": "integracion-partes-antiderivada-inventada"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Confusión con integral simple:",
                        "math": r"\int \sqrt{4 - x^{2}} \, dx = \frac{1}{2} x^{2} + C"
                    }
                ],
                "error_highlight": "Error: antiderivada inventada sin verificación matemática",
                "error_id": "integracion-partes-antiderivada-inventada"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Sustitución incorrecta:",
                        "math": r"x = 2 \tan(\theta), \quad dx = 2 \sec^{2}(\theta) \, d\theta"
                    },
                    {
                        "text": "Complica enormemente:",
                        "math": r"\int \sqrt{4 - 4 \tan^{2}(\theta)} \cdot 2 \sec^{2}(\theta) \, d\theta"
                    }
                ],
                "error_highlight": "Error: sustitución trigonométrica incorrecta (√(a² − x²) requiere sen o cos, no tan)",
                "error_id": "sustitucion-trigonometrica-incorrecta"
            }
        ]
    },
    {
        "question_latex": r"\int \frac{dx}{\sqrt{x^{2} - 9}}",
        "correct_answer": r"\ln|x + \sqrt{x^{2} - 9}| + C",
        "solution_steps": [
            {
                "text": "Forma √(x² − a²) con a = 3:",
                "math": r"\int \frac{dx}{\sqrt{x^{2} - 9}}"
            },
            {
                "text": "Sustitución trigonométrica:",
                "math": r"x = 3 \sec(\theta), \quad dx = 3 \sec(\theta) \tan(\theta) \, d\theta"
            },
            {
                "text": "Integral transformada:",
                "math": r"\int \frac{3 \sec(\theta) \tan(\theta)}{\sqrt{(3 \sec(\theta))^{2} - 9}} \, d\theta = \int \frac{3 \sec(\theta) \tan(\theta)}{\sqrt{9 \sec^{2}(\theta) - 9}} \, d\theta"
            },
            {
                "text": "Simplificamos:",
                "math": r"\int \frac{3 \sec(\theta) \tan(\theta)}{3 \sqrt{\sec^{2}(\theta) - 1}} \, d\theta = \int \frac{\sec(\theta) \tan(\theta)}{|\tan(\theta)|} \, d\theta"
            },
            {
                "text": "Resultado:",
                "math": r"\int \sec(\theta) \, d\theta = \ln|\sec(\theta) + \tan(\theta)| + C"
            },
            {
                "text": "Regresamos a x:",
                "math": r"\sec(\theta) = x/3, \quad \tan(\theta) = \sqrt{(x/3)^{2} - 1} = \sqrt{x^{2}/9 - 1} = \sqrt{(x^{2} - 9)/9}"
            },
            {
                "text": "Forma final:",
                "math": r"\ln|x + \sqrt{x^{2} - 9}| + C"
            }
        ],
        "choices_latex": [
            r"\ln|x + \sqrt{x^{2} - 9}| + C",
            r"\arcsin(x/3) + C",
            r"\frac{1}{3} \ln|x^{2} - 9| + C",
            r"x \sqrt{x^{2} - 9} + C",
            r"\sec^{-1}(x/3) + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Sustitución incorrecta para √(x² − a²):",
                        "math": r"x = 3 \sin(\theta), \quad dx = 3 \cos(\theta) \, d\theta"
                    },
                    {
                        "text": "Complica enormemente:",
                        "math": r"\int \frac{3 \cos(\theta)}{\sqrt{9 \sin^{2}(\theta) - 9}} \, d\theta"
                    }
                ],
                "error_highlight": "Error: sustitución trigonométrica incorrecta (√(x² − a²) requiere sec, no sen)",
                "error_id": "sustitucion-trigonometrica-incorrecta"
            },
            {
                "wrong_steps": [
                    {
                        "text": "No regresa a variable original:",
                        "math": r"\int \sec(\theta) \, d\theta = \ln|\sec(\theta) + \tan(\theta)| + C"
                    },
                    {
                        "text": "Resultado incompleto:",
                        "math": r"\text{Falta expresar en términos de } x"
                    }
                ],
                "error_highlight": "Error: no regresar a variable original en sustitución trigonométrica",
                "error_id": "sustitucion-trigonometrica-sin-regreso"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Antiderivada inventada:",
                        "math": r"\int \frac{dx}{\sqrt{x^{2} - 9}} = \frac{x}{3} + C"
                    },
                    {
                        "text": "Verificación falla:",
                        "math": r"\frac{d}{dx}[\frac{x}{3}] = \frac{1}{3} \neq \frac{1}{\sqrt{x^{2} - 9}}"
                    }
                ],
                "error_highlight": "Error: antiderivada inventada sin verificación matemática",
                "error_id": "integracion-partes-antiderivada-inventada"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Confusión con arcsin:",
                        "math": r"\int \frac{dx}{\sqrt{9 - x^{2}}} = \arcsin(x/3) + C"
                    },
                    {
                        "text": "Pero la integral es √(x² − 9), no √(9 − x²):",
                        "math": r"\arcsin(x/3) \text{ sería para } \sqrt{9 - x^{2}}"
                    }
                ],
                "error_highlight": "Error: confusión entre diferentes formas trigonométricas",
                "error_id": "sustitucion-trigonometrica-incorrecta",
            }
        ]
    },
    {
        "question_latex": r"\int \frac{x^{2} dx}{\sqrt{4 - x^{2}}}",
        "correct_answer": r"-\frac{x}{2} \sqrt{4 - x^{2}} + 2 \arcsin(x/2) + C",
        "solution_steps": [
            {
                "text": "Forma √(a² − x²) con a = 2:",
                "math": r"\int \frac{x^{2} dx}{\sqrt{4 - x^{2}}}"
            },
            {
                "text": "Usamos identidad trigonométrica:",
                "math": r"x^{2} = 4 - (4 - x^{2}) = 4 - (√(4 - x^{2}))^{2}"
            },
            {
                "text": "Sustitución trigonométrica:",
                "math": r"x = 2 \sin(\theta), \quad dx = 2 \cos(\theta) \, d\theta"
            },
            {
                "text": "Reescribimos:",
                "math": r"x^{2} = 4 \sin^{2}(\theta), \quad \sqrt{4 - x^{2}} = 2 \cos(\theta)"
            },
            {
                "text": "Integral transformada:",
                "math": r"\int \frac{4 \sin^{2}(\theta) \cdot 2 \cos(\theta)}{2 \cos(\theta)} \, d\theta = \int 4 \sin^{2}(\theta) \, d\theta"
            },
            {
                "text": "Usamos identidad:",
                "math": r"\sin^{2}(\theta) = \frac{1 - \cos(2\theta)}{2}"
            },
            {
                "text": "Resultado:",
                "math": r"\int 4 \cdot \frac{1 - \cos(2\theta)}{2} \, d\theta = \int 2(1 - \cos(2\theta)) \, d\theta = 2\theta - \sin(2\theta) + C"
            },
            {
                "text": "Regresamos a x:",
                "math": r"\theta = \arcsin(x/2), \quad \sin(2\theta) = 2 \sin\theta \cos\theta = 2 \cdot \frac{x}{2} \cdot \frac{\sqrt{4 - x^{2}}}{2} = \frac{x \sqrt{4 - x^{2}}}{2}"
            },
            {
                "text": "Forma final:",
                "math": r"2 \arcsin(x/2) - \frac{x \sqrt{4 - x^{2}}}{2} + C = -\frac{x}{2} \sqrt{4 - x^{2}} + 2 \arcsin(x/2) + C"
            }
        ],
        "choices_latex": [
            r"-\frac{x}{2} \sqrt{4 - x^{2}} + 2 \arcsin(x/2) + C",
            r"\frac{x^{3}}{3} + C",
            r"\arcsin(x/2) + C",
            r"2 \sqrt{4 - x^{2}} + C",
            r"\frac{1}{2} x^{2} + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "No regresa a variable original:",
                        "math": r"\int 4 \sin^{2}(\theta) \, d\theta = 2\theta - \sin(2\theta) + C"
                    },
                    {
                        "text": "Resultado incompleto:",
                        "math": r"\text{Falta expresar en términos de } x"
                    }
                ],
                "error_highlight": "Error: no regresar a variable original en sustitución trigonométrica",
                "error_id": "sustitucion-trigonometrica-sin-regreso"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Antiderivada inventada:",
                        "math": r"\int \frac{x^{2} dx}{\sqrt{4 - x^{2}}} = \frac{x^{3}}{3} + C"
                    },
                    {
                        "text": "Verificación falla:",
                        "math": r"\frac{d}{dx}[\frac{x^{3}}{3}] = x^{2} \neq \frac{x^{2}}{\sqrt{4 - x^{2}}}"
                    }
                ],
                "error_highlight": "Error: antiderivada inventada sin verificación matemática",
                "error_id": "integracion-partes-antiderivada-inventada"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Confusión con integral simple:",
                        "math": r"\int \frac{x^{2} dx}{\sqrt{4 - x^{2}}} = \frac{1}{2} x^{2} + C"
                    }
                ],
                "error_highlight": "Error: antiderivada inventada sin verificación matemática",
                "error_id": "integracion-partes-antiderivada-inventada"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Sustitución incorrecta:",
                        "math": r"x = 2 \tan(\theta), \quad dx = 2 \sec^{2}(\theta) \, d\theta"
                    },
                    {
                        "text": "Complica enormemente:",
                        "math": r"\int \frac{(2 \tan(\theta))^{2} \cdot 2 \sec^{2}(\theta)}{\sqrt{4 - 4 \tan^{2}(\theta)}} \, d\theta"
                    }
                ],
                "error_highlight": "Error: sustitución trigonométrica incorrecta (√(a² − x²) requiere sen o cos, no tan)",
                "error_id": "sustitucion-trigonometrica-incorrecta"
            }
        ]
    },
    # Integrales definidas impropias - Caso convergente simple
    {
        "question_latex": r"\int_{0}^{1} x^{-1/2} \, dx",
        "correct_answer": r"2",
        "solution_steps": [
            {
                "text": "Esta es una integral impropia tipo I en el límite inferior (x = 0):",
                "math": r"\int_{0}^{1} \frac{1}{\sqrt{x}} \, dx = \lim_{a \to 0^{+}} \int_{a}^{1} x^{-1/2} \, dx"
            },
            {
                "text": "Calculamos la antiderivada:",
                "math": r"\int x^{-1/2} \, dx = \int x^{-1/2} \, dx = 2x^{1/2} + C = 2\sqrt{x} + C"
            },
            {
                "text": "Aplicamos el Teorema Fundamental del Cálculo:",
                "math": r"\lim_{a \to 0^{+}} [2\sqrt{x}]_{a}^{1} = \lim_{a \to 0^{+}} (2\sqrt{1} - 2\sqrt{a}) = \lim_{a \to 0^{+}} (2 - 2\sqrt{a})"
            },
            {
                "text": "Evaluamos el límite:",
                "math": r"\lim_{a \to 0^{+}} (2 - 2\sqrt{a}) = 2 - 2 \cdot 0 = 2"
            },
            {
                "text": "Conclusión: la integral converge al valor 2",
                "math": r"\int_{0}^{1} x^{-1/2} \, dx = 2"
            }
        ],
        "choices_latex": [
            r"2",
            r"\infty",
            r"-\infty",
            r"0",
            r"1"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Error: evaluar la antiderivada sin considerar la impropiedad",
                        "math": r"\int_{0}^{1} x^{-1/2} \, dx = [2\sqrt{x}]_{0}^{1} = 2\sqrt{1} - 2\sqrt{0} = 2 - 0 = 2"
                    },
                    {
                        "text": "Esto parece correcto, pero ignora que √0 no está definido",
                        "math": r"\sqrt{0} = 0, \text{ pero la función no está definida en x = 0}"
                    }
                ],
                "error_highlight": "Error: olvido de analizar la impropiedad en x = 0",
                "error_id": "integral-impropia-ignora-impropiedad"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Error: ignorar el límite cuando x → 0⁺",
                        "math": r"\lim_{x \to 0^{+}} 2\sqrt{x} = 2 \cdot 0 = 0"
                    },
                    {
                        "text": "Concluir que la integral diverge a ∞",
                        "math": r"\int_{0}^{1} x^{-1/2} \, dx = \infty"
                    }
                ],
                "error_highlight": "Error: cálculo incorrecto del límite (lim x→0⁺ √x = 0, no ∞)",
                "error_id": "integral-impropia-algebra-log-mal"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Error: invertir los límites de evaluación",
                        "math": r"[2\sqrt{x}]_{1}^{0} = 2\sqrt{0} - 2\sqrt{1} = 0 - 2 = -2"
                    },
                    {
                        "text": "Concluir que converge a -2",
                        "math": r"\int_{0}^{1} x^{-1/2} \, dx = -2"
                    }
                ],
                "error_highlight": "Error: evaluación invertida de límites (F(a) - F(b) en lugar de F(b) - F(a))",
                "error_id": "integral-definida-limites-invertidos"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Calcular correctamente el límite:",
                        "math": r"\lim_{a \to 0^{+}} (2 - 2\sqrt{a}) = 2 - 0 = 2"
                    },
                    {
                        "text": "Error: concluir que diverge cuando converge",
                        "math": r"\int_{0}^{1} x^{-1/2} \, dx = \infty \quad (\text{incorrecto, converge a 2})"
                    }
                ],
                "error_highlight": "Error: conclusión errónea sobre convergencia/divergencia",
                "error_id": "integral-impropia-convergencia-mal-concluida"
            }
        ]
    },
    # Integrales definidas impropias - Caso divergente simple
    {
        "question_latex": r"\int_{1}^{2} \frac{1}{x - 1} \, dx",
        "correct_answer": r"\infty",
        "solution_steps": [
            {
                "text": "Esta es una integral impropia tipo II en el límite inferior (x = 1):",
                "math": r"\int_{1}^{2} \frac{1}{x - 1} \, dx = \lim_{a \to 1^{+}} \int_{a}^{2} \frac{1}{x - 1} \, dx"
            },
            {
                "text": "Calculamos la antiderivada:",
                "math": r"\int \frac{1}{x - 1} \, dx = \ln|x - 1| + C"
            },
            {
                "text": "Aplicamos el Teorema Fundamental del Cálculo:",
                "math": r"\lim_{a \to 1^{+}} [\ln|x - 1|]_{a}^{2} = \lim_{a \to 1^{+}} (\ln|2 - 1| - \ln|a - 1|)"
            },
            {
                "text": "Evaluamos el límite:",
                "math": r"\lim_{a \to 1^{+}} (\ln 1 - \ln(a - 1)) = \lim_{a \to 1^{+}} (0 - \ln(a - 1))"
            },
            {
                "text": "Como a → 1⁺, (a - 1) → 0⁺, entonces ln(a - 1) → -∞:",
                "math": r"\lim_{a \to 1^{+}} (0 - (-\infty)) = +\infty"
            },
            {
                "text": "Conclusión: la integral diverge",
                "math": r"\int_{1}^{2} \frac{1}{x - 1} \, dx = \infty"
            }
        ],
        "choices_latex": [
            r"\infty",
            r"1",
            r"0",
            r"\ln 2",
            r"-\infty"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Error: evaluar sin considerar la impropiedad",
                        "math": r"\int_{1}^{2} \frac{1}{x - 1} \, dx = [\ln|x - 1|]_{1}^{2} = \ln 1 - \ln 0"
                    },
                    {
                        "text": "Esto es indefinido porque ln(0) no existe",
                        "math": r"\ln 1 - \ln 0 = 0 - (-\infty) = +\infty"
                    }
                ],
                "error_highlight": "Error: olvido de analizar la impropiedad en x = 1",
                "error_id": "integral-definida-sin-evaluar-limites"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Calcular correctamente el límite:",
                        "math": r"\lim_{a \to 1^{+}} (\ln 1 - \ln(a - 1)) = \lim_{a \to 1^{+}} (0 - \ln(a - 1)) = +\infty"
                    },
                    {
                        "text": "Error: concluir que converge cuando diverge",
                        "math": r"\int_{1}^{2} \frac{1}{x - 1} \, dx = 1 \quad (\text{incorrecto, diverge})"
                    }
                ],
                "error_highlight": "Error: conclusión errónea sobre convergencia/divergencia",
                "error_id": "integral-impropia-convergencia-mal-concluida"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Error: invertir los límites de evaluación",
                        "math": r"[\ln|x - 1|]_{2}^{1} = \ln 0 - \ln 1 = -\infty - 0 = -\infty"
                    },
                    {
                        "text": "Concluir que diverge a -∞",
                        "math": r"\int_{1}^{2} \frac{1}{x - 1} \, dx = -\infty"
                    }
                ],
                "error_highlight": "Error: evaluación invertida de límites (F(a) - F(b) en lugar de F(b) - F(a))",
                "error_id": "integral-definida-limites-invertidos"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Error: ignorar el comportamiento cerca de x = 1",
                        "math": r"\lim_{x \to 1^{+}} \frac{1}{x - 1} = +\infty"
                    },
                    {
                        "text": "Concluir que la antiderivada existe en el límite",
                        "math": r"\int_{1}^{2} \frac{1}{x - 1} \, dx = \ln 2 \quad (\text{incorrecto})"
                    }
                ],
                "error_highlight": "Error: ignorar el límite cuando x → 1⁺ en la evaluación",
                "error_id": "integracion-partes-derivada-u"
            }
        ]
    },
]


def generate_dynamic_question(base_question_latex: str) -> Dict[str, Any]:
    """
    Genera un ejercicio dinámico basado en un ejercicio semilla usando LLM.

    Args:
        base_question_latex: LaTeX del ejercicio base

    Returns:
        Dict con la estructura completa del quiz instance generado dinámicamente
    """
    # Generar nuevo enunciado usando LLM
    new_question_latex = generate_week01_exercise(base_question_latex)

    # Usar un template base como estructura (tomamos el primero)
    quiz_templates = get_quiz_templates_for_week("week01")
    template = quiz_templates[0].copy()  # Usar estructura base

    # Reemplazar el enunciado con el generado dinámicamente
    template["question_latex"] = new_question_latex

    # Construir opciones con identificadores únicos (mantenemos la estructura)
    options = []

    # Opción correcta (usamos la estructura pero adaptamos)
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
        "question_latex": new_question_latex,
        "options": options,
        "solution_steps": template.get("solution_steps", []),
        "correct_answer": template.get("correct_answer", ""),
        "week_id": "week01",
        "is_dynamic": True,  # Marca que es generado dinámicamente
        "agent_trace": {
            "source": "llm",
            "model": "gemini-pro-latest"
        }
    }

    return quiz_instance


def get_another_question(current_question_latex: str) -> Dict[str, Any]:
    """
    Genera otro ejercicio dinámico basado en el ejercicio actual.

    Args:
        current_question_latex: LaTeX del ejercicio actual

    Returns:
        Dict con nuevo ejercicio generado dinámicamente
    """
    return generate_dynamic_question(current_question_latex)


def get_random_question(use_dynamic: bool = False, base_question: str = None) -> Dict[str, Any]:
    """
    Retorna una instancia aleatoria del quiz de Semana 1 con opciones mezcladas

    Args:
        use_dynamic: Si True, genera un ejercicio dinámico usando LLM
        base_question: Enunciado base para generar ejercicio dinámico (requerido si use_dynamic=True)

    Returns:
        Dict con la estructura completa del quiz instance
    """
    # Si se solicita ejercicio dinámico, usar LLM generator
    if use_dynamic and base_question:
        return generate_dynamic_question(base_question)

    # Obtener templates desde WeekSpec (mantiene backward compatibility)
    quiz_templates = get_quiz_templates_for_week("week01")

    # Seleccionar plantilla aleatoria
    template = random.choice(quiz_templates).copy()

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
        "week_id": "week01"  # Metadata para identificar la semana
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

        # Verificar que correct_index apunte al elemento correcto
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
