#!/usr/bin/env python3
""" Module for the database"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """Database class
    Methods: _session - Memoized session object to optimize the db functions
             add_user - Method to add user to the database
             find_user_by - Method to search for a userin the database
    """

    def __init__(self) -> None:
        """Initializes a new DB instance. """

        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """A method used to save a user to the database."""
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            new_user = None
        
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Method to find a user based on given arguments"""

        for key in kwargs:
            if key not in User.__table__.columns:
                raise InvalidRequestError

        user = self._session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound

        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Method to locate a user and update the user’s
        attributes as passed in the method’s arguments."""

        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError

        for key, val in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, val)
            else:
                raise ValueError
        
        self._session.commit()
