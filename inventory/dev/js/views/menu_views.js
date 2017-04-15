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
  toggle: true, // Set to `false` if you don't want the menu items to toggle.

  // Binding to model's selection change event
  // Thus having ability to update view state
  initialize: function() {
    _.bindAll(this, 'onClickCallback');
    this.listenTo(this.model, 'change:isSelected', this.onSelectedChange);
  },

  // Simple render override
  render: function() {
    this.$el.html(this.model.get('title'));
    return this;
  },

  // Highlight ourself and do any other logic on click
  onClick: function(event) {
    var publicId = this.$el.find('a').attr('data');
    var model = App.models.userModel.get('projects').find(function(model) {
      return model.get('public_id') === publicId;
    });

    // Only display pane once while active.
    if($('#' + publicId).length <= 0) {
      this.highlight();
      var $choicePane = $('div#projects div.tab-choice-pane');
      var $dataPane = $('<div id="' + publicId + '" class="data-pane"></div>');
      var $closePane = $('<div class="pane-close">X</div>');
      $closePane.appendTo($dataPane);
      $dataPane.appendTo($choicePane);
      var self = this;

      $closePane.one('click', function() {
        $dataPane.remove();
        self.$el.removeClass('active');
      });

      this.onClickCallback(model);
    }
  },

  // If we changed our model's selection property during onClick then
  // update ourself with 'active' class if or model was forced by
  // collection to change selection property to false, then remove
  // 'active' class.
  onSelectedChange: function() {
    if(this.model.get('isSelected') === true) {
      this.$el.addClass('active');
    } else if(this.toggle) {
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
    _.bindAll(this, 'renderCallback');
  },

  // Render each menu item by creating the appropriate view calling its
  // render method and appending the resulting element.
  render: function() {
    var self = this;
    this.$el.empty();
    var container = document.createDocumentFragment();

    _.forEach(this.collection.models, function(model) {
      var item = self.renderCallback(model);
      container.appendChild(item.render().el);
    });

    this.$el.append(container);
    return this;
  }
});


// MENU VIEW ENTRY POINT
// Project entry points
App.Views.ProjectItemMenu = App.Views.MenuItem.extend({
  toggle: false,

  onClickCallback: function(model) {
    App.viewFunctions.project(model);
  }
});


App.Views.ProjectParentMenu = App.Views.Menu.extend({
  renderCallback: function(model) {
    return new App.Views.ProjectItemMenu({model: model});
  }
});


App.Views.ProjectMenu = Backbone.View.extend({
  el: 'div#projects div.tab-choice-pane div.pane-nav',

  initialize: function() {
    _.bindAll(this);
  },

  render: function() {
    var menu = new App.Views.ProjectParentMenu({
      collection: this.collection
    });

    this.$el.append(menu.render().el);
  }
});
