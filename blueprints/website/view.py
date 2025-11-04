from flask import render_template,current_app
from . import *
import json

# Home route for the website
@library_wb_bp.route('/',methods=['GET'])
@library_wb_bp.route('/home',methods=['GET'])
def index():

    # Fetch all books from the Science Library API
    with current_app.test_client() as client:
        response = client.get('/api/v1/books/filter/view_all')

        # Check if the request was successful
        if response.status_code == 200:
            books = json.loads(response.data)
        else:
            books = []

    return render_template('index.html', books = books)