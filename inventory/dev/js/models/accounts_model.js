/*
 * Account models
 *
 * js/models/accounts_model.js
 */

var UserModel = Backbone.Model.extend({
  defaults: {
    public_id: '',
    username: '',
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
    uri: ''
  },

  mutators: {
    projects: {
      set: function(key, value, options, set) {
        var data = [];

        _.forEach(value, function(value, key) {
          var project = new ProjectModel();

          _.forEach(value, function(value, key) {
            project.set(key, value, options);
          });

          data[key] = project;
        });

        set(key, data, options);
      }
    }
  },

  url: function() {
    if (_.isUndefined(this.uri)) {
      return App.loginModel.get('href');
    } else {
      return this.uri;
    }
  }
});

jQuery(function($) {
  App.userModel = new UserModel();
});
