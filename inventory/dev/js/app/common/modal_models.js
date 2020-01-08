/*
 * Common Modal Models
 *
 * js/app/common/logout_model.js
 */

"use strict";


class ErrorNotifyModalModel extends Backbone.Model {
  get id() { return 'ErrorNotifyModalModel'; }

  get defaults() {
    return {
      title: "Error",
      image: "/static/img/molumen_red_square_error_warning_icon.svg",
      message: "Oops",
      noCancel: true,
      //cancel: "Cancel",
      noConfirm: false,
      confirm: "Continue"
    };
  }
};


class ConfirmNotifyModalModel extends Backbone.Model {
  get id() { return 'ConfirmNotifyModalModel'; }

  get defaults() {
    return {
      title: "Confirmation",
      image: "/static/img/rodentia-icons_dialog-warning.svg",
      message: "Are you sure?",
      noCancel: false,
      cancel: "Cancel",
      noConfirm: false,
      confirm: "Continue"
    };
  }
};


class SuccessAlertModalModel extends Backbone.Model {
  get id() { return 'SuccessAlertModalModel'; }

  get defaults() {
    return {
      title: "Success",
      theme: 'success',
      message: "The process has succeeded."
    };
  }
};


class ErrorAlertModalModel extends Backbone.Model {
  get id() { return 'SuccessAlertModalModel'; }

  get defaults() {
    return {
      title: "Failed",
      theme: 'failure',
      message: "The process has failed."
    };
  }
};
