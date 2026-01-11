#!/usr/bin/env python3
"""
Script para diagnosticar problemas de arranque del servicio systemd.
Simula exactamente lo que hace systemd al iniciar el servicio.
"""

import os
import sys
import subprocess
import time

def test_service_environment():
    """Simula el entorno que crea systemd para el servicio."""
    print("🔍 Probando entorno del servicio...")

    # Cambiar al directorio de trabajo
    os.chdir("/home/jarteaga/Documents/cied")

    # Configurar variables de entorno como en el servicio
    os.environ["PATH"] = "/home/jarteaga/.local/bin:/usr/local/bin:/usr/bin:/bin"
    os.environ["PYTHONPATH"] = "/home/jarteaga/Documents/cied"

    # Cambiar usuario/grupo si es posible (solo informativo)
    try:
        import pwd
        user_info = pwd.getpwuid(os.getuid())
        print(f"   Usuario actual: {user_info.pw_name}")
        print(f"   Grupo actual: {user_info.pw_name}")
    except:
        print("   Usuario actual: desconocido")

    print(f"   WorkingDirectory: {os.getcwd()}")
    print(f"   PYTHONPATH: {os.environ.get('PYTHONPATH')}")
    print(f"   PATH: {os.environ.get('PATH')}")

    return True

def test_gunicorn_command():
    """Prueba el comando exacto que usa ExecStart."""
    print("\n🔍 Probando comando Gunicorn...")

    cmd = [
        "/home/jarteaga/.local/bin/gunicorn",
        "--workers", "1",  # Usar 1 worker para testing
        "--bind", "0.0.0.0:8084",  # Puerto diferente
        "--timeout", "10",  # Timeout más corto
        "--log-level", "info",
        "wsgi:app"
    ]

    print(f"   Comando: {' '.join(cmd)}")

    try:
        # Iniciar proceso
        process = subprocess.Popen(
            cmd,
            cwd="/home/jarteaga/Documents/cied",
            env=os.environ.copy(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Esperar un poco para que inicie
        time.sleep(3)

        # Verificar si sigue vivo
        if process.poll() is None:
            print("   ✅ Gunicorn inició correctamente")

            # Terminar proceso
            process.terminate()
            try:
                process.wait(timeout=5)
                print("   ✅ Gunicorn terminó correctamente")
                return True
            except subprocess.TimeoutExpired:
                process.kill()
                print("   ⚠️  Gunicorn forzado a terminar")
                return True
        else:
            stdout, stderr = process.communicate()
            print(f"   ❌ Gunicorn falló con código {process.returncode}")
            print(f"   stdout: {stdout}")
            print(f"   stderr: {stderr}")
            return False

    except Exception as e:
        print(f"   ❌ Error al ejecutar Gunicorn: {e}")
        return False

def test_file_access():
    """Verifica acceso a archivos críticos."""
    print("\n🔍 Verificando acceso a archivos...")

    files_to_check = [
        "/home/jarteaga/.local/bin/gunicorn",
        "/home/jarteaga/Documents/cied/wsgi.py",
        "/home/jarteaga/Documents/cied/app/__init__.py"
    ]

    for file_path in files_to_check:
        if os.path.exists(file_path):
            if os.access(file_path, os.R_OK):
                print(f"   ✅ {file_path}")
            else:
                print(f"   ❌ {file_path} (sin permisos de lectura)")
                return False
        else:
            print(f"   ❌ {file_path} (no existe)")
            return False

    return True

def main():
    """Ejecuta todas las pruebas."""
    print("🚀 Diagnóstico de Servicio CIED")
    print("=" * 40)

    tests = [
        test_file_access,
        test_service_environment,
        test_gunicorn_command,
    ]

    passed = 0
    for test in tests:
        if test():
            passed += 1

    print(f"\n📊 Resultado: {passed}/{len(tests)} pruebas pasaron")

    if passed == len(tests):
        print("✅ El servicio debería funcionar correctamente")
        print("\n💡 Si systemd aún falla, posibles soluciones:")
        print("   1. Copiar cied.service a /etc/systemd/system/")
        print("   2. Ejecutar: sudo systemctl daemon-reload")
        print("   3. Verificar logs: sudo journalctl -u cied.service")
    else:
        print("❌ Hay problemas que impiden el arranque del servicio")
        print("   Revisar permisos y configuración antes de continuar")

    return passed == len(tests)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)