#!/usr/bin/env python3
"""
filtered_logger.py
"""

import logging
import re
import os
import mysql.connector
from typing import List
from mysql.connector.connection import MySQLConnection


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Returns the log message obfuscated with redaction for PII fields"""
    for field in fields:
        message = re.sub(
            f"{field}=.*?{separator}",
            f"{field}={redaction}{separator}",
            message
        )
    return message


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(
            self.fields,
            self.REDACTION,
            record.getMessage(),
            self.SEPARATOR
        )
        return super().format(record)


def get_logger() -> logging.Logger:
    """Creates and configures a logger"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))

    logger.addHandler(stream_handler)
    return logger


def get_db() -> MySQLConnection:
    """Connects to a MySQL database using environment variables"""
    return mysql.connector.connect(
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        database=os.getenv("PERSONAL_DATA_DB_NAME")
    )


def main() -> None:
    """Main function that fetches user data and logs it with redaction"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()

    fields = [i[0] for i in cursor.description]  # column names

    for row in cursor:
        record = "; ".join(f"{field}={value}" for field, value in zip(fields, row)) + ";"
        logger.info(record)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
