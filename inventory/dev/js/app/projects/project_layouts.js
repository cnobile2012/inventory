/*
 * Project Layouts
 *
 * js/app/projects/project_layouts.js
 */

"use strict";


class ProjectListLayout extends Layout {
  constructor(options) {
    super(options);
    this.template = '#project-list-layout';
    this.regions = {
      actions: '.actions-bar-container',
      list: '.list-container'
    };
  }

  get className() {
    return 'row page-container';
  }
}


class ProjectListActionBar extends ModelView {
  constructor(options) {
    super(options);
    this.template = '#project-list-action-bar';
  }

  get className() {
    return 'options-bar col-xs-12';
  }

  get events() {
    return {
      'click button': 'createProject'
    };
  }

  createProject() {
    App.router.navigate('projects/new', true);
  }
}


class ProjectListItemView extends ModelView {
  constructor(options) {
    super(options);
    this.template = '#project-list-item';
  }

  get className() {
    return 'col-xs-12 col-sm-6 col-md-3';
  }

  get events() {
    return {
      'click #delete': 'deleteProject',
      'click #view': 'viewProject'
    };
  }

  initialize(options) {
    this.listenTo(options.model, 'change', this.render);
  }

  deleteProject() {
    this.trigger('project:delete', this.model);
  }

  viewProject() {
    let projectId = this.model.get('id');
    App.router.navigate(`projects/view/${projectId}`, true);
  }
}


class ProjectListView extends CollectionView {
  constructor(options) {
    super(options);
    this.modelView = ProjectListItemView;
  }

  get className() {
    return 'project-list';
  }
}


class ProjectList {
  constructor(options) {
    // Region where the application will be placed
    this.region = options.region;

    // Allow subapplication to listen and trigger events,
    // useful for subapplication wide events
    _.extend(this, Backbone.Events);
  }

  showList(projects) {
    // Create the views
    let layout = new ProjectListLayout(),
        actionBar = new ProjectListActionBar(),
        projectList = new ProjectListView({collection: projects});

    // Show the views
    this.region.show(layout);
    layout.getRegion('actions').show(actionBar);
    layout.getRegion('list').show(projectList);

    this.listenTo(projectList, 'item:project:delete', this.deleteProject);
  }

  deleteProject(view, project) {
    App.askConfirmation('The project will be deleted', (isConfirm) => {
      if (isConfirm) {
        project.destroy({
          success() {
            App.notifySuccess('Project was deleted');
          },
          error() {
            App.notifyError('Ooops... Something went wrong');
          }
        });
      }
    });
  }

  /*
   * Close any active view and remove event listeners
   * to prevent zombie functions
   */
  destroy() {
    this.region.remove();
    this.stopListening();
  }
};
