/*
 * Project Router
 *
 * js/app/projects/project_router.js
 */

"use strict";


class ProjectsRouter extends Backbone.Router {
  get routes() {
    return {
      'projects': 'showProjectList',
      'projects/page/:page': 'showProjectList',
      'projects/create': 'createProject',
      'projects/show/:id': 'showProject',
      'projects/edit/:id': 'editProject'
    };
  }

  constructor(options) {
    super(options);
    this._bindRoutes();
  }

  showProjectList(page) {
    // Page should be a postive number grater than 0
    page = page || 1;
    page = page > 0 ? page : 1;
    let app = this.startApp();
    app.showProjectList(page);
  }

  createProject() {
    let app = this.startApp();
    app.showNewProjectForm();
  }

  showProject(projectId) {
    let app = this.startApp();
    app.showProjectById(projectId);
  }

  editProject(projectId) {
    let app = this.startApp();
    app.showProjectEditorById(projectId);
  }

  startApp() {
    return App.startSubApplication(ProjectsFacade);
  }
}

App.Routers.ProjectsRouter = ProjectsRouter;
