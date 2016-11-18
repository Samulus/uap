/*
    route.js
    Author: Samuel Vargas
    Date: 11/10/2016
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
    store: store,
    computed: {
        audio_playing: function() {
            return store.state.audio_playing;
        }
    },
    router: router
});
