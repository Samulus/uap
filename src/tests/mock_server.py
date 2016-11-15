#!/usr/bin/env python3
#
#   mock_server.py
#   Author: Samuel Vargas
#   Date: 11/4/2016
#
#   This is a mock implementation of the backend server api
#   to enable testing of the server's API and the frontend client.
#
#   TODO: At the time it's not possible to actually stream music
#   using this mock implementation. We need to monkey patch
#   the server to return sample audio every time the user requests
#   a specific audio file.
from src.sessiondb import SessionDB
from src.taglist import TagList
from src.server import Server
from src.userdb import UserDB
import os

ROOT_PATH = os.path.realpath(os.path.join(__file__, ".."))
MUSIC_PATH = "/home/sam/music"  # change this to whatever on your system
MOCK_TAGS_PATH = os.path.join(ROOT_PATH, "tags.json")

if __name__ == '__main__':
    if not os.path.exists(MOCK_TAGS_PATH):
        TagList(audio_directory=MUSIC_PATH).dump_to_json_file(MOCK_TAGS_PATH)

    Server(
        taglist=TagList(use_json_path=MOCK_TAGS_PATH),
        sessiondb=SessionDB(),
        userdb=UserDB(),
        debug=True,
        login_required=False,
        reloader=True).start()
