import re
from database.connection import cursor, conn
import sqlite3

def title_formatter():
    words = re.split(r"[\s]+", title)
    final_title = []
    for word in words:
        if word.lower() not in ["of", "an", "the", "and"]:
            capitalized_word = word.capitalize()
        else:
            capitalized_word = word.lower()
        final_title.append(capitalized_word)
    
    return " ".join(final_title)

class Book:
    def __init__(self, title, author, copies=1):
        
        self._title = title_formatter(title)
        self._author = author
        self._copies = copies
        
        try:
            cursor.execute("INSERT INTO books (title, author, copies) VALUES (?, ?, ?)", (self._title, self._author, self._copies))
            conn.commit()
            self._id = cursor.lastrowid
            print(f"'{self._title}' successfully added to the database!")
        except sqlite3.IntegrityError as e:
            print(f"Error creating book: {e}")
    
    @classmethod
    def delete(title):
        """Delete current book from database."""
        new_title = title_formatter(title)
        try:
            cursor.execute("DELETE FROM books WHERE title = ?", (new_title,))
            conn.commit()
            print(f"The book '{new_title}' has been successfully deleted.")
        except Exception as e:
            print(f"Error deleting book: {e}")
            
    @classmethod
    def get_all(cls):
        try:
            cursor.execute("SELECT title, author, copies FROM books")
            books = cursor.fetchall()
            return books if books else []
        except sqlite3.IntegrityError as e:
            print(f"Error getting books: {e}") 
    
    @classmethod
    def find_by_id(cls, book_id):
        try:
            cursor.execute("SELECT id, title, author, copies FROM books WHERE id = ?", (book_id,))
            return cursor.fetchone()
        except sqlite3.IntegrityError as e:
            print(f"Error finding book: {e}")
    
    @classmethod
    def borrow(cls, book_id):
        try:
            cursor.execute("SELECT copies FROM books WHERE id = ?", (book_id))
            copies = cursor.fetchone()[0]
            if copies > 0:
                   cursor.execute("UPDATE books SET copies = copies - 1 WHERE id = ?", (book_id,))
                   conn.commit()
                   print(f"Book of id {book_id} borrowed.")
            else:
                print(f"Book of id {book_id} is not available for borrowing.")
        except sqlite3.IntegrityError as e:
            print(f"Error borrowing book, check id?: {e}")
            
    @classmethod
    def return_book(cls, book_id):
        cursor.execute("UPDATE books SET copies = copies + 1 WHERE id = ?", (book_id,))
        conn.commit()
        print(f"Book with id {book_id} returned.")
        
    def __repr__(self):
        return f"{self._title} by {self._author}, (Copies:{self._copiess})"
    