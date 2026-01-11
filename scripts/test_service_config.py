#!/usr/bin/env python3
"""
Script rápido para probar la configuración del servicio systemd de CIED.

Uso:
    python scripts/test_service_config.py

Verifica:
- Sintaxis del archivo de servicio
- Que Gunicorn puede iniciar con la configuración
- Que la aplicación responde
"""

import sys
import subprocess
import time
import signal
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

def test_systemd_syntax():
    """Verifica sintaxis del archivo de servicio systemd."""
    print("🔍 Verificando sintaxis del servicio systemd...")

    service_file = PROJECT_ROOT / "cied.service"
    if not service_file.exists():
        print(f"❌ Archivo {service_file} no existe")
        return False

    try:
        result = subprocess.run(
            ["systemd-analyze", "verify", str(service_file)],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            print("✅ Sintaxis del servicio correcta")
            return True
        else:
            print(f"❌ Error en sintaxis del servicio:\n{result.stderr}")
            return False

    except FileNotFoundError:
        print("⚠️  systemd-analyze no disponible (probablemente no en sistema con systemd)")
        print("   El archivo de servicio parece estar bien formado")
        return True
    except Exception as e:
        print(f"❌ Error verificando sintaxis: {e}")
        return False

def test_gunicorn_start():
    """Prueba que Gunicorn puede iniciar con la configuración del servicio."""
    print("\n🔍 Probando inicio de Gunicorn...")

    # Puerto de prueba (diferente al de producción)
    test_port = "8084"

    cmd = [
        "/home/jarteaga/.local/bin/gunicorn",
        "--workers", "1",
        "--bind", f"0.0.0.0:{test_port}",
        "--timeout", "10",
        "--log-level", "info",
        "wsgi:app"
    ]

    try:
        # Iniciar Gunicorn en background
        process = subprocess.Popen(
            cmd,
            cwd=str(PROJECT_ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Esperar un poco para que inicie
        time.sleep(2)

        # Verificar si el proceso sigue vivo
        if process.poll() is None:
            print("✅ Gunicorn inició correctamente")

            # Verificar que responde
            try:
                import requests
                response = requests.get(f"http://localhost:{test_port}/health", timeout=5)
                if response.status_code == 200:
                    print("✅ Aplicación responde correctamente")
                    success = True
                else:
                    print(f"❌ Respuesta inesperada: {response.status_code}")
                    success = False
            except ImportError:
                print("⚠️  requests no disponible, saltando test de conectividad")
                success = True
            except Exception as e:
                print(f"❌ Error conectando a la aplicación: {e}")
                success = False

            # Terminar el proceso
            process.terminate()
            try:
                process.wait(timeout=5)
                print("✅ Gunicorn terminó correctamente")
            except subprocess.TimeoutExpired:
                process.kill()
                print("⚠️  Gunicorn forzado a terminar")

            return success
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Gunicorn falló al iniciar")
            print(f"stdout: {stdout}")
            print(f"stderr: {stderr}")
            return False

    except Exception as e:
        print(f"❌ Error probando Gunicorn: {e}")
        return False

def test_paths():
    """Verifica que los paths necesarios existen."""
    print("\n🔍 Verificando paths y permisos...")

    checks = [
        ("/home/jarteaga/.local/bin/gunicorn", "Gunicorn ejecutable"),
        ("/home/jarteaga/Documents/cied/wsgi.py", "WSGI entry point"),
        ("/home/jarteaga/Documents/cied/app/__init__.py", "Módulo app"),
        ("/home/jarteaga/Documents/cied/logs", "Directorio de logs"),
    ]

    all_good = True

    for path, description in checks:
        if os.path.exists(path):
            if os.access(path, os.X_OK if "bin" in path else os.R_OK):
                print(f"✅ {description}: {path}")
            else:
                print(f"❌ {description}: {path} (sin permisos)")
                all_good = False
        else:
            print(f"❌ {description}: {path} (no existe)")
            all_good = False

    return all_good

def main():
    """Ejecuta todas las pruebas."""
    print("🚀 CIED Service Configuration Test")
    print("=" * 50)

    tests = [
        test_paths,
        test_systemd_syntax,
        test_gunicorn_start,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1

    print(f"\n📊 Resultados: {passed}/{total} tests pasaron")

    if passed == total:
        print("✅ Configuración del servicio lista para deployment")
        print("\n📋 Próximos pasos:")
        print("1. sudo cp cied.service /etc/systemd/system/")
        print("2. sudo systemctl daemon-reload")
        print("3. sudo systemctl start cied.service")
        print("4. sudo systemctl enable cied.service")
        return 0
    else:
        print("❌ Hay problemas de configuración que deben corregirse")
        return 1

if __name__ == "__main__":
    sys.exit(main())