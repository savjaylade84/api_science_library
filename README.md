
# 🧪 Science Library API (Flask) - Under-Developement

A simple and lightweight **Flask RESTful API** for managing a **science library**, including books.  
Built with Python and MongoDB, designed for learning clean, modular API development.

---

## 🚀 Features

- 📚 **CRUD Operations** - Create, Read, Update, Delete books
- 🧠 Categorize materials by scientific fields (Physics, Chemistry, Biology, etc.)  
- 🔍 Search by title, author, or topic  
- ⚡ Lightweight, modular, and easy to extend  
- 🗄️ **MongoDB** - NoSQL database for flexible data storage
- 🔄 **RESTful** - Standard HTTP methods and JSON responses

---

### 🏗️ Tech Stack

| Layer | Technology |
|-------|-------------|
| Language | Python 3.10+ |
| Framework | Flask |
| Database | MongoDB |
| API Type | RESTful |
| Data Format | JSON |
| ODM | PyMongo |

---

## 🛠️ API Endpoints

### 📚 Books Manage

| Method | Endpoint | Description | Request Body | Response | Status |
|--------|-----------|-------------|--------------|----------|----------|
| `POST` | `/api/v1/books/manage/add` | Add new book | `{"id": 1,"title": "A Brief History of Time","author": "Stephen Hawking","year": 1988,"isbn": "9780553380163","subject": "Physics","copies_available": 5,"publisher": "Bantam Books"}` | `{"message": "Book added", "id": "123"}` | ✅ Done |
| `PUT` | `/api/v1/books/manage/update?id=<id>` | Update book | `{"title": "New Title"}` | `{"message": "Book updated"}` | 🚧 In Progress |
| `DELETE` | `/api/v1/books/manage/delete?book_id=<id>` | Delete book | None | `{"message": "Book deleted"}` | ✅ Done |

### 🔍 Books Search & Filter

| Method | Endpoint | Description | Parameters | Response | Status |
|--------|-----------|-------------|------------|----------|----------|
| `GET` | `/api/v1/books/filter/view_all` | Get all books | None | `[{book1}, {book2}, ...]` | ✅ Done |
| `GET` | `/api/v1/books/filter/search` | Search books | `?author=name&subject=physics` | `[{matching_books}]` | ✅ Done |
| `GET` | `/api/v1/books/filter/id/<id>` | Get book by ID | `/<id>` | `{id_book}` | ✅ Done |
| `GET` | `/api/v1/books/filter/author/<author>` | Get books by author | `/<author>` | `[{author_books}]` | ✅ Done |
| `GET` | `/api/v1/books/filter/subject/<subject>` | Get books by subject | `/<subject>` | `[{subject_books}]` | ✅ Done |
| `GET` | `/api/v1/books/filter/isbn/<isbn>` | Get books by isbn | `/<isbn>` | `[{isbn_books}]` | ✅ Done |
| `GET` | `/api/v1/books/filter/publisher/<publisher>` | Get books by publisher | `/<publisher>` | `[{publisher_books}]` | ✅ Done |
| `GET` | `/api/v1/books/filter/title/<titler>` | Get books by title | `/<title>` | `[{title_books}]` | ✅ Done |
| `GET` | `/api/v1/books/filter/year/<year>` | Get books by year | `/<year>` | `[{year_books}]` | ✅ Done |
| `GET` | `/api/v1/books/filter/copies/<copies>` | Get books by no. of copies | `/<copies>` | `[{number_copies_books}]` | ✅ Done |

### 📊 Books Statistics

| Method | Endpoint | Description | Parameters | Response | Status |
|--------|-----------|-------------|------------|----------|----------|
| `GET` | `/api/v1/books/stats/total-copies` | Get total books count | None | `{"total_books": 150}` | ✅ Done |
| `GET` | `/api/v1/books/stats/total-copies-by-subject` | Get books count by subject | None | `{"Physics": 50, "Chemistry": 30}` | ✅ Done |

### 📝 Signup and Signin

| Method | Endpoint | Description | Parameters | Response | Status |
|--------|-----------|-------------|------------|----------|----------|
|`GET`| `/api/v1/books/user/signup` | register a new account | `?username=<username>&passsword=<password>` | `{"status":"successfully register"}` | 🚧 In Progress |
|`POST`| `/api/v1/books/user/signin` | signin account | `?username=<username>&passsword=<password>` | `{"status":"successfully signin"}` | 🚧 In Progress |

### User Account Progress Table (progress in the table will update,remove, or added)

| Functionality | Description | Progress |
|--------|-----------|-------------|
| generate secret key | generate secret key for the token | 🚧 In Progress |
| generate super key | generate super key for the token | 🚧 In Progress |
| register new account | create new account | 🚧 In Progress |
| sigin account | sigin account | 🚧 In Progress |

## 📋 Example Requests

## Website for viewing data

` http://127.0.0.1:5000/home ` or ` http://127.0.0.1:5000/ `

### Add a New Book

```bash
bash curl -X POST http://127.0.0.1:5000/api/v1/books/add \
  -H "Content-Type: application/json" \
  -d '{
          "title": "A Brief History of Time",
          "author": "Stephen Hawking",
          "year": 1988,
          "isbn": "9780553380163",
          "subject": "Physics",
          "copies_available": 5,
          "publisher": "Bantam Books"
  }'
```

### 📊 Database Schema

### Books Collection

```json
{
    "science_library": [
        {
        "id": "<generated id>",
        "title": "A Brief History of Time",
        "author": "Stephen Hawking",
        "year": 1988,
        "isbn": "9780553380163",
        "subject": "Physics",
        "copies_available": 5,
        "publisher": "Bantam Books"
        }
    ]
}
```

### User Account

```json
{
    "user":[
      {
        "id": "<generated id>",
        "username": "user123",
        "password": "<encrypted password>",
        "fullname": "Tom B. Green",
        "first_name": "Tom",
        "middle_name": "Barnacle",
        "last_name": "Green",
        "tokens": {
                "super_key":"<generated token>",
                "secret_keys": {
                        "name": "key",
                        "key": "<generated key>",
                        "exp": "<generated expiration date>"
                }
         }

      }
    ]
}
```

### Clone the repository

`git clone https://github.com/yourusername/science-library-api.git
cd science-library-api`

### Create a virtual environment

`python -m venv venv`

### Activate the environment

### Windows

`venv\Scripts\activate`

### macOS/Linux

`source venv/bin/activate`

### Install dependencies

`pip install -r requirements.txt`

### Copy example environment file

`cp .env.example .env`

### Configure your MongoDB connection in .env

`MONGODB_URI = mongodb://localhost:27017/science_library`

### Start MongoDB service (if running locally)

`sudo systemctl start mongod  # Linux`

### or

### macOS

`brew services start mongodb/brew/mongodb-community`  

### Run Flask app

`python src/app.py`

### Ubuntu/Debian

`sudo apt-get install mongodb`

### macOS with Homebrew

`brew tap mongodb/brew`
`brew install mongodb-community`

### Windows - Download from <https://www.mongodb.com/try/download/community>

### Linux (Systemd)

`sudo systemctl start mongod`
`sudo systemctl enable mongod`

### macOS (Unix)

`brew services start mongodb/brew/mongodb-community`

### Windows (Run as Administrator)

`net start MongoDB`

### Connect to MongoDB shell

`mongosh`

### Check databases

`show dbs`

### Use your database

`use science_library`

### Check collections

`show collections`
