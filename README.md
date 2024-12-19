# Library Management System (SQLite) By Akanle Jeremy

This is a simple command-line library management system built using Python and the `sqlite3` module for database management. It allows librarians to manage books and users, and members to browse, borrow, and return books.

## Features

*   **User Management:**
    *   User registration with email validation.
    *   User login with password hashing (using bcrypt).
    *   Role-based access control (Librarian/Member).
    *   User account deletion.
    *   Email update functionality.
*   **Book Management:**
    *   Add new books to the collection.
    *   View all books.
    *   Search books by title.
    *   Search books by ID.
    *   Delete books.
    *   Borrow and return books (tracks copies available).
*   **Data Persistence:** Uses SQLite for local data storage using the `sqlite3` module.
*   **Clean Interface:** Simple and intuitive command-line interface.

## Technologies Used

*   Python 3.x
*   SQLite (Database)
*   bcrypt (Password hashing)

## Setup and Installation

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/](https://github.com/)<your_username>/<your_repo_name>.git
    cd <your_repo_name>
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    If you don't have a `requirements.txt` file, create one with `pip freeze > requirements.txt` after installing the necessary packages (`pip install bcrypt`).

4.  **Database:**

    The SQLite database file (`library.db`) is *already included* in the `database` folder. You *do not* need to create it manually.

## How to Run

```bash
python main.py
```
