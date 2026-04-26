/*
 * Account Application
 *
 * js/app/auth/auth_app.js
 */

'use strict';


class AuthApp {

  get region() { return null; } // Not used yet new Region({el: '#auth'});

  authenticate(redirect, publicId) {
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
        await App.apps.accountsApp.fetchUserAccount(USER_HREF);
        App.utils.sleep(500);

        // Call the redirect route if any.
        if (redirect !== (void 0)) {
          await redirect(publicId);
        }
      };

      run(this);
    } else if (redirect !== (void 0)) { // Call the redirect route if any.
      redirect(publicId);
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

    //App.events.trigger('loading:start');
    //App.events.trigger('app:projects:started');

    return App.models.rootModel.fetch({
      accepts: { json: 'application/json' }
    }).then((json) => {
      console.log('Root data fetch completed successfully.');
    }).catch((error) => {
      App.utils.showMessage("Error: " + error);
      //App.trigger('server:error', response);
    }).always(() => {
      //App.trigger('loading:stop');
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
