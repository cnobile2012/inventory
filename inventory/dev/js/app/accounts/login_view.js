/*
 * Inventory Login view
 *
 * js/app/accounts/login_view.js
 */

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

    // Prevent multiple requests when there are no changes.
    if(this.model.get('username') !== username
       || this.model.get('password') !== password) {
      this.model.set('username', username);
      this.model.set('password', password);
      let data = {
        username: username,
        password: password
      };
      App.utils.setHeader();

      this.model.save(data, {
        success(data, status, jqXHR) {
          self.model.set('fullname', status.fullname);
          self.model.set('href', status.href);
          $('#user-fullname').text(status.fullname);
          self.model.set('username', 'X');
          self.model.set('password', 'X');
          App.utils.hideMessage();
          IS_AUTHENTICATED = true;
          App.utils.fetchData();
        },

        error(jqXHR, status, errorThrown) {
          let $elm = self.$el.find('.all-error'),
              errors = status.responseJSON;
          App.utils.mimicDjangoErrors(errors, $elm);
          $elm.show();
        }
      });
    }
  }
};
