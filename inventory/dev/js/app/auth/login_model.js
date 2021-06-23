/*
 * Inventory Login Model
 *
 * js/app/auth/login_model.js
 */

"use strict";


class LoginModel extends Backbone.Model {
  get id() { return 'LoginModel'; }
  get urlRoot() { return API_LOGIN; }
  get defaults() {
    return {
      fullname: '',
      href: ''
    };
  }
};
