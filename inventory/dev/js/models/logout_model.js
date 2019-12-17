/*
 * Inventory Logout Model
 *
 * js/models/logout_model.js
 */

"use strict";


class Logout extends Backbone.Model {
  get id() { return 'LogoutModel'; }
  get defaults() { return {}; }

  get urlRoot() {
    return App.models.rootModel.get('accounts').logout.href;
  }
};


jQuery(function($) {
  App.models.logoutModel = new Logout();
});
