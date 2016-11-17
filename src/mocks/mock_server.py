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

from unittest import mock

from src.taglist import TagList
from src.userdb import UserDB
from src.server import Server
from src.mocks.mock_library import MockLibrary
from bottle import static_file, response
from os.path import join, realpath
import json

ROOT_PATH = realpath(join(__file__, ".."))
MOCK_TAGS_PATH = join(ROOT_PATH, "data/tags.json")


def get_flamenco(self, song_path: str):
    if self.session_is_valid():
        response.status = 200
        return static_file("moonlight_jazz.mp3",
                           root=join(ROOT_PATH, "data"))
    else:
        response.status = 403


if __name__ == '__main__':
    tags_to_write = None
    with open(MOCK_TAGS_PATH, "r") as file:
        tags_to_write = json.loads(file.read())

    # create the mock library
    mock_library = MockLibrary(mock_files=tags_to_write)

    # create a taglist using data from mock_library
    mock_taglist = TagList(mock_library.path, ram_db=True)

    # delete the temporary files, we don't need them
    # since we're monkey patching the audio code anyway
    mock_library.cleanup()

    # create the server
    with mock.patch('src.server.Server.get_song', get_flamenco):
        server = Server(
            taglist=mock_taglist,
            userdb=UserDB(ram_db=True),
            debug=True,
            login_required=False,
            reloader=True
        )
        server.start()
