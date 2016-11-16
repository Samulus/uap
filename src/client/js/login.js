/*
    login.js
    Author: Samuel Vargas
    Date: 11/14/2016
*/

Vue.http.options.emulateJSON = true;
var login_vm = new Vue({
    template: "#login-component",
    el: "#login",
    data: {
        got_message_from_server: false,
        message: '',
        username: '',
        password: '',
    },

    methods: {
        action: function(action_type, event) {
            event.preventDefault();
            Vue.http.post('api/' + action_type, {
                'username': this.$data.username,
                'password': this.$data.password,
            }).then(
                function success(response) {
                    location.reload()
                },
                function failure(response) {
                    login_vm.$data.got_message_from_server = true;
                    login_vm.$data.message = response.statusText;
                    setTimeout(function() {
                        login_vm.$data.got_message_from_server = false;
                    }, 3000);
                }
            );
        }
    }

});
