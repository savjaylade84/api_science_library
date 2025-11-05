import pytest 
from  app import create_app


#this a  script for automated testing the api endspoints using pytest framework

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    yield app

@pytest.fixture
def client(app):
    return app.test_client()
    

# test the view all books endpoint
def test_view_all(client):
    response = client.get('/api/v1/books/filter/view_all')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
