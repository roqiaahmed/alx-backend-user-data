#!/usr/bin/env python3
""" Module of Session database authentication
"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Session database authentication"""

    def create_session(self, user_id=None):
        """create session method"""
        session_id = super().create_session(user_id)
        UserSession({"user_id": user_id, "session_id": session_id})
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """user id for session id"""

    def destroy_session(self, request=None):
        """destroy session"""
