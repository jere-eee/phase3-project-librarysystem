from email.utils import parseaddr
import sqlite3
from database.connection import cursor, conn

class User:
    def __init__(self, name, email, role="M"):
        """ Register a user. """
        if isinstance(name, str):
            self._name = name
        else:
            raise ValueError("Name must be a string.")
        name, addr = parseaddr(email)
        if "@" in addr and "." in addr.split("@")[-1]:
            self._email = email
        else:
            raise ValueError("Invalid email address. Must have a valid username and domain.") 
        if role == "M" or role == "L":
            self._role = role
        else:
            raise ValueError("Invalid role. Must be either 'M'(member) or 'L'(librarian).") 
        try:
            cursor.execute("INSERT INTO users (name, email, role) VALUES (?, ?, ?)", (self._name, self._email, self._role))
            conn.commit()
            self._id = cursor.lastrowid
            print(f"{self._name} has been successfully registered!\nThey can now log in.")
        except sqlite3.IntegrityError as e:
            print(f"Error registering user: {e}")
    
    @classmethod
    def all():
        """ Get all users and display."""
        try:
            cursor.execute("SELECT users.name, users.email FROM users")
            result = cursor.fetchall()
            if result:
                return result
            else:
                print("No users in the database")
        except sqlite3.IntegrityError as e:
            print(f"Error accessing users from database: {e}")
            
    @staticmethod
    def find_by_id(user_id):
        """Finds and returns user by id if exists."""
        try:
            cursor.execute("SELECT users.name, users.email, users.role FROM users WHERE id = ?", (user_id,))
            result = cursor.fetchone()
            if result:
                return result
            else:
                raise Exception(f"User with passed id not found.")
        except sqlite3.IntegrityError as e:
            print(f'Error finding user: {e}')
    
    def update_email(self, new_email):
        """Update the email of the current user."""
        name, addr = parseaddr(new_email)
        if "@" in addr and "." in addr.split("@")[-1]:
            self._email = new_email
            try:
                cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, self._id))
                conn.commit()
                print("User ")
            except sqlite3.IntegrityError as e:
                print(f"Error updating email: {e}")
        else:
            raise ValueError("Invalid email address.")
        
    def delete(self):
        """Delete current user from database."""
        try:
            cursor.execute("DELETE FROM users WHERE id = ?", (self._id))
            conn.commit()
            print(f"User with id {self._id} deleted.")
        except Exception as e:
            print(f"Error deleting user: {e}")
            
    @classmethod
    def login(cls, email, role):
        try:
            cursor.execute("SELECT user.name, user.role FROM users WHERE email = ? AND role = ?", (email, role))
            return cursor.fetchone()        
        except sqlite3.IntegrityError as e:
            print(f"Error logging in: {e}")
    
    @staticmethod
    def count():
        pass