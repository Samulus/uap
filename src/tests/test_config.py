import unittest
from unittest import TestCase

from os.path import realpath, join, exists

import src.config

DEFAULT_CONFIG = {
    'host': '127.0.0.1',
    'port': 8080,
    'debug': False,
    'reloader': False,
    'login_required': False,
    'music_folder': None,
}

class UserDBTest(TestCase):
    def test_load_empty_path(self):
        self.assertIsNone(src.config.load_settings_dict())

    def test_cant_find_settings(self):
        EXAMPLE_INI = """
        host = 127.0.0.1
        port = 8080
        debug = False
        reloader = False
        login_required = True
        #music_folder = uncomment this, put your music folder here
        """
        CONFIG_PATH = realpath(join(__file__, "..", "config.ini"))
        src.config.load_settings_dict()
        with self.assertRaises(SyntaxError) :
            print("Missing [settings] at top of config.ini")



if __name__ == '__main__':
    unittest.main()