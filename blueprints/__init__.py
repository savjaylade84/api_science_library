# create type for json 
from typing import Any, TypeAlias
from marshmallow import Schema,fields
from ..extension import mongo
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash
from .log import setup_logger,log_type
import jwt
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

JSONType: TypeAlias = dict[str,Any] | list[Any] | None

def generate_random_id(length:int,additional:str = '') -> str:
    logger.info("Generating random ID")
    return shortuuid.ShortUUID(alphabet=f'1234567890abcdef{additional}').random(length=length)