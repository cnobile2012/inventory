/*
 * Inventory Logout view
 *
 * js/views/logout_view.js
 */

jQuery(function($) {
  // Create a modal view class
  var LogoutModalView = BaseModalView.extend({
    model: App.models.logoutModel,
    el: $("#logout-modal"),
    template: $.tpl.logout_template(),

    events: {
      'click button[name=logout-cancel]': 'close',
      'click button[name=logout-submit]': 'submit',
      'keydown': 'keydownHandler'
    },

    submit: function() {
      App.utils.setHeader();
      this.model.save({}, {
        success: function(data, status, jqXHR) {
          var $messages = $('#messages');
          $messages.text(status.detail);
          $messages.show();
          IS_AUTHENTICATED = false;
          $('#user-fullname').empty();
          destroyApp();
          setTimeout(setLogin, 200);
        },
        error: function(jqXHR, status, errorThrown) {
          var $messages = $('#messages');
          var msg = status.responseJSON.detail +
              " Already logged out please refresh the page.";
          $messages.text(msg);
          $messages.show();
        }
      });

      this.close();
    }
  });

  $('#logout-button').on('click', function() {
    new LogoutModalView().show({show: true});
  });
});
