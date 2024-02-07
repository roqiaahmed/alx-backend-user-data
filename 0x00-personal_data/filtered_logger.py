#!/usr/bin/env python3

"""
Personal data
"""

from re import sub
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, separator: str):
    """
    filter_datum
    """
    for field in fields:
        message = sub(f"{field}=[^{separator}]+", f"{field}={redaction}", message)
    return message
