# -*- coding: utf-8 -*-
#
# inventory/common/tests/record_creation.py
#

from inventory.categories.models import Category
from inventory.projects.models import InventoryType, Project


class RecordCreation(object):
    _INV_TYPE_NAME = "Test Inventory"
    _PROJECT_NAME = "My Test Project"

    def _create_inventory_type(self, name=_INV_TYPE_NAME):
        kwargs = {}
        kwargs['name'] = name
        kwargs['creator'] = self.user
        kwargs['updater'] = self.user
        return InventoryType.objects.create(**kwargs)

    def _create_project(self, i_type, name=_PROJECT_NAME, members=[],
                        public=Project.YES):
        kwargs = {}
        kwargs['name'] = name
        kwargs['inventory_type']= i_type
        kwargs['public'] = public
        kwargs['creator'] = self.user
        kwargs['updater'] = self.user
        obj, created = Project.objects.get_or_create(name=name, defaults=kwargs)
        obj.process_members(members)
        return obj

    def _create_category(self, project, name, parent=None):
        kwargs = {}
        kwargs['project'] = project
        kwargs['name'] = name
        kwargs['parent'] = parent
        kwargs['creator'] = self.user
        kwargs['updater'] = self.user
        return Category.objects.create(**kwargs)
