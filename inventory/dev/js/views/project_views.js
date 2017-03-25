/*
 * Project view
 *
 * js/views/project_view.js
 */

"use strict";


// Single project view
App.Views.Project = Backform.Form.extend({
  tagName: function() {
    return "#projects #" + this.model.get('public_id');
  },

  template: function() {
    return App.templates.project_template();
  }
});

// Test object, if it works then call it in the project menu.
var projectForm = function(model) {
  return new App.Views.Project({
    model: model,
    fields: [
      {name: 'public_id',
       label: App.models.projectMeta.get('public_id').label,
       control: 'uneditable-input'},
      {name: 'name',
       label: App.models.projectMeta.get('name').label,
       control: 'input'},
      {name: 'inventory_type',
       label: App.models.projectMeta.get('inventory_type').label,
       control: 'select',
       options: getOptions()
      },
    ],

    getOptions: function() {
      var options = [], name = "", label = "";

      _.forEach(App.collections.inventoryType, function(value, key) {
        name = App.collections.inventoryType.at(key).get('name');
        label = App.models.inventoryTypeMeta.get('name').label;
        option.push({label: label, value: name});
      });
    }

  });
};
