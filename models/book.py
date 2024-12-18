import re
from database.connection import cursor, conn
import sqlite3

def title_formatter(title):
    words = re.split(r"[\s]+", title)
    final_title = []
    for i, word in enumerate(words):
        if word.lower() not in ["of", "an", "and", "the"] or i == 0:
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
        
    def create(self):
        try:
            cursor.execute("INSERT INTO books (title, author, copies) VALUES (?, ?, ?)", (self._title, self._author, self._copies))
            conn.commit()
            self._id = cursor.lastrowid
            print(f"'{self._title}' successfully added to the database!")
        except sqlite3.IntegrityError as e:
            print(f"Error creating book: {e}")
    
    @staticmethod
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
            result = cursor.fetchone()
            return result if result else print("Book not found.")
        except sqlite3.IntegrityError as e:
            print(f"Error finding book: {e}")
            
    @staticmethod
    def search(title):
        new_title = title_formatter(title)
        try:
            cursor.execute("SELECT title, author, copies, id FROM books WHERE title = ?", (new_title,))
            result = cursor.fetchone()
            if result:
                return result
            else:
                print(f"Book with title {title} not found.")
                return None
        except sqlite3.IntegrityError as e:
            print(f"Error finding book: {e}")
            
    @staticmethod
    def borrow(title):
        try:
            result = Book.search(title)
            if result[2] > 0:
                   cursor.execute("UPDATE books SET copies = copies - 1 WHERE title = ?", (result[3],))
                   conn.commit()
                   print(f"Book of id {result[3]}: {result[0]} borrowed.")
            else:
                print(f"Book of id {result[3]} is not available for borrowing.")
        except sqlite3.IntegrityError as e:
            print(f"Error borrowing book, check id?: {e}")
            
    @classmethod
    def return_book(cls, book_id):
        cursor.execute("UPDATE books SET copies = copies + 1 WHERE id = ?", (book_id,))
        conn.commit()
        print(f"Book with id {book_id} returned.")
        
    def __repr__(self):
        return f"{self._title} by {self._author}, (Copies:{self._copiess})"
    