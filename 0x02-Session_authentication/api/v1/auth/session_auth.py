#!/usr/bin/env python3
""" Manage the API authentication """
from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """ Session Auth Class """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates a Session ID for a user_id """
        if not isinstance(user_id, str):
            return (None)
        session_id = uuid4()
        SessionAuth.user_id_by_session_id[str(session_id)] = user_id
        return (session_id)
