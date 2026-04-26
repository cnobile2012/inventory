/*
 * API root model
 *
 * js/models/root_model.js
 */

"use strict";


class RootModel extends Backbone.Model {
  get urlRoot() { return API_ROOT; }
  get defaults() { return {}; }

  parse(data) {
    _.forEach(data.collection.items, function(value, key) {
      data[key] = value;
    });

    delete data.collection.items;
    return data;
  }
};
