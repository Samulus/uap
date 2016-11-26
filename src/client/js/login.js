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
        password: ''
    },

    methods: {
        action: function (action_type, event) {
            event.preventDefault();
            this.$http.post('api/' + action_type, {
                'username': this.$data.username,
                'password': sha512(this.$data.password),
            }).then(
                function success(response) {
                    location.reload();
                },
                function failure(response) {
                    this.$data.got_message_from_server = true;
                    this.$data.message = response.statusText;
                    setTimeout(function () {
                        this.$data.got_message_from_server = false;
                    }, 3000);
                }
            );
        },
    }

});
