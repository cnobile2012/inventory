/*
 * Account Facade
 *
 * js/app/accounts/account_app.js
 */

'use strict';


// TODO: enable pagination
class AccountsApp {

  constructor(options) {
    this.region = options.region;
  }

  get accept() {
    return App.models.rootModel.get('accounts').users
      .accept_header.json['1.0'];
  }

  get contentType() {
    return App.models.rootModel.get('accounts').users
      .content_type_header.json['1.0'];
  }

  fetchCurrentUserAccount() {
    if(App.models.userModel === (void 0)) {
      App.models.userModel = new UserModel();
    }

    App.models.userModel.fetch({
      accepts: { json: this.accept },
      error(model, response, options) {
        App.utils.showMessage("Error: Could not get data for user '" +
                              USERNAME + "' from API.");
      }
    });
  }

  showAccountList() {
    App.events.trigger('loading:start');
    App.events.trigger('app:accounts:started');

    new AccountCollection().fetch({
      success(collection) {
        // Show the account list subapplication if the list can be fetched.
        this.showList(collection);
        App.events.trigger('loading:stop');
      },
      fail(collection, response) {
        // Show error message if something goes wrong.
        App.events.trigger('loading:stop');
        App.events.trigger('server:error', response);
      }
    });
  }

  showNewAccountForm() {
    App.events.trigger('app:accounts:new:started');
    this.showEditor(new Account());
  }

  showAccountEditorById(accountId) {
    App.events.trigger('loading:start');
    App.events.trigger('app:accounts:started');

    new Account({id: accountId}).fetch({
      success(model) {
        this.showEditor(model);
        App.events.trigger('loading:stop');
      },
      fail(collection, response) {
        App.events.trigger('loading:stop');
        App.events.trigger('server:error', response);
      }
    });
  }

  showAccountById(accountId) {
    App.events.trigger('loading:start');
    App.events.trigger('app:accounts:started');

    new Account({id: accountId}).fetch({
      accept: {json: this.accepts},

      success(model) {
        this.showViewer(model);
        App.events.trigger('loading:stop');
      },
      fail(collection, response) {
        App.events.trigger('loading:stop');
        App.events.trigger('server:error', response);
      }
    });
  }

  showList(accounts) {
    let accountList = this.startController(AccountList);
    accountList.showList(accounts);
  }

  showEditor(account) {
    let accountEditor = this.startController(AccountEditor);
    accountEditor.showEditor(account);
  }

  showViewer(account) {
    let accountViewer = this.startController(AccountViewer);
    accountViewer.showAccount(account);
  }

  startController(Controller) {
    if(!(this.currentController &&
         this.currentController instanceof Controller)) {
      if (this.currentController && this.currentController.destroy) {
        this.currentController.destroy();
      }

      this.currentController = new Controller({region: this.region});
    }

    return this.currentController;
  }
};
