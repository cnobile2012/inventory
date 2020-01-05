/*
 * Project models
 *
 * js/projects/project_models.js
 */

"use strict";


// InventoryType
class InventoryTypeModel extends Backbone.Model {
  urlRoot() {
    return App.models.rootModel.get('projects').inventory_types.href;
  }
};


class InventoryTypeMetaModel extends BaseMetaModel {
  urlRoot() {
    return App.models.rootModel.get('projects').inventory_types.href;
  }
};


class InventoryTypeCollection extends Backbone.Collection {
  get name() { return "InventoryTypeCollection"; }
  get model() { return InventoryTypeModel; }

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


// Project
class ProjectModel extends Backbone.Model {
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


class ProjectMetaModel extends BaseMetaModel {
  get urlRoot() {
    return App.models.rootModel.get('projects').projects.href;
  }
};


class ProjectCollection extends Backbone.Collection {
  get name() { return "Projects"; }
  get model() { return ProjectModel; }

  initialize() {
    // Create project menu
    this.listenTo(this, 'change', function(model) {
      $('div#projects div.tab-choice-pane div').empty();
      let options = [],
          item = null,
          data = "",
          nextModel = null,
          projectMenuCollection = null,
          projectMenuView = null;

      for(let i = 0; i < this.length; i++) {
        nextModel = this.at(i);
        data = nextModel.get('public_id');
        item = {title: '<a href="#project' + i + '" data="' + data + '" >'
                + nextModel.get('name') + '</a>'};
        options[i] = item;
      }

      projectMenuCollection = new MenuModelItems(options);
      projectMenuView = new ProjectMenu(
        {collection: projectMenuCollection});
      projectMenuView.render();
    });
  }
};
