from flask import render_template,current_app,request,session,jsonify,blueprints
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

    # get the user information from the request body
    user = request.get_json()

    # check if user data exists or send error response
    if not user:
        logger.error("No user data provided")
        return jsonify({"Error": "No data provided!"}), 400

    # check for validation errors and register user
    try:
        validate = AccountSchema().load(user)
        return jsonify(register_acc_in_db(validate))
    except ValidationError as e:
        logger.error(f"Validation error during sign up: {e.messages}")
        return jsonify({"Error": e.messages}), 400
    except Exception as e:
        logger.error(f"Unexpected error during sign up: {str(e)}")
        return jsonify({"Error": str(e)}), 500

@library_wb_bp.route('/api/v1/books/user/sign_in',methods=['POST'])
def sign_in() -> dict:

    username: str = request.args.get('username',type=str)
    password: str = request.args.get('password',type=str)
    token: str = request.args.get('token',type=str)
    
    if session.get('logged_in'):
        return jsonify({'Message': 'User already logged in'})
    else:
        if verify_user({"username":username,"password":password}):
            session['logged_in'] = True
            return jsonify({'Message': 'User successfully logged in'})
    
    return jsonify({'Error': 'Invalid username or password'}), 401

# Home route for the website
@library_wb_bp.route('/',methods=['GET'])
@library_wb_bp.route('/home',methods=['GET'])
def index():

    # Fetch all books from the Science Library API
    with current_app.test_client() as client:
        response = client.get('/api/v1/books/filter/view_all')

        # Check if the request was successful
        if response.status_code == 200:
            books = json.loads(response.data)
        else:
            books = []

    return render_template('index.html', books = books)