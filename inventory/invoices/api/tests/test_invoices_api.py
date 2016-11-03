# -*- coding: utf-8 -*-
#
# inventory/invoices/api/tests/test_invoices_api.py
#

from django.contrib.auth import get_user_model

from rest_framework.reverse import reverse
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND)

from inventory.common.api.tests.base_test import BaseTest






class TestItemAPI(BaseTest):

    def __init__(self, name):
        super(TestItemAPI, self).__init__(name)

    def setUp(self):
        super(TestItemAPI, self).setUp()
        # Create an InventoryType and Project.
        self.in_type = self._create_inventory_type()
        self.project = self._create_project(self.in_type, members=[self.user])
        kwargs = {'public_id': self.project.public_id}
        self.project_uri = reverse('project-detail', kwargs=kwargs)







    def test_read_only_shared_projects(self):
        """
        Test read only capability of item from shared projects.
        """
        self.skipTest("Temporarily skipped")
        # Create a second user
        user, client = self._create_user(
            username="SecondUser", password="0987654321")
        # Create second project with second user
        project = self._create_project(
            self.inventory_type, name="Test Project_1")
        project.process_members([user])
        # Create an item for second project sharing default project
        item_number_1 = "NE555"
        item_1 = self._create_item(project, self.collection, item_number_1)
        # Add the default user to the default project and create an item
        self.project.process_members([self.user])
        item_number_2 = "LM7805"
        item_2 = self._create_item(self.project, self.collection, item_number_2)
        item_2.process_shared_projects([project])
        # Test that second project can read default project's item.
        uri = reverse('item-detail', kwargs={'public_id': item_2.public_id})
