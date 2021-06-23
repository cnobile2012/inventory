/*
 * Inventory Login view
 *
 * js/app/auth/login_view.js
 */

"use strict";


// Create a modal view class
class LoginModalView extends MicromodalBaseView {

  get model() { return App.persistentModels.login; }

  get el() { return $("#" + this.tag); }

  get events() {
    return {
      'click button[name=login-success]': 'success',
      'keydown': 'keydownHandler'
    };
  }

  get template() {
    return App.templates.login_template();
  }

  constructor(options) {
    super(options);
    this.tag = 'login-modal';
  }

  successCB(event) {
    let self = this,
        username = this.$el.find('input[type=text]').val(),
        password = this.$el.find('input[type=password]').val();

    if (!IS_AUTHENTICATED) {
      /* set header for every jQuery request */
      $.ajaxPrefilter((options, originalOptions, jqXHR) => {
        jqXHR.setRequestHeader("Authorization",
                               'Basic ' + btoa(username + ':' + password));
      });

      let data = {};
      App.utils.setHeader(); // Eventually put the above in this method.

      this.model.save(data, {
        success: (data, status, jqXHR) => {
          self.model.set('fullname', status.fullname);
          self.model.set('href', status.href);
          $('#user-fullname').text(status.fullname);
          App.utils.hideMessage();
          IS_AUTHENTICATED = true;
        },
        error: (jqXHR, status, errorThrown) => {
          let $elm = self.$el.find('.all-error'),
              errors = status.responseJSON;
          App.utils.mimicDjangoErrors(errors, $elm);
          $elm.show();
        }
      });
    }
  }
};
