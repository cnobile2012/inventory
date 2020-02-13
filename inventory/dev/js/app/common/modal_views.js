/*
 * Common Modal Views
 *
 * js/app/common/modal_views.js
 */

"use strict";


class NotificationModalView extends MicromodalBaseView {

  get el() { return $("#" + this.tag); }

  get events() {
    return {
      'click div[data-micromodal-close]': 'cancel',
      'click button[name=notify-cancel]': 'cancel',
      'click button[name=notify-success]': 'success',
      'keydown': 'keydownHandler'
    };
  }

  get template() {
    return App.templates.notify_template(this.model.toJSON());
  }

  constructor(options) {
    super(options);
    this.tag = 'notify-modal';
  }

  cancelCB() {
    console.log('Cancel');
  }

  successCB() {
    console.log('Success');
  }
};


class AlertModalView extends MicromodalBaseView {

  get el() { return $("#" + this.tag); }

  get events() {
    return {
      'click div[data-micromodal-close]': 'cancel'
    };
  }

  get template() {
    return App.templates.alert_template(this.model.toJSON());
  }

  constructor(options) {
    super(options);
    this.tag = 'alert-modal';
  }
};


// Test Modal View
class TestNotifyModalView extends MicromodalBaseView {

  get el() { return $("#" + this.tag); }

  get events() {
    return {
      'click div[data-micromodal-close]': 'cancel',
      'click button[name=notify-cancel]': 'cancel',
      'click button[name=notify-success]': 'success',
      'keydown': 'keydownHandler'
    };
  }

  get template() {
    return App.templates.test_notify_template(this.model.toJSON());
  }

  constructor(options) {
    super(options);
    this.tag = 'test-notify-modal';
  }

  cancelCB() {
    console.log('Cancel');
  }

  successCB() {
    console.log('Success');
  }
};
