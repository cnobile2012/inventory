/*
 * API root model
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

App.rootModel.fetch({
  //  success: function(collection, response, options) {

  //this.set(response.collection);
  //  },
  error:function(collection, response, options) {
    alert('error!');
  }
});

