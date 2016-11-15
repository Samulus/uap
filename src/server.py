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

import json
import os

import bottle
from beaker.middleware import SessionMiddleware
from bottle import static_file, request, response

from src.sessiondb import SessionDB
from src.taglist import TagList
from src.userdb import UserDB
from src.validation import username_is_valid_length, password_is_valid_length


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

    def __init__(self, sessiondb: SessionDB, userdb: UserDB, taglist: TagList, host='127.0.0.1', port=8080,
                 login_required=True, reloader=False, debug=False):
        super(Server, self).__init__(bottle.app(), Server.session_opts)
        self.__userdb = userdb
        self.__sessiondb = sessiondb
        self.__login_required = login_required
        self.__taglist = taglist
        self.__port = port
        self.__host = host
        self.__reloader = reloader
        self.__debug = debug

        # serve main index / application
        bottle.route("/", "GET", self.__index)

        # login / signup, these return either return the HTTP status 200 + a unique session_token, or status 401
        bottle.route("/api/signup", "POST", self.__sign_up)
        bottle.route("/api/signup/", "POST", self.__sign_up)
        bottle.route("/api/login", "POST", self.__login)
        bottle.route("/api/login/", "POST", self.__login)

        # static content
        bottle.route("/<filename:re:.*\.css>", "GET", self.__static_file)
        bottle.route("/<filename:re:.*\.js>", "GET", self.__static_file)
        bottle.route("/<filename:re:.*\.min.map>", "GET", self.__static_file)

        # restful API
        bottle.route("/api/search", "GET", self.__search)
        bottle.route("/api/search/", "GET", self.__search)
        bottle.route("/api/library", "GET", self.__library)
        bottle.route("/api/library/", "GET", self.__library)

    def start(self):
        bottle.run(app=self, host=self.__host, port=self.__port, reloader=self.__reloader, debug=self.__debug)

    def __sign_up(self):
        # TODO: input sanitation
        # TODO: we should be using SSL eventually
        username = request.forms.get('username') or None
        password = request.forms.get('password') or None

        # if they fail to specify either -> its a bad request
        if username is None or password is None:
            response.status = '400 You forgot to specify a username, a password, or both.'
            return

        # avoid signing up users with identical names
        if self.__userdb.user_exists(username):
            response.status = '409 This username is already taken.'
            return

        # avoid signing up users with username
        # and passwords that contain invalid values
        if (not password_is_valid_length(password, min_length=8, max_length=512)
             or not username_is_valid_length(username, min_length=1, max_length=32)):
            response.status = 400  # Bad Request
            response.responseText = 'Passwords must be between 8 to 512 chars: Usernames 1 to 32 chars'
            return

    def __login(self):
        pass

    def session_is_valid(self):
        # cookie = bottle.request.environ.get('beaker.session')
        return False

        # if self.__public_mode or 'user_id' in session and :
        # return False
        # else:
        # return True

    def __index(self):
        return Server.APP_HTML if self.session_is_valid() else Server.LOGIN_HTML

    def __static_file(self, filename: str):
        static_root_path = os.path.join(Server.ROOT_PATH, "client/")
        return static_file(filename, root=static_root_path)

    def __search(self):
        artist = request.query.artist or None
        album = request.query.album or None
        title = request.query.title or None
        return json.dumps(self.__taglist.search(artist, album, title))

    def __library(self):
        return json.dumps(self.__taglist.tag_hierarchy)
