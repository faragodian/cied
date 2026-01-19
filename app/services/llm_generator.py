"""
CIED - LLM Generator
===================

Generador de ejercicios usando LLMs externos.
Soporta Gemini, DeepSeek y OpenAI con control explícito.

NO existe generación local.
Si ninguna LLM está disponible o falla, se devuelve None
y el sistema sirve un Seed (Se) de forma silenciosa.
"""

import os
import random
import logging

logger = logging.getLogger(__name__)

# ======================================================
# CONFIGURACIÓN EXPLÍCITA (NO MAGIA)
# ======================================================

ENABLE_GEMINI   = True
ENABLE_DEEPSEEK = True
ENABLE_OPENAI   = True

# Orden de prioridad cuando varias están habilitadas
LLM_PRIORITY = ["deepseek", "gemini", "openai"]

# ======================================================
# PROMPT BASE – WEEK 01
# ======================================================

WEEK01_PROMPT = """
Eres un profesor universitario de Cálculo Integral.

Genera UN (1) ejercicio nuevo, similar pero NO idéntico
a ejercicios típicos de Integración por Partes.

Requisitos:
- Nivel: Cálculo universitario
- No incluyas solución
- Usa notación LaTeX válida
- Debe poder resolverse con integración por partes
- Enunciado claro y conciso

Devuelve SOLO el enunciado del ejercicio en LaTeX.
"""

# ======================================================
# LLM IMPLEMENTATIONS
# ======================================================

def _generate_with_gemini(prompt: str):
    try:
        import google.generativeai as genai

        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            logger.warning("GEMINI_API_KEY no definida")
            return None

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("models/gemini-pro-latest")
        response = model.generate_content(prompt)

        if not response or not response.text:
            return None

        return {
            "latex": response.text.strip(),
            "provider": "gemini"
        }

    except Exception as e:
        logger.exception("Gemini falló")
        return None


def _generate_with_deepseek(prompt: str):
    try:
        from openai import OpenAI

        api_key = os.environ.get("DEEPSEEK_API_KEY")
        if not api_key:
            logger.warning("DEEPSEEK_API_KEY no definida")
            return None

        client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )

        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Eres un profesor de matemáticas."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )

        text = resp.choices[0].message.content.strip()
        if not text:
            return None

        return {
            "latex": text,
            "provider": "deepseek"
        }

    except Exception:
        logger.exception("DeepSeek falló")
        return None


def _generate_with_openai(prompt: str):
    try:
        from openai import OpenAI

        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            logger.warning("OPENAI_API_KEY no definida")
            return None

        client = OpenAI(api_key=api_key)

        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un profesor de matemáticas."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )

        text = resp.choices[0].message.content.strip()
        if not text:
            return None

        return {
            "latex": text,
            "provider": "openai"
        }

    except Exception:
        logger.exception("OpenAI falló")
        return None


# ======================================================
# DISPATCHER PRINCIPAL
# ======================================================

def generate_week01_exercise():
    """
    Intenta generar un ejercicio usando LLMs externos.
    Si todos fallan o están deshabilitados → retorna None.
    """

    providers = []

    if ENABLE_DEEPSEEK:
        providers.append("deepseek")
    if ENABLE_GEMINI:
        providers.append("gemini")
    if ENABLE_OPENAI:
        providers.append("openai")

    # Respetar orden de prioridad
    providers = [p for p in LLM_PRIORITY if p in providers]

    for provider in providers:
        if provider == "deepseek":
            result = _generate_with_deepseek(WEEK01_PROMPT)
        elif provider == "gemini":
            result = _generate_with_gemini(WEEK01_PROMPT)
        elif provider == "openai":
            result = _generate_with_openai(WEEK01_PROMPT)
        else:
            result = None

        if result:
            logger.info(f"Ejercicio generado por {provider}")
            return result

    # Ninguna LLM funcionó → Seed
    logger.info("Ninguna LLM disponible, usando Seed")
    return None



