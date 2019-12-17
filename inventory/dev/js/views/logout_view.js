/*
 * Inventory Logout view
 *
 * js/views/logout_view.js
 */

// Create a modal view class
class LogoutModal extends App.Views.BaseModal {
  get model() { return App.models.logoutModel; }
  get el() { return $("#logout-modal"); }
  get template() { return App.templates.logout_template(); }

  get events() {
    return {
      'click button[name=logout-cancel]': 'close',
      'click button[name=logout-submit]': 'submit',
      'keydown': 'keydownHandler'
    };
  }

  constructor(options) {
    super(options);
  }

  submit() {
    App.utils.setHeader();
    this.model.save({}, {
      success(data, status, jqXHR) {
        App.utils.showMessage(status.detail);
        IS_AUTHENTICATED = false;
        $('#user-fullname').empty();
        destroyApp();
        App.utils.setLogin();
      },
      error(jqXHR, status, errorThrown) {
        App.utils.showMessage(status.responseJSON.detail +
                              " Already logged out please refresh the page.");
      }
    });

    this.close();
  }
};

 
jQuery(function($) {  
  $('#logout-button').on('click', function() {
    let logout = new LogoutModal();
    logout.show({show: true});
  });
});
