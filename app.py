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


def get_all_books() -> dict:
    return mongo.db.books.find()

def find_book(book_id) -> dict:
    return mongo.db.books.find_one({"id": int(book_id)})

def delete_book(book_id) -> dict:
    result = mongo.db.books.delete_one({"id": int(book_id)})
    if result.deleted_count:
        return {"Message": "Book deleted successfully!"}
    else:
        return {"Error": "Book not found!"}, 404
    
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
def get_books():
    return jsonify(get_all_books())

@app.route('/books/view', methods=['GET'])
def get_book():
    book_id:int = request.args.get('book_id')
    return jsonify(find_book(book_id))

@app.route('/books/delete', methods=['DELETE'])
def remove_book():
    book_id:int = request.args.get('book_id')
    return jsonify(delete_book(book_id))

if __name__ == '__main__':
    app.run(debug=True)