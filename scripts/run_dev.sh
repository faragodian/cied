#!/usr/bin/env bash
set -e

echo "Iniciando aplicación cied en modo desarrollo..."

# Ir a la raíz del proyecto
cd "$(dirname "$0")/.."

# Activar entorno virtual
source venv/bin/activate

# Variables de entorno mínimas (sin Flask CLI)
export FLASK_ENV=development
export HOST=0.0.0.0
export PORT=8082

# Ejecutar aplicación
python app.py
