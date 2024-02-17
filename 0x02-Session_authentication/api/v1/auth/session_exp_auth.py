#!/usr/bin/env python3
""" Module of Session exp authentication views
"""
from .session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Session Exp Auth class"""

    def __init__(self):
        """init method"""
        s_duration = int(getenv("SESSION_DURATION"))
        if not s_duration or type(s_duration) != int:
            self.session_duration = 0
        self.session_duration = s_duration

    def create_session(self, user_id=None):
        """create session method"""
        try:
            s_id = super().create_session(user_id)
            session_dictionary = {"user_id": user_id, "created_at": datetime.now()}
            self.user_id_by_session_id[s_id] = session_dictionary
            return s_id
        except:
            return None

    def user_id_for_session_id(self, session_id=None):
        """user id for session id"""
        if session_id == None or not self.user_id_by_session_id.get(session_id):
            return None
        if self.session_duration <= 0:
            return self.user_id_by_session_id[session_id].get("user_id")
        created_at = self.user_id_by_session_id[session_id].get("created_at")
        if not created_at:
            return None
        expiry_time = created_at + timedelta(seconds=self.session_duration)
        current_time = datetime.now()
        if expiry_time < current_time:
            return None
        return self.user_id_by_session_id[session_id].get("user_id")
