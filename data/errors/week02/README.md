# Errores - Semana 2: Sustitución Trigonométrica y Fracciones Parciales

Esta carpeta contiene los errores comunes identificados para la **Semana 2** del curso Cálculo Integral, centrada en **Sustitución Trigonométrica y Fracciones Parciales**.

## Temas Cubiertos

### Sustitución Trigonométrica
- Elección correcta del caso trigonométrico
- Regreso a la variable original
- Identidades trigonométricas

### Fracciones Parciales
- Descomposición de funciones racionales
- Factores lineales distintos
- Simplificación previa

## Errores Incluidos

| ID | Título | Tema |
|----|--------|------|
| `sustitucion-trigonometrica-caso-incorrecto` | Error en la elección del caso trigonométrico | Sustitución trigonométrica |
| `sustitucion-trigonometrica-no-retorno` | No regresar a la variable original | Sustitución trigonométrica |
| `sustitucion-trigonometrica-eleccion-caso` | Elección del caso trigonométrico adecuado | Sustitución trigonométrica |
| `sustitucion-trig-identidad-mal` | Error en aplicación de identidades trigonométricas | Sustitución trigonométrica |
| `sustitucion-trig-limites-olvidados` | Olvidar cambiar límites en integrales definidas | Sustitución trigonométrica |
| `fracciones-parciales-descomposicion-lineal` | Error en descomposición con factores lineales | Fracciones parciales |
| `fracciones-parciales-sin-simplificar` | Integrar sin simplificar previamente | Fracciones parciales |
| `fracciones-parciales-coeficientes-mal` | Error en cálculo de coeficientes | Fracciones parciales |
| `fracciones-parciales-integracion-error` | Error al integrar términos individuales | Fracciones parciales |
| `fracciones-parciales-denominador-incompleto` | No factorizar completamente el denominador | Fracciones parciales |

## Estructura de Archivos

Cada archivo JSON sigue la estructura estándar de errores CIED:
- `id`: Identificador único del error
- `titulo`: Título descriptivo
- `descripcion_corta`: Resumen del error
- `patron_error`: Ejemplo del error cometido
- `remediacion`: Estrategia de corrección
- `ejercicio_correctivo`: Ejemplo de aplicación correcta

## Estado

- ✅ Errores básicos creados
- ✅ Estructura validada
- ⏳ Quiz correspondiente pendiente (Fase 2)

## Próximos Pasos

1. Crear `app/services/quizzes/quiz_week02.py`
2. Registrar WeekSpec en `app/services/weeks.py`
3. Actualizar `app/services/errors_repo.py` para soporte multi-semana
4. Validar integración completa

## Referencias

Basado en el syllabus: `docs/syllabus/week02.md`
- **7.3 Sustitución trigonométrica**
- **7.4 Fracciones parciales**