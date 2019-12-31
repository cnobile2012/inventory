/*
 * Inventory base modal view
 *
 * js/views/base_modal_view.js
 */

"use strict";


class BaseModalView extends Backbone.View {
  get template() { return ''; }

  constructor(options) {
    super(options);
  }

  initialize() {
    _.bindAll(this, 'show', 'render', 'close', 'submit', 'keydownHandler');
    this.render();
  }

  show(options) {
    let self = this;
    this.$el.off('hide.bs.modal');
    this.$el.on('hide.bs.modal', function() {
      self.close();
    });

    if(options === (void 0)) {
      options = {};
    }

    this.options = options;
    this.$el.modal(options);
  }

  render() {
    this.$el = $(this.template);
    this.delegateEvents(this.events);
    return this;
  }

  close() {
    this.remove();
    $('.modal-backdrop').remove();
    $('body').removeClass('modal-open');
  }

  submit() {}

  keydownHandler(e) {
    switch (e.which) {
      case 27: // Escape
        if(!(this.options.hasOwnProperty('keyboard'))) {
          this.close();
        }

        break;
      case 13: // Enter
        this.submit();
        break;
    }
  }
};
