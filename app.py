#!/usr/bin/env python3
"""
Punto de entrada principal para desarrollo de cied
"""

from app import create_app
from config import Config

if __name__ == "__main__":
    app = create_app()
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )

