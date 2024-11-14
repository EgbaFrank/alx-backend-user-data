#!/usr/bin/env python3
"""Session authentication with expiration module
"""
from .session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Session authentication definitions"""
    def __init__(self):
        """Initialize"""
        super().__init__()
        try:
            self.session_duration = int(getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create session with expiration"""
        sess_id = super().create_session(user_id)

        if not sess_id:
            return None

        self.user_id_by_session_id[sess_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }

        return sess_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve user_id from session_id"""
        if not session_id:
            return None

        session_data = self.user_id_by_session_id.get(session_id)

        if not session_data:
            return None

        if self.session_duration <= 0:
            return session_data.get("user_id")

        created_at = session_data.get("created_at")

        if not created_at:
            return None

        expiration_time = created_at + timedelta(seconds=self.session_duration)

        if datetime.now() > expiration_time:
            return None

        return session_data.get("user_id")
