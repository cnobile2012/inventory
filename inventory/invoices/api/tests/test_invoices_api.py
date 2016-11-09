# -*- coding: utf-8 -*-
#
# inventory/invoices/api/tests/test_invoices_api.py
#

from django.contrib.auth import get_user_model

from dcolumn.dcolumns.models import ColumnCollection

from rest_framework.reverse import reverse
from rest_framework import status

from inventory.common.api.tests.base_test import BaseTest
from inventory.invoices.models import Condition, Item, Invoice, InvoiceItem

UserModel = get_user_model()


class TestConditionAPI(BaseTest):

    def __init__(self, name):
        super(TestConditionAPI, self).__init__(name)

    def setUp(self):
        super(TestConditionAPI, self).setUp()

    def test_GET_condition_list_with_invalid_permissions(self):
        """
        Test the condition_list endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        uri = reverse('condition-list')
        self._test_users_with_invalid_permissions(
            uri, method, default_user=False)

    def test_GET_condition_list_with_valid_permissions(self):
        """
        Test the condition_list endpoint with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        uri = reverse('condition-list')
        self._test_users_with_valid_permissions(
            uri, method, default_user=False)

    def test_OPTIONS_condition_list_with_invalid_permissions(self):
        """
        Test that the method OPTIONS fails with invald permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'options'
        uri = reverse('condition-list')
        self._test_users_with_invalid_permissions(
            uri, method, default_user=False)

    def test_OPTIONS_condition_list_with_valid_permissions(self):
        """
        Test that the method OPTIONS brings back the correct data.
        """
        method = 'options'
        uri = reverse('condition-list')
        self._test_users_with_valid_permissions(
            uri, method, default_user=False)

    def test_GET_condition_detail_with_invalid_permissions(self):
        """
        Test that a GET on the condition_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        uri = reverse('condition-detail', kwargs={'pk': 1})
        self._test_users_with_invalid_permissions(uri, method)

    def test_GET_condition_detail_with_valid_permissions(self):
        """
        Test that a GET to condition_detail passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        uri = reverse('condition-detail', kwargs={'pk': 1})
        method = 'get'
        self._test_users_with_valid_permissions(uri, method)

    def test_OPTIONS_condition_detail_with_invalid_permissions(self):
        """
        Test that the method OPTIONS fails with invald permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'options'
        uri = reverse('condition-detail', kwargs={'pk': 1})
        self._test_users_with_invalid_permissions(uri, method)

    def test_OPTIONS_condition_detail_with_valid_permissions(self):
        """
        Test that the method OPTIONS brings back the correct data.
        """
        method = 'options'
        uri = reverse('condition-detail', kwargs={'pk': 1})
        self._test_users_with_valid_permissions(uri, method)


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
        kwargs = {}
        kwargs['name'] = "Test Collection"
        kwargs['related_model'] = 'item'
        kwargs['creator'] = self.user
        kwargs['updater'] = self.user
        self.collection = ColumnCollection.objects.create(**kwargs)

    def test_GET_item_list_with_invalid_permissions(self):
        """
        Test the item_list endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        item_number = "NE555"
        item = self._create_item(self.project, self.collection, item_number)
        uri = reverse('item-list')
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_GET_item_list_with_valid_permissions(self):
        """
        Test the item_list endpoint with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        item_number = "NE555"
        item = self._create_item(self.project, self.collection, item_number)
        uri = reverse('item-list')
        self._test_users_with_valid_permissions(uri, method, default_user=False)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_POST_item_list_with_invalid_permissions(self):
        """
        Test that a POST to item_list fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'post'
        uri = reverse('item-list')
        data = {}
        su = data.setdefault('SU', {})
        su['item_number'] = 'NE555'
        su['project'] = self.project_uri
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            uri, method, request_data=data)
        data.setdefault('POW', su.copy())
        data.setdefault('PMA', su.copy())
        data.setdefault('PDU', su.copy())
        self._test_project_users_with_invalid_permissions(
            uri, method, request_data=data)

    def test_POST_item_list_with_valid_permissions(self):
        """
        Test that a POST to item_list passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'post'
        uri = reverse('item-list')
        data = {}
        su = data.setdefault('SU', {})
        su['item_number'] = 'NE555'
        su['project'] = self.project_uri
        ad = data.setdefault('AD', su.copy())
        ad['item_number'] = 'NE556N'
        du = data.setdefault('DU', su.copy())
        du['item_number'] = 'LM311'
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)
        pow = data.setdefault('POW', su.copy())
        pow['item_number'] = 'UA1489'
        pma = data.setdefault('PMA', su.copy())
        pma['item_number'] = 'UA1488'
        pdu = data.setdefault('PDU', su.copy())
        pdu['item_number'] = 'LM393D'
        self._test_project_users_with_valid_permissions(
            uri, method, project_user=False, request_data=data)

    def test_OPTIONS_item_list_with_invalid_permissions(self):
        """
        Test that the method OPTIONS fails with invald permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'options'
        uri = reverse('item-list')
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_OPTIONS_item_list_with_valid_permissions(self):
        """
        Test that the method OPTIONS brings back the correct data.
        """
        method = 'options'
        uri = reverse('item-list')
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_GET_item_detail_with_invalid_permissions(self):
        """
        Test that a GET on the item_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        item = self._create_item(self.project, self.collection, "NE555")
        uri = reverse('item-detail', kwargs={'public_id': item.public_id})
        method = 'get'
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_GET_item_detail_with_valid_permissions(self):
        """
        Test that a GET to item_detail passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        item = self._create_item(self.project, self.collection, "NE555")
        uri = reverse('item-detail', kwargs={'public_id': item.public_id})
        method = 'get'
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_PUT_item_detail_with_invalid_permissions(self):
        """
        Test that a PUT to item_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        item = self._create_item(self.project, self.collection, "NE555")
        uri = reverse('item-detail', kwargs={'public_id': item.public_id})
        method = 'put'
        data = {}
        su = data.setdefault('SU', {})
        su['item_number'] = 'NE555'
        su['project'] = self.project_uri
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            uri, method, request_data=data)
        data.setdefault('POW', su.copy())
        data.setdefault('PMA', su.copy())
        data.setdefault('PDU', su.copy())
        self._test_project_users_with_invalid_permissions(
            uri, method, request_data=data)

    def test_PUT_item_detail_with_valid_permissions(self):
        """
        Test that a PUT to item_detail passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        item = self._create_item(self.project, self.collection, "NE555")
        uri = reverse('item-detail', kwargs={'public_id': item.public_id})
        method = 'put'
        data = {}
        su = data.setdefault('SU', {})
        su['item_number'] = 'NE555'
        su['project'] = self.project_uri
        ad = data.setdefault('AD', su.copy())
        ad['item_number'] = 'NE556N'
        du = data.setdefault('DU', su.copy())
        du['item_number'] = 'LM311'
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)
        pow = data.setdefault('POW', su.copy())
        pow['item_number'] = 'UA1489'
        pma = data.setdefault('PMA', su.copy())
        pma['item_number'] = 'UA1488'
        pdu = data.setdefault('PDU', su.copy())
        pdu['item_number'] = 'LM393D'
        self._test_project_users_with_valid_permissions(
            uri, method, project_user=False, request_data=data)

    def test_PATCH_item_detail_with_invalid_permissions(self):
        """
        Test that a PATCH to item_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        item = self._create_item(self.project, self.collection, "NE555")
        uri = reverse('item-detail', kwargs={'public_id': item.public_id})
        method = 'patch'
        data = {}
        su = data.setdefault('SU', {})
        su['item_number'] = 'NE556N'
        su['project'] = self.project_uri
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            uri, method, request_data=data)
        data.setdefault('POW', su.copy())
        data.setdefault('PMA', su.copy())
        data.setdefault('PDU', su.copy())
        self._test_project_users_with_invalid_permissions(
            uri, method, request_data=data)

    def test_PATCH_item_detail_with_valid_permissions(self):
        """
        Test that a PATCH to item_detail passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        item = self._create_item(self.project, self.collection, "NE555")
        uri = reverse('item-detail', kwargs={'public_id': item.public_id})
        method = 'patch'
        data = {}
        su = data.setdefault('SU', {})
        su['item_number'] = 'NE556N'
        ad = data.setdefault('AD', {})
        ad['item_number'] = 'LM311'
        du = data.setdefault('DU', {})
        du['item_number'] = 'UA1489'
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)
        pow = data.setdefault('POW', {})
        pow['item_number'] = 'UA1488'
        pma = data.setdefault('PMA', {})
        pma['item_number'] = 'LM393D'
        pdu = data.setdefault('PDU', {})
        pdu['item_number'] = 'ULN2003A'
        self._test_project_users_with_valid_permissions(
            uri, method, project_user=False, request_data=data)

    def test_DELETE_item_detail_with_invalid_permissions(self):
        """
        Test that a DELETE to item_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'delete'
        item = self._create_item(self.project, self.collection, "NE555")
        uri = reverse('item-detail', kwargs={'public_id': item.public_id})
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_DELETE_item_detail_with_valid_permissions(self):
        """
        Test that a DELETE to item_detail pass' with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'delete'
        # Test SUPERUSER
        item = self._create_item(self.project, self.collection, "NE555")
        uri = reverse('item-detail', kwargs={'public_id': item.public_id})
        self._test_superuser_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test ADMINISTRATOR
        item = self._create_item(self.project, self.collection, "NE555")
        uri = reverse('item-detail', kwargs={'public_id': item.public_id})
        self._test_administrator_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test DEFAULT_USER
        ## This is an invalid test since the DEFAULT_USER has no access.
        # Test PROJECT_OWNER
        item = self._create_item(self.project, self.collection, "NE555")
        uri = reverse('item-detail', kwargs={'public_id': item.public_id})
        self._test_project_owner_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test PROJECT_MANAGER
        item = self._create_item(self.project, self.collection, "NE555")
        uri = reverse('item-detail', kwargs={'public_id': item.public_id})
        self._test_project_manager_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test PROJECT_USER
        ## This is an invalid test since the PROJECT_USER has no access.

    def test_OPTIONS_item_detail_with_invalid_permissions(self):
        """
        Test that the method OPTIONS fails with invald permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'options'
        item = self._create_item(self.project, self.collection, "NE555")
        uri = reverse('item-detail', kwargs={'public_id': item.public_id})
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_OPTIONS_item_detail_with_valid_permissions(self):
        """
        Test that the method OPTIONS brings back the correct data.
        """
        method = 'options'
        item = self._create_item(self.project, self.collection, "NE555")
        uri = reverse('item-detail', kwargs={'public_id': item.public_id})
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_read_only_shared_projects(self):
        """
        Test read only capability of item from shared projects.
        """
        #self.skipTest("Temporarily skipped")
        # Create a second user
        user, client = self._create_user(
            username="SecondUser", password="0987654321")
        # Create second project with second user
        project = self._create_project(self.in_type, name="Test Project_1")
        project.process_members([user])
        # Create an item for second project sharing default project
        item_number_1 = "NE555"
        item_1 = self._create_item(project, self.collection, item_number_1)
        # Add the default user to the default project and create an item
        self.project.process_members([self.user])
        item_number_2 = "LM7805"
        item_2 = self._create_item(self.project, self.collection, item_number_2)
        uri = reverse('item-detail', kwargs={'public_id': item_2.public_id})
        # Test that secode project cannot read default project's item.
        response = client.get(uri, **self._HEADERS)
        msg = "Response: {} should be {}, content: {}, uri: {}".format(
            response.status_code, status.HTTP_404_NOT_FOUND, response.data, uri)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': "Not found.",
            })
        # Test that second project can read by the default project's item.
        item_2.process_shared_projects([project])
        response = client.get(uri, **self._HEADERS)
        msg = "Response: {} should be {}, content: {}, uri: {}".format(
            response.status_code, status.HTTP_200_OK, response.data, uri)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
