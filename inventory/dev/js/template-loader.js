/*
 * Template loading utility as found in "Backbone.js Cookbook"
 * by: Vadim Mirgorod -- PACKT Publishing
 */

(function($) {
  $(document).ready(function () {
    // Store variable within global jQuery object.
    $.tpl = {}

    $('script.template').each(function(index) {
      // Load template from DOM.
      $.tpl[$(this).attr('id')] = _.template($(this).html());
      // Remove template from DOM.
      $(this).remove();
    });
  });
})(jQuery);
