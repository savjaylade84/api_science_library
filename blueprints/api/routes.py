from flask import blueprints,jsonify,request
from marshmallow import ValidationError
from .services import *
from . import *

# this will add book in the database
@library_bp.route('/api/v1/books/manage/append', methods=['POST'])
def append() -> JSONType:
    
    # get the book information from the request body
    book = request.get_json()

    # check if book data exists or send error response
    if not book:
        logger.error("No book data provided")
        return jsonify({"Error": "No data provided!"}), 400
    
    # check for validation errors and append book
    try:
        validate = BookSchema().load(book)
        return jsonify(append_book_in_db(validate)), 201
    except ValidationError as e:
        logger.error(f"Validation error while appending book: {e.messages}")
        return jsonify({"Error": e.messages}), 400
    except Exception as e:
        logger.error(f"Unexpected error while appending book: {str(e)}")
        return jsonify({"Error": str(e)}), 500


@library_bp.route('/api/v1/books/manage/update',methods=['GET'])
def update() -> JSONType:
    pass

@library_bp.route('/api/v1/books/manage/delete', methods=['DELETE'])
def delete() -> JSONType:
    id: int = request.args.get('id', type=int)
    return jsonify(delete_book_in_db(id))

@library_bp.route('/api/v1/books/filter/view_all', methods=['GET'])
def view_all() -> JSONType:
    return jsonify(find_all_in_db())

@library_bp.route('/api/v1/books/filter/search', methods=['GET'])
def search() -> JSONType:

    # get the query parameters
    id:int = request.args.get('id',type=int)
    title:str = request.args.get('title',type=str)
    author:str = request.args.get('author',type=str)
    year:int = request.args.get('year',type=int)
    isbn:str = request.args.get('isbn',type=str)
    subject:str = request.args.get('subject',type=str)
    copies:int = request.args.get('copies',type=int)
    publisher:str = request.args.get('publisher',type=str)

    query:dict = {}

    #check which parameters are provided and build the query accordingly
    if id:
        query['id'] = int(id)
    
    if title:
        query['title'] = title

    if author:
        query['author'] = author

    if year:
        query['year'] = int(year)

    if isbn:
        query['isbn'] = isbn

    if subject:
        query['subject'] = subject

    if copies:
        query['copies_available'] = int(copies)

    if publisher:
        query['publisher'] = publisher

    return jsonify(search_books_in_db(query))

@library_bp.route('/api/v1/books/filter/author/<string:author>',methods=['GET'])
def find_author(author) -> JSONType:
    return jsonify(find_author_in_db(author))

@library_bp.route('/api/v1/books/filter/subject/<string:subject>',methods=['GET'])
def find_subject(subject) -> JSONType:
    return jsonify(find_subject_in_db(subject))

@library_bp.route('/api/v1/books/filter/id/<int:id>', methods=['GET'])
def find_id(id) -> JSONType:
    return jsonify(find_id_in_db(id))

@library_bp.route('/api/v1/books/filter/isbn/<string:isbn>', methods=['GET'])
def find_isbn(isbn) -> JSONType:
    return jsonify(find_isbn_in_db(isbn))

@library_bp.route('/api/v1/books/filter/publisher/<string:publisher>', methods=['GET'])
def find_publisher(publisher) -> JSONType:
    return jsonify(find_publisher_in_db(publisher))

@library_bp.route('/api/v1/books/filter/title/<string:title>', methods=['GET'])
def find_title(title) -> JSONType:
    return jsonify(find_title_in_db(title))

@library_bp.route('/api/v1/books/filter/year/<int:year>', methods=['GET'])
def find_year(year) -> JSONType:
    return jsonify(find_year_in_db(year))

@library_bp.route('/api/v1/books/filter/copies/<int:copies>', methods=['GET'])
def find_copies(copies) -> JSONType:
    return jsonify(find_copies_in_db(copies))

@library_bp.route('/api/v1/books/stats/total-copies',methods=['GET'])
def count_books() -> JSONType:
    return count_copies_in_db()

@library_bp.route('/api/v1/books/stats/total-copies-by-subject',methods=['GET'])
def count_books_by_subject() -> JSONType:
    return count_copies_by_subject_in_db()

@library_bp.route('/api/v1/books/user/sign_up',methods=['GET'])
def sign_up() -> JSONType:

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

@library_bp.route('/api/v1/books/user/sign_in',methods=['POST'])
def sign_in() -> JSONType:

    username: str = request.args.get('username',type=str)
    password: str = request.args.get('password',type=str)
    token: str = request.args.get('token',type=str)

    if username and password and token:
       return login_user({"username":username,"password":password})
    
    return jsonify({'Error': 'Empty Data'})


