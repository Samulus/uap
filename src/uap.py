#!/usr/bin/env python3
#  
#   uap.py
#   Author: Samuel Vargas
#   Date: 11/20/2016

from src.server import Server
from src.taglist import TagList
from src.userdb import UserDB
from src.config import load_settings_dict

if __name__ == '__main__':

    settings = load_settings_dict()
    if settings is None:
        print("config.ini was not found and an example one was "
              "generated for you. Please modify it and rerun the "
              "program.")
        exit(0)

    server = Server(
        host=settings['host'],
        taglist=TagList(settings['music_folder']),
        userdb=UserDB(),
        debug=settings['debug'],
        reloader=settings['reloader'],
        login_required=settings['login_required'],
    )

    server.start()
