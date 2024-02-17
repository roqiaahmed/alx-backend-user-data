#!/usr/bin/env python3
""" Module of Auth seeeion
"""

from .auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """Session Auth class"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """create session"""
        if user_id is None or type(user_id) != str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """user id for session id"""
        if session_id is None or type(session_id) != str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """current user"""
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """destroy session"""
        session_id = self.session_cookie(request)
        if session_id == None or not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id == None or not User.get(user_id):
            return False
        del self.user_id_by_session_id[session_id]
        return True
