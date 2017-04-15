/*
 * Inventory Login Model
 *
 * js/models/login_model.js
 */

"use strict";


App.Models.Login = Backbone.Model.extend({
  id: 'LoginModel',
  urlRoot: API_LOGIN,
  defaults: {
    username: 'X',
    password: 'X',
    fullname: '',
    href: ''
  }
});


jQuery(function($) {
  App.loginModel = new App.Models.Login();
});
