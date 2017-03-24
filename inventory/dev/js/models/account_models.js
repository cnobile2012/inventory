/*
 * Account models
 *
 * js/models/account_models.js
 */

"use strict";


App.Models.User = Backbone.Model.extend({
  defaults: {
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
  },

  mutators: {
    projects: {
      set: function(key, value, options, set) {
        var projects = new App.Collections.Projects();
        set(key, projects, options);

        _.forEach(value, function(value, key) {
          projects.add(value);
        });
      }
    }
  },

  url: function() {
    var url = this.get('href');

    if(url === '') {
      url = App.loginModel.get('href');
    }

    return url;
  }
});


App.Collections.Users = Backbone.Collection.extend({
  model: App.Models.User});
