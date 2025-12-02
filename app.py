from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Read variables from .env (with defaults)
PORT = int(os.getenv("PORT", 5000))
HOST = os.getenv("HOST", "127.0.0.1")
DEBUG = os.getenv("DEBUG", "True") == "True"

app = Flask(__name__)

# Simple in-memory fake database
users = {
    1: {"name": "Hazem", "email": "hazem@example.com"},
    2: {"name": "Omar", "email": "omar@example.com"}
}

# ========== GET Requests ==========

@app.get("/users")
def get_users():
    print("[GET] Fetching all users...")
    return jsonify(users)

@app.get("/users/<int:user_id>")
def get_user(user_id):
    print(f"[GET] Fetching user with ID {user_id}...")
    user = users.get(user_id)
    return jsonify(user) if user else ("User not found", 404)

# ========== POST Request ==========

@app.post("/users")
def create_user():
    data = request.json
    print(f"[POST] Creating new user: {data}")

    new_id = max(users.keys()) + 1
    users[new_id] = data

    return jsonify({"message": "User created", "id": new_id}), 201

# ========== PUT Request ==========

@app.put("/users/<int:user_id>")
def update_user(user_id):
    data = request.json
    print(f"[PUT] Replacing user {user_id} with: {data}")

    if user_id not in users:
        return ("User not found", 404)

    users[user_id] = data
    return jsonify({"message": "User replaced", "user": users[user_id]})

# ========== PATCH Request ==========

@app.patch("/users/<int:user_id>")
def patch_user(user_id):
    data = request.json
    print(f"[PATCH] Updating part of user {user_id}: {data}")

    if user_id not in users:
        return ("User not found", 404)

    users[user_id].update(data)
    return jsonify({"message": "User updated", "user": users[user_id]})

# ========== DELETE Request ==========

@app.delete("/users/<int:user_id>")
def delete_user(user_id):
    print(f"[DELETE] Removing user {user_id}...")

    if user_id not in users:
        return ("User not found", 404)

    del users[user_id]
    return jsonify({"message": "User deleted"})

# ========== Run Server ==========

if __name__ == "__main__":
    print(f"Server running on http://{HOST}:{PORT}")
    app.run(host=HOST, port=PORT, debug=DEBUG)
