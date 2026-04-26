/*
 * Account Router
 *
 * js/app/accounts/account_router.js
 */

"use strict";


class AccountsRouter extends Backbone.Router {
  get routes() {
    return {
      'accounts': 'showContactList',
      'accounts/page/:page': 'showContactList',
      'accounts/create': 'createContact',
      'accounts/show/:id': 'showContact',
      'accounts/edit/:id': 'editContact'
    };
  }

  constructor(options) {
    super(options);
    this._bindRoutes();
  }

  showAccountList(page) {
    // Page should be a postive number grater than 0
    page = page || 1;
    page = page > 0 ? page : 1;

    let app = this.startApp();
    app.showAccountList(page);
  }

  createAccount() {
    let app = this.startApp();
    app.showNewAccountForm();
  }

  showAccount(accountId) {
    let app = this.startApp();
    app.showAccountById(accountId);
  }

  editAccount(accountId) {
    let app = this.startApp();
    app.showAccountEditorById(accountId);
  }

  startApp() {
    return App.startSubApplication(AccountsApp);
  }
};

App.Routers.AccountsRouter = AccountsRouter;
