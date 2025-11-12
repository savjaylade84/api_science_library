import pytest 
from  ..app import create_app
from  ..blueprints.website import services as services_web
from  ..blueprints.api import services as services_api
from ..blueprints import generate_random_id

#this a  script for automated testing the api endspoints using pytest framework

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

# global verbose flag for detailed output
verbose = False

def print_test_header(test_name:str,function_name:str,message:str,capsys) -> None:
    global verbose
    with capsys.disabled():
        print(f"\n\n=== Running Test: {test_name} ===")
        print(f"Function: {function_name}")
        if verbose:
            print(f"Message: {message}\n")

def test_view_all(client, capsys) -> None:
    response = client.get('/api/v1/books/filter/view_all')
    print_test_header("test_view_all", "client.get", f"send all the data of the books",capsys)
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_find_author(client, capsys) -> None:
    response = client.get('/api/v1/books/filter/author/Thomas S. Kuhn')
    print_test_header("test_find_author", "client.get", f"Response: {response.get_json()}", capsys)
    assert "Thomas S. Kuhn" in response.get_data(as_text=True)
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_find_subject(client, capsys) -> None:
    response = client.get('/api/v1/books/filter/subject/Genetics')
    print_test_header("test_find_subject", "client.get", f"Response: {response.get_json()}", capsys)
    assert "Genetics" in response.get_data(as_text=True)
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_find_isbn(client, capsys) -> None:
    response = client.get('/api/v1/books/filter/isbn/9780743216302')
    print_test_header("test_find_isbn", "client.get", f"Response: {response.get_json()}", capsys)
    assert "9780743216302" in response.get_data(as_text=True)
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_find_publisher(client, capsys) -> None:
    response = client.get('/api/v1/books/filter/publisher/Mariner Books')
    print_test_header("test_find_publisher", "client.get", f"Response: {response.get_json()}", capsys)
    assert "Mariner Books" in response.get_data(as_text=True)
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_find_title(client, capsys) -> None:
    response = client.get('/api/v1/books/filter/title/The Structure of Scientific Revolutions')
    print_test_header("test_find_title", "client.get", f"Response: {response.get_json()}", capsys)
    assert "The Structure of Scientific Revolutions" in response.get_data(as_text=True)
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_find_year(client, capsys) -> None:
    response = client.get('/api/v1/books/filter/year/1996')
    print_test_header("test_find_year", "client.get", f"Response: {response.get_json()}",capsys)
    for item in response.get_json():
        assert item['year'] == 1996
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_find_copies(client, capsys) -> None:
    response = client.get('/api/v1/books/filter/copies/5')
    print_test_header("test_find_copies", "client.get", f"Response: {response.get_json()}",capsys)
    assert "5" in response.get_data(as_text=True)
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_generate_random_id(capsys) -> None:
    random_id = generate_random_id(10)
    print_test_header("test_generate_random_id", "services.generate_random_id", f"Generated Mock Random ID: {random_id}", capsys)
    assert isinstance(random_id, str)
    assert len(random_id) == 10

def test_generate_payload(capsys) -> None:
    payload = services_api.generate_payload({"user_id":123,"username":"test"},services_api.KeyType.SUPER_KEY,True)
    print_test_header("test_generate_payload", "services.generate_payload", f"Generated Mock Payload: {payload}", capsys)
    assert isinstance(payload,dict)

def test_generate_token(capsys) -> None:
    token = services_api.generate_token({"user_id":123,"username":"test"},services_api.KeyType.SUPER_KEY)
    print_test_header("test_generate_token", "services.generate_token", f"Generated Mock Token: {token}", capsys)
    assert isinstance(token,str)

def test_generate_hash_key(capsys) -> None:
    payload = services_api.generate_payload({"user_id":123,"username":"test"},services_api.KeyType.SUPER_KEY,True)
    super_key = generate_random_id(25,"#@&%*")
    hash_key = services_api.generate_hash_key(payload=payload,super_key=super_key)
    print_test_header("test_generate_hash_key", "services.generate_hash_key", f"Generated Mock Hash Key: {hash_key}", capsys)
    assert isinstance(hash_key,str)
    assert len(hash_key) > 0

