from flask_pymongo import PyMongo
from flask import Flask, render_template,jsonify,request
from marshmallow import Schema, fields,ValidationError
import json

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/science_library"
mongo = PyMongo(app)

# this will make sure the user inputs are validated
class BookSchema(Schema):
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    subject = fields.Str(required=True)
    year = fields.Int(required=True)
    isbn = fields.Str(required=True)


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



def search_books_in_db(key:str, value) -> dict:
    return mongo.db.books.find({key: value})

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
    id:int = int(request.args.get('id'))
    title:str = request.args.get('title')
    author:str = request.args.get('author')
    subject:str = request.args.get('subject')
    publisher:str = request.args.get('publisher')
    isbn:str = request.args.get('isbn')

    query:dict = {}

    #check which parameters are provided and build the query accordingly
    if not id is None:
        query["id"] = id
    if not title is None:
        query["title"] = title
    if not author is None:
        query["author"] = author
    if not subject is None:
        query["subject"] = subject
    if not publisher is None:
        query["publisher"] = publisher
    if not isbn is None:
        query["isbn"] = isbn

    return jsonify(mongo.db.books.find(query))


@app.route('/books/view', methods=['GET'])
def find_book():
    book_id:int = request.args.get('id')
    return jsonify(find_book_in_db(book_id))

@app.route('/books/delete', methods=['DELETE'])
def remove_book():
    id:int = request.args.get('id')
    return jsonify(delete_book_in_db(id))

if __name__ == '__main__':
    app.run(debug=True)