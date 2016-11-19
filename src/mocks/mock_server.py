#!/usr/bin/env python3
#
#   mock_server.py
#   Author: Samuel Vargas
#   Date: 11/4/2016
#
#   This is a mock implementation of the backend server api
#   to enable testing of the server's API and the frontend client.
#   At the moment it uses Samuel's library for test data and mocks
#   out any request to 'api/song' (the get_flamenco method in Server)
#   to always return the same sample flamenco song each time.

#   You can use this module to test all logic on the client without
#   actually running the server with your own music collection.
#   In other words this module is fully portable provided you don't
#   move data/moonlight_jazz.mp3 or data/tags.json

from os.path import join, realpath
from unittest import mock

from bottle import static_file, response

from src.server import Server
from src.userdb import UserDB

ROOT_PATH = realpath(join(__file__, ".."))
MOCK_TAGS_PATH = join(ROOT_PATH, "data/tags.json")
MOCK_LIBRARY_HIERARCHY = join(ROOT_PATH, "data/library_hierarchy.json")


# server.py: Stubbed out methods
def get_song(self, song_path: str):
    if self.session_is_valid():
        response.status = 200
        return static_file("moonlight_jazz.mp3",
                           root=join(ROOT_PATH, "data"))
    else:
        response.status = 403


def get_library(self):
    if self.session_is_valid():
        response.status = 200
        with open(MOCK_LIBRARY_HIERARCHY, "r") as library_hierarchy:
            return library_hierarchy.read()
    else:
        response.status = 403


if __name__ == '__main__':
    with mock.patch('src.server.Server.get_song', get_song), \
         mock.patch('src.server.Server.get_library', get_library):
        server = Server(
            taglist=None,
            userdb=UserDB(ram_db=True),
            debug=True,
            login_required=False,
            reloader=False
        )
        server.start()
