#
#   validation.py
#   Author: Samuel Vargas
#   Date: 10/30/2016
#
#   This module contains a number of functions to allow
#   the rest of the program to ensure that miscellaneous
#   user provided strings actually contain valid data


def password_is_valid_length(password: str, min_length=8, max_length=512) -> bool:
    if password is None:
        raise ValueError("validation.py: password cannot be None")
    return min_length <= len(password) <= max_length


def username_is_valid_length(username: str, min_length=1, max_length=32) -> bool:
    if username is None:
        raise ValueError("validation.py: username cannot be None")
    return min_length <= len(username) <= max_length
