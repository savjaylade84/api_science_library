from flask import jsonify
from marshmallow import Schema, fields
from typing import Any,TypeAlias
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from extension import mongo
from dotenv import load_dotenv
from enum import Enum
import datetime
import shortuuid
import jwt
import os
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

# this will create a force format for the account, the id and super key will
# automatically generate
class AccountSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    fullname = fields.Str(required=True)
    first_name = fields.Str(required=True)
    middle_name = fields.Str(required=True)
    last_name = fields.Str(required=True)



class KeyType(Enum):
    SUPER_KEY = 1
    SECRET_KEY = 2

def generate_random_id(length:int,additional:str = '') -> str:
    return shortuuid.ShortUUID(alphabet=f'1234567890abcdef{additional}').random(length=length)

def append_book_in_db(book:dict) -> JSONType:
    
    if not book:
        raise ValueError("Empty Value")

    if "id" not in book:
        book:dict = {"id":generate_random_id(10), **book}

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

# generate hash key
def generate_hash_key(payload:dict,super_key:str) -> str:
    ALGORITHM:str = 'HS256'

    if not payload:
        raise ValueError('Empty payload, can\'t perform jwt')
    
    if not super_key:
        raise ValueError('Empty super key, can\'t perform jwt')

    return jwt.encode(payload,super_key,algorithm=ALGORITHM)

# generate token based on what type of token
def generate_token(user:dict,purpose: KeyType) -> str:

    payload:dict = {}
    acc:dict = {}

    if not user:
        raise ValueError("Empty user")
    
    if not purpose:
        raise ValueError("Empty purpose")
    
    # check if there's a user with the same information
    # then act accordingly 
    if mongo.db.user.find_one(user):
        acc = mongo.db.user.find_one(payload)
        payload = {
            "user_id": acc['user_id'],
            "username": acc['username'],
            "super_key": acc['tokens']['super_key']
        }
    else:
        payload = {
                "user_id": user['user_id'],
                "username": user['username'],
                "super_key": generate_random_id(25,"#@&%*")
        }

    #create a expiration key if the token is a secret key
    if purpose is KeyType.SECRET_KEY:
        today: datetime = datetime.datetime.now() + datetime.timedelta(hours=3) 
        payload["exp"] =  today

    try:
        if payload:
            return generate_hash_key(payload=payload,super_key = payload['super_key'])
    except Exception as e:
        raise e("Failed to generate hash key or token")

def register_acc_in_db(user: dict) -> JSONType:

    if not user:
        raise ValueError("Empty Value")

    if mongo.db.user.find_one({"use_id":user['user_id']}) or mongo.db.user.find_one({"username":user['username']}):
        raise ValueError('User Account Already Existed')

    if "user_id" not in user:
        user:dict = {"user_id":generate_random_id(10),**user}

    if "tokens" not in user:
        user:dict = {"tokens":
                               {
                                   "super_key":generate_token(user=user,purpose=KeyType.SUPER_KEY),
                                   "secret_keys": []                   
                                },**user}

    return jsonify({"Message":"Account is Successfully Registered"})


def sigin(user: dict) -> JSONType:

    if not user:
        raise ValueError("Empty Value")

    return jsonify({"username":user['username'],"password":user['password']})
