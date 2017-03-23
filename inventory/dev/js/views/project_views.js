/*
 * Project view
 *
 * js/views/project_view.js
 */

"use strict";

// Single project view
App.Views.Project = Backbone.View.extend({
  tagName: 'li',
  template: '',

  initialize: function(options) {
    _.bindAll(this, 'insert');
    this.template = App.templates.project_template();

    //this.$container = options.$container;
    this.listenTo(this.model, 'change', this.render);
    this.insert();

  },

  render: function() {


    return this;
  },

  insert: function() {


  }
});
