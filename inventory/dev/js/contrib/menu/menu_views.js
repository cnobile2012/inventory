/*
 * Menu views
 *
 * js/contrib/menu_views.js
 *
 * See: http://stackoverflow.com/questions/12908210/click-menu-item-to-highlight-in-backbone-view
 */

"use strict";


// Single item menu view
class MenuItem extends Backbone.View {

  get tagName() { return 'li'; }
  // Set to `false` if you don't want the menu items to toggle.
  get toggle() { return true; }
  get target() { return null; }
  //get events() { return {'click a': 'projectSelected'}; }
  get events() { return {'click a': 'onClick'}; }

  constructor(options) {
    super(options);
    this.parent = options.parent;
    this.parentPaneSelector = options.parentPaneSelector;
    this.dataPaneClass = options.dataPaneClass;
    this.listenTo(this.model, 'change:isSelected', this.onSelectedChange);
  }

  render() {
    this.$el.html(this.model.get('title'));
    return this;
  }

  // Highlight our self and do any other logic on click
  onClick(event) {
    if (this.target === null) {
      console.error("target:", this.target);
      throw new Error("The 'target' must be set in subclass.");
    }

    if (!App.openDataPanes[this.target]) {
      App.openDataPanes[this.target] = 0;
    }

    if (App.openDataPanes[this.target] < this.parent.maxOpen) {
      // Only display pane once while active.
      if($('#' + this.model.id).length <= 0) {
        this.highlight();
        let $choicePane = $('div#' + this.target + ' '
                            + this.parentPaneSelector),
            $dataPane = $('<div id="' + this.model.id + '" class="'
                          + this.dataPaneClass + '"></div>');
        $dataPane.appendTo($choicePane);
        App.openDataPanes[this.target]++;
      }
    } else {
      this.parent.maxOpenWarning();
    }
  }

  closePane() {
    //if (this.model.id != this.parent.altId) {
      let $dataPane = $('#' + this.model.id + ' .' + this.dataPaneClass);
      $dataPane.remove();
      this.$el.removeClass('active');
    //}

    if (App.openDataPanes[this.target] > 0) {
      App.openDataPanes[this.target]--;
    } else {
      App.openDataPanes[this.target] = 0; // Incase it's negative.
    }
  }

  // If we changed our model's selection property during onClick then update
  // ourself with 'active' class if or model was forced by collection to
  // change selection property to false, then remove 'active' class.
  onSelectedChange() {
    if (this.model.get('isSelected') === true) {
      this.$el.addClass('active');
    } else if (this.toggle) {
      this.$el.removeClass('active');
    }
  }

  // Mark our model as selected
  highlight() {
    this.model.set('isSelected', true);
  }

//  projectSelected(event) {
//    event.preventDefault();
//    this.model.select();
//  }
}


// Whole menu view
class Menu extends Backbone.View {

  get tagName() { return 'ul'; }
  get maxOpen() { return 2; }

  constructor(options) {
    super(options);
    this.collection = options.collection;
    this.viewCollection = [];
  }

  // Render each menu item by creating the appropriate view calling its
  // render method and appending the resulting element.
  render() {
    this.$el.empty();

    _.each(this.collection.toArray(), (model) => {
      let item = this.renderCallback(model);
      this.$el.append(item.render().el);
      this.postRenderCallback(item);
      this.viewCollection.push(item);
    });

    return this;
  }

  maxOpenWarning() {
    console.warn("Cannot open more than " + this.parent.maxOpen + " tabs!");
  }

  renderCallback(model) {}
  postRenderCallback(item) {}
}
