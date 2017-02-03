/*
 * Inventory Login Model
 *
 * js/models/login_model.js
 */

jQuery(function($) {
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

  App.loginModel = new App.Models.Login();
});
