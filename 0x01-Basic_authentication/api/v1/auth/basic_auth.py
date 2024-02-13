#!/usr/bin/env python3
""" Module of Auth class 
"""

from .auth import Auth
import base64, binascii


class BasicAuth(Auth):
    """Basic auth class"""

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """extract base64 authorization header"""
        header = str(authorization_header).split(" ")
        if authorization_header and header[0] == "Basic":
            return authorization_header[6:]
        return None

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """decode base64 authorization header"""
        if (
            base64_authorization_header is None
            or type(base64_authorization_header) != str
        ):
            return None
        try:
            data = base64.b64decode(base64_authorization_header, validate=True)
            return data.decode("utf-8")
        except binascii.Error as e:
            return None
