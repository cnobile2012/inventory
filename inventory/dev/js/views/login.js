/*
 * Inventory Login
 *
 * js/views/login.js
 */

jQuery(function($) {
  if(!IS_AUTHENTICATED) {
    // Create a modal view class
    var LoginModalView = Backbone.Modal.extend({
      template: $.tpl.login_template(),
      cancelEl: '.bbm-button'
    });

    $('<div id="login-modal"></div>').appendTo($('body'));
    App.loginView = new LoginModalView();
    $('#login-modal').html(App.loginView.render().el);
  }
});



/* var _BaseModal = Class.extend({ */

/*   _csrfSafeMethod: function(method) { */
/*     // These HTTP methods do not require CSRF protection. */
/*     return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method)); */
/*   }, */

/*   _setHeader: function() { */
/*     $.ajaxSetup({ */
/*       crossDomain: false, */
/*       beforeSend: function(xhr, settings) { */
/*         if (!this._csrfSafeMethod(settings.type)) { */
/*           xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken')); */
/*         } */
/*       }.bind(this) */
/*     }); */
/*   }, */

/*   setDefault: function(obj, key, value) { */
/*     if(key in obj) { */
/*       return obj[key]; */
/*     } else { */
/*       obj[key] = value; */
/*       return obj[key]; */
/*     } */
/*   } */
/* }); */




/* var Login = function() { */
/*     this._setupSubmit(); */
/* }; */


/* Login.prototype = { */
/*   _FORM_LOAD_TXT: "Wait while loading the form ...", */

/*   _setupSubmit: function() { */
/*     //$('.createUser').click(this._createUserForm); */
/*     var request = null; */

/*     if($('#login_template').length != 0) { */
/*       request = this._loginRequest; */
/*     } else if($('#put-something-here').length != 0) { */
/*       request = this._createUserRequest; */
/*     } else { */
/*       $('#messages').text("Programming error incorrect CSS class."); */
/*       $('#messages').show(); */
/*       return; */
/*     } */

/*     $('form#form').submit(request.bind(this)); */
/*     $('input#id_username').focus(); */
/*   }, */

/*   _createUserForm: function() { */
/*     window.location = "/login/createUser/"; */
/*   }, */

/*   _createUserRequest: function() { */
/*     this._setMessage('Submitted create user request!!'); */
/*     var username = $("input#id_username")[0].value; */
/*     var password1 = $("input#id_password1")[0].value; */
/*     var password2 = $("input#id_password2")[0].value; */
/*     var email = $('input#id_email')[0].value; */
/*     json = {"username": username, "password1": password1, */
/*             "password2": password2, "email": email}; */
/*     this._callAjax("post", this._assembleURI("/login/processCreateUser/"), */
/*                    json, this._createUserCB); */
/*   }, */

/*   _createUserCB: function(json, status) { */
/*     if(json["valid"]) { */
/*       this._setMessage(true, function() { */
/*         $('#content').empty(); */
/*         window.location = "/"; */
/*       }); */
/*     } else { */
/*       this._setMessage(""); */
/*       $('#content').empty(); */
/*       $('div#content').append(json["content"]); */
/*       $('input#id_username').focus(); */
/*       $('input#id_password1').empty(); */
/*       $('input#id_password2').empty(); */
/*       $('form#form').submit(this._createUserRequest.bind(this)); */
/*     } */
/*   }, */

/*   _loginRequest: function() { */
/*     this._setMessage('Processing request please wait!!!'); */
/*     var username = $("input#id_username")[0].value; */
/*     var password = $("input#id_password")[0].value; */
/*     var json = {"username": username, "password": password}; */
/*     this._callAjax("post", this._assembleURI("/login/validate/"), json, */
/*                    this._loginCB); */
/*   }, */

/*   _loginCB: function(json, status) { */
/*     if(json["valid"]) { */
/*       if(!json["cookies"]) { */
/*         window.location = "/"; */
/*       } */

/*       this._setMessage(json["message"]); */
/*       this._setMessage(true, function() { */
/*         location.reload(true); */
/*       }); */

/*       // Debug only */
/*       //$('div#reportError').text(json.toString()); */
/*       var redirect = $('span#redirect').text(); */

/*       if(redirect == "None") { */
/*         redirect = "/"; */
/*       } */

/*       window.location = redirect; */
/*     } else { */
/*       this._setMessage(json["message"]); */
/*     } */
/*   } */
/* }; */


/* if(!IS_AUTHENTICATED) { */
/*   new Login(); */
/* } */
