"""Blueprint dinámico para todas las semanas de quiz (01-16).

Genera rutas /quiz/weekNN para cada semana disponible en app/services/quizzes.
Evita importar el paquete quizzes completo para no provocar ciclos: carga
cada módulo weekNN directamente desde su archivo si existe.
"""

import logging
from pathlib import Path
import importlib
import importlib.util
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..services.errors_repo import get_errors_repo

logger = logging.getLogger(__name__)

quiz_bp = Blueprint("quiz", __name__, template_folder="templates")


def _load_week_module(week_num: int):
    """Carga el módulo quiz_weekNN desde el archivo sin usar el paquete.

    Devuelve el módulo o None si no existe.
    """
    base = Path(__file__).resolve().parent.parent
    module_path = base / "services" / "quizzes" / f"quiz_week{week_num:02d}.py"
    if not module_path.exists():
        return None
    name = f"app.services.quizzes.quiz_week{week_num:02d}"
    spec = importlib.util.spec_from_file_location(name, str(module_path))
    mod = importlib.util.module_from_spec(spec)
    # Pre-import common peer modules so relative imports inside the week module resolve
    try:
        importlib.import_module("app.services.llm_generator")
        importlib.import_module("app.services.weeks")
        importlib.import_module("app.services.week_configs")
    except Exception:
        # ignore import errors here; week module may not need all of them
        pass
    spec.loader.exec_module(mod)
    return mod


def create_quiz_route(week_num: int):
    """Crea rutas GET/POST para /quiz/weekNN usando closures."""

    route_get = f"/quiz/week{week_num:02d}"
    session_key = f"current_quiz_week{week_num:02d}"

    @quiz_bp.get(route_get)
    def quiz_get():
        mod = _load_week_module(week_num)
        if mod is None or not hasattr(mod, "get_random_question"):
            flash("Quiz no disponible para esta semana", "error")
            return redirect(url_for("core.index"))

        question = mod.get_random_question()
        session[session_key] = question

        # metadata de la semana
        try:
            from ..services.week_configs import get_week_config
            cfg = get_week_config(f"week{week_num:02d}")
            week_title = cfg.get("title", f"Semana {week_num}")
            week_subtitle = cfg.get("subtitle", "")
        except Exception:
            week_title = f"Semana {week_num}"
            week_subtitle = ""

        return render_template(
            "quiz.html",
            question=question,
            week_title=week_title,
            week_subtitle=week_subtitle,
            form_action=url_for(f"quiz.quiz_week{week_num:02d}_post"),
            new_question_url=url_for(f"quiz.quiz_week{week_num:02d}_get"),
        )

    @quiz_bp.post(route_get)
    def quiz_post():
        question = session.get(session_key)
        if not question:
            flash("Sesión expirada. Por favor recarga la página.", "error")
            return redirect(url_for(f"quiz.quiz_week{week_num:02d}_get"))

        selected_option_id = request.form.get("answer", "")
        if not selected_option_id:
            flash("Por favor selecciona una opción válida", "error")
            return redirect(url_for(f"quiz.quiz_week{week_num:02d}_get"))

        selected_option = next((o for o in question.get("options", []) if o.get("option_id") == selected_option_id), None)
        if not selected_option:
            flash("Opción inválida", "error")
            return redirect(url_for(f"quiz.quiz_week{week_num:02d}_get"))

        result = {
            "is_correct": selected_option.get("is_correct", False),
            "selected_answer": selected_option.get("latex"),
            "solution_steps": question.get("solution_steps", []),
            "final_answer": question.get("correct_answer", ""),
        }

        if not result["is_correct"]:
            wrong_steps = selected_option.get("wrong_steps", []).copy()
            verification_step = {"text": "Verificación: derivando la respuesta propuesta", "math": rf"\\frac{{d}}{{dx}}[{selected_option.get('latex','')}] = \\text{{?}}"}
            wrong_steps.append(verification_step)
            result["wrong_steps"] = wrong_steps
            result["error_highlight"] = selected_option.get("error_highlight")
            result["error_id"] = selected_option.get("error_id")

            try:
                repo = get_errors_repo()
                error_data = repo.get_error_by_id(result.get("error_id"))
                if error_data:
                    error_info = {
                        "titulo": error_data.get("titulo", "Error desconocido"),
                        "descripcion_corta": error_data.get("descripcion_corta", ""),
                        "id": result.get("error_id"),
                    }
                else:
                    error_info = None
            except Exception as e:
                logger.error(f"Error obteniendo info de error: {e}")
                error_info = None
        else:
            error_info = None

        # metadata de la semana
        try:
            from ..services.week_configs import get_week_config
            cfg = get_week_config(f"week{week_num:02d}")
            week_title = cfg.get("title", f"Semana {week_num}")
            week_subtitle = cfg.get("subtitle", "")
        except Exception:
            week_title = f"Semana {week_num}"
            week_subtitle = ""

        return render_template(
            "quiz.html",
            question=question,
            result=result,
            error_info=error_info,
            week_title=week_title,
            week_subtitle=week_subtitle,
            form_action=url_for(f"quiz.quiz_week{week_num:02d}_post"),
            new_question_url=url_for(f"quiz.quiz_week{week_num:02d}_get"),
        )

    # Asignar nombres únicos a las funciones para Flask
    quiz_get.__name__ = f"quiz_week{week_num:02d}_get"
    quiz_post.__name__ = f"quiz_week{week_num:02d}_post"


# Crear rutas para semanas 01-16
for w in range(1, 17):
    create_quiz_route(w)
