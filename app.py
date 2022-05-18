from crypt import methods
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
    return render_template("index.html")

# TODO: delete this route (placeholder for submission Project Step 3)
@app.route("/index.html")
def index():
    return render_template("index.html")

@app.route("/reviews")
def reviews():
    reviews = []

    reviews.append({
        "rating": 5.0,
        "summary": "Was life changing!",
        "user_handle": "user1"
    })

    reviews.append({
        "rating": 1.0,
        "summary": "Was horrible I fell asleep!",
        "user_handle": "user2"
    })

    reviews.append({
        "rating": 4.6,
        "summary": "I loved it",
        "user_handle": "user3"
    })

    reviews.append({
        "rating": 3.0,
        "summary": "I thought it was just meh",
        "user_handle": "user4"
    })

    reviews.append({
        "rating": 4.5,
        "summary": "I wanted to love it but almost hated it",
        "user_handle": "user5"
    })

    reviews.append({
        "rating": 4.5,
        "summary": "I really liked this one",
        "user_handle": "user6"
    })

    return render_template("reviews.html", reviews= reviews)

@app.route("/genres")
def genres():
    genres = []
    genres.append({
        "description": "Fiction",

    })

    genres.append({
        "description": "Fantasy",

    })

    genres.append({
        "description": "Science Fiction",

    })

    genres.append({
        "description": "Humor",

    })

    genres.append({
        "description": "Children's",

    })
    genres.append({
        "description": "Adventure",

    })
    return render_template("genres.html", genres = genres)

@app.route("/authors")
def authors():
    authors = []
    authors.append({
        "first_name": "J.R.R.",
        "last_name":  "Tolkien"
        })

    authors.append({
        "first_name": "Neil",
        "last_name":  "Gaiman"
        })

    authors.append({
        "first_name": "Terry",
        "last_name":  "Pratchett"
        })
    
    authors.append({
        "first_name": "Jodi",
        "last_name":  "Picoult"
        })
    
    authors.append({
        "first_name": "Samantha",
        "last_name":  "Van Leer"
        })

    authors.append({
        "first_name": "J.K.",
        "last_name":  "Rowling"
        })

    return render_template("authors.html", authors = authors)

# BOOKS CRUD
@app.route("/books", methods=["GET", "POST"])
def books():
    # Get all books
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM books;")
        books = cur.fetchall()
        return render_template("books.html", books=books)
    
    # Add a new book
    if request.method == "POST":
        book = request.form
        cur = mysql.connection.cursor()
        query = "INSERT INTO books (title, publisher, isbn, summary, published_date, msrp, average_rating) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        params = [book["title"], book["publisher"], book["isbn"], book["summary"], book["published_date"], book["msrp"], book["average_rating"]]
        cur.execute(query, params)
        mysql.connection.commit()
        return redirect("/books")

@app.route("/books/edit/<book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    # Display book to edit with current attributes
    if request.method == "GET":
        cur = mysql.connection.cursor()
        query = "SELECT * FROM books WHERE book_id = %s;"
        params = [book_id]
        cur.execute(query, params)
        results = cur.fetchall()
        return render_template("books-edit.html", book=results[0])
    
    # Receive data from edit and update database
    if request.method == "POST":
        book = request.form
        cur = mysql.connection.cursor()
        query = "UPDATE books SET title = %s, publisher = %s, isbn = %s, summary = %s, published_date = %s, msrp = %s, average_rating = %s WHERE book_id = %s;"
        params = [book["title"], book["publisher"], book["isbn"], book["summary"], book["published_date"], book["msrp"], book["average_rating"], book["book_id"]]
        cur.execute(query, params)
        mysql.connection.commit()
        return redirect("/books")

@app.route("/books/delete/<book_id>")
def delete_book(book_id):
    cur = mysql.connection.cursor()
    query = "DELETE FROM books WHERE book_id = %s"
    params = [book_id]
    cur.execute(query, params)
    mysql.connection.commit()
    return redirect("/books")

# AUTHORS_BOOKS CRUD
@app.route("/authors-books")
def authors_books():
    # Get all authors_books
    cur = mysql.connection.cursor()
    query = "SELECT b.title AS title, CONCAT(a.first_name, ' ', a.last_name) AS full_name, "\
            "b.book_id, a.author_id FROM authors AS a "\
            "INNER JOIN authors_books AS ab ON a.author_id = ab.author_id "\
            "INNER JOIN books AS b ON b.book_id = ab.book_id;"
    cur.execute(query)
    results = cur.fetchall()
    return render_template("authors-books.html", authors_books=results)

@app.route("/authors-books/edit/<book_id>/<author_id>", methods=["GET", "POST"])
def edit_ab(book_id, author_id):
    # Show edit page for the selected author/book combination
    if request.method == "GET":
        cur = mysql.connection.cursor()
        books_query = "SELECT book_id, title FROM books;"
        cur.execute(books_query)
        books = cur.fetchall()
        
        authors_query = "SELECT author_id, CONCAT(first_name, ' ', last_name) AS full_name FROM authors;"
        cur.execute(authors_query)
        authors = cur.fetchall()

        # have to cast book_id and author_id to integers for comparison in html!
        return render_template("authors-books-edit.html", books=books, authors=authors, book_id=int(book_id), author_id=int(author_id))
    
    # Update database with user's selection, redirect
    if request.method == "POST":
        ab = request.form
        new_book_id = ab["book"]
        new_author_id = ab["author"]

        cur = mysql.connection.cursor()
        query = "UPDATE authors_books SET author_id=%s, book_id=%s WHERE author_id=%s AND book_id=%s;"
        params = [new_author_id, new_book_id, author_id, book_id]
        cur.execute(query, params)
        mysql.connection.commit()

        return redirect("/authors-books")

@app.route("/authors-books/delete/<book_id>/<author_id>")
def delete_ab(book_id, author_id):
    cur = mysql.connection.cursor()
    query = "DELETE FROM authors_books WHERE author_id=%s AND book_id=%s"
    params = [author_id, book_id]
    cur.execute(query, params)
    mysql.connection.commit()
    return redirect("/authors-books")

# Listener
if __name__ == "__main__":
    app.run(port=56879, debug=True)
