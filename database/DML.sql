-- BOOKS

-- SELECT: Get all book data to populate the Books page
SELECT * from books;

-- INSERT: Add a new book
INSERT INTO books (title, publisher, isbn, summary, published_date, msrp) 
VALUES (:title_input, :publisher_input, :isbn_input, :summary_input, :published_date_input, :msrp_input);

-- UPDATE: Edit an existing book
UPDATE books SET title=:title_input, publisher=:publisher_input, isbn=:isbn_input, published_date=:published_date_input, msrp=:msrp_input 
WHERE book_id = :book_id_from_edit_button;

-- DELETE: Delete an existing book
DELETE FROM books WHERE book_id = :book_id_from_delete_button;

-- REVIEWS

-- SELECT: Get all review data to populate the Reviews page (include book's title)
SELECT r.review_id, r.book_id, b.title, r.rating, r.summary, r.user_handle FROM reviews r
INNER JOIN books b ON r.book_id = b.book_id;

-- INSERT: Get book_id and title to populate the dropdown for adding a review
SELECT book_id, title from books;

-- INSERT: Add a new review
INSERT INTO reviews (book_id, rating, summary, user_handle) 
VALUES (book_id=:book_id_from_add_dropdown, rating=:rating_input, summar=:summary_input, user_handle=user_handle_input);

-- UPDATE: Edit an existing review
UPDATE reviews SET rating=:rating_input, summary=:summary_input, user_handle=:user_handle_input
WHERE review_id = :review_id_from_edit_button;

-- DELETE: Delete an existing review
DELETE FROM reviews WHERE review_id = :review_id_from_delete_button;

-- AUTHORS

-- SELECT: Get all author data for the Author's page ()
SELECT * FROM authors;

-- SELECT: Get all booktitles associated with Authors for Books by Authors Table
SELECT  books.title, CONCAT(authors.first_name,' ',authors.last_name) 
FROM authors
INNER JOIN authors_books ON authors.author_id = authors_books.author_id
INNER JOIN books ON books.book_id = authors_books.book_id;

-- INSERT: Add a new author
INSERT INTO authors (first_name, last_name)
VALUES(first_name:first_name_input, last_name:last_name_input);

-- INSERT: Add a new author, book relationship to authors_books table
INSERT INTO authors_books(author_id, book_id)
VALUES(author_id:author_id_input, book_id:book_id_input);

-- INSERT: Get book_id and title to populate the dropdown for adding a review
SELECT book_id, title from books;

-- INSERT: Get author_id and fullname from authors
SELECT author_id, CONCAT(first_name, last_name) FROM authors;

-- UPDATE: Edit an author
UPDATE authors SET first_name=:first_name_input, last_name=:last_name_input
WHERE author_id =:author_id_from_edit_button;

-- DELETE: Delete an author
DELETE FROM authors WHERE author_id = :author_id_from_delete_button;

-- DELETE: Delete an entry in the authors_books intersection table
DELETE FROM authors_books WHERE author_id =:author_id_from_delete_button AND book_id =:book_id_from_delete_button;

-- GENRES

-- SELECT: Get all genre data for Genres
SELECT * FROM genres;

-- SELECT:
SELECT books.title, genres.description AS genre
FROM genres
INNER JOIN books_genres ON genres.genre_id = books_genres.genre_id
INNER JOIN books ON books.book_id = books_genres.book_id;

-- INSERT: Add a new genre
INSERT INTO genres (description)
VALUES(description:description_input);

-- INSERT: Add a book to a genre making a new books_genres entry in the table
INSERT INTO books_genres (book_id, genre_id)
VALUES(book_id:book_id_input, genre_id:genre_id_input);

-- INSERT: Get book_id and title to populate the dropdown for adding a review
SELECT book_id, title from books;

-- INSERT: Get genre_id, description to populate the dropdown for adding an entry to books_genres
SELECT genre_id, description from genres;

-- UPDATE: Edit a genre
UPDATE genres SET description=:description_input
WHERE genre_id =:genre_id_from_edit_button;

-- DELETE: Delete a genre
DELETE FROM genres WHERE genre_id = :genre_id_from_delete_button;

-- DELETE: Delete an entry in the books_genres interesection table
DELETE FROM books_genres WHERE genre_id = :genre_id_from_delete_button AND book_id =:book_id_from_delete_button;



