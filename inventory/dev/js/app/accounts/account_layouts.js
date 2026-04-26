/*
 * Account Layouts
 *
 * js/app/accounts/account_layouts.js
 */

"use strict";


class AccountListLayout extends Layout {
  constructor(options) {
    super(options);
    this.template = '#account-list-layout';
    this.regions = {
      actions: '.actions-bar-container',
      list: '.list-container'
    };
  }

  get className() {
    return 'row page-container';
  }
}

class AccountListActionBar extends ModelView {
  constructor(options) {
    super(options);
    this.template = '#account-list-action-bar';
  }

  get className() {
    return 'options-bar col-xs-12';
  }

  get events() {
    return {
      'click button': 'createAccount'
    };
  }

  createAccount() {
    App.router.navigate('accounts/new', {trigger: true});
  }
}

class AccountListItemView extends ModelView {
  constructor(options) {
    super(options);
    this.template = '#account-list-item';
  }

  get className() {
    return 'col-xs-12 col-sm-6 col-md-3';
  }

  get events() {
    return {
      'click #delete': 'deleteAccount',
      'click #view': 'viewAccount'
    };
  }

  initialize(options) {
    this.listenTo(options.model, 'change', this.render);
  }

  deleteAccount() {
    this.trigger('account:delete', this.model);
  }

  viewAccount() {
    let accountId = this.model.get('id');
    App.router.navigate(`accounts/view/${accountId}`, {trigger: true});
  }
}

class AccountListView extends CollectionView {
  constructor(options) {
    super(options);
    this.modelView = AccountListItemView;
  }

  get className() {
    return 'account-list';
  }
}

class AccountList {
  constructor(options) {
    // Region where the application will be placed
    this.region = options.region;

    // Allow subapplication to listen and trigger events,
    // useful for subapplication wide events
    _.extend(this, Backbone.Events);
  }

  showList(accounts) {
    // Create the views
    let layout = new AccountListLayout(),
        actionBar = new AccountListActionBar(),
        accountList = new AccountListView({collection: accounts});

    // Show the views
    this.region.show(layout);
    layout.getRegion('actions').show(actionBar);
    layout.getRegion('list').show(accountList);

    this.listenTo(accountList, 'item:account:delete', this.deleteAccount);
  }

  deleteAccount(view, account) {
    App.askConfirmation('The account will be deleted', (isConfirm) => {
      if (isConfirm) {
        account.destroy({
          success() {
            App.notifySuccess('Account was deleted');
          },
          error() {
            App.notifyError('Ooops... Something went wrong');
          }
        });
      }
    });
  }

  // Close any active view and remove event listeners
  // to prevent zombie functions
  destroy() {
    this.region.remove();
    this.stopListening();
  }
};
