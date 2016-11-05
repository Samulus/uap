/*
    client.js
    Author: Samuel Vargas
    Date: 10/31/2016
*/

(function() {

    /*
        State Management
    */

    const store = new Vuex.Store({

        state: {
            library: JSON.parse(localStorage.getItem("library")),
            song_queue: [],
        },

        mutations: {

            add_song_to_queue: function() {
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

    /*
        Components
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
    Vue.component('song-queue', {template: "#song-queue"});
    Vue.component('genre-view', {template: "#genre-view"});

    /*
        Routing
    */

    const routes = [
      { path: '/artists', component: 'artists-view' },
      { path: '/albums/:artist', component: 'artist-albums-view' },
      { path: '/albums',  component: 'all-albums-view' },
      { path: '/albums/:artist/:album', component: 'track-album-view' },
      { path: '/queue',  component: "song-queue" },
      { path: '/genres', component: "genre-view" },
      { path: '/',       redirect: '/queue', component: 'song-queue' },
    ];

    const router = new VueRouter({routes: routes});

    const app = new Vue({
        el: '#app',
        router: router
    });

})();
