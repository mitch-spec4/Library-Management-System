from sqlalchemy import create_engine, func, ForeignKey, Table, Column, Integer, String, DateTime, MetaData
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import random
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)
Base = declarative_base(metadata=metadata)

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    status = Column(String)

    @property
    def is_available(self):
        return self.status == 'available'

    @classmethod
    def create(cls, session, name, status='available'):
        book = cls(name=name, status=status)
        session.add(book)
        session.commit()
        return book

    @classmethod
    def delete(cls, session, book_id):
        book = session.query(cls).filter_by(id=book_id).first()
        if book:
            session.delete(book)
            session.commit()
            return True
        return False

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, book_id):
        return session.query(cls).filter_by(id=book_id).first()

class Track(Base):
    __tablename__ = 'track'
    id = Column(Integer, primary_key=True)
    student_name = Column(String)
    book_name = Column(String, ForeignKey('books.name'))

    @classmethod
    def create(cls, session, student_name, book_name):
        track = cls(student_name=student_name, book_name=book_name)
        session.add(track)
        session.commit()
        return track

    @classmethod
    def delete(cls, session, track_id):
        track = session.query(cls).filter_by(id=track_id).first()
        if track:
            session.delete(track)
            session.commit()
            return True
        return False

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, track_id):
        return session.query(cls).filter_by(id=track_id).first()

class User(Base):
    __tablename__ = 'users'
    username = Column(String, primary_key=True)
    password = Column(String)

    @classmethod
    def create(cls, session, username, password):
        user = cls(username=username, password=password)
        session.add(user)
        session.commit()
        return user

    @classmethod
    def delete(cls, session, username):
        user = session.query(cls).filter_by(username=username).first()
        if user:
            session.delete(user)
            session.commit()
            return True
        return False

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, username):
        return session.query(cls).filter_by(username=username).first()

class Library:
    def __init__(self):
        self.engine = create_engine('sqlite:///library.db')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.initialize_books()

    def initialize_books(self):
        popular_books = [
            ("The Seven Husbands of Evelyn Hugo", "available"),
            ("Where the Crawdads Sing", "available"),
            ("The Midnight Library", "available"),
            ("The Circle", "available"),
            ("The Song of Achilles", "available"),
            ("Educated", "available"),
            ("Becoming", "available"),
            ("Atomic Habits", "available"),
            ("The Body Keeps the Score", "available"),
            ("Sapiens: A Brief History of Humankind", "available"),
            ("The Silent Patient", "available"),
            ("The Last House on Needless Street", "available"),
            ("The Couple Next Door", "available"),
            ("The Priory of the Orange Tree", "available"),
            ("Project Hail Mary", "available"),
            ("The House in the Cerulean Sea", "available"),
            ("Big Little Lies", "available"),
            ("Normal People", "available"),
            ("The Night Circus", "available"),
            ("Little Fires Everywhere", "available")
        ]
        
        selected_books = random.sample(popular_books, 10)
        for name, status in selected_books:
            if not self.session.query(Book).filter_by(name=name).first():
                Book.create(self.session, name=name, status=status)

    def displayAvailableBooks(self):
        books = self.session.query(Book).filter_by(status='available').all()
        return [book.name for book in books]

    def displayBorrowedBooks(self):
        books = self.session.query(Book).filter_by(status='borrowed').all()
        return [book.name for book in books]

    def borrowBook(self, name, bookname):
        book = self.session.query(Book).filter_by(name=bookname, status='available').first()
        if not book:
            return False
        Track.create(self.session, student_name=name, book_name=bookname)
        book.status = 'borrowed'
        self.session.commit()
        return True

    def returnBook(self, bookname):
        track = self.session.query(Track).filter_by(book_name=bookname).first()
        if track:
            book = self.session.query(Book).filter_by(name=bookname).first()
            book.status = 'available'
            self.session.delete(track)
            self.session.commit()
            return True
        return False

    def donateBook(self, bookname):
        Book.create(self.session, name=bookname, status='available')

    def deleteBook(self, bookname):
        book = self.session.query(Book).filter_by(name=bookname).first()
        if book:
            self.session.delete(book)
            self.session.query(Track).filter_by(book_name=bookname).delete()
            self.session.commit()
            return True
        return False

    def registerUser(self, username, password):
        if self.session.query(User).filter_by(username=username).first():
            return False
        User.create(self.session, username=username, password=password)
        return True

    def loginUser(self, username, password):
        user = self.session.query(User).filter_by(username=username, password=password).first()
        return user is not None

class LibraryApp:
    def __init__(self, root, library):
        self.library = library
        self.root = root
        self.root.title("Moneykicks Library")

        self.frame = tk.Frame(root, bg="#f0f0f0")
        self.frame.pack(padx=20, pady=20)

        self.label = tk.Label(self.frame, text="Welcome to the Moneykicks Library", font=("Helvetica", 16), bg="#f0f0f0")
        self.label.pack(pady=10)

        self.login_or_register()

    def login_or_register(self):
        choice = simpledialog.askstring("Login or Register", "Type 'login' to log in or 'register' to create a new account:")
        if choice == 'login':
            self.login()
        elif choice == 'register':
            self.register()
        else:
            messagebox.showerror("Error", "Invalid choice. Please restart the application.")
            self.root.destroy()

    def login(self):
        username = simpledialog.askstring("Login", "Enter your username:")
        password = simpledialog.askstring("Login", "Enter your password:", show='*')
        if self.library.loginUser(username, password):
            messagebox.showinfo("Success", "Logged in successfully!")
            self.show_main_menu(username)
        else:
            messagebox.showerror("Error", "Invalid username or password.")
            self.root.destroy()

    def register(self):
        username = simpledialog.askstring("Register", "Enter a username:")
        password = simpledialog.askstring("Register", "Enter a password:", show='*')
        if self.library.registerUser(username, password):
            messagebox.showinfo("Success", f"Account created successfully! Welcome, {username}!")
            self.show_main_menu(username)
        else:
            messagebox.showerror("Error", "Username already exists. Please restart the application.")
            self.root.destroy()

    def show_main_menu(self, username):
        self.label.config(text=f"Welcome, {username}!")
        self.list_books_button = ttk.Button(self.frame, text="List Available Books", command=self.list_books)
        self.list_books_button.pack(pady=5)

        self.borrow_book_button = ttk.Button(self.frame, text="Borrow Book", command=self.borrow_book)
        self.borrow_book_button.pack(pady=5)

        self.return_book_button = ttk.Button(self.frame, text="Return Book", command=self.return_book)
        self.return_book_button.pack(pady=5)

        self.donate_book_button = ttk.Button(self.frame, text="Donate Book", command=self.donate_book)
        self.donate_book_button.pack(pady=5)

        self.delete_book_button = ttk.Button(self.frame, text="Delete Book", command=self.delete_book)
        self.delete_book_button.pack(pady=5)

        self.borrowed_books_button = ttk.Button(self.frame, text="Show Borrowed Books", command=self.show_borrowed_books)
        self.borrowed_books_button.pack(pady=5)

    def list_books(self):
        books = self.library.displayAvailableBooks()
        messagebox.showinfo("Available Books", "\n".join(books))

    def show_borrowed_books(self):
        books = self.library.displayBorrowedBooks()
        messagebox.showinfo("Borrowed Books", "\n".join(books))

    def borrow_book(self):
        name = simpledialog.askstring("Borrow Book", "Enter your name:")
        bookname = simpledialog.askstring("Borrow Book", "Enter the name of the book:")
        if self.library.borrowBook(name, bookname):
            messagebox.showinfo("Success", "Book borrowed successfully!")
        else:
            messagebox.showerror("Error", "Book is not available.")

    def return_book(self):
        bookname = simpledialog.askstring("Return Book", "Enter the name of the book:")
        if self.library.returnBook(bookname):
            messagebox.showinfo("Success", "Book returned successfully!")
        else:
            messagebox.showerror("Error", "No such book is currently issued.")

    def donate_book(self):
        bookname = simpledialog.askstring("Donate Book", "Enter the name of the book:")
        self.library.donateBook(bookname)
        messagebox.showinfo("Success", "Book donated successfully!")

    def delete_book(self):
        bookname = simpledialog.askstring("Delete Book", "Enter the name of the book:")
        if self.library.deleteBook(bookname):
            messagebox.showinfo("Success", "Book deleted successfully!")
        else:
            messagebox.showerror("Error", "Book does not exist in the library.")

if __name__ == "__main__":
    library = Library()
    root = tk.Tk()
    app = LibraryApp(root, library)
    root.mainloop()