#!/usr/bin/env python3
"""
    server.py
    Author: Samuel Vargas
    Date: 10/31/2016

    This is a simple mock-up website using my library data as an example
    to show what the website should potentially look like / test templating
    with bottle.py. Execute this file and point your browser to http://127.0.0.1:8080
    to preview it.

    TODO: sandbox requests that are outside of the music
    directory
"""

from bottle import route, run, static_file, request, template

from src.taglist import TagList
import json

VALID_SEARCH_TYPES = ("artist", "album", "title")

tags = None
json_tags = None
html = None


@route("/")
def index():
    return html


@route('/<filename:re:.*\.css>')
@route('/<filename:re:.*\.js>')
@route('/<filename:re:.*\.map>')
def static(filename: str):
    return static_file(filename, root="../../client/")


# use regex
@route("/api/search")
def search():
    artist = request.query.artist or None
    album = request.query.album or None
    title = request.query.title or None
    return template("""
    <h1>{{artist}}</h1>
    <h1>{{album}}</h1>
    <h1>{{title}}</h1>
    """, artist=artist, album=album, title=title)


@route("/api/library")
def library():
    return json.dumps(json_tags)


if __name__ == '__main__':
    tags = TagList(None)
    tags.load_from_json("tags.json")
    json_tags = tags.as_json_str()

    with open("../../client/index.html") as txt:
        html = txt.read()

    run(reloader=True, debug=True, port=8080)
