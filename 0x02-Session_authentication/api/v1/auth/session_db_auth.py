#!/usr/bin/env python3
"""Persistant session module
"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """Persistant session definitions"""
    def create_session(self, user_id=None):
        """Create and store user session"""
        sess_id = super().create_session(user_id)
        user_sess = UserSession(user_id=user_id, session_id=sess_id)
        user_sess.save()

        return sess_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve user_id from stored session"""
        if not session_id or not isinstance(session_id, str):
            return None

        try:
            user_sessions = UserSession.search({'session_id': session_id})
        except KeyError:
            return None

        if not user_sessions:
            return None

        user_sess = user_sessions[0]

        if self.session_duration <= 0:
            return user_sess.user_id

        created_at = user_sess.created_at

        expiration_time = created_at + timedelta(seconds=self.session_duration)

        if datetime.now() > expiration_time:
            return None

        return user_sess.user_id

    def destroy_session(self, request=None):
        """Destorys a session"""
        sess_id = self.session_cookie(request)
        try:
            user_sessions = UserSession.search({'session_id': sess_id})
        except KeyError:
            return False

        if not user_sessions:
            return False

        user_sess = user_sessions[0]

        user_sess.remove()
        return True
