# create type for json 
from typing import Any, TypeAlias
from marshmallow import Schema,fields
from datetime import datetime,timedelta
from ..extension import mongo
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash
from .log import setup_logger,log_type
# `jwt_refresh_token_required` was removed from this import because it is deprecated
# in Flask-JWT-Extended version 4.0 and later. The new way to protect an endpoint
# with a refresh token is to use `@jwt_required(refresh=True)`.
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token, get_jwt, set_access_cookies, set_refresh_cookies, unset_jwt_cookies, JWTManager
from flask import render_template,current_app,request,session,jsonify,blueprints,redirect,url_for,make_response
import jwt # type: ignore
import shortuuid

logger = setup_logger(log_type.general)

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

# key type for the token generation
class KeyType(Enum):
    SUPER_KEY = 1
    SECRET_KEY = 2

class Status (Enum):
    Success:str = "Success"
    Failed:str = "Failed"
    Pending:str = "Pending"

JSONType: TypeAlias = dict[str,Any] | list[Any] | None
UserDataType: TypeAlias = int | str | dict[str,Any] | list[Any]

def add_filter(_dict:dict,value:UserDataType,key:str,transform:Any = None) -> UserDataType:
    if value:
        _dict[key] = transform(value) if transform else value
    return _dict

def generate_random_id(length:int,additional:str = '') -> str:
    logger.info("Generating random ID")
    return shortuuid.ShortUUID(alphabet=f'1234567890abcdef{additional}').random(length=length)