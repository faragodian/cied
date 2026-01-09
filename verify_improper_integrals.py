#!/usr/bin/env python3
"""
Script de verificación para los nuevos ejercicios de integrales impropias en Week 01.

Uso:
    python verify_improper_integrals.py

Verifica:
- Que los nuevos ejercicios aparezcan al generar preguntas aleatorias
- Que las opciones sean correctas
- Que los error_id existan
- Validación general de templates
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path para importar módulos
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

from app.services.quiz_week01 import get_random_question, validate_quiz_templates_week01, QUIZ_TEMPLATES


def verify_improper_integrals():
    """Verifica los nuevos ejercicios de integrales impropias."""

    print("🔍 Verificando integrales impropias en Week 01 de CIED")
    print("=" * 60)

    # 1. Validación general de templates
    print("\n1. Ejecutando validación general de templates...")
    validation_result = validate_quiz_templates_week01()

    print(f"   Total templates: {validation_result['total_templates']}")
    print(f"   Errores: {len(validation_result['errors'])}")
    print(f"   Advertencias: {len(validation_result['warnings'])}")
    print(f"   ¿Válido?: {'✅ Sí' if validation_result['is_valid'] else '❌ No'}")

    if validation_result['errors']:
        print("   ❌ Errores encontrados:")
        for error in validation_result['errors']:
            print(f"      - {error}")

    if validation_result['warnings']:
        print("   ⚠️  Advertencias:")
        for warning in validation_result['warnings']:
            print(f"      - {warning}")

    # 2. Verificar que aparezcan los nuevos ejercicios
    print("\n2. Verificando aparición de nuevos ejercicios...")

    improper_questions_found = []
    trials = 50  # Generar varias preguntas para verificar aleatoriedad

    for _ in range(trials):
        question = get_random_question()
        question_latex = question['question_latex']

        if 'x^{-1/2}' in question_latex or '1/(x-1)' in question_latex:
            if question_latex not in improper_questions_found:
                improper_questions_found.append(question_latex)

    print(f"   Preguntas impropias encontradas en {trials} intentos:")
    expected_questions = [
        r"\int_{0}^{1} x^{-1/2} \, dx",
        r"\int_{1}^{2} \frac{1}{x - 1} \, dx"
    ]

    for expected in expected_questions:
        if expected in improper_questions_found:
            print(f"   ✅ {expected}")
        else:
            print(f"   ❌ {expected} (no apareció)")

    # 3. Verificar estructura de los nuevos ejercicios
    print("\n3. Verificando estructura de ejercicios impropios...")

    for i, template in enumerate(QUIZ_TEMPLATES):
        question = template['question_latex']
        if 'x^{-1/2}' in question or '1/(x-1)' in question:
            print(f"\n   Template {i}: {question}")

            # Verificar respuesta correcta
            correct_answer = template['correct_answer']
            choices = template['choices_latex']
            correct_index = template['correct_index']

            if correct_answer in choices:
                print(f"   ✅ Respuesta correcta '{correct_answer}' está en choices")
            else:
                print(f"   ❌ Respuesta correcta '{correct_answer}' NO está en choices")

            if 0 <= correct_index < len(choices) and choices[correct_index] == correct_answer:
                print("   ✅ correct_index apunta correctamente"            else:
                print("   ❌ correct_index incorrecto"            # Verificar wrong_options
            wrong_options = template.get('wrong_options', [])
            print(f"   📋 Tiene {len(wrong_options)} wrong_options")

            for j, wrong_option in enumerate(wrong_options):
                error_id = wrong_option.get('error_id', '')
                if error_id:
                    error_file = root_dir / "data" / "errors" / f"{error_id}.json"
                    if error_file.exists():
                        print(f"   ✅ wrong_option {j}: error_id '{error_id}' tiene JSON")
                    else:
                        print(f"   ❌ wrong_option {j}: error_id '{error_id}' NO tiene JSON")
                else:
                    print(f"   ❌ wrong_option {j}: sin error_id")

    # 4. Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN FINAL")

    total_improper = sum(1 for t in QUIZ_TEMPLATES if 'x^{-1/2}' in t['question_latex'] or '1/(x-1)' in t['question_latex'])
    print(f"   • Total ejercicios impropios agregados: {total_improper}/2")

    all_errors = validation_result['errors']
    improper_errors = [e for e in all_errors if any(str(i) in e for i in range(len(QUIZ_TEMPLATES))
                                                     if 'x^{-1/2}' in QUIZ_TEMPLATES[i]['question_latex'] or
                                                        '1/(x-1)' in QUIZ_TEMPLATES[i]['question_latex'])]
    print(f"   • Errores en ejercicios impropios: {len(improper_errors)}")

    if len(improper_errors) == 0 and total_improper == 2:
        print("   ✅ ¡Integración de ejercicios impropios COMPLETA!")
    else:
        print("   ⚠️  Revisar errores en integración de ejercicios impropios")

    return validation_result['is_valid'] and total_improper == 2


if __name__ == "__main__":
    success = verify_improper_integrals()
    sys.exit(0 if success else 1)