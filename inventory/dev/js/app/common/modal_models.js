/*
 * Common Modal Models
 *
 * js/app/common/logout_model.js
 */

"use strict";


class ConfirmModalModel extends Backbone.Model {
  get id() { return 'ConfirmModalModel'; }

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


class ErrorModalModel extends Backbone.Model {
  get id() { return 'ErrorModalModel'; }

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
