from flask import Flask, request, jsonify, Response
from bson.json_util import dumps
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Load environment variables
PORT = int(os.getenv("PORT", 5000))
MONGO_URI = os.getenv("MONGO_URI")

# Connect to MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client["flaskdb"]          # database name
users = db["users"]             # collection name


# ---------------------------
#        ROUTES
# ---------------------------

@app.route("/api/users", methods=["GET"])
def get_users():
    print("GET request received")
    data = list(users.find({}, {"_id": 0}))
    return jsonify(data)


@app.route("/api/users", methods=["POST"])
def create_user():
    body = request.json
    result = users.insert_one(body)
    body["_id"] = result.inserted_id

    return Response(
        response=dumps({"message": "User created", "data": body}),
        mimetype="application/json"
    )


@app.route("/api/users/<name>", methods=["PUT"])
def replace_user(name):
    print("PUT request received")
    body = request.json
    users.replace_one({"name": name}, body)
    return jsonify({"message": "User replaced", "data": body})


@app.route("/api/users/<name>", methods=["PATCH"])
def update_user(name):
    print("PATCH request received")
    body = request.json
    users.update_one({"name": name}, {"$set": body})
    return jsonify({"message": "User updated", "data": body})


@app.route("/api/users/<name>", methods=["DELETE"])
def delete_user(name):
    print("DELETE request received")
    users.delete_one({"name": name})
    return jsonify({"message": "User deleted"})


# Run server
if __name__ == "__main__":
    print(f"Server running on port {PORT}")
    app.run(port=PORT, debug=True)
