/*
 * Account Application
 *
 * js/app/auth/auth_app.js
 */

'use strict';


class AuthApp {

  constructor(options) {
    this.region = options.region;
  }

  authenticate(redirect) {
    if (!IS_AUTHENTICATED) {
      // Show Login Modal
      let options = {
            backdrop: 'static',
            keyboard: false
      };

      this.showLogin(options);
    } else if(!App.hasRootData()) {
      // Set the href on the login model.
      App.persistentModels.login.set('href', USER_HREF);

      async function run(self) {
        await self.fetchRootApi();
        App.startSubApplication(AccountsApp);
        await App.apps.accountsApp.fetchCurrentUserAccount();
        App.utils.sleep(500);

        // Call the redirect route if any.
        if (redirect !== (void 0)) {
          await redirect();
        }
      };

      run(this);
    } else if (redirect !== (void 0)) { // Call the redirect route if any.
      redirect();
    }
  }

  showLogout(options) {
    let logout = this.startController(LogoutModalView);
    logout.show(options);
  }

  showLogin(options) {
    let login = this.startController(LoginModalView);
    login.show(options);
  }

  fetchRootApi() {
    if (App.models.rootModel === (void 0)) {
      App.models.rootModel = new RootModel();
    }

    return App.models.rootModel.fetch({
      error(model, response, options) {
        App.utils.showMessage("Error: Could not get data from API root.");
      }
    });
  }

  startController(Controller) {
    if (!(this.currentController
         && this.currentController instanceof Controller)) {
      this.currentController = new Controller({region: this.region});
    }

    return this.currentController;
  }
}
