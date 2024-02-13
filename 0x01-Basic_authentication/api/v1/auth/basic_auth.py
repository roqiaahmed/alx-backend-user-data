#!/usr/bin/env python3
""" Module of Auth class 
"""

from typing import List, TypeVar
from flask import request
from .auth import Auth


class BasicAuth(Auth):
    """Basic auth class"""

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """extract base64 authorization header"""
        header = str(authorization_header).split(" ")
        # print(f"===========>{header[0]}")
        if authorization_header and header[0] == "Basic":
            return authorization_header[6:]
        return None
