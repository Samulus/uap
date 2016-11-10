/*
    component.js
    Author: Samuel Vargas
    Date: 10/31/2016
*/

Vue.component('refresh-library', {
    template: "#refresh-library",
    store: store,
    methods: {
        refresh_library: function() {
            this.$store.commit("refresh_library");
        }
    }
})

Vue.component('artists-view', {
    template: "#artists-view",
    store: store,
    computed: {
        library: function() {
            return store.state.library;
        }
    }
});

Vue.component("all-albums-view", {
    template :"#all-albums-view",
    data: function() {
        return {};
    },
    store: store,
    computed: {
        library: function() {
            return store.state.library;
        }
    },
})

Vue.component("artist-albums-view", {
    template: '#artist-albums-view',
    store: store,
    computed: {
        artist_name: function() {
            return this.$route.params.artist;
        },

        artist_albums: function() {
            return store.state.library[this.$route.params.artist];
        },
    },
});

Vue.component("track-album-view", {
    template: "#track-album-view",
    store: store,
    methods: {
        enqueue: function(title) {
            var artist = this.$route.params.artist;
            var album = this.$route.params.album;
            this.$store.commit("add_to_queue", {"artist": artist, "album": album, "title": title});
        }
    },

    computed: {
        artist_name: function() {
            return this.$route.params.artist;
        },

        album_name: function() {
            return this.$route.params.album;
        },

        track_list: function() {
            /* TODO: this can fail if either of these things are undefined */
            return store.state.library[this.$route.params.artist][this.$route.params.album];
        }
    }
});

Vue.component('nav-component', { template: "#nav-component" });
Vue.component('genre-view', {template: "#genre-view"});

Vue.component('song-queue', {
    template: "#song-queue",
    store: store,
    methods: {
        remove: function(i) {
            this.$store.commit("remove_track_index", i);
        }
    },

    computed: {
        get_tracks: function() {
            return store.state.song_queue;
        },

    }
});
