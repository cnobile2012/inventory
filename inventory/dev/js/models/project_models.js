/*
 * Project models
 *
 * js/models/project_models.js
 */

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
    return this.href;
  }
});


jQuery(function($) {
  App.Collections.Projects = Backbone.Collection.extend({
    name: "Projects",
    model: App.Models.Project,

    initialize: function () {
      // Create project menu
      this.listenTo(this, 'change', function(model) {
        $('div#projects div.tab-choice-pane div').empty();
        var options = [], item = null;

        for(var i = 0; i < this.length; i++) {
          item = {title: '<a href="#project-' + i + '">'
                  + this.models[i].get('name') + '</a>'};
          options[i] = item;
        };

        App.collections.projectMenu = new App.Collections.MenuItems(options);

        App.views.projectMenu = new App.Views.ProjectMenu({
          collection: App.collections.projectMenu
        });

        App.views.projectMenu.render();
      });
    }
  });
});
