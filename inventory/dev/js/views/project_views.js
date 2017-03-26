/*
 * Project view
 *
 * js/views/project_view.js
 */

"use strict";


// Single project view
App.Views.Project = Backform.Form.extend();


// Test object, if it works then call it in the project menu.
App.forms.projectForm = function(model) {
  var fields = [
    {name: 'public_id',
     label: App.models.projectMeta.get('public_id').label,
     required: App.models.projectMeta.get('public_id').required,
     control: 'uneditable-input',
     helpMessage: App.models.projectMeta.get('public_id').help_text
    },
    {name: 'inventory_type',
     label: App.models.projectMeta.get('inventory_type').label,
     required: App.models.projectMeta.get('inventory_type').required,
     control: 'select',
     options: [],
     helpMessage: App.models.projectMeta.get('inventory_type').help_text
    },
    {name: 'name',
     label: App.models.projectMeta.get('name').label,
     required: App.models.projectMeta.get('name').required,
     control: 'input',
     helpMessage: App.models.projectMeta.get('name').help_text
    },
    {name: 'image',
     label: App.models.projectMeta.get('image').label,
     required: App.models.projectMeta.get('image').required,
     control: 'input',
     helpMessage: App.models.projectMeta.get('image').help_text
    },
    {name: 'memberships',
     label: App.models.projectMeta.get('memberships').label,
     required: App.models.projectMeta.get('memberships').required,
     control: 'input',
     helpMessage: App.models.projectMeta.get('memberships').help_text
    },
    {name: 'public',
     label: App.models.projectMeta.get('public').label,
     required: App.models.projectMeta.get('public').required,
     control: 'checkbox',
     helpMessage: App.models.projectMeta.get('public').help_text
    },
    {name: 'active',
     label: App.models.projectMeta.get('active').label,
     required: App.models.projectMeta.get('active').required,
     control: 'checkbox',
     helpMessage: App.models.projectMeta.get('active').help_text
    }
  ];

  _.forEach(fields, function(value, key) {
    if(value.name === 'inventory_type') {
      var name = "", label = "", field = value;

      _.forEach(App.collections.inventoryType, function(value, key) {
        label = App.collections.inventoryType.at(key).get('name');
        value = App.collections.inventoryType.at(key).get('public_id');
        field.options.push({label: label, value: value});
      })
    }
  })

  var publicId = model.get('public_id');
  var $template = $(App.templates.project_template());
  $template.attr('id', publicId);
  $template.appendTo($('#projects div.data-pane'));
  var options = {
    template: $template[0],
    model: model,
    el: $("#" + publicId),
    fields: fields,
    showRequiredAsAsterisk: true
  };

  new App.Views.Project(options).render();
};
