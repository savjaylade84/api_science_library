# generate random id
from datetime import datetime
from enum import Enum
from ...extension import mongo
from .. import *
from flask import jsonify


logger = setup_logger(log_type.web)

# key type for the token generation
class KeyType(Enum):
    SUPER_KEY = 1
    SECRET_KEY = 2
    


# generate hash key
def generate_hash_key(payload:dict,super_key:str) -> str:

    logger.info("Generating hash key")

    ALGORITHM:str = 'HS256'

    if not payload:
        logger.warning("Empty payload provided.")
        raise ValueError('Empty payload, can\'t perform jwt')
    
    if not super_key:
        logger.warning("Empty super key provided.")
        raise ValueError('Empty super key, can\'t perform jwt')

    return jwt.encode(payload,super_key,algorithm=ALGORITHM)

def find_user_in_db(user:dict) -> JSONType:

    logger.info("Finding user in database")
    if not user:
        logger.warning("Empty user data provided.")
        raise ValueError("Empty Value")
    return mongo.db.user.find_one(user)



def generate_payload(user:dict,purpose: KeyType,isNewUser:bool=False) -> JSONType:

    if not user:
        logger.warning('Empty user provided')
        raise ValueError('Empty User Provided')
    
    if not purpose:
        logger.warning('Empty purpose provided')
        raise ValueError('Empty Purpose')
    
    if isNewUser is False:
        payload:dict = {
                "user_id": user['user_id'],
                "username": user['username'],
                "super_key": user['tokens']['super_key']
        }
    else:
        payload = {
                "user_id": user['user_id'],
                "username": user['username'],
                "super_key": generate_random_id(25,"#@&%*")
        }

    if purpose is KeyType.SECRET_KEY:
        today: datetime = datetime.now() + datetime.timedelta(hours=3) 
        payload["exp"] =  today

    return payload


# generate token based on what type of token
def generate_token(user:dict,purpose: KeyType) -> str:

    logger.info("Generating token") 

    payload:dict = {}
    acc:dict = {}

    if not user:
        logger.warning("Empty user provided.")
        raise ValueError("Empty user")
    
    if not purpose:
        logger.warning("Empty purpose provided.")
        raise ValueError("Empty purpose")
    
    # check if there's a user with the same information
    # then act accordingly
    if find_user_in_db(user):
        logger.info("User found in database")
        acc = find_user_in_db(user)
        payload = generate_payload(user=acc,purpose=KeyType.SUPER_KEY,isNewUser=False)
    else:
        if purpose is KeyType.SUPER_KEY:
            payload = generate_payload(user=user,purpose=KeyType.SUPER_KEY,isNewUser=True)
        else:
            payload = generate_payload(user=user,purpose=KeyType.SECRET_KEY,isNewUser=True)

    try:
        if payload:
            logger.info("Generating hash key")
            return generate_hash_key(payload=payload,super_key = payload['super_key'])
    except Exception as e:
        logger.error("Failed to generate hash key or token")
        raise e("Failed to generate hash key or token")

# register account in user collection in science library db
def register_acc_in_db(user: dict) -> JSONType:

    logger.info("Registering account in database")

    if not user:
        logger.warning("Empty user data provided.")
        raise ValueError("Empty Value")

    if mongo.db.user.find_one({"use_id":user['user_id']}) or mongo.db.user.find_one({"username":user['username']}):
        logger.warning("User account already exists.")
        raise ValueError('User Account Already Existed')

    if "user_id" not in user:
        logger.info("Generating user_id")
        user:dict = {"user_id":generate_random_id(10),**user}

    if "tokens" not in user:
        logger.info("Generating tokens")
        user:dict = {"tokens":
                               {
                                   "super_key":generate_token(user=user,purpose=KeyType.SUPER_KEY),
                                   "secret_keys": []                   
                                },**user}
        
    user['password'] = generate_password_hash(user['password'])
    #access_token = create_access_token(identity=user['username'])
    #user['access_token'] = access_token
    mongo.db.user.insert_one(user)
    logger.info("Account registered successfully!")

    return jsonify({"Message":"Account is Successfully Registered"})

# find user by username and password
def find_user_by_username_and_password(username:str,password:str) -> bool:

    logger.info("Finding user by username and password")

    if not username or not password:
        logger.warning("Empty username or password provided.")
        raise ValueError("Empty Value")
    
    user:dict = mongo.db.user.find_one({"username":username})

    if not user:
        logger.warning("User not found.")
        raise ValueError("User Not Found")

    if check_password_hash(user['password'],password):
        logger.info("User found and password matched.")
        return True
    
    return False

# login user and return username and password
def verify_user(user: dict) -> bool:

    logger.info("Signing in user")

    if not user:
        logger.warning("Empty user data provided.")
        raise ValueError("Empty Value")
    
    if find_user_by_username_and_password(username=user['username'], password=user['password']):
        return True

    return False