#!/usr/bin/env python3
"""
    uap.py
    Author: Samuel Vargas

    TODO: introduce a configuration file so that users don't
    have to manually specify the path of their music library
    everytime they want to run the server.

"""

from bottle import route, run, static_file, template
from sys import argv
from taglist import TagList
import json

tag_list = None


@route("/api/library")
def library():
    return json.dumps(tag_list.get_tags())


def usage(argv):
    print(""" Usage: {0} [Absolute Path To Music Directory]. """.format(argv[0]))


if __name__ == '__main__':
    if len(argv) != 2:
        usage(argv)
        exit(1)
    print("Loading music library... this may take a while")
    tag_list = TagList(argv[1])
    print("Serving api on port 8080...")
    run(reloader=True, debug=True, port=8080)
