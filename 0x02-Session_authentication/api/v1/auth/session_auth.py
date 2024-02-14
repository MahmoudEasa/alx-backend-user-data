#!/usr/bin/env python3
""" Manage the API authentication """
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """ Session Auth Class """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates a Session ID for a user_id """
        if not isinstance(user_id, str):
            return (None)
        session_id = str(uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return (session_id)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a User ID based on a Session ID """
        if not isinstance(session_id, str):
            return (None)

        return (SessionAuth.user_id_by_session_id.get(session_id))

    def current_user(self, request=None) -> TypeVar('User'):
        """  (overload) returns a User instance based on a cookie value """
        cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie)
        return (User.get(user_id))

    def destroy_session(self, request=None):
        """ Deletes the user session / logout """
        session_id = self.session_cookie(request)
        if not session_id:
            return (False)

        if not self.user_id_for_session_id(session_id):
            return (False)

        del self.user_id_by_session_id[session_id]
        return (True)
