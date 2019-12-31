/*
 * Inventory Logout Model
 *
 * js/app/models/logout_model.js
 */

"use strict";


class LogoutModel extends Backbone.Model {
  get id() { return 'LogoutModel'; }
  get defaults() { return {}; }

  get urlRoot() {
    return App.models.rootModel.get('accounts').logout.href;
  }
};

App.Models.LogoutModel = LogoutModel;
