/*
 * Inventory Logout Model
 *
 * js/models/logout_model.js
 */

App.Models.Logout = Backbone.Model.extend({
  id: 'LogoutModel',
  url: function() {
    return App.models.rootModel.get('accounts').logout;
  },
  defaults: {}
});


jQuery(function($) {
  App.models.logoutModel = new App.Models.Logout();
});
