/*
 * ajaxbase.js
 *
 * CVS/SVN Keywords
 *------------------------------
 * $Author: cnobile $
 * $Date: 2013-06-29 18:35:56 -0400 (Sat, 29 Jun 2013) $
 * $Revision: 71 $
 *------------------------------
 */

Function.prototype.bind = function(object) {
  var method = this;
  temp = function () {
    return method.apply(object, arguments);
  };

  return temp;
}

var extend = function(child, base) {
  if(!document.all) {
    child.prototype.__proto__ = base.prototype;
    child.prototype.__super = base;
  } else {
    for(var property in base.prototype) {
      if(typeof child.prototype[property] == "undefined") {
        child.prototype[property] = base.prototype[property];
      }
    }
  }
};


var AjaxBase = function() {
};

AjaxBase.prototype = {

  _csrfSafeMethod: function(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  },

  _beforeSetup: function(xhr, settings) {
    if (!this._csrfSafeMethod(settings.type)) {
      // Send the token to same-origin, relative URLs only.
      // Send the token only if the method warrants CSRF protection
      xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
    }
  },

  _errorCB: function(request, textStatus, exception) {
    var rStatus = null;
    var rText = null;

    // See: https://bugzilla.mozilla.org/show_bug.cgi?id=238559#c0
    try {
      rStatus = request.status;
      rText = request.statusText;
    } catch (e) {
      //rStatus = e;
      //rText = " ";
    }

    var msg = (rStatus && rText ? rStatus + " " + rText : "");
    var status = (textStatus != undefined ? textStatus
                                          : (exception != undefined
                                          ? exception : ""));
    status = "AJAX " + status + ": " + msg;
    this._setMessage(status);
  },

  _callAjax: function(method, url, json, callback, dataType) {
    if(dataType == undefined) {
      var dataType = "json";
    }

    try {
      $.ajaxSetup({
        crossDomain: false, // Must use jquery >= 1.5.1
        beforeSend: this._beforeSetup.bind(this)
      });

      $.ajax({url: url,
              cache: false,
              type: method,
              dataType: dataType,
              data: json,
              timeout: 20000, // 20 seconds
              error: this._errorCB.bind(this),
              success: callback.bind(this),
              traditional: true
             });
    } catch (e) {
      this._setMessage(e);
    }
  },

  _setMessage: function(msg, func) {
    if(typeof(msg) == "boolean" && msg == true) {
      if(func == undefined) {
        func = function() {
         $('div#message').empty();
         $('div#message').show();
        }
      }

      $('div#message').fadeOut(5000, func);
    } else {
      $('div#message').empty();
      $('div#message').text(msg);
    }

    $('div#message').show();
  },

  _assembleURI: function(path) {
    return location.protocol + "//" + location.host + path;
  }
};
