/*
 * Inventory main entry point.
 *
 * js/main.js
 */

var appConfig = {
  baseURL: location.protocol + '//' + location.host + '/api/',
  loginURL: location.protocol + '//' + location.host + '/api/login/'
};

var App = {
  Models: {},
  Collections: {},
  Views: {},
  Router: {},
  rootModel: null,
  loginView: null
};
