/*
 * Template loading utility as found in "Backbone.js Cookbook"
 * by: Vadim Mirgorod -- PACKT Publishing
 */

(function($) {
  $(document).ready(function () {
    // Store variable within global jQuery object.
    App.templates = {}

    $('script.template').each(function(index) {
      // Load template from DOM.
      App.templates[$(this).attr('id')] = _.template($(this).html());
      // Remove template from DOM.
      $(this).remove();
    });
  });
})(jQuery);
