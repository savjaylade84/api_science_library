import pytest 
from  ..app import create_app
from  ..blueprints.api import services
from typing import get_origin

#this a  script for automated testing the api endspoints using pytest framework

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    yield app

@pytest.fixture
def client(app):
    return app.test_client()
    


def test_view_all(client) -> None:
    response = client.get('/api/v1/books/filter/view_all')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_find_author(client) -> None:
    response = client.get('/api/v1/books/filter/author/Thomas S. Kuhn')
    assert "Thomas S. Kuhn" in response.get_data(as_text=True)
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_find_subject(client) -> None:
    response = client.get('/api/v1/books/filter/subject/Genetics')
    assert "Genetics" in response.get_data(as_text=True)
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_find_isbn(client) -> None:
    response = client.get('/api/v1/books/filter/isbn/9780743216302')
    assert "9780743216302" in response.get_data(as_text=True)
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_find_publisher(client) -> None:
    response = client.get('/api/v1/books/filter/publisher/Mariner Books')
    assert "Mariner Books" in response.get_data(as_text=True)
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_find_title(client) -> None:
    response = client.get('/api/v1/books/filter/title/The Structure of Scientific Revolutions')
    assert "The Structure of Scientific Revolutions" in response.get_data(as_text=True)
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_find_year(client) -> None:
    response = client.get('/api/v1/books/filter/year/1996')
    for item in response.get_json():
        assert item['year'] == 1996
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_find_copies(client) -> None:
    response = client.get('/api/v1/books/filter/copies/5')
    assert "5" in response.get_data(as_text=True)
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_generate_random_id() -> None:
    random_id = services.generate_random_id(10)
    assert isinstance(random_id, str)
    assert len(random_id) == 10

def test_generate_payload() -> None:
    payload = services.generate_payload({"user_id":123,"username":"test"},services.KeyType.SUPER_KEY,True)
    assert isinstance(payload,dict)

def test_generate_token() -> None:
    token = services.generate_token({"user_id":123,"username":"test"},services.KeyType.SUPER_KEY)
    assert isinstance(token,str)

