/*
 * Inventory base modal view
 *
 * js/views/base_modal_view.js
 */

App.Views.BaseModal = Backbone.View.extend({
  template: '',

  initialize: function() {
    _.bindAll(this, 'show', 'render', 'close', 'submit', 'keydownHandler');
    this.render();
  },

  show: function(options) {
    var self = this;
    $(this.$el).off('hide.bs.modal');
    $(this.$el).on('hide.bs.modal', function() {
      self.close();
    });

    if(options === undefined) {
      options = {};
    }

    this.options = options;
    this.$el.modal(options);
  },

  render: function() {
    this.$el = $(this.template);
    this.delegateEvents(this.events);
    return this;
  },

  close: function() {
    this.remove();
    $('.modal-backdrop').remove();
    $('#hiddenlpsubmitdiv').remove();
    $('#_lpinvis').remove();
  },

  submit: function() {},

  keydownHandler: function (e) {
    switch (e.which) {
      // esc
      case 27:
        if(!(this.options.hasOwnProperty('keyboard'))) {
          this.close();
        }

        break;
      case 13:
        this.submit();
        break;
    }
  }
});
