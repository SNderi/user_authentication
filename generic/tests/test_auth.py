#!/usr/bin/env python3
"""Unittest module for auth."""

import unittest
import uuid

User = __import__('user').User
Auth = __import__('auth').Auth

_hash_password = __import__('auth')._hash_password
_generate_uuid = __import__('auth')._generate_uuid


class test_auth(unittest.TestCase):
    """Class for auth tests"""

    my_auth = Auth()

    def test_hash_password(self):
        """Check if _hash_password encrypts the password. """

        hash_pass = _hash_password("Madagascar")
        self.assertIsInstance(hash_pass, bytes)

    def test_register_user(self):
        """Test if register user adds a user to the database if and only
        if the user isn't already registered."""

        new_user = self.my_auth.register_user("test4@test.com", "Algiers")
        self.assertIsInstance(new_user, User)
        self.assertRaises(ValueError, self.my_auth.register_user,
                          "test4@test.com", "Algiers")

    def test_valid_login(self):
        """Check if user validation works properly."""

        self.my_auth.register_user("test5@test.com", "Mozambique")
        self.assertTrue(self.my_auth.valid_login("test5@test.com",
                        "Mozambique"))
        self.assertFalse(self.my_auth.valid_login("test5@test.com",
                         "Mozambiq"))
        self.assertFalse(self.my_auth.valid_login("test0@test.com",
                         "Mozambique"))

    def test_generate_uuid(self):
        """Check if it generates a random uuid."""

        rand = _generate_uuid()
        self.assertIsInstance(rand, str)
        t_rand = uuid.UUID(rand)
        self.assertIsInstance(t_rand, uuid.UUID)

    def test_get_user_from_session_id(self):
        """Check if the method can find user given a session id"""

        self.my_auth.register_user("test6@test.com", "Zimbabwe")
        sess_id = self.my_auth.create_session("test6@test.com")

        user = self.my_auth.get_user_from_session_id(sess_id)

        self.assertIsNotNone(user)
        self.assertIsInstance(user, User)

        self.assertIsNone(self.my_auth.get_user_from_session_id("bla-01bla"))

    def test_get_reset_password_token(self):
        """Test if it generates a reset token. """

        self.my_auth.register_user("test7@test.com", "Gabon")

        token = self.my_auth.get_reset_password_token("test7@test.com")

        self.assertIsInstance(token, str)
        self.assertIsInstance(uuid.UUID(token), uuid.UUID)

        self.assertRaises(ValueError, self.my_auth.get_reset_password_token,
                          "tester@test.com")

    def test_update_password(self):
        """Test if the method correctly updates user password """

        user = self.my_auth.register_user("test8@test.com", "Mauritania")

        token = self.my_auth.get_reset_password_token("test8@test.com")
        self.assertIsNotNone(user.reset_token)
        self.assertTrue(self.my_auth.valid_login("test8@test.com",
                        "Mauritania"))

        self.my_auth.update_password(token, "Nouakchott")
        self.assertTrue(self.my_auth.valid_login("test8@test.com",
                        "Nouakchott"))
        self.assertIsNone(user.reset_token)
