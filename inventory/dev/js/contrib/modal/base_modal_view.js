/*
 * Inventory base modal view
 *
 * js/views/base_modal_view.js
 */

"use strict";


class MicromodalBaseView extends Backbone.View {
  get template() { return ''; }

  constructor(options) {
    super(options);
  }

  initialize() {
    _.bindAll(this, 'show', 'close', 'render', 'cancel', 'success',
              'keydownHandler');
    this.render();
    MicroModal.init({
      //debugMode: true,
      disableScroll: true,
      awaitCloseAnimation: false
    });
  }

  render() {
    this.$el = $(this.template);
    this.delegateEvents(this.events);

    if(!this.$el[0].isConnected) {
      document.querySelector('body').appendChild(this.$el[0]);
    }

    return this;
  }

  show() {
    MicroModal.show(this.tag);
  }

  close(event) {
    if(event !== (void 0)) {
      event.stopImmediatePropagation();
    }

    if(this.$el[0].isConnected) {
      MicroModal.close(this.tag);
      document.querySelector('body').removeChild(this.$el[0]);
    }
  }

  cancel(event) {
    this.cancelCB(event);
    this.close(event);
  }

  cancelCB(event) {}

  success(event) {
    this.successCB(event);
    this.close(event);
  }

  successCB(event) {}

  keydownHandler(event) {
    switch (event.which) {
      case 13: // Enter
        this.success();
        break;
    }
  }
};
