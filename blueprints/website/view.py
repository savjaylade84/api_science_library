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
    pass

@library_wb_bp.route('/api/v1/books/user/sign_in',methods=['POST'])
def sign_in() -> dict:
    pass

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