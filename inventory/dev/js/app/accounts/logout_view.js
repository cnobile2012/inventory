/*
 * Inventory Logout view
 *
 * js/app/accounts/logout_view.js
 */

// Create a modal view class
class LogoutModalView extends MicromodalBaseView {

  get model() { return App.persistentModels.logout; }

  get el() { return $("#" + this.tag); }

  get events() {
    return {
      'click div[data-micromodal-close]': 'cancel',
      'click button[name=logout-cancel]': 'cancel',
      'click button[name=logout-success]': 'success',
      'keydown': 'keydownHandler'
    };
  }

  get template() {
    return App.templates.logout_template();
  }

  constructor(options) {
    super(options);
    this.tag = 'logout-modal';
  }

  successCB(event) {
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
  }
};
