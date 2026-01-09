#!/usr/bin/env python3
"""
Script simple para validar Week 01 de CIED.

Uso:
    python validate_week01.py
"""

import sys
from pathlib import Path

# Agregar raíz del proyecto al path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

from app.services.quiz_week01 import validate_quiz_templates_week01

def main():
    print("🔍 Validando Week 01 de CIED...")
    result = validate_quiz_templates_week01()

    print(f"Total templates: {result['total_templates']}")
    print(f"Errores: {len(result['errors'])}")
    print(f"Advertencias: {len(result['warnings'])}")
    print(f"Válido: {'✅ Sí' if result['is_valid'] else '❌ No'}")

    if result['errors']:
        print("\n❌ ERRORES:")
        for error in result['errors']:
            print(f"  - {error}")

    if result['warnings']:
        print("\n⚠️  ADVERTENCIAS:")
        for warning in result['warnings']:
            print(f"  - {warning}")

    return result['is_valid']

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)