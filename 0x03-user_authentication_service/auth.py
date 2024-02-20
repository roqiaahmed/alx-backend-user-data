#!/usr/bin/env python3
"""
auth class
"""

import uuid
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password):
    bytes = password.encode()
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(bytes, salt)
    return hashed_password


def _generate_uuid() -> str:
    return uuid()


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """init method"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register user method"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """valid login method"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                userBytes = password.encode("utf-8")
                return bcrypt.checkpw(userBytes, user.hashed_password)
            return False
        except NoResultFound:
            return False
