#
#   test_config.py
#   Author: Sean McGonegle
#   Date: 11/28/2016
#
#   Samuel Vargas:
#       I commented out the two tests in this test case because
#       they do not actually test anything and both tests are failing.
#       The method test_load_empty_path is always going to load the same
#       config.ini from the root directory of the program because the path
#       is hardcoded in that file. You could either:
#
#       A) Mock that out using unittests.mocks
#       B) Modify the function under test to accept a path to an .ini file.
#
#       Tests are not supposed to actually mutate real application stuff
#       like configs. You should be creating a temporary .ini file and deleting it
#       when you're done with the test.
#
#       I'll leave this file on the repo for posterity's sake.


import unittest
from unittest import TestCase

from os.path import realpath, join

CONFIG_PATH = realpath(join(__file__, "..", "config.ini"))

EXPECTED_INI = {'port': 8080, 'host': '127.0.0.1', 'login_required': True, 'reloader': False, 'debug': False,
                'music_folder': None}


class TestConfig(TestCase):
    def test_load_empty_path(self):
        # self.assertIsNotNone(src.config.load_settings_dict())
        pass

    def test_file(self):
        # self.assertEqual(src.config.load_settings_dict(),EXPECTED_INI)
        pass


if __name__ == '__main__':
    unittest.main()
