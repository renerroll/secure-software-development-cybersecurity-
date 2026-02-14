# test_app.py
import pytest
from app import app
from werkzeug.exceptions import BadRequest

@pytest.fixture
def client():
    """Створює тестового клієнта для додатку Flask."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_hello_world_route(client):
    """
    Перевіряє, чи правильно працює маршрут '/'.
    """
    response = client.get('/')
    # Замість assert, використовуємо if-else для відповідності вимогам Bandit B101
    if response.status_code != 200:
        raise AssertionError(f"Очікуваний код статусу 200, отримано {response.status_code}")
    if b"Hello, World!" not in response.data:
        raise AssertionError("Очікуваний текст 'Hello, World!' не знайдено.")

def test_execute_route_literal(client):
    """
    Перевіряє, чи правильно маршрут '/execute' обробляє безпечні літерали.
    """
    response = client.get('/execute?code=123')
    if response.status_code != 200:
        raise AssertionError(f"Очікуваний код статусу 200, отримано {response.status_code}")
    if b"Result of execution: 123" not in response.data:
        raise AssertionError("Очікуваний результат 'Result of execution: 123' не знайдено.")

def test_execute_route_invalid_input(client):
    """
    Перевіряє, чи правильно маршрут '/execute' обробляє небезпечні вирази.
    """
    response = client.get('/execute?code=1+1')
    if response.status_code != 200:
        raise AssertionError(f"Очікуваний код статусу 200, отримано {response.status_code}")
    if b"Error: Invalid input. Only literal values allowed." not in response.data:
        raise AssertionError("Очікуване повідомлення про помилку не знайдено.")
