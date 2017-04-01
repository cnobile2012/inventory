/*
 * Project view
 *
 * js/views/project_view.js
 */

"use strict";


// Single project view
App.Views.Project = Backform.Form.extend();


// Test object, if it works then call it in the project menu.
App.Forms.Project = function(model) {
  var fields = [
    {name: 'public_id',
     label: App.models.projectMeta.get('public_id').label,
     required: App.models.projectMeta.get('public_id').required,
     control: 'uneditable-input',
     helpMessage: App.models.projectMeta.get('public_id').help_text
    },
    {name: 'inventory_type_public_id',
     label: App.models.projectMeta.get('inventory_type').label,
     required: true, // Force true--the endpoint has two ways of doing this.
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
    },
    {name: 'creator',
     label: App.models.projectMeta.get('creator').label,
     control: 'uneditable-input'
    },
    {name: 'created',
     label: App.models.projectMeta.get('created').label,
     control: 'uneditable-input'
    },
    {name: 'updater',
     label: App.models.projectMeta.get('updater').label,
     control: 'uneditable-input'
    },
    {name: 'updated',
     label: App.models.projectMeta.get('updated').label,
     control: 'uneditable-input'
    }
  ];

  _.forEach(fields, function(value, key) {
    if(value.name === 'inventory_type_public_id') {
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
  $template.appendTo($('#projects #' + publicId));
  var options = {
    template: $template[0],
    model: model,
    el: $("#" + publicId + ' form'),
    fields: fields,
    showRequiredAsAsterisk: true
  };

  new App.Views.Project(options).render();
};
