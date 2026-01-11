#!/bin/bash
#
# Script de instalación del servicio systemd para CIED
# Uso: ./scripts/install_service.sh
#

set -e  # Salir en caso de error

echo "🚀 Instalando servicio CIED..."

# Verificar que estamos en el directorio correcto
if [ ! -f "cied.service" ]; then
    echo "❌ Error: cied.service no encontrado. Ejecutar desde raíz del proyecto."
    exit 1
fi

# Verificar permisos de sudo
if ! sudo -n true 2>/dev/null; then
    echo "⚠️  Este script requiere permisos de administrador."
    echo "   Se ejecutarán comandos con sudo."
fi

# Copiar archivo de servicio
echo "📋 Copiando archivo de servicio..."
sudo cp cied.service /etc/systemd/system/

# Recargar systemd
echo "🔄 Recargando configuración de systemd..."
sudo systemctl daemon-reload

# Detener servicio si está corriendo
echo "🛑 Deteniendo servicio existente (si existe)..."
sudo systemctl stop cied.service || true

# Habilitar servicio para arranque automático
echo "✅ Habilitando servicio para arranque automático..."
sudo systemctl enable cied.service

# Iniciar servicio
echo "▶️  Iniciando servicio..."
sudo systemctl start cied.service

# Verificar estado
echo "📊 Verificando estado del servicio..."
sleep 2
sudo systemctl status cied.service --no-pager

# Verificar que esté escuchando en el puerto
echo "🔍 Verificando conectividad..."
if curl -s --max-time 5 http://localhost:8082/health > /dev/null 2>&1; then
    echo "✅ Servicio funcionando correctamente en puerto 8082"
else
    echo "⚠️  Servicio iniciado pero no responde en puerto 8082"
    echo "   Revisar logs: sudo journalctl -u cied.service -n 20"
fi

echo ""
echo "🎉 Instalación completada!"
echo ""
echo "Comandos útiles:"
echo "  Ver estado:    sudo systemctl status cied.service"
echo "  Ver logs:      sudo journalctl -u cied.service -f"
echo "  Reiniciar:     sudo systemctl restart cied.service"
echo "  Detener:       sudo systemctl stop cied.service"
echo ""
echo "El servicio ahora debería iniciar automáticamente en cada reboot."