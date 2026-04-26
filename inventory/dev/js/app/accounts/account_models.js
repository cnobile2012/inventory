/*
 * Account models
 *
 * js/app/accounts/account_models.js
 */

"use strict";


class ProjectProxyModel extends Backbone.Model {

  get idAttribute() { return 'public_id'; }
  get urlRoot() { return this.get('href'); }
};


class ProjectProxyCollection extends Backbone.Collection {

  get model() { return ProjectProxyModel; }
};


class UserModel extends Backbone.Model {

  get idAttribute() { return 'public_id'; }

  get defaults() {
    return {
      send_email: false,
      need_password: false,
      projects: [],
      project_default: null,
      answers: [],
      is_active: false,
      is_staff: false,
      is_superuser: false,
      creator: '',
      created: '',
      updater: '',
      updated: '',
      href: ''
    };
  }

  get url() {
    var url = this.get('href');

    if(url === '') {
      url = App.persistentModels.login.get('href');
    }

    return url;
  }

  parse(data) {
    App.models.projectProxies = new ProjectProxyCollection();

    _.forEach(data.projects, (value, key) => {
      App.models.projectProxies.add(value);
    });

    data.projects = App.models.projectProxies;
    return data;
  }
};


class UsersCollection extends Backbone.Collection {

  get name () { return "Users"; }
  get model() { return UserModel; }
  get url() { return App.models.rootModel.get('accounts').users.href; }

  parse(data) {
    this.next = data.next;
    this.prev = data.previous;
    return data.results;
  }
};
