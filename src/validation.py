#
#   validation.py
#   Author: Samuel Vargas
#   Date: 10/30/2016
#
#   This module contains a number of functions to allow
#   the rest of the program to ensure that miscellaneous
#   user provided strings actually contain valid data


def string_is_valid_length(string: str, min_len=8, max_len=512) -> bool:
    if string is None:
        raise ValueError("String cannot be None")
    return min_len <= len(string) <= max_len

