/*
    route.js
    Author: Samuel Vargas
    Date: 11/10/2016
*/

var routes = [
    {path: '/artists', component: 'artists-view'},
    {path: '/albums/:artist', component: 'artist-albums-view'},
    {path: '/albums', component: 'all-albums-view'},
    {path: '/albums/:artist/:album', component: 'track-album-view'},
    {path: '/queue', component: "song-queue-view"},
    {path: '/genres', component: "genre-view"},
    {path: '/settings', component: "settings-view"},
    {path: '/search', component: "search-view"},
    {path: '/', redirect: '/queue', component: 'song-queue'}
];

var router = new VueRouter({routes: routes});

var app = new Vue({
    el: '#app',
    store: store,
    computed: {
        audio_playing: function () {
            return store.state.audio_playing;
        }
    },
    router: router
});
