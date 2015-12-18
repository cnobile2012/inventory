/*
 * regions.js
 *
 * Requires: inheritance.js and jquery.js
 *
 * Carl J. Nobile
 */

(function($) {
  'use strict';

  var Region = Class.extend({
    _CONTACT_SERVER_TXT: "Getting list of regions please wait...",
    _SOURCE_ID: '#id_country',
    _TARGET_ID: '#id_region',
    _API_URI: '/api/v1/regions/country/',

    init: function() {
      this._setupSubmit();
    },

    _setupSubmit: function() {
      var country = $(this._SOURCE_ID);
      country.on('change', this._processRegionRequest.bind(this));

      //if(country[0].value != "") {
      //  this._processRegionRequest();
      //}
    },

    _csrfSafeMethod: function(method) {
      // These HTTP methods do not require CSRF protection.
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    },

    _setHeader: function() {
      $.ajaxSetup({
        crossDomain: false,
        beforeSend: function(xhr, settings) {
          if (!this._csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
          }
        }.bind(this)
      });
    },

    _processRegionRequest: function() {
      var countryId = $('select'+this._SOURCE_ID)
          .find("option:selected").val();
      var $targetSelect = $('select'+this._TARGET_ID);
      this._regionId = parseInt($targetSelect.find("option:selected").val());
      $targetSelect.find('option').remove();

      if(countryId) {
        this._setHeader();
        var options = {
          headers: {Accept: "application/json"},
          url: (location.protocol + "//" + location.host + this._API_URI +
                countryId + "/"),
          cache: false,
          type: 'GET',
          timeout: 20000, // 20 seconds
          success: this._regionCB.bind(this),
          statusCode: {400: this._error400CB.bind(this)},
        };

        $.ajax(options);
      }
    },

    _regionCB: function(json, status) {
      if(json.active) {
        var direction = null;
        var regions = json.regions;

        // Reverse the order for IE.
        //if(document.all) {
        //  regions.reverse();
        //  direction = 1;
        //}

        for(var i = 0; i < regions.length; i++) {
          var option = new Option(regions[i].region, regions[i].id);
          $('select'+this._TARGET_ID).get(0).add(option, direction);

          if(regions[i].id == this._regionId) {
            option.selected = true;
          }
        }
      } else if(json.detail) {
        this._mimicDjangoErrors({region: json.detail});
      } else {
        this._mimicDjangoErrors({country: "Inactive country, choose another."});
      }
    },

    _error400CB(request, textStatus, exception) {
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
      this._mimicDjangoErrors({country: "Bad Request"});
    },

    _mimicDjangoErrors: function(data) {
      // Mimic Django error messages.
      var ul = '<ul class="errorlist"></ul>';
      var li = '<li></li>'
      var $errorUl = null;
      var $errorLi = null;
      var $li = null;

      for(var key in data) {
        $li = $('select[name=' + key +
          '], input[name=' + key + '], textarea[name=' + key + ']').parent();
        $errorUl = $(ul);

        for(var i = 0; i < data[key].length; i++) {
          $errorLi = $(li);
          $errorLi.html(data[key][i]);
          $errorLi.appendTo($errorUl);
        }

        $errorUl.appendTo($li);
      }
    }
  });

  $(document).ready(function() {
    new Region();
  });
})(django.jQuery);
