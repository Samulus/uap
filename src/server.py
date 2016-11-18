#!/usr/bin/env python3
#
#   server.py
#   Author: Samuel Vargas
#   Date: 11/4/2016
#
#   The server module is dual purposed: It serves as the
#   RESTful API (send GET requests to api/search and api/library)
#   and also serves a basic web client (client/index.html and client/*.js)
#   if you send a GET request to ('/').
#

import json
import os

import bottle
from beaker.middleware import SessionMiddleware
from bottle import static_file, request, response

from src.taglist import TagList
from src.userdb import UserDB
from src.validation import string_is_valid_length

ROOT_PATH = os.path.realpath(os.path.join(__file__, ".."))
VALID_SEARCH_TYPES = ("artist", "album", "title")


def get_app_html():
    with open(os.path.join(ROOT_PATH, "client/index.html"), "r") \
            as app_html:
        return app_html.read()


def get_login_html():
    with open(os.path.join(ROOT_PATH, "client/login.html"), "r") \
            as login_html:
        return login_html.read()


class Server(SessionMiddleware):
    APP_HTML = get_app_html()
    LOGIN_HTML = get_login_html()

    session_opts = {
        'session.type': 'memory',
        'session.cookie_expires': 300,
        'session.auto': True
    }

    def __init__(self, userdb: UserDB, taglist: TagList, host='127.0.0.1',
                 port=8080, login_required=True, reloader=False, debug=False):
        super(Server, self).__init__(bottle.app(), Server.session_opts)
        self.__userdb = userdb
        self.__login_required = login_required
        self.__taglist = taglist
        self.__port = port
        self.__host = host
        self.__reloader = reloader
        self.__debug = debug

        # serve main index / application
        bottle.route("/", "GET", self.__index)

        # login / signup, these return either
        # HTTP status 200 or HTTP status 4xx to denote an error
        bottle.route("/api/signup", "POST", self.__sign_up)
        bottle.route("/api/signup/", "POST", self.__sign_up)
        bottle.route("/api/login", "POST", self.__login)
        bottle.route("/api/login/", "POST", self.__login)

        # signout
        bottle.route("/api/logout", "POST", self.__logout)
        bottle.route("/api/logout/", "POST", self.__logout)

        # static content
        bottle.route("/<filename:re:.*\.css>", "GET", self.__static_file)
        bottle.route("/<filename:re:.*\.js>", "GET", self.__static_file)
        bottle.route("/<filename:re:.*\.min.map>", "GET", self.__static_file)
        bottle.route("/<filename:re:.*\.woff>", "GET", self.__static_file)
        bottle.route("/<filename:re:.*\.ttf>", "GET", self.__static_file)

        # restful API
        bottle.route("/api/search", "GET", self.__search)
        bottle.route("/api/search/", "GET", self.__search)
        bottle.route("/api/library", "GET", self.__library)
        bottle.route("/api/library/", "GET", self.__library)

        bottle.route("/api/song/<song_path:path>", "GET", self.get_song)

    def start(self):
        bottle.run(app=self,
                   host=self.__host,
                   port=self.__port,
                   reloader=self.__reloader,
                   debug=self.__debug)

    def __logout(self):
        # get their session_id, find the user that has this
        # session ID and overwrite it.
        session = bottle.request.environ.get('beaker.session')
        if 'session_id' in session:
            self.__userdb.create_new_user_session(session['session_id'])

    def __login(self):
        # TODO: input sanitation
        username = request.forms.get('username') or None
        password = request.forms.get('password') or None

        # if they fail to specify either -> its a bad request
        if username is None or password is None:
            response.status = '400 Specify a username and password.'
            return

        # no such user, bad password -> notify user of bad request
        if not (self.__userdb.find_user(username) and
                    self.__userdb.log_user_in(username, password)):
            response.status = '401 Bad Password or Non-Existent Account'
            return

        # authenticate the user
        else:
            response.status = '200 Login Successful'
            session = bottle.request.environ.get('beaker.session')
            session['session_id'] = self.__userdb.get_user_session_id(username)

    def __sign_up(self):
        # TODO: input sanitation
        username = request.forms.get('username') or None
        password = request.forms.get('password') or None

        # if they fail to specify either -> its a bad request
        if username is None or password is None:
            response.status = '400 Specify a username and a password.'
            return

        # avoid signing up users with identical names
        elif self.__userdb.find_user(username):
            response.status = '409 This username is already taken.'
            return

        # avoid signing up users with username
        # and passwords that contain invalid lengths
        elif (not string_is_valid_length(password, min_len=8, max_len=512)
              or not string_is_valid_length(username, min_len=1, max_len=32)):
            response.status = ('400 Password must be 8 to 512 chars. '
                               'Username must be between 1 and 32 chars')
            return

        # send session id for newly created user if all is well
        else:
            response.status = "200 Welcome to uap!"
            self.__userdb.add_user(username, password)
            session = bottle.request.environ.get('beaker.session')
            session['session_id'] = self.__userdb.get_user_session_id(username)

    def session_is_valid(self):
        session = bottle.request.environ.get('beaker.session')
        if not self.__login_required:
            return True
        if 'session_id' not in session:
            return False
        return self.__userdb.is_valid_session_id(session['session_id'])

    def __index(self):
        if self.session_is_valid():
            if not self.__debug:
                return Server.APP_HTML
            else:
                return get_app_html()
        else:
            if not self.__debug:
                return Server.LOGIN_HTML
            else:
                return get_login_html()

    def __static_file(self, filename: str):
        static_root_path = os.path.join(ROOT_PATH, "client/")
        return static_file(filename, root=static_root_path)

    def get_song(self, song_path: str):
        # TODO: actually verify that the song_path the user is requesting
        # is in the database so that we don't just hand them any url
        print(song_path)
        return static_file(song_path, root=self.__taglist.audio_folder)
        if not self.session_is_valid():
            response.status = 403
            return
        path_to_song = self.__taglist.get_absolute_song_path(song_path)
        if path_to_song is None:
            response.status = 404
        else:
            response.status = 200
            return static_file(song_path, root=self.__taglist.audio_folder)

    def __search(self):
        if self.session_is_valid():
            artist = request.query.artist or None
            album = request.query.album or None
            title = request.query.title or None
            return json.dumps(self.__taglist.search(artist, album, title))
        else:
            response.status = "401 Login First"

    def __library(self):
        if self.session_is_valid():
            return json.dumps(self.__taglist.hierarchy)
        else:
            response.status = "401 Login First"
