# Library Management System - Moneykicks Library

This is a Python-based Library Management System using SQLite3 to manage books, students, and track borrowed items. The application allows students to borrow, return, donate, list, and delete books from the library. It also keeps track of which books are currently borrowed.

## Features
* List all available books: Displays all books that are available in the library.
* Borrow books: Allows students to borrow available books. The borrowed book is tracked.
* Return books: Allows students to return borrowed books, updating their status to 'available'.

* Donate books: Allows students to donate books to the library.
* Track borrowed books: Displays the list of books that are currently borrowed and who has borrowed them.
* Delete books: Allows deleting a book from the library, removing it from both the book collection and the tracking system.

### Requirements
* Python 3.x
*SQLite3 (comes pre-installed with Python)
* Installation Instructions
* Clone this repository to your local machine or download the source code as a ZIP file.
*bash
* Copy code
* git clone https://github.com/your-username/library-management-system.git

#### Navigate to the project directory:
* bash
* Copy code
* cd library-management-system
* Ensure you have Python 3.x installed (SQLite3 is included in Python standard libraries).
* Run the Python script to start the application:
* bash
* Copy code
python library_system.py
Usage
Upon running the program, you'll see a menu of options to choose from:

List all available books: Shows a list of all books that are available in the library.
Borrow books: Prompts you to enter your name and the book you wish to borrow. If the book is available, it is marked as borrowed.
Return books: Prompts you to enter your name and the book you wish to return. It updates the status of the book to available.
Donate books: Allows you to donate a book to the library, which is added to the available collection.
Track borrowed books: Displays a list of books that have been borrowed and the students who borrowed them.
Delete books: Allows you to delete a book from the library. If it's borrowed, it will be removed from both the books list and the borrowed books list.
Exit the library: Exits the program.
Example Interaction
sql
Copy code
Welcome to the Moneykicks Library!

CHOOSE WHAT YOU WANT TO DO:
1. Listing all books
2. Borrow books
3. Return books
4. Donate books
5. Track books
6. Delete a book
7. Exit the library

Enter your choice: 1
♦-- The Song of Achilles
♦-- The Body Keeps the Score
♦-- The Last House on Needless Street
♦-- Becoming
♦-- Educated
♦-- The House in the Cerulean Sea
♦-- Atomic Habits
♦-- Sapiens: A Brief History of Humankind
♦-- The Silent Patient
♦-- The Couple Next Door
Database Schema
The system uses an SQLite database (library.db) with the following two tables:

books: Stores book names and their availability status.

name: Name of the book (TEXT)
status: Status of the book (TEXT) - "available" or "borrowed"
track: Tracks which books are borrowed and by which student.

student_name: Name of the student borrowing the book (TEXT)
book_name: Name of the book borrowed (TEXT)
Code Explanation
Library Class: Manages the books and their statuses. Handles adding, borrowing, returning, donating, and deleting books from the library. It also tracks borrowed books.

Student Class: Allows students to interact with the system by borrowing, returning, and donating books.

SQLite Database: All data is stored in an SQLite database (library.db). The database includes two tables: books and track.

##### To Do / Future Enhancements
* Implement a login system for students (authentication and user management).
* Add a due date feature for borrowed books and fine management.
* Add a feature to search for books by name, genre, or author.
* Improve the UI with a graphical interface (Tkinter or similar library).

###### License
This project is licensed under the MIT License - see the LICENSE file for details.

