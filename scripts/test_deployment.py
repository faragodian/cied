#!/usr/bin/env python3
"""
Script de verificación para deployment de CIED.

Uso:
    python scripts/test_deployment.py

Verifica:
- WSGI application loads correctly
- Flask app can be created
- Basic endpoints respond
- No import errors
"""

import sys
import os
from pathlib import Path

# Setup paths
script_dir = Path(__file__).parent.parent
sys.path.insert(0, str(script_dir))

def test_wsgi_import():
    """Test WSGI application import."""
    print("🔍 Testing WSGI import...")
    try:
        import wsgi
        print("✅ WSGI module imported successfully")
        print(f"   App type: {type(wsgi.app)}")
        return True
    except Exception as e:
        print(f"❌ WSGI import failed: {e}")
        return False

def test_app_creation():
    """Test Flask app creation."""
    print("\n🔍 Testing Flask app creation...")
    try:
        from app import create_app
        app = create_app()
        print("✅ Flask app created successfully")
        print(f"   App name: {app.name}")
        print(f"   Debug mode: {app.debug}")
        print(f"   Testing mode: {app.testing}")
        return app
    except Exception as e:
        print(f"❌ Flask app creation failed: {e}")
        return None

def test_routes(app):
    """Test basic routes."""
    print("\n🔍 Testing routes...")
    if not app:
        print("❌ No app to test")
        return False

    try:
        with app.test_client() as client:
            # Test root endpoint
            response = client.get('/')
            print(f"   GET /: {response.status_code}")

            # Test health endpoint
            response = client.get('/health')
            print(f"   GET /health: {response.status_code}")

            # Test syllabus endpoint
            response = client.get('/syllabus')
            print(f"   GET /syllabus: {response.status_code}")

            print("✅ Route tests completed")
            return True
    except Exception as e:
        print(f"❌ Route testing failed: {e}")
        return False

def test_gunicorn_compatibility():
    """Test Gunicorn compatibility."""
    print("\n🔍 Testing Gunicorn compatibility...")
    try:
        # Test that wsgi:app is callable
        import wsgi
        app = wsgi.app

        # Test that it's a WSGI application (has __call__)
        if hasattr(app, '__call__'):
            print("✅ WSGI application has __call__ method")
        else:
            print("❌ WSGI application missing __call__ method")
            return False

        # Test basic WSGI interface
        try:
            # Create minimal WSGI environ
            environ = {
                'REQUEST_METHOD': 'GET',
                'PATH_INFO': '/',
                'SERVER_NAME': 'localhost',
                'SERVER_PORT': '8082',
                'wsgi.version': (1, 0),
                'wsgi.url_scheme': 'http',
                'wsgi.input': None,
                'wsgi.errors': sys.stderr,
                'wsgi.multithread': False,
                'wsgi.multiprocess': False,
                'wsgi.run_once': False,
            }

            # Test that start_response is accepted
            def start_response(status, headers):
                pass

            result = app(environ, start_response)
            print("✅ WSGI interface test passed")
            return True

        except Exception as e:
            print(f"❌ WSGI interface test failed: {e}")
            return False

    except Exception as e:
        print(f"❌ Gunicorn compatibility test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 CIED Deployment Test Suite")
    print("=" * 40)

    tests = [
        test_wsgi_import,
        lambda: test_routes(test_app_creation()),
        test_gunicorn_compatibility,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1

    print(f"\n📊 Results: {passed}/{total} tests passed")

    if passed == total:
        print("✅ All tests passed! Ready for deployment.")
        return 0
    else:
        print("❌ Some tests failed. Please fix before deploying.")
        return 1

if __name__ == "__main__":
    sys.exit(main())