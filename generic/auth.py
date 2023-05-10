#!/usr/bin/env python3
"""Module to handle user authentication"""

import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User
from uuid import uuid4


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Adds user to the database.
        Args: email
              password
        Return: User
        Raises: Valuerror if user already exists
        """

        try:
            user = self._db.find_user_by(email=email)
            raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            passwd = _hash_password(password)
            user = self._db.add_user(email, passwd)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates user login credentials"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """Retuns a session id for user associated with that email."""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_id = _generate_uuid()
                self._db.update_user(user.id, session_id=session_id)
                return user.session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Method to find user by their session id"""
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Method to delete user session on logout. """
        try:
            self._db.update_user(user_id, session_id=None)
            return None
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Generates a token for password resets. """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        token = _generate_uuid()
        self._db.update_user(user.id, reset_token=token)
        return user.reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates the user's hashed password. """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        hash_password = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hash_password,
                             reset_token=None)
        return None


def _hash_password(password: str) -> bytes:
    """Hashes password using bcrypt.
    Args: password: str - password to encrypt
    Returns: Salted hash password: bytes
    """

    pbytes = password.encode('utf-8')
    salt = bcrypt.gensalt()

    return bcrypt.hashpw(pbytes, salt)


def _generate_uuid() -> str:
    """Generates a string representation of a UUID"""

    return str(uuid4())
