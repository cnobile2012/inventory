/*
 * Inventory main entry point.
 *
 * js/main.js
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
var DefaultRouter = Backbone.Router.extend({
  routes: {
    '': 'defaultRoute'
  },

  // Redirect to contacts app by default
  defaultRoute() {
    this.navigate('contacts', true);
  }
});


var App = {
  Models: {},
  Collections: {},
  Views: {},
  //Forms: {},
  models: {},
  collections: {},
  views: {}, // Use for persistent single views.
  viewFunctions: {}, // Use for functions that call ephemeral views.
  templates: null,
  loginModel: null,
  ViewContainer: null,
  viewContainer: null,
  Router: null,
  utils: null,
  invoiceTimeout: null,
  itemTimeout: null,

  start() {
    // Initialize all available routes
    _.each(_.values(this.Routers), function(Router) {
      new Router();
    });

    // The common place where sub-applications will be shown
    App.mainRegion = new Region({el: '#main'});

    // Create a global router to enable sub-applications to redirect to
    // other urls
    App.router = new DefaultRouter();
    Backbone.history.start();
  },

  // Only one subapplication can be running at once, destroy any
  // currently running subapplication and start the asked for one.
  startSubApplication(SubApplication) {
    // Do not run the same subapplication twice
    if (this.currentSubapp && this.currentSubapp instanceof SubApplication) {
      return this.currentSubapp;
    }

    // Destroy any previous subapplication if we can
    if (this.currentSubapp && this.currentSubapp.destroy) {
      this.currentSubapp.destroy();
    }

    // Run subapplication
    this.currentSubapp = new SubApplication({region: App.mainRegion});
    return this.currentSubapp;
  }
};


/*
 * This function is run when logout happens, so that all data for the
 * user is removed.
 */
window.destroyApp = function() {
  App.models = {};
  App.collections = {};
  App.views = {};
  App.loginModel.clear().set(App.loginModel.defaults);
  App.invoiceTimeout = null;
  App.itemTimeout = null;
  $('div.tab-choice-pane div').not(':first').remove();
  $('div.tab-choice-pane div').empty();
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
