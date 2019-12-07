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


window.App = {
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
  itemTimeout: null
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
window.App.ViewContainer = Backbone.View.extend({
  childView: null,

  render: function() {
    this.$el.html("Greeting Area");

    this.$el.append(this.childView.$el);
    return this;
  }
});


/*
 * Global Router
 */
window.App.Router = Backbone.Router.extend({
  container: null,
  projectViews: {},

  initialize: function() {
      this.container = new window.App.ViewContainer({});
  },

  routes: {
    '': 'homePage',
  },

  handleProjectRoutes: function(key) {
    view = this.projectViews[key];

    if (view === (void 0)) {

      view = new App.Views.Project();
    }

    this.container.childView = view;
    this.container.render();
  }
});
