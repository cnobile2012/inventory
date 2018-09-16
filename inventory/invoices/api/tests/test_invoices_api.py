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
        super().__init__(name)

    def setUp(self):
        super().setUp()

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
        Test that a GET on the condition_detail fails with invalid
        permissions.
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
        super().__init__(name)

    def setUp(self):
        super().setUp()
        # Create an InventoryType and Project.
        self.in_type = self._create_inventory_type()
        self.project = self._create_project(self.in_type, members=[self.user])
        kwargs = {'public_id': self.project.public_id}
        self.project_uri = reverse('project-detail', kwargs=kwargs)
        # Create a ColumnCollection
        kwargs = {}
        kwargs['name'] = "Test Collection"
        kwargs['related_model'] = 'item'
        kwargs['creator'] = self.user
        kwargs['updater'] = self.user
        self.collection = ColumnCollection(**kwargs)
        self.collection.save()

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
        self._test_users_with_valid_permissions(uri, method,
                                                default_user=False)
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
        #self.skipTest("Temporarily skipped")
        method = 'options'
        item = self._create_item(self.project, self.collection, "NE555")
        uri = reverse('item-detail', kwargs={'public_id': item.public_id})
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def _create_shared_project_objects(self):
        # Add the default user to the default project and create an item
        item_number = "LM7805"
        item = self._create_item(self.project, self.collection, item_number)
        uri = reverse('item-detail', kwargs={'public_id': item.public_id})
        # Create a second user
        user, client = self._create_user(
            username="SecondUser", password="0987654321")
        # Create second project with second user
        project = self._create_project(self.in_type, name="Test Project 1")
        project.process_members([user])
        # Create an item for second project sharing default project
        item_number_1 = "NE555"
        item_1 = self._create_item(project, self.collection, item_number_1)
        return client, uri, self.project, item, project, item_1

    def test_GET_only_shared_projects(self):
        """
        Test read only capability of item from shared projects.
        """
        #self.skipTest("Temporarily skipped")
        # Create objects
        (client, uri, project_0, item_0,
         project_1, item_1) = self._create_shared_project_objects()
        # Test that second project cannot read default project's item.
        response = client.get(uri, **self._HEADERS)
        msg = "Response: {} should be {}, content: {}, uri: {}".format(
            response.status_code, status.HTTP_404_NOT_FOUND, response.data,
            uri)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': "Not found.",
            })
        # Share the default project's item with second project.
        item_0.process_shared_projects([project_1])
        # Test that second project can read default project's item.
        response = client.get(uri, **self._HEADERS)
        msg = "Response: {} should be {}, content: {}, uri: {}".format(
            response.status_code, status.HTTP_200_OK, response.data, uri)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)

    def test_invalid_PUT_shared_projects(self):
        #self.skipTest("Temporarily skipped")
        # Create objects
        (client, uri, project_0, item_0,
         project_1, item_1) = self._create_shared_project_objects()
        # Share the default project's item with second project.
        item_0.process_shared_projects([project_1])
        # Test that the shared_project item cannot be updated by a second
        # project user.
        data = {}
        data['item_number'] = 'NE556N'
        data['project'] = reverse('project-detail',
                                  kwargs={'public_id': project_0.public_id})
        response = client.put(uri, data=data, **self._HEADERS)
        msg = "Response: {} should be {}, content: {}, uri: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN, response.data,
            uri)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': "You do not have permission to perform this action.",
            })

    def test_invalid_PATCH_shared_projects(self):
        #self.skipTest("Temporarily skipped")
        # Create objects
        (client, uri, project_0, item_0,
         project_1, item_1) = self._create_shared_project_objects()
        # Share the default project's item with second project.
        item_0.process_shared_projects([project_1])
        # Test that the shared_project item cannot be updated by a second
        # project user.
        data = {'item_number': 'NE556N'}
        response = client.patch(uri, data=data, **self._HEADERS)
        msg = "Response: {} should be {}, content: {}, uri: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN, response.data,
            uri)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': "You do not have permission to perform this action.",
            })

    def test_invalid_DELETE_shared_projects(self):
        #self.skipTest("Temporarily skipped")
        # Create objects
        (client, uri, project_0, item_0,
         project_1, item_1) = self._create_shared_project_objects()
        # Share the default project's item with second project.
        item_0.process_shared_projects([project_1])
        # Test that the shared_project item cannot be updated by a second
        # project user.
        response = client.delete(uri, **self._HEADERS)
        msg = "Response: {} should be {}, content: {}, uri: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN, response.data,
            uri)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': "You do not have permission to perform this action.",
            })

    def test_check_user(self):
        """
        Test that a user is not authorized to access a project.
        """
        #self.skipTest("Temporarily skipped")
        # Create a 2nd user
        kwargs = {}
        kwargs['username'] = 'Second_User'
        kwargs['password'] = 'ykwQ37Ea'
        kwargs['is_active'] = True
        kwargs['is_staff'] = False
        kwargs['login'] = False
        kwargs['is_superuser'] = True
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        # Try to delete a project
        response = client.delete(self.project_uri, **self._HEADERS)
        msg = "Response: {} should be {}, content: {}, uri: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN, response.data,
            self.project_uri)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': "Authentication credentials were not provided.",
            })


class TestInvoiceAPI(BaseTest):

    def __init__(self, name):
        super().__init__(name)

    def setUp(self):
        super().setUp()
        # Create an InventoryType and Project.
        in_type = self._create_inventory_type()
        self.project = self._create_project(in_type, members=[self.user])
        self.project_uri = reverse(
            'project-detail', kwargs={'public_id': self.project.public_id})
        # Create regions
        self.country = self._create_country()
        self.currency = self._create_currency(
            self.country, "US Dollar", "USD", 840, 2)
        self.cur_uri = reverse('currency-detail',
                               kwargs={'pk': self.currency.pk})
        self.supplier = self._create_supplier(self.project)
        self.sup_uri = reverse('supplier-detail',
                               kwargs={'public_id': self.supplier.public_id})

    def test_GET_invoice_list_with_invalid_permissions(self):
        """
        Test the invoice_list endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        invoice_number = "TEST12345"
        invoice = self._create_invoice(
            self.project, self.currency,  self.supplier, invoice_number)
        uri = reverse('invoice-list')
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_GET_invoice_list_with_valid_permissions(self):
        """
        Test the invoice_list endpoint with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        invoice_number = "TEST12345"
        invoice = self._create_invoice(
            self.project, self.currency, self.supplier, invoice_number)
        uri = reverse('invoice-list')
        self._test_users_with_valid_permissions(
            uri, method, default_user=False)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_POST_invoice_list_with_invalid_permissions(self):
        """
        Test that a POST to invoice_list fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'post'
        uri = reverse('invoice-list')
        data = {}
        su = data.setdefault('SU', {})
        su['invoice_number'] = 'TEST12345'
        su['project'] = self.project_uri
        su['currency'] = self.cur_uri
        su['supplier'] = self.sup_uri
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            uri, method, request_data=data)
        data.setdefault('POW', su.copy())
        data.setdefault('PMA', su.copy())
        data.setdefault('PDU', su.copy())
        self._test_project_users_with_invalid_permissions(
            uri, method, request_data=data)

    def test_POST_invoice_list_with_valid_permissions(self):
        """
        Test that a POST to invoice_list passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'post'
        uri = reverse('invoice-list')
        data = {}
        su = data.setdefault('SU', {})
        su['invoice_number'] = 'TEST123456'
        su['project'] = self.project_uri
        su['currency'] = self.cur_uri
        su['supplier'] = self.sup_uri
        ad = data.setdefault('AD', su.copy())
        ad['invoice_number'] = 'TEST234561'
        du = data.setdefault('DU', su.copy())
        du['invoice_number'] = 'TEST345612'
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)
        pow = data.setdefault('POW', su.copy())
        pow['invoice_number'] = 'TEST456123'
        pma = data.setdefault('PMA', su.copy())
        pma['invoice_number'] = 'TEST561234'
        pdu = data.setdefault('PDU', su.copy())
        pdu['invoice_number'] = 'TEST612345'
        self._test_project_users_with_valid_permissions(
            uri, method, project_user=False, request_data=data)

    def test_OPTIONS_invoice_list_with_invalid_permissions(self):
        """
        Test that the method OPTIONS fails with invald permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'options'
        uri = reverse('invoice-list')
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_OPTIONS_invoice_list_with_valid_permissions(self):
        """
        Test that the method OPTIONS brings back the correct data.
        """
        method = 'options'
        uri = reverse('invoice-list')
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_GET_invoice_detail_with_invalid_permissions(self):
        """
        Test that a GET on the invoice_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        invoice_number = "TEST12345"
        invoice = self._create_invoice(
            self.project, self.currency, self.supplier, invoice_number)
        uri = reverse('invoice-detail',
                      kwargs={'public_id': invoice.public_id})
        method = 'get'
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_GET_invoice_detail_with_valid_permissions(self):
        """
        Test that a GET to invoice_detail passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        invoice_number = "TEST12345"
        invoice = self._create_invoice(
            self.project, self.currency, self.supplier, invoice_number)
        uri = reverse('invoice-detail',
                      kwargs={'public_id': invoice.public_id})
        method = 'get'
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_PUT_invoice_detail_with_invalid_permissions(self):
        """
        Test that a PUT to invoice_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        invoice_number = "TEST12345"
        invoice = self._create_invoice(
            self.project, self.currency, self.supplier, invoice_number)
        uri = reverse('invoice-detail',
                      kwargs={'public_id': invoice.public_id})
        method = 'put'
        data = {}
        su = data.setdefault('SU', {})
        su['invoice_number'] = 'TEST12345'
        su['project'] = self.project_uri
        su['currency'] = self.cur_uri
        su['supplier'] = self.sup_uri
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            uri, method, request_data=data)
        data.setdefault('POW', su.copy())
        data.setdefault('PMA', su.copy())
        data.setdefault('PDU', su.copy())
        self._test_project_users_with_invalid_permissions(
            uri, method, request_data=data)

    def test_PUT_invoice_detail_with_valid_permissions(self):
        """
        Test that a PUT to invoice_detail passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        invoice_number = "TEST1234567"
        invoice = self._create_invoice(
            self.project, self.currency, self.supplier, invoice_number)
        uri = reverse('invoice-detail',
                      kwargs={'public_id': invoice.public_id})
        method = 'put'
        data = {}
        su = data.setdefault('SU', {})
        su['invoice_number'] = 'TEST2345671'
        su['project'] = self.project_uri
        su['currency'] = self.cur_uri
        su['supplier'] = self.sup_uri
        ad = data.setdefault('AD', su.copy())
        ad['invoice_number'] = 'TEST3456712'
        du = data.setdefault('DU', su.copy())
        du['invoice_number'] = 'TEST4567123'
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)
        pow = data.setdefault('POW', su.copy())
        pow['invoice_number'] = 'TEST5671234'
        pma = data.setdefault('PMA', su.copy())
        pma['invoice_number'] = 'TEST6712345'
        pdu = data.setdefault('PDU', su.copy())
        pdu['invoice_number'] = 'TEST7123456'
        self._test_project_users_with_valid_permissions(
            uri, method, project_user=False, request_data=data)

    def test_PATCH_invoice_detail_with_invalid_permissions(self):
        """
        Test that a PATCH to invoice_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        invoice_number = "TEST1234567"
        invoice = self._create_invoice(
            self.project, self.currency, self.supplier, invoice_number)
        uri = reverse('invoice-detail',
                      kwargs={'public_id': invoice.public_id})
        method = 'patch'
        data = {}
        su = data.setdefault('SU', {})
        su['invoice_number'] = 'TEST2345671'
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

    def test_PATCH_invoice_detail_with_valid_permissions(self):
        """
        Test that a PATCH to invoice_detail passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        invoice_number = "TEST1234567"
        invoice = self._create_invoice(
            self.project, self.currency, self.supplier, invoice_number)
        uri = reverse('invoice-detail',
                      kwargs={'public_id': invoice.public_id})
        method = 'patch'
        data = {}
        su = data.setdefault('SU', {})
        su['invoice_number'] = 'TEST2345671'
        ad = data.setdefault('AD', {})
        ad['invoice_number'] = 'TEST3456712'
        du = data.setdefault('DU', {})
        du['invoice_number'] = 'TEST4567123'
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)
        pow = data.setdefault('POW', {})
        pow['invoice_number'] = 'TEST5671234'
        pma = data.setdefault('PMA', {})
        pma['invoice_number'] = 'TEST6712345'
        pdu = data.setdefault('PDU', {})
        pdu['invoice_number'] = 'TEST7123456'
        self._test_project_users_with_valid_permissions(
            uri, method, project_user=False, request_data=data)

    def test_DELETE_invoice_detail_with_invalid_permissions(self):
        """
        Test that a DELETE to invoice_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        invoice_number = "TEST1234567"
        method = 'delete'
        invoice = self._create_invoice(
            self.project, self.currency, self.supplier, invoice_number)
        uri = reverse('invoice-detail',
                      kwargs={'public_id': invoice.public_id})
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_DELETE_invoice_detail_with_valid_permissions(self):
        """
        Test that a DELETE to invoice_detail pass' with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        invoice_number = "TEST1234567"
        method = 'delete'
        # Test SUPERUSER
        invoice = self._create_invoice(
            self.project, self.currency, self.supplier, invoice_number)
        uri = reverse('invoice-detail',
                      kwargs={'public_id': invoice.public_id})
        self._test_superuser_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test ADMINISTRATOR
        invoice = self._create_invoice(
            self.project, self.currency, self.supplier, invoice_number)
        uri = reverse('invoice-detail',
                      kwargs={'public_id': invoice.public_id})
        self._test_administrator_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test DEFAULT_USER
        ## This is an invalid test since the DEFAULT_USER has no access.
        # Test PROJECT_OWNER
        invoice = self._create_invoice(
            self.project, self.currency, self.supplier, invoice_number)
        uri = reverse('invoice-detail',
                      kwargs={'public_id': invoice.public_id})
        self._test_project_owner_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test PROJECT_MANAGER
        invoice = self._create_invoice(
            self.project, self.currency, self.supplier, invoice_number)
        uri = reverse('invoice-detail',
                      kwargs={'public_id': invoice.public_id})
        self._test_project_manager_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test PROJECT_USER
        ## This is an invalid test since the PROJECT_USER has no access.

    def test_OPTIONS_invoice_detail_with_invalid_permissions(self):
        """
        Test that the method OPTIONS fails with invald permissions.
        """
        #self.skipTest("Temporarily skipped")
        invoice_number = "TEST1234567"
        method = 'options'
        invoice = self._create_invoice(
            self.project, self.currency, self.supplier, invoice_number)
        uri = reverse('invoice-detail',
                      kwargs={'public_id': invoice.public_id})
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_OPTIONS_invoice_detail_with_valid_permissions(self):
        """
        Test that the method OPTIONS brings back the correct data.
        """
        #self.skipTest("Temporarily skipped")
        invoice_number = "TEST1234567"
        method = 'options'
        invoice = self._create_invoice(
            self.project, self.currency, self.supplier, invoice_number)
        uri = reverse('invoice-detail',
                      kwargs={'public_id': invoice.public_id})
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)


class TestInvoiceItemAPI(BaseTest):

    def __init__(self, name):
        super().__init__(name)

    def setUp(self):
        super().setUp()
        # Create an InventoryType and Project.
        in_type = self._create_inventory_type()
        self.project = self._create_project(in_type, members=[self.user])
        # Create regions
        country = self._create_country()
        currency = self._create_currency(country, "US Dollar", "USD", 840, 2)
        supplier = self._create_supplier(self.project)
        # Create Invoice
        self.invoice = self._create_invoice(
            self.project, currency, supplier, "TEST01234567")
        self.inv_uri = reverse('invoice-detail',
                               kwargs={'public_id': self.invoice.public_id})
        # Create a ColumnCollection
        kwargs = {}
        kwargs['name'] = "Test Collection"
        kwargs['related_model'] = 'item'
        kwargs['creator'] = self.user
        kwargs['updater'] = self.user
        self.collection = ColumnCollection(**kwargs)
        self.collection.save()

    def test_GET_invoice_item_list_with_invalid_permissions(self):
        """
        Test the invoice_item_list endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        item_number = "TEST123456"
        invoice_item = self._create_invoice_item(
            self.invoice, item_number, 5, '1.50')
        uri = reverse('invoice-item-list')
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_GET_invoice_item_list_with_valid_permissions(self):
        """
        Test the invoice_item_list endpoint with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        item_number = "TEST123456"
        invoice_item = self._create_invoice_item(
            self.invoice, item_number, 5, '1.50')
        uri = reverse('invoice-item-list')
        self._test_users_with_valid_permissions(uri, method,
                                                default_user=False)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_POST_invoice_item_list_with_invalid_permissions(self):
        """
        Test that a POST to invoice_item_list fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'post'
        uri = reverse('invoice-item-list')
        data = {}
        su = data.setdefault('SU', {})
        su['item_number'] = 'TEST123456'
        su['quantity'] = 5
        su['unit_price'] = '1.50'
        su['invoice'] = self.inv_uri
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            uri, method, request_data=data)
        data.setdefault('POW', su.copy())
        data.setdefault('PMA', su.copy())
        data.setdefault('PDU', su.copy())
        self._test_project_users_with_invalid_permissions(
            uri, method, request_data=data)

    def test_POST_invoice_item_list_with_valid_permissions(self):
        """
        Test that a POST to invoice_item_list passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'post'
        uri = reverse('invoice-item-list')
        data = {}
        su = data.setdefault('SU', {})
        su['item_number'] = 'TEST123456'
        su['quantity'] = 5
        su['unit_price'] = '1.50'
        su['invoice'] = self.inv_uri
        ad = data.setdefault('AD', su.copy())
        ad['item_number'] = 'TEST234561'
        du = data.setdefault('DU', su.copy())
        du['item_number'] = 'TEST345612'
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)
        pow = data.setdefault('POW', su.copy())
        pow['item_number'] = 'TEST456123'
        pma = data.setdefault('PMA', su.copy())
        pma['item_number'] = 'TEST561234'
        pdu = data.setdefault('PDU', su.copy())
        pdu['item_number'] = 'TEST612345'
        self._test_project_users_with_valid_permissions(
            uri, method, project_user=False, request_data=data)

    def test_OPTIONS_invoice_item_list_with_invalid_permissions(self):
        """
        Test that the method OPTIONS fails with invald permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'options'
        uri = reverse('invoice-item-list')
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_OPTIONS_invoice_item_list_with_valid_permissions(self):
        """
        Test that the method OPTIONS brings back the correct data.
        """
        method = 'options'
        uri = reverse('invoice-item-list')
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_GET_invoice_item_detail_with_invalid_permissions(self):
        """
        Test that a GET on the invoice_item_detail fails with invalid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        item_number = "TEST12345"
        invoice_item = self._create_invoice_item(
            self.invoice, item_number, 5, '1.50')
        uri = reverse('invoice-item-detail',
                      kwargs={'public_id': invoice_item.public_id})
        method = 'get'
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_GET_invoice_item_detail_with_valid_permissions(self):
        """
        Test that a GET to invoice_item_detail passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        item_number = "TEST12345"
        invoice_item = self._create_invoice_item(
            self.invoice, item_number, 5, '1.50')
        uri = reverse('invoice-item-detail',
                      kwargs={'public_id': invoice_item.public_id})
        method = 'get'
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_PUT_invoice_item_detail_with_invalid_permissions(self):
        """
        Test that a PUT to invoice_item_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        item_number = "TEST12345"
        invoice_item = self._create_invoice_item(
            self.invoice, item_number, 5, '1.50')
        uri = reverse('invoice-item-detail',
                      kwargs={'public_id': invoice_item.public_id})
        method = 'put'
        data = {}
        su = data.setdefault('SU', {})
        su['item_number'] = 'TEST12345'
        su['quantity'] = 5
        su['unit_price'] = '1.50'
        su['invoice'] = self.inv_uri
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            uri, method, request_data=data)
        data.setdefault('POW', su.copy())
        data.setdefault('PMA', su.copy())
        data.setdefault('PDU', su.copy())
        self._test_project_users_with_invalid_permissions(
            uri, method, request_data=data)

    def test_PUT_invoice_item_detail_with_valid_permissions(self):
        """
        Test that a PUT to invoice_item_detail passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        item_number = "TEST1234567"
        invoice_item = self._create_invoice_item(
            self.invoice, item_number, 5, '1.50')
        uri = reverse('invoice-item-detail',
                      kwargs={'public_id': invoice_item.public_id})
        method = 'put'
        data = {}
        su = data.setdefault('SU', {})
        su['item_number'] = 'TEST2345671'
        su['quantity'] = 5
        su['unit_price'] = '1.50'
        su['invoice'] = self.inv_uri
        ad = data.setdefault('AD', su.copy())
        ad['item_number'] = 'TEST3456712'
        du = data.setdefault('DU', su.copy())
        du['item_number'] = 'TEST4567123'
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)
        pow = data.setdefault('POW', su.copy())
        pow['item_number'] = 'TEST5671234'
        pma = data.setdefault('PMA', su.copy())
        pma['item_number'] = 'TEST6712345'
        pdu = data.setdefault('PDU', su.copy())
        pdu['item_number'] = 'TEST7123456'
        self._test_project_users_with_valid_permissions(
            uri, method, project_user=False, request_data=data)

    def test_PATCH_invoice_item_detail_with_invalid_permissions(self):
        """
        Test that a PATCH to invoice_item_detail fails with invalid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        item_number = "TEST1234567"
        invoice_item = self._create_invoice_item(
            self.invoice, item_number, 5, '1.50')
        uri = reverse('invoice-item-detail',
                      kwargs={'public_id': invoice_item.public_id})
        method = 'patch'
        data = {}
        su = data.setdefault('SU', {})
        su['item_number'] = 'TEST2345671'
        su['quantity'] = 5
        su['unit_price'] = '1.50'
        su['invoice'] = self.inv_uri
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            uri, method, request_data=data)
        data.setdefault('POW', su.copy())
        data.setdefault('PMA', su.copy())
        data.setdefault('PDU', su.copy())
        self._test_project_users_with_invalid_permissions(
            uri, method, request_data=data)

    def test_PATCH_invoice_item_detail_with_valid_permissions(self):
        """
        Test that a PATCH to invoice_item_detail passes with valid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        item_number = "TEST1234567"
        invoice_item = self._create_invoice_item(
            self.invoice, item_number, 5, '1.50')
        uri = reverse('invoice-item-detail',
                      kwargs={'public_id': invoice_item.public_id})
        method = 'patch'
        data = {}
        su = data.setdefault('SU', {})
        su['item_number'] = 'TEST2345671'
        ad = data.setdefault('AD', {})
        ad['item_number'] = 'TEST3456712'
        du = data.setdefault('DU', {})
        du['item_number'] = 'TEST4567123'
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)
        pow = data.setdefault('POW', {})
        pow['item_number'] = 'TEST5671234'
        pma = data.setdefault('PMA', {})
        pma['item_number'] = 'TEST6712345'
        pdu = data.setdefault('PDU', {})
        pdu['item_number'] = 'TEST7123456'
        self._test_project_users_with_valid_permissions(
            uri, method, project_user=False, request_data=data)

    def test_DELETE_invoice_item_detail_with_invalid_permissions(self):
        """
        Test that a DELETE to invoice_item_detail fails with invalid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        item_number = "TEST1234567"
        method = 'delete'
        invoice_item = self._create_invoice_item(
            self.invoice, item_number, 5, '1.50')
        uri = reverse('invoice-item-detail',
                      kwargs={'public_id': invoice_item.public_id})
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_DELETE_invoice_item_detail_with_valid_permissions(self):
        """
        Test that a DELETE to invoice_item_detail pass' with valid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        item_number = "TEST1234567"
        method = 'delete'
        # Test SUPERUSER
        invoice_item = self._create_invoice_item(
            self.invoice, item_number, 5, '1.50')
        uri = reverse('invoice-item-detail',
                      kwargs={'public_id': invoice_item.public_id})
        self._test_superuser_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test ADMINISTRATOR
        invoice_item = self._create_invoice_item(
            self.invoice, item_number, 5, '1.50')
        uri = reverse('invoice-item-detail',
                      kwargs={'public_id': invoice_item.public_id})
        self._test_administrator_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test DEFAULT_USER
        ## This is an invalid test since the DEFAULT_USER has no access.
        # Test PROJECT_OWNER
        invoice_item = self._create_invoice_item(
            self.invoice, item_number, 5, '1.50')
        uri = reverse('invoice-item-detail',
                      kwargs={'public_id': invoice_item.public_id})
        self._test_project_owner_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test PROJECT_MANAGER
        invoice_item = self._create_invoice_item(
            self.invoice, item_number, 5, '1.50')
        uri = reverse('invoice-item-detail',
                      kwargs={'public_id': invoice_item.public_id})
        self._test_project_manager_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test PROJECT_USER
        ## This is an invalid test since the PROJECT_USER has no access.

    def test_OPTIONS_invoice_item_detail_with_invalid_permissions(self):
        """
        Test that the method OPTIONS fails with invald permissions.
        """
        #self.skipTest("Temporarily skipped")
        item_number = "TEST1234567"
        method = 'options'
        invoice_item = self._create_invoice_item(
            self.invoice, item_number, 5, '1.50')
        uri = reverse('invoice-item-detail',
                      kwargs={'public_id': invoice_item.public_id})
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_OPTIONS_invoice_item_detail_with_valid_permissions(self):
        """
        Test that the method OPTIONS brings back the correct data.
        """
        #self.skipTest("Temporarily skipped")
        item_number = "TEST1234567"
        method = 'options'
        invoice_item = self._create_invoice_item(
            self.invoice, item_number, 5, '1.50')
        uri = reverse('invoice-item-detail',
                      kwargs={'public_id': invoice_item.public_id})
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)
