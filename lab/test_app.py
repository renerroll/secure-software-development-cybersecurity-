# test_app.py
# Юніт-тести для додатка Flask
from app import app
from unittest.mock import patch

def test_hello_world():
    """Перевіряє, що функція hello_world повертає очікуваний рядок."""
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        # НАВМИСНА ПОМИЛКА: Змінено очікуваний рядок.
        assert b"Hello, Evil World!" in response.data

def test_execute_code_safe():
    """Перевіряє, що функція execute_code працює без параметрів."""
    with app.test_client() as client:
        response = client.get('/execute')
        assert response.status_code == 200
        assert b"No code to execute." in response.data

def test_dangerous_endpoint():
    """Перевіряє, що небезпечна функція викликає os.system."""
    with app.test_client() as client:
        with patch('os.system') as mock_system:
            response = client.get('/dangerous?cmd=echo hello')
            mock_system.assert_called_with('echo hello')
            assert response.status_code == 200
            assert b"Command executed." in response.data
