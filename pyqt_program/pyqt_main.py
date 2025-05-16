import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QCheckBox, QListWidget, QMessageBox, QInputDialog, QFormLayout
)
from PyQt5.QtGui import QFont
from book_library import Book, EBook, Library, BookNotAvailableError

class LibraryGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.library = Library()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Library Management System")
        self.setGeometry(100, 100, 600, 500)

        font_label = QFont("Arial", 10)
        font_button = QFont("Arial", 10)

        # Form Layout
        form_layout = QFormLayout()
        self.title_input = QLineEdit()
        self.author_input = QLineEdit()
        self.isbn_input = QLineEdit()
        self.ebook_checkbox = QCheckBox("Is eBook?")
        self.size_input = QLineEdit()
        self.size_input.setDisabled(True)
        self.size_input.setPlaceholderText("MB")

        self.ebook_checkbox.stateChanged.connect(self.toggle_size_input)

        form_layout.addRow("Title:", self.title_input)
        form_layout.addRow("Author:", self.author_input)
        form_layout.addRow("ISBN:", self.isbn_input)
        form_layout.addRow(self.ebook_checkbox)
        form_layout.addRow("Download Size:", self.size_input)

        # Buttons layout
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Book")
        self.lend_button = QPushButton("Lend Book")
        self.return_button = QPushButton("Return Book")
        self.remove_button = QPushButton("Remove Book")
        self.search_button = QPushButton("Search by Author")

        for btn in [self.add_button, self.lend_button, self.return_button, self.remove_button, self.search_button]:
            btn.setFont(font_button)
            button_layout.addWidget(btn)

        # Connect buttons
        self.add_button.clicked.connect(self.add_book)
        self.lend_button.clicked.connect(self.lend_book)
        self.return_button.clicked.connect(self.return_book)
        self.remove_button.clicked.connect(self.remove_book)
        self.search_button.clicked.connect(self.search_by_author)

        # Book List
        self.book_list = QListWidget()
        self.update_book_list()

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(QLabel("Available Books:"))
        main_layout.addWidget(self.book_list)

        self.setLayout(main_layout)

    def toggle_size_input(self, state):
        self.size_input.setDisabled(not state)
        if not state:
            self.size_input.clear()

    def add_book(self):
        title = self.title_input.text()
        author = self.author_input.text()
        isbn = self.isbn_input.text()
        is_ebook = self.ebook_checkbox.isChecked()
        size = self.size_input.text()

        if not title or not author or not isbn:
            QMessageBox.warning(self, "Input Error", "Please fill in Title, Author, and ISBN.")
            return

        if is_ebook:
            if not size or not size.isdigit():
                QMessageBox.warning(self, "Input Error", "Enter valid download size (number only).")
                return
            book = EBook(title, author, isbn, int(size))
        else:
            book = Book(title, author, isbn)

        self.library.add_book(book)
        QMessageBox.information(self, "Success", f"Book '{title}' added successfully.")
        self.update_book_list()
        self.clear_inputs()

    def lend_book(self):
        available_books = [book for book in self.library.books if not book.is_lent]
        if not available_books:
            QMessageBox.information(self, "No Books", "No books available to lend.")
            return

        options = [f"{book.title} (ISBN: {book.isbn})" for book in available_books]
        choice, ok = QInputDialog.getItem(self, "Lend Book", "Select book to lend:", options, 0, False)
        if ok and choice:
            isbn = choice.split("ISBN: ")[-1][:-1] if choice.endswith(")") else choice.split("ISBN: ")[-1]
            try:
                self.library.lend_book(isbn)
                QMessageBox.information(self, "Success", "Book lent successfully.")
                self.update_book_list()
            except BookNotAvailableError as e:
                QMessageBox.warning(self, "Error", str(e))

    def return_book(self):
        lent_books = [book for book in self.library.books if book.is_lent]
        if not lent_books:
            QMessageBox.information(self, "No Books", "No books currently lent out.")
            return

        options = [f"{book.title} (ISBN: {book.isbn})" for book in lent_books]
        choice, ok = QInputDialog.getItem(self, "Return Book", "Select book to return:", options, 0, False)
        if ok and choice:
            isbn = choice.split("ISBN: ")[-1][:-1] if choice.endswith(")") else choice.split("ISBN: ")[-1]
            try:
                self.library.return_book(isbn)
                QMessageBox.information(self, "Success", "Book returned successfully.")
                self.update_book_list()
            except BookNotAvailableError as e:
                QMessageBox.warning(self, "Error", str(e))

    def remove_book(self):
        isbn, ok = QInputDialog.getText(self, "Remove Book", "Enter ISBN:")
        if ok and isbn:
            self.library.remove_book(isbn)
            QMessageBox.information(self, "Success", "Book removed from library.")
            self.update_book_list()

    def search_by_author(self):
        author, ok = QInputDialog.getText(self, "Search by Author", "Enter author's name:")
        if ok and author:
            books = list(self.library.books_by_author(author))
            self.book_list.clear()
            if books:
                self.book_list.addItem(f"Books by {author}:")
                for book in books:
                    self.book_list.addItem(str(book))
            else:
                QMessageBox.information(self, "Not Found", "No books found by that author.")

    def update_book_list(self):
        self.book_list.clear()
        self.book_list.addItem("Available Books:")
        for book in self.library:
            self.book_list.addItem(str(book))

    def clear_inputs(self):
        self.title_input.clear()
        self.author_input.clear()
        self.isbn_input.clear()
        self.size_input.clear()
        self.ebook_checkbox.setChecked(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = LibraryGUI()
    gui.show()
    sys.exit(app.exec_())
