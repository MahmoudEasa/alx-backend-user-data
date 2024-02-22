#!/usr/bin/env python3
"""App model
"""
from flask import Flask, jsonify, request, abort, redirect, url_for
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
        Register User
        Return: {"email": user.email, "message": "user created"}
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


@app.route("/sessions", methods=['POST'])
def login():
    """POST /sessions
        Login
    """
    email = request.form.get("email")
    if not email:
        return (jsonify({"error": "email is required."}), 400)
    password = request.form.get("password")
    if not password:
        return (jsonify({"error": "password is required."}), 400)

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        res = jsonify({"email": email, "message": "logged in"})
        res.set_cookie("session_id", session_id)
        return (res)
    else:
        abort(401)


@app.route("/sessions", methods=['DELETE'])
def logout():
    """DELETE /sessions
        Logout
    """
    session_id = request.cookies.get("session_id")
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return (redirect(url_for('home')))
    abort(403)


@app.route("/profile")
def profile():
    """GET /profile
        Profile
    """
    session_id = request.cookies.get("session_id")
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return (jsonify({"email": user.email}), 200)
    abort(403)


@app.route("/reset_password", methods=['POST'])
def get_reset_password_token():
    """POST /reset_password
        Reset Password
    """
    email = request.form.get("email")
    if email:
        try:
            reset_token = AUTH.get_reset_password_token(email)
            return (jsonify({"email": email, "reset_token": reset_token}), 200)
        except ValueError:
            abort(403)


@app.route("/reset_password", methods=['PUT'])
def update_password():
    """PUT /reset_password
        Reset Password
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    if email and reset_token and new_password:
        try:
            AUTH.update_password(reset_token, new_password)
            return (jsonify({"email": email,
                             "message": "Password updated"}), 200)
        except Exception:
            abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
