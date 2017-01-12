/*
 * Inventory main entry point.
 *
 * js/main.js
 */

var appConfig = {
  baseURL: location.protocol + '//' + location.host + '/api/',
  loginURL: location.protocol + '//' + location.host + '/api/accounts/login/'
};

var App = {
  Models: {},
  Collections: {},
  Views: {},
  Router: {},
  rootModel: null,
  loginModel: null,
  loginView: null
};


var _csrfSafeMethod = function(method) {
  // These HTTP methods do not require CSRF protection.
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
};


var setHeader = function() {
  $.ajaxSetup({
    crossDomain: false,
    beforeSend: function(xhr, settings) {
      if(!_csrfSafeMethod(settings.type)) {
        xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
      }
    }
  });
};
