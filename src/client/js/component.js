/*
    component.js
    Author: Samuel Vargas
    Date: 10/31/2016

    * Include before client.js
*/

(function() {

    /* "Refresh Library" button */
    Vue.component('library-updater', {
        template: document.querySelector("template[id='library-updater']").innerHTML,
        methods: {
            demo: function() {
                this.$http.get('api/library').then(

                    (function(response) {
                        localStorage.setItem("library", JSON.parse(response.body))
                    }),

                    (function(error) {
                        console.log(error)
                    })
                )
            }
        }
    })

    Vue.component('nav-component', {
        template: document.querySelector("template[id='nav-component']").innerHTML
    })

    Vue.component('song-queue', {
        template: document.querySelector("template[id='song-queue']").innerHTML
    });

    Vue.component('artists-view', {
        template: document.querySelector("template[id='artists-view']").innerHTML
    });

})();
