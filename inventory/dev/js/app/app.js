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
      let login = new LoginModalView();
      login.show(options);
    } else {
      // Set the href on the login model.
      App.persistentModels.login.set(
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
  Routers: {},
  router: null, // Only the default router.
  // Multiple instance variables.
  collections: {},
  layouts: {},
  models: {},
  persistentModels: {},
  regions: {},
  templates: {},
  views: {}, // Use for persistent single views.
  viewFunctions: {}, // Use for functions that call ephemeral views.
  // Single instance variables.
  ViewContainer: null,
  viewContainer: null,
  utils: null,
  invoiceTimeout: null,
  itemTimeout: null,

  start() {
    // Load all the templates.
    this.templateLoader();

    // Create the login and logout models instances.
    this.createNeededModels();
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
      let tag = $(this).attr('id');

      if(App.templates[tag] === (void 0)) {
        App.templates[tag] = _.template($(this).html());
        // Remove template from DOM.
        $(this).remove();
      }
    });
  },

  createNeededModels() {
    if(this.persistentModels.login === (void 0))
      this.persistentModels.login = new LoginModel();

    if(this.persistentModels.logout === (void 0))
      this.persistentModels.logout = new LogoutModel();
  },

  activateLogoutModal() {
    $('#logout-button').on('click', function(event) {
      let logout = new LogoutModalView();
      logout.show({show: true});
    });
  },

  /*
   * This function is run when logout happens, so that all data for the
   * user is removed.
   */
  destroyApp() {
    App.persistentModels.login.clear()
      .set(App.persistentModels.login.defaults);
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

  errorMessage(message) {
    let model = new ErrorNotifyModalModel();
    if(message !== (void 0)) model.set('message', message);
    let nmv = new NotificationModalView({model: model});
    nmv.show();
  },

  askConfirmation(message, callback) {
    if(typeof message === 'function') {
      callback = message;
      message = (void 0);
    }

    let model = new ConfirmNotifyModalModel();
    if(message !== (void 0)) model.set('message', message);
    let nmv = new NotificationModalView({model: model});
    if(callback !== (void 0)) nmv.submitCallback = callback;
    nmv.show();
  },

  alertSuccess(message) {
    let model = new SuccessAlertModalModel();
    if(message !== (void 0)) model.set('message', message);
    let amv = new AlertModalView({model: model});
    amv.show();
    setTimeout(() => {
      $('#alert-modal').fadeOut(2000, () => { amv.close(); });
    }, 2000);
  },

  alertError(message) {
    let model = new ErrorAlertModalModel();
    if(message !== (void 0)) model.set('message', message);
    let amv = new AlertModalView({model: model});
    amv.show();
    setTimeout(() => {
      $('#alert-modal').fadeOut(2000, () => { amv.close(); });
    }, 2000);
  }
};


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
