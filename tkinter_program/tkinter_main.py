
# gui_app.py
import tkinter as tk
from tkinter import messagebox, simpledialog
from book_library import Book, EBook, Library, BookNotAvailableError

# Create an instance of Library to manage our books
library = Library()

# Initialize the main window for the GUI
root = tk.Tk()
root.title("Library Management System")
root.geometry("600x600")  # Set a larger window size

# ====================== Function Definitions ======================

def add_book():
    """
    Adds a new book or eBook to the library.
    Gets data from the user input fields and validates them.
    """
    title = title_entry.get()
    author = author_entry.get()
    isbn = isbn_entry.get()
    is_ebook = ebook_var.get()
    size = size_entry.get()

    # Basic validation
    if not title or not author or not isbn:
        messagebox.showerror("Error", "Title, Author, and ISBN are required.")
        return

    if is_ebook and not size:
        messagebox.showerror("Error", "Download size required for eBooks.")
        return

    # Create the appropriate book object
    if is_ebook:
        book = EBook(title, author, isbn, size)
    else:
        book = Book(title, author, isbn)

    # Add the book to the library
    library.add_book(book)
    messagebox.showinfo("Success", f"Book '{title}' added to the library.")
    update_book_list()

def lend_book():
    """
    Lends a book by ISBN, updates list, and handles exceptions.
    Prompts user for ISBN.
    """
    isbn = simpledialog.askstring("Lend Book", "Enter ISBN of the book to lend:")
    if isbn:
        try:
            library.lend_book(isbn)
            messagebox.showinfo("Success", "Book lent successfully.")
            update_book_list()
        except BookNotAvailableError as e:
            messagebox.showerror("Error", str(e))

def return_book():
    """
    Returns a book by ISBN. Validates and updates library.
    """
    isbn = simpledialog.askstring("Return Book", "Enter ISBN of the book to return:")
    if isbn:
        try:
            library.return_book(isbn)
            messagebox.showinfo("Success", "Book returned successfully.")
            update_book_list()
        except BookNotAvailableError as e:
            messagebox.showerror("Error", str(e))

def remove_book():
    """
    Removes a book from the library by ISBN.
    """
    isbn = simpledialog.askstring("Remove Book", "Enter ISBN of the book to remove:")
    if isbn:
        library.remove_book(isbn)
        messagebox.showinfo("Success", "Book removed from library.")
        update_book_list()

def view_books_by_author():
    """
    Uses generator to display all books by a specific author.
    """
    author = simpledialog.askstring("Search by Author", "Enter author's name:")
    if author:
        books = list(library.books_by_author(author))
        if books:
            listbox.delete(0, tk.END)
            listbox.insert(tk.END, f"Books by {author}:")
            for book in books:
                listbox.insert(tk.END, str(book))
        else:
            messagebox.showinfo("Not Found", "No books by this author.")

def update_book_list():
    """
    Updates the Listbox to show all currently available (not lent) books.
    Uses the custom iterator implemented in Library.
    """
    listbox.delete(0, tk.END)  # Clear existing entries
    listbox.insert(tk.END, "Available Books:")
    for book in library:
        listbox.insert(tk.END, str(book))

# ====================== GUI Widgets ======================

# Input: Title
tk.Label(root, text="Title:").pack()
title_entry = tk.Entry(root)
title_entry.pack()

# Input: Author
tk.Label(root, text="Author:").pack()
author_entry = tk.Entry(root)
author_entry.pack()

# Input: ISBN
tk.Label(root, text="ISBN:").pack()
isbn_entry = tk.Entry(root)
isbn_entry.pack()

# Checkbox for eBook selection
ebook_var = tk.BooleanVar()
tk.Checkbutton(root, text="eBook?", variable=ebook_var).pack()

# Input: Download size (only for eBooks)
tk.Label(root, text="Download Size (MB):").pack()
size_entry = tk.Entry(root)
size_entry.pack()

# Button: Add book
tk.Button(root, text="Add Book", command=add_book).pack(pady=5)

# Button: Lend book
tk.Button(root, text="Lend Book", command=lend_book).pack(pady=5)

# Button: Return book
tk.Button(root, text="Return Book", command=return_book).pack(pady=5)

# Button: Remove book
tk.Button(root, text="Remove Book", command=remove_book).pack(pady=5)

# Button: View books by author (uses generator)
tk.Button(root, text="View Books by Author", command=view_books_by_author).pack(pady=5)

# Separator Label
tk.Label(root, text="Library Inventory:").pack()

# Listbox to display current book list
listbox = tk.Listbox(root, width=70)
listbox.pack(pady=10)

# Show all available books at start
update_book_list()

# Start the GUI event loop
root.mainloop()

