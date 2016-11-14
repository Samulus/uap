#!/usr/bin/env python3
#
#   server.py
#   Author: Samuel Vargas
#   Date: 11/4/2016
#
#   The server module is dual purposed: It serves as the
#   RESTful API (send GET requests to api/search and api/library)
#   and also serves a basic web client (client/index.html and client/*.js)
#   if you send a GET request to ('/'). The only requirement is that you pass
#   in a TagList object (see src.taglist).

#   TODO: This needs to be a fully static class.
#   TODO: STOP ACCEPTING PASSWORDS via PLAINTEXT


import json
import os

import bottle
from beaker.middleware import SessionMiddleware
from bottle import static_file, request, redirect

from src.sessiondb import SessionDB
from src.taglist import TagList
from src.userdb import UserDB


class Server(SessionMiddleware):
    ROOT_PATH = os.path.realpath(os.path.join(__file__, ".."))
    VALID_SEARCH_TYPES = ("artist", "album", "title")

    with open(os.path.join(ROOT_PATH, "client/index.html"), "r") as app_html:
        APP_HTML = app_html.read()

    with open(os.path.join(ROOT_PATH, "client/login.html"), "r") as login_html:
        LOGIN_HTML = login_html.read()

    session_opts = {
        'session.type': 'file',
        'session.cookie_expires': 300,
        'session.data_dir': './uap_cookies',
        'session.auto': True
    }

    def __init__(self, sessiondb: SessionDB, userdb: UserDB, taglist: TagList, host='127.0.0.1', port=8080, public_mode=True, reloader=False, debug=False):
        super(Server, self).__init__(bottle.app(), Server.session_opts)
        self.__userdb = userdb
        self.__sessiondb = sessiondb
        self.__public_mode = public_mode
        self.__taglist = taglist
        self.__port = port
        self.__host = host
        self.__reloader = reloader
        self.__debug = debug

        # serve main app
        bottle.route("/", method="GET", callback=self.__index)

        # process signup post
        bottle.route("/api/signup", method="POST", callback=self.__sign_up)
        bottle.route("/api/signup/", method="POST", callback=self.__sign_up)

        # static content
        bottle.route("/<filename:re:.*\.css>", method="GET", callback=self.__static_file)
        bottle.route("/<filename:re:.*\.js>", method="GET", callback=self.__static_file)
        bottle.route("/<filename:re:.*\.min.map>", method="GET", callback=self.__static_file)

        # restful API
        bottle.route("/api/search", method="GET", callback=self._search)
        bottle.route("/api/search/", method="GET", callback=self._search)
        bottle.route("/api/library", method="GET", callback=self._library)
        bottle.route("/api/library/", method="GET", callback=self._library)

    def start(self):
        bottle.run(app=self, host=self.__host, port=self.__port, reloader=self.__reloader, debug=self.__debug)

    def __sign_up(self):
        username = request.forms.get('username')
        password = request.forms.get('password')
        print("New Signup Request: {0}, {1}".format(username, password))

    def session_is_valid(self):
        #cookie = bottle.request.environ.get('beaker.session')
        return True

        #if self.__public_mode or 'user_id' in session and :
            #return False
        #else:
            #return True

    def __index(self):
        return Server.APP_HTML if self.session_is_valid() else Server.LOGIN_HTML

    def __static_file(self, filename: str):
        static_root_path = os.path.join(Server.ROOT_PATH, "client/")
        return static_file(filename, root=static_root_path)

    def _search(self):
        artist = request.query.artist or None
        album = request.query.album or None
        title = request.query.title or None
        return json.dumps(self.__taglist.search(artist, album, title))

    def _library(self):
        return json.dumps(self.__taglist.tag_hierarchy)
