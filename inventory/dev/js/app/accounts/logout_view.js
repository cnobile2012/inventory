/*
 * Inventory Logout view
 *
 * js/app/accounts/logout_view.js
 */

// Create a modal view class
class LogoutModalView extends BaseModalView {
  get model() { return App.persistentModels.logout; }
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
        $('#user-fullname').empty();
        App.destroyApp();
        App.router.navigate('', {trigger: true});
      },
      error(jqXHR, status, errorThrown) {
        App.utils.showMessage(status.responseJSON.detail +
                              " Already logged out please refresh the page.");
      }
    });

    this.close();
  }
};
