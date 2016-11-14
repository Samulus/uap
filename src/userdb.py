#
#   userdb.py
#   Author: Samuel Vargas
#   Date: 11/14/2016
#
#   The UserDB module utilizes TinyDB to store a list of eve
#   in application in 
#   users and their misc account information. It contains information
#   like their Username, Account Status, Hashed Password, And Password
#   Salt.

from tinydb import TinyDB, Query
import os


class UserDB:
    DEFAULT_DB_PATH = os.path.realpath(os.path.join(__file__, "..", "db.json"))

    def __init__(self, db_path=DEFAULT_DB_PATH):
        self.db_path = db_path
        #raise NotImplementedError

    def add_user(self, username: str, password: bytes) -> bool:
        raise NotImplementedError

    def is_correct_password(self, username: str, password: bytes) -> bool:
        raise NotImplementedError

    def get_user_info(self):
        raise NotImplementedError

    def remove_user(self, username: str):
        raise NotImplementedError

