/*
 * Invoice models
 *
 * js/models/invoice_models.js
 */

jQuery(function($) {
   App.Models.Invoices = Backbone.Model.extend({
    defaults: {
      public_id: '',
      project: null,
      currency: null,
      supplier: null,
      invoices_number: '',
      invoice_date: '',
      credit: 0,
      shipping: 0,
      other: 0,
      tax: 0,
      notes: '',
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

  App.Models.InvoicesMeta = Backbone.Model.extend({
    defaults: {
      project_public_id: '',
      count: 0,
      next: null,
      previous: null,
      options: {}
    },
  });

  App.Models.Items = Backbone.Model.extend({
    defaults: {
      public_id: '',
      project: null,
      sku: '',
      item_number: '',
      item_number_mfg: '',
      manufacturer: null,
      description: '',
      quantity: 0,
      categories: [],
      location_codes: [],
      shared_projects: [],
      purge: false,
      active: false,
      creator: '',
      created: '',
      updater: '',
      updated: '',
      uri: ''
    },

    url: function() {
      return this.uri;
    }
  });

  App.Models.ItemsMeta = Backbone.Model.extend({
    defaults: {
      count: 0,
      next: null,
      previous: null,
      options: {}
    },
  });


  // Invoices
  App.Collections.Invoices = Backbone.Collection.extend({
    name: "Invoices",
    model: App.Models.Invoices,

    parse: function(response, options) {
      var models = response.results;
      var project_public_id = models[0].project_public_id;
      App.models.invoicesMeta = new App.Models.InvoicesMeta({
        project_public_id: project_public_id,
        count: response.count,
        next: response.next,
        previous: response.previous
      })
      return models;
    }
  });

  // InvoiceItems





  // Items
  App.Collections.Items = Backbone.Collection.extend({
    name: "Items",
    model: App.Models.Items,

    parse: function(response, options) {
      var models = response.results;
      var project_public_id = models[0].project_public_id;
      App.models.itemsMeta = new App.Models.ItemsMeta({
        project_public_id: project_public_id,
        count: response.count,
        next: response.next,
        previous: response.previous
      })
      return models;
    }
  });

  // Fetch Invoices
  window.populateInvoiceCollection = function(url, project) {
    clearTimeout(App.invoiceTimeout);
    var invoices = new App.Collections.Invoices();
    project.set('invoices', invoices);
    invoices.url = url;
    invoices.fetch({
      success: function(collection, response, options) {
        console.log(response);
      },

      error: function(collection, response, options) {
        console.log(response);
      }
    });
  };

  // Fetch Items
  window.populateItemCollection = function(url, project) {
    clearTimeout(App.itemTimeout);
    var items = new App.Collections.Items();
    project.set('items', items);
    items.url = url;
    items.fetch({
      success: function(collection, response, options) {
        console.log(response);
      },

      error: function(collection, response, options) {
        console.log(response);
      }
    });
  };
});
