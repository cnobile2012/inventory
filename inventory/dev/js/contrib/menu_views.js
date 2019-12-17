/*
 * Menu views
 *
 * js/contrib/menu_views.js
 *
 * See:
 * http://stackoverflow.com/questions/12908210/click-menu-item-to-highlight-in-backbone-view
 */

"use strict";


// Single menu item view
class MenuItem extends Backbone.View {
  get tagName() { return 'li'; }

  get events() {
    return {
      'click': 'onClick'
    };
  }

  // Set to `false` if you don't want the menu items to toggle.
  get toggle() { return true; }

  // Binding to model's selection change event
  // Thus having ability to update view state
  initialize() {
    _.bindAll(this, 'onClickCallback');
    this.listenTo(this.model, 'change:isSelected', this.onSelectedChange);
  }

  // Simple render override
  render() {
    this.$el.html(this.model.get('title'));
    return this;
  }

  // Highlight our self and do any other logic on click
  onClick(event) {
    let publicId = this.$el.find('a').attr('data'),
        model = App.models.userModel.get('projects').find(function(model) {
          return model.get('public_id') === publicId;
        });

    // Only display pane once while active.
    if($('#' + publicId).length <= 0) {
      this.highlight();
      let $choicePane = $('div#projects div.tab-choice-pane'),
          $dataPane = $('<div id="' + publicId + '" class="data-pane"></div>'),
          $closePane = $('<div class="pane-close">X</div>'),
          self = this;
      $closePane.appendTo($dataPane);
      $dataPane.appendTo($choicePane);
      $closePane.one('click', function() {
        $dataPane.remove();
        self.$el.removeClass('active');
      });

      this.onClickCallback(model);
    }
  }

  // If we changed our model's selection property during onClick then
  // update ourself with 'active' class if or model was forced by
  // collection to change selection property to false, then remove
  // 'active' class.
  onSelectedChange() {
    if(this.model.get('isSelected') === true) {
      this.$el.addClass('active');
    } else if(this.toggle) {
      this.$el.removeClass('active');
    }
  }

  // Mark our model as selected
  highlight() {
    this.model.set('isSelected', true);
  }
};

App.Views.MenuItem = MenuItem;


// Whole menu view
class Menu extends Backbone.View {
  get tagName() { return 'ul'; }

  // Initialize menu items collection here
  initialize() {
    _.bindAll(this, 'renderCallback');
  }

  // Render each menu item by creating the appropriate view calling its
  // render method and appending the resulting element.
  render() {
    let self = this,
        container = document.createDocumentFragment();
    this.$el.empty();

    _.forEach(this.collection.models, function(model) {
      let item = self.renderCallback(model);
      container.appendChild(item.render().el);
    });

    this.$el.append(container);
    return this;
  }
};

App.Views.Menu = Menu;


//  Examples:

// Inventory Menu
//class InventoryItemMenu extends App.Views.MenuItem {
//  get toggle() { return true; }

//  onClickCallback(model) {
//    App.viewFunctions.inventory(model);
//  }
//};


//class InventoryParentMenu extends App.Views.Menu{
//  renderCallback(model) {
//    return new InventoryItemMenu({model: model});
//  }
//};


//class InventoryMenu extends Backbone.View {
//  get el() { return 'div#content'; }

//  initialize() {
//    _.bindAll(this);
//  }

//  render() {
//    var menu = new InventoryParentMenu({collection: this.collection});
//    this.$el.append(menu.render().el);
//  }
//};
