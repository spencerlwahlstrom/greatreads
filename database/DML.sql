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
