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
          var $message = $('#messages');
          $message.text(status.message);
          $message.show();
        },
        error: function(jqXHR, textStatus, errorThrown) {
          console.log(textStatus);
          }
      });

      this.close();
    }
  });

  $('#logout-button').on('click', function() {
    new LogoutModalView().show({backdrop: 'static'});
  });
});
