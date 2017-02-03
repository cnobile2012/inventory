/*
 * Inventory Logout Model
 *
 * js/models/logout_model.js
 */

jQuery(function($) {
  App.Models.Logout = Backbone.Model.extend({
    id: 'LogoutModel',
    url: function() {
      return App.rootModel.get('accounts').logout;
    },
    defaults: {}
  });


  App.logoutModel = new App.Models.Logout();
});
