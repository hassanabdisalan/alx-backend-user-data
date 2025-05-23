#!/usr/bin/env python3
"""
encrypt_password.py
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt and returns the hashed password as bytes.

    Args:
        password (str): The plain text password to hash.

    Returns:
        bytes: The salted, hashed password.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates a password against a given hashed password using bcrypt.

    Args:
        hashed_password (bytes): The hashed password.
        password (str): The plain text password to validate.

    Returns:
        bool: True if the password matches the hashed password, False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
