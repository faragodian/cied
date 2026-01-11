# Validación de Week 01 - CIED

Este documento explica el sistema de validación automática implementado para "congelar" Week 01 y asegurar su integridad.

## 🎯 Propósito

- **Congelar Week 01**: Asegurar que los templates pedagógicos de Week 01 mantengan integridad matemática y estructural
- **Validación automática**: Ejecutar validación solo en desarrollo para detectar errores temprano
- **No romper producción**: Gunicorn/systemd continúa funcionando aunque haya errores en templates

## 🔧 Componentes Implementados

### 1. Validación Explícita (Variable de Entorno)

**Ubicación**: `app/__init__.py` en `create_app()`

**Comportamiento**:
- ✅ Se ejecuta solo cuando `CIED_VALIDATE_WEEK01=1` está definido
- ✅ Aborta el arranque si encuentra errores críticos
- ✅ Registra warnings pero permite continuar
- ✅ En producción (sin variable) NO se ejecuta automáticamente

**Detección de ambiente**:
```python
if os.environ.get('CIED_VALIDATE_WEEK01') == '1':
    # Ejecutar validación
```

### 2. Comando Manual

**Ubicación**: `scripts/validate_week01.py`

**Uso**:
```bash
cd /ruta/a/cied
python scripts/validate_week01.py
```

**Salida**:
- Exit code 0: ✅ Validación exitosa
- Exit code 1: ❌ Errores encontrados
- Imprime detalles de errores y advertencias

### 3. Función de Validación

**Ubicación**: `app/services/quiz_week01.py`

**Qué valida**:
- ✅ `correct_answer ∈ choices_latex`
- ✅ `correct_index` apunta al elemento correcto
- ✅ Último paso menciona resultado correcto
- ✅ **NUEVO**: Integrales impropias mencionan "límite"
- ✅ **NUEVO**: Error IDs tienen archivos JSON correspondientes

## 📋 Instrucciones de Uso

### Verificar que funciona con validación explícita

1. **Activar validación**:
   ```bash
   export CIED_VALIDATE_WEEK01=1
   ```

2. **Ejecutar aplicación**:
   ```bash
   python app.py
   ```

3. **Ver logs**: Deberías ver:
   ```
   INFO - CIED_VALIDATE_WEEK01=1 detectado - ejecutando validación de Week 01...
   INFO - ✅ Validación de Week 01 completada exitosamente
   ```

4. **Si hay errores**: El arranque se abortará con mensaje claro

### Verificar que NO funciona en producción (comportamiento por defecto)

1. **Sin variables especiales**:
   ```bash
   # No definir CIED_VALIDATE_WEEK01 o definirlo como cualquier cosa que no sea "1"
   unset CIED_VALIDATE_WEEK01
   # o
   export CIED_VALIDATE_WEEK01=0
   ```

2. **Ejecutar con Gunicorn**:
   ```bash
   gunicorn --bind 0.0.0.0:8082 wsgi:app
   ```

3. **Ver logs**: NO deberías ver mensajes de validación, la app arranca normalmente

### Ejecutar validación manual

```bash
# Desde la raíz del proyecto
python scripts/validate_week01.py

# Ejemplo de salida exitosa:
🔍 Validando Week 01 de CIED...
==================================================
📊 Resultados:
   • Total templates: 25
   • Errores: 0
   • Advertencias: 0
   • Estado: ✅ VÁLIDO

✅ VALIDACIÓN COMPLETADA EXITOSAMENTE

# Ejemplo de salida con errores:
🔍 Validando Week 01 de CIED...
==================================================
📊 Resultados:
   • Total templates: 25
   • Errores: 2
   • Advertencias: 1
   • Estado: ❌ INVÁLIDO

❌ ERRORES ENCONTRADOS (2):
   1. Template 15: correct_answer '2' no está en choices_latex
   2. Template 20: error_id 'error-inexistente' no tiene archivo JSON correspondiente

⚠️  ADVERTENCIAS (1):
   1. Template 5: último paso no menciona resultado 'π'

❌ VALIDACIÓN FALLIDA - REVISAR ERRORES
```

## 🔒 Seguridad y Robustez

- **No rompe producción**: Validación solo cuando `CIED_VALIDATE_WEEK01=1` está definido
- **Manejo de errores**: Excepciones claras con logging solo cuando se solicita validación
- **Exit codes**: Para integración con CI/CD
- **Sin dependencias nuevas**: Usa solo módulos estándar

## 🧪 Pruebas

Para verificar que el sistema funciona:

1. **En desarrollo con templates válidos**: ✅ Debe pasar
2. **En desarrollo con templates inválidos**: ❌ Debe abortar arranque
3. **En producción**: ✅ No debe ejecutar validación
4. **Comando manual**: ✅ Debe reportar estado correcto

## 📝 Notas de Implementación

- La validación automática se integra en `create_app()` para ejecutarse una sola vez al inicio
- Los errores críticos abortan el arranque en desarrollo para forzar corrección
- Las advertencias se loguean pero permiten continuar (para flexibilidad pedagógica)
- El comando manual permite validación bajo demanda sin afectar la app en ejecución