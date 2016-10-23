#!/usr/bin/env python3

"""
    database_writer.py
    Author: Samuel Vargas
"""

import sqlite3
from unittest import TestCase
from os.path import isabs


class DatabaseWriter:
    def __init__(self,  abs_path):
        if (not isabs(abs_path)):
            raise ValueError("abs_db_path must be absolute")

        self.abs_db_path = abs_path
        self.conn = sqlite3.connect(abs_path)

class WriteDatabaseUnittest(TestCase):
    pass
