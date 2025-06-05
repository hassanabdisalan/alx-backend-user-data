#!/usr/bin/env python3
"""
Authentication module that provides methods for user authentication,
registration, session management, and password reset functionality.
"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt with salt.
    
    Args:
        password: The password to hash.
    
    Returns:
        The salted hash of the password as bytes.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


def _generate_uuid() -> str:
    """Generate a new UUID.
    
    Returns:
        A string representation of the generated UUID.
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    
    Provides methods for user registration, login validation,
    session management, and password reset functionality.
    """

    def __init__(self):
        """Initialize a new Auth instance."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user with email and password.
        
        Args:
            email: The email of the user.
            password: The password of the user.
        
        Returns:
            The newly created User object.
        
        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user login credentials.
        
        Args:
            email: The email of the user.
            password: The password to validate.
        
        Returns:
            True if the credentials are valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Create a new session for a user.
        
        Args:
            email: The email of the user.
        
        Returns:
            The session ID if successful, None otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Get user from session ID.
        
        Args:
            session_id: The session ID to look up.
        
        Returns:
            The corresponding User object if found, None otherwise.
        """
        if session_id is None:
            return None
        
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy a user's session.
        
        Args:
            user_id: The ID of the user.
        """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generate a reset password token.
        
        Args:
            email: The email of the user requesting a password reset.
        
        Returns:
            The generated reset token.
        
        Raises:
            ValueError: If no user with the given email exists.
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Update user's password using reset token.
        
        Args:
            reset_token: The reset token for verification.
            password: The new password.
        
        Raises:
            ValueError: If the reset token is invalid.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(user.id,
                                hashed_password=hashed_password,
                                reset_token=None)
        except NoResultFound:
            raise ValueError
