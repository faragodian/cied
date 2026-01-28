"""Week01 quiz seeds (clean implementation).

Provides get_random_question() returning a quiz instance compatible with templates/quiz.html.
"""

import random
from typing import Dict, Any, List

# Compat flags (algunas semanas importan SEED_RATIO desde quiz_week01)
SEED_RATIO = 0.8
LLM_RATIO = 0.2


QUIZ_TEMPLATES: List[Dict[str, Any]] = [
    # 15 Integración por partes (w1-1 .. w1-15)
    {
        "question_latex": r"\int x e^{x} \, dx",
        "correct_answer": r"e^{x}(x - 1) + C",
        "solution_steps": [
            {"text": r"Aplicamos integración por partes", "math": r"\int u\,dv = uv - \int v\,du"},
            {"text": r"Elegimos u = x, dv = e^{x} dx", "math": r"u=x,\ dv=e^{x}dx"},
            {"text": r"Calculamos v = e^{x}, du = dx", "math": r"v=e^{x},\ du=dx"},
            {"text": r"Aplicamos la fórmula y simplificamos", "math": r"x e^{x} - \int e^{x} dx = x e^{x} - e^{x} + C"},
        ],
        "choices_latex": [
            r"e^{x}(x - 1) + C",
            r"x e^{x} + C",
            r"e^{x}(x + 1) + C",
            r"x e^{x} - e^{x} + C",
        ],
        "correct_index": 0,
        "wrong_options": [
            {"wrong_steps": [{"text": r"Elección inapropiada u/dv", "math": r"u=e^{x},dv=x dx"}], "error_highlight": "Elección de u/dv inapropiada", "error_id": "integracion-partes-eleccion-uv"},
            {"wrong_steps": [{"text": r"Signo mal aplicado", "math": r"\int u dv = uv + \int v du"}], "error_highlight": "Signo incorrecto en la fórmula", "error_id": "integracion-partes-signo-formula"},
            {"wrong_steps": [{"text": r"Derivada de u mal calculada", "math": r"du\neq 2x\,dx"}], "error_highlight": "Cálculo de derivada incorrecto", "error_id": "integracion-partes-derivada-u"},
        ],
        "source": "seed",
        "seed_id": "w1-1",
        "origin_label": "Se",
    },
    {
        "question_latex": r"\int x \sin(x) \, dx",
        "correct_answer": r"-x\cos x + \sin x + C",
        "solution_steps": [
            {"text": r"Integración por partes: u=x, dv=\sin x dx", "math": r"u=x,\ dv=\sin x dx"},
            {"text": r"v = -\cos x, du = dx", "math": r"v=-\cos x,\ du=dx"},
            {"text": r"Aplicamos la fórmula y simplificamos", "math": r"-x\cos x + \sin x + C"},
        ],
        "choices_latex": [
            r"-x\cos x + \sin x + C",
            r"x\cos x + C",
            r"\sin x - x\sin x + C",
            r"x(-\cos x) + C",
        ],
        "correct_index": 0,
        "wrong_options": [
            {"wrong_steps": [{"text": r"Intercambio u/dv", "math": r"u=\sin x,\ dv=x dx"}], "error_highlight": "Elección errónea de u/dv", "error_id": "integracion-partes-eleccion-uv"},
            {"wrong_steps": [{"text": r"Se olvidó signo en v", "math": r"v=\cos x en lugar de -\cos x"}], "error_highlight": "Signo omitido en antiderivada", "error_id": "integracion-partes-signo-formula"},
            {"wrong_steps": [{"text": r"Integral mal resuelta", "math": r"\int\cos x dx \neq -\sin x"}], "error_highlight": "Integración incorrecta", "error_id": "integracion-partes-innecesaria"},
        ],
        "source": "seed",
        "seed_id": "w1-2",
        "origin_label": "Se",
    },
    {
        "question_latex": r"\int \ln(x) \, dx",
        "correct_answer": r"x\ln x - x + C",
        "solution_steps": [
            {"text": r"Elegimos u=\ln x, dv=dx", "math": r"u=\ln x,\ dv=dx"},
            {"text": r"v=x, du=dx/x", "math": r"v=x,\ du=dx/x"},
            {"text": r"Aplicamos la fórmula y simplificamos", "math": r"x\ln x - \int 1\,dx = x\ln x - x + C"},
        ],
        "choices_latex": [
            r"x\ln x - x + C",
            r"\ln x + C",
            r"x\ln x + C",
            r"\frac{1}{2}(\ln x)^2 + C",
        ],
        "correct_index": 0,
        "wrong_options": [
            {"wrong_steps": [{"text": r"Omitió integral restante", "math": r"\int 1 dx = 0"}], "error_highlight": "Olvido de la integral restante", "error_id": "integracion-partes-innecesaria"},
            {"wrong_steps": [{"text": r"Confusión u/dv", "math": r"u=1,\ dv=\ln x dx"}], "error_highlight": "Elección incorrecta u/dv", "error_id": "integracion-partes-eleccion-uv"},
            {"wrong_steps": [{"text": r"Resultado sin -x", "math": r"faltó -x"}], "error_highlight": "Falta término -x", "error_id": "integracion-partes-derivada-u"},
        ],
        "source": "seed",
        "seed_id": "w1-3",
        "origin_label": "Se",
    },
    {
        "question_latex": r"\int x e^{2x} \, dx",
        "correct_answer": r"\frac{e^{2x}}{2}(x - \tfrac{1}{2}) + C",
        "solution_steps": [
            {"text": r"Integración por partes: u=x, dv=e^{2x}dx", "math": r"u=x,\ dv=e^{2x}dx"},
            {"text": r"v=\tfrac{1}{2}e^{2x}, du=dx", "math": r"v=\tfrac{1}{2}e^{2x},\ du=dx"},
            {"text": r"Aplicamos la fórmula y simplificamos", "math": r"x\cdot\tfrac{e^{2x}}{2}-\tfrac{1}{2}\int e^{2x}dx = \tfrac{e^{2x}}{2}(x-\tfrac{1}{2})+C"},
        ],
        "choices_latex": [
            r"\frac{e^{2x}}{2}\left(x-\tfrac{1}{2}\right)+C",
            r"\tfrac{e^{2x}}{4}(2x-1)+C",
            r"x e^{2x} + C",
            r"\frac{e^{2x}}{2}x + C",
        ],
        "correct_index": 0,
        "wrong_options": [
            {"wrong_steps": [{"text": r"No dividir por 2 en v", "math": r"v=e^{2x} (olvido\ \tfrac{1}{2})"}], "error_highlight": "Error en constante de v", "error_id": "integracion-partes-derivada-u"},
            {"wrong_steps": [{"text": r"Olvidó restar integral", "math": r"no\ se\ restó\ \tfrac{1}{2}\int e^{2x}dx"}], "error_highlight": "Paso incompleto", "error_id": "integracion-partes-innecesaria"},
            {"wrong_steps": [{"text": r"Resultado inventado", "math": r"\text{sin verificación}"}], "error_highlight": "Antiderivada inventada", "error_id": "integracion-partes-antiderivada-inventada"},
        ],
        "source": "seed",
        "seed_id": "w1-4",
        "origin_label": "Se",
    },
    {
        "question_latex": r"\int x^2 e^{x} \, dx",
        "correct_answer": r"e^{x}(x^2-2x+2)+C",
        "solution_steps": [
            {"text": r"Aplicar integración por partes dos veces", "math": r"\int x^2 e^{x}dx = x^2 e^{x} - \int 2x e^{x}dx"},
            {"text": r"Integrar segunda parte por partes", "math": r"\int 2x e^{x}dx = 2(x e^{x}-e^{x})"},
            {"text": r"Combinar y simplificar", "math": r"e^{x}(x^2-2x+2)+C"},
        ],
        "choices_latex": [
            r"e^{x}(x^2-2x+2)+C",
            r"e^{x}(x^2-2x)+C",
            r"x^2 e^{x} + C",
            r"\frac{e^{x}}{2}(x^2-2x+2)+C",
        ],
        "correct_index": 0,
        "wrong_options": [
            {"wrong_steps": [{"text": r"Omitió segunda integración por partes", "math": r"se\ dejó\  \int 2x e^{x}dx\ sin\ resolver"}], "error_highlight": "Paso omitido", "error_id": "integracion-partes-innecesaria"},
            {"wrong_steps": [{"text": r"Falló en combinaciones", "math": r"errores\ en\ algebra\ al\ combinar\ términos"}], "error_highlight": "Error algebraico", "error_id": "integracion-partes-derivada-u"},
            {"wrong_steps": [{"text": r"Resultado inventado", "math": r"\text{sin verificación}"}], "error_highlight": "Antiderivada inventada", "error_id": "integracion-partes-antiderivada-inventada"},
        ],
        "source": "seed",
        "seed_id": "w1-5",
        "origin_label": "Se",
    },
    {
        "question_latex": r"\int e^{x}\cos x \, dx",
        "correct_answer": r"\tfrac{1}{2}e^{x}(\sin x + \cos x) + C",
        "solution_steps": [
            {"text": r"Uso de partes cíclicas o resolver sistema", "math": r"I=\int e^{x}\cos x dx"},
            {"text": r"Integrar por partes y resolver para I", "math": r"I = e^{x}\cos x + e^{x}\sin x - I \Rightarrow 2I = e^{x}(\sin x + \cos x)"},
            {"text": r"Despejar I", "math": r"I=\tfrac{1}{2}e^{x}(\sin x + \cos x) + C"},
        ],
        "choices_latex": [
            r"\tfrac{1}{2}e^{x}(\sin x + \cos x) + C",
            r"e^{x}(\sin x - \cos x) + C",
            r"e^{x}\cos x + C",
            r"-\tfrac{1}{2}e^{x}(\sin x + \cos x) + C",
        ],
        "correct_index": 0,
        "wrong_options": [
            {"wrong_steps": [{"text": r"No resolvió el sistema cíclico", "math": r"se\ dejó\ I\ en\ ambos\ lados"}], "error_highlight": "No resolver ciclo", "error_id": "integracion-partes-innecesaria"},
            {"wrong_steps": [{"text": r"Signo equivocado al despejar", "math": r"error\ de\ algebra\ al\ despejar"}], "error_highlight": "Signo algebraico incorrecto", "error_id": "integracion-partes-signo-formula"},
            {"wrong_steps": [{"text": r"Antiderivada inventada", "math": r"\text{sin verificación}"}], "error_highlight": "Antiderivada inventada", "error_id": "integracion-partes-antiderivada-inventada"},
        ],
        "source": "seed",
        "seed_id": "w1-6",
        "origin_label": "Se",
    },
    {
        "question_latex": r"\int x\ln(x) \, dx",
        "correct_answer": r"\tfrac{x^{2}}{2}\ln x - \tfrac{x^{2}}{4} + C",
        "solution_steps": [
            {"text": r"u=\ln x, dv = x dx", "math": r"u=\ln x,\ dv=x dx"},
            {"text": r"du=dx/x, v=\tfrac{x^{2}}{2}", "math": r"du=\tfrac{dx}{x},\ v=\tfrac{x^{2}}{2}"},
            {"text": r"Aplicar la fórmula y simplificar", "math": r"\tfrac{x^{2}}{2}\ln x - \tfrac{1}{2}\int x dx = \tfrac{x^{2}}{2}\ln x - \tfrac{x^{2}}{4} + C"},
        ],
        "choices_latex": [
            r"\tfrac{x^{2}}{2}\ln x - \tfrac{x^{2}}{4} + C",
            r"x^{2}\ln x + C",
            r"\ln x + C",
            r"\tfrac{x^{2}}{2}\ln x + \tfrac{x^{2}}{4} + C",
        ],
        "correct_index": 0,
        "wrong_options": [
            {"wrong_steps": [{"text": r"No calc. v correctamente", "math": r"v\neq \tfrac{x^{2}}{2}"}], "error_highlight": "Error en v", "error_id": "integracion-partes-derivada-u"},
            {"wrong_steps": [{"text": r"Olvidó restar integral", "math": r"se\ omitió\ -\tfrac{1}{2}\int x dx"}], "error_highlight": "Paso omitido", "error_id": "integracion-partes-innecesaria"},
            {"wrong_steps": [{"text": r"Resultado sin simplificar", "math": r"no\ simplificó\ términos"}], "error_highlight": "Falta simplificación", "error_id": "integracion-partes-antiderivada-inventada"},
        ],
        "source": "seed",
        "seed_id": "w1-7",
        "origin_label": "Se",
    },
    {
        "question_latex": r"\int x\cos(2x) \, dx",
        "correct_answer": r"\tfrac{\cos(2x)}{4} + \tfrac{x\sin(2x)}{2} + C",
        "solution_steps": [
            {"text": r"u=x, dv=\cos2x dx", "math": r"u=x,\ dv=\cos2x dx"},
            {"text": r"v=\tfrac{1}{2}\sin2x, du=dx", "math": r"v=\tfrac{1}{2}\sin2x,\ du=dx"},
            {"text": r"Aplicar partes y simplificar", "math": r"x\cdot\tfrac{1}{2}\sin2x - \tfrac{1}{2}\int \sin2x dx = \tfrac{x\sin2x}{2} + \tfrac{\cos2x}{4} + C"},
        ],
        "choices_latex": [
            r"\tfrac{\cos2x}{4} + \tfrac{x\sin2x}{2} + C",
            r"\tfrac{x\cos2x}{2} + C",
            r"\sin2x + C",
            r"-\tfrac{\cos2x}{4} + \tfrac{x\sin2x}{2} + C",
        ],
        "correct_index": 0,
        "wrong_options": [
            {"wrong_steps": [{"text": r"v calculado sin 1/2", "math": r"v=\sin2x (olvido\ \tfrac{1}{2})"}], "error_highlight": "Error en v", "error_id": "integracion-partes-derivada-u"},
            {"wrong_steps": [{"text": r"No integró sin2x correctamente", "math": r"\int\sin2x dx \neq -\cos2x"}], "error_highlight": "Integración incorrecta", "error_id": "integracion-partes-innecesaria"},
            {"wrong_steps": [{"text": r"Signo equivocado", "math": r"error\ de\ signo\ al\ simplificar"}], "error_highlight": "Signo incorrecto", "error_id": "integracion-partes-signo-formula"},
        ],
        "source": "seed",
        "seed_id": "w1-8",
        "origin_label": "Se",
    },
    {
        "question_latex": r"\int x e^{3x} \, dx",
        "correct_answer": r"\tfrac{e^{3x}}{3}(x - \tfrac{1}{3}) + C",
        "solution_steps": [
            {"text": r"u=x, dv=e^{3x}dx", "math": r"u=x,\ dv=e^{3x}dx"},
            {"text": r"v=\tfrac{1}{3}e^{3x}, du=dx", "math": r"v=\tfrac{1}{3}e^{3x},\ du=dx"},
            {"text": r"Aplicamos partes y simplificamos", "math": r"x\cdot\tfrac{e^{3x}}{3}-\tfrac{1}{3}\int e^{3x}dx = \tfrac{e^{3x}}{3}(x-\tfrac{1}{3})+C"},
        ],
        "choices_latex": [
            r"\tfrac{e^{3x}}{3}(x-\tfrac{1}{3})+C",
            r"x e^{3x} + C",
            r"\tfrac{e^{3x}}{9}(3x-1)+C",
            r"\tfrac{e^{3x}}{2}(x-\tfrac{1}{2})+C",
        ],
        "correct_index": 0,
        "wrong_options": [
            {"wrong_steps": [{"text": r"Olvidó factor 1/3 en v", "math": r"v=e^{3x} (olvido\ \tfrac{1}{3})"}], "error_highlight": "Error en constante de v", "error_id": "integracion-partes-derivada-u"},
            {"wrong_steps": [{"text": r"No restó la integral", "math": r"no\ restó\ \tfrac{1}{3}\int e^{3x}dx"}], "error_highlight": "Paso omitido", "error_id": "integracion-partes-innecesaria"},
            {"wrong_steps": [{"text": r"Resultado inventado", "math": r"\text{sin verificación}"}], "error_highlight": "Antiderivada inventada", "error_id": "integracion-partes-antiderivada-inventada"},
        ],
        "source": "seed",
        "seed_id": "w1-9",
        "origin_label": "Se",
    },
    {
        "question_latex": r"\int x^2 \sin x \, dx",
        "correct_answer": r"-x^2\cos x + 2x\sin x + 2\cos x + C",
        "solution_steps": [
            {"text": r"Integración por partes repetida", "math": r"\int x^2\sin x dx = -x^2\cos x + 2\int x\cos x dx"},
            {"text": r"Integrar la segunda por partes", "math": r"\int x\cos x dx = x\sin x + \cos x + C"},
            {"text": r"Combinar resultados", "math": r"-x^2\cos x + 2x\sin x + 2\cos x + C"},
        ],
        "choices_latex": [
            r"-x^2\cos x + 2x\sin x + 2\cos x + C",
            r"x^2\cos x + C",
            r"-x^2\cos x + x\sin x + C",
            r"-x^2\cos x + 2x\sin x - 2\cos x + C",
        ],
        "correct_index": 0,
        "wrong_options": [
            {"wrong_steps": [{"text": r"Omitió una integración por partes", "math": r"se\ omitió\ integrar\ x\cos x"}], "error_highlight": "Paso omitido", "error_id": "integracion-partes-innecesaria"},
            {"wrong_steps": [{"text": r"Se perdió un signo", "math": r"error\ de\ signo\ al\ combinar"}], "error_highlight": "Signo incorrecto", "error_id": "integracion-partes-signo-formula"},
            {"wrong_steps": [{"text": r"Resultado inventado", "math": r"\text{sin verificación}"}], "error_highlight": "Antiderivada inventada", "error_id": "integracion-partes-antiderivada-inventada"},
        ],
        "source": "seed",
        "seed_id": "w1-10",
        "origin_label": "Se",
    },
    # 15 Integrales trigonométricas (w1-11 .. w1-25)
    {
        "question_latex": r"\int \sin^{2}x \, dx",
        "correct_answer": r"\tfrac{x}{2} - \tfrac{\sin 2x}{4} + C",
        "solution_steps": [
            {"text": r"Usar identidad: sin^2 x = (1 - cos 2x)/2", "math": r"\sin^2 x=\tfrac{1-\cos 2x}{2}"},
            {"text": r"Integrar término a término", "math": r"\int\sin^2 x dx = \tfrac{1}{2}\int dx - \tfrac{1}{2}\int\cos2x dx"},
            {"text": r"Resultado final", "math": r"\tfrac{x}{2} - \tfrac{\sin 2x}{4} + C"},
        ],
        "choices_latex": [
            r"\tfrac{x}{2} - \tfrac{\sin 2x}{4} + C",
            r"-\tfrac{x}{2} + \tfrac{\sin 2x}{4} + C",
            r"\sin x + C",
            r"\tfrac{1-\cos x}{2} + C",
        ],
        "correct_index": 0,
        "wrong_options": [
            {"wrong_steps": [{"text": r"No aplicó identidad", "math": r"\sin^2 x\rightarrow\sin x (incorrecto)"}], "error_highlight": "No uso de identidad", "error_id": "integrales-trig-identidad"},
            {"wrong_steps": [{"text": r"Error integrando cos2x", "math": r"\int\cos2x dx = \sin2x? (falta factor)"}], "error_highlight": "Integración de cos2x incorrecta", "error_id": "integrales-trig-paridad"},
            {"wrong_steps": [{"text": r"Resultado inventado", "math": r"\text{sin verificación}"}], "error_highlight": "Antiderivada inventada", "error_id": "integracion-partes-antiderivada-inventada"},
        ],
        "source": "seed",
        "seed_id": "w1-11",
        "origin_label": "Se",
    },
    {
        "question_latex": r"\int \cos^{2}x \, dx",
        "correct_answer": r"\tfrac{x}{2} + \tfrac{\sin 2x}{4} + C",
        "solution_steps": [
            {"text": r"Usar identidad: cos^2 x = (1 + cos 2x)/2", "math": r"\cos^2 x=\tfrac{1+\cos 2x}{2}"},
            {"text": r"Integrar y simplificar", "math": r"\tfrac{x}{2} + \tfrac{\sin 2x}{4} + C"},
        ],
        "choices_latex": [
            r"\tfrac{x}{2} + \tfrac{\sin 2x}{4} + C",
            r"\tfrac{x}{2} - \tfrac{\sin 2x}{4} + C",
            r"\cos x + C",
            r"\sin x + C",
        ],
        "correct_index": 0,
        "wrong_options": [
            {"wrong_steps": [{"text": r"Identidad mal aplicada", "math": r"cos^2 x -> (1-cos2x)/2 (incorrecto)"}], "error_highlight": "Identidad incorrecta", "error_id": "integrales-trig-identidad"},
            {"wrong_steps": [{"text": r"Error al integrar cos2x", "math": r"\int\cos2x dx = 2\sin2x (factor incorrecto)"}], "error_highlight": "Factor en integración", "error_id": "integrales-trig-paridad"},
            {"wrong_steps": [{"text": r"Resultado inventado", "math": r"\text{sin verificación}"}], "error_highlight": "Antiderivada inventada", "error_id": "integracion-partes-antiderivada-inventada"},
        ],
        "source": "seed",
        "seed_id": "w1-12",
        "origin_label": "Se",
    },
    {
        "question_latex": r"\int \sin^{3}x \, dx",
        "correct_answer": r"-\tfrac{1}{3}\cos^{3}x + C (equivalente)",
        "solution_steps": [
            {"text": r"Usar \u201csustitución\u201d u=\cos x, du=-\sin x dx o identidad", "math": r"\sin^3 x=(1-\cos^2 x)\sin x"},
            {"text": r"Sustituir y integrar", "math": r"\int (1-\cos^2 x)\sin x dx = -\cos x + \tfrac{1}{3}\cos^3 x + C"},
        ],
        "choices_latex": [
            r"-\tfrac{1}{3}\cos^{3}x + C",
            r"\tfrac{1}{3}\cos^{3}x + C",
            r"\sin x + C",
            r"-\cos x + C",
        ],
        "correct_index": 0,
        "wrong_options": [
            {"wrong_steps": [{"text": r"No usó identidad de reducción", "math": r"se\ intentó\ integrar\ sin\ sustituir"}], "error_highlight": "No simplificó la potencia", "error_id": "integrales-trig-identidad"},
            {"wrong_steps": [{"text": r"Sustitución mal hecha", "math": r"u=\sin x (incorrecto)"}], "error_highlight": "Sustitución incorrecta", "error_id": "integrales-trig-sustitucion-signo"},
            {"wrong_steps": [{"text": r"Resultado inventado", "math": r"\text{sin verificación}"}], "error_highlight": "Antiderivada inventada", "error_id": "integracion-partes-antiderivada-inventada"},
        ],
        "source": "seed",
        "seed_id": "w1-13",
        "origin_label": "Se",
    },
    {
        "question_latex": r"\int \cos^{3}x \, dx",
        "correct_answer": r"\tfrac{\sin x}{3} + \tfrac{\sin x \cos^{2}x}{3} + C (forma equivalente)",
        "solution_steps": [
            {"text": r"Usar identidad y sustitución u=\sin x o split", "math": r"\cos^3 x = \cos x(1-\sin^2 x)"},
            {"text": r"Integrar término a término", "math": r"\int \cos x dx - \int \cos x \sin^2 x dx = \sin x - \tfrac{1}{3}\sin^3 x + C"},
        ],
        "choices_latex": [
            r"\sin x - \tfrac{1}{3}\sin^{3}x + C",
            r"\tfrac{1}{3}\cos^{3}x + C",
            r"\cos x + C",
            r"-\sin x + C",
        ],
        "correct_index": 0,
        "wrong_options": [
            {"wrong_steps": [{"text": r"No usó la identidad correcta", "math": r"no\ separar\ cos^3x"}], "error_highlight": "No uso de identidad", "error_id": "integrales-trig-identidad"},
            {"wrong_steps": [{"text": r"Error al integrar sin^3", "math": r"\int\sin^3 x dx mal calculado"}], "error_highlight": "Integración polinomial incorrecta", "error_id": "integracion-partes-innecesaria"},
            {"wrong_steps": [{"text": r"Resultado inventado", "math": r"\text{sin verificación}"}], "error_highlight": "Antiderivada inventada", "error_id": "integracion-partes-antiderivada-inventada"},
        ],
        "source": "seed",
        "seed_id": "w1-14",
        "origin_label": "Se",
    },
    {
        "question_latex": r"\int \sin x \cos x \, dx",
        "correct_answer": r"\tfrac{1}{2}\sin^{2}x + C",
        "solution_steps": [
            {"text": r"Usar sustitución u=\sin x, du=\cos x dx", "math": r"u=\sin x,\ du=\cos x dx"},
            {"text": r"Transformar la integral", "math": r"\int u\,du = \tfrac{1}{2}u^{2} + C"},
            {"text": r"Volver a x", "math": r"\tfrac{1}{2}\sin^{2}x + C"},
        ],
        "choices_latex": [
            r"\tfrac{1}{2}\sin^{2}x + C",
            r"\sin x + C",
            r"\cos x + C",
            r"\tfrac{1}{2}\cos^{2}x + C",
        ],
        "correct_index": 0,
        "wrong_options": [
            {"wrong_steps": [{"text": r"No hizo sustitución", "math": r"no\ identificar\ u=\sin x"}], "error_highlight": "No sustituyó", "error_id": "integrales-trig-sustitucion-signo"},
            {"wrong_steps": [{"text": r"Integró mal", "math": r"\int u du = u + C (incorrecto)"}], "error_highlight": "Error en regla de potencias", "error_id": "integrales-trig-paridad"},
            {"wrong_steps": [{"text": r"Resultado inventado", "math": r"\text{sin verificación}"}], "error_highlight": "Antiderivada inventada", "error_id": "integracion-partes-antiderivada-inventada"},
        ],
        "source": "seed",
        "seed_id": "w1-15",
        "origin_label": "Se",
    },
    {
        "question_latex": r"\int \tan x \sec^{2}x \, dx",
        "correct_answer": r"\tfrac{1}{2}\tan^{2}x + C",
        "solution_steps": [
            {"text": r"Sustitución u=\tan x, du=\sec^{2}x dx", "math": r"u=\tan x,\ du=\sec^{2}x dx"},
            {"text": r"Integrar u du", "math": r"\int u du = \tfrac{1}{2}u^{2} + C"},
            {"text": r"Volver a x", "math": r"\tfrac{1}{2}\tan^{2}x + C"},
        ],
        "choices_latex": [
            r"\tfrac{1}{2}\tan^{2}x + C",
            r"\tan x + C",
            r"\sec x + C",
            r"\tfrac{1}{2}\sec^{2}x + C",
        ],
        "correct_index": 0,
        "wrong_options": [
            {"wrong_steps": [{"text": r"No identificó u correctamente", "math": r"no\ uso\ u=\tan x"}], "error_highlight": "Sustitución fallida", "error_id": "integrales-trig-sustitucion-signo"},
            {"wrong_steps": [{"text": r"Integró mal u du", "math": r"\int u du = u + C (incorrecto)"}], "error_highlight": "Regla de potencias mal aplicada", "error_id": "integrales-trig-paridad"},
            {"wrong_steps": [{"text": r"Resultado inventado", "math": r"\text{sin verificación}"}], "error_highlight": "Antiderivada inventada", "error_id": "integracion-partes-antiderivada-inventada"},
        ],
        "source": "seed",
        "seed_id": "w1-16",
        "origin_label": "Se",
    },
    {
        "question_latex": r"\int \sec^{2}x \, dx",
        "correct_answer": r"\tan x + C",
        "solution_steps": [
            {"text": r"Reconocer derivada de tan x", "math": r"\frac{d}{dx}\tan x = \sec^{2}x"},
            {"text": r"Integrar directo", "math": r"\int \sec^{2}x dx = \tan x + C"},
        ],
        "choices_latex": [
            r"\tan x + C",
            r"\sec x + C",
            r"\sin x + C",
            r"-\tan x + C",
        ],
        "correct_index": 0,
        "wrong_options": [
            {"wrong_steps": [{"text": r"Confundió derivadas", "math": r"pensó\ que\ d/dx\ sec x = sec^2 x"}], "error_highlight": "Confusión de derivadas", "error_id": "integrales-trig-paridad"},
            {"wrong_steps": [{"text": r"Intentó sustitución innecesaria", "math": r"intentar\ u-sub\ no\ necesario"}], "error_highlight": "Sustitución innecesaria", "error_id": "integrales-trig-identidad"},
            {"wrong_steps": [{"text": r"Resultado inventado", "math": r"\text{sin verificación}"}], "error_highlight": "Antiderivada inventada", "error_id": "integracion-partes-antiderivada-inventada"},
        ],
        "source": "seed",
        "seed_id": "w1-17",
        "origin_label": "Se",
    },
    {
        "question_latex": r"\int \sin(2x)\cos(3x) \, dx",
        "correct_answer": r"\tfrac{1}{5}\sin(5x) + \tfrac{1}{1}\sin(-x) + C (expressions equivalent)",
        "solution_steps": [
            {"text": r"Usar producto a suma: sin a cos b = ...", "math": r"\sin A \cos B = \tfrac{1}{2}[\sin(A+B)+\sin(A-B)]"},
            {"text": r"Aplicar identidad y simplificar", "math": r"\tfrac{1}{2}[\sin5x + \sin(-x)] = \tfrac{1}{2}\sin5x - \tfrac{1}{2}\sin x"},
            {"text": r"Integrar término a término", "math": r"\int \tfrac{1}{2}\sin5x dx - \int \tfrac{1}{2}\sin x dx = -\tfrac{1}{10}\cos5x + \tfrac{1}{2}\cos x + C (formas equivalentes)"},
        ],
        "choices_latex": [
            r"-\tfrac{1}{10}\cos5x + \tfrac{1}{2}\cos x + C",
            r"\tfrac{1}{5}\sin5x + C",
            r"\sin(2x)\sin(3x) + C",
            r"\cos(5x) + C",
        ],
        "correct_index": 0,
        "wrong_options": [
            {"wrong_steps": [{"text": r"No aplicó producto a suma", "math": r"no\ transformó\ el\ producto"}], "error_highlight": "No usó identidad trigonométrica", "error_id": "integrales-trig-identidad"},
            {"wrong_steps": [{"text": r"Integró mal términos resultantes", "math": r"errores\ en\ integrar\ sin5x"}], "error_highlight": "Integración incorrecta", "error_id": "integrales-trig-paridad"},
            {"wrong_steps": [{"text": r"Resultado inventado", "math": r"\text{sin verificación}"}], "error_highlight": "Antiderivada inventada", "error_id": "integracion-partes-antiderivada-inventada"},
        ],
        "source": "seed",
        "seed_id": "w1-18",
        "origin_label": "Se",
    },
    {
        "question_latex": r"\int \sin^{4}x \, dx",
        "correct_answer": r"\tfrac{3x}{8} - \tfrac{1}{4}\sin 2x + \tfrac{1}{32}\sin 4x + C",
        "solution_steps": [
            {"text": r"Usar identidad de potencia reducida: sin^4 x = (3-4cos2x+cos4x)/8", "math": r"\sin^4 x = \tfrac{3-4\cos2x+\cos4x}{8}"},
            {"text": r"Integrar término a término", "math": r"\int ... dx = \tfrac{3x}{8} - \tfrac{1}{4}\sin2x + \tfrac{1}{32}\sin4x + C"},
        ],
        "choices_latex": [
            r"\tfrac{3x}{8} - \tfrac{1}{4}\sin 2x + \tfrac{1}{32}\sin 4x + C",
            r"\tfrac{x}{2} - \tfrac{\sin2x}{2} + C",
            r"\sin^2 x + C",
            r"\tfrac{3x}{8} + C",
        ],
        "correct_index": 0,
        "wrong_options": [
            {"wrong_steps": [{"text": r"No aplicó identidad de reducción", "math": r"no\ usar\ identidades"}], "error_highlight": "No uso de identidad", "error_id": "integrales-trig-identidad"},
            {"wrong_steps": [{"text": r"Error integrando cos4x", "math": r"fallo\ en\ integrar\ cos4x"}], "error_highlight": "Integración incorrecta", "error_id": "integrales-trig-paridad"},
            {"wrong_steps": [{"text": r"Resultado inventado", "math": r"\text{sin verificación}"}], "error_highlight": "Antiderivada inventada", "error_id": "integracion-partes-antiderivada-inventada"},
        ],
        "source": "seed",
        "seed_id": "w1-19",
        "origin_label": "Se",
    },
    {
        "question_latex": r"\int \cos^{3}x \sin x \, dx",
        "correct_answer": r"-\tfrac{\cos^{4}x}{4} + C",
        "solution_steps": [
            {"text": r"Sustitución u=\cos x, du=-\sin x dx", "math": r"u=\cos x,\ du=-\sin x dx"},
            {"text": r"Transformar integral", "math": r"\int \cos^3 x \sin x dx = -\int u^3 du = -\tfrac{u^4}{4} + C"},
            {"text": r"Volver a x", "math": r"-\tfrac{\cos^4 x}{4} + C"},
        ],
        "choices_latex": [
            r"-\tfrac{\cos^{4}x}{4} + C",
            r"\tfrac{\cos^{4}x}{4} + C",
            r"\cos^3 x + C",
            r"\sin x + C",
        ],
        "correct_index": 0,
        "wrong_options": [
            {"wrong_steps": [{"text": r"Sustitución errónea", "math": r"u=\sin x (incorrecto)"}], "error_highlight": "Sustitución incorrecta", "error_id": "sustitucion-trigonometrica-eleccion-caso"},
            {"wrong_steps": [{"text": r"Olvidó el signo de du", "math": r"du=-\sin x dx omitido"}], "error_highlight": "Signo perdido en sustitución", "error_id": "integrales-trig-sustitucion-signo"},
            {"wrong_steps": [{"text": r"Resultado inventado", "math": r"\text{sin verificación}"}], "error_highlight": "Antiderivada inventada", "error_id": "integracion-partes-antiderivada-inventada"},
        ],
        "source": "seed",
        "seed_id": "w1-20",
        "origin_label": "Se",
    },
    {
        "question_latex": r"\int \sin(3x)\sin(2x) \, dx",
        "correct_answer": r"-\tfrac{1}{2}\left(\tfrac{\cos x}{1} - \tfrac{\cos 5x}{5}\right) + C (equiv.)",
        "solution_steps": [
            {"text": r"Usar producto a suma", "math": r"\sin A \sin B = \tfrac{1}{2}[\cos(A-B)-\cos(A+B)]"},
            {"text": r"Integrar términos resultantes", "math": r"\tfrac{1}{2}\int \cos x dx - \tfrac{1}{2}\int \cos5x dx = \tfrac{1}{2}\sin x - \tfrac{1}{10}\sin5x + C"},
        ],
        "choices_latex": [
            r"\tfrac{1}{2}\sin x - \tfrac{1}{10}\sin5x + C",
            r"\cos 5x + C",
            r"\sin(3x+2x) + C",
            r"\tfrac{1}{2}\cos x + C",
        ],
        "correct_index": 0,
        "wrong_options": [
            {"wrong_steps": [{"text": r"No aplicó producto a suma", "math": r"no\ convertir\ producto"}], "error_highlight": "No uso de identidad", "error_id": "integrales-trig-identidad"},
            {"wrong_steps": [{"text": r"Error integrando cos5x", "math": r"\int\cos5x dx mal"}], "error_highlight": "Error en integración", "error_id": "integrales-trig-paridad"},
            {"wrong_steps": [{"text": r"Resultado inventado", "math": r"\text{sin verificación}"}], "error_highlight": "Antiderivada inventada", "error_id": "integracion-partes-antiderivada-inventada"},
        ],
        "source": "seed",
        "seed_id": "w1-21",
        "origin_label": "Se",
    },
    {
        "question_latex": r"\int \sec x \tan x \, dx",
        "correct_answer": r"\sec x + C",
        "solution_steps": [
            {"text": r"Reconocer derivada de sec x", "math": r"\frac{d}{dx}\sec x = \sec x \tan x"},
            {"text": r"Integrar directo", "math": r"\int \sec x \tan x dx = \sec x + C"},
        ],
        "choices_latex": [
            r"\sec x + C",
            r"\tan x + C",
            r"\ln|\sec x + \tan x| + C",
            r"-\sec x + C",
        ],
        "correct_index": 0,
        "wrong_options": [
            {"wrong_steps": [{"text": r"Confundió la derivada", "math": r"pensó\ que\ d/dx\sec x = \tan x"}], "error_highlight": "Confusión de derivadas", "error_id": "integrales-trig-paridad"},
            {"wrong_steps": [{"text": r"Intentó u-sub innecesaria", "math": r"u=\sec x (no ayuda)"}], "error_highlight": "Sustitución innecesaria", "error_id": "integrales-trig-sustitucion-signo"},
            {"wrong_steps": [{"text": r"Resultado inventado", "math": r"\text{sin verificación}"}], "error_highlight": "Antiderivada inventada", "error_id": "integracion-partes-antiderivada-inventada"},
        ],
        "source": "seed",
        "seed_id": "w1-22",
        "origin_label": "Se",
    },
    {
        "question_latex": r"\int \csc^{2}x \, dx",
        "correct_answer": r"-\cot x + C",
        "solution_steps": [
            {"text": r"Reconocer derivada de -cot x", "math": r"\frac{d}{dx}\cot x = -\csc^{2}x"},
            {"text": r"Integrar directo", "math": r"\int \csc^{2}x dx = -\cot x + C"},
        ],
        "choices_latex": [
            r"-\cot x + C",
            r"\cot x + C",
            r"\csc x + C",
            r"\tan x + C",
        ],
        "correct_index": 0,
        "wrong_options": [
            {"wrong_steps": [{"text": r"Confundió signo", "math": r"usó\ +\cot x en lugar de -\cot x"}], "error_highlight": "Signo invertido", "error_id": "integrales-trig-paridad"},
            {"wrong_steps": [{"text": r"Confusión de funciones", "math": r"pensó\ que\ integral\ de\ csc^2 = csc"}], "error_highlight": "Confusión de funciones", "error_id": "integrales-trig-identidad"},
            {"wrong_steps": [{"text": r"Resultado inventado", "math": r"\text{sin verificación}"}], "error_highlight": "Antiderivada inventada", "error_id": "integracion-partes-antiderivada-inventada"},
        ],
        "source": "seed",
        "seed_id": "w1-23",
        "origin_label": "Se",
    },
    {
        "question_latex": r"\int \sin(\tfrac{x}{2}) \, dx",
        "correct_answer": r"-2\cos(\tfrac{x}{2}) + C",
        "solution_steps": [
            {"text": r"Sustitución u=x/2, du=dx/2", "math": r"u=\tfrac{x}{2},\ du=\tfrac{dx}{2}"},
            {"text": r"Integrar y ajustar factor", "math": r"\int \sin u \cdot 2 du = -2\cos u + C"},
            {"text": r"Volver a x", "math": r"-2\cos(\tfrac{x}{2}) + C"},
        ],
        "choices_latex": [
            r"-2\cos(\tfrac{x}{2}) + C",
            r"2\cos(\tfrac{x}{2}) + C",
            r"\sin(\tfrac{x}{2}) + C",
            r"-\cos x + C",
        ],
        "correct_index": 0,
        "wrong_options": [
            {"wrong_steps": [{"text": r"Olvidó factor 2", "math": r"no\ multiplicó\ por\ 2\ al\ sustituir"}], "error_highlight": "Factor olvidado", "error_id": "integracion-partes-innecesaria"},
            {"wrong_steps": [{"text": r"Sustitución errónea", "math": r"u=x (incorrecto)"}], "error_highlight": "Sustitución incorrecta", "error_id": "integrales-trig-sustitucion-signo"},
            {"wrong_steps": [{"text": r"Resultado inventado", "math": r"\text{sin verificación}"}], "error_highlight": "Antiderivada inventada", "error_id": "integracion-partes-antiderivada-inventada"},
        ],
        "source": "seed",
        "seed_id": "w1-24",
        "origin_label": "Se",
    },
    {
        "question_latex": r"\int x\sin(2x) \, dx",
        "correct_answer": r"-\tfrac{x\cos2x}{2} + \tfrac{\sin2x}{4} + C",
        "solution_steps": [
            {"text": r"Integración por partes: u=x, dv=\sin2x dx", "math": r"u=x,\ dv=\sin2x dx"},
            {"text": r"v=-\tfrac{1}{2}\cos2x, du=dx", "math": r"v=-\tfrac{1}{2}\cos2x,\ du=dx"},
            {"text": r"Aplicar y simplificar", "math": r"-\tfrac{x\cos2x}{2} + \tfrac{1}{2}\int \cos2x dx = -\tfrac{x\cos2x}{2} + \tfrac{\sin2x}{4} + C"},
        ],
        "choices_latex": [
            r"-\tfrac{x\cos2x}{2} + \tfrac{\sin2x}{4} + C",
            r"\tfrac{x\sin2x}{2} + C",
            r"\sin2x + C",
            r"x\cos2x + C",
        ],
        "correct_index": 0,
        "wrong_options": [
            {"wrong_steps": [{"text": r"Se olvidó 1/2 en v", "math": r"v=\cos2x (olvido\ \tfrac{1}{2})"}], "error_highlight": "Constante en v incorrecta", "error_id": "integracion-partes-derivada-u"},
            {"wrong_steps": [{"text": r"No restó integral resultante", "math": r"no\ completar\ el\ paso\ final"}], "error_highlight": "Paso incompleto", "error_id": "integracion-partes-innecesaria"},
            {"wrong_steps": [{"text": r"Resultado inventado", "math": r"\text{sin verificación}"}], "error_highlight": "Antiderivada inventada", "error_id": "integracion-partes-antiderivada-inventada"},
        ],
        "source": "seed",
        "seed_id": "w1-25",
        "origin_label": "Se",
    },
    {
        "question_latex": r"\int x^3 e^{x} \, dx",
        "correct_answer": r"e^{x}(x^3-3x^2+6x-6)+C",
        "solution_steps": [
            {"text": r"Integrar por partes repetidas veces", "math": r"\int x^3 e^{x}dx = x^3 e^{x} - 3\int x^2 e^{x}dx"},
            {"text": r"Continuar con x^2 e^x (ya conocido)", "math": r"=e^{x}(x^3-3x^2+6x-6)+C"},
        ],
        "choices_latex": [
            r"e^{x}(x^3-3x^2+6x-6)+C",
            r"x^3 e^{x} + C",
            r"e^{x}(x^3-3x^2)+C",
            r"\tfrac{e^{x}}{2}(x^3-3x^2+6x)+C",
        ],
        "correct_index": 0,
        "wrong_options": [
            {"wrong_steps": [{"text": r"Omitió repeticiones de partes", "math": r"no\ completar\ todos\ los\ pasos\ iterativos"}], "error_highlight": "Paso repetitivo omitido", "error_id": "integracion-partes-innecesaria"},
            {"wrong_steps": [{"text": r"Error algebraico", "math": r"combinación\ de\ términos\ incorrecta"}], "error_highlight": "Error algebraico", "error_id": "integracion-partes-derivada-u"},
            {"wrong_steps": [{"text": r"Antiderivada inventada", "math": r"\text{sin verificación}"}], "error_highlight": "Antiderivada inventada", "error_id": "integracion-partes-antiderivada-inventada"},
        ],
        "source": "seed",
        "seed_id": "w1-26",
        "origin_label": "Se",
    },
    {
        "question_latex": r"\int \sin^{2}x \cos x \, dx",
        "correct_answer": r"\tfrac{\sin^{3}x}{3} + C",
        "solution_steps": [
            {"text": r"Sustitución u=\sin x, du=\cos x dx", "math": r"u=\sin x,\ du=\cos x dx"},
            {"text": r"Integrar u^2 du", "math": r"\int u^2 du = \tfrac{u^3}{3} + C"},
            {"text": r"Volver a x", "math": r"\tfrac{\sin^3 x}{3} + C"},
        ],
        "choices_latex": [
            r"\tfrac{\sin^{3}x}{3} + C",
            r"\sin^2 x + C",
            r"\tfrac{\cos^3 x}{3} + C",
            r"\sin x + C",
        ],
        "correct_index": 0,
        "wrong_options": [
            {"wrong_steps": [{"text": r"No sustituyó correctamente", "math": r"no\ usar\ u=\sin x"}], "error_highlight": "Sustitución fallida", "error_id": "integrales-trig-sustitucion-signo"},
            {"wrong_steps": [{"text": r"Integró mal u^2", "math": r"\int u^2 du = u + C (incorrecto)"}], "error_highlight": "Integración incorrecta", "error_id": "integrales-trig-paridad"},
            {"wrong_steps": [{"text": r"Resultado inventado", "math": r"\text{sin verificación}"}], "error_highlight": "Antiderivada inventada", "error_id": "integracion-partes-antiderivada-inventada"},
        ],
        "source": "seed",
        "seed_id": "w1-27",
        "origin_label": "Se",
    },
    {
        "question_latex": r"\int \cos x \sin^{3}x \, dx",
        "correct_answer": r"\tfrac{\sin^{4}x}{4} + C",
        "solution_steps": [
            {"text": r"Sustitución u=\sin x, du=\cos x dx", "math": r"u=\sin x,\ du=\cos x dx"},
            {"text": r"Integrar u^3 du", "math": r"\int u^3 du = \tfrac{u^4}{4} + C"},
            {"text": r"Volver a x", "math": r"\tfrac{\sin^4 x}{4} + C"},
        ],
        "choices_latex": [
            r"\tfrac{\sin^{4}x}{4} + C",
            r"\sin^3 x + C",
            r"\cos x + C",
            r"\tfrac{\sin^{2}x}{2} + C",
        ],
        "correct_index": 0,
        "wrong_options": [
            {"wrong_steps": [{"text": r"No sustituyó u", "math": r"no\ hacer\ u=\sin x"}], "error_highlight": "No sustituyó", "error_id": "integrales-trig-sustitucion-signo"},
            {"wrong_steps": [{"text": r"Integró mal u^3", "math": r"\int u^3 du = u^2 (incorrecto)"}], "error_highlight": "Error en potencia", "error_id": "integrales-trig-paridad"},
            {"wrong_steps": [{"text": r"Resultado inventado", "math": r"\text{sin verificación}"}], "error_highlight": "Antiderivada inventada", "error_id": "integracion-partes-antiderivada-inventada"},
        ],
        "source": "seed",
        "seed_id": "w1-28",
        "origin_label": "Se",
    },
    {
        "question_latex": r"\int \sin x \, dx",
        "correct_answer": r"-\cos x + C",
        "solution_steps": [
            {"text": r"Integrar directo", "math": r"\int \sin x dx = -\cos x + C"},
        ],
        "choices_latex": [
            r"-\cos x + C",
            r"\cos x + C",
            r"\sin x + C",
            r"-\sin x + C",
        ],
        "correct_index": 0,
        "wrong_options": [
            {"wrong_steps": [{"text": r"Confundió signos", "math": r"pensó\ que\ \int\sin x = \cos x"}], "error_highlight": "Signo invertido", "error_id": "integrales-trig-paridad"},
            {"wrong_steps": [{"text": r"Resultado inventado", "math": r"\text{sin verificación}"}], "error_highlight": "Antiderivada inventada", "error_id": "integracion-partes-antiderivada-inventada"},
            {"wrong_steps": [{"text": r"Usó u-sub innecesaria", "math": r"u=\sin x (innecesario)"}], "error_highlight": "Sustitución innecesaria", "error_id": "integrales-trig-sustitucion-signo"},
        ],
        "source": "seed",
        "seed_id": "w1-29",
        "origin_label": "Se",
    },
    {
        "question_latex": r"\int \cos x \, dx",
        "correct_answer": r"\sin x + C",
        "solution_steps": [
            {"text": r"Integrar directo", "math": r"\int \cos x dx = \sin x + C"},
        ],
        "choices_latex": [
            r"\sin x + C",
            r"-\sin x + C",
            r"\cos x + C",
            r"\tan x + C",
        ],
        "correct_index": 0,
        "wrong_options": [
            {"wrong_steps": [{"text": r"Confundió funciones", "math": r"pensó\ que\ \int\cos x = \cos x"}], "error_highlight": "Confusión básica", "error_id": "integrales-trig-paridad"},
            {"wrong_steps": [{"text": r"Resultado inventado", "math": r"\text{sin verificación}"}], "error_highlight": "Antiderivada inventada", "error_id": "integracion-partes-antiderivada-inventada"},
            {"wrong_steps": [{"text": r"Usó u-sub innecesaria", "math": r"u=\cos x (innecesario)"}], "error_highlight": "Sustitución innecesaria", "error_id": "integrales-trig-sustitucion-signo"},
        ],
        "source": "seed",
        "seed_id": "w1-30",
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
