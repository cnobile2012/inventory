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
  models: {},
  collections: {},
  views: {},
  invoiceTimeout: null,
  itemTimeout: null,
  utils: null
};


// Can only run this function after initial load has completed.
window.destroyApp = function() {
  App.Views = {};
  App.Router = {};
  App.models.rootModel.clear().set(App.models.rootModel.defaults);
  App.models.loginModel.clear().set(App.models.loginModel.defaults);
  App.models.logoutModel.clear().set(App.models.logoutModel.defaults);
  App.models.userModel.clear().set(App.models.userModel.defaults);
  App.collections = {};
  App.picTimeout = null;
};


var Utilities = function() {
  this.initialize();
};

Utilities.prototype = {

  initialize: function() {
  },

  _csrfSafeMethod: function(method) {
    // These HTTP methods do not require CSRF protection.
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  },

  setHeader: function() {
    $.ajaxSetup({
      crossDomain: false,
      beforeSend: function(xhr, settings) {
        if(!_csrfSafeMethod(settings.type)) {
          xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
        }
      }
    });
  },

  errorCB: function(jqXHR, status, errorThrown) {
    try {
      var json = $.parseJSON(jqXHR.responseText);
      var msg = '';

      for(var key in json) {
        msg += key + ": " + json[key] + "<br />";
      }

      this.showMessage(msg);
    } catch (e) {
      this.showMessage(jqXHR.statusText + ": " + jqXHR.status);
    }
  },

  showMessage: function(message, fade) {
    var $messages = $('#messages');
    $messages.html(message);
    $messages.show();

    if(fade !== (void 0) && fade === true) {
      $messages.fadeOut(7500);
    }
  },

  hideMessage: function() {
    var $messages = $('#messages');
    $messages.html("");
    $messages.hide();
  },

  mimicDjangoErrors: function(elm, data) {
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
  }
};

window.App.utils = new Utilities();
