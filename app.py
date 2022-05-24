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

# Reviews CRUD
@app.route("/reviews", methods=["GET", "POST"])
def reviews():
    cur = mysql.connection.cursor()
    if request.method == "GET":
        cur.execute("SELECT r.review_id, r.book_id, b.title, r.rating, r.summary, r.user_handle FROM reviews r INNER JOIN books b ON r.book_id = b.book_id;")
        reviews = cur.fetchall()
        cur.execute("SELECT * FROM books;")
        books = cur.fetchall()
        return render_template("reviews.html", reviews= reviews, books = books)

    if request.method == "POST":
        review = request.form
        query = "INSERT INTO reviews (book_id, rating, summary, user_handle) VALUES (%s, %s, %s, %s);"
        params = [review["book"], review["rating"], review["summary"], review["user_handle"]]
        cur.execute(query, params)
        mysql.connection.commit()
        return redirect("/reviews")

@app.route("/reviews/edit/<review_id>", methods=["GET", "POST"])
def edit_review(review_id):
    if request.method == "GET":
        cur = mysql.connection.cursor()
        query = "SELECT * FROM reviews WHERE review_id = %s;"
        params = [review_id]
        cur.execute(query, params)
        results = cur.fetchall()
        return render_template("reviews-edit.html", review=results[0])
    
    if request.method == "POST":
        review = request.form
        cur = mysql.connection.cursor()
        query = "UPDATE reviews SET rating= %s, summary= %s, user_handle=%s WHERE review_id = %s;"
        params = [review["rating"], review["summary"], review["user_handle"], review["review_id"]]
        cur.execute(query, params)
        mysql.connection.commit()
        return redirect("/reviews")

@app.route("/reviews/delete/<review_id>")
def delete_review(review_id):
    cur = mysql.connection.cursor()
    query = "DELETE FROM reviews WHERE review_id = %s;"
    params = [review_id]
    cur.execute(query, params)
    mysql.connection.commit()
    return redirect("/reviews")
    
# Genres CRUD and books_genres CRUD
@app.route("/genres", methods=["GET", "POST"])
def genres():
    cur = mysql.connection.cursor()
    if request.method == "GET":
        cur.execute("SELECT * FROM genres;")
        genres = cur.fetchall()
        query = "SELECT books.title AS title, books.book_id AS book_id, genres.genre_id AS genre_id, genres.description AS description FROM genres "\
                "INNER JOIN books_genres ON genres.genre_id = books_genres.genre_id "\
                "INNER JOIN books ON books.book_id = books_genres.book_id "\
                "ORDER BY description ASC;"
        cur.execute(query)
        books_genres = cur.fetchall()
        cur.execute("SELECT * FROM books;")
        books = cur.fetchall()
        return render_template("genres.html", genres = genres, books_genres = books_genres, books = books)

    if request.method == "POST":
        # Checks which form it is to insert into to correct table
        if request.form["hidden"] == "addGenre":
            genre = request.form
            query = "INSERT INTO genres (description) VALUES(%s);"
            params = [genre["description"]]
            cur.execute(query, params) 
            mysql.connection.commit()
            return redirect("/genres")
        if request.form["hidden"] == "addBookToGenre":
            genre_book = request.form
            query = "INSERT INTO books_genres (book_id, genre_id) VALUES(%s, %s);"
            params = [genre_book["book_id"], genre_book["genre_id"]]
            cur.execute(query, params)
            mysql.connection.commit()
            return redirect("/genres")

@app.route("/genres/edit/<genre_id>", methods=["GET", "POST"])
def edit_genre(genre_id):
    cur = mysql.connection.cursor()
    if request.method == "GET":
        query = "SELECT * FROM genres WHERE genre_id = %s;"
        params = [genre_id]
        cur.execute(query, params)
        results = cur.fetchall()
        return render_template("genres-edit.html", genre = results[0])

    if request.method == "POST":
        genre = request.form
        query = "UPDATE genres SET description = %s WHERE genre_id = %s;"
        params = [genre["description"], genre["genre_id"]]
        cur.execute(query, params)
        mysql.connection.commit()
        return redirect("/genres")

@app.route("/genres/edit/<book_id>/<genre_id>", methods=["GET", "POST"])
def edit_book_genre(book_id, genre_id):
    cur = mysql.connection.cursor()
    if request.method == "GET":
        query = "SELECT * FROM books WHERE book_id = %s;"
        params = [book_id]
        cur.execute(query, params) 
        book = cur.fetchall()
        query = "SELECT * FROM genres WHERE genre_id = %s;"
        params = [genre_id]
        cur.execute(query, params)  
        genre = cur.fetchall()
        cur.execute("SELECT * FROM genres;")
        genres = cur.fetchall()
        return render_template("books-genres.html", book = book[0], genre = genre[0], genres = genres)
    
    if request.method == "POST":
        book_genre = request.form
        query = "UPDATE books_genres SET genre_id = %s WHERE genre_id = %s AND book_id =%s;"
        params = [book_genre["genre_id"], book_genre["original_genre_id"], book_genre["book_id"]]
        cur.execute(query, params)
        mysql.connection.commit()
        return redirect("/genres")


@app.route("/genres/delete/<genre_id>")
def delete_genre(genre_id):
    cur = mysql.connection.cursor()
    query = "DELETE FROM genres WHERE genre_id = %s;"
    params = [genre_id]
    cur.execute(query, params)
    mysql.connection.commit()
    return redirect("/genres")

@app.route("/genres/delete/<book_id>/<genre_id>")
def delete_book_genre(book_id, genre_id):
    cur = mysql.connection.cursor()
    query = "DELETE FROM books_genres WHERE book_id = %s AND genre_id = %s;"
    params = [book_id, genre_id]
    cur.execute(query, params)
    mysql.connection.commit()
    return redirect("/genres")

# Authors CRUD
@app.route("/authors", methods=["GET", "POST"])
def authors():
    cur = mysql.connection.cursor()
    if request.method == "GET":
        cur.execute("SELECT * FROM authors;")
        authors = cur.fetchall()
        return render_template("authors.html", authors = authors)
    
    if request.method == "POST":
        author = request.form
        query = "INSERT INTO authors (first_name, last_name) VALUES(%s, %s);"
        params = [author["first_name"], author["last_name"]]
        cur.execute(query, params) 
        mysql.connection.commit()
        return redirect("/authors")

@app.route("/authors/edit/<int:author_id>", methods=["GET", "POST"])
def edit_author(author_id):
    cur = mysql.connection.cursor()
    if request.method == "GET":
        query = "SELECT * FROM authors WHERE author_id = %s;"
        params = [author_id]
        cur.execute(query, params)
        results = cur.fetchall()
        return render_template("authors-edit.html", author=results[0])

    if request.method == "POST":
        author = request.form
        query = "UPDATE authors SET first_name= %s, last_name= %s WHERE author_id = %s;"
        params = [author["first_name"], author["last_name"], author["author_id"]]
        cur.execute(query, params)
        mysql.connection.commit()
        return redirect("/authors")


@app.route("/authors/delete/<int:author_id>")
def delete_author(author_id):
    cur = mysql.connection.cursor()
    query = "DELETE FROM authors WHERE author_id = %s"
    params = [author_id]
    cur.execute(query, params)
    mysql.connection.commit()
    return redirect("/authors")

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

@app.route("/books/edit/<int:book_id>", methods=["GET", "POST"])
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

@app.route("/books/delete/<int:book_id>")
def delete_book(book_id):
    cur = mysql.connection.cursor()
    query = "DELETE FROM books WHERE book_id = %s;"
    params = [book_id]
    cur.execute(query, params)
    mysql.connection.commit()
    return redirect("/books")

# AUTHORS_BOOKS CRUD
@app.route("/authors-books", methods=["GET", "POST"])
def authors_books():
    # Get all authors_books
    cur = mysql.connection.cursor()
    if request.method == "GET":
        query = "SELECT b.title AS title, CONCAT(a.first_name, ' ', a.last_name) AS full_name, "\
            "b.book_id, a.author_id FROM authors AS a "\
            "INNER JOIN authors_books AS ab ON a.author_id = ab.author_id "\
            "INNER JOIN books AS b ON b.book_id = ab.book_id;"
        cur.execute(query)
        results = cur.fetchall()
        cur.execute("SELECT * FROM authors;")
        authors = cur.fetchall()
        cur.execute("SELECT * FROM books;")
        books = cur.fetchall()
        return render_template("authors-books.html", authors_books=results, authors=authors, books=books)

    if request.method == "POST":
        author_book = request.form
        query = "INSERT INTO authors_books(author_id, book_id) VALUES(%s, %s);"
        params = [author_book["author_id"], author_book["book_id"]]
        cur.execute(query, params)
        mysql.connection.commit()
        return redirect("/authors-books")
    

@app.route("/authors-books/edit/<int:book_id>/<int:author_id>", methods=["GET", "POST"])
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
    query = "DELETE FROM authors_books WHERE author_id=%s AND book_id=%s;"
    params = [author_id, book_id]
    cur.execute(query, params)
    mysql.connection.commit()
    return redirect("/authors-books")

# Listener
if __name__ == "__main__":
    app.run(port=56879, debug=True)
