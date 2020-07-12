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
      'projects/create': 'createProject',
      'projects/:id': 'showProject',
      'projects/edit/:id': 'editProject',
      '*nothingMatchedProjectsRouter': 'pageNotFoundRoute'
    };
  }

  constructor(options) {
    super(options);
    this._bindRoutes();
    App.events.bind('app:projects:projects', this.goToProjects.bind(this));
  }

  goToProjects() {
    this.navigate('projects', {trigger: true});
  }

  showProjectList() {
    let projectApp = this.startApp();
    App.events.trigger('app:auth:auth',
                       projectApp.showProjectList.bind(projectApp));
  }

  createProject() {
    this.startApp().showCreateProjectForm();
  }

  showProject(id) {
    this.startApp().showProjectById(id);
  }

  editProject(id) {
    this.startApp().showProjectEditById(id);
  }

  pageNotFoundRoute(failedRoute) {
    console.error("ProjectsRouter: (" + failedRoute
                  + ") Did not match any routes!");
  }

  startApp() {
    return App.startSubApplication(ProjectsApp);
  }
}

App.Routers.ProjectsRouter = ProjectsRouter;
