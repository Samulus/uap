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

ROOT_PATH = os.path.realpath(os.path.join(__file__, ".."))
VALID_SEARCH_TYPES = ("artist", "album", "title")


def get_app_html() -> str:
    """
    Returns the client interface html to the caller

    :returns: A string containing the client html.
    """
    with open(os.path.join(ROOT_PATH, "client/index.html"), "r") \
            as app_html:
        return app_html.read()


def get_login_html() -> str:
    """
    Returns the login interface html to the caller

    :returns: A string containing the login html.
    """
    with open(os.path.join(ROOT_PATH, "client/login.html"), "r") \
            as login_html:
        return login_html.read()


def string_is_valid_length(string: str, min_len: int, max_len: int) -> bool:
    """
    Checks if a string falls within a specified max / min length.

    :param string: The string in question.
    :param min_len: The maximum length the string should be.
    :param max_len: The minimum length the string should be.
    :returns: True if the string falls within the specified range, false
             otherwise.
    """
    if max_len <= min_len or min_len >= max_len:
        raise ValueError("min_len must be less than max_len")

    if string is None:
        raise ValueError("String cannot be None")

    return min_len <= len(string) <= max_len


class Server(SessionMiddleware):
    APP_HTML = get_app_html()
    LOGIN_HTML = get_login_html()

    session_opts = {
        'session.type': 'memory',
        'session.cookie_expires': False,
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
        bottle.route("/api/library", "GET", self._get_library)
        bottle.route("/api/library/", "GET", self._get_library)

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
        # log in before requesting a song
        if not self.session_is_valid():
            response.status = 403
            return

        # verify the song they're requesting is a song and not a random file
        if self.__taglist.is_song_path_in_taglist(song_path):
            response.status = 200
            return static_file(song_path, root=self.__taglist.audio_folder)

        # if they ask for a path that has no song that corresponds to it
        # then refuse
        else:
            response.status = "404 Couldn't find song " + song_path

    def __search(self):
        if self.session_is_valid():
            artist = request.query.artist or None
            album = request.query.album or None
            title = request.query.title or None
            return json.dumps(self.__taglist.search(artist, album, title))
        else:
            response.status = "401 Login First"

    def _get_library(self):
        if self.session_is_valid():
            return json.dumps(self.__taglist.hierarchy_song_dict)
        else:
            response.status = "401 Login First"
