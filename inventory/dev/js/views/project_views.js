/*
 * Project view
 *
 * js/views/project_view.js
 */

"use strict";

// Single project view
App.Views.Project = Backbone.View.extend({
  tagName: 'li',
  template: null,

  initialize: function(options) {
    _.bindAll(this, 'render', 'insert');
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
