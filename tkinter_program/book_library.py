# book_library.py

class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_lent = False

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"

class EBook(Book):
    def __init__(self, title, author, isbn, size):
        super().__init__(title, author, isbn)
        self.size = size  # ✅ THIS LINE IS CRITICAL!

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn}, Size: {self.size}MB)"

class BookNotAvailableError(Exception):
    pass

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        for existing in self.books:
            if existing.isbn == book.isbn:
                raise ValueError("Book with this ISBN already exists.")
        self.books.append(book)

    def remove_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                self.books.remove(book)
                return
        raise ValueError("Book not found.")

    def lend_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                if book.is_lent:
                    raise BookNotAvailableError("Book is already lent.")
                book.is_lent = True
                return
        raise BookNotAvailableError("Book not found.")

    def return_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                if not book.is_lent:
                    raise BookNotAvailableError("Book was not lent.")
                book.is_lent = False
                return
        raise BookNotAvailableError("Book not found.")

    def books_by_author(self, author):
        return (book for book in self.books if book.author.lower() == author.lower())
