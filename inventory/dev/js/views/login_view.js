/*
 * Inventory Login view
 *
 * js/views/login_view.js
 */

jQuery(function($) {
  var options = {
    backdrop: 'static',
    keyboard: false
  };

  if(!IS_AUTHENTICATED) {
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
              self.close();
              window.getAPIRoot();
            },

            error: function(jqXHR, textStatus, errorThrown) {
              var $elm = self.$el.find('.all-error');
              var errors = textStatus.responseJSON;
              mimicDjangoErrors($elm, errors);
              $elm.show();
              //console.log(errors);
            }
          });
        }
      }
    });

    new LoginModalView().show(options);
  } else {
    $('#login-button').on('click', function() {
      new LoginModalView().show(options);
    });
  }
});
