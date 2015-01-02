/*
 * regions.js
 *
 * CVS/SVN Keywords
 *------------------------------
 * $Author: cnobile $
 * $Date: 2011-11-10 20:29:49 -0500 (Thu, 10 Nov 2011) $
 * $Revision: 54 $
 *------------------------------
 */

var Region = function() {
  this._setupSubmit();
};


Region.prototype = {
  _CONTACT_SERVER_TXT: "Getting list of regions please wait...",
  _SELECT_ID: "id_state",

  _setupSubmit: function() {
    var country = $('#id_country');
    country.change(this._processRegionRequest.bind(this));

    if(country[0].value != "") {
      this._processRegionRequest();
    }
  },

  _processRegionRequest: function() {
    //this._setMessage(this._CONTACT_SERVER_TXT);
    $('select#'+this._SELECT_ID).find('option:gt(0)').remove();
    $('select#'+this._SELECT_ID).find('option:eq(0)').remove();
    this._callAjax("post", this._assembleURI("/lookup/regions/"),
     this._createJSON(), this._regionCB);
  },

  _regionCB: function(json, status) {
    if(json['valid']) {
      var direction = null;
      var regions = json['regions'];

      // Reverse the order for IE.
      if(document.all) {
        regions.reverse();
        direction = 1;
      }

      var selected = json['selected'];

      for(var i = 0; i < regions.length; i++) {
        var option = new Option(regions[i][0], regions[i][1]);
        $('select#'+this._SELECT_ID).get(0).add(option, direction);

        if(selected == regions[i][1]) {
          option.selected = true;
        }
      }
    } else {
      //this._setMessage(json['message']);
    }
  },

  _createJSON: function() {
    var country = $('select#id_country').find("option:selected")[0].text;
    return {country: country, pathname: location.pathname};
  }
};


$(document).ready(function() {
  extend(Region, AjaxBase);
  new Region();
});
