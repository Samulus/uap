# Project Dependencies
* python3
    * ...
* [mutagen](https://pypi.python.org/pypi/mutagen)
    * For reading tags from audio files
* [bottle.py](http://bottlepy.org/docs/dev/)
    * For serving HTML / json to the client 
* [bottle-beaker](https://pypi.python.org/pypi/bottle-beaker/)
    * For managing sessions and authentication
* [scrypt](https://pypi.python.org/pypi/scrypt/)
    * For hashing client passwords serverside for security purposes.
* [tinydb](http://tinydb.readthedocs.io/en/latest/)
        * For saving information about users, sessions, and the music library

# Useful Documentation Shortcuts

## Helpful IDE Stuff
* http://www.pydev.org/
* https://www.jetbrains.com/pycharm/

## Version Control
* https://try.github.io/levels/1/challenges/1
* https://www.atlassian.com/git/
* http://rypress.com/tutorials/git/index

## Backend Documentations
* http://www.blog.pythonlibrary.org/2016/07/07/python-3-testing-an-intro-to-unittest/
* https://docs.python.org/3/library/unittest.html
* https://pypi.python.org/pypi/pytaglib
* https://python.swaroopch.com/
* https://docs.python.org/3/tutorial/index.html

## Frontend Documentation 
* https://vuejs.org/v2/guide/
* http://router.vuejs.org/en/index.html
* http://vuex.vuejs.org/en/index.html
* https://vitalcss.com/components/

# Misc Frontend Information

* Please execute tests/mock_server.py and point your web browser
to http://127.0.0.1:8080 to preview and work on the client 

* If you attempt to open index.html and download data
from the server directly it won't work (the AJAX get requests
will fail)
