## TODO:
The project can be divided into three distinct portions that need to be
completed: The backend, the frontend client, and the actual playback 
of audio in the client (we're going to have to use js / ajax
to request specific audio files from the server).

### Backend

I (Samuel) can handle the backend on my own. I'm going to code 
everything pertaining to loading music from the servers music directory,
serializing this to a SQlite3 database, and handling general 
configuration things. I don't expect this to take too long but 
it needs to be done so might as well.

### Client
I created a barebones mock demo in the mocks folder of what the
client could potentially look like. This can 100% change and if any
of you guys have way more experience with, say Angular + Bootstrap,
please feel free to recode it how you see fit. I used
vital.css and vue.js for now. Vue is basically a smaller simpler version
of Angular. To simplify things the server will send the client a single 
HTML page with all the required information embedded in the page 
(but not everything will be rendered immediately). From here using 
Javascript we can dynamically update the onscreen view depending on what 
tab is selected. I posted an extremely rudimentary demo of this in the 
mocks folder. Just run library.py and point the web browser at 
http://127.0.0.1:8080

### Client Audio Player
I'm including this as it's own category because it is slightly distinct
from the client itself. We need to make sure that our client can play at
MP3 / Flac / Ogg files in the web browser. It doesn't need to know 
anything about how the client works, it just needs to be able to 
request a file using ajax, and then take that file and play it in the
web browser. We can glue it into the client later.

### Task Delegation
I think that the client by far will take the most amount of time
so we should delegate two people to it for now. I can handle the 
backend and then join the rest of you guys in further developing the
web client when I finish. 

* Backend
    * Samuel

* Client
    * ???
    * ???

* Audio Player
    * ???