/*
 * Inventory Login Model
 *
 * js/models/login.js
 */

var LoginModel = Backbone.Model.extend({
  urlRoot: appConfig.loginURL,
  defaults: {
    username: '',
    password: '',
    fullname: '',
    href: ''
  },
});

App.loginModel = new LoginModel();
