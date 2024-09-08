import csv
import hashlib
import os

# Function to hash the password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to register a user
def register_user(username, password, confirm_password):
    if password != confirm_password:
        print("Passwords do not match!")
        return

    hashed_password = hash_password(password)
    user_data = [username, hashed_password]

    # Write to CSV file
    with open('C:\\Users\\Harkiran\\Documents\\SIH-24\\SIH-24\\users.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(user_data)

    # Convert CSV to binary
    with open('C:\\Users\\Harkiran\\Documents\\SIH-24\\SIH-24\\users.csv', 'rb') as csvfile:
        binary_data = csvfile.read()
    
    with open('C:\\Users\\Harkiran\\Documents\\SIH-24\\SIH-24\\users_binary.csv', 'wb') as binaryfile:
        binaryfile.write(binary_data)
    
    print("User registered successfully!")

# Function to get user input
def get_user_input():
    username = input("Enter username: ")
    password = input("Enter password: ")
    confirm_password = input("Confirm password: ")
    return username, password, confirm_password

if __name__ == "__main__":
    username, password, confirm_password = get_user_input()
    register_user(username, password, confirm_password)
