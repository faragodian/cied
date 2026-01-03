# cded - Cálculo Integral + Ecuaciones Diferenciales

Una aplicación web educativa para catalogar y consultar errores comunes en cálculo integral y ecuaciones diferenciales, construida con Flask.

## 🚀 Características

- **API RESTful** para consultar errores matemáticos
- **Búsqueda inteligente** por título, tags y descripción
- **Estructura modular** siguiendo mejores prácticas de Flask
- **Almacenamiento en JSON** para simplicidad y versionado
- **Application Factory** pattern para escalabilidad

## 📋 Requisitos

- Python 3.8+
- Ubuntu Server (o cualquier sistema con Python)

## 🛠️ Instalación y Configuración

### 1. Clonar y configurar entorno virtual

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Estructura del proyecto

```
cded/
├── app/                    # Código de la aplicación
│   ├── __init__.py        # Application factory
│   ├── blueprints/        # Blueprints de rutas
│   ├── services/          # Servicios de negocio
│   └── config.py          # Configuración
├── data/                  # Datos JSON
│   └── errors/           # Archivos de errores
├── tests/                # Pruebas unitarias
├── scripts/              # Scripts de utilidad
├── instance/             # Configuración local (no versionada)
├── app.py                # Punto de entrada para desarrollo
├── config.py             # Configuración global
└── requirements.txt      # Dependencias
```

### 3. Ejecutar la aplicación

#### Opción A: Script de desarrollo
```bash
./scripts/run_dev.sh
```

#### Opción B: Manualmente
```bash
export FLASK_ENV=development
export FLASK_APP=app.py
python app.py
```

#### Opción C: Con Flask CLI
```bash
export FLASK_ENV=development
flask run
```

La aplicación estará disponible en `http://127.0.0.1:5000`

## 📚 API Endpoints

### Endpoints principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Estado básico de la aplicación |
| `GET` | `/health` | Health check con estadísticas |
| `GET` | `/errors` | Lista todos los errores |
| `GET` | `/errors/<id>` | Obtiene error específico por ID |
| `GET` | `/errors/search?q=<query>` | Busca errores por término |

### Ejemplos de uso

```bash
# Health check
curl http://127.0.0.1:5000/health

# Listar todos los errores
curl http://127.0.0.1:5000/errors

# Obtener error específico
curl http://127.0.0.1:5000/errors/edo-factor-integrante-signo

# Buscar errores
curl "http://127.0.0.1:5000/errors/search?q=factor"
```

## 📄 Formato de Datos de Error

Los errores se almacenan como archivos JSON en `data/errors/`. Cada archivo representa un error único con la siguiente estructura:

```json
{
  "id": "edo-factor-integrante-signo",
  "curso": "Ecuaciones Diferenciales",
  "tema": "Ecuaciones de Primer Orden",
  "subtema": "Ecuaciones Lineales",
  "titulo": "Error en el factor integrante: olvidar considerar el signo",
  "descripcion_corta": "Al resolver ecuaciones diferenciales lineales...",
  "prerrequisitos": ["Ecuaciones diferenciales lineales", "Método del factor integrante"],
  "sintomas": ["La ecuación no se resuelve correctamente", "El factor integrante parece incorrecto"],
  "patron_error": {
    "latex": "\\frac{dy}{dx} + P(x)y = Q(x) \\implies \\mu(x) = e^{\\int P(x)\\,dx}",
    "explicacion": "El error ocurre cuando se calcula mal el factor integrante"
  },
  "deteccion": {
    "tipo": "Verificación algebraica",
    "reglas": ["Verificar d/dx[μy] = μQ(x)", "Comprobar solución en ED original"]
  },
  "remediacion": {
    "estrategia": "Revisar cálculo del factor integrante",
    "pistas": ["Identificar P(x) correctamente", "Calcular ∫P(x)dx con cuidado"],
    "mini_leccion": {
      "latex": "\\mu(x) = e^{\\int P(x)\\,dx}",
      "nota": "El signo de P(x) es crucial"
    }
  },
  "ejercicio_correctivo": [
    {
      "enunciado": "Resuelve: dy/dx - 2xy = x",
      "solucion": "Forma estándar: dy/dx + (-2x)y = x",
      "dificultad": "baja"
    }
  ],
  "verificacion": {
    "metodo": "Sustitución directa",
    "sugerido": "Verificar que dy/dx + P(x)y = Q(x)",
    "criterio": "La ED original debe satisfacerse"
  },
  "metadata": {
    "version": "1.0",
    "autor": "Sistema cded",
    "creado": "2024-01-02",
    "actualizado": "2024-01-02",
    "tags": ["ecuaciones diferenciales", "factor integrante", "signo"]
  }
}
```

## 🧪 Pruebas

Ejecutar las pruebas con pytest:

```bash
# Todas las pruebas
pytest

# Con cobertura
pytest --cov=app --cov-report=html

# Pruebas específicas
pytest tests/test_routes.py -v
```

## ➕ Agregar Nuevos Errores

1. **Crear archivo JSON**: Crea un nuevo archivo en `data/errors/` con nombre descriptivo
2. **Formato**: Sigue la estructura JSON documentada arriba
3. **ID único**: Asegúrate de que el campo `id` sea único
4. **Validar**: Ejecuta las pruebas para verificar que se carga correctamente

Ejemplo de comando para crear un nuevo error:

```bash
# Crear archivo base
cp data/errors/edo-factor-integrante-signo.json data/errors/nuevo-error.json

# Editar con tu editor favorito
nano data/errors/nuevo-error.json
```

## 🚀 Despliegue

### Desarrollo local
- Usa `scripts/run_dev.sh` para desarrollo
- La aplicación se recarga automáticamente con cambios

### Producción
- Configura variables de entorno apropiadas
- Usa un servidor WSGI como Gunicorn
- Considera usar Cloudflare Tunnel para exposición externa

### Variables de entorno

```bash
export FLASK_ENV=production
export SECRET_KEY=tu-clave-secreta-produccion
export LOG_LEVEL=INFO
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## 📞 Soporte

Para soporte técnico o preguntas sobre el proyecto:
- Abre un issue en GitHub
- Revisa la documentación de la API
- Ejecuta las pruebas para verificar funcionamiento

---

**¡Feliz aprendizaje matemático!** 🧮✨
