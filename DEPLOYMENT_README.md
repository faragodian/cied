# 🚀 Deployment de CIED

Este documento explica cómo desplegar la aplicación CIED usando Gunicorn y systemd.

## 📋 Requisitos Previos

- Python 3.12+
- Gunicorn instalado: `pip install gunicorn`
- Usuario del sistema: `jarteaga`
- Directorio del proyecto: `/home/jarteaga/Documents/cied`

## 🔧 Configuración del Servicio Systemd

### 1. Probar configuración local

```bash
# Ejecutar tests de configuración
cd /home/jarteaga/Documents/cied
python3 scripts/test_service_config.py

# Debería mostrar: ✅ Configuración del servicio lista para deployment
```

### 2. Copiar el archivo de servicio

```bash
# Como root o con sudo
sudo cp /home/jarteaga/Documents/cied/cied.service /etc/systemd/system/
sudo systemctl daemon-reload
```

### 2. Crear directorio de logs y ajustar permisos

```bash
# Como usuario jarteaga
mkdir -p /home/jarteaga/Documents/cied/logs
touch /home/jarteaga/Documents/cied/logs/access.log
touch /home/jarteaga/Documents/cied/logs/error.log

# Ajustar permisos
chmod 755 /home/jarteaga/Documents/cied
chmod 644 /home/jarteaga/Documents/cied/logs/*.log
```

### 3. Verificar configuración del servicio

```bash
# Verificar sintaxis del servicio
sudo systemctl status cied.service

# Ver logs del servicio
sudo journalctl -u cied.service -f
```

## 🎯 Comandos de Control del Servicio

### Iniciar el servicio
```bash
sudo systemctl start cied.service
```

### Detener el servicio
```bash
sudo systemctl stop cied.service
```

### Reiniciar el servicio
```bash
sudo systemctl restart cied.service
```

### Ver estado del servicio
```bash
sudo systemctl status cied.service
```

### Habilitar arranque automático
```bash
sudo systemctl enable cied.service
```

### Ver logs en tiempo real
```bash
sudo journalctl -u cied.service -f
```

## 🧪 Verificación del Deployment

### Ejecutar tests de deployment
```bash
cd /home/jarteaga/Documents/cied
python3 scripts/test_deployment.py
```

Deberías ver:
```
📊 Results: 3/3 tests passed
✅ All tests passed! Ready for deployment.
```

### Probar endpoints manualmente
```bash
# Test básico
curl http://localhost:8082/health

# Test página principal
curl http://localhost:8082/

# Test quiz
curl http://localhost:8082/quiz/week01
```

## 🔍 Troubleshooting

### Verificación rápida antes del deployment
```bash
# Ejecutar tests completos de configuración
cd /home/jarteaga/Documents/cied
python3 scripts/test_service_config.py
```

### Problema: Servicio no inicia
```bash
# Ver logs detallados
sudo journalctl -u cied.service -n 50

# Ver errores de Python
sudo journalctl -u cied.service | grep -i error

# Verificar que gunicorn está en el PATH correcto
which gunicorn
/home/jarteaga/.local/bin/gunicorn --version
```

### Problema: Puertos ocupados
```bash
# Ver qué usa el puerto 8082
sudo netstat -tlnp | grep :8082

# Cambiar puerto en cied.service si es necesario
sudo systemctl edit cied.service
# Cambiar: --bind 0.0.0.0:8082
```

### Problema: Permisos
```bash
# Verificar permisos del directorio
ls -la /home/jarteaga/Documents/cied/

# Ajustar si es necesario
chmod -R 755 /home/jarteaga/Documents/cied/
```

### Problema: Dependencias faltantes
```bash
# Verificar instalación de Python packages
cd /home/jarteaga/Documents/cied
python3 -c "import flask, gunicorn; print('Dependencies OK')"

# Instalar si faltan
pip install -r requirements.txt
```

## 📊 Monitoreo

### Ver métricas del servicio
```bash
# Ver uso de recursos
sudo systemctl status cied.service

# Ver procesos de Gunicorn
ps aux | grep gunicorn

# Ver conexiones activas
sudo netstat -tlnp | grep :8082
```

### Logs de aplicación
```bash
# Logs de acceso
tail -f /home/jarteaga/Documents/cied/logs/access.log

# Logs de error
tail -f /home/jarteaga/Documents/cied/logs/error.log

# Logs del sistema
sudo journalctl -u cied.service -f
```

## 🔧 Configuración del Servicio

### Configuración Simplificada (Actual)
El servicio usa configuración básica probada:

```ini
[Service]
User=jarteaga
Group=jarteaga
WorkingDirectory=/home/jarteaga/Documents/cied
Environment=PATH=/home/jarteaga/.local/bin:/usr/local/bin:/usr/bin:/bin
ExecStart=/home/jarteaga/.local/bin/gunicorn --workers 2 --bind 0.0.0.0:8082 --timeout 30 --log-level info wsgi:app
Restart=always
RestartSec=5
NoNewPrivileges=true
ProtectHome=false
```

### Variables de entorno opcionales
```bash
# En /etc/systemd/system/cied.service agregar:
Environment=FLASK_ENV=production
Environment=CIED_VALIDATE_WEEK01_STRICT=0
```

### Escalado básico
Para más workers, editar `--workers 2` en ExecStart:
- CPU dual-core: `--workers 2` (actual)
- CPU quad-core: `--workers 4`
- Alta carga: `--workers 8`

## 📞 Soporte

Si encuentras problemas:

1. Ejecuta `python3 scripts/test_deployment.py`
2. Revisa logs: `sudo journalctl -u cied.service -n 100`
3. Verifica permisos y dependencias
4. Asegura que el puerto 8082 esté disponible

## ✅ Checklist de Deployment

- [ ] `python3 scripts/test_deployment.py` pasa todos los tests
- [ ] Servicio systemd copiado a `/etc/systemd/system/`
- [ ] `sudo systemctl daemon-reload` ejecutado
- [ ] Directorio `logs/` creado con permisos correctos
- [ ] `sudo systemctl start cied.service` inicia sin errores
- [ ] Endpoints responden correctamente
- [ ] `sudo systemctl enable cied.service` para arranque automático
- [ ] Verificar logs no muestran errores críticos