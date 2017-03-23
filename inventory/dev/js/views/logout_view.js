/*
 * Inventory Logout view
 *
 * js/views/logout_view.js
 */

jQuery(function($) {
  // Create a modal view class
  App.Views.LogoutModal = App.Views.BaseModal.extend({
    model: App.models.logoutModel,
    el: $("#logout-modal"),
    template: App.templates.logout_template(),

    events: {
      'click button[name=logout-cancel]': 'close',
      'click button[name=logout-submit]': 'submit',
      'keydown': 'keydownHandler'
    },

    submit: function() {
      App.utils.setHeader();
      this.model.save({}, {
        success: function(data, status, jqXHR) {
          App.utils.showMessage(status.detail);
          IS_AUTHENTICATED = false;
          $('#user-fullname').empty();
          destroyApp();
          App.utils.setLogin();
        },

        error: function(jqXHR, status, errorThrown) {
          App.utils.showMessage(status.responseJSON.detail +
            " Already logged out please refresh the page.");
        }
      });

      this.close();
    }
  });

  $('#logout-button').on('click', function() {
    new App.Views.LogoutModal().show({show: true});
  });
});
