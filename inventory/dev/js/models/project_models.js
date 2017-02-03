/*
 * Project models
 *
 * js/models/project_models.js
 */

jQuery(function($) {
  App.Models.Project = Backbone.Model.extend({
    defaults: {
      public_id: '',
      name: '',
      members: [],
      memberships: [],
      invoices: '',
      items: '',
      inventory_type: '',
      public: false,
      active: false,
      creator: '',
      created: '',
      updater: '',
      updated: '',
      uri: ''
    },

    mutators: {
      invoices: {
        set: function(key, value, options, set) {
          set(key, value, options);

          if(value.length > 0) {
            App.picTimeout = setTimeout(populateInvoiceCollection, 200, value);
          }
        }
      }
    },

    url: function() {
      if (_.isUndefined(this.uri)) {
        return "";
      } else {
        return this.uri;
      }
    }
  });

  App.Collections.Projects = Backbone.Collection.extend({
    model: App.Models.Project});
});
