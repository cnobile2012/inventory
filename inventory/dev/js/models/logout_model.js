/*
 * Inventory Logout Model
 *
 * js/models/logout_model.js
 */

"use strict";


App.Models.Logout = Backbone.Model.extend({
  id: 'LogoutModel',
  defaults: {},
  urlRoot: function() {
    return App.models.rootModel.get('accounts').logout;
  }
});


jQuery(function($) {
  App.models.logoutModel = new App.Models.Logout();
});
