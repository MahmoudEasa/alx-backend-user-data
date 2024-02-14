#!/usr/bin/env python3
""" Manage the API authentication """
from datetime import datetime, timedelta
from os import getenv
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """ Session expiration Class """
    def __init__(self) -> None:
        try:
            self.session_duration = int(getenv("SESSION_DURATION", 0))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None) -> str:
        """ (Overload) Create a Session ID by calling super() """
        session_id = super().create_session(user_id)
        if not session_id:
            return (None)

        self.user_id_by_session_id[session_id] = {
                "user_id": user_id,
                "created_at": datetime.now()
            }
        return (session_id)

    def user_id_for_session_id(self, session_id=None) -> str:
        """  Return user_id from the session dictionary """
        if not session_id:
            return (None)

        session_obj = super().user_id_for_session_id(session_id)
        if not session_obj:
            return (None)

        if self.session_duration <= 0:
            return (session_obj.get("user_id"))

        created_at = session_obj.get("created_at")
        expire = created_at + timedelta(seconds=self.session_duration)
        if expire < datetime.now():
            return (None)

        return (session_obj.get("user_id"))
