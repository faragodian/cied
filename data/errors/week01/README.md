# Errores - Semana 1: Integración por Partes

Esta carpeta contiene los errores comunes identificados para la **Semana 1** del curso Cálculo Integral, centrada en **Integración por Partes**.

## Temas Cubiertos

- Integración por partes básica
- Elección correcta de u y dv
- Cálculo de derivadas e integrales
- Errores algebraicos comunes

## Errores Incluidos

| ID | Título | Tema |
|----|--------|------|
| `integracion-partes-signo-formula` | Error en el signo de la fórmula | Integración por partes |
| `integracion-partes-derivada-u` | Error en el cálculo de la derivada de u | Integración por partes |
| `integracion-partes-eleccion-uv` | Elección incorrecta de u y dv | Integración por partes |
| `integracion-partes-antiderivada-inventada` | Antiderivada inventada | Integración por partes |
| `integracion-partes-innecesaria` | Integración por partes innecesaria | Integración por partes |

## Estructura de Archivos

Cada archivo JSON sigue la estructura estándar de errores CIED:
- `id`: Identificador único del error
- `titulo`: Título descriptivo
- `descripcion_corta`: Resumen del error
- `patron_error`: Ejemplo del error cometido
- `remediacion`: Estrategia de corrección
- `ejercicio_correctivo`: Ejemplo de aplicación correcta

## Validación

Para validar que todos los errores están correctamente estructurados:

```bash
cd /home/jarteaga/Documents/cied
python3 scripts/validate_week01.py
```

## Conexión con Quiz

Los errores en esta carpeta están conectados con el sistema de quiz en `app/services/quiz_week01.py` y son utilizados por el **Agente Detector de Errores** para proporcionar retroalimentación pedagógica específica.