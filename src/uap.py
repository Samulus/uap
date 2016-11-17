#!/usr/bin/env python3
#  
#   uap.py
#   Author: Samuel Vargas

#   TODO: introduce a configuration file so that users don't
#   have to manually specify the path of their music library
#   everytime they want to run the server.
   

from bottle import route, run, static_file, template
from sys import argv
from src.taglist import TagList

tag_list = None

def usage(av):
    print(""" Usage: {0} [abs path to audio folder]. """.format(av[0]))


if __name__ == '__main__':
    if len(argv) != 2:
        usage(argv)
        exit(1)
    print("Loading music library... this may take a while")
    tag_list = TagList(argv[1])
    print("Serving api on port 8080...")
    run(reloader=True, debug=True, port=8080)
