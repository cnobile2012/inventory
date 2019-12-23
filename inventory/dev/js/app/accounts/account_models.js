/*
 * Account models
 *
 * js/models/account_models.js
 */

"use strict";


class User extends Backbone.Model {
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
          var projects = new App.Collections.Projects();
          set(key, projects, options);

          _.forEach(value, function(value, key) {
            projects.add(value);
          });
        }
      }
    };
  }

  get url() {
    var url = this.get('href');

    if(url === '') {
      url = App.loginModel.get('href');
    }

    return url;
  }
};

App.Models.User = User;


class Users extends Backbone.Collection {
  get model() { return App.Models.User; }
};

App.Collections.Users = Users;
