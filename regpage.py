import csv
import hashlib
from pymongo import MongoClient
import os

# Function to hash the password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to write users to a CSV file
def write_users_to_csv(users, filename='users.csv'):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["username", "password"])
        for user in users:
            writer.writerow([user['username'], user['password']])

# Function to read users from a CSV file
def read_users_from_csv(filename='users.csv'):
    users = []
    if os.path.exists(filename):
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                users.append(row)
    return users

# Function to upload the CSV file to MongoDB as binary
def upload_csv_to_mongodb(filename='users.csv'):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['user_database']
    collection = db['users_csv']
    
    with open(filename, 'rb') as csvfile:
        binary_data = csvfile.read()

    collection.update_one({}, {"$set": {"file": binary_data}}, upsert=True)

# Function to download the CSV file from MongoDB
def download_csv_from_mongodb(filename='users.csv'):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['user_database']
    collection = db['users_csv']
    
    document = collection.find_one()
    if document and 'file' in document:
        with open(filename, 'wb') as csvfile:
            csvfile.write(document['file'])

# Function to register a user
def register_user(username, password, confirm_password):
    if password != confirm_password:
        print("Passwords do not match!")
        return

    hashed_password = hash_password(password)
    users = read_users_from_csv()

    # Check if username already exists
    if any(user['username'] == username for user in users):
        print("Username already exists!")
        return

    users.append({"username": username, "password": hashed_password})
    write_users_to_csv(users)
    upload_csv_to_mongodb()
    
    print("User registered successfully!")
