#
#   test_userdb.py
#   Author: Steve Campbell
#   Date: 11/28/2016
#
#   This module is responsible for testing the userdb.py module
#   for bugs, security issues, and ease of use. It should ensure that
#   the userdb module is free from injection attacks / other security
#   problems etc.

import unittest
from src.userdb import UserDB


class UserDBTest(unittest.TestCase):
    def test_find_user(self):
        db = UserDB(ram_db=True)

        # Searching for user who is not in the  database
        self.assertIsNone(db.find_user("Fail"))

        # Searching for someone who is
        db.add_user("user123", "password123")
        self.assertIsNotNone(db.find_user("user123"))

    def test_add_user(self):
        db = UserDB(ram_db=True)

        # Check if the username already exists
        db.add_user("user123", "password123")
        self.assertFalse(db.add_user("user123", "password123"))

        # Check if a new user has been successfully added
        self.assertTrue(db.add_user("usert321", "password321"))

    def test_remove_user(self):
        db = UserDB(ram_db=True)

        # Removing someone that doesn't exist
        db.add_user("user123", "password123")
        self.assertFalse(db.remove_user("user321"))
        # Removing someone who does
        self.assertTrue(db.remove_user("user123"))

    def test_change_password(self):
        db = UserDB(ram_db=True)
        db.add_user("user123", "password123")

        # Change password of someone that doesn't exist
        self.assertFalse(db.change_password("user321", "password321"))

        # Change password of someone who does
        self.assertTrue(db.change_password("user123", "password321"))

        # Trying to change password to invalid password
        # TODO check to make sure new password is valid

    def test_log_user_in(self):
        db = UserDB(ram_db=True)
        db.add_user("user123", "password123")

        # Log in someone who does not exist
        self.assertFalse(db.log_user_in("user321", "password321"))

        # Log someone in who does exists
        self.assertTrue(db.log_user_in("user123", "password123"))

    def test_log_user_out(self):
        db = UserDB(ram_db=True)
        db.add_user("user123", "password123")
        db.log_user_in("user123", "password123")
        #id = db.get_user_session_id("user123")
        #db.create_new_user_session(id)

        db.log_user_out("user123")
        self.assertRaises(AssertionError, db.log_user_out, "user321")

    def test_get_user_session_id(self):
        db = UserDB(ram_db=True)
        db.add_user("user123", "password123")
        db.log_user_in("user123", "password123")

        # getting the session ID of someone who is logged in
        self.assertIsNotNone(db.get_user_session_id("user123"))

        # getting the session ID of someone who does not have an ID
        self.assertIsNone(db.get_user_session_id("user321"))


    def test_create_new_user_session(self):
        db = UserDB(ram_db=True)
        db.add_user("user123", "password123")
        db.log_user_in("user123", "password123")

        id = db.get_user_session_id("user123")

        # Create a session for someone that exists
        try:
            db.create_new_user_session(id)
        except AssertionError:
            self.fail("Fail 1")
        else:
            pass


    def test_is_valid_session_id(self):
        db = UserDB(ram_db=True)
        db.add_user("user123", "password123")
        db.log_user_in("user123", "password123")

        id = db.get_user_session_id("user123")

        try:
            db.is_valid_session_id(id)
        except AssertionError:
            self.fail("Fail 1")
        else:
            pass


    if __name__ == '__main__':
        unittest.main()