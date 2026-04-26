/*
 * Project models
 *
 * js/projects/project_models.js
 */

"use strict";


// InventoryType
class InventoryTypeMetaModel extends BaseMetaModel {

  get urlRoot() {
    return App.models.rootModel.get('projects').inventory_types.href;
  }
}


class InventoryTypeModel extends Backbone.Model {

  get idAttribute() { return 'public_id'; }

  get urlRoot() {
    return App.models.rootModel.get('projects').inventory_types.href;
  }

  parse(data) {
    let subApp = App.startSubApplication(AccountsApp),
        creator = App.models.users.findWhere({href: data.creator}),
        updater = App.models.users.findWhere({href: data.updater});

    if (creator === (void 0)) {
      subApp.fetchUserAccount(data.creator);
      creator = App.models.users.findWhere({href: data.creator});
    }

    if (updater === (void 0)) {
      subApp.fetchUserAccount(data.updater);
      updater = App.models.users.findWhere({href: data.updater});
    }

    data.creator = creator.get('full_name');
    data.updater = updater.get('full_name');
    data.created = new Date(data.created).toLocaleString();
    data.updated = new Date(data.updated).toLocaleString();
    data.meta = App.models.inventoryTypeMeta.toJSON();
    return data;
  }
}


class InventoryTypeCollection extends Backbone.Collection {

  get url() {
    return App.models.rootModel.get('projects').inventory_types.href;
  }

  get name() { return "InventoryTypeCollection"; }
  get model() { return InventoryTypeModel; }

  parse(data) {
    this.next = data.next;
    this.prev = data.previous;
    return data.results;
  }
}


// Project
class ProjectMetaModel extends BaseMetaModel {

  get urlRoot() { return App.models.rootModel.get('projects').projects.href; }
}


class ProjectModel extends Backbone.Model {

  get idAttribute() { return 'public_id'; }
  get urlRoot() { return this.get('href'); }

  get defaults() {
    return {
      public_id: '',
      name: '',
      members: [],
      invoices_href: '',
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

  parse(data) {
    let subApp = App.startSubApplication(AccountsApp),
        creator = App.models.users.findWhere({href: data.creator}),
        updater = App.models.users.findWhere({href: data.updater});

    data.inventory_type = App.models.inventoryTypes.findWhere({
      href: data.inventory_type
    }).get('name');

    if (creator === (void 0)) {
      subApp.fetchUserAccount(data.creator);
      creator = App.models.users.findWhere({href: data.creator});
    }

    if (updater === (void 0)) {
      subApp.fetchUserAccount(data.updater);
      updater = App.models.users.findWhere({href: data.updater});
    }

    data.creator = creator.get('full_name');
    data.updater = updater.get('full_name');
    data.created = new Date(data.created).toLocaleString();
    data.updated = new Date(data.updated).toLocaleString();
    data.meta = App.models.projectMeta.toJSON();
    return data;
  }
}


class ProjectCollection extends Backbone.Collection {

  get name() { return "Projects"; }
  get model() { return ProjectModel; }
  get url() { return App.models.rootModel.get('projects').projects.href; }

  parse(data) {
    this.next = data.next;
    this.prev = data.previous;
    return data.results;
  }
}
