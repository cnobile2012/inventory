/*
 * Menu model
 *
 * js/contrib/menu_model.js
 *
 * See:
 * http://stackoverflow.com/questions/12908210/click-menu-item-to-highlight-in-backbone-view
 */

"use strict";


class MenuModelItem extends Backbone.Model {
  get defaults() {
    return {
      title: 'Default Title',
      isSelected: false
    };
  }
};


class MenuModelItems extends Backbone.Collection {
  get model() { return MenuModelItem; }

  constructor(options) {
    super(options);
  }

  // Listen to any model's isSelected change event
  initialize() {
    this.listenTo(this, 'change:isSelected', this.onSelectedChanged);
  }

  /*
   * If any model changes it's selection property to true, go through
   * each model in collection, checking if it has isSelected property
   * equal to true and not being changed during this change event. if
   * found any--reset it's isSelected property to false.
   */
  onSelectedChanged(currentModel, value) {
    // Only check if `isSelected` is `true`.
    if(value === true) {
      this.each(function(model) {
        if(model.get('isSelected') === true && currentModel !== model) {
          model.set('isSelected', false);
        }
      });
    }
  }
};
