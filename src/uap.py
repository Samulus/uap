#!/usr/bin/env python3
#  
#   uap.py
#   Author: Samuel Vargas

#   TODO: introduce a configuration file so that users don't
#   have to manually specify the path of their music library
#   everytime they want to run the server.


from src.server import Server
from src.taglist import TagList
from src.userdb import UserDB

if __name__ == '__main__':
    server = Server(
        host='127.0.0.1',
        taglist=TagList("D:\music"), # change this to your music folder
        userdb=UserDB(),
        debug=True,
        reloader=False,
        login_required=True,
    )
    server.start()
