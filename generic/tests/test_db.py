#!/usr/bin/env python3


import unittest
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
DB = __import__('db').DB
User = __import__('user').User


class DB_test(unittest.TestCase):
    """Tests for the database."""

    my_db = DB()

    def test_add_user(self):
        """Test if the function takes in 2 strings and returns a 
        User object with correct email and hashed_password fields
        """

        user_1 = DB_test.my_db.add_user("test0@test.com", "SuperHashedPwd0")
        user_2 = DB_test.my_db.add_user("test1@test.com", "SuperHashedPwd1")

        self.assertEqual(user_1.id, 1)
        self.assertEqual(user_2.id, 2)
        self.assertEqual(user_1.email, "test0@test.com")
        self.assertEqual(user_2.hashed_password, "SuperHashedPwd1")

    def test_find_user_by(self):
        """Test if the function finds the correct user and returns the 
        correct error message if it doesn't. """

        user = DB_test.my_db.add_user("test2@test.com", "SuperHashedPwd2")
        
        found_user = DB_test.my_db.find_user_by(email="test2@test.com")

        self.assertEqual(found_user.id, user.id)
        self.assertRaises(NoResultFound, DB_test.my_db.find_user_by,
                          email="test@test.com")
        self.assertRaises(InvalidRequestError, DB_test.my_db.find_user_by,
                         emall="test0@test.com")

    def test_update_user(self):
        """Test if the function updates user's information correctly."""

        user = DB_test.my_db.add_user("test3@test.com", "SuperHashedPwd3")

        DB_test.my_db.update_user(user.id, hashed_password="Newpass")

        self.assertEqual(user.hashed_password, "Newpass")
        self.assertRaises(ValueError, DB_test.my_db.update_user,
                          user.id, hashed_pwd="Newpass")
