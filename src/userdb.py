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

#         We should probably set a 15-20 min timelimit on sessions and require
#         the user's client to ping us every so often so we know to keep their
#         connection alive.


from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage
import os
import crypt
import copy
import scrypt
import base64


class UserDB:
    DB_PATH = os.path.realpath(os.path.join(__file__, "..", "database/users.json"))
    USER_SCHEMA = {'username': None,  # username of the client
                   'password': None,  # scrypt hashed password
                   'salt': None,  # salt for user
                   'playlists': [],  # list of their playlists
                   'account_type': 'user',  # account type
                   'session_id': None  # their session_id (stored in a hmac cookie clientside)
                   }

    def __init__(self, db_path=DB_PATH, use_debug_db=False):
        self.__database = TinyDB(db_path) if not use_debug_db else TinyDB(storage=MemoryStorage)

    def add_user(self, username: str, password: str) -> bool:
        """
        Create and add a new user to the database. Note that
        a default session_id for every user is created and added
        to the database. There is no need to manually do it
        elsewhere.

        :param username: The username, should be verified before
                         this function is called.
        :param password: The password, should be verified before this function is called.
                         Will be HASHED using scrypt and then stored in the database.
                         as a base64 encoded string.
        :returns:   If adding the user was successful or not.
        """

        # refuse to add a new user if another one exists already
        if self.find_user(username):
            return False

        # otherwise copy the schema, create the new user, insert them into database
        new_user = copy.deepcopy(UserDB.USER_SCHEMA)
        new_user['username'] = username
        new_user['salt'] = crypt.mksalt(crypt.METHOD_SHA512)
        new_user['session_id'] = crypt.mksalt(crypt.METHOD_SHA512)
        new_user['password'] = UserDB.__generate_hashed_b64_password(password, new_user['salt'])
        self.__database.insert(new_user)
        return True

    def change_password(self, username: str, password: str) -> bool:
        # TODO: ensure we redirect the user to the login page '/' again when this is called
        user = self.find_user(username)

        # refuse to change password for non existent user
        if not user:
            return False

        # change the user's password and reset their session_id, forcing them to relogin
        new_salt = crypt.mksalt(crypt.METHOD_SHA512)
        new_password = UserDB.__generate_hashed_b64_password(password, new_salt)
        new_session_id = crypt.mksalt(crypt.METHOD_SHA512)
        self.__database.update({'session_id': new_session_id, 'password': new_password, 'salt': new_salt},
                               eids=[user.eid])
        return True

    def log_user_out(self, username: str) -> bool:
        # sanity checking
        user = self.find_user(username)
        assert user is not None, "We can't log a user who doesn't exist out"

        # reset their session_id so it is no longer valid (redirect them to '/')
        self.__database.update({'session_id': crypt.mksalt(crypt.METHOD_SHA512)})

    def log_user_in(self, username: str, password_to_verify: str) -> bool:
        # can't login if you don't exist
        user = self.find_user(username)
        if user is None:
            return False

        # determine if their password is correct
        password_to_verify = scrypt.hash(password_to_verify, user['salt'])
        known_good_password = UserDB.__decode_hashed_b64_password(user['password'], user['salt'])

        # generate a new session_id on log in
        if password_to_verify == known_good_password:
            self.__database.update({'session_id': crypt.mksalt(crypt.METHOD_SHA512)}, eids=[user.eid])
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
        assert len(results) < 2, "It should be impossible to have two users with the same username."
        return results[0] if len(results) == 1 else None

    def is_valid_session_id(self, session_id):
        results = self.__database.search(Query().session_id == session_id)
        assert len(results) < 2, "It should be impossible to have two users with the same session id"
        return len(results) == 1

    def get_user_session_id(self, username) -> str:
        user = self.find_user(username)
        return user['session_id'] if user is not None else None

    def create_new_user_session(self, session_id: str):
        results = self.__database.search(Query().session_id == session_id)
        assert len(results) < 2, "It should be impossible to have two users with the same session id"
        if len(results) != 1:
            return

        # get their ID and then give them a new session id
        eid = results[0].eid
        self.__database.update({'session_id': crypt.mksalt(crypt.METHOD_SHA512)}, eids=[eid])

    @staticmethod
    def __generate_hashed_b64_password(password=None, salt=None) -> str:
        if password is None or salt is None:
            raise ValueError("Password and Salt cannot be none.")
        return base64.encodebytes(scrypt.hash(password, salt)).decode('utf-8')

    @staticmethod
    def __decode_hashed_b64_password(password=None, salt=None):
        if password is None or salt is None:
            raise ValueError("Password and Salt cannot be none.")
        return base64.decodebytes(password.encode('utf-8'))
