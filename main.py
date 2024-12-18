import sys
from models.user import User
from database.connection import cursor, conn


current_user = None

def menu():
    global current_user
    while True:
        print(f"Welcome, {current_user}!")
        print("\n1.View all users\n2.Find user by id\n3.Update my email\n4.Delete my account\n5.Exit")
        choice = input("Pick a number and explore: ")
        
        if choice == "1":
            result = User.get_all()
            for r in result:
                print(r)
        
        elif choice == "2":
            id = input("Enter user id: ")
            result = User.find_by_id(id)
            print(result)
            
        elif choice == "3":
            new_email = input("Type out your new email: ")
            current_user.update_email(new_email=new_email)
            
        elif choice == "4":
            confirm = input("Are you sure you'd like to delete your account? (y/n) ").lower()
            if confirm == "y":
                current_user.delete()
                current_user = None
                main()
        elif choice == "5":
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
                menu()
        
        elif choice == "2":
            email = input("Enter your email address: ")
            password = input("Enter password: ")
            
            result = User.login(email=email, password=password)
            if result:
                print(f"{result[0]} successfully logged in!")
                current_user = User(name=result[0], email=result[1], password=result[2], role=result[3])
                menu()
            else:
                print("Invalid credentials or error in logging in.")
        
        elif choice == "3":
            sys.exit()
            
if __name__ == "__main__":
    main()