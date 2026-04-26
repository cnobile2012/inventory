/*
 * Project Viewer
 *
 * js/projects/project_viewer.js
 */

'use strict';


class ProjectViewLayout extends Layout {

  get el() { return '#projects .tab-choice-pane'; }

  constructor(options) {
    super(options);
    this.regions = {
      actions: 'action-bar',
      content: 'items'
    };
  }
}


class ProjectViewActionBar extends ModelView {

  get template() { return App.templates.project_action_bar; }
  get multiple() { return true; }

  get events() {
    return {
      'click button[name=project-save]': 'saveProject',
      'click button[name=project-edit]': 'editProject',
      'click button[name=project-close]': 'closeProject',
      'click button[name=project-delete]': 'deleteProject'
    };
  }

  constructor(options) {
    super(options);
    this.setElement('#' + options.model.id);
  }

  saveProject(event) {
    console.log('save', this, event);

  }

  editProject(event) {
    console.log('edit', this, event);

  }

  closeProject(event) {
    let close = 'app:projects:' + this.model.id + ':close',
        contact = 'app:projects:' + this.model.id + ':contact';
    App.events.trigger(close);
    App.events.stopListening(App.events, close);
    App.events.trigger(contact);
    App.events.stopListening(App.events, contact);

    // Revert back to #Projects
    console.log('POOP', App.openDataPanes.projects);
    if (App.openDataPanes.projects <= 0) {
      App.events.trigger('app:projects:projects');
    } else {
      let id = $('#projects .data-pane').attr('id');
      App.router.navigate('projects/' + id); //, {trigger: true});
    }
  }

  deleteProject(event) {
    console.log('delete', this, event);

  }
}


class ProjectContent extends ModelView {

  get template() { return App.templates.project_content; }
  get multiple() { return true; }

  get events() {
    return {
      click: 'makeActive'
    };
  }

  constructor(options) {
    super(options);
    this.setElement('#' + options.model.id);
  }

  onRender() {
    if ($('#' + this.model.id + ' .items').length) {
      App.events.listenTo(
        App.events, 'app:projects:' + this.model.id + ':contact',
        this.makeActive.bind(this));
    }

    this.makeActive();
  }

  makeActive(event) {
    $('#projects .data-pane .items').removeClass('darken');

    if (App.openDataPanes.projects > 0) {
      App.router.navigate('projects/' + this.model.id, {trigger: true});
    }

    if (App.openDataPanes.projects > 1) {
      $('#projects .data-pane:not(#' + this.model.id  + ') > .items')
        .addClass('darken');
    }
  }
}


class ProjectViewer {

  constructor(options) {
    this.region = new Region({el: ''});
    // Allow subapplication to listen and trigger events,
    // useful for subapplication wide events
    _.extend(this, Backbone.Events);
  }

  showProject(project) {
    // Create the views
    let layout = new ProjectViewLayout(),
        actionBar = new ProjectViewActionBar({model: project}),
        content = new ProjectContent({model: project});

    // Show the views
    this.region.show(layout);
    layout.getRegion('actions').show(actionBar, true);
    layout.getRegion('content').show(content, true);

    //this.listenTo(projectMenu, 'project:delete', this._deleteProject);
  }

  _deleteProject(project) {
    App.askConfirmation('The project will be deleted', isConfirm => {
      if (isConfirm) {
        project.destroy({
          success() {
            // Regirect user to the projects list after
            // deletion
            App.notifySuccess('Project was deleted');
            App.router.navigate('projects', {trigger: true});
          },
          error() {
            // Show error message when something is wrong
            App.notifyError('Something goes wrong');
          }
        });
      }
    });
  }
}
