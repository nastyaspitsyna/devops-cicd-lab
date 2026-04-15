import os
import pytest

# Добавляем путь, чтобы импортировать из src
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert 'service' in data
    assert 'version' in data
    assert 'hostname' in data

def test_health_endpoint(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json() == {'status': 'ok'}

def test_greeting_old_default(client):
    response = client.get('/greeting')
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Hello, world!'}

def test_greeting_new_feature():
    # Устанавливаем переменную окружения перед импортом модуля
    os.environ['FEATURE_NEW_GREETING'] = 'true'
    
    # Переимпортируем модуль заново
    import importlib
    import sys
    if 'src.app' in sys.modules:
        del sys.modules['src.app']
    from src.app import app as new_app
    
    with new_app.test_client() as client:
        response = client.get('/greeting')
        assert response.status_code == 200
        assert response.get_json() == {'message': 'Hello from the new feature!'}
    
    # Очищаем переменную, чтобы не влиять на другие тесты
    del os.environ['FEATURE_NEW_GREETING']