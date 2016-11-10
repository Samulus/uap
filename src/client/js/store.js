/*
    store.js
    Author: Samuel Vargas

    All application-wide logic / state is located here.
*/

const store = new Vuex.Store({
    state: {
        library: JSON.parse(localStorage.getItem("library")),
        song_queue: [],
    },

    mutations: {
        remove_track_index: function(state, i) {
            state.song_queue.splice(i, 1);
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
