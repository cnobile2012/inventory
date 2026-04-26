/*
 * Project Application
 *
 * js/app/projects/project_app.js
 */

'use strict';


class ProjectsApp {

  get region() { return new Region({el: '.data-pane'}); }

  get accept() {
    return App.models.rootModel.get('projects').projects
      .accept_header.json['1.0'];
  }

  get contentType() {
    return App.models.rootModel.get('projects').projects
      .content_type_header.json['1.0'];
  }

  showProjectList() {
    async function run(self) {
      await self.fetchInventoryTypeMeta();
      await self.fetchInventoryTypes();
      await self.fetchProjectMeta();
      await self.fetchProjects();
      await self.showList(App.models.projectProxies);
    }

    run(this);
  }

  showProjectById(publicId) {
    async function run(self) {
      if (!App.doesElementExist('#projects .pane-nav ul')) {
        await self.showProjectList();
      }

      let model = await App.waitFor(() => {
        return App.models.projects.findWhere({'public_id': publicId});
      }, 400);

      if ($('#' + publicId).length <= 0) {
        App.events.trigger('app:projects:' + publicId + ':open');
      }

      await self.showViewer(model);
    }

    run(this);
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

  showList(projects) {
    this.startController(ProjectList).showList(projects);
  }

  showEditor(project) {
    this.startController(ProjectEditor).showEditor(project);
  }

  showViewer(project) {
    this.startController(ProjectViewer).showProject(project);
  }

  fetchInventoryTypeMeta() {
    if (App.models.inventoryTypeMeta === (void 0)) {
      App.models.inventoryTypeMeta = new InventoryTypeMetaModel();
    }

    //App.events.trigger('loading:start');
    //App.events.trigger('app:projects:started');

    if (App.models.inventoryTypeMeta.values().length === 0) {
      return App.models.inventoryTypeMeta.fetch({
        accepts: { json: this.accept }
      }).then((json) => {
        console.log('InventoryType meta data fetch completed successfully.');
      }).catch((error) => {
        App.utils.showMessage("Error: " + error);
        //App.trigger('server:error', response);
      }).always(() => {
        //App.trigger('loading:stop');
      });
    } else {
      return Promise.resolve();
    }
  }

  fetchInventoryTypes() {
    if (App.models.inventoryTypes === (void 0)) {
      App.models.inventoryTypes = new InventoryTypeCollection();
    }

    //App.events.trigger('loading:start');
    //App.events.trigger('app:projects:started');

    if (App.models.inventoryTypes.length === 0) {
      return App.models.inventoryTypes.fetch({
        accepts: { json: this.accept }
      }).then((json) => {
        console.log('InventoryTypes data fetch completed successfully.');
      }).catch((error) => {
        App.utils.showMessage("Error: " + error);
        //App.trigger('server:error', response);
      }).always(() => {
        //App.trigger('loading:stop');
      });
    } else {
      return Promise.resolve();
    }
  }

  fetchProjectMeta() {
    if (App.models.projectMeta === (void 0)) {
      App.models.projectMeta = new ProjectMetaModel();
    }

    //App.events.trigger('loading:start');
    //App.events.trigger('app:projects:started');

    if (App.models.projectMeta.values().length === 0) {
      return App.models.projectMeta.fetch({
        accepts: { json: this.accept }
      }).then((json) => {
        console.log('Project meta data fetch completed successfully.');
      }).catch((error) => {
        App.utils.showMessage("Error: " + error);
        //App.trigger('server:error', response);
      }).always(() => {
        //App.trigger('loading:stop');
      });
    } else {
      return Promise.resolve();
    }
  }

  /*
   * This method only returns projects when there have been none loaded.
   */
  fetchProjects(reset=false) {
    if (App.models.projects === (void 0)) {
      App.models.projects = new ProjectCollection();
    }

    //App.events.trigger('loading:start');
    //App.events.trigger('app:projects:started');

    if (App.models.projects.length < 1) {
      return App.models.projects.fetch({
        reset: reset
      }).then((json) => {
        console.log('Project data fetch completed successfully.');
      }).catch((error) => {
        console.error('Project data fetch failed, ' + error);
      }).always(() => {
        //App.events.trigger('loading:stop');
      });
    } else {
      return Promise.resolve();
    }
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
