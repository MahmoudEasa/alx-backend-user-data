#!/usr/bin/env python3
"""Auth model
"""
from typing import Union
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """ Return bytes hash of the input password """
    return (bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()))


def _generate_uuid() -> str:
    """ Generate UUID """
    return (str(uuid.uuid4()))


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

    def valid_login(self, email: str, password: str) -> bool:
        """ Validate email and password """
        try:
            user = self._db.find_user_by(email=email)
            return (bcrypt.checkpw(
                password.encode('utf-8'), user.hashed_password))
        except Exception:
            return (False)

    def create_session(self, email: str) -> str:
        """ Create Session """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user.session_id = session_id
            self._db.update_user(user.id, session_id=session_id)
            return (session_id)
        except Exception:
            return (None)
        
    def get_user_from_session_id(self, session_id: str) -> Union[User | None]:
        """ Get User from Session ID """
        try:
            return (self._db.find_user_by(session_id=session_id))
        except Exception:
            return (None)
