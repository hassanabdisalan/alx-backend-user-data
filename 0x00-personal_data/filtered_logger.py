#!/usr/bin/env python3
"""
Module for filtering personal data from log messages.
"""

import re
import logging
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Obfuscates specified fields in a log message.
    """
    return re.sub(rf'({"|".join(fields)})=[^{separator}]*', rf'\1={redaction}', message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize with fields to redact
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Redact sensitive fields in the log message
        """
        record.msg = filter_datum(self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)
        return super().format(record)
