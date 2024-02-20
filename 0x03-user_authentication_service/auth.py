#!/usr/bin/env python3
"""
auth class
"""

import bcrypt


def _hash_password(password):
    bytes = password.encode()
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash
