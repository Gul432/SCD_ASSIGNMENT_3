import tkinter as tk
from tkinter import messagebox, simpledialog
from book_library import Book, EBook, Library, BookNotAvailableError

library = Library()

root = tk.Tk()
root.title("Library Management System")
root.geometry("700x600")
root.configure(bg="#f2f2f2")

# ====================== Handlers ======================

def toggle_ebook_field():
    """
    Enable or disable size_entry based on eBook checkbox.
    """
    if ebook_var.get():
        size_entry.config(state='normal')
    else:
        size_entry.delete(0, tk.END)
        size_entry.config(state='disabled')

def add_book():
    title = title_entry.get()
    author = author_entry.get()
    isbn = isbn_entry.get()
    is_ebook = ebook_var.get()
    size = size_entry.get()

    if not title or not author or not isbn:
        messagebox.showerror("Error", "Title, Author, and ISBN are required.")
        return

    if is_ebook:
        if not size:
            messagebox.showerror("Error", "Download size required for eBooks.")
            return
        try:
            size = float(size)
        except ValueError:
            messagebox.showerror("Error", "Download size must be a number.")
            return
        book = EBook(title, author, isbn, size)
    else:
        book = Book(title, author, isbn)

    library.add_book(book)
    messagebox.showinfo("Success", f"Book '{title}' added.")
    update_book_list()

def lend_book():
    isbn = simpledialog.askstring("Lend Book", "Enter ISBN:")
    if isbn:
        try:
            library.lend_book(isbn)
            messagebox.showinfo("Success", "Book lent.")
            update_book_list()
        except BookNotAvailableError as e:
            messagebox.showerror("Error", str(e))

def return_book():
    isbn = simpledialog.askstring("Return Book", "Enter ISBN:")
    if isbn:
        try:
            library.return_book(isbn)
            messagebox.showinfo("Success", "Book returned.")
            update_book_list()
        except BookNotAvailableError as e:
            messagebox.showerror("Error", str(e))

def remove_book():
    isbn = simpledialog.askstring("Remove Book", "Enter ISBN:")
    if isbn:
        library.remove_book(isbn)
        messagebox.showinfo("Removed", "Book removed.")
        update_book_list()

def view_books_by_author():
    author = simpledialog.askstring("Search", "Enter author's name:")
    if author:
        books = list(library.books_by_author(author))
        listbox.delete(0, tk.END)
        if books:
            listbox.insert(tk.END, f"Books by {author}:")
            for book in books:
                listbox.insert(tk.END, str(book))
        else:
            messagebox.showinfo("Not Found", "No books by this author.")

def update_book_list():
    listbox.delete(0, tk.END)
    listbox.insert(tk.END, "Available Books:")
    for book in library:
        listbox.insert(tk.END, str(book))

# ====================== GUI Layout ======================

# Title
tk.Label(root, text="Title:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
title_entry = tk.Entry(root, width=40)
title_entry.grid(row=0, column=1, pady=5)

# Author
tk.Label(root, text="Author:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
author_entry = tk.Entry(root, width=40)
author_entry.grid(row=1, column=1, pady=5)

# ISBN
tk.Label(root, text="ISBN:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
isbn_entry = tk.Entry(root, width=40)
isbn_entry.grid(row=2, column=1, pady=5)

# eBook Checkbox
ebook_var = tk.BooleanVar()
ebook_check = tk.Checkbutton(root, text="eBook?", variable=ebook_var, command=toggle_ebook_field)
ebook_check.grid(row=3, column=0, padx=5, pady=5)

# Download Size
tk.Label(root, text="Download Size (MB):").grid(row=3, column=1, sticky="w")
size_entry = tk.Entry(root, width=15, state='disabled')  # Initially disabled
size_entry.grid(row=3, column=1, sticky="e")

# Buttons
tk.Button(root, text="Add Book", width=20, command=add_book).grid(row=4, column=0, pady=10)
tk.Button(root, text="Lend Book", width=20, command=lend_book).grid(row=4, column=1)
tk.Button(root, text="Return Book", width=20, command=return_book).grid(row=5, column=0, pady=5)
tk.Button(root, text="Remove Book", width=20, command=remove_book).grid(row=5, column=1)
tk.Button(root, text="View by Author", width=43, command=view_books_by_author).grid(row=6, column=0, columnspan=2, pady=10)

# Inventory Label
tk.Label(root, text="Library Inventory:").grid(row=7, column=0, columnspan=2)

# Book List
listbox = tk.Listbox(root, width=80, height=15)
listbox.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

# Show books at start
update_book_list()

# Main Loop
root.mainloop()
