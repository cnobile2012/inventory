/*
 * Inventory Login Model
 *
 * js/models/login_model.js
 */

"use strict";


class Login extends Backbone.Model {
  get id() { return 'LoginModel'; }
  get urlRoot() { return API_LOGIN; }
  get defaults() {
    return {
      username: 'X',
      password: 'X',
      fullname: '',
      href: ''
    };
  }
};


jQuery(function($) {
  App.loginModel = new Login();
});
