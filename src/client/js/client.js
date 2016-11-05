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
            library: JSON.parse(localStorage.getItem("library"))
        },
        mutations: {
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

    Vue.component("albums-view", {
        template: '#albums-view',
        store: store,
        computed: {
            viewing_specific_artist: function() {
                return Object.keys(this.$route.params).length == 1;
            },

            artist_name: function() {
                return Object.keys(this.$route.params).length == 0 ?
                    "Albums" : this.$route.params.artist
            },

            artist_albums: function() {
                return store.state.library[this.artist_name];
            },

            library: function() {
                return store.state.library;
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
      { path: '/albums/:artist', component: 'albums-view' },
      { path: '/albums',  component: 'albums-view' },
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
