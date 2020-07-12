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

  constructor(options) {
    super(options);
    this.target = options.target;
    this.models = options.models;
  }

  // Binding to model's selection change event
  // Thus having ability to update view state
  initialize() {
    _.bindAll(this, 'onClickCallback', 'closePaneCallback');
    this.listenTo(this.model, 'change:isSelected', this.onSelectedChange);
  }

  // Simple render override
  render() {
    this.$el.html(this.model.get('title'));
    return this;
  }

  // Highlight our self and do any other logic on click
  onClick(event) {
    let id = this.$el.find('a').attr('data'),
        model = this.models.find(function(model) {
          return model.id === id;
        }),
        dataPaneClass = 'data-pane';

    // Only display pane once while active.
    if($('#' + id).length <= 0) {
      this.highlight();
      let $choicePane = $('div#' + this.target + ' div.tab-choice-pane'),
          $dataPane = $('<div id="' + id + '" class="' + dataPaneClass + '"></div>'),
          $closePane = $('<div class="pane-close">X</div>'),
          self = this;
      $closePane.appendTo($dataPane);
      $dataPane.appendTo($choicePane);
      $closePane.one('click', function() {
        $dataPane.remove();
        self.$el.removeClass('active');
        self.closePaneCallback(dataPaneClass);
      });

      this.onClickCallback(model);
    }
  }

  onClickCallback() {}
  closePaneCallback(dataPaneClass) {}

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
