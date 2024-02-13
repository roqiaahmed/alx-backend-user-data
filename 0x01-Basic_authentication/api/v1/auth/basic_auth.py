#!/usr/bin/env python3
""" Module of Auth class 
"""

from typing import List, TypeVar
from flask import request
from .auth import Auth


class BasicAuth(Auth):
    """Basic auth class"""
