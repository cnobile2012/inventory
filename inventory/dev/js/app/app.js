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

  initialize() {
    this.route('', 'loginRoute');
    this.route('login', 'loginRoute');
    App.events.bind('app:auth:auth', this.redirectLoginRoute.bind(this));
  }

  loginRoute() {
    this.redirectLoginRoute();
  }

  redirectLoginRoute(redirect) {
    App.startSubApplication(AuthApp).authenticate(redirect);
  }
}


var App = {
  Routers: {},
  router: null, // Only the default router.
  //globalRegion: null,
  // Multiple instance variables.
  apps: {},
  layouts: {},
  models: {},
  persistentModels: {},
  regions: {},
  templates: {},
  views: {}, // Use for persistent single views.
  openDataPanes: {},
  // Single instance variables.
  viewContainer: null,
  utils: null,
  invoiceTimeout: null,
  itemTimeout: null,
  // Create an event aggregator
  events: _.extend({}, Backbone.Events),

  start() {
    // Load all the templates.
    this.templateLoader();
    // Create the login and logout models instances.
    this.createPersistentModels();
    this.activateLogoutModal();

    // Initialize all available routes
    _.each(_.values(this.Routers), (Router) => {
      new Router();
    });

    // Create a global router to enable sub-applications to redirect to
    // other urls
    this.router = new DefaultRouter();

    // The common place where sub-applications will be showen.
    //this.globalRegion = new Region({el: '#content'});

    if(!Backbone.History.started) {
      Backbone.history.start();
      Backbone.history.listenTo(Backbone.history, 'route',
                                this.removeTabs.bind(this));
    }
  },

  templateLoader() {
    $('script.template').each(function(index) {
      // Load template from DOM.
      let tag = $(this).attr('id');

      if (App.templates[tag] === (void 0)) {
        App.templates[tag] = _.template($(this).html());
        // Remove template from DOM.
        $(this).remove();
      }
    });
  },

  createPersistentModels() {
    if (this.persistentModels.login === (void 0))
      this.persistentModels.login = new LoginModel();

    if (this.persistentModels.logout === (void 0))
      this.persistentModels.logout = new LogoutModel();
  },

  activateLogoutModal() {
    // Activate Logout Model
    $('#logout-button').on('click', {self: this}, function(event) {
      let self = event.data.self;
      self.startSubApplication(AuthApp);
      self.apps.authApp.showLogout();
    });
  },

  /*
   * This function is run when logout happens, so that all data for the
   * user is removed.
   */
  destroyApp() {
    App.persistentModels.login.clear()
      .set(App.persistentModels.login.defaults);
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

  removeTabs(router, method) {
    //console.log('POOP', router.routes, method, route);
    let defRoutes = ['projects', 'invoices', 'items', 'suppliers',
                     'categories', 'locations', 'accounts'],
        currentRoute = Object.keys(router.routes).find(
          key => router.routes[key] == method);

    if (defRoutes.hasOwnProperty(currentRoute)) {
      _.each(defRoutes, route => {
        if (route !== currentRoute) {
          //console.log('POOP', route, currentRoute);
          App.events.trigger('app:' + route + ':closeall');
        }
      });
    }
  },

  hasRootData() {
    return (this.models.rootModel !== (void 0));
  },

  doesElementExist(elem) {
    let result = false;

    if ($(elem).length) {
      result = true;
    }

    return result;
  },

  /*
   * Only one subapplication can be running at once, destroy any
   * currently running subapplication and start the asked for one.
   */
  startSubApplication(SubApplication) {
    // Do not run the same subapplication twice
    let idx = SubApplication.name.indexOf('App');
    this.utils.assert(idx > 0, "Programming Error: " + SubApplication.name
                      + " is not a sub application or is named wrong.");
    let instName = SubApplication.name.substr(0, idx).toLowerCase()
        + SubApplication.name.substr(idx);

    if (!(this.apps[instName] !== (void 0)
         && this.apps[instName] instanceof SubApplication)) {
      // Destroy any previous subapplication if we can.
      if (this.apps[instName] && this.apps[instName].destroy !== (void 0)) {
        this.apps[instName].destroy();
      }

      // Run subapplication.
      this.apps[instName] = new SubApplication();
    }

    return this.apps[instName];
  },

  errorMessage(message) {
    let model = new ErrorNotifyModalModel();
    if (message !== (void 0)) model.set('message', message);
    let nmv = new NotificationModalView({model: model});
    nmv.show();
  },

  // https://stackoverflow.com/questions/21518381/proper-way-to-wait-for-one-function-to-finish-before-continuing
  waitFor(func, ms=1000) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        let result = func();
        resolve(result);
      }, ms);
    });
  },

  askConfirmation(message, callback) {
    if (typeof message === 'function') {
      callback = message;
      message = (void 0);
    }

    let model = new ConfirmNotifyModalModel();
    if (message !== (void 0)) model.set('message', message);
    let nmv = new NotificationModalView({model: model});
    if (callback !== (void 0)) nmv.submitCallback = callback;
    nmv.show();
  },

  alertSuccess(message) {
    let model = new SuccessAlertModalModel();
    if (message !== (void 0)) model.set('message', message);
    let amv = new AlertModalView({model: model});
    amv.show();
    setTimeout(() => {
      $('#alert-modal').fadeOut(3000, () => { amv.close(); });
    }, 2000);
  },

  alertError(message) {
    let model = new ErrorAlertModalModel();
    if (message !== (void 0)) model.set('message', message);
    let amv = new AlertModalView({model: model});
    amv.show();
    setTimeout(() => {
      $('#alert-modal').fadeOut(3000, () => { amv.close(); });
    }, 2000);
  },

  testModal(message) {
    let model = new TestNotifyModalModel();
    if (message !== (void 0)) model.set('message', message);
    let tnmv = new TestNotifyModalView({model: model});
    tnmv.show();
  }
};

window.App = App;


jQuery(function($) {
  App.start();
});
