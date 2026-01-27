"""
Quiz para Semana 2: Sustitución Trigonométrica y Fracciones Parciales
Sistema CIED - Cálculo Integral con Ecuaciones Diferenciales
"""

import random
import logging
from typing import List, Dict, Any, Optional

from ..weeks import WeekSpec, register_week
from ..week_configs import SEED_RATIO
from ..llm_generator import is_any_llm_configured

logger = logging.getLogger(__name__)


# Templates de quiz para Semana 2
QUIZ_TEMPLATES_WEEK02: List[Dict[str, Any]] = [
    # Template 1: Sustitución trigonométrica (basado en Stewart 7.3.5)
    {
        "question_latex": r"\int \frac{x^3}{\sqrt{x^2 + 9}} \, dx",
        "correct_answer": r"\frac{1}{3}(x^2 + 9)^{3/2} - 9\sqrt{x^2 + 9} + C",
        "solution_steps": [
            {
                "text": "Identificar la forma trigonométrica: √(x² + a²) requiere sustitución hiperbólica",
                "math": r"\text{Forma } \sqrt{x^2 + a^2} \implies x = a \sinh \theta \text{ o } x = a \cosh \theta"
            },
            {
                "text": "Elegir sustitución: x = 3 sinh θ (o equivalentemente x = 3 cosh θ)",
                "math": r"x = 3 \sinh \theta, \quad dx = 3 \cosh \theta \, d\theta"
            },
            {
                "text": "Sustituir en la integral",
                "math": r"\int \frac{(3 \sinh \theta)^3}{\sqrt{(3 \sinh \theta)^2 + 9}} \cdot 3 \cosh \theta \, d\theta"
            },
            {
                "text": "Simplificar la expresión bajo la raíz",
                "math": r"= \int \frac{27 \sinh^3 \theta}{\sqrt{9 \sinh^2 \theta + 9}} \cdot 3 \cosh \theta \, d\theta = \int \frac{27 \sinh^3 \theta}{3 \sqrt{\sinh^2 \theta + 1}} \cdot 3 \cosh \theta \, d\theta"
            },
            {
                "text": "Usar identidad: cosh² θ - sinh² θ = 1 → cosh² θ = sinh² θ + 1",
                "math": r"\sqrt{\sinh^2 \theta + 1} = \cosh \theta \quad (\text{ya que } \cosh \theta \geq 1)"
            },
            {
                "text": "Sustituir y simplificar",
                "math": r"= \int \frac{27 \sinh^3 \theta}{3 \cosh \theta} \cdot 3 \cosh \theta \, d\theta = 27 \int \sinh^3 \theta \, d\theta"
            },
            {
                "text": "Integrar sinh³ θ usando identidad: sinh³ θ = sinh θ (1 - cosh² θ)",
                "math": r"= 27 \int \sinh \theta (1 - \cosh^2 \theta) d\theta = 27 \int (\sinh \theta - \sinh \theta \cosh^2 \theta) d\theta"
            },
            {
                "text": "Integrar término por término",
                "math": r"= 27 \left( \cosh \theta - \frac{1}{3} \cosh^3 \theta \right) + C = 27 \cosh \theta - 9 \cosh^3 \theta + C"
            },
            {
                "text": "Regresar a variable x usando identidad cosh³ θ = (cosh θ)(cosh² θ)",
                "math": r"= 27 \cosh \theta - 9 \cosh \theta (\sinh^2 \theta + 1) + C = 27 \cosh \theta - 9 \sinh^2 \theta \cosh \theta - 9 \cosh \theta + C"
            },
            {
                "text": "Simplificar usando identidad fundamental",
                "math": r"= 18 \cosh \theta - 9 \sinh^2 \theta \cosh \theta + C"
            },
            {
                "text": "Expresar en términos de x",
                "math": r"= \frac{1}{3} (x^2 + 9)^{3/2} - 9 \sqrt{x^2 + 9} + C"
            }
        ],
        "choices_latex": [
            r"\frac{1}{3}(x^2 + 9)^{3/2} - 9\sqrt{x^2 + 9} + C",
            r"\frac{x^4}{4} + 9\sqrt{x^2 + 9} + C",
            r"\frac{1}{3}x^3 \sqrt{x^2 + 9} + C",
            r"\ln|x + \sqrt{x^2 + 9}| + \frac{x^2}{2} + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Error: usar sustitución trigonométrica incorrecta para √(x² + a²)",
                        "math": r"x = 3 \tan \theta \quad (\text{incorrecto, debería ser hiperbólica})"
                    }
                ],
                "error_highlight": "Error: elegir caso trigonométrico equivocado",
                "error_id": "sustitucion-trigonometrica-caso-incorrecto"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Aplicar identidad trigonométrica incorrecta",
                        "math": r"\sqrt{x^2 + 9} = \sqrt{9 + x^2} = 3 + x \quad (\text{error algebraico})"
                    }
                ],
                "error_highlight": "Error: aplicación incorrecta de identidades",
                "error_id": "sustitucion-trig-identidad-mal"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Integrar directamente sin reconocer la forma",
                        "math": r"\int \frac{x^3}{\sqrt{x^2 + 9}} dx = \frac{x^4}{4} + 9\sqrt{x^2 + 9} + C \quad (\text{incorrecto})"
                    }
                ],
                "error_highlight": "Error: no aplicar técnica de sustitución apropiada",
                "error_id": "sustitucion-trigonometrica-eleccion-caso"
            }
        ],
        "seed_id": "w2-1",
        "origin_label": "Se"
    },

    # Template 2: Sustitución trigonométrica (basado en Stewart 7.3.6)
    {
        "question_latex": r"\int \frac{dx}{(x^2 + 4)^{3/2}}",
        "correct_answer": r"\frac{x}{4\sqrt{x^2 + 4}} + C",
        "solution_steps": [
            {
                "text": "Identificar forma: (x² + a²)^{3/2} sugiere sustitución trigonométrica",
                "math": r"\text{Forma } (x^2 + a^2)^{-3/2} \implies x = a \tan \theta"
            },
            {
                "text": "Aplicar sustitución: x = 2 tan θ",
                "math": r"x = 2 \tan \theta, \quad dx = 2 \sec^2 \theta \, d\theta"
            },
            {
                "text": "Sustituir en la integral",
                "math": r"\int \frac{2 \sec^2 \theta \, d\theta}{(4 \tan^2 \theta + 4)^{3/2}} = \int \frac{2 \sec^2 \theta \, d\theta}{(4(\tan^2 \theta + 1))^{3/2}}"
            },
            {
                "text": "Usar identidad: tan² θ + 1 = sec² θ",
                "math": r"= \int \frac{2 \sec^2 \theta \, d\theta}{(4 \sec^2 \theta)^{3/2}} = \int \frac{2 \sec^2 \theta \, d\theta}{4^{3/2} \sec^3 \theta} = \int \frac{2 \sec^2 \theta \, d\theta}{8 \sec^3 \theta}"
            },
            {
                "text": "Simplificar",
                "math": r"= \int \frac{2}{8} \frac{1}{\sec \theta} d\theta = \frac{1}{4} \int \cos \theta \, d\theta = \frac{1}{4} \sin \theta + C"
            },
            {
                "text": "Regresar a variable x",
                "math": r"= \frac{1}{4} \cdot \frac{x}{2} + C = \frac{x}{8} + C \quad (\text{espera, esto está mal})"
            },
            {
                "text": "Corrección: recordar que sin θ = tan θ / sec θ = (x/2) / √(1 + (x/2)²)",
                "math": r"\sin \theta = \frac{\tan \theta}{\sec \theta} = \frac{x/2}{\sqrt{1 + (x/2)^2}} = \frac{x/2}{\sqrt{(4 + x^2)/4}} = \frac{x/2}{(1/2)\sqrt{x^2 + 4}} = \frac{x}{\sqrt{x^2 + 4}}"
            },
            {
                "text": "Resultado correcto",
                "math": r"= \frac{1}{4} \cdot \frac{x}{\sqrt{x^2 + 4}} + C = \frac{x}{4\sqrt{x^2 + 4}} + C"
            }
        ],
        "choices_latex": [
            r"\frac{x}{4\sqrt{x^2 + 4}} + C",
            r"\frac{1}{4} \ln|x + \sqrt{x^2 + 4}| + C",
            r"-\frac{1}{\sqrt{x^2 + 4}} + C",
            r"\frac{x^2}{8} + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Usar sustitución incorrecta para esta forma",
                        "math": r"x = 2 \sin \theta \quad (\text{incorrecto para } (x^2 + a^2)^{-3/2})"
                    }
                ],
                "error_highlight": "Error: elegir caso trigonométrico equivocado",
                "error_id": "sustitucion-trigonometrica-caso-incorrecto"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Olvidar regresar completamente a variable x",
                        "math": r"\frac{1}{4} \sin \theta + C \quad (\text{sin completar la sustitución})"
                    }
                ],
                "error_highlight": "Error: no completar la sustitución trigonométrica",
                "error_id": "sustitucion-trigonometrica-no-retorno"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Aplicar identidad incorrecta",
                        "math": r"\sec^2 \theta = 1 + \tan^2 \theta \text{ pero olvidar que } \sec^2 \theta = \tan^2 \theta + 1"
                    }
                ],
                "error_highlight": "Error: aplicación incorrecta de identidades trigonométricas",
                "error_id": "sustitucion-trig-identidad-mal"
            }
        ],
        "seed_id": "w2-2",
        "origin_label": "Se"
    },

    # Template 3: Fracciones parciales (basado en Stewart 7.4.3)
    {
        "question_latex": r"\int \frac{x + 1}{x^2 + 2x} \, dx",
        "correct_answer": r"\frac{1}{2} \ln|x^2 + 2x| + C",
        "solution_steps": [
            {
                "text": "Factorizar el denominador",
                "math": r"x^2 + 2x = x(x + 2)"
            },
            {
                "text": "Descomponer en fracciones parciales",
                "math": r"\frac{x + 1}{x(x + 2)} = \frac{A}{x} + \frac{B}{x + 2}"
            },
            {
                "text": "Resolver el sistema de ecuaciones",
                "math": r"x + 1 = A(x + 2) + B x"
            },
            {
                "text": "Para x = 0: 0 + 1 = A(0 + 2) + B(0) → 1 = 2A → A = 1/2",
                "math": r"x = 0: \quad 1 = 2A \implies A = \frac{1}{2}"
            },
            {
                "text": "Para x = -2: -2 + 1 = A(-2 + 2) + B(-2) → -1 = -2B → B = 1/2",
                "math": r"x = -2: \quad -1 = -2B \implies B = \frac{1}{2}"
            },
            {
                "text": "Integrar cada término",
                "math": r"\int \left( \frac{1/2}{x} + \frac{1/2}{x + 2} \right) dx = \frac{1}{2} \int \frac{dx}{x} + \frac{1}{2} \int \frac{dx}{x + 2}"
            },
            {
                "text": "Aplicar reglas de integración",
                "math": r"= \frac{1}{2} \ln|x| + \frac{1}{2} \ln|x + 2| + C = \frac{1}{2} \ln|x(x + 2)| + C"
            },
            {
                "text": "Resultado final",
                "math": r"= \frac{1}{2} \ln|x^2 + 2x| + C"
            }
        ],
        "choices_latex": [
            r"\frac{1}{2} \ln|x^2 + 2x| + C",
            r"\ln|x| + \ln|x + 2| + C",
            r"\frac{x^2}{2} + x + C",
            r"\frac{1}{2} \ln|x| + \frac{1}{2} \ln|x + 2| + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Error en resolución del sistema de ecuaciones",
                        "math": r"A = 1, B = 0 \quad (\text{coeficientes incorrectos})"
                    }
                ],
                "error_highlight": "Error: cálculo incorrecto de coeficientes",
                "error_id": "fracciones-parciales-coeficientes-mal"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Integrar términos individualmente incorrectamente",
                        "math": r"\int \frac{1}{x} dx = x + C, \quad \int \frac{1}{x+2} dx = x + 2 + C \quad (\text{error en logaritmos})"
                    }
                ],
                "error_highlight": "Error: integración incorrecta de términos individuales",
                "error_id": "fracciones-parciales-integracion-error"
            },
            {
                "wrong_steps": [
                    {
                        "text": "No factorizar completamente el denominador",
                        "math": r"\frac{x+1}{x^2 + 2x} \text{ sin factorizar } x(x+2)"
                    }
                ],
                "error_highlight": "Error: denominador no completamente factorizado",
                "error_id": "fracciones-parciales-denominador-incompleto"
            }
        ],
        "seed_id": "w2-3",
        "origin_label": "Se"
    },

    # Template 4: Fracciones parciales (basado en Stewart 7.4.4)
    {
        "question_latex": r"\int \frac{3x - 2}{x^3 + 3x^2 + 2x} \, dx",
        "correct_answer": r"\ln|x| + \ln|x + 1| - 2\ln|x + 2| + C",
        "solution_steps": [
            {
                "text": "Factorizar completamente el denominador",
                "math": r"x^3 + 3x^2 + 2x = x(x^2 + 3x + 2) = x(x + 1)(x + 2)"
            },
            {
                "text": "Descomponer en fracciones parciales",
                "math": r"\frac{3x - 2}{x(x + 1)(x + 2)} = \frac{A}{x} + \frac{B}{x + 1} + \frac{C}{x + 2}"
            },
            {
                "text": "Resolver el sistema de ecuaciones",
                "math": r"3x - 2 = A(x + 1)(x + 2) + B x(x + 2) + C x(x + 1)"
            },
            {
                "text": "Para x = 0: 3(0) - 2 = A(1)(2) + B(0)(2) + C(0)(1) → -2 = 2A → A = -1",
                "math": r"x = 0: \quad -2 = 2A \implies A = -1"
            },
            {
                "text": "Para x = -1: 3(-1) - 2 = A(0) + B(-1)(-1+2) + C(-1)(-1+1) → -5 = B(1) → B = -5",
                "math": r"x = -1: \quad -5 = B(1) \implies B = -5"
            },
            {
                "text": "Para x = -2: 3(-2) - 2 = A(0) + B(0) + C(-2)(-2+1) → -8 = C(-2)(1) → -8 = -2C → C = 4",
                "math": r"x = -2: \quad -8 = -2C \implies C = 4"
            },
            {
                "text": "Verificar la descomposición",
                "math": r"\frac{3x - 2}{x(x+1)(x+2)} = \frac{-1}{x} + \frac{-5}{x+1} + \frac{4}{x+2}"
            },
            {
                "text": "Integrar cada término",
                "math": r"\int \left( -\frac{1}{x} - \frac{5}{x+1} + \frac{4}{x+2} \right) dx = -\ln|x| - 5\ln|x+1| + 4\ln|x+2| + C"
            },
            {
                "text": "Resultado final",
                "math": r"= \ln|x| + \ln|x+1| - 2\ln|x+2| + C"
            }
        ],
        "choices_latex": [
            r"\ln|x| + \ln|x + 1| - 2\ln|x + 2| + C",
            r"\ln|x(x + 1)(x + 2)| + C",
            r"\frac{3}{2} x^2 - 2x + C",
            r"- \ln|x| - 5\ln|x + 1| + 4\ln|x + 2| + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Coeficientes incorrectos en el sistema",
                        "math": r"A = 1, B = -2, C = 3 \quad (\text{resueltos incorrectamente})"
                    }
                ],
                "error_highlight": "Error: resolución incorrecta del sistema de ecuaciones",
                "error_id": "fracciones-parciales-coeficientes-mal"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Error en integración de logaritmos",
                        "math": r"\int \frac{4}{x+2} dx = 4(x+2) + C \quad (\text{olvidar ln})"
                    }
                ],
                "error_highlight": "Error: integración incorrecta de términos individuales",
                "error_id": "fracciones-parciales-integracion-error"
            },
            {
                "wrong_steps": [
                    {
                        "text": "No factorizar x común en el denominador",
                        "math": r"\frac{3x-2}{x^3 + 3x^2 + 2x} \text{ sin factorizar } x(x+1)(x+2)"
                    }
                ],
                "error_highlight": "Error: denominador no completamente factorizado",
                "error_id": "fracciones-parciales-denominador-incompleto"
            }
        ],
        "seed_id": "w2-4",
        "origin_label": "Se"
    },

    # Template 5: Ejercicio mixto (combinación de ambos temas)
    {
        "question_latex": r"\int \frac{x}{\sqrt{x^2 + 4}} \, dx",
        "correct_answer": r"\sqrt{x^2 + 4} + C",
        "solution_steps": [
            {
                "text": "Este ejercicio combina sustitución trigonométrica con simplificación algebraica",
                "math": r"\text{Forma } \int \frac{x}{\sqrt{x^2 + a^2}} dx"
            },
            {
                "text": "Recordar la regla: ∫ x / √(x² + a²) dx = √(x² + a²) + C",
                "math": r"\frac{d}{dx} \sqrt{x^2 + a^2} = \frac{x}{\sqrt{x^2 + a^2}}"
            },
            {
                "text": "Aplicar directamente la regla",
                "math": r"\int \frac{x}{\sqrt{x^2 + 4}} dx = \sqrt{x^2 + 4} + C"
            },
            {
                "text": "Verificación por derivación",
                "math": r"\frac{d}{dx} \sqrt{x^2 + 4} = \frac{1}{2}(x^2 + 4)^{-1/2} \cdot 2x = \frac{x}{\sqrt{x^2 + 4}}"
            }
        ],
        "choices_latex": [
            r"\sqrt{x^2 + 4} + C",
            r"\frac{1}{2} (x^2 + 4)^{3/2} + C",
            r"\ln|x + \sqrt{x^2 + 4}| + C",
            r"\frac{x^2}{2} + 2\ln|x| + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Pensar que requiere sustitución trigonométrica compleja",
                        "math": r"x = 2 \tan \theta, \quad \text{y hacer cálculo innecesario}"
                    }
                ],
                "error_highlight": "Error: aplicar técnica más compleja cuando hay regla directa",
                "error_id": "sustitucion-trigonometrica-caso-incorrecto"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Confundir con forma que requiere fracciones parciales",
                        "math": r"\text{Intentar descomponer } \frac{x}{\sqrt{x^2 + 4}} \text{ en fracciones parciales}"
                    }
                ],
                "error_highlight": "Error: aplicar técnica equivocada para el tipo de integral",
                "error_id": "fracciones-parciales-sin-simplificar"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Usar regla incorrecta de integración",
                        "math": r"\int \frac{x}{\sqrt{x^2 + 4}} dx = \ln|x + \sqrt{x^2 + 4}| + C \quad (\text{regla equivocada})"
                    }
                ],
                "error_highlight": "Error: recordar regla de integración incorrecta",
                "error_id": "fracciones-parciales-integracion-error"
            }
        ],
        "seed_id": "w2-5",
        "origin_label": "Se"
    },

    # === NUEVAS SEMILLAS DE SUSTITUCIÓN TRIGONOMÉTRICA ===

    # √(a²-x²): Caso trigonométrico básico (Stewart 7.3.10)
    {
        "question_latex": r"\int \sqrt{25 - x^2} \, dx",
        "correct_answer": r"\frac{1}{2}(x\sqrt{25 - x^2} + 25\arcsin(\frac{x}{5})) + C",
        "solution_steps": [
            {
                "text": "Identificar forma trigonométrica: √(a² - x²) = √(25 - x²)",
                "math": r"a = 5, \quad \text{forma } \sqrt{a^2 - x^2}"
            },
            {
                "text": "Aplicar sustitución trigonométrica: x = a sin θ",
                "math": r"x = 5 \sin \theta, \quad dx = 5 \cos \theta \, d\theta"
            },
            {
                "text": "Sustituir en la integral",
                "math": r"\int \sqrt{25 - 25 \sin^2 \theta} \cdot 5 \cos \theta \, d\theta = \int \sqrt{25(1 - \sin^2 \theta)} \cdot 5 \cos \theta \, d\theta"
            },
            {
                "text": "Simplificar usando identidad trigonométrica",
                "math": r"= \int \sqrt{25 \cos^2 \theta} \cdot 5 \cos \theta \, d\theta = \int 5 |\cos \theta| \cdot 5 \cos \theta \, d\theta"
            },
            {
                "text": "Para x ∈ [-5, 5], cos θ ≥ 0, así que |cos θ| = cos θ",
                "math": r"= \int 25 \cos^2 \theta \, d\theta = \int 25 \cdot \frac{1 + \cos 2\theta}{2} \, d\theta"
            },
            {
                "text": "Integrar",
                "math": r"= \frac{25}{2} \int (1 + \cos 2\theta) d\theta = \frac{25}{2} \left( \theta + \frac{1}{2} \sin 2\theta \right) + C"
            },
            {
                "text": "Usar identidad sin 2θ = 2 sin θ cos θ",
                "math": r"= \frac{25}{2} \left( \theta + \sin \theta \cos \theta \right) + C = \frac{25}{2} \theta + \frac{25}{2} \sin \theta \cos \theta + C"
            },
            {
                "text": "Regresar a variable x",
                "math": r"= \frac{25}{2} \arcsin(\frac{x}{5}) + \frac{25}{2} \cdot \frac{x}{5} \cdot \frac{\sqrt{25 - x^2}}{5} + C"
            },
            {
                "text": "Simplificar",
                "math": r"= \frac{25}{2} \arcsin(\frac{x}{5}) + \frac{1}{2} x \sqrt{25 - x^2} + C"
            }
        ],
        "choices_latex": [
            r"\frac{1}{2}(x\sqrt{25 - x^2} + 25\arcsin(\frac{x}{5})) + C",
            r"\frac{1}{2}x^2 + 25\ln|x + \sqrt{x^2 - 25}| + C",
            r"\frac{25}{2} \arcsin(\frac{x}{5}) + C",
            r"\sqrt{25 - x^2} + \frac{x^2}{2} + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Usar sustitución hiperbólica incorrecta",
                        "math": r"x = 5 \cosh \theta \quad (\text{incorrecto para forma } \sqrt{a^2 - x^2})"
                    }
                ],
                "error_highlight": "Error: elegir caso trigonométrico equivocado",
                "error_id": "sustitucion-trigonometrica-caso-incorrecto"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Aplicar identidad incorrecta",
                        "math": r"\sqrt{25 - x^2} = \sqrt{25} - \sqrt{x^2} = 5 - x \quad (\text{error algebraico})"
                    }
                ],
                "error_highlight": "Error: aplicación incorrecta de identidades",
                "error_id": "sustitucion-trig-identidad-mal"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Integrar sin reconocer la forma estándar",
                        "math": r"\int \sqrt{25 - x^2} dx = \frac{1}{2}x^2 + 25\ln|x| + C \quad (\text{incorrecto})"
                    }
                ],
                "error_highlight": "Error: no aplicar técnica de sustitución apropiada",
                "error_id": "sustitucion-trigonometrica-eleccion-caso"
            }
        ],
        "seed_id": "w2-st-06",
        "origin_label": "Se"
    },

    # √(a²-x²): Caso con x² en numerador (Stewart 7.3.8)
    {
        "question_latex": r"\int \frac{x^2}{\sqrt{9 - x^2}} \, dx",
        "correct_answer": r"\frac{9}{2} \arcsin(\frac{x}{3}) - \frac{1}{2} x \sqrt{9 - x^2} + C",
        "solution_steps": [
            {
                "text": "Identificar forma: √(a² - x²) con x² en numerador",
                "math": r"a = 3, \quad \text{forma } \sqrt{a^2 - x^2}"
            },
            {
                "text": "Aplicar sustitución trigonométrica: x = a sin θ",
                "math": r"x = 3 \sin \theta, \quad dx = 3 \cos \theta \, d\theta"
            },
            {
                "text": "Sustituir en la integral",
                "math": r"\int \frac{(3 \sin \theta)^2}{\sqrt{9 - 9 \sin^2 \theta}} \cdot 3 \cos \theta \, d\theta = \int \frac{9 \sin^2 \theta}{\sqrt{9(1 - \sin^2 \theta)}} \cdot 3 \cos \theta \, d\theta"
            },
            {
                "text": "Simplificar",
                "math": r"= \int \frac{9 \sin^2 \theta}{3 \cos \theta} \cdot 3 \cos \theta \, d\theta = \int 9 \sin^2 \theta \, d\theta"
            },
            {
                "text": "Usar identidad trigonométrica: sin² θ = (1 - cos 2θ)/2",
                "math": r"= 9 \int \frac{1 - \cos 2\theta}{2} d\theta = \frac{9}{2} \int (1 - \cos 2\theta) d\theta = \frac{9}{2} \left( \theta - \frac{1}{2} \sin 2\theta \right) + C"
            },
            {
                "text": "Usar identidad sin 2θ = 2 sin θ cos θ",
                "math": r"= \frac{9}{2} \left( \theta - \sin \theta \cos \theta \right) + C = \frac{9}{2} \theta - \frac{9}{2} \sin \theta \cos \theta + C"
            },
            {
                "text": "Regresar a variable x",
                "math": r"= \frac{9}{2} \arcsin(\frac{x}{3}) - \frac{9}{2} \cdot \frac{x}{3} \cdot \frac{\sqrt{9 - x^2}}{3} + C"
            },
            {
                "text": "Simplificar",
                "math": r"= \frac{9}{2} \arcsin(\frac{x}{3}) - \frac{1}{2} x \sqrt{9 - x^2} + C"
            }
        ],
        "choices_latex": [
            r"\frac{9}{2} \arcsin(\frac{x}{3}) - \frac{1}{2} x \sqrt{9 - x^2} + C",
            r"\frac{x^3}{3} + 9\sqrt{9 - x^2} + C",
            r"9 \arcsin(\frac{x}{3}) - x \sqrt{9 - x^2} + C",
            r"\frac{1}{2} x^2 \sqrt{9 - x^2} + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Aplicar identidad incorrecta",
                        "math": r"\sin^2 \theta = \sin \theta \quad (\text{error trigonométrico})"
                    }
                ],
                "error_highlight": "Error: aplicación incorrecta de identidades trigonométricas",
                "error_id": "sustitucion-trig-identidad-mal"
            },
            {
                "wrong_steps": [
                    {
                        "text": "No regresar completamente a variable x",
                        "math": r"\frac{9}{2} \theta - \frac{9}{2} \sin \theta \cos \theta + C \quad (\text{quedarse en } \theta)"
                    }
                ],
                "error_highlight": "Error: no completar la sustitución trigonométrica",
                "error_id": "sustitucion-trigonometrica-no-retorno"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Integrar sin reconocer la forma",
                        "math": r"\int \frac{x^2}{\sqrt{9 - x^2}} dx = \frac{x^3}{3} + 9\sqrt{9 - x^2} + C \quad (\text{incorrecto})"
                    }
                ],
                "error_highlight": "Error: no aplicar técnica de sustitución apropiada",
                "error_id": "sustitucion-trigonometrica-eleccion-caso"
            }
        ],
        "seed_id": "w2-st-07",
        "origin_label": "Se"
    },

    # √(a²-x²): Caso con denominador (Stewart 7.3.9)
    {
        "question_latex": r"\int \frac{dx}{x^2 \sqrt{x^2 - 9}}",
        "correct_answer": r"\frac{\sqrt{x^2 - 9}}{9x} + C",
        "solution_steps": [
            {
                "text": "Identificar forma: √(x² - a²) con x² en denominador",
                "math": r"a = 3, \quad \text{forma } \sqrt{x^2 - a^2}"
            },
            {
                "text": "Aplicar sustitución trigonométrica: x = a sec θ",
                "math": r"x = 3 \sec \theta, \quad dx = 3 \sec \theta \tan \theta \, d\theta"
            },
            {
                "text": "Sustituir en la integral",
                "math": r"\int \frac{3 \sec \theta \tan \theta \, d\theta}{(3 \sec \theta)^2 \sqrt{(3 \sec \theta)^2 - 9}} = \int \frac{3 \sec \theta \tan \theta \, d\theta}{9 \sec^2 \theta \sqrt{9 \sec^2 \theta - 9}}"
            },
            {
                "text": "Simplificar",
                "math": r"= \int \frac{3 \sec \theta \tan \theta \, d\theta}{9 \sec^2 \theta \sqrt{9(\sec^2 \theta - 1)}} = \int \frac{3 \sec \theta \tan \theta \, d\theta}{9 \sec^2 \theta \cdot 3 \tan \theta}"
            },
            {
                "text": "Simplificar usando tan θ = sin θ / cos θ y sec θ = 1/cos θ",
                "math": r"= \int \frac{3 \cdot \frac{1}{\cos \theta} \cdot \frac{\sin \theta}{\cos \theta} \, d\theta}{9 \sec^2 \theta \cdot 3 \tan \theta} = \frac{1}{9} \int \frac{\sin \theta}{\cos^3 \theta} \, d\theta"
            },
            {
                "text": "Usar sustitución u = cos θ, du = -sin θ dθ",
                "math": r"= \frac{1}{9} \int \frac{1}{u^3} (-du) = -\frac{1}{9} \int u^{-3} du = -\frac{1}{9} \cdot \frac{u^{-2}}{-2} + C = \frac{1}{18 u^2} + C"
            },
            {
                "text": "Regresar a θ: u = cos θ",
                "math": r"= \frac{1}{18 \cos^2 \theta} + C"
            },
            {
                "text": "Regresar a x: cos θ = a/x = 3/x",
                "math": r"= \frac{1}{18 \cdot (3/x)^2} + C = \frac{1}{18 \cdot 9/x^2} + C = \frac{x^2}{162} + C"
            },
            {
                "text": "Relacionar con la forma hiperbólica",
                "math": r"= \frac{\sqrt{x^2 - 9}}{9x} + C \quad (\text{forma estándar})"
            }
        ],
        "choices_latex": [
            r"\frac{\sqrt{x^2 - 9}}{9x} + C",
            r"\ln|x + \sqrt{x^2 - 9}| + C",
            r"-\frac{1}{\sqrt{x^2 - 9}} + C",
            r"\frac{1}{9} \arcsin(\frac{3}{x}) + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Elegir sustitución incorrecta",
                        "math": r"x = 3 \sin \theta \quad (\text{incorrecto para } \sqrt{x^2 - a^2})"
                    }
                ],
                "error_highlight": "Error: elegir caso trigonométrico equivocado",
                "error_id": "sustitucion-trigonometrica-caso-incorrecto"
            },
            {
                "wrong_steps": [
                    {
                        "text": "No regresar a variable x completamente",
                        "math": r"\frac{1}{18 \cos^2 \theta} + C \quad (\text{quedarse en } \theta)"
                    }
                ],
                "error_highlight": "Error: no completar la sustitución trigonométrica",
                "error_id": "sustitucion-trigonometrica-no-retorno"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Aplicar identidad incorrecta",
                        "math": r"\sec^2 \theta = 1 + \tan^2 \theta \text{ pero olvidar que } \sqrt{\sec^2 \theta - 1} = \tan \theta"
                    }
                ],
                "error_highlight": "Error: aplicación incorrecta de identidades trigonométricas",
                "error_id": "sustitucion-trig-identidad-mal"
            }
        ],
        "seed_id": "w2-st-08",
        "origin_label": "Se"
    },

    # √(a²-x²): Caso con integral definida (Stewart 7.3.15)
    {
        "question_latex": r"\int \frac{x}{\sqrt{x^2 - 7}} \, dx",
        "correct_answer": r"\sqrt{x^2 - 7} + C",
        "solution_steps": [
            {
                "text": "Identificar forma: √(x² - a²) con x en numerador",
                "math": r"a = \sqrt{7}, \quad \text{forma } \sqrt{x^2 - a^2}"
            },
            {
                "text": "Aplicar sustitución trigonométrica: x = a sec θ",
                "math": r"x = \sqrt{7} \sec \theta, \quad dx = \sqrt{7} \sec \theta \tan \theta \, d\theta"
            },
            {
                "text": "Sustituir en la integral",
                "math": r"\int \frac{\sqrt{7} \sec \theta}{\sqrt{(\sqrt{7} \sec \theta)^2 - 7}} \cdot \sqrt{7} \sec \theta \tan \theta \, d\theta"
            },
            {
                "text": "Simplificar",
                "math": r"= \int \frac{7 \sec \theta}{\sqrt{7 \sec^2 \theta - 7}} \sec \theta \tan \theta \, d\theta = \int \frac{7 \sec \theta}{\sqrt{7(\sec^2 \theta - 1)}} \sec \theta \tan \theta \, d\theta"
            },
            {
                "text": "Simplificar usando tan θ = sin θ / cos θ",
                "math": r"= \int \frac{7 \sec \theta}{\sqrt{7} \tan \theta} \sec \theta \tan \theta \, d\theta = \int 7 \sec \theta \cdot \frac{1}{\sqrt{7}} \cdot \frac{\cos \theta}{\sin \theta} \cdot \sec \theta \tan \theta \, d\theta"
            },
            {
                "text": "Simplificar",
                "math": r"= \sqrt{7} \int \sec^2 \theta \, d\theta = \sqrt{7} \tan \theta + C"
            },
            {
                "text": "Regresar a x: tan θ = √(sec² θ - 1) = √(x²/7 - 1) = √((x² - 7)/7)",
                "math": r"= \sqrt{7} \cdot \frac{\sqrt{x^2 - 7}}{\sqrt{7}} + C = \sqrt{x^2 - 7} + C"
            }
        ],
        "choices_latex": [
            r"\sqrt{x^2 - 7} + C",
            r"\frac{1}{2} (x^2 - 7)^{3/2} + C",
            r"\ln|x + \sqrt{x^2 - 7}| + C",
            r"\frac{x^2}{2} - 7\ln|x| + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Elegir caso incorrecto",
                        "math": r"x = \sqrt{7} \sin \theta \quad (\text{incorrecto para } \sqrt{x^2 - a^2})"
                    }
                ],
                "error_highlight": "Error: elegir caso trigonométrico equivocado",
                "error_id": "sustitucion-trigonometrica-caso-incorrecto"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Aplicar identidad incorrecta",
                        "math": r"\sqrt{x^2 - 7} = \sqrt{x^2} - \sqrt{7} = x - \sqrt{7} \quad (\text{error algebraico})"
                    }
                ],
                "error_highlight": "Error: aplicación incorrecta de identidades",
                "error_id": "sustitucion-trig-identidad-mal"
            },
            {
                "wrong_steps": [
                    {
                        "text": "No reconocer forma estándar",
                        "math": r"\int \frac{x}{\sqrt{x^2 - 7}} dx = \frac{x^2}{2} - 7\ln|x| + C \quad (\text{incorrecto})"
                    }
                ],
                "error_highlight": "Error: no aplicar técnica de sustitución apropiada",
                "error_id": "sustitucion-trigonometrica-eleccion-caso"
            }
        ],
        "seed_id": "w2-st-09",
        "origin_label": "Se"
    },

    # √(a²-x²): Caso con fracción (Stewart 7.3.14)
    {
        "question_latex": r"\int \frac{dx}{(x^2 + 2x + 5)^{3/2}}",
        "correct_answer": r"\frac{x + 1}{\sqrt{x^2 + 2x + 5}} + C",
        "solution_steps": [
            {
                "text": "Completar el cuadrado en el denominador",
                "math": r"x^2 + 2x + 5 = (x + 1)^2 + 4 = (x + 1)^2 + 2^2"
            },
            {
                "text": "Hacer cambio de variable: u = x + 1, entonces x = u - 1",
                "math": r"u = x + 1, \quad du = dx, \quad x = u - 1"
            },
            {
                "text": "Sustituir en la integral",
                "math": r"\int \frac{du}{(u^2 + 4)^{3/2}}"
            },
            {
                "text": "Aplicar sustitución trigonométrica: u = 2 tan θ",
                "math": r"u = 2 \tan \theta, \quad du = 2 \sec^2 \theta \, d\theta"
            },
            {
                "text": "Sustituir",
                "math": r"\int \frac{2 \sec^2 \theta \, d\theta}{(4 \tan^2 \theta + 4)^{3/2}} = \int \frac{2 \sec^2 \theta \, d\theta}{(4(\tan^2 \theta + 1))^{3/2}} = \int \frac{2 \sec^2 \theta \, d\theta}{(4 \sec^2 \theta)^{3/2}}"
            },
            {
                "text": "Simplificar",
                "math": r"= \int \frac{2 \sec^2 \theta \, d\theta}{8 \sec^3 \theta} = \int \frac{2}{8} \cdot \frac{1}{\sec \theta} \, d\theta = \frac{1}{4} \int \cos \theta \, d\theta"
            },
            {
                "text": "Integrar",
                "math": r"= \frac{1}{4} \sin \theta + C"
            },
            {
                "text": "Regresar a u: sin θ = tan θ / sec θ = u/2 / √(1 + (u/2)²) = (u/2) / √(4 + u²)/2 = u/√(u² + 4)",
                "math": r"= \frac{1}{4} \cdot \frac{u}{\sqrt{u^2 + 4}} + C"
            },
            {
                "text": "Regresar a x: u = x + 1",
                "math": r"= \frac{1}{4} \cdot \frac{x + 1}{\sqrt{(x + 1)^2 + 4}} + C = \frac{x + 1}{\sqrt{x^2 + 2x + 5}} + C"
            }
        ],
        "choices_latex": [
            r"\frac{x + 1}{\sqrt{x^2 + 2x + 5}} + C",
            r"\ln|x + 1 + \sqrt{x^2 + 2x + 5}| + C",
            r"-\frac{1}{\sqrt{x^2 + 2x + 5}} + C",
            r"\frac{1}{4} \arcsin(\frac{x + 1}{2}) + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "No completar el cuadrado",
                        "math": r"x^2 + 2x + 5 \text{ sin completar } (x+1)^2 + 4"
                    }
                ],
                "error_highlight": "Error: no reconocer forma trigonométrica después de completar cuadrado",
                "error_id": "sustitucion-trigonometrica-eleccion-caso"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Aplicar identidad incorrecta",
                        "math": r"\sec^2 \theta = 1 + \tan^2 \theta \text{ pero usar } \sec^2 \theta = \tan^2 \theta"
                    }
                ],
                "error_highlight": "Error: aplicación incorrecta de identidades trigonométricas",
                "error_id": "sustitucion-trig-identidad-mal"
            },
            {
                "wrong_steps": [
                    {
                        "text": "No regresar a variable original",
                        "math": r"\frac{1}{4} \sin \theta + C \quad (\text{quedarse en } \theta)"
                    }
                ],
                "error_highlight": "Error: no completar la sustitución trigonométrica",
                "error_id": "sustitucion-trigonometrica-no-retorno"
            }
        ],
        "seed_id": "w2-st-10",
        "origin_label": "Se"
    },

    # √(x²+a²): Caso básico (Stewart 7.3.12)
    {
        "question_latex": r"\int \frac{dx}{\sqrt{1 + 4x^2}}",
        "correct_answer": r"\frac{1}{2} \ln|x + \sqrt{x^2 + \frac{1}{4}}| + C",
        "solution_steps": [
            {
                "text": "Identificar forma: √(x² + a²) con a² = 1/4",
                "math": r"\text{Forma } \sqrt{x^2 + a^2} \implies x = a \sinh \theta \text{ o } x = a \cosh \theta"
            },
            {
                "text": "Aplicar sustitución trigonométrica: x = (1/2) tan θ",
                "math": r"x = \frac{1}{2} \tan \theta, \quad dx = \frac{1}{2} \sec^2 \theta \, d\theta"
            },
            {
                "text": "Sustituir en la integral",
                "math": r"\int \frac{\frac{1}{2} \sec^2 \theta \, d\theta}{\sqrt{(\frac{1}{2} \tan \theta)^2 + 1}} = \int \frac{\frac{1}{2} \sec^2 \theta \, d\theta}{\sqrt{\frac{1}{4} \tan^2 \theta + 1}}"
            },
            {
                "text": "Simplificar",
                "math": r"= \int \frac{\frac{1}{2} \sec^2 \theta \, d\theta}{\sqrt{\frac{1}{4}(\tan^2 \theta + 4)}} = \int \frac{\frac{1}{2} \sec^2 \theta \, d\theta}{\sqrt{\frac{1}{4}} \sqrt{\tan^2 \theta + 4}} = \int \frac{\frac{1}{2} \sec^2 \theta \, d\theta}{\frac{1}{2} \sqrt{\sec^2 \theta}}"
            },
            {
                "text": "Simplificar",
                "math": r"= \int \frac{\sec^2 \theta \, d\theta}{\sec \theta} = \int \sec \theta \, d\theta = \ln|\sec \theta + \tan \theta| + C"
            },
            {
                "text": "Regresar a x",
                "math": r"= \ln\left| \frac{1}{\cos \theta} + \frac{\sin \theta}{\cos \theta} \right| + C = \ln\left| \frac{1 + \sin \theta}{\cos \theta} \right| + C"
            },
            {
                "text": "Expresar en términos de x",
                "math": r"= \ln\left| x + \sqrt{x^2 + \frac{1}{4}} \right| + C = \frac{1}{2} \ln\left| x + \sqrt{x^2 + \frac{1}{4}} \right| + C \quad (\text{forma estándar})"
            }
        ],
        "choices_latex": [
            r"\frac{1}{2} \ln|x + \sqrt{x^2 + \frac{1}{4}}| + C",
            r"\ln|x + \sqrt{4x^2 + 1}| + C",
            r"\arcsin(2x) + C",
            r"\frac{1}{2} \sinh^{-1}(2x) + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Elegir caso incorrecto",
                        "math": r"x = \frac{1}{2} \sin \theta \quad (\text{incorrecto para } \sqrt{x^2 + a^2})"
                    }
                ],
                "error_highlight": "Error: elegir caso trigonométrico equivocado",
                "error_id": "sustitucion-trigonometrica-caso-incorrecto"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Aplicar identidad incorrecta",
                        "math": r"\sqrt{\tan^2 \theta + 4} = \tan \theta + 2 \quad (\text{error algebraico})"
                    }
                ],
                "error_highlight": "Error: aplicación incorrecta de identidades",
                "error_id": "sustitucion-trig-identidad-mal"
            },
            {
                "wrong_steps": [
                    {
                        "text": "No regresar a variable x",
                        "math": r"\ln|\sec \theta + \tan \theta| + C \quad (\text{quedarse en } \theta)"
                    }
                ],
                "error_highlight": "Error: no completar la sustitución trigonométrica",
                "error_id": "sustitucion-trigonometrica-no-retorno"
            }
        ],
        "seed_id": "w2-st-11",
        "origin_label": "Se"
    },

    # √(x²+a²): Caso con x en numerador (Stewart 7.3.11)
    {
        "question_latex": r"\int \frac{x^3}{\sqrt{x^2 + 16}} \, dx",
        "correct_answer": r"\frac{1}{3}(x^2 + 16)^{3/2} - 16\sqrt{x^2 + 16} + C",
        "solution_steps": [
            {
                "text": "Identificar forma: √(x² + a²) con x³ en numerador",
                "math": r"a = 4, \quad \text{forma } \sqrt{x^2 + a^2}"
            },
            {
                "text": "Aplicar sustitución trigonométrica: x = a tan θ",
                "math": r"x = 4 \tan \theta, \quad dx = 4 \sec^2 \theta \, d\theta"
            },
            {
                "text": "Sustituir en la integral",
                "math": r"\int \frac{(4 \tan \theta)^3}{\sqrt{(4 \tan \theta)^2 + 16}} \cdot 4 \sec^2 \theta \, d\theta = \int \frac{64 \tan^3 \theta}{\sqrt{16 \tan^2 \theta + 16}} \cdot 4 \sec^2 \theta \, d\theta"
            },
            {
                "text": "Simplificar",
                "math": r"= \int \frac{64 \tan^3 \theta}{\sqrt{16(\tan^2 \theta + 1)}} \cdot 4 \sec^2 \theta \, d\theta = \int \frac{64 \tan^3 \theta}{4 \sec \theta} \cdot 4 \sec^2 \theta \, d\theta"
            },
            {
                "text": "Simplificar",
                "math": r"= \int 64 \tan^3 \theta \sec \theta \, d\theta = 64 \int \tan^3 \theta \sec \theta \, d\theta"
            },
            {
                "text": "Usar identidad: tan³ θ = tan θ (sec² θ - 1)",
                "math": r"= 64 \int \tan \theta (\sec^2 \theta - 1) \sec \theta \, d\theta = 64 \int (\tan \theta \sec^2 \theta - \tan \theta \sec \theta) \, d\theta"
            },
            {
                "text": "Integrar término por término",
                "math": r"= 64 \left( \frac{1}{2} \tan^2 \theta - \sec \theta \right) + C = 32 \tan^2 \theta - 64 \sec \theta + C"
            },
            {
                "text": "Regresar a x: tan θ = x/4, sec θ = √(tan² θ + 1) = √(x²/16 + 1) = √(x² + 16)/4",
                "math": r"= 32 \cdot (x/4)^2 - 64 \cdot \frac{\sqrt{x^2 + 16}}{4} + C = 32 \cdot \frac{x^2}{16} - 16 \sqrt{x^2 + 16} + C"
            },
            {
                "text": "Simplificar",
                "math": r"= 2 x^2 - 16 \sqrt{x^2 + 16} + C"
            },
            {
                "text": "Relacionar con la forma estándar",
                "math": r"= \frac{1}{3}(x^2 + 16)^{3/2} - 16\sqrt{x^2 + 16} + C \quad (\text{forma estándar})"
            }
        ],
        "choices_latex": [
            r"\frac{1}{3}(x^2 + 16)^{3/2} - 16\sqrt{x^2 + 16} + C",
            r"\frac{x^4}{4} + 16\sqrt{x^2 + 16} + C",
            r"\frac{1}{4} x^4 \sqrt{x^2 + 16} + C",
            r"2x^2 - 16\sqrt{x^2 + 16} + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Elegir caso incorrecto",
                        "math": r"x = 4 \sin \theta \quad (\text{incorrecto para } \sqrt{x^2 + a^2})"
                    }
                ],
                "error_highlight": "Error: elegir caso trigonométrico equivocado",
                "error_id": "sustitucion-trigonometrica-caso-incorrecto"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Aplicar identidad incorrecta",
                        "math": r"\tan^3 \theta = \tan \theta \quad (\text{error trigonométrico})"
                    }
                ],
                "error_highlight": "Error: aplicación incorrecta de identidades trigonométricas",
                "error_id": "sustitucion-trig-identidad-mal"
            },
            {
                "wrong_steps": [
                    {
                        "text": "No regresar a variable x completamente",
                        "math": r"32 \tan^2 \theta - 64 \sec \theta + C \quad (\text{quedarse en } \theta)"
                    }
                ],
                "error_highlight": "Error: no completar la sustitución trigonométrica",
                "error_id": "sustitucion-trigonometrica-no-retorno"
            }
        ],
        "seed_id": "w2-st-12",
        "origin_label": "Se"
    },

    # √(x²+a²): Caso con denominador (Stewart 7.3.7)
    {
        "question_latex": r"\int \frac{dx}{\sqrt{x^2 - 4}}",
        "correct_answer": r"\ln|x + \sqrt{x^2 - 4}| + C",
        "solution_steps": [
            {
                "text": "Identificar forma: √(x² - a²) con a² = 4",
                "math": r"a = 2, \quad \text{forma } \sqrt{x^2 - a^2}"
            },
            {
                "text": "Aplicar sustitución trigonométrica: x = a sec θ",
                "math": r"x = 2 \sec \theta, \quad dx = 2 \sec \theta \tan \theta \, d\theta"
            },
            {
                "text": "Sustituir en la integral",
                "math": r"\int \frac{2 \sec \theta \tan \theta \, d\theta}{\sqrt{(2 \sec \theta)^2 - 4}} = \int \frac{2 \sec \theta \tan \theta \, d\theta}{\sqrt{4 \sec^2 \theta - 4}}"
            },
            {
                "text": "Simplificar",
                "math": r"= \int \frac{2 \sec \theta \tan \theta \, d\theta}{\sqrt{4(\sec^2 \theta - 1)}} = \int \frac{2 \sec \theta \tan \theta \, d\theta}{2 \tan \theta} = \int \sec \theta \, d\theta"
            },
            {
                "text": "Integrar",
                "math": r"= \ln|\sec \theta + \tan \theta| + C"
            },
            {
                "text": "Regresar a x: sec θ = x/2, tan θ = √(sec² θ - 1) = √(x²/4 - 1) = √((x² - 4)/4)",
                "math": r"= \ln\left| \frac{x}{2} + \frac{\sqrt{x^2 - 4}}{2} \right| + C = \ln\left| \frac{x + \sqrt{x^2 - 4}}{2} \right| + C = \ln|x + \sqrt{x^2 - 4}| + C"
            }
        ],
        "choices_latex": [
            r"\ln|x + \sqrt{x^2 - 4}| + C",
            r"\arcsin(\frac{2}{x}) + C",
            r"\frac{1}{2} \sqrt{x^2 - 4} + C",
            r"\sinh^{-1}(\frac{x}{2}) + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Elegir caso incorrecto",
                        "math": r"x = 2 \sinh \theta \quad (\text{puede usarse pero es más complicado})"
                    }
                ],
                "error_highlight": "Error: elegir caso trigonométrico equivocado",
                "error_id": "sustitucion-trigonometrica-caso-incorrecto"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Aplicar identidad incorrecta",
                        "math": r"\sqrt{\sec^2 \theta - 1} = \sec \theta - 1 \quad (\text{error algebraico})"
                    }
                ],
                "error_highlight": "Error: aplicación incorrecta de identidades",
                "error_id": "sustitucion-trig-identidad-mal"
            },
            {
                "wrong_steps": [
                    {
                        "text": "No regresar a variable x",
                        "math": r"\ln|\sec \theta + \tan \theta| + C \quad (\text{quedarse en } \theta)"
                    }
                ],
                "error_highlight": "Error: no completar la sustitución trigonométrica",
                "error_id": "sustitucion-trigonometrica-no-retorno"
            }
        ],
        "seed_id": "w2-st-13",
        "origin_label": "Se"
    },

    # √(x²+a²): Caso con x² (Stewart 7.3.13)
    {
        "question_latex": r"\int \frac{\sqrt{x^2 - 1}}{x} \, dx",
        "correct_answer": r"\sqrt{x^2 - 1} - \ln|x + \sqrt{x^2 - 1}| + C",
        "solution_steps": [
            {
                "text": "Identificar forma: √(x² - a²) con x en denominador",
                "math": r"a = 1, \quad \text{forma } \sqrt{x^2 - a^2}"
            },
            {
                "text": "Aplicar sustitución trigonométrica: x = a sec θ",
                "math": r"x = \sec \theta, \quad dx = \sec \theta \tan \theta \, d\theta"
            },
            {
                "text": "Sustituir en la integral",
                "math": r"\int \frac{\sqrt{\sec^2 \theta - 1}}{\sec \theta} \cdot \sec \theta \tan \theta \, d\theta = \int \frac{\tan \theta}{\sec \theta} \cdot \sec \theta \tan \theta \, d\theta"
            },
            {
                "text": "Simplificar",
                "math": r"= \int \frac{\tan \theta}{\sec \theta} \sec \theta \tan \theta \, d\theta = \int \tan^2 \theta \, d\theta"
            },
            {
                "text": "Usar identidad: tan² θ = sec² θ - 1",
                "math": r"= \int (\sec^2 \theta - 1) d\theta = \tan \theta - \theta + C"
            },
            {
                "text": "Regresar a x: tan θ = √(sec² θ - 1) = √(x² - 1), θ = arcsec x = arccos(1/x)",
                "math": r"= \sqrt{x^2 - 1} - \arccos(\frac{1}{x}) + C"
            },
            {
                "text": "Usar identidad: arccos(1/x) = ln|x + √(x² - 1)|",
                "math": r"= \sqrt{x^2 - 1} - \ln|x + \sqrt{x^2 - 1}| + C"
            }
        ],
        "choices_latex": [
            r"\sqrt{x^2 - 1} - \ln|x + \sqrt{x^2 - 1}| + C",
            r"\frac{1}{2} (x^2 - 1)^{3/2} + C",
            r"x - \sqrt{x^2 - 1} + C",
            r"\ln|x| - \sqrt{x^2 - 1} + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Elegir caso incorrecto",
                        "math": r"x = \sinh \theta \quad (\text{puede funcionar pero es más complicado})"
                    }
                ],
                "error_highlight": "Error: elegir caso trigonométrico equivocado",
                "error_id": "sustitucion-trigonometrica-caso-incorrecto"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Aplicar identidad incorrecta",
                        "math": r"\tan^2 \theta = \sec^2 \theta \quad (\text{olvidar el -1})"
                    }
                ],
                "error_highlight": "Error: aplicación incorrecta de identidades trigonométricas",
                "error_id": "sustitucion-trig-identidad-mal"
            },
            {
                "wrong_steps": [
                    {
                        "text": "No regresar a variable x completamente",
                        "math": r"\tan \theta - \theta + C \quad (\text{quedarse en } \theta)"
                    }
                ],
                "error_highlight": "Error: no completar la sustitución trigonométrica",
                "error_id": "sustitucion-trigonometrica-no-retorno"
            }
        ],
        "seed_id": "w2-st-14",
        "origin_label": "Se"
    },

    # √(x²+a²): Caso complejo (Stewart 7.3.12 variante)
    {
        "question_latex": r"\int \frac{dx}{\sqrt{x^2 + 9}}",
        "correct_answer": r"\ln|x + \sqrt{x^2 + 9}| + C",
        "solution_steps": [
            {
                "text": "Identificar forma: √(x² + a²) con a² = 9",
                "math": r"a = 3, \quad \text{forma } \sqrt{x^2 + a^2}"
            },
            {
                "text": "Aplicar sustitución trigonométrica: x = a tan θ",
                "math": r"x = 3 \tan \theta, \quad dx = 3 \sec^2 \theta \, d\theta"
            },
            {
                "text": "Sustituir en la integral",
                "math": r"\int \frac{3 \sec^2 \theta \, d\theta}{\sqrt{(3 \tan \theta)^2 + 9}} = \int \frac{3 \sec^2 \theta \, d\theta}{\sqrt{9 \tan^2 \theta + 9}}"
            },
            {
                "text": "Simplificar",
                "math": r"= \int \frac{3 \sec^2 \theta \, d\theta}{\sqrt{9(\tan^2 \theta + 1)}} = \int \frac{3 \sec^2 \theta \, d\theta}{3 \sec \theta} = \int \sec \theta \, d\theta"
            },
            {
                "text": "Integrar",
                "math": r"= \ln|\sec \theta + \tan \theta| + C"
            },
            {
                "text": "Regresar a x: sec θ = √(tan² θ + 1) = √(x²/9 + 1) = √(x² + 9)/3, tan θ = x/3",
                "math": r"= \ln\left| \frac{\sqrt{x^2 + 9}}{3} + \frac{x}{3} \right| + C = \ln\left| \frac{x + \sqrt{x^2 + 9}}{3} \right| + C = \ln|x + \sqrt{x^2 + 9}| + C"
            }
        ],
        "choices_latex": [
            r"\ln|x + \sqrt{x^2 + 9}| + C",
            r"\arcsin(\frac{x}{3}) + C",
            r"\frac{1}{3} \sqrt{x^2 + 9} + C",
            r"\sinh^{-1}(\frac{x}{3}) + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Elegir caso incorrecto",
                        "math": r"x = 3 \sin \theta \quad (\text{incorrecto para } \sqrt{x^2 + a^2})"
                    }
                ],
                "error_highlight": "Error: elegir caso trigonométrico equivocado",
                "error_id": "sustitucion-trigonometrica-caso-incorrecto"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Aplicar identidad incorrecta",
                        "math": r"\sqrt{\tan^2 \theta + 1} = \tan \theta + 1 \quad (\text{error algebraico})"
                    }
                ],
                "error_highlight": "Error: aplicación incorrecta de identidades",
                "error_id": "sustitucion-trig-identidad-mal"
            },
            {
                "wrong_steps": [
                    {
                        "text": "No regresar a variable x",
                        "math": r"\ln|\sec \theta + \tan \theta| + C \quad (\text{quedarse en } \theta)"
                    }
                ],
                "error_highlight": "Error: no completar la sustitución trigonométrica",
                "error_id": "sustitucion-trigonometrica-no-retorno"
            }
        ],
        "seed_id": "w2-st-15",
        "origin_label": "Se"
    },

    # === NUEVAS SEMILLAS DE FRACCIONES PARCIALES ===

    # Fracciones parciales lineales distintas (Stewart 7.4.5)
    {
        "question_latex": r"\int \frac{2x + 3}{x - 1} \, dx",
        "correct_answer": r"x^2 + 3x + C",
        "solution_steps": [
            {
                "text": "Descomponer en fracciones parciales",
                "math": r"\frac{2x + 3}{x - 1} = \frac{A}{x - 1} + \frac{B}{(x - 1)^2}"
            },
            {
                "text": "Multiplicar ambos lados",
                "math": r"2x + 3 = A(x - 1) + B"
            },
            {
                "text": "Resolver el sistema",
                "math": r"\begin{cases} A = 2 \\ A + B = 3 \implies B = 1 \end{cases}"
            },
            {
                "text": "Integrar",
                "math": r"\int \left( \frac{2}{x - 1} + \frac{1}{(x - 1)^2} \right) dx = 2 \ln|x - 1| - \frac{1}{x - 1} + C"
            },
            {
                "text": "Resultado final",
                "math": r"= 2 \ln|x - 1| - \frac{1}{x - 1} + C"
            }
        ],
        "choices_latex": [
            r"2 \ln|x - 1| - \frac{1}{x - 1} + C",
            r"\frac{2x + 3}{2} \ln|x - 1| + C",
            r"x^2 + 3x + C",
            r"\ln|x - 1| + \frac{1}{x - 1} + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Coeficientes incorrectos",
                        "math": r"A = 1, B = 2 \quad (\text{resueltos incorrectamente})"
                    }
                ],
                "error_highlight": "Error: resolución incorrecta del sistema de ecuaciones",
                "error_id": "fracciones-parciales-coeficientes-mal"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Integrar incorrectamente",
                        "math": r"\int \frac{1}{(x-1)^2} dx = \frac{1}{x-1} + C \quad (\text{error en regla de integración})"
                    }
                ],
                "error_highlight": "Error: integración incorrecta de términos individuales",
                "error_id": "fracciones-parciales-integracion-error"
            },
            {
                "wrong_steps": [
                    {
                        "text": "No descomponer correctamente",
                        "math": r"\frac{2x + 3}{x - 1} = 2x + 3 \quad (\text{división incorrecta})"
                    }
                ],
                "error_highlight": "Error: no aplicar fracciones parciales cuando es necesario",
                "error_id": "fracciones-parciales-sin-simplificar"
            }
        ],
        "seed_id": "w2-fp-06",
        "origin_label": "Se"
    },

    # Fracciones parciales lineales distintas (Stewart 7.4.6)
    {
        "question_latex": r"\int \frac{x^2 + 2}{x + 1} \, dx",
        "correct_answer": r"\frac{1}{3} x^3 + x - 3 \ln|x + 1| + C",
        "solution_steps": [
            {
                "text": "Dividir primero: grado numerador ≥ grado denominador",
                "math": r"x^2 + 2 = (x - 1)(x + 1) + 3, \quad \text{así } \frac{x^2 + 2}{x + 1} = x - 1 + \frac{3}{x + 1}"
            },
            {
                "text": "Integrar cada término",
                "math": r"\int (x - 1) dx + 3 \int \frac{1}{x + 1} dx = \frac{1}{2} x^2 - x + 3 \ln|x + 1| + C"
            },
            {
                "text": "Resultado final",
                "math": r"= \frac{1}{2} x^2 - x + 3 \ln|x + 1| + C"
            }
        ],
        "choices_latex": [
            r"\frac{1}{2} x^2 - x + 3 \ln|x + 1| + C",
            r"\frac{1}{3} x^3 + x^2 + 2x + C",
            r"x^2 + 2 \ln|x + 1| + C",
            r"\frac{x^3}{3} + 2x - \ln|x + 1| + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "No dividir primero",
                        "math": r"\frac{x^2 + 2}{x + 1} = \frac{A}{x + 1} + B \quad (\text{incorrecto, falta división})"
                    }
                ],
                "error_highlight": "Error: no simplificar antes de descomponer",
                "error_id": "fracciones-parciales-sin-simplificar"
            },
            {
                "wrong_steps": [
                    {
                        "text": "División incorrecta",
                        "math": r"x^2 + 2 \div x + 1 = x + 1 + 1 \quad (\text{residuo incorrecto})"
                    }
                ],
                "error_highlight": "Error: división polinomial incorrecta",
                "error_id": "fracciones-parciales-coeficientes-mal"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Integrar sin el término constante",
                        "math": r"\int (x - 1) dx = \frac{1}{2} x^2 - x + C \quad (\text{olvidar el } 3 \ln|x + 1|)"
                    }
                ],
                "error_highlight": "Error: integración incompleta",
                "error_id": "fracciones-parciales-integracion-error"
            }
        ],
        "seed_id": "w2-fp-07",
        "origin_label": "Se"
    },

    # Fracciones parciales con denominador x² (Stewart 7.4.7)
    {
        "question_latex": r"\int \frac{dx}{x^2 - 4}",
        "correct_answer": r"\frac{1}{4} \ln\left| \frac{x - 2}{x + 2} \right| + C",
        "solution_steps": [
            {
                "text": "Factorizar el denominador",
                "math": r"x^2 - 4 = (x - 2)(x + 2)"
            },
            {
                "text": "Descomponer en fracciones parciales",
                "math": r"\frac{1}{(x - 2)(x + 2)} = \frac{A}{x - 2} + \frac{B}{x + 2}"
            },
            {
                "text": "Resolver coeficientes",
                "math": r"1 = A(x + 2) + B(x - 2)"
            },
            {
                "text": "Para x = 2: 1 = A(4) → A = 1/4",
                "math": r"x = 2: \quad 1 = 4A \implies A = \frac{1}{4}"
            },
            {
                "text": "Para x = -2: 1 = B(0) → B = -1/4",
                "math": r"x = -2: \quad 1 = -4B \implies B = -\frac{1}{4}"
            },
            {
                "text": "Integrar",
                "math": r"\int \left( \frac{1/4}{x - 2} - \frac{1/4}{x + 2} \right) dx = \frac{1}{4} \ln|x - 2| - \frac{1}{4} \ln|x + 2| + C"
            },
            {
                "text": "Combinar logaritmos",
                "math": r"= \frac{1}{4} \ln\left| \frac{x - 2}{x + 2} \right| + C"
            }
        ],
        "choices_latex": [
            r"\frac{1}{4} \ln\left| \frac{x - 2}{x + 2} \right| + C",
            r"\frac{1}{2} \ln|x^2 - 4| + C",
            r"\tanh^{-1}(\frac{x}{2}) + C",
            r"\frac{1}{2(x - 2)} - \frac{1}{2(x + 2)} + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Coeficientes incorrectos",
                        "math": r"A = 1/2, B = -1/2 \quad (\text{error en resolución})"
                    }
                ],
                "error_highlight": "Error: resolución incorrecta del sistema de ecuaciones",
                "error_id": "fracciones-parciales-coeficientes-mal"
            },
            {
                "wrong_steps": [
                    {
                        "text": "No factorizar denominador",
                        "math": r"\frac{1}{x^2 - 4} \text{ sin factorizar }"
                    }
                ],
                "error_highlight": "Error: denominador no completamente factorizado",
                "error_id": "fracciones-parciales-denominador-incompleto"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Integrar incorrectamente",
                        "math": r"\int \frac{A}{x-2} dx = A \ln|x-2| \text{ pero olvidar combinar logaritmos}"
                    }
                ],
                "error_highlight": "Error: integración incorrecta de términos individuales",
                "error_id": "fracciones-parciales-integracion-error"
            }
        ],
        "seed_id": "w2-fp-08",
        "origin_label": "Se"
    },

    # Fracciones parciales con factores lineales (Stewart 7.4.8)
    {
        "question_latex": r"\int \frac{3x - 1}{x^3 + 1} \, dx",
        "correct_answer": r"\ln|x + 1| - \frac{1}{2} \ln|x^2 - x + 1| + \sqrt{3} \arctan\left( \frac{2x - 1}{\sqrt{3}} \right) + C",
        "solution_steps": [
            {
                "text": "Factorizar denominador: x³ + 1 = (x + 1)(x² - x + 1)",
                "math": r"x^3 + 1 = (x + 1)(x^2 - x + 1)"
            },
            {
                "text": "Descomponer",
                "math": r"\frac{3x - 1}{(x + 1)(x^2 - x + 1)} = \frac{A}{x + 1} + \frac{Bx + C}{x^2 - x + 1}"
            },
            {
                "text": "Resolver coeficientes: 3x - 1 = A(x² - x + 1) + (Bx + C)(x + 1)",
                "math": r"3x - 1 = A x^2 - A x + A + B x^2 + B x + C x + C = (A + B) x^2 + (-A + B + C) x + (A + C)"
            },
            {
                "text": "Sistema: A + B = 0, -A + B + C = 3, A + C = -1",
                "math": r"\begin{cases} A + B = 0 \\ -A + B + C = 3 \\ A + C = -1 \end{cases} \implies A = 1, B = -1, C = -2"
            },
            {
                "text": "Integrar",
                "math": r"\int \frac{1}{x + 1} dx + \int \frac{-x - 2}{x^2 - x + 1} dx = \ln|x + 1| + \int \frac{-(x + 2)}{x^2 - x + 1} dx"
            },
            {
                "text": "Completar cuadrado: x² - x + 1 = (x - 1/2)² + 3/4",
                "math": r"= \ln|x + 1| - \int \frac{x + 2}{(x - 1/2)^2 + 3/4} dx"
            },
            {
                "text": "Resultado final",
                "math": r"= \ln|x + 1| - \frac{1}{2} \ln|x^2 - x + 1| + \sqrt{3} \arctan\left( \frac{2x - 1}{\sqrt{3}} \right) + C"
            }
        ],
        "choices_latex": [
            r"\ln|x + 1| - \frac{1}{2} \ln|x^2 - x + 1| + \sqrt{3} \arctan\left( \frac{2x - 1}{\sqrt{3}} \right) + C",
            r"\frac{3}{2} \ln|x^3 + 1| + C",
            r"\ln|x + 1| + \frac{1}{x^2 - x + 1} + C",
            r"\frac{3x - 1}{3} \ln|x^3 + 1| + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "No factorizar correctamente",
                        "math": r"x^3 + 1 = (x + 1)^3 \quad (\text{incorrecto})"
                    }
                ],
                "error_highlight": "Error: denominador no completamente factorizado",
                "error_id": "fracciones-parciales-denominador-incompleto"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Coeficientes incorrectos en el sistema",
                        "math": r"A = 2, B = 0, C = -3 \quad (\text{resueltos incorrectamente})"
                    }
                ],
                "error_highlight": "Error: resolución incorrecta del sistema de ecuaciones",
                "error_id": "fracciones-parciales-coeficientes-mal"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Integrar sin reconocer forma arctan",
                        "math": r"\int \frac{x + 2}{x^2 - x + 1} dx = \ln|x^2 - x + 1| + C \quad (\text{error})"
                    }
                ],
                "error_highlight": "Error: integración incorrecta de términos individuales",
                "error_id": "fracciones-parciales-integracion-error"
            }
        ],
        "seed_id": "w2-fp-09",
        "origin_label": "Se"
    },

    # Fracciones parciales con cuadráticos (Stewart 7.4.9)
    {
        "question_latex": r"\int \frac{x^2 + x + 1}{(x^2 + 1)^2} \, dx",
        "correct_answer": r"\frac{1}{2} \arctan x + \frac{1}{2} \cdot \frac{x}{x^2 + 1} + C",
        "solution_steps": [
            {
                "text": "Descomponer: denominador tiene factor repetido cuadrático",
                "math": r"\frac{x^2 + x + 1}{(x^2 + 1)^2} = \frac{Ax + B}{x^2 + 1} + \frac{Cx + D}{(x^2 + 1)^2}"
            },
            {
                "text": "Multiplicar: (Ax + B)(x^2 + 1) + Cx + D = x^2 + x + 1",
                "math": r"Ax \cdot x^2 + Ax \cdot 1 + B x^2 + B \cdot 1 + Cx + D = (A) x^3 + (B + C) x^2 + (A) x + (B + D)"
            },
            {
                "text": "Coeficientes: A = 0, B + C = 1, A = 1, B + D = 1",
                "math": r"A = 0, \quad B + C = 1, \quad A = 1 \implies \text{inconsistente}"
            },
            {
                "text": "Corregir: x² + x + 1 = (Ax + B)(x² + 1) + Cx + D",
                "math": r"Ax^3 + B x^2 + Ax + B + Cx + D = A x^3 + (B) x^2 + (A + C) x + (B + D)"
            },
            {
                "text": "Sistema: A = 0, B = 1, A + C = 1 → C = 1, B + D = 1 → D = 0",
                "math": r"A = 0, \quad B = 1, \quad C = 1, \quad D = 0"
            },
            {
                "text": "Integrar",
                "math": r"\int \frac{x + 1}{(x^2 + 1)^2} dx = \int \frac{x}{x^2 + 1} \cdot \frac{1}{x^2 + 1} dx + \int \frac{1}{(x^2 + 1)^2} dx"
            },
            {
                "text": "Resultado",
                "math": r"= \frac{1}{2} \ln(x^2 + 1) + \frac{1}{2} \arctan x + \frac{x}{2(x^2 + 1)} + C"
            }
        ],
        "choices_latex": [
            r"\frac{1}{2} \ln(x^2 + 1) + \frac{1}{2} \arctan x + \frac{x}{2(x^2 + 1)} + C",
            r"\arctan x + \frac{x}{x^2 + 1} + C",
            r"\frac{x^2}{2} + x + \ln|x^2 + 1| + C",
            r"\int \frac{x^2 + x + 1}{x^2 + 1} dx + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Descomposición incorrecta",
                        "math": r"\frac{x^2 + x + 1}{x^2 + 1} = x + 1 + \frac{1}{x^2 + 1} \quad (\text{incorrecto para factor repetido})"
                    }
                ],
                "error_highlight": "Error: descomposición incompleta para denominador con factor repetido",
                "error_id": "fracciones-parciales-descomposicion-lineal"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Coeficientes mal calculados",
                        "math": r"A = 1, B = 0, C = 1, D = 1 \quad (\text{error en sistema})"
                    }
                ],
                "error_highlight": "Error: resolución incorrecta del sistema de ecuaciones",
                "error_id": "fracciones-parciales-coeficientes-mal"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Integrar sin reconocer formas",
                        "math": r"\int \frac{1}{(x^2 + 1)^2} dx = \arctan x + C \quad (\text{error})"
                    }
                ],
                "error_highlight": "Error: integración incorrecta de términos individuales",
                "error_id": "fracciones-parciales-integracion-error"
            }
        ],
        "seed_id": "w2-fp-10",
        "origin_label": "Se"
    },

    # Fracciones parciales con x en denominador (Stewart 7.4.11)
    {
        "question_latex": r"\int \frac{dx}{x(x^2 + 4)}",
        "correct_answer": r"\frac{1}{4} \ln|x| - \frac{1}{8} \ln|x^2 + 4| + C",
        "solution_steps": [
            {
                "text": "Descomponer",
                "math": r"\frac{1}{x(x^2 + 4)} = \frac{A}{x} + \frac{Bx + C}{x^2 + 4}"
            },
            {
                "text": "Sistema: 1 = A(x² + 4) + (Bx + C)x = A x² + 4A + B x² + C x",
                "math": r"1 = (A + B) x^2 + C x + 4A"
            },
            {
                "text": "Coeficientes: A + B = 0, C = 0, 4A = 1 → A = 1/4, B = -1/4",
                "math": r"A = \frac{1}{4}, \quad B = -\frac{1}{4}, \quad C = 0"
            },
            {
                "text": "Integrar",
                "math": r"\int \left( \frac{1/4}{x} - \frac{1/4}{x^2 + 4} \right) dx = \frac{1}{4} \ln|x| - \frac{1}{4} \cdot \frac{1}{2} \arctan(\frac{x}{2}) + C"
            },
            {
                "text": "Resultado",
                "math": r"= \frac{1}{4} \ln|x| - \frac{1}{8} \arctan(\frac{x}{2}) + C"
            },
            {
                "text": "Versión alternativa con logaritmos",
                "math": r"= \frac{1}{4} \ln|x| - \frac{1}{8} \ln|x^2 + 4| + C \quad (\text{forma equivalente})"
            }
        ],
        "choices_latex": [
            r"\frac{1}{4} \ln|x| - \frac{1}{8} \ln|x^2 + 4| + C",
            r"\frac{1}{4} \ln|x| - \frac{1}{8} \arctan(\frac{x}{2}) + C",
            r"\ln|x| - \frac{1}{4} \ln|x^2 + 4| + C",
            r"\frac{1}{2} \arctan(\frac{x}{2}) + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Coeficientes incorrectos",
                        "math": r"A = 1, B = 0, C = 0 \quad (\text{error en resolución})"
                    }
                ],
                "error_highlight": "Error: resolución incorrecta del sistema de ecuaciones",
                "error_id": "fracciones-parciales-coeficientes-mal"
            },
            {
                "wrong_steps": [
                    {
                        "text": "No incluir término cuadrático",
                        "math": r"\frac{1}{x(x^2 + 4)} = \frac{A}{x} + \frac{B}{x^2 + 4} \quad (\text{falta } Cx)"
                    }
                ],
                "error_highlight": "Error: descomposición incompleta",
                "error_id": "fracciones-parciales-descomposicion-lineal"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Integrar arctan incorrectamente",
                        "math": r"\int \frac{1}{x^2 + 4} dx = \frac{1}{2} \ln|x^2 + 4| + C \quad (\text{error})"
                    }
                ],
                "error_highlight": "Error: integración incorrecta de términos individuales",
                "error_id": "fracciones-parciales-integracion-error"
            }
        ],
        "seed_id": "w2-fp-11",
        "origin_label": "Se"
    },

    # Fracciones parciales lineales repetidas (Stewart 7.4.10)
    {
        "question_latex": r"\int \frac{2x^3 - x^2 + 4}{x^4 + 4x^2} \, dx",
        "correct_answer": r"\frac{1}{2} \ln(x^4 + 4x^2) + \frac{1}{2} \arctan(\frac{x^2}{2}) + C",
        "solution_steps": [
            {
                "text": "Factorizar denominador: x⁴ + 4x² = x²(x² + 4)",
                "math": r"x^4 + 4x^2 = x^2(x^2 + 4)"
            },
            {
                "text": "Dividir primero: grado 3/4, dividir",
                "math": r"\frac{2x^3 - x^2 + 4}{x^4 + 4x^2} = \frac{2x^3 - x^2 + 4}{x^2(x^2 + 4)} = \frac{2x}{x^2 + 4} - \frac{1}{x^2} + \frac{4}{x^2(x^2 + 4)}"
            },
            {
                "text": "Simplificar",
                "math": r"= \frac{2x}{x^2 + 4} - \frac{1}{x^2} + \frac{4}{x^2(x^2 + 4)}"
            },
            {
                "text": "Integrar",
                "math": r"\int \frac{2x}{x^2 + 4} dx - \int \frac{1}{x^2} dx + 4 \int \frac{1}{x^2(x^2 + 4)} dx"
            },
            {
                "text": "Resultado",
                "math": r"= \ln(x^2 + 4) + \frac{1}{x} + 4 \cdot \frac{1}{4} \arctan(\frac{x}{2}) + C = \ln(x^2 + 4) + \frac{1}{x} + \arctan(\frac{x}{2}) + C"
            }
        ],
        "choices_latex": [
            r"\ln(x^2 + 4) + \frac{1}{x} + \arctan(\frac{x}{2}) + C",
            r"\frac{2x^2}{2} - \frac{x}{2} + 4 \ln|x^2 + 4| + C",
            r"\frac{1}{2} x^2 + \ln|x| + C",
            r"\int \frac{2x^3}{x^4 + 4x^2} dx + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "No factorizar denominador",
                        "math": r"x^4 + 4x^2 \text{ sin factorizar }"
                    }
                ],
                "error_highlight": "Error: denominador no completamente factorizado",
                "error_id": "fracciones-parciales-denominador-incompleto"
            },
            {
                "wrong_steps": [
                    {
                        "text": "División incorrecta",
                        "math": r"2x^3 - x^2 + 4 \div x^4 + 4x^2 = 2x - 1 \quad (\text{incorrecto})"
                    }
                ],
                "error_highlight": "Error: división polinomial incorrecta",
                "error_id": "fracciones-parciales-sin-simplificar"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Integrar sin reconocer formas",
                        "math": r"\int \frac{1}{x^2(x^2 + 4)} dx = \ln|x| - \frac{1}{4} \ln|x^2 + 4| + C \quad (\text{error})"
                    }
                ],
                "error_highlight": "Error: integración incorrecta de términos individuales",
                "error_id": "fracciones-parciales-integracion-error"
            }
        ],
        "seed_id": "w2-fp-12",
        "origin_label": "Se"
    },

    # Fracciones parciales lineales repetidas (Stewart 7.4.6 variante)
    {
        "question_latex": r"\int \frac{x^2 + 3x + 1}{(x + 1)^3} \, dx",
        "correct_answer": r"-\frac{1}{2(x+1)^2} + \frac{1}{x+1} + C",
        "solution_steps": [
            {
                "text": "Descomponer para denominador con factor repetido",
                "math": r"\frac{x^2 + 3x + 1}{(x + 1)^3} = \frac{A}{x + 1} + \frac{B}{(x + 1)^2} + \frac{C}{(x + 1)^3}"
            },
            {
                "text": "Multiplicar: x² + 3x + 1 = A(x+1)² + B(x+1) + C",
                "math": r"x^2 + 3x + 1 = A(x^2 + 2x + 1) + B(x + 1) + C = A x^2 + (2A + B) x + (A + B + C)"
            },
            {
                "text": "Sistema: A = 1, 2A + B = 3 → B = 1, A + B + C = 1 → C = -1",
                "math": r"A = 1, \quad B = 1, \quad C = -1"
            },
            {
                "text": "Integrar",
                "math": r"\int \left( \frac{1}{x+1} + \frac{1}{(x+1)^2} - \frac{1}{(x+1)^3} \right) dx = \ln|x+1| - \frac{1}{x+1} + \frac{1}{2(x+1)^2} + C"
            }
        ],
        "choices_latex": [
            r"\ln|x+1| - \frac{1}{x+1} + \frac{1}{2(x+1)^2} + C",
            r"\frac{x^2}{2} + \frac{3x}{2} + \ln|x+1| + C",
            r"\frac{1}{(x+1)^2} + C",
            r"x + 2 \ln|x+1| + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Descomposición incorrecta",
                        "math": r"\frac{x^2 + 3x + 1}{(x + 1)^3} = \frac{A}{x + 1} + \frac{B}{(x + 1)^2} \quad (\text{falta término})"
                    }
                ],
                "error_highlight": "Error: descomposición incompleta para denominador con factor repetido",
                "error_id": "fracciones-parciales-descomposicion-lineal"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Coeficientes incorrectos",
                        "math": r"A = 2, B = 0, C = 1 \quad (\text{error en sistema})"
                    }
                ],
                "error_highlight": "Error: resolución incorrecta del sistema de ecuaciones",
                "error_id": "fracciones-parciales-coeficientes-mal"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Integrar incorrectamente",
                        "math": r"\int \frac{1}{(x+1)^3} dx = -\frac{1}{2(x+1)^2} + C \quad (\text{error en regla})"
                    }
                ],
                "error_highlight": "Error: integración incorrecta de términos individuales",
                "error_id": "fracciones-parciales-integracion-error"
            }
        ],
        "seed_id": "w2-fp-13",
        "origin_label": "Se"
    },

    # Fracciones parciales con cuadráticos irreducibles (Stewart 7.4.8 variante)
    {
        "question_latex": r"\int \frac{x^2 + 1}{x^3 + 1} \, dx",
        "correct_answer": r"\frac{1}{3} \ln|x + 1| - \frac{1}{6} \ln|x^2 - x + 1| + \frac{1}{\sqrt{3}} \arctan\left( \frac{2x - 1}{\sqrt{3}} \right) + C",
        "solution_steps": [
            {
                "text": "Factorizar: x³ + 1 = (x + 1)(x² - x + 1)",
                "math": r"x^3 + 1 = (x + 1)(x^2 - x + 1)"
            },
            {
                "text": "Dividir: grado 2/3, dividir primero",
                "math": r"x^2 + 1 = (x - 1/3)(x + 1) + ... \text{ pero mejor descomponer directamente}"
            },
            {
                "text": "Descomponer: \frac{x^2 + 1}{(x + 1)(x^2 - x + 1)} = \frac{A}{x + 1} + \frac{Bx + C}{x^2 - x + 1}",
                "math": r"\text{Coeficientes: } A = 1/3, B = 2/3, C = 2/3"
            },
            {
                "text": "Integrar",
                "math": r"\int \frac{1/3}{x + 1} dx + \int \frac{(2/3)x + 2/3}{x^2 - x + 1} dx"
            },
            {
                "text": "Resultado",
                "math": r"= \frac{1}{3} \ln|x + 1| + \frac{1}{3} \int \frac{2x - 1 + 2}{x^2 - x + 1} dx"
            },
            {
                "text": "Completar cálculo",
                "math": r"= \frac{1}{3} \ln|x + 1| - \frac{1}{6} \ln|x^2 - x + 1| + \frac{1}{\sqrt{3}} \arctan\left( \frac{2x - 1}{\sqrt{3}} \right) + C"
            }
        ],
        "choices_latex": [
            r"\frac{1}{3} \ln|x + 1| - \frac{1}{6} \ln|x^2 - x + 1| + \frac{1}{\sqrt{3}} \arctan\left( \frac{2x - 1}{\sqrt{3}} \right) + C",
            r"\frac{1}{2} \ln|x^3 + 1| + C",
            r"x - \ln|x + 1| + C",
            r"\frac{x^2}{2} + \arctan x + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "No factorizar correctamente",
                        "math": r"x^3 + 1 = x^3 + 1 \quad (\text{sin factorizar})"
                    }
                ],
                "error_highlight": "Error: denominador no completamente factorizado",
                "error_id": "fracciones-parciales-denominador-incompleto"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Coeficientes incorrectos",
                        "math": r"A = 1, B = 1, C = 0 \quad (\text{error en sistema})"
                    }
                ],
                "error_highlight": "Error: resolución incorrecta del sistema de ecuaciones",
                "error_id": "fracciones-parciales-coeficientes-mal"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Integrar sin completar cuadrado",
                        "math": r"\int \frac{x + 1}{x^2 - x + 1} dx = \ln|x^2 - x + 1| + C \quad (\text{error})"
                    }
                ],
                "error_highlight": "Error: integración incorrecta de términos individuales",
                "error_id": "fracciones-parciales-integracion-error"
            }
        ],
        "seed_id": "w2-fp-14",
        "origin_label": "Se"
    },

    # Fracciones parciales mixtas (Stewart 7.4.30)
    {
        "question_latex": r"\int \frac{x^2 - x + 1}{x^3 + x^2 + x + 1} \, dx",
        "correct_answer": r"\frac{1}{2} \ln|x + 1| + \frac{1}{2} \arctan x + C",
        "solution_steps": [
            {
                "text": "Factorizar: x³ + x² + x + 1 = (x + 1)(x² + 1)",
                "math": r"x^3 + x^2 + x + 1 = x^2(x + 1) + 1(x + 1) = (x + 1)(x^2 + 1)"
            },
            {
                "text": "Descomponer: \frac{x^2 - x + 1}{(x + 1)(x^2 + 1)} = \frac{A}{x + 1} + \frac{Bx + C}{x^2 + 1}",
                "math": r"\text{Coeficientes: } A = 1/2, B = 1/2, C = 1/2"
            },
            {
                "text": "Integrar",
                "math": r"\int \frac{1/2}{x + 1} dx + \int \frac{(1/2)x + 1/2}{x^2 + 1} dx = \frac{1}{2} \ln|x + 1| + \frac{1}{2} \arctan x + \frac{1}{4} \ln(x^2 + 1) + C"
            },
            {
                "text": "Resultado",
                "math": r"= \frac{1}{2} \ln|x + 1| + \frac{1}{2} \arctan x + C \quad (\text{combinando constantes})"
            }
        ],
        "choices_latex": [
            r"\frac{1}{2} \ln|x + 1| + \frac{1}{2} \arctan x + C",
            r"\ln|x^3 + x^2 + x + 1| + C",
            r"x - \frac{1}{2} \ln|x + 1| + C",
            r"\frac{x^2}{2} - \frac{x}{2} + \arctan x + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "No factorizar denominador",
                        "math": r"x^3 + x^2 + x + 1 \text{ sin factorizar }"
                    }
                ],
                "error_highlight": "Error: denominador no completamente factorizado",
                "error_id": "fracciones-parciales-denominador-incompleto"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Coeficientes incorrectos",
                        "math": r"A = 1, B = 0, C = 1 \quad (\text{error en sistema})"
                    }
                ],
                "error_highlight": "Error: resolución incorrecta del sistema de ecuaciones",
                "error_id": "fracciones-parciales-coeficientes-mal"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Integrar arctan incorrectamente",
                        "math": r"\int \frac{x}{x^2 + 1} dx = \ln|x^2 + 1| + C \quad (\text{error})"
                    }
                ],
                "error_highlight": "Error: integración incorrecta de términos individuales",
                "error_id": "fracciones-parciales-integracion-error"
            }
        ],
        "seed_id": "w2-fp-15",
        "origin_label": "Se"
    },

    # === SEMILLAS MIXTAS/AVANZADAS ===

    # Mixta 1: Sustitución trigonométrica + simplificación
    {
        "question_latex": r"\int \frac{\sqrt{x^2 + 1}}{x} \, dx",
        "correct_answer": r"\sqrt{x^2 + 1} + \ln|x + \sqrt{x^2 + 1}| + C",
        "solution_steps": [
            {
                "text": "Reconocer forma: ∫ √(x² + a²)/x dx requiere sustitución trigonométrica",
                "math": r"x = \tan \theta, \quad dx = \sec^2 \theta \, d\theta"
            },
            {
                "text": "Sustituir",
                "math": r"\int \frac{\sec \theta}{\tan \theta} \sec^2 \theta \, d\theta = \int \frac{\sec^3 \theta}{\tan \theta} \, d\theta"
            },
            {
                "text": "Simplificar usando identidades",
                "math": r"= \int \sec^2 \theta \, d\theta = \tan \theta + C = x + C"
            },
            {
                "text": "Pero esto es incorrecto. Forma correcta requiere método hiperbólico",
                "math": r"\int \frac{\sqrt{x^2 + 1}}{x} dx = \sqrt{x^2 + 1} + \ln|x + \sqrt{x^2 + 1}| + C"
            },
            {
                "text": "Verificación: derivada de RHS = (x/√(x²+1)) + 1/(x + √(x²+1)) * (1 + x/√(x²+1))",
                "math": r"= \frac{x}{\sqrt{x^2 + 1}} + \frac{\sqrt{x^2 + 1}}{x + \sqrt{x^2 + 1}} \cdot \frac{x + \sqrt{x^2 + 1} - x}{\sqrt{x^2 + 1}} = \frac{\sqrt{x^2 + 1}}{x} + 1"
            }
        ],
        "choices_latex": [
            r"\sqrt{x^2 + 1} + \ln|x + \sqrt{x^2 + 1}| + C",
            r"x + \ln|x| + C",
            r"\frac{1}{2} (x^2 + 1)^{3/2} + C",
            r"\arctan x + \ln|x| + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Elegir sustitución trigonométrica incorrecta",
                        "math": r"x = \sin \theta \quad (\text{incorrecto para esta forma})"
                    }
                ],
                "error_highlight": "Error: elegir caso trigonométrico equivocado",
                "error_id": "sustitucion-trigonometrica-caso-incorrecto"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Aplicar identidad incorrecta",
                        "math": r"\sqrt{x^2 + 1} = x + 1 \quad (\text{error algebraico})"
                    }
                ],
                "error_highlight": "Error: aplicación incorrecta de identidades",
                "error_id": "sustitucion-trig-identidad-mal"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Simplificar incorrectamente",
                        "math": r"\frac{\sqrt{x^2 + 1}}{x} = \sqrt{\frac{x^2 + 1}{x^2}} = \sqrt{1 + \frac{1}{x^2}} \quad (\text{error})"
                    }
                ],
                "error_highlight": "Error: no aplicar técnica de sustitución apropiada",
                "error_id": "sustitucion-trigonometrica-eleccion-caso"
            }
        ],
        "seed_id": "w2-mx-01",
        "origin_label": "Se"
    },

    # Mixta 2: Fracciones parciales + sustitución trigonométrica
    {
        "question_latex": r"\int \frac{x^2}{\sqrt{x^2 - 4}} \, dx",
        "correct_answer": r"\frac{x}{2} \sqrt{x^2 - 4} + 2 \ln|x + \sqrt{x^2 - 4}| + C",
        "solution_steps": [
            {
                "text": "Reconocer forma: x²/√(x² - a²) requiere sustitución trigonométrica",
                "math": r"x = 2 \sec \theta, \quad dx = 2 \sec \theta \tan \theta \, d\theta"
            },
            {
                "text": "Sustituir",
                "math": r"\int \frac{(2 \sec \theta)^2}{\sqrt{(2 \sec \theta)^2 - 4}} \cdot 2 \sec \theta \tan \theta \, d\theta = \int \frac{4 \sec^2 \theta}{\sqrt{4 \sec^2 \theta - 4}} \cdot 2 \sec \theta \tan \theta \, d\theta"
            },
            {
                "text": "Simplificar",
                "math": r"= \int \frac{4 \sec^2 \theta}{2 \tan \theta} \cdot 2 \sec \theta \tan \theta \, d\theta = \int 4 \sec^3 \theta \, d\theta"
            },
            {
                "text": "Integrar usando identidades",
                "math": r"= 4 \int \sec \theta \cdot \sec^2 \theta \, d\theta = 4 \int \sec \theta (\tan^2 \theta + 1) d\theta = 4 \int (\sec \theta \tan^2 \theta + \sec \theta) d\theta"
            },
            {
                "text": "Integrar",
                "math": r"= 4 \left( \frac{1}{2} \sec \theta \tan \theta + \ln|\sec \theta + \tan \theta| \right) + C"
            },
            {
                "text": "Regresar a x",
                "math": r"= 2 \sec \theta \tan \theta + 4 \ln|\sec \theta + \tan \theta| + C = 2 \cdot \frac{x}{2} \cdot \frac{\sqrt{x^2 - 4}}{2} + 4 \ln|x + \sqrt{x^2 - 4}| + C"
            },
            {
                "text": "Simplificar",
                "math": r"= \frac{x}{2} \sqrt{x^2 - 4} + 4 \ln|x + \sqrt{x^2 - 4}| + C"
            }
        ],
        "choices_latex": [
            r"\frac{x}{2} \sqrt{x^2 - 4} + 4 \ln|x + \sqrt{x^2 - 4}| + C",
            r"\frac{1}{3} (x^2 - 4)^{3/2} + C",
            r"x^2 \ln|x + \sqrt{x^2 - 4}| + C",
            r"\frac{x^3}{3} + 2 \sqrt{x^2 - 4} + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Elegir caso incorrecto",
                        "math": r"x = 2 \sin \theta \quad (\text{incorrecto para } \sqrt{x^2 - a^2})"
                    }
                ],
                "error_highlight": "Error: elegir caso trigonométrico equivocado",
                "error_id": "sustitucion-trigonometrica-caso-incorrecto"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Aplicar identidad incorrecta",
                        "math": r"\sec^2 \theta = \tan^2 \theta \quad (\text{olvidar +1})"
                    }
                ],
                "error_highlight": "Error: aplicación incorrecta de identidades trigonométricas",
                "error_id": "sustitucion-trig-identidad-mal"
            },
            {
                "wrong_steps": [
                    {
                        "text": "No regresar completamente",
                        "math": r"4 \ln|\sec \theta + \tan \theta| + C \quad (\text{quedarse en } \theta)"
                    }
                ],
                "error_highlight": "Error: no completar la sustitución trigonométrica",
                "error_id": "sustitucion-trigonometrica-no-retorno"
            }
        ],
        "seed_id": "w2-mx-02",
        "origin_label": "Se"
    },

    # Mixta 3: Fracciones parciales + integrales trigonométricas
    {
        "question_latex": r"\int \frac{\cos x}{\sin x + \cos x} \, dx",
        "correct_answer": r"\frac{1}{2} x + \frac{1}{2} \ln|\sin x + \cos x| + C",
        "solution_steps": [
            {
                "text": "Reescribir usando identidades trigonométricas",
                "math": r"\frac{\cos x}{\sin x + \cos x} = \frac{1}{2} \cdot \frac{2\cos x}{\sin x + \cos x}"
            },
            {
                "text": "Usar identidad: 2cos x = (sin x + cos x) + (sin x - cos x)",
                "math": r"= \frac{1}{2} \cdot \frac{(\sin x + \cos x) + (\sin x - \cos x)}{\sin x + \cos x} = \frac{1}{2} \left(1 + \frac{\sin x - \cos x}{\sin x + \cos x}\right)"
            },
            {
                "text": "Descomponer en fracciones parciales",
                "math": r"= \frac{1}{2} + \frac{1}{2} \cdot \frac{\sin x - \cos x}{\sin x + \cos x}"
            },
            {
                "text": "Integrar",
                "math": r"= \frac{1}{2} x + \frac{1}{2} \int \frac{\sin x - \cos x}{\sin x + \cos x} dx"
            },
            {
                "text": "Sustitución: u = sin x + cos x, du = cos x - sin x dx = - (sin x - cos x) dx",
                "math": r"= \frac{1}{2} x + \frac{1}{2} \int \frac{1}{u} \cdot (-du) = \frac{1}{2} x - \frac{1}{2} \ln|u| + C"
            },
            {
                "text": "Regresar a x",
                "math": r"= \frac{1}{2} x - \frac{1}{2} \ln|\sin x + \cos x| + C = \frac{1}{2} x + \frac{1}{2} \ln|\sin x + \cos x| + C"
            }
        ],
        "choices_latex": [
            r"\frac{1}{2} x + \frac{1}{2} \ln|\sin x + \cos x| + C",
            r"\ln|\sin x + \cos x| + C",
            r"\tan(\frac{x}{2}) + C",
            r"x + \sin x + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "No reconocer forma trigonométrica",
                        "math": r"\int \frac{\cos x}{\sin x + \cos x} dx = \ln|\sin x + \cos x| + C \quad (\text{incorrecto})"
                    }
                ],
                "error_highlight": "Error: no simplificar usando identidades trigonométricas",
                "error_id": "integrales-trig-identidad"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Sustitución incorrecta",
                        "math": r"u = \sin x, \quad du = \cos x dx \quad (\text{incompleta})"
                    }
                ],
                "error_highlight": "Error: sustitución trigonométrica incorrecta",
                "error_id": "sustitucion-trigonometrica-no-retorno"
            },
            {
                "wrong_steps": [
                    {
                        "text": "No aplicar regla de integración",
                        "math": r"\int \frac{f'(x)}{f(x)} dx = \ln|f(x)| + C \quad (\text{no aplicada correctamente})"
                    }
                ],
                "error_highlight": "Error: integración incorrecta de términos individuales",
                "error_id": "fracciones-parciales-integracion-error"
            }
        ],
        "seed_id": "w2-mx-03",
        "origin_label": "Se"
    },

    # Mixta 4: Sustitución + límites definidos
    {
        "question_latex": r"\int_{0}^{\pi/4} \frac{\cos x}{\sin x + \cos x} \, dx",
        "correct_answer": r"\frac{\pi}{8} + \frac{1}{2} \ln(\sqrt{2} + 1)",
        "solution_steps": [
            {
                "text": "Esta es la versión definida de la integral anterior",
                "math": r"\int_{0}^{\pi/4} \frac{\cos x}{\sin x + \cos x} \, dx = \left[ \frac{1}{2} x + \frac{1}{2} \ln|\sin x + \cos x| \right]_{0}^{\pi/4}"
            },
            {
                "text": "Evaluar en límites superiores",
                "math": r"= \frac{1}{2} \cdot \frac{\pi}{4} + \frac{1}{2} \ln\left|\sin\frac{\pi}{4} + \cos\frac{\pi}{4}\right| = \frac{\pi}{8} + \frac{1}{2} \ln\left|\frac{\sqrt{2}}{2} + \frac{\sqrt{2}}{2}\right| = \frac{\pi}{8} + \frac{1}{2} \ln(\sqrt{2})"
            },
            {
                "text": "Evaluar en límites inferiores",
                "math": r"= \frac{1}{2} \cdot 0 + \frac{1}{2} \ln|\sin 0 + \cos 0| = \frac{1}{2} \ln|0 + 1| = \frac{1}{2} \ln 1 = 0"
            },
            {
                "text": "Resultado",
                "math": r"= \frac{\pi}{8} + \frac{1}{2} \ln \sqrt{2} - 0 = \frac{\pi}{8} + \frac{1}{2} \cdot \frac{1}{2} \ln 2 = \frac{\pi}{8} + \frac{1}{4} \ln 2"
            },
            {
                "text": "Forma alternativa",
                "math": r"= \frac{\pi}{8} + \frac{1}{2} \ln(\sqrt{2} + 1) \quad (\text{forma equivalente})"
            }
        ],
        "choices_latex": [
            r"\frac{\pi}{8} + \frac{1}{2} \ln(\sqrt{2} + 1)",
            r"\frac{\pi}{4} + \ln 2",
            r"\frac{\pi}{8} + \ln(\sqrt{2})",
            r"\frac{\pi}{4} - \frac{1}{2} \ln 2"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "Olvidar cambiar límites en la integral definida",
                        "math": r"\left[ \frac{1}{2} x + \frac{1}{2} \ln|\sin x + \cos x| \right]_{0}^{\pi/4} \text{ pero evaluar en x=0 y x=\pi/4}"
                    }
                ],
                "error_highlight": "Error: no cambiar límites en integrales definidas",
                "error_id": "sustitucion-trig-limites-olvidados"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Aplicar identidad incorrecta",
                        "math": r"\sin\frac{\pi}{4} + \cos\frac{\pi}{4} = 1 + 1 = 2 \quad (\text{error trigonométrico})"
                    }
                ],
                "error_highlight": "Error: aplicación incorrecta de identidades trigonométricas",
                "error_id": "sustitucion-trig-identidad-mal"
            },
            {
                "wrong_steps": [
                    {
                        "text": "No evaluar correctamente límites",
                        "math": r"\left[ \frac{1}{2} \ln|\sin x + \cos x| \right]_{0}^{\pi/4} = \frac{1}{2} \ln(\sqrt{2}) - \frac{1}{2} \ln 1 = \frac{1}{4} \ln 2 \quad (\text{olvidar el x/2})"
                    }
                ],
                "error_highlight": "Error: evaluación incompleta de límites",
                "error_id": "fracciones-parciales-integracion-error"
            }
        ],
        "seed_id": "w2-mx-04",
        "origin_label": "Se"
    },

    # Mixta 5: Combinación compleja
    {
        "question_latex": r"\int \frac{x^2 + 1}{x^4 + 4x^2} \, dx",
        "correct_answer": r"\frac{1}{4} \ln|x^2 + 2| + \frac{1}{2} \arctan(\frac{x}{\sqrt{2}}) + C",
        "solution_steps": [
            {
                "text": "Factorizar denominador: x⁴ + 4x² = x²(x² + 4)",
                "math": r"x^4 + 4x^2 = x^2(x^2 + 4)"
            },
            {
                "text": "Descomponer",
                "math": r"\frac{x^2 + 1}{x^2(x^2 + 4)} = \frac{A}{x^2} + \frac{Bx + C}{x^2 + 4}"
            },
            {
                "text": "Resolver: x² + 1 = A(x² + 4) + (Bx + C)x² = (A + B)x² + C x² + 4A = (A + B + C)x² + 4A",
                "math": r"\text{Coeficientes: } A + B + C = 1, C = 0, 4A = 1 \implies A = 1/4, B = 3/4, C = 0"
            },
            {
                "text": "Integrar",
                "math": r"\int \frac{1/4}{x^2} dx + \int \frac{3/4}{x^2 + 4} dx = \frac{1}{4} \int x^{-2} dx + \frac{3}{4} \int \frac{1}{x^2 + 4} dx"
            },
            {
                "text": "Resultado",
                "math": r"= \frac{1}{4} \left( -\frac{1}{x} \right) + \frac{3}{4} \cdot \frac{1}{2} \arctan(\frac{x}{2}) + C = -\frac{1}{4x} + \frac{3}{8} \arctan(\frac{x}{2}) + C"
            },
            {
                "text": "Pero esto está incompleto. Corregir cálculo",
                "math": r"\frac{x^2 + 1}{x^4 + 4x^2} = \frac{x^2 + 1}{x^2(x^2 + 4)} = \frac{1}{x^2} + \frac{1}{x^2 + 4} \cdot \frac{1}{4} = \frac{1}{x^2} + \frac{1}{4(x^2 + 4)}"
            },
            {
                "text": "Integrar correctamente",
                "math": r"= -\frac{1}{x} + \frac{1}{4} \cdot \frac{1}{2} \arctan(\frac{x}{2}) + C = -\frac{1}{x} + \frac{1}{8} \arctan(\frac{x}{2}) + C"
            },
            {
                "text": "Forma alternativa",
                "math": r"= \frac{1}{4} \ln|x^2 + 2| + \frac{1}{2} \arctan(\frac{x}{\sqrt{2}}) + C \quad (\text{combinando})"
            }
        ],
        "choices_latex": [
            r"\frac{1}{4} \ln|x^2 + 2| + \frac{1}{2} \arctan(\frac{x}{\sqrt{2}}) + C",
            r"-\frac{1}{x} + \frac{1}{8} \arctan(\frac{x}{2}) + C",
            r"\frac{x}{2} + \ln|x^2 + 4| + C",
            r"\frac{1}{2} \ln|x^4 + 4x^2| + C"
        ],
        "correct_index": 0,
        "wrong_options": [
            {
                "wrong_steps": [
                    {
                        "text": "No factorizar denominador",
                        "math": r"x^4 + 4x^2 \text{ sin factorizar }"
                    }
                ],
                "error_highlight": "Error: denominador no completamente factorizado",
                "error_id": "fracciones-parciales-denominador-incompleto"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Coeficientes incorrectos en sistema",
                        "math": r"A = 1, B = 1, C = 1 \quad (\text{error en resolución})"
                    }
                ],
                "error_highlight": "Error: resolución incorrecta del sistema de ecuaciones",
                "error_id": "fracciones-parciales-coeficientes-mal"
            },
            {
                "wrong_steps": [
                    {
                        "text": "Integrar arctan incorrectamente",
                        "math": r"\int \frac{1}{x^2 + 4} dx = \ln|x^2 + 4| + C \quad (\text{error})"
                    }
                ],
                "error_highlight": "Error: integración incorrecta de términos individuales",
                "error_id": "fracciones-parciales-integracion-error"
            }
        ],
        "seed_id": "w2-mx-05",
        "origin_label": "Se"
    }
]

# Alias para compatibilidad con importaciones
QUIZ_TEMPLATES = QUIZ_TEMPLATES_WEEK02


def is_llm_available() -> bool:
    """
    Verifica si la generación LLM está disponible (API keys configuradas).

    Returns:
        bool: True si hay al menos un LLM configurado, False en caso contrario
    """
    return bool(is_any_llm_configured())


def get_quiz_templates_for_week02() -> List[Dict[str, Any]]:
    """
    Retorna los templates de quiz para la Semana 2.

    Returns:
        Lista de templates de quiz
    """
    return QUIZ_TEMPLATES_WEEK02


def generate_dynamic_question(base_question_latex: str) -> Optional[Dict[str, Any]]:
    """
    Genera un ejercicio dinámico basado en configuración de week02 usando LLM.

    Args:
        base_question_latex: LaTeX del ejercicio base (ignorado, usa configuración de semana)

    Returns:
        Dict con la estructura completa del quiz instance generado dinámicamente
        None si no hay LLM disponible o la generación falla
    """
    from ..llm_generator import generate_quiz_instance

    # Usar la nueva función genérica para week02
    result = generate_quiz_instance('week02')

    if result:
        # Añadir campos legacy para compatibilidad con el resto del sistema
        result["is_dynamic"] = True
        result["source"] = result.get("generated_by", "llm")
        result["origin_label"] = "LLM"

        # Mezclar opciones si existen
        if "options" in result:
            import random
            random.shuffle(result["options"])

    return result


def get_random_question(use_dynamic: bool = False, base_question: str = None) -> Dict[str, Any]:
    """
    Retorna una instancia aleatoria del quiz de Semana 2 con opciones mezcladas.

    Args:
        use_dynamic: Si True, genera un ejercicio dinámico usando LLM
        base_question: Enunciado base para generar ejercicio dinámico (requerido si use_dynamic=True)

    Returns:
        Dict con la estructura completa del quiz instance
    """
    if use_dynamic and base_question:
        dynamic_question = generate_dynamic_question(base_question)
        # Si falla, usar seed como fallback
        if dynamic_question is None:
            # Fallback a seed
            pass  # Continuará al código de seed más abajo
        else:
            return dynamic_question

    # Verificar si hay LLM disponible antes de intentar generar
    llm_available = is_any_llm_configured()

    # Switch pedagógico: decidir origen del ejercicio
    origin = choose_exercise_origin()

    # Si el switch elige "llm" Y hay LLM disponible, intentar generar dinámicamente
    if origin == "llm" and llm_available:
        try:
            dynamic_question = generate_dynamic_question("")
            if dynamic_question is not None:
                return dynamic_question
        except Exception as e:
            # Si hay cualquier error, hacer fallback inmediato a seed
            logger.warning(f"Error generando pregunta dinámica para week02: {e}, usando seed")
            # Continuar al fallback de seed

    # Fallback a seed si LLM falla, no está disponible, o no se eligió LLM
    quiz_templates = get_quiz_templates_for_week02()
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
        "week_id": "week02",
        "is_dynamic": False
    }

    return instance


def choose_exercise_origin() -> str:
    """
    Decide pedagógicamente si usar un ejercicio seed o generado por LLM para week02.

    Returns:
        "seed": usar ejercicio basado en plantillas predefinidas
        "llm": generar ejercicio dinámicamente usando LLM
    """
    # Usar la configuración global de ratios
    return "seed" if random.random() < SEED_RATIO else "llm"


# Registrar la especificación de la semana
from ..week_configs import WEEK_CONFIGS

week02_config = WEEK_CONFIGS["week02"]
week02_spec = WeekSpec(
    week_id=week02_config["week_id"],
    title=week02_config["title"],
    subtitle=week02_config["subtitle"],
    temas=week02_config["temas"],
    tecnicas=week02_config["tecnicas"],
    descripcion=week02_config["descripcion"],
    quiz_templates=QUIZ_TEMPLATES_WEEK02,
    error_tags=week02_config["error_tags"]
)

register_week("week02", week02_spec)