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
      if (_.isUndefined(this.uri)) {
        return "";
      } else {
        return this.uri;
      }
    }
  });


  // Invoices
  App.Collections.Invoices = Backbone.Collection.extend({
    model: App.Models.Invoices});
  // InvoiceItems

  // Items
  App.Collections.Items = Backbone.Collection.extend({
    model: App.Models.Items});

  window.populateInvoiceCollection = function(url) {
    console.log(url);

  };
});
