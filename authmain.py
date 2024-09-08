import regpage
import loginpage
import getpass

# Function to get user input
def get_user_input(prompt):
    return input(prompt)

if __name__ == "__main__":
    while True:
        print("1. Register")
        print("2. Login")
        print("3. Forgot Password")
        print("4. Exit")
        choice = get_user_input("Enter your choice: ")

        if choice == '1':
            username = get_user_input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            confirm_password = getpass.getpass("Confirm password: ")
            regpage.register_user(username, password, confirm_password)

        elif choice == '2':
            username = get_user_input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            loginpage.authenticate_user(username, password)

        elif choice == '3':
            username = get_user_input("Enter username: ")
            new_password = getpass.getpass("Enter new password: ")
            confirm_password = getpass.getpass("Confirm new password: ")
            loginpage.reset_password(username, new_password, confirm_password)

        elif choice == '4':
            break

        else:
            print("Invalid choice. Please try again.")