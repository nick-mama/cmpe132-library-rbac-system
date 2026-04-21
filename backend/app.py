from flask import Flask, request, jsonify
from flask_cors import CORS
import bcrypt
import json
import os

app = Flask(__name__)
CORS(app)

USERS_FILE = "users.json"

# Helper functions
def load_users():
    if not os.path.exists(USERS_FILE):
        return []

    try:
        with open(USERS_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except json.JSONDecodeError:
        return []

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def find_user(username):
    users = load_users()
    for user in users:
        if user["username"] == username:
            return user
    return None

# RBAC
ROLES = {
    "admin": ["add_user", "delete_user", "view_books"],
    "librarian": ["view_books", "manage_books"],
    "student": ["view_books"]
}

def check_permission(role, action):
    return action in ROLES.get(role, [])

# Routes
@app.route("/")
def home():
    return jsonify({"message": "Flask backend running"})

# Register
@app.route("/register", methods=["POST"])
def register():
    data = request.json

    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "student")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    if find_user(username):
        return jsonify({"error": "User already exists"}), 400

    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    new_user = {
        "username": username,
        "password": hashed_pw.decode("utf-8"),
        "role": role
    }

    users = load_users()
    users.append(new_user)
    save_users(users)

    return jsonify({"message": "User registered successfully"})

# Login
@app.route("/login", methods=["POST"])
def login():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    user = find_user(username)

    if not user:
        return jsonify({"error": "User not found"}), 404

    stored_hash = user["password"].encode("utf-8")

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

    if not username or not action:
        return jsonify({"error": "Username and action are required"}), 400

    user = find_user(username)

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

# Delete user
@app.route("/delete-user", methods=["POST"])
def delete_user():
    data = request.json
    username = data.get("username")

    if not username:
        return jsonify({"error": "Username is required"}), 400

    users = load_users()
    new_users = [user for user in users if user["username"] != username]

    if len(users) == len(new_users):
        return jsonify({"error": "User not found"}), 404

    save_users(new_users)
    return jsonify({"message": "User deleted successfully"})

# Run server
if __name__ == "__main__":
    app.run(debug=True)