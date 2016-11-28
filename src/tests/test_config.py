import unittest
from unittest import TestCase

import src.config
from configparser import ConfigParser
from os.path import realpath, join, exists

CONFIG_PATH = realpath(join(__file__, "..", "config.ini"))

EXPECTED_INI ={'port': 8080, 'host': '127.0.0.1', 'login_required': True, 'reloader': False, 'debug': False, 'music_folder': None}

class UserDBTest(TestCase):
    def test_load_empty_path(self):
        self.assertIsNotNone(src.config.load_settings_dict())

    def test_file(self):
        self.assertEqual(src.config.load_settings_dict(),EXPECTED_INI)

if __name__ == '__main__':
    unittest.main()