#!/bin/bash

# Script to inject dummy data into the library management system
# Each curl command sends a POST request to add a book with various attributes
#---------------------------------------------------------------
URL="http://127.0.0.1:5000/books/add" # Adjust the URL as needed
HEADER="Content-Type: application/json" # Adjust the header as needed

# Print a message indicating the start of the process
echo "📚 Adding science books one by one..."

# Each curl command adds a book with various attributes
#---------------------------------------------------------------

# Book 1
curl -X POST $URL -H "$HEADER" -d '{
  "id": 1,
  "title": "A Brief History of Time",
  "author": "Stephen Hawking",
  "year": 1988,
  "isbn": "9780553380163",
  "subject": "Physics",
  "copies_available": 5,
  "publisher": "Bantam Books"
}'

# Book 2
curl -X POST $URL -H "$HEADER" -d '{
  "id": 2,
  "title": "The Selfish Gene",
  "author": "Richard Dawkins",
  "year": 1976,
  "isbn": "9780198788607",
  "subject": "Biology",
  "copies_available": 4,
  "publisher": "Oxford University Press"
}'

# Book 3
curl -X POST $URL -H "$HEADER" -d '{
  "id": 3,
  "title": "Cosmos",
  "author": "Carl Sagan",
  "year": 1980,
  "isbn": "9780345539434",
  "subject": "Astronomy",
  "copies_available": 6,
  "publisher": "Ballantine Books"
}'

# Book 4
curl -X POST $URL -H "$HEADER" -d '{
  "id": 4,
  "title": "The Origin of Species",
  "author": "Charles Darwin",
  "year": 1859,
  "isbn": "9781509827695",
  "subject": "Evolution",
  "copies_available": 3,
  "publisher": "Macmillan Collector’s Library"
}'

# Book 5
curl -X POST $URL -H "$HEADER" -d '{
  "id": 5,
  "title": "The Elegant Universe",
  "author": "Brian Greene",
  "year": 1999,
  "isbn": "9780393338102",
  "subject": "Physics",
  "copies_available": 5,
  "publisher": "W. W. Norton & Company"
}'

# Book 6
curl -X POST $URL -H "$HEADER" -d '{
  "id": 6,
  "title": "Pale Blue Dot",
  "author": "Carl Sagan",
  "year": 1994,
  "isbn": "9780345376596",
  "subject": "Astronomy",
  "copies_available": 4,
  "publisher": "Ballantine Books"
}'

# Book 7
curl -X POST $URL -H "$HEADER" -d '{
  "id": 7,
  "title": "The Double Helix",
  "author": "James D. Watson",
  "year": 1968,
  "isbn": "9780743216302",
  "subject": "Genetics",
  "copies_available": 3,
  "publisher": "Touchstone"
}'

# Book 8
curl -X POST $URL -H "$HEADER" -d '{
  "id": 8,
  "title": "The Structure of Scientific Revolutions",
  "author": "Thomas S. Kuhn",
  "year": 1962,
  "isbn": "9780226458120",
  "subject": "Philosophy of Science",
  "copies_available": 2,
  "publisher": "University of Chicago Press"
}'

# Book 9
curl -X POST $URL -H "$HEADER" -d '{
  "id": 9,
  "title": "Silent Spring",
  "author": "Rachel Carson",
  "year": 1962,
  "isbn": "9780618249060",
  "subject": "Environmental Science",
  "copies_available": 4,
  "publisher": "Mariner Books"
}'

# Book 10
curl -X POST $URL -H "$HEADER" -d '{
  "id": 10,
  "title": "Brief Answers to the Big Questions",
  "author": "Stephen Hawking",
  "year": 2018,
  "isbn": "9781984819192",
  "subject": "Physics",
  "copies_available": 5,
  "publisher": "Bantam"
}'
#---------------------------------------------------------------
# Print a completion message
echo "✅ Done adding all 10 books!"
