#!/usr/bin/env python3
""" Module of Auth class
"""

from .auth import Auth
import binascii
import base64
from typing import Tuple


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

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> Tuple[str, str]:
        """extract user credentials"""
        u_credential = str(decoded_base64_authorization_header).split(":")
        if (
            not decoded_base64_authorization_header
            or type(decoded_base64_authorization_header) != str
            or len(u_credential) == 1
        ):
            return (None, None)
        return tuple(u_credential)
