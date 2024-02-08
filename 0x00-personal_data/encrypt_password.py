#!/usr/bin/env python3

"""
Encrypting passwords
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hash password function"""
    bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Is valid check"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
