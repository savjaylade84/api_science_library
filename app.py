from flask import Flask, render_template,jsonify,request
import json

app = Flask(__name__)

def get_all_books() -> dict:
    try:
        with open('books.json', 'r') as file:
            books:dict = json.load(file)
            return books
    except FileNotFoundError:
        return {"Error":"File not found!"}

def find_book(book_id) -> dict:
    books = get_all_books()
    for book in books.get("science_books", []):
        if int(book.get("id")) == int(book_id):
            return book
    return {"Error": "Book not found!"}

def delete_book(book_id) -> dict:
    books = get_all_books()
    for i, book in enumerate(books.get("science_books", [])):
        if int(book.get("id")) == int(book_id):
            del books["science_books"][i]
            with open('books.json', 'w') as file:
                json.dump(books, file, indent=4)
            return {"Message": "Book deleted successfully!"}
    return {"Error": "Book not found!"}
    

@app.route('/books/view_all', methods=['GET'])
def get_books():
    return jsonify(get_all_books())

@app.route('/books/view/all', methods=['GET'])
def get_book():
    book_id:int = request.args.get('book_id')
    return jsonify(find_book(book_id))

@app.route('/books/delete', methods=['DELETE'])
def remove_book():
    book_id:int = request.args.get('book_id')
    return jsonify(delete_book(book_id))

if __name__ == '__main__':
    app.run(debug=True)