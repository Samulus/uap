/*
    component.js
    Author: Samuel Vargas
    Date: 10/31/2016

    Please note that the order the components are declared in
    this file should match the order that the components are
    declared in index.html. This will make it easier to look
    up components and spend less time hunting things down.

    Additionally the following naming scheme for elements
    and components is used:

    Anything that is a component (i.e. doesn't represent an
    entirely different page in the application) should have the
    name <foo>-<bar>-component.

    Anything that is a view (i.e. represents a specific view
    like Artists page, search page, etc) is a <foo>-<bar>-<view>

    Every component or view should have a
    <template id='<foo>-<bar>-<view|component>'></template>
    tag that corresponds to it

    If you add another component that should be routable
    make sure you update it and add an entry for it
    in route.js too!
*/

Vue.component('nav-component', {
    template: "#nav-component"
});

Vue.component('song-queue-view', {
    template: "#song-queue-view",
    store: store,
    methods: {
        play: function(i) {
            this.$store.commit("start_playing", i)
        },
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
            this.$store.commit("add_to_queue",
            {"artist": artist, "album": album, "title": title});
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

Vue.component('genre-view', {
    template: "#genre-view"
});


Vue.component('signout-component', {
    template: "#signout-component",
    methods: {
        signout: function(event) {
            Vue.http.options.emulateJSON = true;
            event.preventDefault();
            Vue.http.post('api/logout', {
                'session_id': Cookies.get('beaker.session.id')
            }).then(
                function success(response) {
                    /* basically force a page reload */
                    window.location.href = "../../"
                },
                function failure(response) {
                    alert("Could not sign out, try again later.");
                    }
                );
            }
        }
});

Vue.component('refresh-library-component', {
    template: "#refresh-library-component",
    store: store,
    methods: {
        refresh_library: function() {
            this.$store.commit("refresh_library");
        }
    }
})

Vue.component('now-playing-component', { template: "#now-playing-component" });

Vue.component('settings-view', {
    template: "#settings-view"
});






