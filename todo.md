# Useful Documentation Shortcuts 

## Helpful IDE Stuff
* http://www.pydev.org/

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

# Backend TODO (Priority)

* Implement the tests/mock_library.py module, it should use the
tempfile module to populate a temporary directory with
bogus audio files with random (but fixed and non-changing tags)
for testing the misc backend modules in the application.

* Implement the tests/test_taglist.py using the Unittest module
built into Python. It should adequately test all of the functions
and use the aforementioned tests/mock_library.py module to do the 
job.

* Modify src/taglist.py so that it does not include the absolute
filepath to the user's audio files when it scans the directory. It's
a security problem and it's extraneous information that doesn't
need to be sent to the client every time they request more
data (wastes space).

* Modify the def __construct_tag_hierarchy(self) method in 
src/taglist.py so that it doesn't ignore audio files that are missing 
an artist tag, an album tag, or a title tag.

* Implement a src/config.py module that allows the user to save all 
configuration information like the port / host / music directory
offline to a json file. We can use the getopt module in src/uap.py
to parse commandline arguments to the application and allow the user
to either pass the path to their config.json file OR have it load
a default config.json file from the application directory.

* Add support to src/server.py for requesting a specific
audio file from the server to the client.

# Frontend TODO (Priority)
* Fix the fact that "nulls" and "undefineds" are showing up due to the 
fact that the Vue components indiscriminately insert the contents
of the library even if the key has no value (thus inserting an undefined)

* Implement the song-queue component in client/index.html /
client/client.js so that when a user clicks the "Enqueue" button on a track,
the, the track is sent to the queue.

* Implement some kind of now-playing component in client/index.html / client/client.js
whenever the user is playing a track.

* Implement HTML5 audio controls / wrapper component tied to now-playing
component

# Backend TODO (Low Priority)
* Implement some kind of login page / basic security to prevent anyone
from using the web app.

# Frontend TODO (Low Priority)
* Improve application performance on mobile devices.