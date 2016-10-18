# -*- coding: utf-8 -*-
#
# inventory/suppliers/api/tests/test_suppliers_api.py
#

from rest_framework.reverse import reverse
from rest_framework import status

from inventory.common.api.tests.base_test import BaseTest
from inventory.regions.models import Country, Subdivision
from inventory.suppliers.models import Supplier


class TestSupplierAPI(BaseTest):

    def __init__(self, name):
        super(TestSupplierAPI, self).__init__(name)

    def setUp(self):
        super(TestSupplierAPI, self).setUp()
        self.in_type = self._create_inventory_type()
        self.project = self._create_project(self.in_type, members=[self.user])
        kwargs = {'public_id': self.project.public_id}
        self.project_uri = self._resolve('project-detail', **kwargs)
        #self.country = self._create_country()
        #self.subdivision = self._create_subdivision(country)

    def test_GET_supplier_list_with_invalid_permissions(self):
        """
        Test the supplier_list endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        supplier = self._create_supplier(self.project)
        uri = reverse('supplier-list')
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_GET_supplier_list_with_valid_permissions(self):
        """
        Test the supplier_list endpoint with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        supplier = self._create_supplier(self.project)
        uri = reverse('supplier-list')
        self._test_users_with_valid_permissions(uri, method, default_user=False)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_POST_supplier_list_with_invalid_permissions(self):
        """
        Test that a POST to supplier_list fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'post'
        uri = reverse('supplier-list')
        data = {}
        su = data.setdefault('SU', {})
        su['name'] = 'TestSupplier-01'
        su['project'] = self.project_uri
        su['stype'] = Supplier.BOTH_MFG_DIS
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            uri, method, request_data=data)
        data.setdefault('POW', su.copy())
        data.setdefault('PMA', su.copy())
        data.setdefault('PDU', su.copy())
        self._test_project_users_with_invalid_permissions(
            uri, method, request_data=data)

    def test_POST_supplier_list_with_valid_permissions(self):
        """
        Test that a POST to supplier_list passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'post'
        uri = reverse('supplier-list')
        data = {}
        su = data.setdefault('SU', {})
        su['name'] = 'TestSupplier-01'
        su['project'] = self.project_uri
        su['stype'] = Supplier.BOTH_MFG_DIS
        ad = data.setdefault('AD', su.copy())
        ad['name'] = 'TestSupplier-02'
        du = data.setdefault('DU', su.copy())
        du['name'] = 'TestSupplier-03'
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)
        pow = data.setdefault('POW', su.copy())
        pow['name'] = 'TestSupplier-04'
        pma = data.setdefault('PMA', su.copy())
        pma['name'] = 'TestSupplier-05'
        pdu = data.setdefault('PDU', su.copy())
        pdu['name'] = 'TestSupplier-06'
        self._test_project_users_with_valid_permissions(
            uri, method, project_user=False, request_data=data)

    def test_OPTIONS_supplier_list_with_invalid_permissions(self):
        """
        Test that the method OPTIONS fails with invald permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'options'
        uri = reverse('supplier-list')
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_OPTIONS_supplier_list_with_valid_permissions(self):
        """
        Test that the method OPTIONS brings back the correct data.
        """
        method = 'options'
        uri = reverse('supplier-list')
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_GET_supplier_detail_with_invalid_permissions(self):
        """
        Test that a GET on the supplier_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        supplier = self._create_supplier(self.project)
        uri = reverse('supplier-detail',
                      kwargs={'public_id': supplier.public_id})
        method = 'get'
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_GET_supplier_detail_with_valid_permissions(self):
        """
        Test that a GET to supplier_detail passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        supplier = self._create_supplier(self.project)
        uri = reverse('supplier-detail',
                      kwargs={'public_id': supplier.public_id})
        method = 'get'
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_PUT_supplier_detail_with_invalid_permissions(self):
        """
        Test that a PUT to supplier_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        supplier = self._create_supplier(self.project)
        uri = reverse('supplier-detail',
                      kwargs={'public_id': supplier.public_id})
        method = 'put'
        data = {}
        su = data.setdefault('SU', {})
        su['name'] = 'TestSupplier-01'
        su['project'] = self.project_uri
        su['stype'] = Supplier.BOTH_MFG_DIS
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            uri, method, request_data=data)
        data.setdefault('POW', su.copy())
        data.setdefault('PMA', su.copy())
        data.setdefault('PDU', su.copy())
        self._test_project_users_with_invalid_permissions(
            uri, method, request_data=data)

    def test_PUT_supplier_detail_with_valid_permissions(self):
        """
        Test that a PUT to supplier_detail passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        supplier = self._create_supplier(self.project)
        uri = reverse('supplier-detail',
                      kwargs={'public_id': supplier.public_id})
        method = 'put'
        data = {}
        su = data.setdefault('SU', {})
        su['name'] = 'TestSupplier-01'
        su['project'] = self.project_uri
        su['stype'] = Supplier.BOTH_MFG_DIS
        ad = data.setdefault('AD', su.copy())
        ad['name'] = 'TestSupplier-02'
        du = data.setdefault('DU', su.copy())
        du['name'] = 'TestSupplier-03'
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)
        pow = data.setdefault('POW', su.copy())
        pow['name'] = 'TestSupplier-04'
        pma = data.setdefault('PMA', su.copy())
        pma['name'] = 'TestSupplier-05'
        pdu = data.setdefault('PDU', su.copy())
        pdu['name'] = 'TestSupplier-06'
        self._test_project_users_with_valid_permissions(
            uri, method, project_user=False, request_data=data)

    def test_PATCH_supplier_detail_with_invalid_permissions(self):
        """
        Test that a PATCH to supplier_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        supplier = self._create_supplier(self.project)
        uri = reverse('supplier-detail',
                      kwargs={'public_id': supplier.public_id})
        method = 'patch'
        data = {}
        su = data.setdefault('SU', {})
        su['name'] = 'TestSupplier-01'
        su['project'] = self.project_uri
        su['stype'] = Supplier.BOTH_MFG_DIS
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            uri, method, request_data=data)
        data.setdefault('POW', su.copy())
        data.setdefault('PMA', su.copy())
        data.setdefault('PDU', su.copy())
        self._test_project_users_with_invalid_permissions(
            uri, method, request_data=data)

    def test_PATCH_supplier_detail_with_valid_permissions(self):
        """
        Test that a PATCH to supplier_detail passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        supplier = self._create_supplier(self.project)
        uri = reverse('supplier-detail',
                      kwargs={'public_id': supplier.public_id})
        method = 'patch'
        data = {}
        su = data.setdefault('SU', {})
        su['name'] = 'TestSupplier-01'
        su['project'] = self.project_uri
        su['stype'] = Supplier.BOTH_MFG_DIS
        ad = data.setdefault('AD', {})
        ad['name'] = 'TestSupplier-02'
        du = data.setdefault('DU', {})
        du['name'] = 'TestSupplier-03'
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)
        pow = data.setdefault('POW', {})
        pow['name'] = 'TestSupplier-04'
        pma = data.setdefault('PMA', {})
        pma['name'] = 'TestSupplier-05'
        pdu = data.setdefault('PDU', {})
        pdu['name'] = 'TestSupplier-06'
        self._test_project_users_with_valid_permissions(
            uri, method, project_user=False, request_data=data)

    def test_DELETE_supplier_detail_with_invalid_permissions(self):
        """
        Test that a DELETE to supplier_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'delete'
        supplier = self._create_supplier(self.project)
        uri = reverse('supplier-detail',
                      kwargs={'public_id': supplier.public_id})
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_DELETE_supplier_detail_with_valid_permissions(self):
        """
        Test that a DELETE to supplier_detail pass' with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'delete'
        # Test SUPERUSER
        supplier = self._create_supplier(self.project)
        uri = reverse('supplier-detail',
                      kwargs={'public_id': supplier.public_id})
        self._test_superuser_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test ADMINISTRATOR
        supplier = self._create_supplier(self.project)
        uri = reverse('supplier-detail',
                      kwargs={'public_id': supplier.public_id})
        self._test_administrator_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test DEFAULT_USER
        ## This is an invalid test since the DEFAULT_USER has no access.
        # Test PROJECT_OWNER
        supplier = self._create_supplier(self.project)
        uri = reverse('supplier-detail',
                      kwargs={'public_id': supplier.public_id})
        self._test_project_owner_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test PROJECT_MANAGER
        supplier = self._create_supplier(self.project)
        uri = reverse('supplier-detail',
                      kwargs={'public_id': supplier.public_id})
        self._test_project_manager_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test PROJECT_USER
        ## This is an invalid test since the PROJECT_USER has no access.

    def test_OPTIONS_supplier_detail_with_invalid_permissions(self):
        """
        Test that the method OPTIONS fails with invald permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'options'
        supplier = self._create_supplier(self.project)
        uri = reverse('supplier-detail',
                      kwargs={'public_id': supplier.public_id})
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_OPTIONS_supplier_detail_with_valid_permissions(self):
        """
        Test that the method OPTIONS brings back the correct data.
        """
        method = 'options'
        supplier = self._create_supplier(self.project)
        uri = reverse('supplier-detail',
                      kwargs={'public_id': supplier.public_id})
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)
