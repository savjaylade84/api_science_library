from flask import jsonify,request
from marshmallow import ValidationError
from .services import *

from . import *

# This set will store the unique identifiers (jti) of revoked JWTs.
# When a user logs out, their token's jti is added here.
# The JWTManager is configured in the main app to check this blocklist.
BLOCKLIST = set()

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

    query:dict = {}
    query = add_filter(query,request.args.get('id',type=int),'id',int)
    query = add_filter(query,request.args.get('title',type=str),'title',str)
    query = add_filter(query,request.args.get('author',type=str),'author',str)
    query = add_filter(query,request.args.get('year',type=int),'year',int)
    query = add_filter(query,request.args.get('isbn',type=str),'isbn',str)
    query = add_filter(query,request.args.get('subject',type=str),'subject',str)
    query = add_filter(query,request.args.get('copies',type=int),'copies',int)
    query = add_filter(query,request.args.get('publisher',type=str),'publisher',str)

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
    return jsonify(count_copies_in_db())

@library_bp.route('/api/v1/books/stats/total-copies-by-subject',methods=['GET'])
def count_books_by_subject() -> JSONType:
    return jsonify(count_copies_by_subject_in_db())

@library_bp.route('/api/v1/books/users/identify_current_user',methods=['GET'])
@library_bp.route('/api/v1/books/users/identify_current_user',methods=['POST']) # Changed to POST for security
def identify_current_user() -> JSONType:
    # For POST requests, get data from JSON body
    if request.is_json:
        username = request.json.get('username', None)
        password = request.json.get('password', None)
    else:
        return jsonify({'Error': 'Request must be JSON'}), 415
    
    if username and password:
        result = verify_user_in_db({"username":username,"password":password})
        # Assuming verify_user_in_db returns a dictionary with 'Status' and 'Data'
        if result and result.get('Status') == Status.Success:
            # Create the tokens
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            return jsonify(access_token=access_token, refresh_token=refresh_token), 200
        else:
            return jsonify({'Error': 'Invalid username or password'}), 401
    return jsonify({'Error': 'Missing username or password'}), 400

@library_bp.route('/api/v1/books/users/refresh_token', methods=['POST'])
# In Flask-JWT-Extended v4.0+, `jwt_refresh_token_required()` was deprecated.
# The new standard is to use `@jwt_required(refresh=True)` to protect
# an endpoint with a refresh token.
@jwt_required(refresh=True) 
def refresh_token() -> JSONType:
    """
    Refresh token endpoint. This will generate a new access token from
    a valid refresh token.
    """
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token), 200

@library_bp.route('/api/v1/books/users/logout', methods=['DELETE'])
@jwt_required()
def logout() -> JSONType:
    """
    Endpoint for revoking the current access token.
    """
    # A JWT's "jti" (JWT ID) is a unique identifier for that token.
    # We get the jti of the token being used to access this endpoint...
    jti = get_jwt()["jti"]
    # ...and add it to the blocklist. Now, this specific token can't be used again.
    BLOCKLIST.add(jti)
    return jsonify({"msg": "Access token revoked"}), 200

@library_bp.route('/api/v1/books/users/logout_refresh', methods=['DELETE'])
# This endpoint is also protected with a refresh token, following the updated
# decorator syntax for Flask-JWT-Extended v4.0+.
@jwt_required(refresh=True) 
def logout_refresh() -> JSONType:
    """
    Endpoint for revoking the current refresh token.
    """
    # Just like with the access token logout, we get the refresh token's jti...
    jti = get_jwt()["jti"]
    # ...and add it to the blocklist to revoke it.
    BLOCKLIST.add(jti)
    return jsonify({"msg": "Refresh token revoked"}), 200