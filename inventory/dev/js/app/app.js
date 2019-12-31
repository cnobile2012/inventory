/*
 * Inventory main entry point.
 *
 * js/app/app.js
 *
 * Variables used from HTML
 * ========================
 * API_LOGIN -- URI to the login endpoint.
 * API_ROOT -- URI to the root of the REST API.
 * IS_AUTHENTICATED -- True if already authenticated on initial page load.
 * USER_HREF -- Current user's API endpoint.
 * USERNAME -- Current user's username.
 */

"use strict";


/*
 * Global Router (non sub-application dependents)
 */
class DefaultRouter extends Backbone.Router {
  get routes() {
    return {
      '': 'defaultRoute',
      'login': 'loginRoute',
      'projects': 'projectRoute',
      'accounts': 'accountRoute'
    };
  }

  // Show the main screen
  defaultRoute() {
    this.navigate('login', {trigger: true, replace: true});
  }

  loginRoute() {
    if(!IS_AUTHENTICATED) {
      // Show Login Modal
      let options = {
            backdrop: 'static',
            keyboard: false
          };
      let login = new App.Views.LoginModalView();
      login.show(options);
    } else {
      // Set the href on the login model.
      App.login.set(
        'href', location.protocol + '//' + location.host + USER_HREF);
      App.utils.fetchData();
    }
  }

  projectRoute() {
    this.navigate('projects', {trigger: true});
  }

  accountRoute() {
    this.navigate('accounts', {trigger: true});
  }
};


var App = {
  Collections: {},
  collections: {},
  Layouts: {},
  layouts: {},
  Models: {},
  models: {},
  Regions: {},
  regions: {},
  Routers: {},
  router: null, // Only the default router.
  Views: {},
  views: {}, // Use for persistent single views.
  viewFunctions: {}, // Use for functions that call ephemeral views.
  templates: {},
  login: null, // Instance
  logout: null, // Instance
  ViewContainer: null,
  viewContainer: null,
  utils: null,
  invoiceTimeout: null,
  itemTimeout: null,

  start() {
    // Load all the templates.
    this.templateLoader();

    // Create the login and logout models instances.
    this.createLogInOutModels();
    this.activateLogoutModal();

    // Initialize all available routes
    _.each(_.values(this.Routers), (Router) => {
      new Router();
    });

    // The common place where sub-applications will be shown
    this.regions.region = new Region({el: '#main'});

    // Create a global router to enable sub-applications to redirect to
    // other urls
    this.router = new DefaultRouter();

    if(!Backbone.History.started) {
      Backbone.history.start();
    }

    this.router.navigate('', {trigger: true});
  },

  templateLoader() {
    $('script.template').each(function(index) {
      // Load template from DOM.
      if(App.templates[$(this).attr('id')] === (void 0)) {
        App.templates[$(this).attr('id')] = _.template($(this).html());
        // Remove template from DOM.
        $(this).remove();
      }
    });
  },

  createLogInOutModels() {
    if(this.login === null) {
      this.login = new this.Models.LoginModel();
    }

    if(this.logout === null) {
      this.logout = new this.Models.LogoutModel();
    }
  },

  activateLogoutModal() {
    $('#logout-button').on('click', function(event) {
      let logout = new App.Views.LogoutModalView();
      logout.show({show: true});
      //App.router.navigate('logout', {trigger: true, replace: true});
    });
  },

  /*
   * This function is run when logout happens, so that all data for the
   * user is removed.
   */
  destroyApp() {
    App.login.clear().set(App.login.defaults);
    App.collections = {};
    App.layouts = {};
    App.models = {};
    App.regions = {};
    App.views = {};
    App.invoiceTimeout = null;
    App.itemTimeout = null;
    IS_AUTHENTICATED = false;
    $('div.tab-choice-pane div').not(':first').remove();
    $('div.tab-choice-pane div').empty();
  },

  // Only one subapplication can be running at once, destroy any
  // currently running subapplication and start the asked for one.
  startSubApplication(SubApplication) {
    // Do not run the same subapplication twice
    if(this.currentSubapp && this.currentSubapp instanceof SubApplication) {
      return this.currentSubapp;
    }

    // Destroy any previous subapplication if we can.
    if(this.currentSubapp && this.currentSubapp.destroy) {
      this.currentSubapp.destroy();
    }

    // Run subapplication.
    this.currentSubapp = new SubApplication({region: App.mainRegion});
    return this.currentSubapp;
  },

  successMessage(message) {
    let options = {
      title: 'Success',
      type: 'success',
      text: message,
      confirmButtonText: 'Okay'
    };

    swal(options);
  },

  errorMessage(message) {
    let options = {
      title: 'Error',
      type: 'error',
      text: message,
      confirmButtonText: 'Okay'
    };

    swal(options);
  },

  askConfirmation(message, callback) {
    let options = {
      title: 'Are you sure?',
      // Show the warning icon
      type: 'warning',
      text: message,
      // By default the cancel button is not shown
      showCancelButton: true,
      confirmButtonText: 'Yes, do it!',
      // Overwrite the default button color
      confirmButtonColor: '#5cb85c',
      cancelButtonText: 'No'
    };

    // Show the message
    swal(options, function(isConfirm) {
      callback(isConfirm);
    });
  },

  notifySuccess(message) {
    new noty({
      text: message,
      layout: 'topRight',
      theme: 'relax',
      type: 'success',
      timeout: 3000 // close automatically
    });
  },

  notifyError(message) {
    new noty({
      text: message,
      layout: 'topRight',
      theme: 'relax',
      type: 'error',
      timeout: 3000 // close automatically
    });
  }
};

// Attach contrib objects.
App.Views.MenuItem = MenuItem;
App.Views.Menu = Menu;
App.Collections.MenuModelItems = MenuModelItems;
App.Views.BaseModalView = BaseModalView;


/*
 * ViewContainer
 */
class ViewContainer extends Backbone.View {
  get childView() { return null; }

  render() {
    this.$el.html("Greeting Area");

    this.$el.append(this.childView.$el);
    return this;
  }
};

App.ViewContainer = ViewContainer;


// Allow App object to listen and trigger events, useful for global events.
_.extend(App, Backbone.Events);

window.App = App;


jQuery(function($) {
  App.start();
});
