/*
 * Inventory Login view
 *
 * js/views/login_view.js
 */

jQuery(function($) {
  // Create a modal view class
  App.Views.LoginModal = App.Views.BaseModal.extend({
    model: App.loginModel,
    el: $("#login-modal"),
    template: App.templates.login_template(),

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
        App.utils.setHeader();

        this.model.save(data, {
          success: function(data, status, jqXHR) {
            self.model.set('fullname', status.fullname);
            self.model.set('href', status.href);
            $('#user-fullname').text(status.fullname);
            self.close();
            self.model.set('username', 'X');
            self.model.set('password', 'X');
            App.utils.hideMessage();
            IS_AUTHENTICATED = true;
            App.utils.fetchData();
          },

          error: function(jqXHR, status, errorThrown) {
            var $elm = self.$el.find('.all-error');
            var errors = status.responseJSON;
            App.utils.mimicDjangoErrors($elm, errors);
            $elm.show();
          }
        });
      }
    }
  });

  App.utils.setLogin();
});
