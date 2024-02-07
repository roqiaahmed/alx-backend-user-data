#!/usr/bin/env python3

"""
Personal data
"""

from re import sub


def filter_datum(fields, redaction, message, separator):
    """
    filter_datum
    """
    for field in fields:
        res = sub(f"{field}=[^{separator}]+", f"{field}={redaction}", message)
    return res
