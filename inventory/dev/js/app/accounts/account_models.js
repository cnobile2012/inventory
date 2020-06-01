/*
 * Account models
 *
 * js/app/accounts/account_models.js
 */

"use strict";


class UserModel extends Backbone.Model {
  get defaults() {
    return {
      public_id: '',
      username: '',
      picture: '',
      send_email: false,
      need_password: false,
      first_name: '',
      last_name: '',
      address_01: '',
      address_02: '',
      city: '',
      subdivision: '',
      postal_code: '',
      country: '',
      language: '',
      timezone: '',
      dob: '',
      email: '',
      role: '',
      projects: [],
      project_default: '',
      answers: [],
      is_active: false,
      is_staff: false,
      is_superuser: false,
      last_login: '',
      date_joined: '',
      href: ''
    };
  }

  get mutators() {
    return {
      projects: {
        set(key, value, options, set) {
          App.models.projects = new ProjectCollection();
          set(key, App.models.projects, options);

          _.forEach(value, (value, key) => {
            App.models.projects.add(value);
          });
        }
      }
    };
  }

  get url() {
    var url = this.get('href');

    if(url === '') {
      url = App.persistentModels.login.get('href');
    }

    return url;
  }
};


class UsersCollection extends Backbone.Collection {
  get model() { return User; }
};
