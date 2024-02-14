#!/usr/bin/env python3
""" Module of Session Auth views
"""
from os import getenv
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def login() -> str:
    """ POST /auth_session/login
    Return:
        - Dictionary representation of the User
    """
    email = request.form.get('email')
    if not email:
        return (jsonify({"error": "email missing"}), 400)
    password = request.form.get('password')
    if not password:
        return (jsonify({"error": "password missing"}), 400)

    user = User.search({"email": email})
    if not user:
        return (jsonify({"error": "no user found for this email"}), 404)

    user = user[0]
    if not user.is_valid_password(password):
        return (jsonify({"error": "wrong password"}), 401)

    from api.v1.app import auth
    session = auth.create_session(user.id)
    res = jsonify(user.to_json())
    res.set_cookie(getenv('SESSION_NAME'), session)
    return (res)


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout() -> str:
    """ Deleting the Session ID contains in the request as cookie """
    """ DELETE /auth_session/login
    Return:
        - Dictionary representation of the User
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return (jsonify({}), 200)
