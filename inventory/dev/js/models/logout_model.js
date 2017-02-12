/*
 * Inventory Logout Model
 *
 * js/models/logout_model.js
 */

jQuery(function($) {
  App.Models.Logout = Backbone.Model.extend({
    id: 'LogoutModel',
    url: function() {
      return App.models.rootModel.get('accounts').logout;
    },
    defaults: {}
  });


  App.models.logoutModel = new App.Models.Logout();
});
