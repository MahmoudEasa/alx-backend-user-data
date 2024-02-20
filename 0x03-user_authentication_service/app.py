#!/usr/bin/env python3
"""App model
"""
from flask import Flask, jsonify, request
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def home():
    """GET /
        The home route
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'])
def register():
    """POST /users
        Register Users
    """
    email = request.form.get("email")
    if not email:
        return (jsonify({"error": "email is required."}), 400)
    password = request.form.get("password")
    if not password:
        return (jsonify({"error": "password is required."}), 400)

    try:
        user = AUTH.register_user(email, password)
        return (jsonify({"email": user.email, "message": "user created"}))
    except ValueError:
        return (jsonify({"message": "email already registered"}), 400)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
