/*
 * Inventory Logout view
 *
 * js/views/logout_view.js
 */

jQuery(function($) {
  // Create a modal view class
  var LogoutModalView = BaseModalView.extend({
    model: App.logoutModel,
    el: $("#logout-modal"),
    template: $.tpl.logout_template(),

    events: {
      'click button[name=logout-cancel]': 'close',
      'click button[name=logout-submit]': 'submit',
      'keydown': 'keydownHandler'
    },

    submit: function() {
      setHeader();
      this.model.save({}, {
        success: function(data, status, jqXHR) {
          var $messages = $('#messages');
          $messages.text(status.detail);
          $messages.show();
          IS_AUTHENTICATED = false;
          $('#user-fullname').empty();
          window.destroyApp();
          window.setTimeout(window.setLogin(), 200);
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
