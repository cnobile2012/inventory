/*
 * Inventory main entry point.
 *
 * js/main.js
 */

var appConfig = {
  baseURL: location.protocol + '//' + location.host + '/api/'
};

var App = {
  Models: {},
  Collections: {},
  Views: {},
  Router: {},
  rootModel: null
};
