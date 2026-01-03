"""
Configuración de la aplicación cied
"""

import os
from pathlib import Path


class Config:
    """
    Configuración base de la aplicación
    """

    # ─────────────────────────────
    # Seguridad
    # ─────────────────────────────
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

    # ─────────────────────────────
    # Entorno Flask
    # ─────────────────────────────
    FLASK_ENV = os.environ.get("FLASK_ENV", "development")
    DEBUG = FLASK_ENV == "development"

    HOST = os.environ.get("HOST", "0.0.0.0")
    PORT = int(os.environ.get("PORT", "8082"))

    # ─────────────────────────────
    # Rutas del proyecto
    # ─────────────────────────────
    BASE_DIR = Path(__file__).resolve().parent
    PROJECT_ROOT = BASE_DIR
    DATA_DIR = PROJECT_ROOT / "data"
    ERRORS_DIR = DATA_DIR / "errors"
    EXERCISES_DIR = DATA_DIR / "exercises"
    DOCS_DIR = PROJECT_ROOT / "docs"

    # ─────────────────────────────
    # Logging
    # ─────────────────────────────
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

    @staticmethod
    def init_app(app):
        """
        Inicialización adicional de la aplicación
        (reservado para logging, extensiones, etc.)
        """
        pass

