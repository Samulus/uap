/*
    bind.js
    Author: Samuel Vargas
    Date: 10/22/2016
    
    Extremely rudimentary demo of using vue.js for dynamic
    tab switching
*/

(function() {

    var view_queue = new Vue({
        el: "#VUE_view_queue",
        methods: {
            viewTab: function(e) {
                document.getElementById("VUE_view").innerHTML =
                document.getElementById("VUE_queue").innerHTML;
            }
        }
    });

    var view_queue = new Vue({
        el: "#VUE_view_library",
        methods: {
            viewTab: function(e) {
                document.getElementById("VUE_view").innerHTML =
                document.getElementById("VUE_library").innerHTML;
            }
        }
    });

    var view_queue = new Vue({
        el: "#VUE_view_settings",
        methods: {
            viewTab: function(e) {
                document.getElementById("VUE_view").innerHTML =
                document.getElementById("VUE_settings").innerHTML;
            }
        }
    });

})();
