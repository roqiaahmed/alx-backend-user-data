#!/usr/bin/env python3

"""
Module for handling Personal Data
"""

from re import sub
from typing import List
import logging
from os import environ
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """filter_datum function"""
    for field in fields:
        res = sub(f"{field}=[^{separator}]+", f"{field}={redaction}", message)
        message = res
    return res


def get_logger():
    """get_logger function"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)
    return logger


def get_db():
    """get_db function"""
    host_env = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    database_env = environ.get("PERSONAL_DATA_DB_NAME")
    user_env = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    pass_env = environ.get("PERSONAL_DATA_DB_PASSWORD", "")

    db = mysql.connector.connect(
        host=host_env,
        database=database_env,
        user=user_env,
        password=pass_env,
    )
    return db


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
