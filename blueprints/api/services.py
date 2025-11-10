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

    if "id" not in book:
        logger.info("Generating random ID for new book")
        book:dict = {"id":generate_random_id(10), **book}

    if mongo.db.books.find_one({"id": book["id"]}) or mongo.db.books.find_one({"isbn":book["isbn"]}):
        logger.warning("Book with this ID already exists.")
        raise ValueError("Book with this ID already exists.")

    mongo.db.books.insert_one(book)
    logger.info("Book added successfully!")
    return {"Message": "Book added successfully!", "book_id": book["id"]}

def delete_book_in_db(id:int) -> JSONType:

    logger.info("Deleting book from database")

    if not id:
        logger.warning("Empty ID provided.")
        raise ValueError("Empty Value")

    logger.info("Deleting book from database")
    result = mongo.db.books.delete_one({"id": id})

    if result.deleted_count:
        logger.info("Book deleted successfully!")
        return {"Message": "Book deleted successfully!"}
    else:
        logger.warning("Book not found!")
        return {"Error": "Book not found!"}, 404

def search_books_in_db(query:dict) -> JSONType:

    logger.info("Searching books in database")

    if not query:
        logger.warning("Empty query provided.")
        raise ValueError("Empty Value")

    return mongo.db.books.find(query)

def find_author_in_db(author:str) -> JSONType:

    logger.info("Searching books by author in database")

    if not author:
        logger.warning("Empty author provided.")
        raise ValueError("Empty Value")

    return mongo.db.books.find({"author":author})

def find_subject_in_db(subject:str) -> JSONType:

    logger.info("Searching books by subject in database")

    if not subject:
        logger.warning("Empty subject provided.")
        raise ValueError("Empty Value")

    return mongo.db.books.find({"subject":subject})

def find_all_in_db() -> JSONType:
    logger.info("Finding all books in database")
    return mongo.db.books.find()

def find_id_in_db(id:int) -> JSONType:

    logger.info("Searching books by ID in database")

    if not id:
        logger.warning("Empty ID provided.")
        raise ValueError("Empty Value")

    return mongo.db.books.find_one({"id": id})

def find_isbn_in_db(isbn:str) -> JSONType:

    logger.info("Searching books by ISBN in database")

    if not isbn:
        logger.warning("Empty ISBN provided.")
        raise ValueError("Empty Value")

    return mongo.db.books.find({"isbn":isbn})

def find_publisher_in_db(publisher:str) -> JSONType:

    logger.info("Searching books by publisher in database")

    if not publisher:
        logger.warning("Empty publisher provided.")
        raise ValueError("Empty Value")

    return mongo.db.books.find({"publisher":publisher})

def find_title_in_db(title:str) -> JSONType:

    logger.info("Searching books by title in database")

    if not title:
        logger.warning("Empty title provided.")
        raise ValueError("Empty Value")

    return mongo.db.books.find({"title":title})

def find_year_in_db(year:int) -> JSONType:

    logger.info("Searching books by year in database")

    if not year:
        logger.warning("Empty year provided.")
        raise ValueError("Empty Value")

    return mongo.db.books.find({"year":year})

def find_copies_in_db(copies:int) -> JSONType:

    logger.info("Searching books by copies available in database")

    if not copies:
        logger.warning("Empty copies provided.")
        raise ValueError("Empty Value")

    return mongo.db.books.find({"copies_available":copies})

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
    return {"total_copies": total_copies}

def count_copies_by_subject_in_db() -> JSONType:

    logger.info("Counting total copies by subject in database")

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




