#!/usr/bin/env python3
#
#   test_server.py
#   Author: Samuel Vargas
#   Date: 10/31/2016
#
#   This is a mock implementation of the server of the
#   to enable testing of the server api. It loads
#   tags from tag.json in the same directory as this test.

#   TODO: Rewrite this so that the contents of this file become
#         ../server.py and this module uses http requests to
#         ACTUALLY test the server.



import json
import os

from bottle import route, run, static_file, request

from src.taglist import TagList

VALID_SEARCH_TYPES = ("artist", "album", "title")
ROOT_PATH = os.path.realpath(os.path.join(__file__, ".."))
tags = None


@route("/")
def index():
    html_path = os.path.join(ROOT_PATH, "../client/index.html")
    with open(html_path, "r") as html:
        return html.read()


@route('/<filename:re:.*\.css>')
@route('/<filename:re:.*\.js>')
@route('/<filename:re:.*\.min.map>')
def static(filename: str):
    static_root_path = os.path.join(ROOT_PATH, "../client/")
    return static_file(filename, root=static_root_path)


@route("/api/search")
def search():
    artist = request.query.artist or None
    album = request.query.album or None
    title = request.query.title or None
    return "not implemented ;-( "


@route("/api/library")
def library():
    return json.dumps(tags.tag_hierarchy)


if __name__ == "__main__":
    tag_path = os.path.join(ROOT_PATH, "tags.json")
    tags = TagList(use_json_path=tag_path)
    run(reloader=True, debug=True, port=8080)
