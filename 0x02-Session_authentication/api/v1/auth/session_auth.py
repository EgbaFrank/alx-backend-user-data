#!/usr/bin/env python3
"""
Session authentication module
"""
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """Class for session authentication
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session id for a user"""
        if not user_id or not isinstance(user_id, str):
            return None

        sess_id = str(uuid4())
        self.user_id_by_session_id[sess_id] = user_id

        return sess_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieve a user_id based on session id"""
        if not session_id or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Retrieves User instance based on a cookie value"""
        if not request:
            return None

        sess_id = self.session_cookie(request)
        if not sess_id:
            return None

        user_id = self.user_id_for_session_id(sess_id)
        if not user_id:
            return None

        return User.get(user_id)

    def destroy_session(self, request=None):
        """deletes the user session"""
        if not request:
            return False

        sess_id = self.session_cookie(request)

        if not sess_id:
            return False

        user_id = self.user_id_for_session_id(sess_id)

        if not user_id:
            return False

        del self.user_id_by_session_id[sess_id]

        return True
