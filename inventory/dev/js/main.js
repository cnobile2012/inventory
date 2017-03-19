/*
 * Inventory main entry point.
 *
 * js/main.js
 *
 * Variables used from HTML
 * ========================
 * IS_AUTHENTICATED
 * USER_HREF
 * USERNAME
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
  //Routers: {},
  models: {},
  collections: {},
  views: {},
  templates: null,
  loginModel: null,
  utils: null,
  invoiceTimeout: null,
  itemTimeout: null
};


// This function is run when logout happens, so that all data for the
// user is removed.
window.destroyApp = function() {
  App.models = {};
  App.collections = {};
  App.views = {};
  App.loginModel.clear().set(App.loginModel.defaults);
  App.invoiceTimeout = null;
  App.itemTimeout = null;
  $('div.tab-choice-pane div').not(':first').remove();
  $('div.tab-choice-pane div').empty();
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
        if(!this._csrfSafeMethod(settings.type)) {
          xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
        }
      }.bind(this)
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
  },

  // Set a default value on an object key--similar to Python's
  // <dict>.setdefault(<key>, value).
  setDefault: function(obj, key, value) {
    if(key in obj) {
      return obj[key];
    } else {
      obj[key] = value;
      return obj[key];
    }
  }
};

window.App.utils = new Utilities();
