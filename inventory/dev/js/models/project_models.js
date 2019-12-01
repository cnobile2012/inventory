/*
 * Project models
 *
 * js/models/project_models.js
 */

"use strict";


// InventoryType
App.Models.InventoryType = Backbone.Model.extend({
  urlRoot: function() {
    return App.models.rootModel.get('projects').inventory_types.href;
  }
});


App.Models.InventoryTypeMeta = App.Models.BaseMetaModel.extend({
  urlRoot: function() {
    return App.models.rootModel.get('projects').inventory_type.href;
  }
});


App.Collections.InventoryType = Backbone.Collection.extend({
  name: "InventoryType",
  model: App.Models.InventoryType,

  initialize: function () {
  },

  parse: function(response, options) {
    var models = response.results;
    App.models.inventoryTypeMeta.set({
      count: response.count,
      next: response.next,
      previous: response.previous
    });
    return models;
  },

  url: function() {
    return App.models.rootModel.get('projects').inventory_types.href;
  }
});


// Project
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
          App.invoiceTimeout = setTimeout(App.utils.fetchInvoiceCollection,
                                          200, value, this);
        }
      }
    },

    items_href: {
      set: function(key, value, options, set) {
        set(key, value, options);

        if(value.length > 0) {
          App.itemTimeout = setTimeout(App.utils.fetchItemCollection,
                                       200, value, this);
        }
      }
    },

    creator: function() {
      var name = "Not Found";
      var href = this.attributes.creator;
      var userHREF = App.models.userModel.get('href');

      // Check if it's the current user first.
      if(href === userHREF) {
        name = App.models.userModel.get('full_name');
      } else {
        // Get the creator with the 'href'.
      }

      return name;
    },

    created: function() {
      return new Date(this.attributes.created).toLocaleString();
    },

    updater: function() {
        var name = "Not Found",
            href = this.attributes.updater,
            userHREF = App.models.userModel.get('href');

      // Check if it's the current user first.
      if(href === userHREF) {
        name = App.models.userModel.get('full_name');
      } else {
        // Get the updater with the 'href'.
      }

      return name;
    },

    updated: {
      get: function() {
        return new Date(this.attributes.updated).toLocaleString();
      }
    }
  },

  urlRoot: function() {
    return this.get('href');
  }
});


App.Models.ProjectMeta = App.Models.BaseMetaModel.extend({
  urlRoot: function() {
    return App.models.rootModel.get('projects').projects.href;
  }
});


App.Collections.Projects = Backbone.Collection.extend({
  name: "Projects",
  model: App.Models.Project,

  initialize: function () {
    // Create project menu
    this.listenTo(this, 'change', function(model) {
      $('div#projects div.tab-choice-pane div').empty();
        var options = [],
            item = null,
            model = null,
            data = "";

      for(var i = 0; i < this.length; i++) {
        model = this.at(i);
        data = model.get('public_id');
        item = {title: '<a href="#project' + i + '" data="' + data + '" >'
                + model.get('name') + '</a>'};
        options[i] = item;
      }

      App.collections.projectMenu = new App.Collections.MenuItems(options);

      App.views.projectMenu = new App.Views.ProjectMenu({
        collection: App.collections.projectMenu
      });

      App.views.projectMenu.render();
    });
  }
});
