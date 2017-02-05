/*
 * Inventory main entry point.
 *
 * js/main.js
 */

"use strict";

var appConfig = {
  baseURL: location.protocol + '//' + location.host + '/api/',
  loginURL: location.protocol + '//' + location.host + '/api/accounts/login/'
};


window.App = {
  Models: {},
  Collections: {},
  Views: {},
  Router: {},
  rootModel: null,
  loginModel: null,
  logoutModel: null,
  userModel: null,
  collections: {},
  invoiceTimeout: null,
  itemTimeout: null
};


// Can only run this function after initial load has completed.
window.destroyApp = function() {
  App.Views = {};
  App.Router = {};
  App.rootModel.clear().set(App.rootModel.defaults);
  App.loginModel.clear().set(App.loginModel.defaults);
  App.logoutModel.clear().set(App.logoutModel.defaults);
  App.userModel.clear().set(App.userModel.defaults);
  App.collections = {};
  App.picTimeout = null;
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


var mimicDjangoErrors = function(elm, data) {
  // Mimic Django error messages.
  var ul = '<ul class="errorlist"></ul>';
  var li = '<li></li>';
  var $tag = null, $errorUl = null, $errorLi = null;
  $('ul.errorlist').remove();

  for(var key in data) {
    $tag = $('select[name=' + key + '], input[name=' + key +
      '], textarea[name=' + key + ']');
    $errorUl = $(ul);

    if($tag.prev().prop('tagName') === 'LABEL') {
      $tag = $tag.prev();
      $errorUl.insertBefore($tag);
    } else if($tag.length === 0) {
      $tag = $(elm);
      $errorUl.appendTo($tag);
    }

    for(let i = 0; i < data[key].length; i++) {
      $errorLi = $(li);
      $errorLi.html(data[key][i]);
      $errorLi.appendTo($errorUl);
    }
  }
};
