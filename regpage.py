import hashlib
from pymongo import MongoClient
import getpass

# Function to hash the password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to register a user
def register_user(username, password, confirm_password):
    if password != confirm_password:
        print("Passwords do not match!")
        return

    hashed_password = hash_password(password)

    # Connect to MongoDB
    client = MongoClient('mongodb+srv://userData:sihdata2024@techtitans.jnat6.mongodb.net/')
    db = client['userData']
    collection = db['users']

    # Check if username already exists
    if collection.find_one({"username": username}):
        print("Username already exists!")
        return

    # Insert user data into MongoDB
    user_data = {
        "username": username,
        "password": hashed_password
    }
    collection.insert_one(user_data)
    
    print("User registered successfully!")

# Function to get user input
def get_user_input():
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")  # Hides input for password
    confirm_password = getpass.getpass("Confirm password: ")  # Hides input for password
    return username, password, confirm_password

if __name__ == "__main__":
    username, password, confirm_password = get_user_input()
    register_user(username, password, confirm_password)
