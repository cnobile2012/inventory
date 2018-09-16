# -*- coding: utf-8 -*-
#
# inventory/common/tests/test_storage_models.py
#

from inventory.projects.models import Project

from ..storage import create_file_path

from .base_tests import BaseTest

class TestStorage(BaseTest):

    def __init__(self, name):
        super().__init__(name)

    def setUp(self):
        super().setUp()
        self.inventory_type = self._create_inventory_type()
        self.project = self._create_project(self.inventory_type)

    def test_create_file_path(self):
        #self.skipTest("Temporarily skipped")
        filename = "some_file.jpg"
        path = create_file_path(self.project, filename)
        new_path = "{}/{}/{}".format(
            self.project._meta.app_label, self.project.public_id, filename)
        msg = "The generated path '{}' should be '{}'.".format(path, new_path)
        self.assertTrue(path == new_path, msg)
