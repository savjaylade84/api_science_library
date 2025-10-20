from flask_pymongo import PyMongo
from flask import Flask, render_template,jsonify,request
from marshmallow import Schema, fields,ValidationError
from typing import Any,TypeAlias
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import os
import jwt
import json

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/science_library"
app.config['SECRET_KEY'] = os.getenv('SUPER_SECRET_KEY','default_secret_key')
mongo = PyMongo(app)

mongo.db.books.create_index("id",unique=True)
mongo.db.books.create_index("isbn",unique=True)

# create type for json 
JSONType: TypeAlias = dict[str,Any] | list[Any] | None


# this will make sure the user inputs are validated
class BookSchema(Schema):
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    year = fields.Int(required=True)
    isbn = fields.Str(required=True)
    subject = fields.Str(required=True)
    copies_available = fields.Int(required=True)
    publisher = fields.Str(required=True)

def delete_book_in_db(id:int) -> JSONType:
    result = mongo.db.books.delete_one({"id": id})
    if result.deleted_count:
        return {"Message": "Book deleted successfully!"}
    else:
        return {"Error": "Book not found!"}, 404

def search_books_in_db(query:dict) -> JSONType:
    return mongo.db.books.find(query,{"id":0})

def find_author_in_db(author:str) -> JSONType:
    return mongo.db.books.find({"author":author})

def find_subject_in_db(subject:str) -> JSONType:
    return mongo.db.books.find({"subject":subject})

def find_all_in_db() -> JSONType:
    return mongo.db.books.find()

def find_id_in_db(id:int) -> JSONType:
    return mongo.db.books.find_one({"id": id})

def find_isbn_in_db(isbn:str) -> JSONType:
    return mongo.db.books.find({"isbn":isbn})

def find_publisher_in_db(publisher:str) -> JSONType:
    return mongo.db.books.find({"publisher":publisher})

def find_title_in_db(title:str) -> JSONType:
    return mongo.db.books.find({"title":title})

def find_year_in_db(year:int) -> JSONType:
    return mongo.db.books.find({"year":year})

def find_copies_in_db(copies:int) -> JSONType:
    return mongo.db.books.find({"copies_available":copies})

def count_copies_in_db() -> JSONType:
    pipeline = [
        {
            "$group": {
                "_id": None,
                "total_copies": {"$sum": "$copies_available"}
            }
        }
    ]
    result = list(mongo.db.books.aggregate(pipeline))
    total_copies = result[0]['total_copies'] if result else 0
    return {"total_copies": total_copies}

def count_copies_by_subject_in_db() -> JSONType:
    pipeline = [
        {
            "$group": {
                "_id": "$subject",
                "total_copies": {"$sum": "$subject"}
            }
        }
    ]
    result = list(mongo.db.books.aggregate(pipeline))
    total = []
    for item in result:
        item['total_copies'] += 1
        total.append({item['_id']:item['total_copies']})
    return jsonify(total)

def register(user: dict) -> JSONType:
    return jsonify({"username":user['username'],"password":user['password']})


def sigin(user: dict) -> JSONType:
    return jsonify({"username":user['username'],"password":user['password']})

# this will add book in the database
@app.route('/api/v1/books/manage/append', methods=['POST'])
def append() -> JSONType:
    book = request.get_json()
    if not book:
        return jsonify({"Error": "No data provided!"}), 400
    
    try:
        validate = BookSchema().load(book)
        result = mongo.db.books.insert_one(validate)
        return jsonify({"Message": "Book added successfully!", "book_id": str(result.inserted_id)}), 201
    except ValidationError as e:
        return jsonify({"Error": e.messages}), 400
    except Exception as e:
        return jsonify({"Error": str(e)}), 500


@app.route('/api/v1/books/manage/update',methods=['GET'])
def update() -> JSONType:
    pass

@app.route('/api/v1/books/manage/delete', methods=['DELETE'])
def delete() -> JSONType:
    id: int = request.args.get('id', type=int)
    return jsonify(delete_book_in_db(id))

@app.route('/api/v1/books/filter/view_all', methods=['GET'])
def view_all() -> JSONType:
    return jsonify(find_all_in_db())

@app.route('/api/v1/books/filter/search', methods=['GET'])
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

@app.route('/api/v1/books/filter/author/<string:author>',methods=['GET'])
def find_author(author) -> JSONType:
    return jsonify(find_author_in_db(author))

@app.route('/api/v1/books/filter/subject/<string:subject>',methods=['GET'])
def find_subject(subject) -> JSONType:
    return jsonify(find_subject_in_db(subject))

@app.route('/api/v1/books/filter/id/<int:id>', methods=['GET'])
def find_id(id) -> JSONType:
    return jsonify(find_id_in_db(id))

@app.route('/api/v1/books/filter/isbn/<string:isbn>', methods=['GET'])
def find_isbn(isbn) -> JSONType:
    return jsonify(find_isbn_in_db(isbn))

@app.route('/api/v1/books/filter/publisher/<string:publisher>', methods=['GET'])
def find_publisher(publisher) -> JSONType:
    return jsonify(find_publisher_in_db(publisher))

@app.route('/api/v1/books/filter/title/<string:title>', methods=['GET'])
def find_title(title) -> JSONType:
    return jsonify(find_title_in_db(title))

@app.route('/api/v1/books/filter/year/<int:year>', methods=['GET'])
def find_year(year) -> JSONType:
    return jsonify(find_year_in_db(year))

@app.route('/api/v1/books/filter/copies/<int:copies>', methods=['GET'])
def find_copies(copies) -> JSONType:
    return jsonify(find_copies_in_db(copies))

@app.route('/api/v1/books/stats/total-copies',methods=['GET'])
def count_books() -> JSONType:
    return count_copies_in_db()

@app.route('/api/v1/books/stats/total-copies-by-subject',methods=['GET'])
def count_books_by_subject() -> JSONType:
    return count_copies_by_subject_in_db()

@app.route('/api/v1/books/user/signup',methods=['GET'])
def get_user() -> JSONType:

    username: str = request.args.get('username',type=str)
    password: str = request.args.get('password',type=str)

    if username and password:
       return register({"username": username,"password":password})
    
    return jsonify({'Error': 'Empty Data'})

@app.route('/api/v1/books/user/sigin',methods=['POST'])
def sigin_user() -> JSONType:

    username: str = request.args.get('username',type=str)
    password: str = request.args.get('password',type=str)

    if username and password:
       return sigin({"username":username,"password":password})
    
    return jsonify({'Error': 'Empty Data'})
    

if __name__ == '__main__':
    app.run(debug=True)