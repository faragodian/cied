#!/usr/bin/env python3
"""
Script de validación manual para Week 01 de CIED.

Uso:
    python scripts/validate_week01.py

Salida:
    - Exit code 0: Validación exitosa
    - Exit code 1: Errores encontrados
    - Imprime detalles de errores/advertencias
"""

import sys
import os

# Agregar la raíz del proyecto al path
script_dir = os.path.dirname(__file__)
project_root = os.path.dirname(script_dir)
sys.path.insert(0, project_root)

def main():
    """Ejecuta validación de Week 01 y reporta resultados."""
    print("🔍 Validando Week 01 de CIED...")
    print("=" * 50)

    try:
        # Importar y ejecutar validación
        from app.services.quiz_week01 import validate_quiz_templates_week01

        result = validate_quiz_templates_week01()

        print(f"📊 Resultados:")
        print(f"   • Total templates: {result['total_templates']}")
        print(f"   • Errores: {len(result['errors'])}")
        print(f"   • Advertencias: {len(result['warnings'])}")
        print(f"   • Estado: {'✅ VÁLIDO' if result['is_valid'] else '❌ INVÁLIDO'}")

        # Mostrar errores
        if result['errors']:
            print(f"\n❌ ERRORES ENCONTRADOS ({len(result['errors'])}):")
            for i, error in enumerate(result['errors'], 1):
                print(f"   {i}. {error}")

        # Mostrar advertencias
        if result['warnings']:
            print(f"\n⚠️  ADVERTENCIAS ({len(result['warnings'])}):")
            for i, warning in enumerate(result['warnings'], 1):
                print(f"   {i}. {warning}")

        # Resultado final
        if result['is_valid']:
            print("\n✅ VALIDACIÓN COMPLETADA EXITOSAMENTE")
            return True
        else:
            print("\n❌ VALIDACIÓN FALLIDA - REVISAR ERRORES")
            return False

    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("Asegúrate de estar ejecutando desde la raíz del proyecto")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)