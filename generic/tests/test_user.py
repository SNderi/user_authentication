#!/usr/bin/env python3


import unittest
User = __import__('user').User


print("{} class exists and it contains {} table.".format(User.__name__,
      User.__tablename__))


class TestUser(unittest.TestCase):
    """Test for the user model"""

    def test_properties(self):
        """Test that correct properties were set."""
        correct_result = {'email': 'VARCHAR(250)',
                          'hashed_password': 'VARCHAR(250)',
                          'id': 'INTEGER',
                          'reset_token': 'VARCHAR(250)',
                          'session_id': 'VARCHAR(250)'
                          }
        result = {}
        col_by_name = {}
        for column in User.__table__.columns:
            col_by_name[column.description] = column.type

        col_keys = col_by_name.keys()
        for col_key in sorted(col_keys):
            result[col_key] = str(col_by_name[col_key])

        self.assertEqual(result, correct_result)
