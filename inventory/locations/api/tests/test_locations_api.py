# -*- coding: utf-8 -*-
#
# inventory/locations/api/tests/test_locations_api.py
#

import random

from django.contrib.auth import get_user_model

from rest_framework.reverse import reverse
from rest_framework import status

from inventory.common.api.tests.base_test import BaseTest
from inventory.locations.models import (
    LocationSetName, LocationFormat, LocationCode)

UserModel = get_user_model()


class TestLocationSetNameAPI(BaseTest):

    def __init__(self, name):
        super(TestLocationSetNameAPI, self).__init__(name)

    def setUp(self):
        super(TestLocationSetNameAPI, self).setUp()
        # Create an InventoryType and Project.
        self.in_type = self._create_inventory_type()
        self.project = self._create_project(self.in_type, members=[self.user])
        kwargs = {'public_id': self.project.public_id}
        self.project_uri = self._resolve('project-detail', **kwargs)

    def test_GET_location_set_name_list_with_invalid_permissions(self):
        """
        Test the location_set_name_list endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        location_set_name = self._create_location_set_name(self.project)
        uri = reverse('location-set-name-list')
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_GET_location_set_name_list_with_valid_permissions(self):
        """
        Test the location_set_name_list endpoint with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        location_set_name = self._create_location_set_name(self.project)
        uri = reverse('location-set-name-list')
        self._test_users_with_valid_permissions(uri, method, default_user=False)
        self._test_project_users_with_valid_permissions(uri, method)


    def test_POST_location_set_name_list_with_invalid_permissions(self):
        """
        Test that a POST to location_set_name_list fails with invalid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'post'
        uri = reverse('location-set-name-list')
        data = {}
        su = data.setdefault('SU', {})
        su['name'] = 'Test Location Set Name 01'
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

    def test_POST_location_set_name_list_with_valid_permissions(self):
        """
        Test that a POST to location_set_name_list passes with valid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'post'
        uri = reverse('location-set-name-list')
        data = {}
        su = data.setdefault('SU', {})
        su['name'] = 'Test Location Set Name 01'
        su['project'] = self.project_uri
        ad = data.setdefault('AD', su.copy())
        ad['name'] = 'Test Location Set Name 02'
        du = data.setdefault('DU', su.copy())
        du['name'] = 'Test Location Set Name 03'
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)
        pow = data.setdefault('POW', su.copy())
        pow['name'] = 'Test Location Set Name 04'
        pma = data.setdefault('PMA', su.copy())
        pma['name'] = 'Test Location Set Name 05'
        pdu = data.setdefault('PDU', su.copy())
        pdu['name'] = 'Test Location Set Name 06'
        self._test_project_users_with_valid_permissions(
            uri, method, project_user=False, request_data=data)

    def test_OPTIONS_location_set_name_list_with_invalid_permissions(self):
        """
        Test that the method OPTIONS fails with invald permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'options'
        uri = reverse('location-set-name-list')
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_OPTIONS_location_set_name_list_with_valid_permissions(self):
        """
        Test that the method OPTIONS brings back the correct data.
        """
        method = 'options'
        uri = reverse('location-set-name-list')
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_GET_location_set_name_detail_with_invalid_permissions(self):
        """
        Test that a GET on the location_set_name_detail fails with invalid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        location_set_name = self._create_location_set_name(self.project)
        uri = reverse('location-set-name-detail',
                      kwargs={'public_id': location_set_name.public_id})
        method = 'get'
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_GET_location_set_name_detail_with_valid_permissions(self):
        """
        Test that a GET to location_set_name_detail passes with valid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        location_set_name = self._create_location_set_name(self.project)
        uri = reverse('location-set-name-detail',
                      kwargs={'public_id': location_set_name.public_id})
        method = 'get'
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_PUT_location_set_name_detail_with_invalid_permissions(self):
        """
        Test that a PUT to location_set_name_detail fails with invalid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        location_set_name = self._create_location_set_name(self.project)
        uri = reverse('location-set-name-detail',
                      kwargs={'public_id': location_set_name.public_id})
        method = 'put'
        data = {}
        su = data.setdefault('SU', {})
        su['name'] = 'Test Location Set Name 01'
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

    def test_PUT_location_set_name_detail_with_valid_permissions(self):
        """
        Test that a PUT to location_set_name_detail passes with valid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        location_set_name = self._create_location_set_name(self.project)
        uri = reverse('location-set-name-detail',
                      kwargs={'public_id': location_set_name.public_id})
        method = 'put'
        data = {}
        su = data.setdefault('SU', {})
        su['name'] = 'Test Location Set Name 01'
        su['project'] = self.project_uri
        ad = data.setdefault('AD', su.copy())
        ad['name'] = 'Test Location Set Name 02'
        du = data.setdefault('DU', su.copy())
        du['name'] = 'Test Location Set Name 03'
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)
        pow = data.setdefault('POW', su.copy())
        pow['name'] = 'Test Location Set Name 04'
        pma = data.setdefault('PMA', su.copy())
        pma['name'] = 'Test Location Set Name 05'
        pdu = data.setdefault('PDU', su.copy())
        pdu['name'] = 'Test Location Set Name 06'
        self._test_project_users_with_valid_permissions(
            uri, method, project_user=False, request_data=data)

    def test_PATCH_location_set_name_detail_with_invalid_permissions(self):
        """
        Test that a PATCH to location_set_name_detail fails with invalid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        location_set_name = self._create_location_set_name(self.project)
        uri = reverse('location-set-name-detail',
                      kwargs={'public_id': location_set_name.public_id})
        method = 'patch'
        data = {}
        su = data.setdefault('SU', {})
        su['name'] = 'Test Location Set Name 01'
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

    def test_PATCH_location_set_name_detail_with_valid_permissions(self):
        """
        Test that a PATCH to location_set_name_detail passes with valid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        location_set_name = self._create_location_set_name(self.project)
        uri = reverse('location-set-name-detail',
                      kwargs={'public_id': location_set_name.public_id})
        method = 'patch'
        data = {}
        su = data.setdefault('SU', {})
        su['name'] = 'Test Location Set Name 01'
        su['project'] = self.project_uri
        ad = data.setdefault('AD', {})
        ad['name'] = 'Test Location Set Name 02'
        du = data.setdefault('DU', {})
        du['name'] = 'Test Location Set Name 03'
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)
        pow = data.setdefault('POW', {})
        pow['name'] = 'Test Location Set Name 04'
        pma = data.setdefault('PMA', {})
        pma['name'] = 'Test Location Set Name 05'
        pdu = data.setdefault('PDU', {})
        pdu['name'] = 'Test Location Set Name 06'
        self._test_project_users_with_valid_permissions(
            uri, method, project_user=False, request_data=data)

    def test_DELETE_location_set_name_detail_with_invalid_permissions(self):
        """
        Test that a DELETE to location_set_name_detail fails with invalid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'delete'
        location_set_name = self._create_location_set_name(self.project)
        uri = reverse('location-set-name-detail',
                      kwargs={'public_id': location_set_name.public_id})
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_DELETE_location_set_name_detail_with_valid_permissions(self):
        """
        Test that a DELETE to location_set_name_detail pass' with valid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'delete'
        # Test SUPERUSER
        location_set_name = self._create_location_set_name(self.project)
        uri = reverse('location-set-name-detail',
                      kwargs={'public_id': location_set_name.public_id})
        self._test_superuser_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test ADMINISTRATOR
        location_set_name = self._create_location_set_name(self.project)
        uri = reverse('location-set-name-detail',
                      kwargs={'public_id': location_set_name.public_id})
        self._test_administrator_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test SET_NAME_USER
        ## This is an invalid test since the SET_NAME_USER has no access.
        # Test PROJECT_OWNER
        location_set_name = self._create_location_set_name(self.project)
        uri = reverse('location-set-name-detail',
                      kwargs={'public_id': location_set_name.public_id})
        self._test_project_owner_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test PROJECT_MANAGER
        location_set_name = self._create_location_set_name(self.project)
        uri = reverse('location-set-name-detail',
                      kwargs={'public_id': location_set_name.public_id})
        self._test_project_manager_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test PROJECT_USER
        ## This is an invalid test since the PROJECT_USER has no access.

    def test_OPTIONS_location_set_name_detail_with_invalid_permissions(self):
        """
        Test that the method OPTIONS fails with invald permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'options'
        location_set_name = self._create_location_set_name(self.project)
        uri = reverse('location-set-name-detail',
                      kwargs={'public_id': location_set_name.public_id})
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_OPTIONS_location_set_name_detail_with_valid_permissions(self):
        """
        Test that the method OPTIONS brings back the correct data.
        """
        method = 'options'
        location_set_name = self._create_location_set_name(self.project)
        uri = reverse('location-set-name-detail',
                      kwargs={'public_id': location_set_name.public_id})
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_POST_length_of_separator(self):
        """
        Test that the length of the separator is not longer than the defined
        length of the database column.
        """
        #self.skipTest("Temporarily skipped")
        method = 'post'
        uri = reverse('location-set-name-list')
        data = {}
        data['name'] = 'Test Location Set Name 01'
        data['project'] = self.project_uri
        data['separator'] = '--->'
        response = self.client.post(uri, data=data, format='json')
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        self.assertTrue(self._has_error(response, error_key='separator'), msg)
        self._test_errors(response, tests={
            'separator': "Ensure this field has no more than 3 characters.",
            })
 

class TestLocationFormatAPI(BaseTest):

    def __init__(self, name):
        super(TestLocationFormatAPI, self).__init__(name)

    def setUp(self):
        super(TestLocationFormatAPI, self).setUp()
        # Create an InventoryType, Project, and LocationSetName.
        self.in_type = self._create_inventory_type()
        self.project = self._create_project(self.in_type, members=[self.user])
        self.location_set_name = self._create_location_set_name(self.project)
        kwargs = {'public_id': self.location_set_name.public_id}
        self.location_set_name_uri = self._resolve('location-set-name-detail',
                                                   **kwargs)

    def test_GET_location_format_list_with_invalid_permissions(self):
        """
        Test the location_format_list endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        location_format = self._create_location_format(
            self.location_set_name, "T\d\d")
        uri = reverse('location-format-list')
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_GET_location_format_list_with_valid_permissions(self):
        """
        Test the location_format_list endpoint with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        location_format = self._create_location_format(
            self.location_set_name, "T\d\d")
        uri = reverse('location-format-list')
        self._test_users_with_valid_permissions(uri, method, default_user=False)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_POST_location_format_list_with_invalid_permissions(self):
        """
        Test that a POST to location_format_list fails with invalid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'post'
        uri = reverse('location-format-list')
        data = {}
        su = data.setdefault('SU', {})
        su['char_definition'] = 'T\d\d'
        su['location_set_name'] = self.location_set_name_uri
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            uri, method, request_data=data)
        data.setdefault('POW', su.copy())
        data.setdefault('PMA', su.copy())
        data.setdefault('PDU', su.copy())
        self._test_project_users_with_invalid_permissions(
            uri, method, request_data=data)

    def test_POST_location_format_list_with_valid_permissions(self):
        """
        Test that a POST to location_format_list passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'post'
        uri = reverse('location-format-list')
        data = {}
        su = data.setdefault('SU', {})
        su['char_definition'] = 'A\d\d'
        su['location_set_name'] = self.location_set_name_uri
        ad = data.setdefault('AD', su.copy())
        ad['char_definition'] = 'B\d\d'
        du = data.setdefault('DU', su.copy())
        du['char_definition'] = 'C\d\d'
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)
        pow = data.setdefault('POW', su.copy())
        pow['char_definition'] = 'D\d\d'
        pma = data.setdefault('PMA', su.copy())
        pma['char_definition'] = 'E\d\d'
        pdu = data.setdefault('PDU', su.copy())
        pdu['char_definition'] = 'F\d\d'
        self._test_project_users_with_valid_permissions(
            uri, method, project_user=False, request_data=data)

    def test_OPTIONS_location_format_list_with_invalid_permissions(self):
        """
        Test that the method OPTIONS fails with invald permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'options'
        uri = reverse('location-format-list')
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_OPTIONS_location_format_list_with_valid_permissions(self):
        """
        Test that the method OPTIONS brings back the correct data.
        """
        method = 'options'
        uri = reverse('location-format-list')
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_GET_location_format_detail_with_invalid_permissions(self):
        """
        Test that a GET on the location_format_detail fails with invalid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        location_format = self._create_location_format(
            self.location_set_name, "A\d\d")
        uri = reverse('location-format-detail',
                      kwargs={'public_id': location_format.public_id})
        method = 'get'
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_GET_location_format_detail_with_valid_permissions(self):
        """
        Test that a GET to location_format_detail passes with valid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        location_format = self._create_location_format(
            self.location_set_name, "A\d\d")
        uri = reverse('location-format-detail',
                      kwargs={'public_id': location_format.public_id})
        method = 'get'
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_PUT_location_format_detail_with_invalid_permissions(self):
        """
        Test that a PUT to location_format_detail fails with invalid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        location_format = self._create_location_format(
            self.location_set_name, "A\d\d")
        uri = reverse('location-format-detail',
                      kwargs={'public_id': location_format.public_id})
        method = 'put'
        data = {}
        su = data.setdefault('SU', {})
        su['char_definition'] = 'A\d\d'
        su['location_set_name'] = self.location_set_name_uri
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            uri, method, request_data=data)
        data.setdefault('POW', su.copy())
        data.setdefault('PMA', su.copy())
        data.setdefault('PDU', su.copy())
        self._test_project_users_with_invalid_permissions(
            uri, method, request_data=data)

    def test_PUT_location_format_detail_with_valid_permissions(self):
        """
        Test that a PUT to location_format_detail passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        location_format = self._create_location_format(
            self.location_set_name, "A\d\d")
        uri = reverse('location-format-detail',
                      kwargs={'public_id': location_format.public_id})
        method = 'put'
        data = {}
        su = data.setdefault('SU', {})
        su['char_definition'] = 'A\d\d'
        su['location_set_name'] = self.location_set_name_uri
        ad = data.setdefault('AD', su.copy())
        ad['char_definition'] = 'B\d\d'
        ad['location_set_name'] = self.location_set_name_uri
        du = data.setdefault('DU', su.copy())
        du['char_definition'] = 'C\d\d'
        du['location_set_name'] = self.location_set_name_uri
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)
        pow = data.setdefault('POW', su.copy())
        pow['char_definition'] = 'D\d\d'
        pow['location_set_name'] = self.location_set_name_uri
        pma = data.setdefault('PMA', su.copy())
        pma['char_definition'] = 'E\d\d'
        pma['location_set_name'] = self.location_set_name_uri
        pdu = data.setdefault('PDU', su.copy())
        pdu['char_definition'] = 'F\d\d'
        pdu['location_set_name'] = self.location_set_name_uri
        self._test_project_users_with_valid_permissions(
            uri, method, project_user=False, request_data=data)

    def test_PATCH_location_format_detail_with_invalid_permissions(self):
        """
        Test that a PATCH to location_format_detail fails with invalid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        location_format = self._create_location_format(
            self.location_set_name, "A\d\d")
        uri = reverse('location-format-detail',
                      kwargs={'public_id': location_format.public_id})
        method = 'patch'
        data = {}
        su = data.setdefault('SU', {})
        su['char_definition'] = 'B\d\d'
        su['location_set_name'] = self.location_set_name_uri
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            uri, method, request_data=data)
        data.setdefault('POW', su.copy())
        data.setdefault('PMA', su.copy())
        data.setdefault('PDU', su.copy())
        self._test_project_users_with_invalid_permissions(
            uri, method, request_data=data)

    def test_PATCH_location_format_detail_with_valid_permissions(self):
        """
        Test that a PATCH to location_format_detail passes with valid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        location_format = self._create_location_format(
            self.location_set_name, "A\d\d")
        uri = reverse('location-format-detail',
                      kwargs={'public_id': location_format.public_id})
        method = 'patch'
        data = {}
        su = data.setdefault('SU', {})
        su['char_definition'] = 'B\d\d'
        su['location_set_name'] = self.location_set_name_uri
        ad = data.setdefault('AD', {})
        ad['char_definition'] = 'C\d\d'
        du = data.setdefault('DU', {})
        du['char_definition'] = 'D\d\d'
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)
        pow = data.setdefault('POW', {})
        pow['char_definition'] = 'E\d\d'
        pma = data.setdefault('PMA', {})
        pma['char_definition'] = 'F\d\d'
        pdu = data.setdefault('PDU', {})
        pdu['char_definition'] = 'G\d\d'
        self._test_project_users_with_valid_permissions(
            uri, method, project_user=False, request_data=data)

    def test_DELETE_location_format_detail_with_invalid_permissions(self):
        """
        Test that a DELETE to location_format_detail fails with invalid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'delete'
        location_format = self._create_location_format(
            self.location_set_name, "A\d\d")
        uri = reverse('location-format-detail',
                      kwargs={'public_id': location_format.public_id})
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_DELETE_location_format_detail_with_valid_permissions(self):
        """
        Test that a DELETE to location_format_detail pass' with valid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'delete'
        # Test SUPERUSER
        location_format = self._create_location_format(
            self.location_set_name, "A\d\d")
        uri = reverse('location-format-detail',
                      kwargs={'public_id': location_format.public_id})
        self._test_superuser_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test ADMINISTRATOR
        location_format = self._create_location_format(
            self.location_set_name, "B\d\d")
        uri = reverse('location-format-detail',
                      kwargs={'public_id': location_format.public_id})
        self._test_administrator_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test DEFAULT_USER
        ## This is an invalid test since the DEFAULT_USER has no access.
        # Test PROJECT_OWNER
        location_format = self._create_location_format(
            self.location_set_name, "C\d\d")
        uri = reverse('location-format-detail',
                      kwargs={'public_id': location_format.public_id})
        self._test_project_owner_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test PROJECT_MANAGER
        location_format = self._create_location_format(
            self.location_set_name, "D\d\d")
        uri = reverse('location-format-detail',
                      kwargs={'public_id': location_format.public_id})
        self._test_project_manager_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test PROJECT_USER
        ## This is an invalid test since the PROJECT_USER has no access.

    def test_OPTIONS_location_format_detail_with_invalid_permissions(self):
        """
        Test that the method OPTIONS fails with invald permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'options'
        location_format = self._create_location_format(
            self.location_set_name, "A\d\d")
        uri = reverse('location-format-detail',
                      kwargs={'public_id': location_format.public_id})
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_OPTIONS_location_format_detail_with_valid_permissions(self):
        """
        Test that the method OPTIONS brings back the correct data.
        """
        method = 'options'
        location_format = self._create_location_format(
            self.location_set_name, "A\d\d")
        uri = reverse('location-format-detail',
                      kwargs={'public_id': location_format.public_id})
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_delimitor_in_char_definition(self):
        """
        Test that the delimitor is not in the character definition.
        """
        #self.skipTest("Temporarily skipped")
        # Test delimitor in char_definition.
        data = {}
        data['location_set_name'] = self.location_set_name_uri
        data['char_definition'] = 'T{}\d\d'.format(
            self.location_set_name.separator)
        data['segment_order'] = 0
        data['description'] = "Test POST"
        uri = reverse('location-format-list')
        response = self.client.post(uri, data=data, format='json')
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        self.assertTrue(self._has_error(response, 'char_definition'), msg)
        self._test_errors(response, tests={
            'char_definition': u"Invalid format, found separator",
            })

    def test_char_definition_length_is_not_zero(self):
        """
        Test that the char_definition length is not zero.
        """
        #self.skipTest("Temporarily skipped")
        # Test that character_definition length is not zero.
        data = {}
        data['location_set_name'] = self.location_set_name_uri
        data['char_definition'] = ''
        data['segment_order'] = 0
        data['description'] = "Test POST"
        uri = reverse('location-format-list')
        response = self.client.post(uri, data=data, format='json')
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertTrue(self._has_error(response, 'char_definition'), msg)
        self._test_errors(response, tests={
            'char_definition': u"This field may not be blank.",
            })


class TestLocationCodeAPI(BaseTest):

    def __init__(self, name):
        super(TestLocationCodeAPI, self).__init__(name)

    def setUp(self):
        super(TestLocationCodeAPI, self).setUp()
        # Create an InventoryType, Project, and LocationSetName.
        self.in_type = self._create_inventory_type()
        self.project = self._create_project(self.in_type, members=[self.user])
        self.location_set_name = self._create_location_set_name(self.project)
        self.location_format = self._create_location_format(
            self.location_set_name, 'A\d\d')
        kwargs = {'public_id': self.location_format.public_id}
        self.location_format_uri = self._resolve('location-format-detail',
                                                 **kwargs)

    def test_GET_location_code_list_with_invalid_permissions(self):
        """
        Test the location_code_list endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        location_code = self._create_location_code(self.location_format, "A01")
        uri = reverse('location-code-list')
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_GET_location_code_list_with_valid_permissions(self):
        """
        Test the location_code_list endpoint with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        location_code = self._create_location_code(self.location_format, "A01")
        uri = reverse('location-code-list')
        self._test_users_with_valid_permissions(uri, method, default_user=False)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_POST_location_code_list_with_invalid_permissions(self):
        """
        Test that a POST to location_code_list fails with invalid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'post'
        uri = reverse('location-code-list')
        data = {}
        su = data.setdefault('SU', {})
        su['segment'] = 'A01'
        su['location_format'] = self.location_format_uri
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            uri, method, request_data=data)
        data.setdefault('POW', su.copy())
        data.setdefault('PMA', su.copy())
        data.setdefault('PDU', su.copy())
        self._test_project_users_with_invalid_permissions(
            uri, method, request_data=data)

    def test_POST_location_code_list_with_valid_permissions(self):
        """
        Test that a POST to location_code_list passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'post'
        uri = reverse('location-code-list')
        data = {}
        su = data.setdefault('SU', {})
        su['segment'] = 'A01'
        su['location_format'] = self.location_format_uri
        ad = data.setdefault('AD', su.copy())
        ad['segment'] = 'A01'
        du = data.setdefault('DU', su.copy())
        du['segment'] = 'A01'
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)
        pow = data.setdefault('POW', su.copy())
        pow['segment'] = 'A01'
        pma = data.setdefault('PMA', su.copy())
        pma['segment'] = 'A01'
        pdu = data.setdefault('PDU', su.copy())
        pdu['segment'] = 'A01'
        self._test_project_users_with_valid_permissions(
            uri, method, project_user=False, request_data=data)

        for lc in LocationCode.objects.all():
            print("name: {}, format: {}, parent: {}, path: {}".format(
                lc.location_format.location_set_name, lc.location_format,
                lc.parent, lc.path))

    def test_OPTIONS_location_code_list_with_invalid_permissions(self):
        """
        Test that the method OPTIONS fails with invald permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'options'
        uri = reverse('location-code-list')
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_OPTIONS_location_code_list_with_valid_permissions(self):
        """
        Test that the method OPTIONS brings back the correct data.
        """
        method = 'options'
        uri = reverse('location-code-list')
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)










    def test_create_post_location_code(self):
        """
        Test that a record can be created with a POST.
        """
        # Create LocationCode with POST.
        self.skipTest("Temporarily skipped")
        ld = self._create_location_set_name()
        lf = self._create_location_code(ld)
        lf_uri = reverse('location-format-detail', kwargs={'pk': lf.id})
        new_data = {'char_definition': lf_uri, 'segment': 'T01'}
        #, 'parent': None} This should be permitted
        uri = reverse('location-code-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Read record with GET.
        pk = data.get('id')
        uri = reverse('location-code-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('segment'), new_data.get('segment'), msg)

    def test_create_location_code_post_token_superuser(self):
        """
        Test LocationCode with API with token.
        """
        self.skipTest("Temporarily skipped")
        app_name = 'Token Test'
        data = self._make_app_token(
            self.user, app_name, self.client, client_type='public',
            grant_type='client_credentials')
        # Use API to create a LocationSet_name.
        ld = self._create_location_set_name()
        lf = self._create_location_format(ld)
        lf_uri = reverse('location-format-detail', kwargs={'pk': lf.id})
        new_data = {'char_definition': lf_uri, 'segment': 'T01'}
        #, 'parent': None} This should be permitted
        uri = reverse('location-code-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)

    def test_create_location_code_post_token_administrator(self):
        """
        Test LocationCode with API with token. We don't use the self.client
        created in the setUp method from the base class.
        """
        self.skipTest("Temporarily skipped")
        # Create a non-logged in user, but one that has a valid token.
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(
            username, password, email='test@example.com',
            role=UserModel.ADMINISTRATOR)
        app_name = 'Token Test'
        data = self._make_app_token(
            user, app_name, client, client_type='public',
            grant_type='client_credentials')
        # Use API to create a supplier.
        ld = self._create_location_set_name()
        lf = self._create_location_format(ld)
        lf_uri = reverse('location-format-detail', kwargs={'pk': lf.id})
        new_data = {'char_definition': lf_uri, 'segment': 'T01'}
        #, 'parent': None} This should be permitted
        uri = reverse('location-code-list')
        response = client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)

    def test_create_location_code_post_token_project_manager(self):
        """
        Test LocationCode with API with token. We don't use the self.client
        created in the setUp method from the base class.
        """
        self.skipTest("Temporarily skipped")
        # Create a non-logged in user, but one that has a valid token.
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(
            username, password, email='test@example.com')
        app_name = 'Token Test'
        data = self._make_app_token(
            user, app_name, client, client_type='public',
            grant_type='client_credentials')
        # Create a project for this user.
        project = self._create_project(user)
        # Get the user, to be sure we get the updated members and managers.
        user = UserModel.objects.get(pk=user.pk)
        msg = "user.role: {} sould be {}.".format(
            user.role,  UserModel.PROJECT_MANAGER)
        self.assertEqual(user.role, UserModel.PROJECT_MANAGER, msg)
        # Use API to create a supplier.
        ld = self._create_location_set_name()
        lf = self._create_location_format(ld)
        lf_uri = reverse('location-format-detail', kwargs={'pk': lf.id})
        new_data = {'char_definition': lf_uri, 'segment': 'T01'}
        #, 'parent': None} This should be permitted
        uri = reverse('location-code-list')
        response = client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)

    def test_create_location_code_post_token_set_name_user(self):
        """
        Test LocationCode with API with token. We don't use the self.client
        created in the setUp method from the base class.
        """
        self.skipTest("Temporarily skipped")
        # Create a non-logged in user, but one that has a valid token.
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(
            username, password, email='test@example.com',
            role=UserModel.SET_NAME_USER)
        app_name = 'Token Test'
        data = self._make_app_token(
            user, app_name, client, client_type='public',
            grant_type='client_credentials')
        # Use API to create a supplier.
        ld = self._create_location_set_name()
        lf = self._create_location_format(ld)
        lf_uri = reverse('location-format-detail', kwargs={'pk': lf.id})
        new_data = {'char_definition': lf_uri, 'segment': 'T01'}
        uri = reverse('location-code-list')
        response = client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg)

    def test_update_put_location_code(self):
        """
        Test that a record can be updated with a PUT.
        """
        self.skipTest("Temporarily skipped")
        # Create LocationCode with POST.
        ld = self._create_location_set_name()
        lf = self._create_location_format(ld)
        lf_uri = reverse('location-format-detail', kwargs={'pk': lf.id})
        new_data = {'char_definition': lf_uri, 'segment': 'T01'}
        uri = reverse('location-code-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Update record with PUT.
        pk = data.get('id')
        uri = reverse('location-code-detail', kwargs={'pk': pk})
        new_data['segment'] = r'T02'
        response = self.client.put(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        # Read record with GET.
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}, new_data: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data),
            new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('segment'), new_data.get('segment'), msg)

    def test_update_put_location_code_set_name_user(self):
        """
        Test that a record can be updated with a PUT for a set_name user.
        """
        self.skipTest("Temporarily skipped")
        # Create a non-logged in user, but one that has a valid token.
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(
            username, password, email='test@example.com',
            role=UserModel.SET_NAME_USER)
        app_name = 'Token Test'
        data = self._make_app_token(
            user, app_name, client, client_type='public',
            grant_type='client_credentials')
        # Create LocationCode with POST by superuser.
        ld = self._create_location_set_name()
        lf = self._create_location_format(ld)
        lf_uri = reverse('location-format-detail', kwargs={'pk': lf.id})
        new_data = {'char_definition': lf_uri, 'segment': 'T01'}
        uri = reverse('location-code-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Update record with PUT by set_name role.
        pk = data.get('id')
        uri = reverse('location-code-detail', kwargs={'pk': pk})
        new_data['segment'] = 'T02'
        response = client.put(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg)

    def test_update_patch_location_code(self):
        """
        Test that a record can be updated with a PATCH.
        """
        self.skipTest("Temporarily skipped")
        # Create LocationCode with POST.
        ld = self._create_location_set_name()
        lf = self._create_location_format(ld)
        lf_uri = reverse('location-format-detail', kwargs={'pk': lf.id})
        new_data = {'char_definition': lf_uri, 'segment': 'T01'}
        uri = reverse('location-code-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Update record with PATCH.
        pk = data.get('id')
        uri = reverse('location-code-detail', kwargs={'pk': pk})
        updated_data = {'segment': 'T02'}
        response = self.client.patch(uri, updated_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        # Read record with GET.
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('segment'), updated_data.get('segment'), msg)

    def test_delete_location_code(self):
        """
        Test that a record can be removed with a DELETE.
        """
        self.skipTest("Temporarily skipped")
        # Create LocationCode with POST.
        ld = self._create_location_set_name()
        lf = self._create_location_format(ld)
        lf_uri = reverse('location-format-detail', kwargs={'pk': lf.id})
        new_data = {'char_definition': lf_uri, 'segment': 'T01'}
        uri = reverse('location-code-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Delete the User.
        pk = data.get('id')
        uri = reverse('location-code-detail', kwargs={'pk': pk})
        response = self.client.delete(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertTrue(data is None, msg)
        # Get the same record through the API.
        response = self.client.get(uri, format='json')
        code = response.status_code
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_404_NOT_FOUND,
            self._clean_data(data))
        self.assertEqual(code, status.HTTP_404_NOT_FOUND, msg)

    def test_options_location_code(self):
        """
        Test that OPTIONS returns the correct data.
        """
        self.skipTest("Temporarily skipped")
        # Create LocationCode with POST.
        ld = self._create_location_set_name()
        lf = self._create_location_format(ld)
        lf_uri = reverse('location-format-detail', kwargs={'pk': lf.id})
        new_data = {'char_definition': lf_uri, 'segment': 'T01'}
        uri = reverse('location-code-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        pk = data.get('id')
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Get the API list OPTIONS.
        response = self.client.options(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('name'), 'Location Code List', msg)
        # Get the API detail OPTIONS.
        uri = reverse('location-code-detail', kwargs={'pk': pk})
        response = self.client.options(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('name'), 'Location Code Detail', msg)

    def test_invalid_segment(self):
        """
        Test that a segment obays the rules.
        """
        self.skipTest("Temporarily skipped")
        # Test delimitor in segment.
        ld = self._create_location_set_name()
        lf = self._create_location_format(ld)
        lf_uri = reverse('location-format-detail', kwargs={'pk': lf.id})
        new_data = {
            'char_definition': lf_uri, 'segment': 'T{}01'.format(ld.separator)
            }
        uri = reverse('location-code-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        self.assertTrue("does not conform to " in data.get('segment')[0], msg)
        # Test inconsistant format.
        new_data = {'char_definition': lf_uri, 'segment': 'S01'}
        uri = reverse('location-code-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        self.assertTrue("does not conform to " in data.get('segment')[0], msg)

    def test_segment_not_parent_to_itself(self):
        """
        Test that a segment is not a parent to itself.
        """
        self.skipTest("Temporarily skipped")
        # Create the location set_name and format objects.
        ld = self._create_location_set_name()
        lf = self._create_location_format(ld)
        lf_uri = reverse('location-format-detail', kwargs={'pk': lf.id})
        # Create the first location code.
        new_data = {'char_definition': lf_uri, 'segment': 'T01'}
        uri = reverse('location-code-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Create a second location code.
        lc_uri = reverse('location-code-detail', kwargs={'pk': data.get('id')})
        new_data = {'char_definition': lf_uri, 'segment': 'T01',
                    'parent': lc_uri}
        uri = reverse('location-code-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        self.assertTrue("child to itself." in data.get('__all__')[0], msg)

    def test_segments_have_same_location_set_name(self):
        """
        Test that all the segments in a given tree have the same location
        set_name.
        """
        self.skipTest("Temporarily skipped")
        # Create the location set_name and format objects.
        ld0 = self._create_location_set_name()
        lf0 = self._create_location_format(ld0)
        lf0_uri = reverse('location-format-detail', kwargs={'pk': lf0.id})
        # Create second set of location set_name and format objects.
        ld1 = self._create_location_set_name(name="This one fails")
        lf1 = self._create_location_format(ld1, char_definition=r'C\d\dR\d\d',
                                           segment_order=1)
        lf1_uri = reverse('location-format-detail', kwargs={'pk': lf1.id})
        # Create first location code.
        new_data = {'char_definition': lf0_uri, 'segment': 'T01'}
        uri = reverse('location-code-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Create second location code.
        lc0_uri = reverse('location-code-detail', kwargs={'pk': data.get('id')})
        new_data = {'char_definition': lf1_uri, 'segment': 'C01R01',
                    'parent': lc0_uri}
        uri = reverse('location-code-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        self.assertTrue(
            "All segments must be derived" in data.get('__all__')[0], msg)

    def test_number_segments_number_formats(self):
        """
        Test that the number of segments defined are equal to or less than
        the number of formats for this location set_name.
        """
        self.skipTest("Temporarily skipped")
        # Create the location set_name and format objects.
        ld0 = self._create_location_set_name()
        lf0 = self._create_location_format(ld0)
        lf0_uri = reverse('location-format-detail', kwargs={'pk': lf0.id})
        # Create second set of location format object.
        lf1 = self._create_location_format(ld0, char_definition=r'C\d\dR\d\d',
                                           segment_order=1)
        lf1_uri = reverse('location-format-detail', kwargs={'pk': lf1.id})
        # Create first location code.
        new_data = {'char_definition': lf0_uri, 'segment': 'T01'}
        uri = reverse('location-code-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Create second location code.
        lc0_uri = reverse('location-code-detail', kwargs={'pk': data.get('id')})
        new_data = {'char_definition': lf1_uri, 'segment': 'C01R01',
                    'parent': lc0_uri}
        uri = reverse('location-code-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Create third location code which will fail.
        lc1_uri = reverse('location-code-detail', kwargs={'pk': data.get('id')})
        new_data = {'char_definition': lf1_uri, 'segment': 'C01R01',
                    'parent': lc1_uri}
        uri = reverse('location-code-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        self.assertTrue("as a child to itself." in data.get('__all__')[0], msg)
