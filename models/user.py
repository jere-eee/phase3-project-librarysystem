from email.utils import parseaddr
import sqlite3
from database.connection import cursor, conn
import bcrypt

class User:
    def __init__(self, name, email, password, role="M"):
        """ Register a user. """
        if isinstance(name, str) and len(name) > 0:
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
        self._password_hash = self.hash_password(password)
        
    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    @staticmethod
    def verify_password(password, hashed):
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def create(self):
        try:
            cursor.execute("INSERT INTO users (name, email, role, password) VALUES (?, ?, ?, ?)", (self._name, self._email, self._role, self._password_hash))
            conn.commit()
            self._id = cursor.lastrowid
            print(f"{self._name} has been successfully registered!\nThey can now log in.")
        except sqlite3.IntegrityError as e:
            print(f"Error registering user: {e}")
    
    @staticmethod
    def get_all():
        """ Get all users and display."""
        try:
            cursor.execute("SELECT users.id, users.name, users.email, users.role FROM users")
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
            cursor.execute("SELECT users.id, users.name, users.email, users.role FROM users WHERE id = ?", (user_id,))
            result = cursor.fetchone()
            if result:
                return result
            else:
                raise Exception(f"User with passed id not found.")
        except sqlite3.IntegrityError as e:
            print(f'Error finding user: {e}')
            
    @staticmethod
    def search(name):
        try:
            cursor.execute("SELECT id, name, email, role FROM users WHERE name LIKE ?", (f"%{name}%",))
            result = cursor.fetchall()
            if result:
                return result
            else:
                print(f"No users found with name {name}.")
                return []
        except sqlite3.IntegrityError as e:
            print(f"Error finding user(s): {e}")
            return []
    
    def update_email(self, new_email):
        """Update the email of the current user."""
        name, addr = parseaddr(new_email)
        if "@" in addr and "." in addr.split("@")[-1]:
            try:
                cursor.execute("UPDATE users SET email = ? WHERE email = ?", (new_email, self._email))
                conn.commit()
                self._email = new_email
                print("Your email is successfully updated!")
            except sqlite3.IntegrityError as e:
                print(f"Error updating email: {e}")
        else:
            raise ValueError("Invalid email address.")
    
    def delete(self):
        """Delete current user from database."""
        try:
            cursor.execute("DELETE FROM users WHERE email = ?", (self._email,))
            conn.commit()
            print(f"You've successfully deleted your account.")
        except Exception as e:
            print(f"Error deleting user: {e}")
            
    @classmethod
    def login(cls, email, password):
        try:
            cursor.execute("SELECT users.name, users.email, users.password, users.role FROM users WHERE email = ?", (email,))
            result = cursor.fetchone()
            if result:
                email, password_hash = result[1], result[2]
                if cls.verify_password(password=password, hashed=password_hash):
                    return result
                else:
                    print("Invalid password. Try again.")
                    return None
            else:
                print("User not found.")
                return None
        except sqlite3.IntegrityError as e:
            print(f"Error logging in: {e}")
            return None
    
    def get_id(self):
        result = cursor.execute("SELECT id FROM users WHERE email = ?", (self._email,)).fetchone()
        if result:
            return result[0]
    
    def __repr__(self):
        return f"{self._name}, role: ({self._role})"