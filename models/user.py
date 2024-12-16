from email.utils import parseaddr
from database.connection import cursor, conn

class User:
    def __init__(self, name, email):
        if isinstance(name, str):
            self._name = name
        else:
            raise ValueError("Name must be a string.")
        name, addr = parseaddr(email)
        if "@" in addr and "." in addr.split("@")[-1]:
            self._email = email
        else:
            raise ValueError("Invalid email address. Must be a valid username and domain email string.") 
        
        try:
            cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (self._name, self._email))
            conn.commit()
            self._id = cursor.lastrowid
        except Exception as e:
            print(f"Error registering user: {e}")