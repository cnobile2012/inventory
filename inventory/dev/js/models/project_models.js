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
      invoices: [],
      invoices_href: '',
      items: [],
      items_href: '',
      inventory_type: '',
      public: false,
      active: false,
      creator: '',
      created: '',
      updater: '',
      updated: '',
      href: ''
    },

    mutators: {
      invoices_href: {
        set: function(key, value, options, set) {
          set(key, value, options);

          if(value.length > 0) {
            App.invoiceTimeout = setTimeout(populateInvoiceCollection, 200,
                                            value, this);
          }
        }
      },

      items_href: {
        set: function(key, value, options, set) {
          set(key, value, options);

          if(value.length > 0) {
            App.itemTimeout = setTimeout(populateItemCollection, 200,
                                         value, this);
          }
        }
      },
    },

    url: function() {
      return this.uri;
    }
  });

  App.Collections.Projects = Backbone.Collection.extend({
    name: "Projects",
    model: App.Models.Project});
});
