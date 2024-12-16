from email.utils import parseaddr
import sqlite3
from database.connection import cursor, conn

class User:
    def __init__(self, name, email):
        """ Register a user. """
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
        except sqlite3.IntegrityError as e:
            print(f"Error registering user: {e}")
    
    @classmethod
    def all():
        """ Get all users and display."""
        try:
            cursor.execute("SELECT users.name, users.email FROM users")
            result = cursor.fetchall()
            if result:
                return [user[0] for user in result]
            else:
                print("No users in the database")
        except sqlite3.IntegrityError as e:
            print(f"Error accessing users from database: {e}")
            
    def find_by_id(self):
        try:
            cursor.execute("SELECT users.name, users.email FROM users WHERE id = ?", (self._id,))
            result = cursor.fetchone()
            if result:
                return result
            else:
                raise Exception(f"User {self._name} with id:{self._id} not found.")
        except sqlite3.IntegrityError as e:
            print(f'Error finding user: {e}')
    
    def update_email(self, new_email):
        """Update the email of the current user."""
        name, addr = parseaddr(new_email)
        if "@" in addr and "." in addr.split("@")[-1]:
            self._email = new_email
            try:
                cursor.execute("UPDATE users SET email = ? WHERE id = ?", (self._email, self._id))
                conn.commit()
            except sqlite3.IntegrityError as e:
                print(f"Error updating email: {e}")
        else:
            raise ValueError("Invalid email address.")
        
    def delete(self):
        """Delete current user from database."""
        try:
            cursor.execute("DELETE FROM users WHERE id = ?", (self._id))
            conn.commit()
            print(f"User {self._name} deleted.")
        except Exception as e:
            print(f"Error deleting user {self._name}: {e}")