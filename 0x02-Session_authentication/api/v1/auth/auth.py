#!/usr/bin/env python3
""" Module of Auth class
"""

from typing import List, TypeVar
from flask import request
from os import getenv


class Auth:
    """Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require auth function"""
        if path is None or excluded_paths is None:
            return True
        for p in excluded_paths:
            if path[-1] != "/":
                path += "/"
            if p == path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorization header function"""
        if request is None:
            return None
        auth = request.headers.get("Authorization")
        return auth

    def session_cookie(self, request=None):
        "session cookie"
        if request is None:
            return None
        session_name = getenv("SESSION_NAME")
        return request.cookies.get(session_name)

    def current_user(self, request=None) -> TypeVar("User"):  # type: ignore
        """current user function"""
        return None
