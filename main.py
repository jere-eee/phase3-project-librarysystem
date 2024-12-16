import sys
from models.user import User

current_user = None

def main():
    while True:
        print("\n1.Register User\n2.Login\n3.Exit")
        choice = input("Welcome To The Library System, Select an Option: ")
        
        if choice == "1":
            name = input("Enter name: ")
            email = input("Enter a valid email address: ")
            role = input("State role: Member(M) or Librarian(L) ")
            user = User(name, email, role)
            current_user = user
            print(current_user)
        
        if choice == "3":
            sys.exit()
            
if __name__ == "__main__":
    main()