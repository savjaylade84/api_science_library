from flask_pymongo import PyMongo
from flask import Flask, render_template,jsonify,request
from marshmallow import Schema, fields,ValidationError
import json

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/science_library"
mongo = PyMongo(app)

mongo.db.books.create_index("id",unique=True)
mongo.db.books.create_index("isbn",unique=True)

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

def find_all_books_in_db() -> dict:
    return mongo.db.books.find()

def find_book_in_db(book_id) -> dict:
    return mongo.db.books.find_one({"id": int(book_id)})

def delete_book_in_db(book_id) -> dict:
    result = mongo.db.books.delete_one({"id": int(book_id)})
    if result.deleted_count:
        return {"Message": "Book deleted successfully!"}
    else:
        return {"Error": "Book not found!"}, 404

def search_books_in_db(query:dict) -> dict:
    return mongo.db.books.find(query,{"id":0})

def find_author_in_db(author:str) -> dict:
    return mongo.db.books.find({"author":author})

def find_subject_in_db(subject: str) -> dict:
    return mongo.db.books.find({"subject":subject})

# this will add book in the database
@app.route('/books/add', methods=['POST'])
def add_book():
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


@app.route('/books/view_all', methods=['GET'])
def find_books():
    return jsonify(find_all_books_in_db())

@app.route('/books/search', methods=['GET'])
def search_books():

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

@app.route('/books/author',methods=['GET'])
def find_author():
    author: str = request.args.get('author',type=str)
    return jsonify(find_author_in_db(author))

@app.route('/books/subject',methods=['GET'])
def find_subject():
    subject: str = request.args.get('subject')
    return jsonify(find_subject_in_db(subject))

@app.route('/books/view', methods=['GET'])
def find_book():
    id: int = request.args.get('id', type=int)
    return jsonify(find_book_in_db(id))

@app.route('/books/delete', methods=['DELETE'])
def remove_book():
    id: int = request.args.get('id', type=int)
    return jsonify(delete_book_in_db(id))

if __name__ == '__main__':
    app.run(debug=True)