"""
WSGI entry point for CIED Flask application.

This module creates the Flask application instance for production deployment
with Gunicorn or other WSGI servers.
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import the application factory
from app import create_app

# Create the Flask application instance
app = create_app()

# Optional: Log that WSGI is loading
if __name__ != '__main__':
    print("CIED WSGI application loaded", file=sys.stderr)
