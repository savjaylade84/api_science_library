
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

### 📚 Books Management

| Method | Endpoint | Description | Request Body | Response | Status |
|--------|-----------|-------------|--------------|----------|----------|
| `GET` | `/books/view_all` | Get all books | None | `[{book1}, {book2}, ...]` | ✅ Done |
| `GET` | `/books/view?book_id<id>` | Get book by ID | None | `{book_data}` | ✅ Done |
| `POST` | `/books/add` | Add new book | `{"title": "Book", "author": "Author", "year": 2023}` | `{"message": "Book added", "id": "123"}` | ✅ Done |
| `PUT` | `/books/update?book_id=<id>` | Update book | `{"title": "New Title"}` | `{"message": "Book updated"}` | 🚧 In Progress |
| `DELETE` | `/books/delete?book_id=<id>` | Delete book | None | `{"message": "Book deleted"}` | ✅ Done |

### 🔍 Search & Filter

| Method | Endpoint | Description | Parameters | Response | Status |
|--------|-----------|-------------|------------|----------|----------|
| `GET` | `/books/search` | Search books | `?author=name&subject=physics` | `[{matching_books}]` | ✅ Done |
| `GET` | `/books/author` | Get books by author | `?author=name` | `[{author_books}]` | ✅ Done |
| `GET` | `/books/subject` | Get books by subject | `?subject=name` | `[{subject_books}]` | ✅ Done |

### 📊 Statistics

| Method | Endpoint | Description | Parameters | Response | Status |
|--------|-----------|-------------|------------|----------|----------|
| `GET` | `/stats/books-count` | Get total books count | None | `{"total_books": 150}` | 🚧 In Progress |
| `GET` | `/stats/books-by-subject` | Get books count by subject | None | `{"Physics": 50, "Chemistry": 30}` | 🚧 In Progress |
| `GET` | `/stats/authors-count` | Get unique authors count | None | `{"total_authors": 45}` | 🚧 In Progress |
| `GET` | `/stats/publication-years` | Get books by publication year | None | `{"2020": 10, "2021": 15}` | 🚧 In Progress |

## 📋 Example Requests

### Add a New Book

```bash
bash curl -X POST http://127.0.0.1:5000/books/add \
  -H "Content-Type: application/json" \
  -d '{
          "id": 1,
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
        "id": 1,
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
