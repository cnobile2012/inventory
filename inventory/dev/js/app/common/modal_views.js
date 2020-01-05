/*
 * Common Modal Views
 *
 * js/app/common/modal_views.js
 */

"use strict";


class NotificationModalView extends BaseModalView {

  get el() { return $("#notify-modal"); }

  get template() {
    return App.templates.notify_template(this.model.toJSON());
  }

  get events() {
    return {
      'click button[name=cancel]': 'close',
      'click button[name=success]': 'submit',
      'keydown': 'keydownHandler'
    };
  }

  constructor(options) {
    super(options);
  }

  submit() {}
};
