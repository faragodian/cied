"""
Pruebas básicas para las rutas de la aplicación cied
"""

import pytest
import json
from pathlib import Path
from app import create_app


@pytest.fixture
def app():
    """Fixture para crear la aplicación de prueba"""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Fixture para crear cliente de pruebas"""
    return app.test_client()


def test_index_route(client):
    """Prueba el endpoint raíz"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'CIED' in response.data
    assert b'C\xc3\xa1lculo Integral' in response.data


def test_health_route(client):
    """Prueba el endpoint de health check"""
    response = client.get('/health')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert data['status'] == 'ok'
    assert 'docs_available' in data
    assert data['service'] == 'cied-web'


def test_list_errors_route(client):
    """Prueba el endpoint para listar errores"""
    response = client.get('/errors/')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert 'count' in data
    assert 'errors' in data
    assert isinstance(data['errors'], list)

    # Debería haber al menos un error (el de ejemplo)
    assert data['count'] >= 1

    # Verificar estructura del primer error
    if data['errors']:
        error = data['errors'][0]
        assert 'id' in error
        assert 'titulo' in error
        assert 'curso' in error


def test_get_specific_error(client):
    """Prueba obtener un error específico por ID"""
    # Primero obtener la lista para saber qué ID existe
    response = client.get('/errors/')
    data = json.loads(response.data)

    if data['errors']:
        error_id = data['errors'][0]['id']

        # Ahora obtener el error específico
        response = client.get(f'/errors/{error_id}')
        assert response.status_code == 200

        error_data = json.loads(response.data)
        assert error_data['id'] == error_id
        assert 'titulo' in error_data
        assert 'descripcion_corta' in error_data
    else:
        pytest.skip("No hay errores para probar")


def test_get_nonexistent_error(client):
    """Prueba obtener un error que no existe"""
    response = client.get('/errors/nonexistent-id')
    assert response.status_code == 404


def test_search_errors_empty_query(client):
    """Prueba búsqueda con query vacío (debería devolver todos)"""
    response = client.get('/errors/search')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert 'count' in data
    assert 'results' in data


def test_search_errors_with_query(client):
    """Prueba búsqueda con query específico"""
    # Buscar por un término que debería existir en el error de ejemplo
    response = client.get('/errors/search?q=factor')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert 'query' in data
    assert 'count' in data
    assert 'results' in data
    assert data['query'] == 'factor'


def test_search_errors_no_results(client):
    """Prueba búsqueda que no debería encontrar resultados"""
    response = client.get('/errors/search?q=terminoquenoexiste12345')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert data['count'] == 0
    assert data['results'] == []
