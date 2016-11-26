/*
    store.js
    Author: Samuel Vargas

    All application-wide logic / state is located here.
 */

var store = new Vuex.Store({
    state: {
        library: JSON.parse(localStorage.getItem("library")),
        song_queue: [],
        audio_index_playing: -1,
        audio_stream: null,
        audio_stream_paused: false
    },

    mutations: {
        remove_track_index: function (state, i) {
            state.song_queue.splice(i, 1);

            /* if we remove the song that is currently playing
             * then stop the audio and reset the application playing
             * state */

            if (state.audio_index_playing == i) {
                state.audio_index_playing = -1;
                state.audio_stream_paused = false;
                if (state.audio_stream !== null)
                    state.audio_stream.stop();
                state.audio_stream = null;
            }

           /* if removing an element less than
            * the current audio element that is playing
            * then decrement audio_index_playing 
            * appropriately
            */

           if (i <= state.audio_index_playing) {
              state.audio_index_playing -= 1;
           }
        },

        reorder_list: function (state, indices) {
            var deleted = state.song_queue.splice(indices.old, 1);
            state.song_queue.splice(indices.new, 0, deleted[0]);

            /* if we drag a song that IS NOT  playing to where
             * the currently playing song is then we either
             * have to move the now playing song either
             * -1 or +1 depending on where we are
             */

            if (indices.new == state.audio_index_playing) {
                if (indices.old < indices.new) {
                  state.audio_index_playing -= 1;
                } else {
                  state.audio_index_playing += 1;
                }
            }

            /* if we're dragging a song that IS currently playing
             * then we need to update state.audio_index_playing
             * to accurately reflect the new position */
            else if (indices.old == state.audio_index_playing) {
                state.audio_index_playing = indices.new;
            }
        },

        resume: function (state, i) {
            if (i < 0) {
                alert("Cannot resume non-existent track");
                return;
            }

            state.audio_stream.play();
            state.audio_stream_paused = false;
        },

        pause: function (state, i) {
            if (i < 0) {
                alert("Cannot pause non-existent track");
                return;
            }
            state.audio_stream.pause();
            state.audio_stream_paused = true;
        },

        play_next_song_in_queue: function (state) {

            /* if we're at the end of the song queue, don't try to
             * play another song and reset the playing state of the
             * application */

            if (state.audio_index_playing >= state.song_queue.length - 1) {
                state.audio_stream_paused = false;
                state.audio_index_playing = -1;
                return;
            }

            /* otherwise play the next song */
            else {
                store.commit("start_playing", state.audio_index_playing + 1);
            }


        },

        start_playing: function (state, i) {
            var artist = state.song_queue[i].artist;
            var album = state.song_queue[i].album;
            var title = state.song_queue[i].title;
            var path = state.library[artist][album][title].filepath;
            state.audio_index_playing = i;

            /* avoid playing multiple sounds at the same time */
            if (state.audio_stream !== null) {
                state.audio_stream.stop();
                state.audio_stream = null;
            }

            state.audio_stream = new Howl({
                src: ['api/song/' + path],
                ext: ['mp3', 'ogg', '.flac'],
                autoplay: true,
                html5: true,
                onend: function () {
                    store.commit("play_next_song_in_queue");
                }
            });

            state.audio_stream_paused = false;
        },

        add_to_queue: function (state, track_object) {
            state.song_queue.push(track_object);
        },

        refresh_library: function () {
            Vue.http.get('api/library').then(
                (function (response) {
                    localStorage.setItem("library", response.body);
                    store.state.library = JSON.parse(response.body);
                }),
                (function (error) {
                    alert("failed to retrieve library list from server");
                })
            );
        }
    }
});
