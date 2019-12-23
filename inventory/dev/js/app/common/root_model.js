/*
 * API root model
 *
 * js/models/root_model.js
 */

"use strict";


class RootModel extends Backbone.Model {
  get urlRoot() { return API_ROOT; }
  get defaults() { return {}; }
  get mutators() {
    return {
      collection: {
        set(key, value, options, set) {
          let self = this;

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
    };
  }
};

App.Models.RootModel = RootModel;
