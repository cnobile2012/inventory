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

App.loginModel = new LoginModel();
