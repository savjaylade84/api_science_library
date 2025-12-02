from flask import jsonify
from ...extension import mongo
from .. import *


# load the logging instance
logger = setup_logger(log_type.api)


# append book to db
def append_book_in_db(book:dict) -> JSONType:

    logger.info("Appending book to database")

    if not book:
        logger.warning("Empty book data provided.")
        raise ValueError("Empty Value")

    # check if id is existed if not then the data is for new book information
    # then generate id for the new book
    if "id" not in book:
        logger.info("Generating random ID for new book")
        book:dict = {"id":generate_random_id(10), **book}

    if mongo.db.books.find_one({"id": book["id"]}) or mongo.db.books.find_one({"isbn":book["isbn"]}):
        logger.warning("Book with this ID already exists.")
        raise ValueError("Book with this ID already exists.")

    mongo.db.books.insert_one(book)
    logger.info("Book added successfully!")
    return {"Message": "Book added successfully!","Status":Status.Success, "book_id": book["id"]}

def delete_book_in_db(id:int) -> JSONType:

    logger.info("Deleting book from database")

    if not id:
        logger.warning("Empty ID provided.")
        raise ValueError("Empty Value")

    logger.info("Deleting book from database")
    result = mongo.db.books.delete_one({"id": id})

    if result.deleted_count:
        logger.info("Book deleted successfully!")
        return {"Message": "Book deleted successfully!","Status":Status.Success}
    else:
        logger.warning("Book not found!")
        return {"Message": "Book not found!","Status":Status.Failure}, 404

def search_books_in_db(query:dict) -> JSONType:

    logger.info("Searching books in database")

    if not query:
        logger.warning("Empty query provided.")
        raise ValueError("Empty Value")

    logger.info("Books found!")
    return {"Message":"Books found!","Status":Status.Success,"Data": mongo.db.books.find(query)}

def find_author_in_db(author:str) -> JSONType:

    logger.info("Searching books by author in database")

    if not author:
        logger.warning("Empty author provided.")
        raise ValueError("Empty Value")

    logger.info(f"Author: {author} Books found!")
    return {"Message":f" Author:{author} Books found!","Status":Status.Success,"Data": mongo.db.books.find({"author":author})}

def find_subject_in_db(subject:str) -> JSONType:

    logger.info("Searching books by subject in database")

    if not subject:
        logger.warning("Empty subject provided.")
        raise ValueError("Empty Value")

    logger.info(f"Subject: {subject} Books found!")
    return {"Message":f" Subject:{subject} Books found!","Status":Status.Success,"Data": mongo.db.books.find({"subject":subject})}

def find_all_in_db() -> JSONType:
    logger.info(f"Finding all books in database")
    return {"Message":"All books found!","Status":Status.Success,"Data": mongo.db.books.find()}

def find_id_in_db(id:int) -> JSONType:

    logger.info("Searching books by ID in database")

    if not id:
        logger.warning("Empty ID provided.")
        raise ValueError("Empty Value")

    logger.info(f"ID: {id} Book found!")
    return {"Message": f"ID:{id}Book found!","Status":Status.Success,"Data": mongo.db.books.find_one({"id": id})}

def find_isbn_in_db(isbn:str) -> JSONType:

    logger.info("Searching books by ISBN in database")

    if not isbn:
        logger.warning("Empty ISBN provided.")
        raise ValueError("Empty Value")

    logger.info(f"ISBN: {isbn} Books found!")
    return {"Message": f"ISBN:{isbn} Books found!","Status":Status.Success,"Data": mongo.db.books.find({"isbn":isbn})}

def find_publisher_in_db(publisher:str) -> JSONType:

    logger.info("Searching books by publisher in database")

    if not publisher:
        logger.warning("Empty publisher provided.")
        raise ValueError("Empty Value")

    logger.info(f"Publisher: {publisher} Books found!")
    return {"Message": f"Publisher:{publisher} Books found!","Status":Status.Success,"Data": mongo.db.books.find({"publisher":publisher})}

def find_title_in_db(title:str) -> JSONType:

    logger.info("Searching books by title in database")

    if not title:
        logger.warning("Empty title provided.")
        raise ValueError("Empty Value")

    logger.info(f"Title: {title} Books found!")
    return {"Message": f"Title:{title} Books found!","Status":Status.Success,"Data": mongo.db.books.find({"title":title})}

def find_year_in_db(year:int) -> JSONType:

    logger.info("Searching books by year in database")

    if not year:
        logger.warning("Empty year provided.")
        raise ValueError("Empty Value")

    logger.info(f"Year: {year} Books found!")
    return {"Message": f"Year:{year} Books found!","Status":Status.Success,"Data":mongo.db.books.find({"year":year})}

def find_copies_in_db(copies:int) -> JSONType:

    logger.info("Searching books by copies available in database")

    if not copies:
        logger.warning("Empty copies provided.")
        raise ValueError("Empty Value")

    logger.info(f"Copies: {copies} Books found!")
    return {"Message": f"Copies:{copies} Books found!","Status":Status.Success,"Data":mongo.db.books.find({"copies_available":copies})}

def count_copies_in_db() -> JSONType:

    logger.info("Counting total copies in database")

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
    logger.info(f"Total copies counted: {total_copies}")
    return {"Message": "Total copies counted","Status":Status.Success,"Data":{"total_copies": total_copies}}

def count_copies_by_subject_in_db() -> JSONType:

    logger.info("Counting total copies by subject in database")

    pipeline = [
        # The $group stage groups documents by the 'subject' field.
        {
            "$group": {
                "_id": "$subject",
                # The $sum accumulator was changed from "$subject" (which is a string and incorrect)
                # to "$copies_available" to correctly sum the number of available copies
                # for each subject group.
                "total_copies": {"$sum": "$copies_available"}
            }
        }
    ]
    result = list(mongo.db.books.aggregate(pipeline))
    total = []
    for item in result:
        # This line was removed as it was incorrectly incrementing the already summed total.
        # The aggregation pipeline now provides the correct count directly.
        total.append({item['_id']:item['total_copies']})
        
    logger.info("Total copies by subject counted")
    return {"Message": "Total copies by subject counted","Status":Status.Success,"Data": total}

# --------------------------------------------------------------

def find_user_in_db(user:dict) -> JSONType:

    logger.info("Finding user in database")
    if not user:
        logger.warning("Empty user data provided.")
        raise ValueError("Empty Value")
    
    if mongo.db.user.find_one(user) is None:
        logger.warning("User information not found")
        return {"Message": "User information not found","Status":Status.Failed}
    
    logger.info("User information found")
    return {"Message": "User information found","Status":Status.Success,"Data": mongo.db.user.find_one(user)}

def verify_user_in_db(user:dict) -> JSONType:
    
    if not user['username'] or not user['password']:
        logger.warning('Empty Username or Password')
        raise ValueError('Empty Username or Password')
    
    search_result = mongo.db.users.find_one(user)
    
    # This function was refactored to return a Python dictionary instead of a Flask Response object.
    # This improves separation of concerns, making the service layer more reusable and easier to test
    # without needing a Flask application context. The route handler is now responsible for jsonify-ing the response.
    if not search_result:
        return {"Message":"Failed to find the specific user","Status":Status.Failed}
    else:
        # The duplicate return statement was removed.
        return {"Message":"Successfully find the user","Status":Status.Success,"Data":search_result}
    
def register_user_in_db(user:dict) -> JSONType:
    
    if not user:
        logger.warning('Empty User Information')
        raise ValueError('Empty User Information')
    
    search_result = mongo.db.user.find_one(user)
    
    if not search_result:
        # If the user doesn't exist, insert them into the database.
        mongo.db.user.insert_one(user)
        # Return a success message. This was also changed from a Flask Response to a dictionary.
        return {"Message":"User registered successfully","Status":Status.Success}
    else: 
        logger.warning('Already Existed User')
        # Return a failure message if the user already exists.
        return {"Message":"There's already Existed User","Status":Status.Failed}
    
#------------------------------------------------------------------------------------------

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
    
def generate_payload(user:dict,purpose: KeyType,isNewUser:bool=False) -> JSONType:

    payload:dict = {
        "user_id": user['user_id'],
        "username": user['username'],
        "super_key": None
    }

    if not user:
        logger.warning('Empty user provided')
        raise ValueError('Empty User Provided')
    
    if not purpose:
        logger.warning('Empty purpose provided')
        raise ValueError('Empty Purpose')
    
    
    if isNewUser is False:
        payload['super_key'] = user['tokens']['super_key']
    else:
        payload["super_key"] = generate_random_id(25,"#@&%*")

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
    if find_user_in_db(user)['Status'] is Status.Success:
        logger.info("User found in database")
        acc = find_user_in_db(user)['Data']
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

def decode_token() -> JSONType:
    pass

def verify_token(token:str) -> JSONType:
    pass 