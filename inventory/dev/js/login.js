/*
 * login.js
 *
 * CVS/SVN Keywords
 *------------------------------
 * $Author: cnobile $
 * $Date: 2011-11-10 20:29:49 -0500 (Thu, 10 Nov 2011) $
 * $Revision: 54 $
 *------------------------------
 */

var Login = function() {
    this._setupSubmit();
};


Login.prototype = {
  _FORM_LOAD_TXT: "Wait while loading the form ...",

  _setupSubmit: function() {
    $('.createUser').click(this._createUserForm);
    var request = null;

    if($('#content ul.login').length != 0) {
      request = this._loginRequest;
    } else if($('#content ul.create').length != 0) {
      request = this._createUserRequest;
    } else {
      this._setMessage("Programming error incorrect CSS class.");
      return;
    }
    
    $('form#form').submit(request.bind(this));
    $('input#id_username').focus();
  },

  _createUserForm: function() {
    window.location = "/login/createUser/";
  },

  _createUserRequest: function() {
    this._setMessage('Submitted create user request!!');
    var username = $("input#id_username")[0].value;
    var password1 = $("input#id_password1")[0].value;
    var password2 = $("input#id_password2")[0].value;
    var email = $('input#id_email')[0].value;
    json = {"username": username, "password1": password1,
            "password2": password2, "email": email};
    this._callAjax("post", this._assembleURI("/login/processCreateUser/"),
                   json, this._createUserCB);
  },

  _createUserCB: function(json, status) {
    if(json["valid"]) {
      this._setMessage(true, function() {
        $('#content').empty();
        window.location = "/";
      });
    } else {
      this._setMessage("");
      $('#content').empty();
      $('div#content').append(json["content"]);
      $('input#id_username').focus();
      $('input#id_password1').empty();
      $('input#id_password2').empty();
      $('form#form').submit(this._createUserRequest.bind(this));
    }
  },

  _loginRequest: function() {
    this._setMessage('Processing request please wait!!!');
    var username = $("input#id_username")[0].value;
    var password = $("input#id_password")[0].value;
    var json = {"username": username, "password": password};
    this._callAjax("post", this._assembleURI("/login/validate/"), json,
                   this._loginCB);
  },

  _loginCB: function(json, status) {
    if(json["valid"]) {
      if(!json["cookies"]) {
        window.location = "/";
      }

      this._setMessage(json["message"]);
      this._setMessage(true, function() {
        location.reload(true);
      });

      // Debug only
      //$('div#reportError').text(json.toString());
      var redirect = $('span#redirect').text();

      if(redirect == "None") {
        redirect = "/";
      }

      window.location = redirect;
    } else {
      this._setMessage(json["message"]);
    }
  }
};


$(document).ready(function() {
  extend(Login, AjaxBase);
  new Login();
});
