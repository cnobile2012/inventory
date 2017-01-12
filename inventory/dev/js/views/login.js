/*
 * Inventory Login
 *
 * js/views/login.js
 */

jQuery(function($) {
  if(!IS_AUTHENTICATED) {
    // Create a modal view class
    var LoginModalView = Backbone.Modal.extend({
      model: App.loginModel,
      template: $.tpl.login_template(),
      submitEl: '.bbm-button',
      beforeSubmit: function() {
        setHeader();
      },
      submit: function() {
        var self = this;
        var username = this.$el.find('input[type=text]').val();
        var password = this.$el.find('input[type=password]').val();
        //var csrfmiddlewaretoken = this.$el.find('input[type=hidden]').val();
        this.model.set('username', username);
        this.model.set('password', password);
        var data = {
          username: username,
          password: password
        }

        this.model.save(data, {
          success: function(data, status, jqXHR) {
            self.model.set('fullname', data.fullname);
            self.model.set('href', data.href);
            getAPIRoot();
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
    });

    $('<div id="login-modal"></div>').appendTo($('body'));
    App.loginView = new LoginModalView();
    $('#login-modal').html(App.loginView.render().el);
  }
});
