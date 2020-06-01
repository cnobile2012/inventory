/*
 * Inventory Login Model
 *
 * js/app/accounts/login_model.js
 */

"use strict";


class LoginModel extends Backbone.Model {
  get id() { return 'LoginModel'; }
  get urlRoot() { return API_LOGIN; }
  get defaults() {
    return {
      username: 'X',
      password: 'X',
      fullname: '',
      href: ''
    };
  }
};
