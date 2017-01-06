/*
 * Inventory main entry point.
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
