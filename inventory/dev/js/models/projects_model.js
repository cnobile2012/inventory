/*
 * Project models
 *
 * js/models/projects_model.js
 */

var ProjectModel = Backbone.Model.extend({
  defaults: {
    public_id: '',
    name: '',
    members: [],
    memberships: [],
    inventory_type: '',
    public: false,
    active: false,
    creator: '',
    created: '',
    updater: '',
    updated: '',
    uri: ''
  },

  url: function() {
    if (_.isUndefined(this.uri)) {
      return "";
    } else {
      return this.uri;
    }
  }
});

jQuery(function($) {
  //  App.userModel = new projectModel();
});
