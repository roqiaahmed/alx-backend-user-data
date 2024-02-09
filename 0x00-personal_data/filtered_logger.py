#!/usr/bin/env python3

"""
Module for handling Personal Data
"""

import re
from typing import List
import logging
from os import getenv
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """Filter datum function"""
    for field in fields:
        res = re.sub(f"{field}=[^{separator}]+", f"{field}={redaction}", message)
        message = res
    return res


def get_logger() -> logging.Logger:
    """Get logger function"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Get db function"""
    host_env = getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database_env = getenv("PERSONAL_DATA_DB_NAME")
    user_env = getenv("PERSONAL_DATA_DB_USERNAME", "root")
    pass_env = getenv("PERSONAL_DATA_DB_PASSWORD", "")

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
        return super(RedactingFormatter, self).format(record)


def main():
    """Main function"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    field_names = [i[0] for i in cursor.description]
    logger = get_logger()
    for row in cursor:
        info_answer = ""
        for k, r in zip(field_names, row):
            info_answer += f"{k}={r}; "
        logger.info(info_answer)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
