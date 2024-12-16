import re
from database.connection import cursor, conn
import sqlite3

def title_formatter():
    words = re.split(r"[\s]+", title)
    final_title = []
    for word in words:
        if word.lower() not in ["of", "the", "and"]:
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
        except sqlite3.IntegrityError as e:
            print(f"Error creating book: {e}")
        
    def delete(self):
        """Delete current book from database."""
        try:
            cursor.execute("DELETE FROM books WHERE id = ?", (self._id))
            conn.commit()
            print(f"Book with id {self._id} deleted.")
        except Exception as e:
            print(f"Error deleting book: {e}")
            
    
    