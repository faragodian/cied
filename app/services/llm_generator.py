"""
Agente Generador de Ejercicios basado en LLM
Sistema CIED - Week 01
"""

import os
import random

# Importar y configurar Gemini solo cuando sea necesario
def _get_gemini_model():
    """Obtiene el modelo Gemini configurado, o None si no hay API key."""
    try:
        import google.generativeai as genai
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return None
        genai.configure(api_key=api_key)
        return genai.GenerativeModel("models/gemini-pro-latest")
    except ImportError:
        # Si no está instalado google-generativeai, usar fallback
        return None
    except Exception:
        # Cualquier otro error (configuración, etc.)
        return None

def generate_week01_exercise(question_latex: str) -> str:
    """
    Genera un nuevo ejercicio similar para Week 01 (Integración por partes)
    a partir de un problema semilla.
    """

    prompt = f"""
Eres el Agente Generador de Ejercicios del sistema CIED.

Contexto académico:
- Curso: Cálculo Integral (nivel universitario)
- Semana: Week 01
- Técnica: Integración por partes
- Tipo de problema: Integral indefinida o definida
- Formato: Selección múltiple con una única respuesta correcta

Problema semilla:
\"\"\"
{question_latex}
\"\"\"

Instrucciones estrictas:
1. Genera UN nuevo ejercicio matemático distinto pero equivalente en dificultad y técnica.
2. Debe poder resolverse por integración por partes.
3. NO reutilices funciones, constantes ni límites del problema semilla.
4. NO incluyas solución ni opciones.
5. Devuelve solo el enunciado en LaTeX.
6. El ejercicio debe ser adecuado para activar errores comunes de integración por partes.

Salida esperada:
- Un único enunciado matemático en LaTeX.
"""

    # Intentar usar Gemini si está disponible
    model = _get_gemini_model()
    if model:
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception:
            # Si falla la API, usar fallback local
            pass

    # Fallback local: seleccionar ejercicio aleatorio diferente al problema semilla
    fallback_exercises = [
        r"\int x \sin(x) \, dx",
        r"\int x \cos(x) \, dx",
        r"\int x^2 e^{x} \, dx",
        r"\int x \ln(x) \, dx"
    ]

    # Filtrar ejercicios que no sean idénticos al problema semilla
    available_exercises = [ex for ex in fallback_exercises if ex != question_latex]

    # Si todos son iguales o la lista está vacía, devolver uno por defecto
    if not available_exercises:
        return r"\int x \sin(x) \, dx"

    return random.choice(available_exercises)