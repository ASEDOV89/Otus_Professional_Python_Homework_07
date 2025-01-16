import requests

def test_get_method():
    response = requests.get('http://localhost:8080')
    assert response.status_code == 200
    assert 'Добро пожаловать' in response.text

def test_head_method():
    response = requests.head('http://localhost:8080')
    assert response.status_code == 200
    assert response.text == ''

if __name__ == "__main__":
    test_get_method()
    test_head_method()
    print("функциональное тестирование пройдено")