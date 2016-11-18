/*
    store.js
    Author: Samuel Vargas

    All application-wide logic / state is located here.
*/

const store = new Vuex.Store({
    state: {
        library: JSON.parse(localStorage.getItem("library")),
        song_queue: [],
        audio_playing: false,
        audio_stream: null,
    },

    mutations: {
        remove_track_index: function(state, i) {
            state.song_queue.splice(i, 1);
        },

        start_playing: function(state, i) {
            var artist = state.song_queue[i]["artist"];
            var album  = state.song_queue[i]["album"];
            var title  = state.song_queue[i]["title"];
            var path   = state.library[artist][album][title]["filepath"];

            state.audio_stream = new Howl({
                src: ['api/song/' + path],
                ext: ['mp3', 'ogg', '.flac'],
                autoplay: true,
                html5: true,
            })

            state.audio_playing = true;
        },

        add_to_queue: function(state, track_object) {
            state.song_queue.push(track_object);
        },

        refresh_library: function() {
            Vue.http.get('api/library').then(
                (function(response) {
                    localStorage.setItem("library", response.body)
                    store.state.library = JSON.parse(response.body)
                }),
                (function(error) {
                    alert("failed to retrieve library list from server")
                })
            )
        }
    }
})
