"""
cied - Cálculo Integral + Ecuaciones Diferenciales
Application factory para Flask
"""

import logging
import os
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
    from .blueprints.quiz import quiz_bp

    app.register_blueprint(core_bp)
    app.register_blueprint(errors_bp, url_prefix="/errors")
    app.register_blueprint(quiz_bp)

    # Configurar ruta estática para docs
    docs_dir = app.config['DOCS_DIR']
    if docs_dir.exists():
        app.add_url_rule('/docs/<path:filename>', 'docs', lambda filename: send_from_directory(docs_dir, filename))
    # Validación automática de Week 01 (opcional, no bloquea producción por defecto)
    #
    # - Para ejecutar: export CIED_VALIDATE_WEEK01=1
    # - Para abortar el arranque ante errores: export CIED_VALIDATE_WEEK01_STRICT=1
    #
    # Nota: En producción (Gunicorn/systemd) se recomienda NO activar estas variables.
    if os.environ.get("CIED_VALIDATE_WEEK01") == "1":
        try:
            from .services.quiz_week01 import validate_quiz_templates_week01

            validation_result = validate_quiz_templates_week01()
            errors = validation_result.get("errors", []) if isinstance(validation_result, dict) else []
            warnings = validation_result.get("warnings", []) if isinstance(validation_result, dict) else []

            if errors:
                logger.error("❌ Validación de Week 01 detectó %s errores", len(errors))
                for err in errors[:10]:
                    logger.error("  - %s", err)
                if len(errors) > 10:
                    logger.error("  ... y %s errores más", len(errors) - 10)

                # Solo abortar si se solicita explícitamente, o si estamos en debug.
                if os.environ.get("CIED_VALIDATE_WEEK01_STRICT") == "1" or app.debug:
                    raise RuntimeError(f"Errores de validación en Week 01: {len(errors)} errores encontrados")
                else:
                    logger.warning(
                        "Continuando el arranque a pesar de errores (CIED_VALIDATE_WEEK01_STRICT no está activo)."
                    )
            else:
                logger.info("✅ Validación de Week 01 completada exitosamente")

            if warnings:
                logger.warning("⚠️  Validación de Week 01 reportó %s advertencias", len(warnings))
                for w in warnings[:5]:
                    logger.warning("  - %s", w)
                if len(warnings) > 5:
                    logger.warning("  ... y %s advertencias más", len(warnings) - 5)

        except Exception as e:
            logger.exception("Error ejecutando validación automática de Week 01: %s", e)
            if os.environ.get("CIED_VALIDATE_WEEK01_STRICT") == "1" or app.debug:
                raise
    logger.info("Aplicación cied inicializada correctamente")

    return app