/*
 * API root model
 *
 * js/models/root_model.js
 */

var RootModel = Backbone.Model.extend({
  urlRoot: appConfig.baseURL,
  defaults: {},
  mutators: {
    collection: {
      set: function(key, value, options, set) {
        var self = this;

        _.forEach(value, function(value, key) {
          if(key === 'items') {
            _.forEach(value, function(value, key) {
              self.set(key, value, options);
            });
          } else {
            self.set(key, value, options);
          }
        });
      }
    }
  }
});


jQuery(function($) {
  App.rootModel = new RootModel();

  window.getAPIRoot = function() {
    App.rootModel.fetch({
      error: function(collection, response, options) {
        $('#messages').text("Error: Could not get data from API root.");
        $('#messages').show();
      }
    });
  };


  if(IS_AUTHENTICATED) {
    window.getAPIRoot();
  }
});
