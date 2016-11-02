/**
    client.js
    Author: Samuel Vargas
    Date: 10/31/2016

    * Include after component.js
   
*/

(function() {


    /*
        Routing
    */

    Vue.use(VueRouter);

    const routes = [
      { path: '/artists', component: 'artists-view' },
      { path: '/queue', component: "song-queue" }
    ]

    const router = new VueRouter({routes})

    const app = new Vue({
        el: '#app',
        router: router
    });

})();
