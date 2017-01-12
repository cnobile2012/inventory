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

App.rootModel = new RootModel();

var getAPIRoot = function() {
  App.rootModel.fetch({
    error: function(collection, response, options) {
      $('#messages').text("Error: Could not get data from API root.");
      $('#messages').show();
    }
  });
};


if(IS_AUTHENTICATED) {
  getAPIRoot();
}
