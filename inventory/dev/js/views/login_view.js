/*
 * Inventory Login view
 *
 * js/views/login_view.js
 */

jQuery(function($) {
  // Create a modal view class
  var LoginModalView = BaseModalView.extend({
    model: App.loginModel,
    el: $("#login-modal"),
    template: $.tpl.login_template(),

    events: {
      'click button[name=login-submit]': 'submit',
      'keydown': 'keydownHandler'
    },

    submit: function() {
      var self = this;
      var username = this.$el.find('input[type=text]').val();
      var password = this.$el.find('input[type=password]').val();

      // Prevent multiple requests when there are no changes.
      if(this.model.get('username') !== username
          || this.model.get('password') !== password) {
        this.model.set('username', username);
        this.model.set('password', password);
        var data = {
          username: username,
          password: password
        };
        setHeader();

        this.model.save(data, {
          success: function(data, status, jqXHR) {
            self.model.set('fullname', status.fullname);
            self.model.set('href', status.href);
            $('#user-fullname').text(status.fullname);
            self.model.set('username', 'X');
            self.model.set('password', 'X');
            var $messages = $('#messages');
            $messages.empty();
            $messages.hide();
            IS_AUTHENTICATED = true;
            window.getAPIRoot();
            _fetchUser();
          },

          error: function(jqXHR, status, errorThrown) {
            var $elm = self.$el.find('.all-error');
            var errors = status.responseJSON;
            mimicDjangoErrors($elm, errors);
            $elm.show();
          }
        });

        this.close();
      }
    }
  });

  var _fetchUser = function() {
    if(App.userModel === null) {
      App.userModel = new App.Models.User();
    }

    App.userModel.fetch({
      error: function(collection, response, options) {
        $('#messages').text("Error: Could not get data for user '" +
          USERNAME + "' from API.");
        $('#messages').show();
      }
    });
  };

  window.setLogin = function() {
    if(!IS_AUTHENTICATED) {
      var options = {
        backdrop: 'static',
        keyboard: false
      };
      new LoginModalView().show(options);
    } else {
      App.loginModel.set(
        'href', location.protocol + '//' + location.host + USER_HREF);
      _fetchUser();
    }
  }

  window.setLogin();
});
