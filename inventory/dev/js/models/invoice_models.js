/*
 * Invoice models
 *
 * js/models/invoice_models.js
 */

"use strict";


// Invoices
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
    href: ''
  },

  mutators: {
    invoice_items: {
      set: function(key, value, options, set) {
        var invoice_items = new App.Collections.InvoiceItems();
        set(key, invoice_items, options);

        _.forEach(value, function(value, key) {
          invoice_items.add(value);
        });
      }
    }
  },

  url: function() {
    return this.get('href');
  }
});


App.Models.InvoicesMeta = Backbone.Model.extend({
  defaults: {
    project_public_id: '',
    count: 0,
    next: null,
    previous: null,
    options: {}
  }
});


App.Collections.InvoicesMeta = Backbone.Collection.extend({
  name: "InvoicesMeta",
  model: App.Models.InvoicesMeta
});


App.Collections.Invoices = Backbone.Collection.extend({
  name: "Invoices",
  model: App.Models.Invoices,

  parse: function(response, options) {
    var models = response.results;

    if(App.collections.invoicesMeta === (void 0)) {
      App.collections.invoicesMeta = new App.Collections.InvoicesMeta();
    }

    if(response.count > 0) {
      var project_public_id = models[0].project_public_id;
      var invoicesMeta = new App.Models.InvoicesMeta({
        project_public_id: project_public_id,
        count: response.count,
        next: response.next,
        previous: response.previous
      });
      App.collections.invoicesMeta.add(invoicesMeta);
    }

    return models;
  }
});


// InvoiceItems
App.Models.InvoiceItems = Backbone.Model.extend({
  defaults: {
    invoice: '',
    invoice_public_id: '',
    item_number: '',
    description: '',
    quantity: 0,
    unit_price: '',
    process: true,
    item: '',
    href: ''
  },

  url: function() {
    return this.get('href');
  }
});


App.Models.InvoiceItemsMeta = Backbone.Model.extend({
  defaults: {
    invoice_public_id: '',
    count: 0,
    next: null,
    previous: null,
    options: {}
  }
});


App.Collections.InvoiceItemsMeta = Backbone.Collection.extend({
  name: "InvoiceItemsMeta",
  model: App.Models.InvoiceItemsMeta
});


App.Collections.InvoiceItems = Backbone.Collection.extend({
  name: "InvoiceItems",
  model: App.Models.InvoiceItems
});


// Items
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
    href: ''
  },

  url: function() {
    return this.get('href');
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


App.Collections.ItemsMeta = Backbone.Collection.extend({
  name: "ItemsMeta",
  model: App.Models.ItemsMeta
});


App.Collections.Items = Backbone.Collection.extend({
  name: "Items",
  model: App.Models.Items,

  parse: function(response, options) {
    var models = response.results;

    if(App.collections.itemsMeta === (void 0)) {
      App.collections.itemsMeta = new App.Collections.ItemsMeta();
    }

    if(response.count > 0) {
      var project_public_id = models[0].project_public_id;
      var itemsMeta = new App.Models.ItemsMeta({
        project_public_id: project_public_id,
        count: response.count,
        next: response.next,
        previous: response.previous
      });

      App.collections.itemsMeta.add(itemsMeta);
    }

    return models;
  }
});
