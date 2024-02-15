#!/usr/bin/env python3
""" Module of Auth class
"""

from .auth import Auth
import binascii
import base64
from typing import Tuple, TypeVar
from models.user import User


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

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar("User"):  # type: ignore
        """user object from credentials"""
        if (
            not user_email
            or type(user_email) != str
            or not user_pwd
            or type(user_pwd) != str
        ):
            return None
        try:
            user = User.search({"email": user_email})
            if not user or not user[0].is_valid_password(user_pwd):
                return None
            return user[0]
        except Exception as e:
            return None

    def current_user(self, request=None) -> TypeVar("User"):  # type: ignore
        """current user"""
        auth_header = self.authorization_header(request)
        if not auth_header:
            return None

        incode_auth = self.extract_base64_authorization_header(auth_header)
        if not incode_auth:
            return None

        decode_auth = self.decode_base64_authorization_header(incode_auth)
        if not decode_auth:
            return None

        email, pwd = self.extract_user_credentials(decode_auth)

        if not email or not pwd:
            return None

        user = self.user_object_from_credentials(email, pwd)

        return user
