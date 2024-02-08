#!/usr/bin/env python3

"""
Encrypting passwords
"""

import bcrypt
from typing import ByteString


def hash_password(password: str) -> ByteString:
    """Hash password function"""
    bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Is valid check"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
