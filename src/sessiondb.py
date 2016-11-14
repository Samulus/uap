#
#   sessiondb.py
#   Author: Samuel Vargas
#   Date: 11/12/2016
#
#   Maintains a list of all the currently logged in users
#   and allows the server to verify if a user is actually
#   logged in or not.

from src.userdb import UserDB


class SessionDB:
    def __init__(self):
        pass

    def user_is_logged_in(self):
        raise NotImplementedError

    def token_is_valid(self):
        raise NotImplementedError
