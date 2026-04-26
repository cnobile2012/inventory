/*
 * Project Lists
 *
 * js/projects/project_list.js
 */

'use strict';


// Project Menu
class ProjectItemMenu extends MenuItem {

  get toggle() { return false; }
  get target() { return 'projects'; }

  constructor(options) {
    super(options);
  }
}


class ProjectParentMenu extends Menu {

  get maxOpen() { return 2; }

  constructor(options) {
    super(options);
    //App.events.listenTo(App.events, 'app:projects:closeall',
    //                    this.remove.bind(this));
  }

  renderCallback(model) {
    return new ProjectItemMenu({
      parent: this,
      model: model,
      parentPaneSelector: 'div.tab-choice-pane',
      dataPaneClass: 'data-pane'
    });
  }

  postRenderCallback(item) {
    App.events.listenTo(App.events, 'app:projects:' + item.model.id + ':open',
                        item.onClick.bind(item));
    App.events.listenTo(App.events, 'app:projects:' + item.model.id + ':close',
                        item.closePane.bind(item));
  }

  remove() {
    _.each(this.viewCollection, view => {
      let open = 'app:projects:' + view.model.id + ':open',
          close = 'app:projects:' + view.model.id + ':close',
          contact = 'app:projects:' + view.model.id + ':contact',
          closeall = 'app:projects:closeall';
      App.events.stopListening(App.events, open);
      App.events.trigger(close);
      App.events.stopListening(App.events, close);
      App.events.stopListening(App.events, contact);
      App.events.stopListening(App.events, closeall);
      view.remove();
    });

    Backbone.View.prototype.remove.call(this);
  }

  maxOpenWarning() {
    App.alertError("Cannot open more than " + this.maxOpen + " tabs!");
  }
}


class ProjectMenu extends Backbone.View {

  get el() { return 'div#projects div.tab-choice-pane div.pane-nav'; }
  get altId() { return 'create-project'; }

  constructor(options) {
    super(options);
    this.projects = options.projects;
  }

  render() {
    this.$el.empty();
    let menu = new ProjectParentMenu({collection: this.collection});
    this.$el.append(menu.render().el);
    return this;
  }

  show() {
    let $ul = $('#projects .pane-nav ul'),
        items = [];

    // Update the Globle Menu
    new InventoryMenuBar().update('projects');

    // Create Project Action Bar
    _.each(this.projects.toArray(), (model) => {
      let item = {
        public_id: model.id,
        title: '<a href="' + "#projects/" + model.id + '">'
          + model.get('name') + '</a>'
      };
      items.push(item);
    });

    items.unshift({
      public_id: this.altId,
      title: '<a href="#projects/create">Create New Project</a>'
    });
    this.collection = new MenuModelItems(items);
    this.render();
  }
}


class ProjectList {

  constructor(options) {
    this.region = options.region;
  }

  showList(projects) {
    // Show the Project Menu
    new ProjectMenu({projects: projects}).show();
  }
}
