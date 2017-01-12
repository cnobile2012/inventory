/*
 * Inventory Login
 *
 * js/views/login_view.js
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

        // Prevent multiple requests when there are no changes.
        if(this.model.get('username') !== username
           || this.model.get('password') !== password) {
          this.model.set('username', username);
          this.model.set('password', password);
          var data = {
            username: username,
            password: password
          };

          this.model.save(data, {
            success: function(data, status, jqXHR) {
              self.model.set('fullname', status.fullname);
              self.model.set('href', status.href);
              $('#user-fullname').text(status.fullname);
              self.destroy();
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
      },
      afterSubmit: function(e) {
        return false;
      },
      beforeCancel: function() {
        return false; // Stop closing on click outside of modal.
      },
      triggerSubmit: function(e) {
        var _ref, _ref1;

        if(e != null) {
          e.preventDefault();
        }

        if(Backbone.$(e.target).is('textarea')) {
          return;
        }

        if(this.beforeSubmit && this.beforeSubmit(e) === false) {
          return;
        }

        if(this.currentView && this.currentView.beforeSubmit
            && this.currentView.beforeSubmit(e) === false) {
          return;
        }

        if(!this.submit && !((_ref = this.currentView) != null
            ? _ref.submit : void 0) && !this.getOption('submitEl')) {
          return this.triggerCancel();
        }

        if((_ref1 = this.currentView) != null) {
          if(typeof _ref1.submit === "function") {
            _ref1.submit();
          }
        }

        if(typeof this.submit === "function") {
          this.submit();
        }

        if(typeof this.afterSubmit === "function" && !this.afterSubmit(e)) {
          return;
        }

        if(this.regionEnabled) {
          return this.trigger('modal:destroy');
        } else {
          return this.destroy();
        }
      }
    });

    $('<div id="login-modal"></div>').appendTo($('body'));
    App.loginView = new LoginModalView();
    $('#login-modal').html(App.loginView.render().el);
  }
});
