from email.utils import parseaddr
from database.connection import cursor, conn
import sqlite3

class Author:
    def __init__(self, name, email):
        if isinstance(name, str) and len(name) > 0:
            self._name = name
        else:
            raise ValueError("Name must be a string.")

        name, addr = parseaddr(email)
        if "@" in addr and "." in addr.split("@")[-1]:
            self._email = email
        else:
            raise ValueError("Invalid email address. Must have a valid username and domain.") 

        try:
            cursor.execute("INSERT INTO authors (name, email) VALUES (?, ?)", (self._name, self._email, self._role))
            conn.commit()
            self._id = cursor.lastrowid
            print(f"{self._name} has been successfully registered!")
        except sqlite3.IntegrityError as e:
            print(f"Error registering author: {e}")
        