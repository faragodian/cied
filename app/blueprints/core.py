"""
Blueprint principal para rutas core de la aplicación cied
Maneja la landing page y páginas generales
"""

import logging
from flask import Blueprint, render_template, url_for, current_app
from pathlib import Path

logger = logging.getLogger(__name__)

# Crear blueprint
core_bp = Blueprint("core", __name__, template_folder="templates")


@core_bp.get("/")
def index():
    """
    Página principal (landing page) de cied
    """
    return render_template("index.html")


@core_bp.get("/syllabus")
def syllabus():
    """
    Página que muestra el syllabus del curso con enlaces a cada semana
    """
    # Información de las semanas del syllabus
    weeks = [
        {
            "number": 1,
            "title": "Integración por partes e integrales trigonométricas",
            "filename": "week01.md"
        },
        {
            "number": 2,
            "title": "Sustitución trigonométrica y fracciones parciales",
            "filename": "week02.md"
        },
        {
            "number": 3,
            "title": "Fracciones parciales e integrales impropias",
            "filename": "week03.md"
        },
        {
            "number": 4,
            "title": "Parcial 1 y números complejos",
            "filename": "week04.md"
        }
    ]

    return render_template("syllabus.html", weeks=weeks)


@core_bp.get("/health")
def health():
    """
    Endpoint de health check (mantenido para compatibilidad)
    """
    try:
        # Verificar que la aplicación esté funcionando
        docs_path = current_app.config.get('DOCS_DIR')
        docs_exists = docs_path and Path(docs_path).exists()

        return {
            "status": "ok",
            "service": "cied-web",
            "docs_available": docs_exists
        }, 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "error",
            "message": str(e)
        }, 500

