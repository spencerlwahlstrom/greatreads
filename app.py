from flask import Flask, render_template, json, redirect, request
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv, find_dotenv

# Load .env and get secrets
load_dotenv(find_dotenv())

host = os.environ.get("340DBHOST")
user = os.environ.get("340DBUSER")
pw = os.environ.get("340DBPW")
db = os.environ.get("340DB")

app = Flask(__name__)

# Assign secrets to app config
app.config["MYSQL_HOST"] = host
app.config["MYSQL_USER"] = user
app.config["MYSQL_PASSWORD"] = pw
app.config["MYSQL_DB"] = db
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

# Routes
@app.route("/")
def root():
    return render_template("layout.html")

@app.route("/books")
def books():
    # temporary books array
    # TODO: populate data from database
    books = []

    books.append({
        "book_id": 1,
        "title": "The Fellowship of the Ring",
        "publisher": "George Allen & Unwin",
        "isbn": 9780007136599,
        "summary": "A meek Hobbit from the Shire and...",
        "published_date": "1954-07-29",
        "msrp": 10.95,
        "average_rating": 4.5
    })

    books.append({
        "book_id": 2,
        "title": "Good Omens: The Nice and...",
        "publisher": "Workman",
        "isbn": 9780060853983,
        "summary": "According to The Nice and...",
        "published_date": "1990-05-10",
        "msrp": 8.99,
        "average_rating": 4.7
    })

    books.append({
        "book_id": 3,
        "title": "Between the Lines",
        "publisher": "Simon Pulse",
        "isbn": 9781451635812,
        "summary": "Delilah, a 15-year-old...",
        "published_date": "2012-06-12",
        "msrp": 8.07,
        "average_rating": 4.3
    })

    books.append({
        "book_id": 4,
        "title": "Harry Potter and the Philosopher's Stone",
        "publisher": "Bloomsbury",
        "isbn": 9780939173341,
        "summary": "Adaptation of the first...",
        "published_date": "1997-06-26",
        "msrp": 7.50,
        "average_rating": 4.8
    })

    return render_template("books.html", books=books)

@app.route("/reviews")
def reviews():
    reviews = []

    reviews.append({
        "review_id": 1,
        "book_id": 1,
        "rating": 5.0,
        "summary": "Was life changing!",
        "user_handle": "user1"
    })

    reviews.append({
        "review_id": 2,
        "book_id": 1,
        "rating": 1.0,
        "summary": "Was horrible I fell asleep!",
        "user_handle": "user2"
    })

    reviews.append({
        "review_id": 3,
        "book_id": 2,
        "rating": 4.6,
        "summary": "I loved it",
        "user_handle": "user3"
    })

    reviews.append({
        "review_id": 4,
        "book_id": 3,
        "rating": 3.0,
        "summary": "I thought it was just meh",
        "user_handle": "user4"
    })

    reviews.append({
        "review_id": 5,
        "book_id": 4,
        "rating": 4.5,
        "summary": "I wanted to love it but almost hated it",
        "user_handle": "user5"
    })

    reviews.append({
        "review_id": 6,
        "book_id": 5,
        "rating": 4.5,
        "summary": "I really liked this one",
        "user_handle": "user6"
    })

    return render_template("reviews.html", reviews= reviews)

@app.route("/genres")
def genres():
    genres = []
    genres.append({
        "genre_id": 1,
        "description": "Fiction",

    })

    genres.append({
        "genre_id": 2,
        "description": "Fantasy",

    })

    genres.append({
        "genre_id": 3,
        "description": "Science Fiction",

    })

    genres.append({
        "genre_id": 4,
        "description": "Humor",

    })

    genres.append({
        "genre_id": 5,
        "description": "Children's",

    })
    genres.append({
        "genre_id": 6,
        "description": "Adventure",

    })
    return render_template("genres.html", genres = genres)

@app.route("/authors")
def authors():
    authors = []
    authors.append({
        "author_id": 1,
        "first_name": "J.R.R.",
        "last_name":  "Tolkien"
        })

    authors.append({
        "author_id": 2,
        "first_name": "Neil",
        "last_name":  "Gaiman"
        })

    authors.append({
        "author_id": 3,
        "first_name": "Terry",
        "last_name":  "Pratchett"
        })
    
    authors.append({
        "author_id": 4,
        "first_name": "Jodi",
        "last_name":  "Picoult"
        })
    
    authors.append({
        "author_id": 5,
        "first_name": "Samantha",
        "last_name":  "Van Leer"
        })

    authors.append({
        "author_id": 6,
        "first_name": "J.K.",
        "last_name":  "Rowling"
        })

    return render_template("authors.html", authors = authors)
    
# Listener
if __name__ == "__main__":
    app.run(port=8337, debug=True)
