#!/usr/bin/env python3
"""
Script para probar si una API key de Gemini está activa y funciona.
Uso: python3 test_gemini_api.py
"""

import google.generativeai as genai
import sys

def test_gemini_api():
    """Prueba la funcionalidad de una API key de Gemini."""

    # Solicita la API key al usuario
    api_key = input('Ingresa tu API key de Gemini: ').strip()

    if not api_key:
        print('❌ No se proporcionó una API key.')
        return False

    try:
        print('🔄 Probando API key...')

        # Configura la API
        genai.configure(api_key=api_key)

        # Intenta listar modelos disponibles
        models = genai.list_models()

        # Filtra solo modelos Gemini
        gemini_models = [m for m in models if 'gemini' in m.name.lower()]

        if gemini_models:
            print('✅ API key válida y activa!')
            print(f'📋 Modelos Gemini disponibles ({len(gemini_models)}):')
            for m in gemini_models:
                print(f'   - {m.name}')
            return True
        else:
            print('⚠️ API key válida pero no hay modelos Gemini disponibles.')
            return False

    except Exception as e:
        error_msg = str(e).lower()
        if 'invalid' in error_msg or 'api_key' in error_msg:
            print('❌ API key inválida o expirada.')
        elif 'quota' in error_msg:
            print('❌ API key válida pero has excedido el límite de uso (quota).')
        elif 'permission' in error_msg:
            print('❌ API key válida pero sin permisos suficientes.')
        else:
            print(f'❌ Error al probar API key: {e}')
        return False

if __name__ == '__main__':
    success = test_gemini_api()
    sys.exit(0 if success else 1)