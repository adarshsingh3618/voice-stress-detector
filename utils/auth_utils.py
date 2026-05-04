import json
import os

USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def signup(username, password):
    users = load_users()

    if username in users:
        return False, "User already exists"

    users[username] = password
    save_users(users)

    return True, "Signup successful"

def login(username, password):
    users = load_users()

    if username in users and users[username] == password:
        return True, "Login successful"

    return False, "Invalid credentials"