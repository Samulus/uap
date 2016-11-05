#!/usr/bin/env python3
#
#   server.py
#   Author: Samuel Vargas
#   Date: 11/4/2016
#
#   The server module is dual purposed: It serves as the
#   RESTful API (send GET requests to api/search and api/library)
#   and also serves a basic web client (client/index.html and client/client.js)
#   if you send a GET request to ('/'). The only requirement is that you pass
#   in a TagList object (see src.taglist).


import json
import os

from bottle import static_file, request, Bottle
from src.taglist import TagList


class Server:
    ROOT_PATH = os.path.realpath(os.path.join(__file__, ".."))
    VALID_SEARCH_TYPES = ("artist", "album", "title")

    def __init__(self, taglist: TagList, host='127.0.0.1', port=8080):
        self._taglist = taglist
        self._port = port
        self._host = host
        self._app = Bottle()
        self._app.route("/", method="GET", callback=self._index)
        self._app.route("/<filename:re:.*\.css>", method="GET", callback=self._static)
        self._app.route("/<filename:re:.*\.js>", method="GET", callback=self._static)
        self._app.route("/<filename:re:.*\.min.map>", method="GET", callback=self._static)
        self._app.route("/api/search", method="GET", callback=self._search)
        self._app.route("/api/search/", method="GET", callback=self._search)
        self._app.route("/api/library", method="GET", callback=self._library)
        self._app.route("/api/library/", method="GET", callback=self._library)

    def start(self):
        self._app.run(host=self._host, port=self._port)

    def _index(self):
        html_path = os.path.join(Server.ROOT_PATH, "client/index.html")
        with open(html_path, "r") as html:
            return html.read()

    def _static(self, filename: str):
        static_root_path = os.path.join(Server.ROOT_PATH, "client/")
        return static_file(filename, root=static_root_path)

    def _search(self):
        artist = request.query.artist or None
        album = request.query.album or None
        title = request.query.title or None
        return json.dumps(self._taglist.search(artist, album, title))

    def _library(self):
        return json.dumps(self._taglist.tag_hierarchy)
