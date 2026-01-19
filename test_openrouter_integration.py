#!/usr/bin/env python3
"""
Prueba rápida de integración de OpenRouter en el proyecto CIED
"""

import os
import sys

# Agregar el directorio raíz al path para importar módulos locales
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.llm_generator import generate_week01_exercise, ENABLE_OPENROUTER, ENABLE_OPENAI, ENABLE_GEMINI, ENABLE_DEEPSEEK
from app.services.quiz_week01 import is_llm_available

def test_env_vars():
    """Verificar que las variables de entorno están configuradas"""
    print("🔍 Verificando variables de entorno:")

    env_vars = {
        'OPENAI_API_KEY': os.environ.get('OPENAI_API_KEY'),
        'GEMINI_API_KEY': os.environ.get('GEMINI_API_KEY'),
        'DEEPSEEK_API_KEY': os.environ.get('DEEPSEEK_API_KEY'),
        'OPENROUTER_API_KEY': os.environ.get('OPENROUTER_API_KEY')
    }

    for var, value in env_vars.items():
        if value:
            print(f"  ✅ {var}: {'*' * 20}... (configurada)")
        else:
            print(f"  ❌ {var}: no configurada")

    return env_vars

def test_config_flags():
    """Verificar configuración de flags"""
    print("\n🔧 Verificando configuración de flags:")

    flags = {
        'ENABLE_OPENAI': ENABLE_OPENAI,
        'ENABLE_GEMINI': ENABLE_GEMINI,
        'ENABLE_DEEPSEEK': ENABLE_DEEPSEEK,
        'ENABLE_OPENROUTER': ENABLE_OPENROUTER
    }

    for flag, enabled in flags.items():
        status = "✅ habilitado" if enabled else "❌ deshabilitado"
        print(f"  {status}: {flag}")

    return flags

def test_llm_availability():
    """Probar función is_llm_available()"""
    print("\n🤖 Probando disponibilidad de LLM:")
    available = is_llm_available()
    status = "✅ disponible" if available else "❌ no disponible"
    print(f"  {status}: is_llm_available() = {available}")

    return available

def test_generation():
    """Probar generación de ejercicio"""
    print("\n📝 Probando generación de ejercicio:")
    try:
        result = generate_week01_exercise()
        if result:
            print("  ✅ Generación exitosa:")
            print(f"    Proveedor: {result['provider']}")
            print(f"    Longitud: {len(result['latex'])} caracteres")
            print(f"    Contenido: {result['latex'][:100]}...")
        else:
            print("  ❌ Generación falló: retornó None")
        return result
    except Exception as e:
        print(f"  ❌ Error en generación: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Test de integración OpenRouter - CIED\n")

    # Ejecutar todas las pruebas
    env_vars = test_env_vars()
    flags = test_config_flags()
    available = test_llm_availability()
    result = test_generation()

    print("\n" + "="*50)
    print("📊 RESULTADO FINAL:")

    if result:
        print("✅ ¡ÉXITO! Las APIs funcionan correctamente en CIED")
        print(f"   Último ejercicio generado por: {result['provider']}")
    else:
        print("❌ Problema detectado")

        # Diagnóstico
        if not available:
            print("   Causa: is_llm_available() retorna False")
            enabled_count = sum(flags.values())
            env_count = sum(1 for v in env_vars.values() if v)
            print(f"   Flags habilitados: {enabled_count}/4")
            print(f"   Variables de entorno: {env_count}/4")

        if not env_vars['OPENROUTER_API_KEY'] and flags['ENABLE_OPENROUTER']:
            print("   Solución: configurar OPENROUTER_API_KEY")
        elif not any(env_vars.values()):
            print("   Solución: configurar al menos una API key")