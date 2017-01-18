/*
 * Inventory Login Model
 *
 * js/models/login_model.js
 */

var LoginModel = Backbone.Model.extend({
  urlRoot: appConfig.loginURL,
  defaults: {
    username: 'X',
    password: 'X',
    fullname: '',
    href: ''
  },
});

jQuery(function($) {
  App.loginModel = new LoginModel();
});
