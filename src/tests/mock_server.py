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

from src.taglist import TagList
from src.server import Server
import os

if __name__ == '__main__':
    file_path = os.path.realpath(os.path.join(__file__, ".."))
    tag_path = os.path.join(file_path, "tags.json")
    Server(TagList(use_json_path=tag_path)).start()
