/*
 * Base meta models
 *
 * js/models/base_meta_model.js
 */

"use strict";


class BaseMetaModel extends Backbone.Model {
  get mutators() {
    return {
      actions: {
        set(key, value, options, set) {
          _.forEach(value.POST, function(value, key) {
            this.set(key, value);
          }.bind(this));
        }
      }
    };
  }

  sync(method, model, options) {
    let type = 'OPTIONS';

    // Default options, unless specified.
    _.defaults(options || (options = {}), {
      emulateHTTP: Backbone.emulateHTTP,
      emulateJSON: Backbone.emulateJSON
    });

    // Default JSON-request options.
    let params = {type: type, dataType: 'json'};

    // Ensure that we have a URL.
    if (!options.url) {
      params.url = _.result(model, 'url') || urlError();
    }

    // Pass along `textStatus` and `errorThrown` from jQuery.
    let error = options.error;
    options.error = function(xhr, textStatus, errorThrown) {
      options.textStatus = textStatus;
      options.errorThrown = errorThrown;
      if (error) error.call(options.context, xhr, textStatus, errorThrown);
    };

    // Make the request, allowing the user to override any Ajax options.
    let xhr = options.xhr = Backbone.ajax(_.extend(params, options));
    model.trigger('request', model, xhr, options);
    return xhr;
  }
};
