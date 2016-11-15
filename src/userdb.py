#
#   userdb.py
#   Author: Samuel Vargas
#   Date: 11/14/2016
#
#   The UserDB module utilizes TinyDB to store a list of eve
#   in application in users and their misc account information.
#   It contains information like their Username, Account Status,
#   Hashed Password, And Password Salt.

from tinydb import TinyDB, Query
import os
import crypt
import copy
import scrypt
import base64


class UserDB:
    DB_PATH = os.path.realpath(os.path.join(__file__, "..", "database/users.json"))
    USER_SCHEMA = {'username': None, 'password': None, 'salt': None, 'playlists': None}

    def __init__(self, db_path=DB_PATH):
        self.__database = TinyDB(db_path)

    def add_user(self, username: str, password: str) -> bool:
        """
        Add a new user to the database, sets their information and hashes
        their password for storage.

        :param username: The username, should be verified before this function is called.
        :param password: The password, should be verified before this function is called.
                         Will be HASHED using scrypt and then stored in the database.
        """
        if self.user_exists(username):
            return False
        new_user = copy.deepcopy(UserDB.USER_SCHEMA)
        new_user['username'] = username
        new_user['salt'] = crypt.mksalt(crypt.METHOD_SHA512)
        new_user['password'] = UserDB.__generate_hashed_b64_password(
            password=password, salt=new_user['salt'])
        new_user['playlists'] = []
        self.__database.insert(new_user)
        return True

    def is_correct_password(self, username: str, password_to_verify: str) -> bool:
        if not self.user_exists(username):
            return False
        results = self.__database.search(Query().username == username)
        user = results[0]
        password_to_verify = scrypt.hash(password_to_verify, user['salt'])
        known_good_password = UserDB.__decode_hashed_b64_password(user['password'], user['salt'])
        return password_to_verify == known_good_password

    def get_user_info(self):
        raise NotImplementedError

    def remove_user(self, username: str) -> bool:
        raise NotImplementedError

    def user_exists(self, username) -> bool:
        search_count = len(self.__database.search(Query().username == username))
        assert search_count < 2, "It should be impossible to have two users with the same username."
        return search_count == 1

    @staticmethod
    def __generate_hashed_b64_password(password=None, salt=None) -> str:
        if password is None or salt is None:
            raise ValueError("userdb.py: Password and Salt cannot be none.")
        return base64.encodebytes(scrypt.hash(password, salt)).decode('utf-8')

    @staticmethod
    def __decode_hashed_b64_password(password=None, salt=None):
        if password is None or salt is None:
            raise ValueError("userdb.py: Password and Salt cannot be none.")
        return base64.decodebytes(password.encode('utf-8'))

    @staticmethod
    def __are_b64_passwords_equal(p1: str, p2: str):
        return base64.decodebytes(p1) == base64.decodebytes(p2)


if __name__ == '__main__':
    # example usage
    x = UserDB()
    x.add_user("Karen",  "GOAT 🐐 GOAT")
    if x.is_correct_password("Karen", "GOAT 🐐 GOAT"):
        print("Correct Password")
    else:
        print("Wrong Password")