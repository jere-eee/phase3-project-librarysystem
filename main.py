import sys
from models.book import Book
from models.user import User
from database.connection import cursor, conn


current_user = None
def librarian_menu():
    global current_user
    while True:
        print(f"Welcome, {current_user}!")
        print("\n1.Add book to collection\n2.View all books\n3.Find Book by Title\n4.Find Book by ID\n5.Delete book\n6.View all users\n7.Find user by name/id\n8.Exit")
        
        choice = input("Pick a number to manage the library: ")
        
        if choice == "1":
            title = input("Enter Book Title: ")
            author = input("Enter author name: ")
            copies = input("How many copies? ")
            book = Book(title, author, copies)
            book.create()
        elif choice == "2":
            result = Book.get_all()
            if result:
                for r in result:
                    print(f"ID: {r[3]}, Title: {r[0]}, Author: {r[1]}, Copies: {r[2]}")
        elif choice == "3":
            title = input("Enter book title: ")
            result = Book.search(title)
            print(f"ID: {result[3]}, Title: {result[0]}, Author: {result[1]}, Copies: {result[2]}")
        elif choice == "4":
            id = input("Enter book id: ")
            book = Book.find_by_id(id)
            print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Copies: {book[3]}")
        
        elif choice == "5":
            title = input("Enter book title: ")
            result = Book.search(title)
            if result:
                sure = input(f"Are you sure you'd like to delete {result}? (y/n)").strip().lower()
                if sure == "y":
                    Book.delete(title)
        elif choice == "6":
            result = User.get_all()
            for r in result:
                print(f"ID: {r[0]}, Name: {r[1]}, Email: {r[2]}, Role: {r[3]}")
        elif choice == "7":
            by = input("Would you like to search by name or id? (n for name/i for id) ").strip().lower()
            if by == "n":
                name = input("Enter username: ")
                result = User.search(name)
                if result:
                    for r in result:
                        print(f"ID: {r[0]}, Name: {r[1]}, Email: {r[2]}, Role: {r[3]}")
                else:
                    print("No users found.")
            elif by == "i":
                user_id = input("Enter user id: ")
                result = User.find_by_id(user_id)
                if result:
                    print(f"ID: {result[0]}, Name: {result[1]}, Email: {result[2]}, Role: {result[3]}")
            else:
                print("Please pick either n for name or i for id.")
        elif choice == "8":
            sys.exit()
def menu():
    global current_user
    while True:
        print(f"Welcome, {current_user}!")
        print("\n1.View all books\n2.Find book by title\n3.Borrow book\n4.Return book\n5.Update my email\n6.Delete my account\n7.Exit")
        choice = input("Pick a number and explore: ")
            
        if choice == "1":
            result = Book.get_all()
            if result:
                for r in result:
                    print(f"ID: {r[3]}, Title: {r[0]}, Author: {r[1]}, Copies: {r[2]}")
        
        elif choice == "2":
            title = input("Enter book title: ")
            result = Book.search(title)
            print(f"ID: {result[3]}, Title: {result[0]}, Author: {result[1]}, Copies: {result[2]}")
        
        elif choice == "3":
            title = input("Enter book title: ")
            user_id = current_user.get_id()
            Book.borrow(title, user_id)
        
        elif choice == "4":
            title = input("Enter book title: ")
            user_id = current_user.get_id()
            Book.return_book(title, user_id)
        elif choice == "5":
            new_email = input("Type out your new email: ")
            current_user.update_email(new_email=new_email)
            
        elif choice == "6":
            confirm = input("Are you sure you'd like to delete your account? (y/n) ").lower()
            if confirm == "y":
                current_user.delete()
                current_user = None
                main()
        elif choice == "7":
            sys.exit()

def main():
    global current_user
    while True:
        print("\n1.Register User\n2.Login\n3.Exit")
        choice = input("Welcome To The Library System, Select an Option: ")
        
        if choice == "1":
            name = input("Enter name: ")
            email = input("Enter a valid email address: ")
            role = input("State role: Member(M) or Librarian(L) ").strip().capitalize()
            password = input("Enter password: ")
            confirm_password = input("Confirm password: ")
            if password == confirm_password:
                user = User(name, email, password, role)
                user.create()
            else:
                print("Passwords must match to continue.")
            logged = input(f"Would you like to log in as {user}? (y/n) ").lower()
            if logged == "y":
                current_user = user
                if current_user._role == "M":
                    menu()
                else:
                    librarian_menu()
        elif choice == "2":
            email = input("Enter your email address: ")
            password = input("Enter password: ")
            
            result = User.login(email=email, password=password)
            if result:
                print(f"{result[0]} successfully logged in!")
                current_user = User(name=result[0], email=result[1], password=result[2], role=result[3])
                if current_user._role == "M":
                    menu()
                else:
                    librarian_menu()
            else:
                print("Invalid credentials or error in logging in.")
        
        elif choice == "3":
            sys.exit()
            
if __name__ == "__main__":
    main()