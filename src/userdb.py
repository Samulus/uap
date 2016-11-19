#
#   userdb.py
#   Author: Samuel Vargas
#   Date: 11/14/2016
#
#   The UserDB module utilizes TinyDB to store a list of users
#   in application in users and their misc account information.
#   It contains information like their Username, Account Status,
#   Hashed Password, And Password Salt.
#
#   TODO: Right now we're essentially using forever cookies that stay valid
#         until the user either A) Signs out, B) Signs in. This means that
#         someone could log in, wait a year, and then log back in with the
#         same cookie if they wanted to. It's a detail but it is important.

import base64
import copy
import os
from os.path import realpath, join

import scrypt
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage


def random_salt():
    return base64.encodebytes(os.urandom(24)).decode("utf8")


class UserDB:
    DB_PATH = realpath(join(__file__, "..", "database/users.json"))
    USER_SCHEMA = {'username': None,
                   'password': None,
                   'salt': None,
                   'playlists': [],
                   'account_type': 'user',
                   'session_id': None
                   }

    def __init__(self, db_path=DB_PATH, ram_db=False):
        if ram_db:
            self.__database = TinyDB(storage=MemoryStorage)
        else:
            self.__database = TinyDB(db_path)

    def add_user(self, username: str, password: str) -> bool:
        """
        Create and add a new user to the database. Note that
        a default session_id for every user is created and added
        to the database. There is no need to manually do it
        elsewhere.

        :param username: The username, should be verified before
                         this function is called.
        :param password: The password, should be verified before
                         this function is called. Will be salted
                         and hashed and then stored into the data
                         base.

        :returns:   If adding the user was successful or not.
        """

        # refuse to add a new user if another one exists already
        if self.find_user(username):
            return False

        # copy the schema, create the new user, insert them into database
        new_user = copy.deepcopy(UserDB.USER_SCHEMA)
        new_user['username'] = username
        new_user['salt'] = random_salt()
        new_user['session_id'] = random_salt()

        # create a bs64 string by hashing their password and salt
        # and encoding this as bs64, then store it in the db
        base64_password = UserDB.__create_password(password, new_user['salt'])
        new_user['password'] = base64_password
        self.__database.insert(new_user)
        return True

    def change_password(self, username: str, password: str) -> bool:
        # refuse to change password for non existent user
        user = self.find_user(username)
        if not user:
            return False

        # TODO verify that the users knows the old password to change
        # the new password

        # change the user's password and reset their session_id
        # they will have to log back in
        new_salt = random_salt()
        new_password = UserDB.__create_password(password, new_salt)
        new_session_id = random_salt()
        self.__database.update({'session_id': new_session_id,
                                'password': new_password,
                                'salt': new_salt},
                               eids=[user.eid])
        return True

    def log_user_out(self, username: str) -> bool:
        # sanity checking
        user = self.find_user(username)
        assert user is not None, \
            "We can't log a user who doesn't exist out"

        # reset their session id so their new requests become invalid
        # this forces them to log back in
        self.__database.update(
            {'session_id': random_salt()})

    def log_user_in(self, username: str, password_to_verify: str) -> bool:
        # can't login if you don't exist
        user = self.find_user(username)
        if user is None:
            return False

        # determine if their password is correct
        password_to_verify = scrypt.hash(password_to_verify, user['salt'])
        known_good_password = UserDB.__decode_password(user['password'],
                                                       user['salt'])

        # generate a new session_id on log in
        if password_to_verify == known_good_password:
            self.__database.update({'session_id': random_salt()},
                                   eids=[user.eid])
            return True

        # bad password
        else:
            return False

    def remove_user(self, username: str) -> bool:
        user = self.find_user(username)
        if user is not None:
            self.__database.remove(eids=[user.eid])
            return True
        return False

    def find_user(self, username):
        results = self.__database.search(Query().username == username)
        assert len(results) < 2, \
            "Two users cannot have the same username."
        return results[0] if len(results) == 1 else None

    def is_valid_session_id(self, session_id):
        results = self.__database.search(Query().session_id == session_id)
        assert len(results) < 2, \
            "Two users cannot have the same session_id."
        return len(results) == 1

    def get_user_session_id(self, username) -> str:
        user = self.find_user(username)
        return user['session_id'] if user is not None else None

    def create_new_user_session(self, session_id: str):
        results = self.__database.search(Query().session_id == session_id)
        assert len(results) < 2, \
            "Two users cannot have the same session_id."
        if len(results) != 1:
            return

        # get their ID and then give them a new session id
        eid = results[0].eid
        self.__database.update({"session_id": random_salt()},
                               eids=[eid])

    @staticmethod
    def __create_password(password=None, salt=None) -> str:
        if password is None or salt is None:
            raise ValueError("Password and Salt cannot be none.")
        return base64.encodebytes(scrypt.hash(password, salt)).decode('utf-8')

    @staticmethod
    def __decode_password(password=None, salt=None):
        if password is None or salt is None:
            raise ValueError("Password and Salt cannot be none.")
        return base64.decodebytes(password.encode('utf-8'))
