/*
 * Project Facade
 *
 * js/app/projectss/project_facade.js
 */

'use strict';


// TODO: enable pagination
class ProjectsFacade {
  constructor(options) {
    this.region = options.region;
  }

  showProjectList() {
    App.trigger('loading:start');
    App.trigger('app:projects:started');

    new ProjectCollection().fetch({
      success: (collection) => {
        // Show the project list subapplication if
        // the list can be fetched
        this.showList(collection);
        App.trigger('loading:stop');
      },
      fail: (collection, response) => {
        // Show error message if something goes wrong
        App.trigger('loading:stop');
        App.trigger('server:error', response);
      }
    });
  }

  showNewProjectForm() {
    App.trigger('app:projects:new:started');
    this.showEditor(new ProjectModel());
  }

  showProjectEditorById(projectId) {
    App.trigger('loading:start');
    App.trigger('app:projects:started');

    new ProjectModel({id: projectId}).fetch({
      success: (model) => {
        this.showEditor(model);
        App.trigger('loading:stop');
      },
      fail: (collection, response) => {
        App.trigger('loading:stop');
        App.trigger('server:error', response);
      }
    });
  }

  showProjectById(projectId) {
    App.trigger('loading:start');
    App.trigger('app:projects:started');

    new Project({id: projectId}).fetch({
      success: (model) => {
        this.showViewer(model);
        App.trigger('loading:stop');
      },
      fail: (collection, response) => {
        App.trigger('loading:stop');
        App.trigger('server:error', response);
      }
    });
  }

  showList(projects) {
    let projectList = this.startController(ProjectList);
    projectList.showList(projects);
  }

  showEditor(project) {
    let projectEditor = this.startController(ProjectEditor);
    projectEditor.showEditor(project);
  }

  showViewer(project) {
    let projectViewer = this.startController(ProjectViewer);
    projectViewer.showProject(project);
  }

  startController(Controller) {
    if (this.currentController &&
        this.currentController instanceof Controller) {
      return this.currentController;
    }

    if (this.currentController && this.currentController.destroy) {
      this.currentController.destroy();
    }

    this.currentController = new Controller({region: this.region});
    return this.currentController;
  }
};
