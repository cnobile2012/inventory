/*
 * Menu views
 *
 * js/views/menu_views.js
 *
 * See:
 * http://stackoverflow.com/questions/12908210/click-menu-item-to-highlight-in-backbone-view
 */

"use strict";

// Single menu item view
App.Views.MenuItem = Backbone.View.extend({
  tagName: 'li',
  events: {
    'click': 'onClick'
  },

  // Binding to model's selection change event
  // Thus having ability to update view state
  initialize: function() {
    _.bindAll(this);
    this.model.on('change:isSelected', this.onSelectedChange.bind(this));
  },

  // Simple render override
  render: function() {
    this.$el.html(this.model.get('title'));
    return this;
  },

  // Highlight ourself and do any other logic on click
  onClick: function(event) {
    this.highlight();
    var $choicePane = $('div#projects div.tab-choice-pane');
    var $dataPane = $('<div class="data-pane"></div>');
    $dataPane.appendTo($choicePane);
    var publicId = this.$el.find('a').attr('data');
    var model = App.models.userModel.get('projects').find(function(model) {
      return model.get('public_id') === publicId;
    });

    console.log(model);
    //var view = new App.Views.Project({model: model});

  },

  // If we changed our model's selection property during onClick then
  // update ourself with 'active' class if or model was forced by
  // collection to change selection property to false, then remove
  // 'active' class.
  onSelectedChange: function() {
    if(this.model.get('isSelected') === true) {
      this.$el.addClass('active');
    } else {
      this.$el.removeClass('active');
    }
  },

  // Mark our model as selected
  highlight: function() {
    this.model.set('isSelected', true);
  }
});


// Whole menu view
App.Views.Menu = Backbone.View.extend({
  tagName: 'ul',

  // Initialize menu items collection here
  initialize: function() {
    _.bindAll(this);
  },

  // Render each menu item by creating the appropriate view calling its
  // render method and appending the resulting element.
  render: function() {
    this.$el.empty();
    var container = document.createDocumentFragment();

    _.forEach(this.collection.models, function(model) {
      var item = new App.Views.MenuItem({model: model});
      container.appendChild(item.render().el);
    });

    this.$el.append(container);
    return this;
  }
});


// MENU ENTRY POINT VIEWS
// Project entry point view
App.Views.ProjectMenu = Backbone.View.extend({
  el: 'div#projects div.tab-choice-pane div.pane-nav',

  initialize: function() {
    _.bindAll(this);
  },

  render: function() {
    var menu = new App.Views.Menu({
      collection: this.collection
    });

    this.$el.append(menu.render().el);
  }
});
