"""
Blueprint para el sistema de quiz del proyecto CIED
"""

import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..services.quiz_week01 import get_random_question
from ..services.errors_repo import get_errors_repo

logger = logging.getLogger(__name__)

# Crear blueprint
quiz_bp = Blueprint("quiz", __name__, template_folder="templates")


@quiz_bp.get("/quiz/week01")
def quiz_week01_get():
    """
    Muestra el quiz de la Semana 1: Integración por partes
    """
    question = get_random_question()
    # Guardar la instancia del quiz en la sesión para mantener el orden aleatorio
    session['current_quiz'] = question
    return render_template("quiz_week01.html", question=question)


@quiz_bp.post("/quiz/week01")
def quiz_week01_post():
    """
    Procesa la respuesta del quiz de la Semana 1
    """
    try:
        # Obtener la respuesta seleccionada (ahora es option_id)
        selected_option_id = request.form.get("answer", "")

        if not selected_option_id:
            flash("Por favor selecciona una opción válida", "error")
            return redirect(url_for("quiz.quiz_week01_get"))

        # Obtener la instancia del quiz de la sesión
        question = session.get('current_quiz')
        if not question:
            flash("Sesión expirada. Por favor recarga la página.", "error")
            return redirect(url_for("quiz.quiz_week01_get"))

        # Buscar la opción seleccionada
        selected_option = None
        for option in question["options"]:
            if option["option_id"] == selected_option_id:
                selected_option = option
                break

        if not selected_option:
            flash("Opción inválida", "error")
            return redirect(url_for("quiz.quiz_week01_get"))

        # Preparar resultado
        result = {
            "is_correct": selected_option["is_correct"],
            "selected_answer": selected_option["latex"],
            # Siempre incluir el procedimiento correcto completo
            "solution_steps": question["solution_steps"],
            "final_answer": question["correct_answer"]
        }

        # Si es incorrecta, agregar información del error específico
        if not selected_option["is_correct"]:
            # Copiar los wrong_steps y agregar verificación con la expresión completa
            wrong_steps = selected_option["wrong_steps"].copy()
            # Agregar paso de verificación usando la expresión completa seleccionada
            verification_step = {
                "text": "Verificación: derivando la respuesta propuesta",
                "math": rf"\frac{{d}}{{dx}}[{selected_option['latex']}] = \text{{?}}"
            }
            wrong_steps.append(verification_step)

            result["wrong_steps"] = wrong_steps
            result["error_highlight"] = selected_option["error_highlight"]
            result["error_id"] = selected_option["error_id"]

        # Si es incorrecta, obtener información adicional del error del banco
        error_info = None
        if not result["is_correct"]:
            try:
                repo = get_errors_repo()
                error_data = repo.get_error_by_id(result["error_id"])
                if error_data:
                    error_info = {
                        "titulo": error_data.get("titulo", "Error desconocido"),
                        "descripcion_corta": error_data.get("descripcion_corta", ""),
                        "id": result["error_id"]
                    }
            except Exception as e:
                logger.error(f"Error obteniendo información del error: {e}")

        return render_template(
            "quiz_week01.html",
            question=question,
            result=result,
            error_info=error_info
        )

    except Exception as e:
        logger.error(f"Error procesando respuesta del quiz: {e}")
        flash("Ocurrió un error procesando tu respuesta", "error")
        return redirect(url_for("quiz.quiz_week01_get"))
