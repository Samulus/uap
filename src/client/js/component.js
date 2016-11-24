/*
    Author: Samuel Vargas
    Date: 10/31/2016
 */


/* nav component */
Vue.component('nav-component', {
    template: "#nav-component"
});

/* search component */
Vue.component('search-view', {
    template: "#search-view",
    store: store,

    data: function () {
        return {
            artist: "",
            album: "",
            title: "",
            results: [],
            display_results: false
        };
    },

    methods: {
        update_results: function (results) {
            this.$data.results = results;
            this.$data.display_results = true;
        },

        enqueue: function (i) {
            this.$store.commit("add_to_queue",
                {
                    "artist": this.$data.results[i].artist[0],
                    "album": this.$data.results[i].album[0],
                    "title": this.$data.results[i].title[0]
                });
        },

        search: function (event) {
            event.preventDefault();
            Vue.http.options.emulateJSON = true;

            /* generate search query url */
            var url = 'api/search?artist=' + this.$data.artist +
                '&album=' + this.$data.album +
                "&title=" + this.$data.title;

            this.$http.get(url).then(
                function success(response) {
                    var results = JSON.parse(response.body);
                    var required_tags = ["artist", "album", "title", "filepath"];
                    for (var i = results.length - 1; i >= 0; --i) {
                        for (var k = required_tags.length - 1; k >= 0; --k) {
                            if (typeof results[i] === "undefined" ||
                                typeof results[i][required_tags[k]] === "undefined") {
                                results.splice(i, 1);
                            }
                        }
                    }
                    this.$data.results = results;
                    this.$data.display_results = true;
                },
                function failure(response) {
                    alert("Error");
                }
            );
        }
    }
});

/* 
 * now playing component
 */

Vue.component('now-playing-component', {
    template: "#now-playing-component"
    /* TODO: cody */
});

Vue.component('song-queue-view', {
    template: "#song-queue-view",
    store: store,

    events: {
        sort: function (item, oldIndex, newIndex) {
            this.$store.commit("reorder_list", {old: "oldIndex", new: "newIndex"});
        }
    },

    directives: {
        sortable: {
            bind: function (el, binding) {
                /* where callback_func == this.$methods.on_reorder */
                callback_func = binding.value;
                Sortable.create(el, {
                    onUpdate: function (event) {
                        callback_func(event.oldIndex, event.newIndex);
                    }
                });
            },
        },
    },

    data: function () {
        return {
            get_tracks: store.state.song_queue,
        };
    },

    computed: {
        audio_index_playing: function () {
            return store.state.audio_index_playing;
        },

        audio_stream_paused: function () {
            return store.state.audio_stream_paused;
        }
    },

    methods: {
        play: function (i) {
            this.$store.commit("start_playing", i);
        },

        resume: function (i) {
            this.$store.commit("resume", i);
        },

        pause: function (i) {
            this.$store.commit("pause", i);
        },

        on_reorder: function (oldIndex, newIndex) {
            this.$store.commit("reorder_list", {old: oldIndex, new: newIndex});
        },

        remove: function (i) {
            this.$store.commit("remove_track_index", i);
        }
    },


});

/* the page with every single artist on it */
Vue.component('artists-view', {
    template: "#artists-view",
    store: store,
    computed: {
        library: function () {
            return store.state.library;
        }
    }
});

/* the page with all all artists + their albums */
Vue.component("all-albums-view", {
    template: "#all-albums-view",
    data: function () {
        return {};
    },
    store: store,
    computed: {
        library: function () {
            return store.state.library;
        }
    },
});

Vue.component("artist-albums-view", {
    template: '#artist-albums-view',
    store: store,
    computed: {
        artist_name: function () {
            return this.$route.params.artist;
        },

        artist_albums: function () {
            return store.state.library[this.$route.params.artist];
        },
    },
});

Vue.component("track-album-view", {
    template: "#track-album-view",
    store: store,
    methods: {
        enqueue: function (title) {
            var artist = this.$route.params.artist;
            var album = this.$route.params.album;
            this.$store.commit("add_to_queue",
                {"artist": artist, "album": album, "title": title});
        }
    },

    computed: {
        artist_name: function () {
            return this.$route.params.artist;
        },

        album_name: function () {
            return this.$route.params.album;
        },

        track_list: function () {
            if (typeof this.$route.params.artist == "undefined" ||
                typeof this.$route.params.album == "undefined")
                return [];

            return store.state.library[this.$route.params.artist][this.$route.params.album];
        }
    }
});

Vue.component('settings-view', {
    template: "#settings-view",
    methods: {
        signout: function (event) {
            Vue.http.options.emulateJSON = true;
            event.preventDefault();
            Vue.http.post('api/logout', {
                'session_id': Cookies.get('beaker.session.id')
            }).then(
                function success(response) {
                    /* TODO: basically force a page reload, this is gross find a better way */
                    window.location.href = "../../";
                },
                function failure(response) {
                    alert("Could not sign out, try again later.");
                }
            );
        },
        refresh_library: function () {
            this.$store.commit("refresh_library");
        }
    },
});
