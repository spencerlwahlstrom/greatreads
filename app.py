# Citation
# scope: all router functions for app.py
# date: 6/6/2022
# originality: functions based on functions flask guide
# Source: https://github.com/osu-cs340-ecampus/flask-starter-app

from flask import Flask, render_template, redirect, request
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


# Home
@app.route("/")
def root():
    return render_template("index.html")


# Home for project submission
@app.route("/index.html")
def index():
    return render_template("index.html")


# REVIEWS CRUD
@app.route("/reviews", methods=["GET", "POST"])
def reviews():
    cur = mysql.connection.cursor()

    # READ - Show all reviews
    if request.method == "GET":
        cur.execute("SELECT r.review_id, r.book_id, b.title, r.rating, \
                    r.summary, r.user_handle FROM reviews r \
                    LEFT JOIN books b ON r.book_id = b.book_id;")
        reviews = cur.fetchall()

        # Catch cases where book_id is None (book has been deleted)
        for review in reviews:
            if not review["title"]:
                review["title"] = "NULL"

        cur.execute("SELECT * FROM books;")
        books = cur.fetchall()
        return render_template("reviews.html", reviews=reviews, books=books)

    # CREATE - Add a new review
    if request.method == "POST":
        review = request.form
        query = "INSERT INTO reviews (book_id, rating, summary, user_handle) \
                VALUES (%s, %s, %s, %s);"
        params = [
                    review["book"], review["rating"],
                    review["summary"], review["user_handle"]
                ]
        cur.execute(query, params)
        mysql.connection.commit()
        return redirect("/reviews")


@app.route("/reviews/edit/<int:review_id>", methods=["GET", "POST"])
def edit_review(review_id):
    # UPDATE - Change a review
    if request.method == "POST":
        review = request.form
        cur = mysql.connection.cursor()
        query = "UPDATE reviews SET rating= %s, summary= %s, user_handle=%s \
                WHERE review_id = %s;"
        params = [
                    review["rating"], review["summary"],
                    review["user_handle"], review_id
                ]
        cur.execute(query, params)
        mysql.connection.commit()
        return redirect("/reviews")


@app.route("/reviews/delete/<int:review_id>")
def delete_review(review_id):
    # DELETE - Delete a review
    cur = mysql.connection.cursor()
    query = "DELETE FROM reviews WHERE review_id = %s;"
    params = [review_id]
    cur.execute(query, params)
    mysql.connection.commit()
    return redirect("/reviews")


# GENRES / BOOKS_GENRES CRUD
def bg_duplicate_helper(book_id, genre_id):
    """
    Helper function returns None or the duplicate
    Books_Genres entry if found
    """
    cur = mysql.connection.cursor()
    # Check for duplicates
    query = "SELECT b.title AS title, g.description AS description "\
            "FROM genres AS g "\
            "INNER JOIN books_genres AS bg ON g.genre_id = bg.genre_id "\
            "INNER JOIN books AS b ON b.book_id = bg.book_id "\
            "WHERE g.genre_id=%s AND b.book_id=%s;"
    params = [genre_id, book_id]
    cur.execute(query, params)
    duplicate = cur.fetchall()
    return duplicate


@app.route("/genres", methods=["GET", "POST"])
def genres():
    cur = mysql.connection.cursor()

    # READ - Show all genres and books_genres
    if request.method == "GET":
        cur.execute("SELECT * FROM genres;")
        genres = cur.fetchall()
        query = "SELECT b.title AS title, b.book_id AS book_id, "\
                "g.genre_id AS genre_id, g.description AS "\
                "description FROM genres AS g "\
                "INNER JOIN books_genres AS bg ON g.genre_id = bg.genre_id "\
                "INNER JOIN books AS b ON b.book_id = bg.book_id "\
                "ORDER BY description ASC;"
        cur.execute(query)
        books_genres = cur.fetchall()
        cur.execute("SELECT * FROM books;")
        books = cur.fetchall()
        return render_template(
                "genres.html",
                genres=genres,
                books_genres=books_genres,
                books=books
                )

    # CREATE - Add a new genre or book_genre relationship
    if request.method == "POST":
        # Checks which form it is to insert into to correct table
        if request.form["hidden"] == "addGenre":
            genre = request.form
            query = "INSERT INTO genres (description) VALUES(%s);"
            params = [genre["description"]]
            cur.execute(query, params)
            mysql.connection.commit()
            return redirect("/genres")
        if request.form["hidden"] == "addGenreToBook":
            genre_book = request.form

            # Check for duplicates
            duplicate = bg_duplicate_helper(
                        genre_book["book_id"],
                        genre_book["genre_id"]
                        )

            # Update if no duplicates found, display error otherwise
            if not duplicate:
                query = "INSERT INTO books_genres (book_id, genre_id) "\
                        "VALUES(%s, %s);"
                params = [genre_book["book_id"], genre_book["genre_id"]]
                cur.execute(query, params)
                mysql.connection.commit()
                return redirect("/genres")
            else:
                return render_template("duplicate.html", bg=duplicate[0])


@app.route("/genres/edit/<int:genre_id>", methods=["GET", "POST"])
def edit_genre(genre_id):
    cur = mysql.connection.cursor()

    # READ - Show a specific genre
    if request.method == "GET":
        query = "SELECT * FROM genres WHERE genre_id = %s;"
        params = [genre_id]
        cur.execute(query, params)
        results = cur.fetchall()
        return render_template("genres-edit.html", genre=results[0])

    # UPDATE - Change a specific genre
    if request.method == "POST":
        genre = request.form
        query = "UPDATE genres SET description = %s WHERE genre_id = %s;"
        params = [genre["description"], genre_id]
        cur.execute(query, params)
        mysql.connection.commit()
        return redirect("/genres")


@app.route(
        "/genres/edit/<int:book_id>/<int:genre_id>",
        methods=["GET", "POST"]
        )
def edit_book_genre(book_id, genre_id):
    cur = mysql.connection.cursor()

    # UPDATE - Change a specific book_genre relationship
    if request.method == "POST":
        book_genre = request.form

        # Check for duplicates
        duplicate = bg_duplicate_helper(
                    book_id,
                    book_genre["genre_id"]
                    )

        # Update if no duplicates found, display error otherwise
        if not duplicate:
            query = "UPDATE books_genres SET genre_id = %s "\
                    "WHERE genre_id = %s AND book_id =%s;"
            params = [
                        book_genre["genre_id"],
                        genre_id,
                        book_id,
                    ]
            cur.execute(query, params)
            mysql.connection.commit()
            return redirect("/genres")
        else:
            return render_template("/duplicate.html", bg=duplicate[0])


@app.route("/genres/delete/<int:genre_id>")
def delete_genre(genre_id):
    # DELETE - Delete a genre
    cur = mysql.connection.cursor()
    query = "DELETE FROM genres WHERE genre_id = %s;"
    params = [genre_id]
    cur.execute(query, params)
    mysql.connection.commit()
    return redirect("/genres")


@app.route("/genres/delete/<int:book_id>/<int:genre_id>")
def delete_book_genre(book_id, genre_id):
    # DELETE - Delete a book_genre relationship
    cur = mysql.connection.cursor()
    query = "DELETE FROM books_genres WHERE book_id = %s AND genre_id = %s;"
    params = [book_id, genre_id]
    cur.execute(query, params)
    mysql.connection.commit()
    return redirect("/genres")


# AUTHORS CRUD
@app.route("/authors", methods=["GET", "POST"])
def authors():
    cur = mysql.connection.cursor()

    # READ - Show all authors
    if request.method == "GET":
        query = "SELECT b.title AS title, "\
                "CONCAT(a.first_name, ' ', a.last_name) AS full_name, "\
                "b.book_id, a.author_id FROM authors AS a "\
                "INNER JOIN authors_books AS ab "\
                "ON a.author_id = ab.author_id "\
                "INNER JOIN books AS b ON b.book_id = ab.book_id;"
        cur.execute(query)
        authors_books = cur.fetchall()
        cur.execute("SELECT * FROM authors;")
        authors = cur.fetchall()
        cur.execute("SELECT * FROM books;")
        books = cur.fetchall()
        return render_template(
                "authors.html",
                authors_books=authors_books,
                authors=authors,
                books=books
                )

    # CREATE - Add a new author
    if request.method == "POST":
        if request.form["hidden"] == "addAuthor":
            author = request.form
            query = "INSERT INTO authors (first_name, last_name) "\
                    "VALUES(%s, %s);"
            params = [author["first_name"], author["last_name"]]
            cur.execute(query, params)
            mysql.connection.commit()
            return redirect("/authors")
        if request.form["hidden"] == "addAuthorBook":
            author_book = request.form

            # Check for duplicates
            duplicate = ab_duplicate_helper(
                        author_book["book_id"],
                        author_book["author_id"]
                        )

            # Insert if no duplicates found, display error otherwise
            if not duplicate:
                query = "INSERT INTO authors_books(author_id, book_id) "\
                        "VALUES(%s, %s);"
                params = [author_book["author_id"], author_book["book_id"]]
                cur.execute(query, params)
                mysql.connection.commit()
                return redirect("/authors")
            else:
                return render_template("duplicate.html", ab=duplicate[0])


@app.route("/authors/filter/<int:author_id>", methods=["GET", "POST"])
def filter_author(author_id):
    cur = mysql.connection.cursor()
    # query filters authors_books table by author_id paramter
    query = "SELECT b.title AS title, "\
            "CONCAT(a.first_name, ' ', a.last_name) AS full_name, "\
            "b.book_id, a.author_id FROM authors AS a "\
            "INNER JOIN authors_books AS ab "\
            "ON a.author_id = ab.author_id "\
            "INNER JOIN books AS b ON b.book_id = ab.book_id "\
            "WHERE a.author_id = %s ;"
    params = [author_id]
    cur.execute(query, params)
    authors_books = cur.fetchall()
    cur.execute("SELECT * FROM authors;")
    authors = cur.fetchall()
    cur.execute("SELECT * FROM books;")
    books = cur.fetchall()
    return render_template(
                "authors.html",
                authors_books=authors_books,
                authors=authors,
                books=books)


@app.route("/authors/edit/<int:author_id>", methods=["GET", "POST"])
def edit_author(author_id):
    cur = mysql.connection.cursor()
    # UPDATE - Change a specific author
    if request.method == "POST":
        author = request.form
        query = "UPDATE authors SET first_name= %s, last_name= %s "\
                "WHERE author_id = %s;"
        params = [author["first_name"], author["last_name"], author_id]
        cur.execute(query, params)
        mysql.connection.commit()
        return redirect("/authors")


@app.route("/authors/delete/<int:author_id>")
def delete_author(author_id):
    # DELETE - Delete an author
    cur = mysql.connection.cursor()
    query = "DELETE FROM authors WHERE author_id = %s"
    params = [author_id]
    cur.execute(query, params)
    mysql.connection.commit()
    return redirect("/authors")


# BOOKS CRUD
@app.route("/books", methods=["GET", "POST"])
def books():
    # READ - Get all books
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM books;")
        books = cur.fetchall()
        return render_template("books.html", books=books)

    # CREATE - Add a new book
    if request.method == "POST":
        book = request.form
        cur = mysql.connection.cursor()
        query = "INSERT INTO books (title, publisher, isbn, summary, "\
                "published_date, msrp, average_rating) "\
                "VALUES (%s, %s, %s, %s, %s, %s, %s);"
        params = [
                    book["title"], book["publisher"], book["isbn"],
                    book["summary"], book["published_date"], book["msrp"],
                    book["average_rating"]
                ]
        cur.execute(query, params)
        mysql.connection.commit()
        return redirect("/books")


@app.route("/books/edit/<int:book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    # UPDATE - Change a specific book
    if request.method == "POST":
        book = request.form
        cur = mysql.connection.cursor()
        query = "UPDATE books SET title = %s, publisher = %s, isbn = %s, "\
                "summary = %s, published_date = %s, msrp = %s, "\
                "average_rating = %s WHERE book_id = %s;"
        params = [
                    book["title"], book["publisher"], book["isbn"],
                    book["summary"], book["published_date"], book["msrp"],
                    book["average_rating"], book_id
                ]
        cur.execute(query, params)
        mysql.connection.commit()
        return redirect("/books")


@app.route("/books/delete/<int:book_id>")
def delete_book(book_id):
    # DELETE - Delete a book
    cur = mysql.connection.cursor()
    query = "DELETE FROM books WHERE book_id = %s;"
    params = [book_id]
    cur.execute(query, params)
    mysql.connection.commit()
    return redirect("/books")


# AUTHORS_BOOKS CRUD
def ab_duplicate_helper(book_id, author_id):
    """
    Helper function returns None or the duplicate
    Author_Book entry if found
    """
    cur = mysql.connection.cursor()
    # Check for duplicates
    query = "SELECT b.title AS title, "\
            "CONCAT(a.first_name, ' ', a.last_name) AS full_name "\
            "FROM authors AS a "\
            "INNER JOIN authors_books AS ab ON a.author_id = ab.author_id "\
            "INNER JOIN books AS b ON b.book_id = ab.book_id "\
            "WHERE a.author_id=%s AND b.book_id=%s;"
    params = [author_id, book_id]
    cur.execute(query, params)
    duplicate = cur.fetchall()
    return duplicate


@app.route(
        "/authors/edit/<int:book_id>/<int:author_id>",
        methods=["GET", "POST"]
        )
def edit_ab(book_id, author_id):
    # UPDATE - Change a specific author_book relationship
    if request.method == "POST":
        cur = mysql.connection.cursor()
        ab = request.form
        new_book_id = ab["book"]
        new_author_id = ab["author"]

        # Check for duplicates
        duplicate = ab_duplicate_helper(new_book_id, new_author_id)

        # Update if no duplicates found, display error otherwise
        if not duplicate:
            query = "UPDATE authors_books SET author_id=%s, book_id=%s "\
                    "WHERE author_id=%s AND book_id=%s;"
            params = [new_author_id, new_book_id, author_id, book_id]
            cur.execute(query, params)
            mysql.connection.commit()
            return redirect("/authors")
        else:
            return render_template("/duplicate.html", ab=duplicate[0])


@app.route("/authors/delete/<book_id>/<author_id>")
def delete_ab(book_id, author_id):
    # DELETE - Delete an author_book relationship
    cur = mysql.connection.cursor()
    query = "DELETE FROM authors_books WHERE author_id=%s AND book_id=%s;"
    params = [author_id, book_id]
    cur.execute(query, params)
    mysql.connection.commit()
    return redirect("/authors")


# Listener
if __name__ == "__main__":
    app.run(port=56879, debug=True)
