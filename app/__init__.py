"""
cied - Cálculo Integral + Ecuaciones Diferenciales
Application factory para Flask
"""

import logging
from flask import Flask, send_from_directory
from config import Config

logger = logging.getLogger(__name__)


def create_app(config_class=Config):
    """
    Application factory para crear la aplicación Flask
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Cargar configuración adicional desde instance/config.py si existe
    app.config.from_pyfile('config.py', silent=True)

    # Inicializar repositorio de errores
    from .services.errors_repo import init_errors_repo
    errors_dir = app.config['ERRORS_DIR']
    init_errors_repo(errors_dir)

    # Registrar blueprints
    from .blueprints.core import core_bp
    from .blueprints.errors import errors_bp

    app.register_blueprint(core_bp)
    app.register_blueprint(errors_bp, url_prefix="/errors")

    # Configurar ruta estática para docs
    docs_dir = app.config['DOCS_DIR']
    if docs_dir.exists():
        app.add_url_rule('/docs/<path:filename>', 'docs', lambda filename: send_from_directory(docs_dir, filename))


    logger.info("Aplicación cied inicializada correctamente")

    return app
