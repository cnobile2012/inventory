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
      'projects/:id': 'showProject',
      'projects/create': 'createProject',
      'projects/edit/:id': 'editProject',
      '*nothingMatchedRouter': 'pageNotFoundRoute'
    };
  }

//  get collection() { return App.models.projectProxies; }

//  constructor(options) {
//    super(options);
//  }

  initialize() {
    /*
    this.route(/projects\/?/, 'showProjectList');
    this.route('projects/create', 'createProject');
    this.route('projects/:id', 'showProject');
    this.route('projects/edit/:id', 'editProject');
    this.route('*nothingMatchedRouter', 'pageNotFoundRoute');
    //this._bindRoutes();
    */
    App.events.bind('app:projects:projects', this.goToProjects.bind(this));
  }

  goToProjects() {
    this.navigate('projects'); //, {trigger: true});
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
    if (!App.doesElementExist('#' + id + ' .action-bar')) {
      let projectApp = this.startApp();
      App.events.trigger('app:auth:auth',
                         _.bind(projectApp.showProjectById, projectApp, id));
    }

  }

  editProject(id) {
    this.startApp().showProjectEditById(id);
  }

  pageNotFoundRoute(name) {
    console.error("ProjectsRouter: '" + name + "' Did not match any routes!");
  }

  startApp() {
    return App.startSubApplication(ProjectsApp);
  }
}

App.Routers.ProjectsRouter = ProjectsRouter;
