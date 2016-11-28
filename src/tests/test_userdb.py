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


class UserDBTest(unittest.TestCase):
    def test_add_user(self):
        raise NotImplementedError

    def test_avoid_adding_duplicate_user(self):
        raise NotImplementedError

    def test_get_user_info(self):
        raise NotImplementedError

    def test_is_correct_password(self):
        raise NotImplementedError

    def test_remove_user(self):
        raise NotImplementedError

    def test_injection_attacks(self):
        raise NotImplementedError

    def test_change_password(self):
        raise NotImplementedError
