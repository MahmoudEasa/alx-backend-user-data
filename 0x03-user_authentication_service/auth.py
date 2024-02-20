#!/usr/bin/env python3
"""Auth model
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ Return bytes hash of the input password """
    return (bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()))


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Register User """
        try:
            self._db.find_user_by(email=email)
            raise (ValueError(f"User {email} already exists"))
        except NoResultFound:
            hash_pass = _hash_password(password)
            return (self._db.add_user(email, hash_pass))
