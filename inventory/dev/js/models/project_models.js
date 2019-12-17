/*
 * Project models
 *
 * js/models/project_models.js
 */

"use strict";


// InventoryType
class InventoryModelType extends Backbone.Model {
  urlRoot() {
    return App.models.rootModel.get('projects').inventory_types.href;
  }
};


class InventoryTypeMeta extends App.Models.BaseMetaModel {
  urlRoot() {
    return App.models.rootModel.get('projects').inventory_types.href;
  }
};

App.Models.InventoryTypeMeta = InventoryTypeMeta;


class InventoryType extends Backbone.Collection {
  get name() { return "InventoryModelType"; }
  get model() { return InventoryModelType; }

  initialize() {}

  parse(response, options) {
    let models = response.results;
    App.models.inventoryTypeMeta.set({
      count: response.count,
      next: response.next,
      previous: response.previous
    });
    return models;
  }

  url() {
    return App.models.rootModel.get('projects').inventory_types.href;
  }
};

App.Collections.InventoryType = InventoryType;


// Project
class Project extends Backbone.Model {
  get urlRoot() {
    return this.get('href');
  }

  get defaults() {
    return {
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
    };
  }

  get mutators() {
    return {
      invoices_href: {
        set(key, value, options, set) {
          set(key, value, options);

          if(value.length > 0) {
            App.invoiceTimeout = setTimeout(App.utils.fetchInvoiceCollection,
                                            200, value, this);
          }
        }
      },
      items_href: {
        set(key, value, options, set) {
          set(key, value, options);

          if(value.length > 0) {
            App.itemTimeout = setTimeout(App.utils.fetchItemCollection,
                                         200, value, this);
          }
        }
      },
      creator() {
        let name = "Not Found",
            href = this.attributes.creator,
            userHREF = App.models.userModel.get('href');

        // Check if it's the current user first.
        if(href === userHREF) {
          name = App.models.userModel.get('full_name');
        } else {
          // Get the creator with the 'href'.
        }

        return name;
      },
      created() {
        return new Date(this.attributes.created).toLocaleString();
      },
      updater() {
        let name = "Not Found",
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
        get() {
          return new Date(this.attributes.updated).toLocaleString();
        }
      }
    };
  }
};

App.Models.Project = Project;

class ProjectMeta extends App.Models.BaseMetaModel {
  get urlRoot() {
    return App.models.rootModel.get('projects').projects.href;
  }
};

App.Models.ProjectMeta = ProjectMeta;


class Projects extends Backbone.Collection {
  get name() { return "Projects"; }
  get model() { return App.Models.Project; }

  initialize() {
    // Create project menu
    this.listenTo(this, 'change', function(model) {
      $('div#projects div.tab-choice-pane div').empty();
      let options = [],
          item = null,
          data = "",
          nextModel = null;

      for(let i = 0; i < this.length; i++) {
        nextModel = this.at(i);
        data = nextModel.get('public_id');
        item = {title: '<a href="#project' + i + '" data="' + data + '" >'
                + nextModel.get('name') + '</a>'};
        options[i] = item;
      }

      App.collections.projectMenu = new App.Collections.MenuModelItems(
        options);
      App.views.projectMenu = new App.Views.ProjectMenu(
        {collection: App.collections.projectMenu});
      App.views.projectMenu.render();
    });
  }
};

App.Collections.Projects = Projects;
