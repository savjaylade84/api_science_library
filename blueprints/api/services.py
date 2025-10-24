from flask import jsonify
from marshmallow import Schema, fields
from typing import Any,TypeAlias
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from extension import mongo
import shortuuid
import datetime
import jwt
import json


# create type for json 
JSONType: TypeAlias = dict[str,Any] | list[Any] | None


# this will make sure the user inputs are validated
class BookSchema(Schema):
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    year = fields.Int(required=True)
    isbn = fields.Str(required=True)
    subject = fields.Str(required=True)
    copies_available = fields.Int(required=True)
    publisher = fields.Str(required=True)

def append_book_in_db(book:dict) -> JSONType:
    
    if not book:
        raise ValueError("Empty Value")

    if "id" not in book:
        book = {"id":shortuuid.ShortUUID(alphabet='1234567890abcdef').random(length=10), **book}

    if mongo.db.books.find_one({"id": book["id"]}) or mongo.db.books.find_one({"isbn":book["isbn"]}):
        raise ValueError("Book with this ID already exists.")

    mongo.db.books.insert_one(book)
    return {"Message": "Book added successfully!", "book_id": book["id"]}

def delete_book_in_db(id:int) -> JSONType:

    if not id:
        raise ValueError("Empty Value")

    result = mongo.db.books.delete_one({"id": id})
    if result.deleted_count:
        return {"Message": "Book deleted successfully!"}
    else:
        return {"Error": "Book not found!"}, 404

def search_books_in_db(query:dict) -> JSONType:

    if not query:
        raise ValueError("Empty Value")

    return mongo.db.books.find(query)

def find_author_in_db(author:str) -> JSONType:

    if not author:
        raise ValueError("Empty Value")

    return mongo.db.books.find({"author":author})

def find_subject_in_db(subject:str) -> JSONType:

    if not subject:
        raise ValueError("Empty Value")

    return mongo.db.books.find({"subject":subject})

def find_all_in_db() -> JSONType:

    return mongo.db.books.find()

def find_id_in_db(id:int) -> JSONType:

    if not id:
        raise ValueError("Empty Value")

    return mongo.db.books.find_one({"id": id})

def find_isbn_in_db(isbn:str) -> JSONType:

    if not isbn:
        raise ValueError("Empty Value")

    return mongo.db.books.find({"isbn":isbn})

def find_publisher_in_db(publisher:str) -> JSONType:

    if not publisher:
        raise ValueError("Empty Value")

    return mongo.db.books.find({"publisher":publisher})

def find_title_in_db(title:str) -> JSONType:

    if not title:
        raise ValueError("Empty Value")

    return mongo.db.books.find({"title":title})

def find_year_in_db(year:int) -> JSONType:

    if not year:
        raise ValueError("Empty Value")

    return mongo.db.books.find({"year":year})

def find_copies_in_db(copies:int) -> JSONType:

    if not copies:
        raise ValueError("Empty Value")

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

def signup(user: dict) -> JSONType:

    if not user:
        raise ValueError("Empty Value")

    return jsonify({"username":user['username'],"password":user['password']})


def sigin(user: dict) -> JSONType:

    if not user:
        raise ValueError("Empty Value")

    return jsonify({"username":user['username'],"password":user['password']})
