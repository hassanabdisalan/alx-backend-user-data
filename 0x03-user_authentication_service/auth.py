#!/usr/bin/env python3
"""Authentication module"""

import bcrypt
from db import DB
from user import User
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """Hashes a password with a salt using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a new UUID and return its string representation."""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user if they don't exist"""
        try:
            if self._db.find_user_by(email=email):
                raise ValueError(f"User {email} already exists")
        except Exception:
            hashed_pwd = _hash_password(password)
            return self._db.add_user(email, hashed_pwd)

        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """Validates login credentials"""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)
        except Exception:
            return False

    def create_session(self, email: str) -> Union[str, None]:
        """Creates a session ID for the user and returns it"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception:
            return None
