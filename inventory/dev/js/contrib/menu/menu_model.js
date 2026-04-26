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

  get idAttribute() { return 'public_id'; }

  get defaults() {
    return {
      public_id: null,
      title: 'Default Title',
      isSelected: false
    };
  }

//  select() {
//    this.set({isSelected: true});
//    this.collection.selectProject(this);
//  }
}


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
   * each model in the collection, checking if it has its isSelected
   * property equal to true and not being changed during this change
   * event. if found any--reset it's isSelected property to false.
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

//  selectProject() {
//    App.events.trigger('app:projects:selected', project);
//  }
}
