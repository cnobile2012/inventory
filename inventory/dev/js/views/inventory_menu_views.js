/*
 * Inventory Menu Views
 *
 * js/views/menu_views.js
 *
 */

"use strict";

// MENU VIEW ENTRY POINT
// Project entry points
App.Views.ProjectItemMenu = App.Views.MenuItem.extend({
  toggle: false,

  onClickCallback: function(model) {
    App.viewFunctions.project(model);
  }
});


App.Views.ProjectParentMenu = App.Views.Menu.extend({
  renderCallback: function(model) {
    return new App.Views.ProjectItemMenu({model: model});
  }
});


App.Views.ProjectMenu = Backbone.View.extend({
  el: 'div#projects div.tab-choice-pane div.pane-nav',

  initialize: function() {
    _.bindAll(this);
  },

  render: function() {
    var menu = new App.Views.ProjectParentMenu({
      collection: this.collection
    });

    this.$el.append(menu.render().el);
  }
});
