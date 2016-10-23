#!/usr/bin/env python3
"""
    library.py
    Author: Samuel Vargas
    Date: 10/15/2016

    This is a simple mockup website using my library data as an example
    to show what the website should potentially look like / test templating
    with bottle.py. Execute this file and point your browser to http://127.0.0.1:8080
    to preview it.
"""

from bottle import route, run, static_file, template
from os.path import realpath, dirname, join
import json


@route("<filename:path>")
def static(filename: str):
   return static_file(filename, root="../frontend/")


@route("/")
def index():
   with open("../mockdata/bins/db.json") as file:
      path = join(dirname(realpath("../")), "mocks/frontend/library.tpl")
      db = json.loads(file.read())
      return template(path, library=db)


if __name__ == '__main__':
   run(reloader=True, debug=True, port=8080)
