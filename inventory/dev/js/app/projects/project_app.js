/*
 * Project Facade
 *
 * js/app/projects/project_app.js
 */

'use strict';


// TODO: enable pagination
class ProjectsApp {

  constructor(options) {
    this.region = options.region;
  }

  get accept() {
    return App.models.rootModel.get('projects').projects
      .accept_header.json['1.0'];
  }

  get contentType() {
    return App.models.rootModel.get('projects').projects
      .content_type_header.json['1.0'];
  }

  showProjectList(page) {
    //App.events.trigger('loading:start');
    //App.events.trigger('app:projects:started');
    this.fetchProjectMeta();
    // The projects themselves are returned with the fetch to the user
    // however, we can reference them in the App.models.projects.
  }

  fetchProjectMeta() {
    if (App.models.projectMeta === (void 0)) {
      App.models.projectMeta = new ProjectMetaModel();
    }

    if (App.models.projectMeta.values().length === 0) {
      return App.models.projectMeta.fetch({
        accepts: { json: this.accept },
        success: (model, response, options) => {
          this.showList(App.models.projects);
          //App.trigger('loading:stop');
        },
        error: (model, response, options) => {
          App.utils.showMessage(options.textStatus + " "
                                + options.errorThrown);
          //App.trigger('loading:stop');
          //App.trigger('server:error', response);
        }
      });
    }
  }

  showCreateProjectForm() {
    App.events.trigger('app:projects:new:started');
    this.showEditor(new ProjectModel());
  }

  showProjectEditById(projectId) {
    App.events.trigger('loading:start');
    App.events.trigger('app:projects:started');

    new ProjectModel({id: projectId}).fetch({
      success: (model) => {
        this.showEditor(model);
        App.events.trigger('loading:stop');
      },
      fail: (collection, response) => {
        App.events.trigger('loading:stop');
        App.events.trigger('server:error', response);
      }
    });
  }

  showProjectById(projectId) {
    App.events.trigger('loading:start');
    App.events.trigger('app:projects:started');

    new Project({id: projectId}).fetch({
      success(model) {
        this.showViewer(model);
        App.events.trigger('loading:stop');
      },
      fail(collection, response) {
        App.events.trigger('loading:stop');
        App.events.trigger('server:error', response);
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
    if(!(this.currentController &&
         this.currentController instanceof Controller)) {
      if(this.currentController && this.currentController.destroy) {
        this.currentController.destroy();
      }

      this.currentController = new Controller({region: this.region});
    }

    return this.currentController;
  }
};
