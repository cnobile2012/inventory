/*
 * Inventory Utilities.
 *
 * js/utils.js
 */

"use strict";


/*
 * Utilities
 */
var Utilities = function() {
  this.initialize();
};

Utilities.prototype = {

  initialize: function() {
  },

  _csrfSafeMethod: function(method) {
    // These HTTP methods do not require CSRF protection.
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  },

  setHeader: function() {
    var self = this;

    $.ajaxPrefilter(function(options, originalOptions, jqXHR) {
      options.crossDomain = false;

      // Set the Django CSRF token.
      options.beforeSend = function(xhr, settings) {
        if(!self._csrfSafeMethod(settings.type)) {
          xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
        }
      }.bind(self);
    });
  },

  showMessage: function(message, fade) {
    var $messages = $('#messages');
    $messages.html(message);
    $messages.show();

    if(fade !== (void 0) && fade === true) {
      $messages.fadeOut(7500);
    }
  },

  hideMessage: function() {
    var $messages = $('#messages');
    $messages.hide();
    $messages.empty();
  },

  mimicDjangoErrors: function(data, elm) {
    // Mimic Django error messages.
      let ul = '<ul class="errorlist"></ul>',
          li = '<li></li>',
          $tag = null, $errorUl = null, $errorLi = null;
    $('ul.errorlist').remove();

    for(var key in data) {
      $tag = $('select[name=' + key + '], input[name=' + key +
               '], textarea[name=' + key + ']');
      $errorUl = $(ul);

      if($tag.prev().prop('tagName') === 'LABEL') {
        $tag = $tag.prev();
        $errorUl.insertBefore($tag);
      } else if($tag.length === 0) {
        $tag = $(elm);
        $errorUl.appendTo($tag);
      }

      for(var i = 0; i < data[key].length; i++) {
        $errorLi = $(li);
        $errorLi.html(data[key][i]);
        $errorLi.appendTo($errorUl);
      }
    }
  },

  // Set a default value on an object key--similar to Python's
  // <dict>.setdefault(<key>, value).
  setDefault: function(obj, key, value) {
    if(key in obj) {
      return obj[key];
    } else {
      obj[key] = value;
      return obj[key];
    }
  },

  getMetaChoices: function(choices) {
    let out = {};

    for(let i = 0; i < choices.length; i++) {
      out[choices[i].value] = choices[i].display_name;
    }

    return out;
  },

  assert: function(condition, message) {
    if(!condition) {
      message = message || "Assertion Error";

      if(typeof Error !== (void 0)) {
        throw new Error(message);
      }

      throw message; // If the Error exception does not exist.
    }
  },

  arrayDiff: function(a1, a2) {
    // https://stackoverflow.com/questions/1187518/how-to-get-the-difference-between-two-arrays-in-javascript
    let a = [], diff = [];

    for(let i = 0; i < a1.length; i++) {
      a[a1[i]] = true;
    }

    for(let i = 0; i < a2.length; i++) {
      if(a[a2[i]]) {
        delete a[a2[i]];
      } else {
        a[a2[i]] = true;
      }
    }

    for(let k in a) {
      diff.push(k);
    }

    return diff;
  },

  arrayUnique: function(array) {
    let a = array.concat();

    for(let i = 0; i < a.length; ++i) {
      for(let j = i + 1; j < a.length; ++j) {
        if(a[i] === a[j]) {
          a.splice(j--, 1);
        }
      }
    }
  },

  arrayAdd: function(a1, a2) {
    return this.arrayUnique(a1.concat(a2));
  },

  sleep: function(milliseconds) {
    let start = new Date().getTime();

    while((new Date().getTime() - start) < milliseconds);
  },

  // Inventory specific methods.

  setLogin: function() {
    if(!IS_AUTHENTICATED) {
      var options = {
        backdrop: 'static',
        keyboard: false
      };
      new App.Views.LoginModal().show(options);
    } else {
      App.loginModel.set(
        'href', location.protocol + '//' + location.host + USER_HREF);
      this.fetchData();
    }
  },

  fetchData: function() {
    this.fetchUser();
    this.fetchRoot();
  },

  fetchUser: function() {
    if(App.models.userModel === (void 0)) {
      App.models.userModel = new App.Models.User();
    }

    return App.models.userModel.fetch({
      error: function(model, response, options) {
        App.utils.showMessage("Error: Could not get data for user '" +
                              USERNAME + "' from API.");
      }
    });
  },

  fetchRoot: function() {
    if(App.models.rootModel === (void 0)) {
      App.models.rootModel = new App.Models.RootModel();
    }

    return App.models.rootModel.fetch({
      success: function(model, response, options) {
        App.utils.fetchProjectMeta();
        App.utils.fetchInventoryType();
        App.utils.fetchInventoryTypeMeta();
      },

      error: function(model, response, options) {
        App.utils.showMessage("Error: Could not get data from API root.");
      }
    });
  },

  fetchProjectMeta: function() {
    if(App.models.projectMeta === (void 0)) {
      App.models.projectMeta = new App.Models.ProjectMeta();
    }

    return App.models.projectMeta.fetch({
      success: function(model, response, options) {
        //console.log(model.get('projects').projects);
      },

      error: function(model, response, options) {
        App.utils.showMessage(options.textStatus + " " + options.errorThrown);
      }
    });
  },

  fetchInventoryType: function() {
    if(App.collections.inventoryType === (void 0)) {
      App.collections.inventoryType = new App.Collections.InventoryType();
    }

    return App.collections.inventoryType.fetch({
      success: function(model, response, options) {
        //console.log(model.get('projects').projects);
      },

      error: function(model, response, options) {
        App.utils.showMessage(options.textStatus + " " + options.errorThrown);
      }
    });
  },

  fetchInventoryTypeMeta: function() {
    if(App.models.inventoryTypeMeta === (void 0)) {
      App.models.inventoryTypeMeta = new App.Models.InventoryTypeMeta();
    }

    return App.models.inventoryTypeMeta.fetch({
      success: function(model, response, options) {
        //console.log(model.get('projects').projects);
      },

      error: function(model, response, options) {
        App.utils.showMessage(options.textStatus + " " + options.errorThrown);
      }
    });
  },

  // Fetch Invoices
  fetchInvoiceCollection: function(url, project) {
    clearTimeout(App.invoiceTimeout);
    var invoices = new App.Collections.Invoices();
    project.set('invoices', invoices);
    invoices.url = url;
    invoices.fetch({
      success: function(collection, response, options) {
        console.log(response);
      },

      error: function(collection, response, options) {
        console.log(response);
      }
    });
  },

  // Fetch Items
  fetchItemCollection: function(url, project) {
    clearTimeout(App.itemTimeout);
    var items = new App.Collections.Items();
    project.set('items', items);
    items.url = url;
    items.fetch({
      success: function(collection, response, options) {
        console.log(response);
      },

      error: function(collection, response, options) {
        console.log(response);
      }
    });
  },

  // SEARCH ENDPOINTS
  searchEndpoint: function(event) {
    var self = event.data.self;
    var uri = event.data.endpoint;
    // ex. App.models.rootModel.get('accounts').users
    var search = encodeURI($(this).val().trim());

    if(search !== "") {
      var options = {
        url: uri + '?search=' + search,
        cache: true,
        type: 'GET',
        contentType: false,
        processData: false,
        timeout: 10000, // 10 seconds
        error: self.errorCB.bind(self),
        success: self.searchRequestCB.bind(self)
      };
      $.ajax(options);
    } else {
      var $input = $(event.data.input);
      $input.prop('data', 0);
      $input.empty();
    }
  },

  searchRequestCB: function(data, status, jqXHR) {
    if(data.count > 0) {
      var result = null;
      var $listUl = $('#model-choice');
      var li = '<li></li>';
      var $li = null;
      $ul.empty();
      var options = {
        self: this,
        $listUi: $listUi
      };

      for(var i = 0; i < data.results.length; i++) {
        result = data.results[i];
        $li = $(li);
        $li.text('' + result.year + ' ' + result.make + ' ' + result.model);
        $li.prop('data', result.pk);
        $li.on('click', options, this.chooseItem);
        $li.appendTo($ul);
      }

      $ul.show();
    }
  },

  errorCB: function(jqXHR, status, errorThrown) {
    try {
      var json = $.parseJSON(jqXHR.responseText);
      var msg = '';

      for(var key in json) {
        msg += key + ": " + json[key] + "<br />";
      }

      this.showMessage(msg);
    } catch (e) {
      this.showMessage(jqXHR.statusText + ": " + jqXHR.status);
    }
  },

  chooseItem: function(event) {
    var self = event.data.self;
    var $input = $(event.data.input);
    $input.prop('data', $(this).prop('data'));
    $input.val($(this).text());
    event.data.$listUl.hide();
  }
};

window.App.utils = new Utilities();
