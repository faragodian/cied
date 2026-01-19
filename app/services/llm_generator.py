"""
CIED - LLM Generator
===================

Generador de ejercicios usando LLMs externos.
Soporta Gemini, DeepSeek, OpenRouter y OpenAI con control explícito.

NO existe generación local.
Si ninguna LLM está disponible o falla, se devuelve None
y el sistema sirve un Seed (Se) de forma silenciosa.
"""

import os
import json
import re
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# ======================================================
# CONFIGURACIÓN EXPLÍCITA (NO MAGIA)
# ======================================================

ENABLE_GEMINI   = True
ENABLE_DEEPSEEK = False
ENABLE_OPENROUTER = True
ENABLE_OPENAI   = True

# Orden de prioridad cuando varias están habilitadas
LLM_PRIORITY = ["openai", "gemini", "openrouter"]  

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
# PROMPT ESTRUCTURADO – WEEK 01 (QUIZ JSON)
# ======================================================

# Lista acotada de error_ids existentes en data/errors (Week01 / integración por partes)
WEEK01_ALLOWED_ERROR_IDS = [
    "integracion-partes-eleccion-uv",
    "integracion-partes-signo-formula",
    "integracion-partes-derivada-u",
    "integracion-partes-antiderivada-inventada",
    "integracion-partes-innecesaria",
]

WEEK01_QUIZ_JSON_PROMPT = f"""
Eres un profesor universitario de Cálculo Integral.

Genera UN (1) ítem de quiz de Integración por Partes.
Debe ser coherente: enunciado ↔ respuesta correcta ↔ distractores ↔ pasos ↔ error_id.

Restricciones:
- Nivel: Cálculo universitario
- No uses integrales imposibles; debe poder resolverse con integración por partes
- Usa LaTeX válido (sin delimitadores $$ ni \\[ \\]; solo el contenido)
- Incluye constante +C si es integral indefinida
- Si es definida, entrega un valor numérico/expresión final sin +C

Debes devolver SOLO un JSON válido (sin markdown), con esta estructura:
{{
  "question_latex": "....",          // La integral, por ejemplo: "\\\\int x e^{{2x}}\\\\,dx"
  "correct_answer": "....",          // respuesta final en LaTeX
  "solution_steps": [                // lista de pasos correctos
    {{"text":"...", "math":"..."}},
    ...
  ],
  "options": [                       // EXACTAMENTE 4 opciones
    {{
      "option_id": "A",
      "latex": "....",
      "is_correct": true
    }},
    {{
      "option_id": "B",
      "latex": "....",
      "is_correct": false,
      "wrong_steps": [{{"text":"...","math":"..."}}, ...],
      "error_highlight": "...",
      "error_id": "..."
    }},
    ...
  ],
  "seed_id": null,
  "origin_label": "LLM"
}}

Reglas para options:
- Exactamente una opción con "is_correct": true y su latex debe ser EXACTAMENTE igual a correct_answer.
- Las 3 opciones incorrectas deben ser plausibles y distintas entre sí.
- Para cada opción incorrecta:
  - "error_id" DEBE ser uno de: {WEEK01_ALLOWED_ERROR_IDS}
  - Los 3 error_id deben ser DISTINTOS entre sí (no repetir error_id).
  - "wrong_steps" debe explicar el error cometido (3 a 7 pasos).
  - "error_highlight" debe resumir el error en una frase corta.

Devuelve SOLO el JSON.
""".strip()

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

        messages = [
            {"role": "system", "content": "Eres un profesor de matemáticas."},
            {"role": "user", "content": prompt},
        ]

        # Intentar forzar JSON si el prompt lo pide explícitamente.
        # Si el modelo no soporta response_format, caemos al request normal.
        try:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7,
                response_format={"type": "json_object"},
            )
        except Exception:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
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


def _generate_with_openrouter(prompt: str):
    try:
        from openai import OpenAI

        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            logger.warning("OPENROUTER_API_KEY no definida")
            return None

        client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )

        messages = [
            {"role": "system", "content": "Eres un profesor de matemáticas."},
            {"role": "user", "content": prompt},
        ]

        # Igual que OpenAI: intentar forzar JSON si se solicita.
        try:
            resp = client.chat.completions.create(
                model="deepseek/deepseek-chat",  # Usar DeepSeek a través de OpenRouter
                messages=messages,
                temperature=0.7,
                response_format={"type": "json_object"},
            )
        except Exception:
            resp = client.chat.completions.create(
                model="deepseek/deepseek-chat",
                messages=messages,
                temperature=0.7,
            )

        text = resp.choices[0].message.content.strip()
        if not text:
            return None

        return {
            "latex": text,
            "provider": "openrouter"
        }

    except Exception:
        logger.exception("OpenRouter falló")
        return None


def _extract_first_json_object(text: str) -> Optional[Dict[str, Any]]:
    """
    Extrae el primer objeto JSON válido encontrado en un string.
    Útil porque algunos modelos envuelven el JSON con texto extra.
    """
    if not text:
        return None
    # Intentar parse directo primero
    try:
        obj = json.loads(text)
        if isinstance(obj, dict):
            return obj
    except Exception:
        pass

    # Buscar el primer bloque {...} de forma aproximada
    m = re.search(r"\{[\s\S]*\}", text)
    if not m:
        return None
    candidate = m.group(0)
    try:
        obj = json.loads(candidate)
        return obj if isinstance(obj, dict) else None
    except Exception:
        return None


def is_any_llm_configured() -> bool:
    """
    Verifica configuración local (flags + API keys) sin hacer llamadas a red.
    """
    if ENABLE_OPENAI and os.environ.get("OPENAI_API_KEY"):
        return True
    if ENABLE_GEMINI and os.environ.get("GEMINI_API_KEY"):
        return True
    if ENABLE_OPENROUTER and os.environ.get("OPENROUTER_API_KEY"):
        return True
    if ENABLE_DEEPSEEK and os.environ.get("DEEPSEEK_API_KEY"):
        return True
    return False


def generate_week01_quiz_instance() -> Optional[Dict[str, Any]]:
    """
    Genera un ítem de quiz completo (enunciado + respuesta + opciones + errores) usando LLMs.
    Si falla, retorna None para que el sistema caiga a Seeds.
    """
    providers = []
    if ENABLE_DEEPSEEK:
        providers.append("deepseek")
    if ENABLE_GEMINI:
        providers.append("gemini")
    if ENABLE_OPENROUTER:
        providers.append("openrouter")
    if ENABLE_OPENAI:
        providers.append("openai")
    providers = [p for p in LLM_PRIORITY if p in providers]

    for provider in providers:
        if provider == "deepseek":
            raw = _generate_with_deepseek(WEEK01_QUIZ_JSON_PROMPT)
        elif provider == "gemini":
            raw = _generate_with_gemini(WEEK01_QUIZ_JSON_PROMPT)
        elif provider == "openrouter":
            raw = _generate_with_openrouter(WEEK01_QUIZ_JSON_PROMPT)
        elif provider == "openai":
            raw = _generate_with_openai(WEEK01_QUIZ_JSON_PROMPT)
        else:
            raw = None

        if not raw or "latex" not in raw:
            continue

        obj = _extract_first_json_object(raw["latex"])
        if not obj:
            logger.warning("LLM devolvió salida no-JSON (provider=%s)", provider)
            continue

        # Validación mínima (coherencia básica)
        try:
            if not isinstance(obj.get("question_latex"), str) or not obj["question_latex"].strip():
                continue
            if not isinstance(obj.get("correct_answer"), str) or not obj["correct_answer"].strip():
                continue
            options = obj.get("options")
            if not isinstance(options, list) or len(options) != 4:
                continue
            correct = [o for o in options if o.get("is_correct") is True]
            if len(correct) != 1:
                continue
            if str(correct[0].get("latex", "")).strip() != obj["correct_answer"].strip():
                continue
            for o in options:
                if o.get("is_correct") is False:
                    if o.get("error_id") not in WEEK01_ALLOWED_ERROR_IDS:
                        raise ValueError("error_id fuera de whitelist")
                    if not isinstance(o.get("wrong_steps"), list) or len(o["wrong_steps"]) < 2:
                        raise ValueError("wrong_steps inválido")
                    if not isinstance(o.get("error_highlight"), str) or not o["error_highlight"].strip():
                        raise ValueError("error_highlight inválido")
            # Enforce: no repetir error_id entre incorrectas
            wrong_ids = [o.get("error_id") for o in options if o.get("is_correct") is False]
            if len(wrong_ids) != len(set(wrong_ids)):
                raise ValueError("error_id repetido en opciones incorrectas")
        except Exception:
            logger.exception("Quiz JSON inválido (provider=%s)", provider)
            continue

        obj["origin_label"] = "LLM"
        obj["seed_id"] = None
        logger.info("Quiz dinámico generado por %s", provider)
        return obj

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
    if ENABLE_OPENROUTER:
        providers.append("openrouter")
    if ENABLE_OPENAI:
        providers.append("openai")

    # Respetar orden de prioridad
    providers = [p for p in LLM_PRIORITY if p in providers]

    for provider in providers:
        if provider == "deepseek":
            result = _generate_with_deepseek(WEEK01_PROMPT)
        elif provider == "gemini":
            result = _generate_with_gemini(WEEK01_PROMPT)
        elif provider == "openrouter":
            result = _generate_with_openrouter(WEEK01_PROMPT)
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



