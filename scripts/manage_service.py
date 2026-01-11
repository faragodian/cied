#!/usr/bin/env python3
"""
Script de gestión del servicio systemd para CIED.

Uso:
    python scripts/manage_service.py [comando]

Comandos disponibles:
    start     - Iniciar el servicio
    stop      - Detener el servicio
    restart   - Reiniciar el servicio
    status    - Ver estado del servicio
    logs      - Ver logs del servicio
    enable    - Habilitar arranque automático
    disable   - Deshabilitar arranque automático
    test      - Ejecutar tests de deployment
"""

import sys
import subprocess
import argparse
from pathlib import Path

SERVICE_NAME = "cied.service"
PROJECT_ROOT = Path(__file__).parent.parent

def run_command(cmd, check=True, capture_output=False):
    """Ejecuta un comando del sistema."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=check,
            capture_output=capture_output,
            text=True,
            cwd=PROJECT_ROOT
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando comando: {e}")
        return None

def service_command(action):
    """Ejecuta un comando de systemctl."""
    cmd = f"sudo systemctl {action} {SERVICE_NAME}"
    print(f"🔧 Ejecutando: {cmd}")
    result = run_command(cmd)
    if result and result.returncode == 0:
        print(f"✅ Servicio {action} ejecutado correctamente")
    return result

def show_logs(lines=50):
    """Muestra logs del servicio."""
    cmd = f"sudo journalctl -u {SERVICE_NAME} -n {lines}"
    print(f"📋 Mostrando últimas {lines} líneas de logs:")
    run_command(cmd)

def show_status():
    """Muestra estado detallado del servicio."""
    print("📊 Estado del servicio CIED:")
    service_command("status")

def run_tests():
    """Ejecuta tests de deployment."""
    print("🧪 Ejecutando tests de deployment...")
    cmd = "python3 scripts/test_deployment.py"
    result = run_command(cmd)
    return result and result.returncode == 0

def main():
    parser = argparse.ArgumentParser(
        description="Gestión del servicio systemd para CIED",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python scripts/manage_service.py start
  python scripts/manage_service.py logs
  python scripts/manage_service.py test
        """
    )

    parser.add_argument(
        "command",
        choices=["start", "stop", "restart", "status", "logs", "enable", "disable", "test"],
        help="Comando a ejecutar"
    )

    parser.add_argument(
        "--lines", "-n",
        type=int,
        default=50,
        help="Número de líneas de logs a mostrar (default: 50)"
    )

    args = parser.parse_args()

    print(f"🚀 CIED Service Manager - Comando: {args.command}")
    print("=" * 50)

    if args.command == "test":
        success = run_tests()
        if success:
            print("✅ Tests pasaron correctamente")
        else:
            print("❌ Tests fallaron")
        return 0 if success else 1

    elif args.command == "logs":
        show_logs(args.lines)
        return 0

    elif args.command == "status":
        show_status()
        return 0

    else:
        # Comandos de systemctl: start, stop, restart, enable, disable
        result = service_command(args.command)
        return result.returncode if result else 1

if __name__ == "__main__":
    sys.exit(main())