#!/usr/bin/env python3
"""
Module for filtering personal data from log messages.
"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Obfuscates specified fields in a log message.
    """
    return re.sub(rf'({"|".join(fields)})=[^{separator}]*', rf'\1={redaction}', message)
