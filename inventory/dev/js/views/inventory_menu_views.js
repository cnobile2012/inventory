/*
 * Inventory Menu Views
 *
 * js/views/menu_views.js
 *
 * MENU VIEW ENTRY POINTS
 */

"use strict";


// Inventory Menu
class InventoryItemMenu extends App.Views.MenuItem {
  get toggle() { return true; }

  onClickCallback(model) {
    App.viewFunctions.inventory(model);
  }
};


class InventoryParentMenu extends App.Views.Menu{
  renderCallback(model) {
    return new InventoryItemMenu({model: model});
  }
};


class InventoryMenu extends Backbone.View {
  get el() { return 'div#content'; }

  initialize() {
    _.bindAll(this);
  }

  render() {
    var menu = new InventoryParentMenu({collection: this.collection});
    this.$el.append(menu.render().el);
  }
};


// Project Menu
class ProjectItemMenu extends App.Views.MenuItem {
  get toggle() { return false; }

  onClickCallback(model) {
    App.viewFunctions.project(model);
  }
};


class ProjectParentMenu extends App.Views.Menu {
  renderCallback(model) {
    return new ProjectItemMenu({model: model});
  }
};


class ProjectMenu extends Backbone.View {
  get el() { return 'div#projects div.tab-choice-pane div.pane-nav'; }

  initialize() {
    _.bindAll(this);
  }

  render() {
    var menu = new ProjectParentMenu({collection: this.collection});
    this.$el.append(menu.render().el);
  }
};

App.Views.ProjectMenu = ProjectMenu;
