from flask import Flask, request, jsonify
from flask_cors import CORS
import bcrypt
import json
import os

app = Flask(__name__)
CORS(app)

# File used to store user data
USERS_FILE = "users.json"

# Load users from the JSON file
def load_users():
    # If file doesn't exist, return an empty list
    if not os.path.exists(USERS_FILE):
        return []

    try:
        with open(USERS_FILE, "r") as f:
            content = f.read().strip()
            # If file is empty, return an empty list
            if not content:
                return []
            return json.loads(content)
    except json.JSONDecodeError:
        # If file has invalid JSON, return an empty list
        return []

# Find single user by username, return None if not found
def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def find_user(username):
    users = load_users()
    for user in users:
        if user["username"] == username:
            return user
    return None

# RBAC permission map
# Each role has a list of actions they are allowed to perform
ROLES = {
    "admin": ["add_user", "delete_user", "view_books"],
    "librarian": ["view_books", "manage_books"],
    "student": ["view_books"]
}

# Check if given role has permission to perform the action
def check_permission(role, action):
    return action in ROLES.get(role, [])

# Home route to confirm server is running
@app.route("/")
def home():
    return jsonify({"message": "Flask backend running"})

# Register new user w/ username, password, and role
@app.route("/register", methods=["POST"])
def register():
    data = request.json

    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "student")

    # Both fields are filled out
    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    # Check if user already exists
    if find_user(username):
        return jsonify({"error": "User already exists"}), 400

    # Hash the password before storing
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    # Build new user object
    new_user = {
        "username": username,
        "password": hashed_pw.decode("utf-8"),
        "role": role
    }

    # Add new user and save file
    users = load_users()
    users.append(new_user)
    save_users(users)

    return jsonify({"message": "User registered successfully"})

# Login to exisitng user account veryifying password
@app.route("/login", methods=["POST"])
def login():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    user = find_user(username)

    # Return error if user doesn't exist
    if not user:
        return jsonify({"error": "User not found"}), 404

    stored_hash = user["password"].encode("utf-8")

    # Compare given password against stored hash
    if bcrypt.checkpw(password.encode("utf-8"), stored_hash):
        return jsonify({
            "message": "Login successful",
            "role": user["role"]
        })
    else:
        return jsonify({"error": "Invalid password"}), 401

# Authorization check
@app.route("/check-permission", methods=["POST"])
def permission():
    data = request.json

    username = data.get("username")
    action = data.get("action")

    # Both fields needed
    if not username or not action:
        return jsonify({"error": "Username and action are required"}), 400

    user = find_user(username)

    # Return error if user doesn't exist
    if not user:
        return jsonify({"error": "User not found"}), 404

    role = user["role"]
    allowed = check_permission(role, action)

    return jsonify({
        "username": username,
        "role": role,
        "action": action,
        "allowed": allowed
    })

# Delete user by username
@app.route("/delete-user", methods=["POST"])
def delete_user():
    data = request.json
    username = data.get("username")

    # Username needed to delete
    if not username:
        return jsonify({"error": "Username is required"}), 400

    users = load_users()
    # Filter out user to be deleted
    new_users = [user for user in users if user["username"] != username]

    # If list length is unchanged, user was not found
    if len(users) == len(new_users):
        return jsonify({"error": "User not found"}), 404

    save_users(new_users)
    return jsonify({"message": "User deleted successfully"})

# Start Flask development server
if __name__ == "__main__":
    app.run(debug=True)