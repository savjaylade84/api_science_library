from marshmallow import ValidationError
from . import *
from .services import *
import json

@library_wb_bp.route('/api/v1/books/users/validation',methods=['GET'])
def validate_users() -> JSONType:
    pass


@library_wb_bp.route('/api/v1/books/users/append',methods=['GET'])
def append_user() -> JSONType:
    pass

@library_wb_bp.route('/api/v1/books/users/update',methods=['GET'])
def update_users() -> JSONType:
    pass


@library_wb_bp.route('/api/v1/books/user/sign_up',methods=['GET'])
def sign_up() -> dict:
    pass

@library_wb_bp.route('/api/v1/books/user/sign_in',methods=['POST'])
def sign_in() -> dict:
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return render_template('login.html', error="Username and password are required.")

    # Use the test_client to "mock" a call to our own API endpoint
    with current_app.test_client() as client:
        api_response = client.post(
            '/api/v1/books/users/identify_current_user',
            json={'username': username, 'password': password}
        )

    if api_response.status_code == 200:
        tokens = api_response.get_json()
        access_token = tokens.get('access_token')
        refresh_token = tokens.get('refresh_token')
        response = make_response(redirect(url_for('library_wb.index'))) # Redirect to home page
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)
        return response
    else:
        return render_template('login.html', error="Invalid username or password") # Render login form with error

# Home route for the website
@library_wb_bp.route('/',methods=['GET'])
@library_wb_bp.route('/home',methods=['GET'])
@jwt_required() # This decorator ensures a valid access token is present
def index():

    # Fetch all books from the Science Library API
    with current_app.test_client() as client:
        response = client.get('/api/v1/books/filter/view_all')

        # Check if the request was successful
        if response.status_code == 200: # type: ignore
            books = json.loads(response.data)
        else:
            # If API call fails, handle it gracefully
            # For example, log the error and return an empty list or an error message
            current_app.logger.error(f"Failed to fetch books from API: {response.status_code}") # type: ignore
            books = []

    return render_template('index.html', books = books)

@library_wb_bp.route('/logout', methods=['POST'])
def logout():
    response = make_response(redirect(url_for('library_wb.sign_in'))) # Redirect to login page
    unset_jwt_cookies(response)
    return response