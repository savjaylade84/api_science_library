# 🧪 Science Library API (Flask)

A simple and lightweight **Flask RESTful API** for managing a **science library**, including books.  
Built with Python and designed for learning clean, modular API development.

---

## 🚀 Features

- 📚 Manage books
- 👩‍🔬 Add and update researcher profiles  
- 🧠 Categorize materials by scientific fields (Physics, Chemistry, Biology, etc.)  
- 🔍 Search by title, author, or topic  
- ⚡ Lightweight, modular, and easy to extend  

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-------------|
| Language | Python 3.10+ |
| Framework | Flask |
| Database | JSON |
| API Type | RESTful |
| Data Format | JSON |


## ⚙️ Installation

### Prerequisites
- Python 3.10 or newer  
- Git

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/science-library-api.git

cd science-library-api

# Create a virtual environment
python -m venv venv

# Activate the environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy example environment file
cp .env.example .env

# Run Flask app
python src/app.py