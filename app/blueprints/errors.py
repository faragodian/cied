"""
Blueprint para rutas relacionadas con errores (JSON)
"""

import logging
from flask import Blueprint, jsonify, request, abort

from ..services.errors_repo import get_errors_repo

logger = logging.getLogger(__name__)

# Se registra en app/__init__.py con url_prefix="/errors"
errors_bp = Blueprint("errors", __name__)


@errors_bp.get("/")
def list_errors():
    """
    Lista todos los errores disponibles (vista resumida)
    """
    try:
        repo = get_errors_repo()
        errors = repo.load_all_errors()

        error_list = [
            {
                "id": e.get("id"),
                "titulo": e.get("titulo"),
                "curso": e.get("curso"),
                "tema": e.get("tema"),
                "subtema": e.get("subtema"),
            }
            for e in errors
        ]

        return jsonify({"count": len(error_list), "errors": error_list}), 200

    except Exception as e:
        logger.error(f"Error listando errores: {e}")
        return jsonify({"error": "Error interno del servidor", "message": str(e)}), 500


@errors_bp.get("/<error_id>")
def get_error(error_id: str):
    """
    Obtiene un error específico por ID (detalle completo)
    """
    repo = get_errors_repo()
    error = repo.get_error_by_id(error_id)

    if error is None:
        abort(404, description=f"Error con ID '{error_id}' no encontrado")

    return jsonify(error), 200


@errors_bp.get("/search")
def search_errors():
    """
    Busca errores por query string (?q=...)
    Devuelve resultados en vista resumida.
    """
    try:
        query = request.args.get("q", "").strip()
        repo = get_errors_repo()

        results = repo.search_errors(query) if query else repo.load_all_errors()

        search_results = [
            {
                "id": e.get("id"),
                "titulo": e.get("titulo"),
                "curso": e.get("curso"),
                "tema": e.get("tema"),
                "subtema": e.get("subtema"),
                "descripcion_corta": e.get("descripcion_corta"),
            }
            for e in results
        ]

        return jsonify({"query": query, "count": len(search_results), "results": search_results}), 200

    except Exception as e:
        logger.error(f"Error en búsqueda: {e}")
        return jsonify({"error": "Error interno del servidor", "message": str(e)}), 500
