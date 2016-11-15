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
        error: false,
        error_message: '',
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
                    console.log('EVERYTHING IS PEACHY KEEN');
                    console.log(response.statusText);
                    alert(response.statusText);
                },
                function failure(response) {
                    login_vm.$data.error = true;
                    login_vm.$data.error_message = response.statusText;
                    setTimeout(function() {
                        login_vm.$data.error = false;
                    }, 3000);
                }
            );
        }
    }

});
