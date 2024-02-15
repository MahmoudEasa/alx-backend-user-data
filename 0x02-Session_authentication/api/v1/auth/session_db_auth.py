#!/usr/bin/env python3
""" Manage the API authentication """
from datetime import datetime, timedelta
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ Session DB Auth Class """
    def create_session(self, user_id=None) -> str:
        """ Creates and stores new instance of UserSession
            and returns the Session ID
        """
        session_id = super().create_session(user_id)
        if isinstance(session_id, str):
            user_session = UserSession(user_id=user_id, session_id=session_id)
            user_session.save()
            return (session_id)
        return (None)

    def user_id_for_session_id(self, session_id=None) -> str:
        """ Returns the User ID by requesting UserSession
            in the database based on session_id
        """
        try:
            sessions = UserSession.search({"session_id": session_id})
        except Exception:
            return (None)

        if not len(sessions):
            return (None)

        current_time = datetime.utcnow()
        created_at = sessions[0].created_at
        expire = created_at + timedelta(seconds=self.session_duration)
        if expire < current_time:
            return (None)
        return (sessions[0].user_id)

    def destroy_session(self, request=None) -> bool:
        """ Destroys the UserSession based on the Session ID
            from the request cookie
        """
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({"session_id": session_id})
        except Exception:
            return (False)

        if len(sessions):
            sessions[0].remove()
            return (True)

        return (False)
