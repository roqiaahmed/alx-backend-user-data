#!/usr/bin/env python3

"""
Personal data
"""

from re import sub
from typing import List
import logging


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """filter_datum"""
    for field in fields:
        res = sub(f"{field}=[^{separator}]+", f"{field}={redaction}", message)
        message = res
    return res


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """format"""
        record.msg = filter_datum(
            self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR
        )
        print(super(RedactingFormatter, self).format(record))
