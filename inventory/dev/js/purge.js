/*
 * purge.js
 *
 * CVS/SVN Keywords
 *------------------------------
 * $Author: cnobile $
 * $Date: 2011-11-10 20:29:49 -0500 (Thu, 10 Nov 2011) $
 * $Revision: 54 $
 *------------------------------
 */

var Purge = function() {
  this._setupSubmit();
  this._CONFIRM_REQUEST = null;
  this._DELETE_REQUEST = null;
};


Purge.prototype = {
  _CONTACT_SERVER_TXT: "Wait while contacting the server...",

  _setupSubmit: function() {
    this._CONFIRM_REQUEST = this._confirmationRequest.bind(this);
    this._DELETE_REQUEST = this._deleteRequest.bind(this);
    $('form#form').submit(this._CONFIRM_REQUEST);
    $('input#search').click(function() {
       window.location = "/maintenance/purge/";
     });
    $('input#reset').click(function () {
       this._setMessage("");
     }.bind(this));
  },

  _confirmationRequest: function() {
    this._setMessage(this._CONTACT_SERVER_TXT);
    this._callAjax("post", this._assembleURI("/maintenance/confirm/"),
     this._createJSON(), this._confirmationCB);
  },

  _confirmationCB: function(json, status) {
    this._setMessage(json['message']);

    if(json['valid']) {
      $('form#form').unbind('submit',  this._CONFIRM_REQUEST);
      $('form#form').bind('submit', this._DELETE_REQUEST);
    }
  },

  _deleteRequest: function() {
    this._callAjax("post", this._assembleURI("/maintenance/delete/"),
     this._createJSON(), this._deleteCB);
  },

  _deleteCB: function(json, status) {
    this._setMessage(json["message"]);

    if(json['valid']) {
      $('td input[type=checkbox]').each(function() {
        if(this.checked) {
          $(this).parent().parent().remove();
        }
       });
    }

    $('form#form').unbind('submit', this._DELETE_REQUEST);
    $('form#form').bind('submit', this._CONFIRM_REQUEST);
    this._setMessage(true);
  },

  _createJSON: function() {
    var checkboxes = $('td > input[type=checkbox]');
    var pks = [];

    for(var i = 0; i < checkboxes.length; i++) {
      var box = checkboxes[i];

      if(box.checked) {
        var node = $(box).parent().parent().find("td > input[type=hidden]");
        pks[i] = node[0].value;
      }
    }

    var json = {pks: pks};
    return json;
  }
};


$(document).ready(function() {
  extend(Purge, AjaxBase);
  new Purge();
});
