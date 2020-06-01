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
      'projects/list/:page': 'showProjectList',
      'projects/create': 'createProject',
      'projects/show/:id': 'showProject',
      'projects/edit/:id': 'editProject'
    };
  }

  get region() {
    return new Region({el: '#projects.pane-nav'});
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
    app.showCreateProjectForm();
  }

  showProject(id) {
    let app = this.startApp();
    app.showProjectById(id);
  }

  editProject(id) {
    let app = this.startApp();
    app.showProjectEditById(id);
  }

  startApp() {
    return App.startSubApplication(ProjectsApp, this.region);
  }
}

App.Routers.ProjectsRouter = ProjectsRouter;
