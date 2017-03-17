/*
 * Inventory Login Model
 *
 * js/models/login_model.js
 */

App.Models.Login = Backbone.Model.extend({
  id: 'LoginModel',
  urlRoot: appConfig.loginURL,
  defaults: {
    username: 'X',
    password: 'X',
    fullname: '',
    href: ''
  },
});


jQuery(function($) {
  App.models.loginModel = new App.Models.Login();
});
