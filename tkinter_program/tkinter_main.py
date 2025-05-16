import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from book_library import Book, EBook, Library, BookNotAvailableError

class LibraryApp:
    def __init__(self, root):
        self.library = Library()
        self.search_highlight_tag = "highlight"

        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("900x750")
        self.root.configure(bg="#f5f5f5")

        self.setup_styles()
        self.create_widgets()
        self.update_book_list()

        self.root.bind('<Return>', lambda event: self.add_book())  # Add book on Enter key

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.configure('TFrame', background="#f5f5f5")
        self.style.configure('TLabel', background="#f5f5f5", font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        self.style.configure('TEntry', font=('Arial', 10), padding=5)
        self.style.map('TButton', 
                      foreground=[('active', 'black'), ('disabled', 'gray')],
                      background=[('active', '#e1e1e1'), ('disabled', '#f0f0f0')])

    def create_widgets(self):
        self.main_frame = ttk.Frame(self.root, padding="15")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.create_entry_frame()
        self.create_button_frame()
        self.create_inventory_frame()

    def create_entry_frame(self):
        entry_frame = ttk.LabelFrame(self.main_frame, text="Add New Book", padding=10)
        entry_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        ttk.Label(entry_frame, text="Title:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.title_entry = ttk.Entry(entry_frame, width=40)
        self.title_entry.grid(row=0, column=1, pady=5, sticky="ew")

        ttk.Label(entry_frame, text="Author:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.author_entry = ttk.Entry(entry_frame, width=40)
        self.author_entry.grid(row=1, column=1, pady=5, sticky="ew")

        ttk.Label(entry_frame, text="ISBN:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.isbn_entry = ttk.Entry(entry_frame, width=40)
        self.isbn_entry.grid(row=2, column=1, pady=5, sticky="ew")

        self.ebook_var = tk.BooleanVar()
        self.ebook_check = ttk.Checkbutton(entry_frame, text="eBook?", variable=self.ebook_var, command=self.toggle_ebook_field)
        self.ebook_check.grid(row=3, column=0, padx=5, pady=5, sticky="e")

        self.size_label = ttk.Label(entry_frame, text="Download Size (MB):", state='disabled')
        self.size_label.grid(row=3, column=1, sticky="w", padx=5)
        self.size_entry = ttk.Entry(entry_frame, width=15, state='disabled')
        self.size_entry.grid(row=3, column=1, sticky="e", padx=5)

        entry_frame.columnconfigure(1, weight=1)

    def create_button_frame(self):
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=1, column=0, sticky="ew", pady=10)

        buttons = [
            ("Add Book", self.add_book),
            ("Lend Book", self.lend_book),
            ("Return Book", self.return_book),
            ("Remove Book", self.remove_book),
            ("View by Author", self.view_books_by_author),
            ("Clear Highlight", self.clear_highlight)
        ]

        for i, (text, command) in enumerate(buttons):
            ttk.Button(button_frame, text=text, command=command, width=15).grid(row=0, column=i, padx=5, pady=5)

        button_frame.columnconfigure(tuple(range(len(buttons))), weight=1)

    def create_inventory_frame(self):
        inventory_frame = ttk.LabelFrame(self.main_frame, text="Library Inventory", padding=10)
        inventory_frame.grid(row=2, column=0, sticky="nsew", pady=10)

        self.tree = ttk.Treeview(inventory_frame, columns=("title", "author", "isbn", "status", "size"), show="headings", selectmode="extended", height=20)

        self.tree.heading("title", text="Title", anchor="w")
        self.tree.heading("author", text="Author", anchor="w")
        self.tree.heading("isbn", text="ISBN", anchor="w")
        self.tree.heading("status", text="Status", anchor="center")
        self.tree.heading("size", text="Size (MB)", anchor="center")

        self.tree.column("title", width=250, stretch=tk.YES)
        self.tree.column("author", width=200, stretch=tk.YES)
        self.tree.column("isbn", width=120, stretch=tk.YES)
        self.tree.column("status", width=100, stretch=tk.NO)
        self.tree.column("size", width=100, stretch=tk.NO)

        self.tree.tag_configure(self.search_highlight_tag, background='yellow')

        y_scroll = ttk.Scrollbar(inventory_frame, orient="vertical", command=self.tree.yview)
        y_scroll.pack(side="right", fill="y")
        x_scroll = ttk.Scrollbar(inventory_frame, orient="horizontal", command=self.tree.xview)
        x_scroll.pack(side="bottom", fill="x")

        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(2, weight=1)

    def toggle_ebook_field(self):
        if self.ebook_var.get():
            self.size_entry.config(state='normal')
            self.size_label.config(state='normal')
        else:
            self.size_entry.delete(0, tk.END)
            self.size_entry.config(state='disabled')
            self.size_label.config(state='disabled')

    def clear_fields(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.isbn_entry.delete(0, tk.END)
        self.ebook_var.set(False)
        self.size_entry.delete(0, tk.END)
        self.size_entry.config(state='disabled')
        self.size_label.config(state='disabled')
        self.title_entry.focus_set()

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        isbn = self.isbn_entry.get().strip()
        is_ebook = self.ebook_var.get()
        size = self.size_entry.get().strip()

        if not title or not author or not isbn:
            messagebox.showerror("Error", "Title, Author, and ISBN are required.")
            return

        if any(book.isbn == isbn for book in self.library.books):
            messagebox.showerror("Error", "A book with this ISBN already exists.")
            return

        try:
            if is_ebook:
                if not size:
                    messagebox.showerror("Error", "Download size required for eBooks.")
                    return
                try:
                    size = float(size)
                    if size <= 0:
                        raise ValueError("Size must be positive")
                except ValueError:
                    messagebox.showerror("Error", "Download size must be a positive number.")
                    return
                book = EBook(title, author, isbn, size)
            else:
                book = Book(title, author, isbn)

            self.library.add_book(book)
            self.update_book_list()
            messagebox.showinfo("Success", f"Book '{title}' added.")
            self.clear_fields()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add book: {str(e)}")

    def lend_book(self):
        available_books = [book for book in self.library.books if not book.is_lent]
        if not available_books:
            messagebox.showinfo("Info", "No available books to lend.")
            return

        book_list = "\n".join(f"{book.title} ({book.isbn})" for book in available_books)
        isbn = simpledialog.askstring("Lend Book", f"Available Books:\n{book_list}\n\nEnter ISBN to lend:")
        if isbn:
            try:
                self.library.lend_book(isbn)
                messagebox.showinfo("Success", "Book lent.")
                self.update_book_list()
            except BookNotAvailableError as e:
                messagebox.showerror("Error", str(e))

    def return_book(self):
        lent_books = [book for book in self.library.books if book.is_lent]
        if not lent_books:
            messagebox.showinfo("Info", "No books to return.")
            return

        book_list = "\n".join(f"{book.title} ({book.isbn})" for book in lent_books)
        isbn = simpledialog.askstring("Return Book", f"Lent Books:\n{book_list}\n\nEnter ISBN to return:")
        if isbn:
            try:
                self.library.return_book(isbn)
                messagebox.showinfo("Success", "Book returned.")
                self.update_book_list()
            except BookNotAvailableError as e:
                messagebox.showerror("Error", str(e))

    def remove_book(self):
        isbn = simpledialog.askstring("Remove Book", "Enter ISBN:")
        if isbn:
            confirm = messagebox.askyesno("Confirm", f"Remove book with ISBN {isbn}?")
            if confirm:
                try:
                    self.library.remove_book(isbn)
                    messagebox.showinfo("Removed", "Book removed.")
                    self.update_book_list()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to remove book: {str(e)}")

    def view_books_by_author(self):
        author = simpledialog.askstring("Search", "Enter author's name:")
        if author:
            self.clear_highlight()
            books = list(self.library.books_by_author(author))
            if books:
                for item in self.tree.get_children():
                    values = self.tree.item(item, 'values')
                    if values and values[1].strip().lower() == author.strip().lower():
                        self.tree.item(item, tags=(self.search_highlight_tag,))
                messagebox.showinfo("Search Results", f"Found {len(books)} books by {author}")
            else:
                messagebox.showinfo("Not Found", "No books by this author.")

    def clear_highlight(self):
        for item in self.tree.get_children():
            self.tree.item(item, tags=())

    def update_book_list(self):
        self.tree.delete(*self.tree.get_children())
        for book in self.library.books:
            status = "Lent" if book.is_lent else "Available"
            size = f"{book.size:.2f}" if isinstance(book, EBook) else ""
            self.tree.insert("", "end", values=(book.title, book.author, book.isbn, status, size))

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
