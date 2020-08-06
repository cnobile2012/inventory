# -*- coding: utf-8 -*-
#
# inventory/locations/api/tests/test_locations_api.py
#

import random

from django.contrib.auth import get_user_model

from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from inventory.common.api.tests.base_test import BaseTest
from inventory.locations.models import (
    LocationSetName, LocationFormat, LocationCode)
from inventory.projects.models import Membership

UserModel = get_user_model()


class TestLocationSetNameAPI(BaseTest, APITestCase):
    PROJECT_USER = Membership.ROLE_MAP[Membership.PROJECT_USER]
 
    def __init__(self, name):
        super().__init__(name)

    def setUp(self):
        super().setUp()
        # Create an InventoryType and Project.
        self.in_type = self._create_inventory_type()
        members = [
            {'user': self.user, 'role_text': self.PROJECT_USER}
            ]
        self.project = self._create_project(self.in_type, members=members)
        kwargs = {'public_id': self.project.public_id}
        self.project_uri = reverse('project-detail', kwargs=kwargs)

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
        self._test_users_with_valid_permissions(uri, method,
                                                default_user=False)
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
        uri = reverse('location-set-name-list')
        data = {}
        data['name'] = 'Test Location Set Name 01'
        data['project'] = self.project_uri
        data['separator'] = '--->'
        response = self.client.post(uri, data=data, format='json')
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        self.assertTrue(self._has_error(response, error_key='separator'), msg)
        self._test_errors(response, tests={
            'separator': "Ensure this field has no more than 3 characters.",
            })

    def test_POST_creates_root_format_and_code(self):
        """
        Test that both a ROOT format and a ROOT code are created when a
        set name is created.
        """
        #self.skipTest("Temporarily skipped")
        uri = reverse('location-set-name-list')
        data = {}
        data['name'] = 'Test Location Set Name 01'
        data['description'] = "Test ROOTS for format and code."
        data['project'] = self.project_uri
        response = self.client.post(uri, data=data, format='json')
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Test that the ROOT format now exists.
        lf_uris = response.data.get('location_formats')
        self.assertTrue(len(lf_uris) > 0, msg)
        response = self.client.get(lf_uris[0], format='json')
        msg = "data: {}".format(response.data)
        self.assertEqual(response.data.get('char_definition'),
                         LocationCode.ROOT_NAME, msg)
        # Test that the ROOT code now exists.
        lc_uris = response.data.get('location_codes')
        self.assertTrue(len(lc_uris) > 0, msg)
        response = self.client.get(lc_uris[0], format='json')
        msg = "data: {}".format(response.data)
        self.assertEqual(response.data.get('segment'),
                         LocationCode.ROOT_NAME, msg)


class TestLocationFormatAPI(BaseTest, APITestCase):
    PROJECT_USER = Membership.ROLE_MAP[Membership.PROJECT_USER]

    def __init__(self, name):
        super().__init__(name)

    def setUp(self):
        super().setUp()
        # Create an InventoryType, Project, and LocationSetName.
        self.in_type = self._create_inventory_type()
        members = [
            {'user': self.user, 'role_text': self.PROJECT_USER}
            ]
        self.project = self._create_project(self.in_type, members=members)
        self.location_set_name = self._create_location_set_name(self.project)
        kwargs = {'public_id': self.location_set_name.public_id}
        self.location_set_name_uri = reverse('location-set-name-detail',
                                             kwargs=kwargs)

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
        self._test_users_with_valid_permissions(uri, method,
                                                default_user=False)
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
        Test that a POST to location_format_list passes with valid
        permissions.
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
        Test that a PUT to location_format_detail passes with valid
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
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, msg)
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


class TestLocationCodeAPI(BaseTest, APITestCase):
    PROJECT_USER = Membership.ROLE_MAP[Membership.PROJECT_USER]

    def __init__(self, name):
        super().__init__(name)

    def setUp(self):
        super().setUp()
        # Create an InventoryType, Project, and LocationSetName.
        self.in_type = self._create_inventory_type()
        members = [
            {'user': self.user, 'role_text': self.PROJECT_USER}
            ]
        self.project = self._create_project(self.in_type, members=members)
        self.location_set_name = self._create_location_set_name(self.project)
        self.location_format = self._create_location_format(
            self.location_set_name, 'A\d\d')
        kwargs = {'public_id': self.location_format.public_id}
        self.location_format_uri = reverse('location-format-detail',
                                           kwargs=kwargs)

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
        self._test_users_with_valid_permissions(
            uri, method, default_user=False)
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
        Test that a POST to location_code_list passes with valid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'post'
        uri = reverse('location-code-list')
        data = {}
        su = data.setdefault('SU', {})
        su['segment'] = 'A01'
        su['location_format'] = self.location_format_uri
        ad = data.setdefault('AD', su.copy())
        ad['segment'] = 'A02'
        du = data.setdefault('DU', su.copy())
        du['segment'] = 'A03'
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)
        pow = data.setdefault('POW', su.copy())
        pow['segment'] = 'A04'
        pma = data.setdefault('PMA', su.copy())
        pma['segment'] = 'A05'
        pdu = data.setdefault('PDU', su.copy())
        pdu['segment'] = 'A06'
        self._test_project_users_with_valid_permissions(
            uri, method, project_user=False, request_data=data)

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

    def test_GET_location_code_detail_with_invalid_permissions(self):
        """
        Test that a GET on the location_code_detail fails with invalid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        location_code = self._create_location_code(self.location_format, "A01")
        uri = reverse('location-format-detail',
                      kwargs={'public_id': location_code.public_id})
        method = 'get'
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_GET_location_format_detail_with_valid_permissions(self):
        """
        Test that a GET to location_format_detail passes with valid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        location_code = self._create_location_code(self.location_format, "A01")
        uri = reverse('location-code-detail',
                      kwargs={'public_id': location_code.public_id})
        method = 'get'
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_PUT_location_code_detail_with_invalid_permissions(self):
        """
        Test that a PUT to location_code_detail fails with invalid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        location_code = self._create_location_code(
            self.location_format, "A01")
        uri = reverse('location-code-detail',
                      kwargs={'public_id': location_code.public_id})
        method = 'put'
        data = {}
        su = data.setdefault('SU', {})
        su['segment'] = 'A11'
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

    def test_PUT_location_code_detail_with_valid_permissions(self):
        """
        Test that a PUT to location_code_detail passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        location_code = self._create_location_code(self.location_format, "A01")
        uri = reverse('location-code-detail',
                      kwargs={'public_id': location_code.public_id})
        method = 'put'
        data = {}
        su = data.setdefault('SU', {})
        su['segment'] = 'A11'
        su['location_format'] = self.location_format_uri
        ad = data.setdefault('AD', su.copy())
        ad['segment'] = 'A12'
        ad['location_format'] = self.location_format_uri
        du = data.setdefault('DU', su.copy())
        du['segment'] = 'A13'
        du['location_format'] = self.location_format_uri
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)
        pow = data.setdefault('POW', su.copy())
        pow['segment'] = 'A21'
        pow['location_format'] = self.location_format_uri
        pma = data.setdefault('PMA', su.copy())
        pma['segment'] = 'A22'
        pma['location_format'] = self.location_format_uri
        pdu = data.setdefault('PDU', su.copy())
        pdu['segment'] = 'A23'
        pdu['location_format'] = self.location_format_uri
        self._test_project_users_with_valid_permissions(
            uri, method, project_user=False, request_data=data)

    def test_PATCH_location_code_detail_with_invalid_permissions(self):
        """
        Test that a PATCH to location_code_detail fails with invalid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        location_code = self._create_location_code(self.location_format, "A11")
        uri = reverse('location-code-detail',
                      kwargs={'public_id': location_code.public_id})
        method = 'patch'
        data = {}
        su = data.setdefault('SU', {})
        su['segment'] = 'A11'
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

    def test_PATCH_location_code_detail_with_valid_permissions(self):
        """
        Test that a PATCH to location_code_detail passes with valid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        location_code = self._create_location_code(self.location_format, "A11")
        uri = reverse('location-code-detail',
                      kwargs={'public_id': location_code.public_id})
        method = 'patch'
        data = {}
        su = data.setdefault('SU', {})
        su['segment'] = 'A12'
        ad = data.setdefault('AD', {})
        ad['segment'] = 'A13'
        du = data.setdefault('DU', {})
        du['segment'] = 'A14'
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)
        pow = data.setdefault('POW', {})
        pow['segment'] = 'A15'
        pma = data.setdefault('PMA', {})
        pma['segment'] = 'A16'
        pdu = data.setdefault('PDU', {})
        pdu['segment'] = 'A17'
        self._test_project_users_with_valid_permissions(
            uri, method, project_user=False, request_data=data)

    def test_DELETE_location_code_detail_with_invalid_permissions(self):
        """
        Test that a DELETE to location_code_detail fails with invalid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'delete'
        location_code = self._create_location_code(self.location_format, "A11")
        uri = reverse('location-code-detail',
                      kwargs={'public_id': location_code.public_id})
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_DELETE_location_code_detail_with_valid_permissions(self):
        """
        Test that a DELETE to location_code_detail pass' with valid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'delete'
        # Test SUPERUSER
        location_code = self._create_location_code(self.location_format, "A11")
        uri = reverse('location-code-detail',
                      kwargs={'public_id': location_code.public_id})
        self._test_superuser_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test ADMINISTRATOR
        location_code = self._create_location_code(self.location_format, "A11")
        uri = reverse('location-code-detail',
                      kwargs={'public_id': location_code.public_id})
        self._test_administrator_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test DEFAULT_USER
        ## This is an invalid test since the DEFAULT_USER has no access.
        # Test PROJECT_OWNER
        location_code = self._create_location_code(self.location_format, "A11")
        uri = reverse('location-code-detail',
                      kwargs={'public_id': location_code.public_id})
        self._test_project_owner_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test PROJECT_MANAGER
        location_code = self._create_location_code(self.location_format, "A11")
        uri = reverse('location-code-detail',
                      kwargs={'public_id': location_code.public_id})
        self._test_project_manager_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test PROJECT_USER
        ## This is an invalid test since the PROJECT_USER has no access.

    def test_OPTIONS_location_code_detail_with_invalid_permissions(self):
        """
        Test that the method OPTIONS fails with invald permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'options'
        location_code = self._create_location_code(self.location_format, "A11")
        uri = reverse('location-code-detail',
                      kwargs={'public_id': location_code.public_id})
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_OPTIONS_location_code_detail_with_valid_permissions(self):
        """
        Test that the method OPTIONS brings back the correct data.
        """
        method = 'options'
        location_code = self._create_location_code(self.location_format, "A11")
        uri = reverse('location-code-detail',
                      kwargs={'public_id': location_code.public_id})
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_invalid_segment(self):
        """
        Test that a segment obays the rules.
        """
        #self.skipTest("Temporarily skipped")
        # Test delimitor in segment.
        data = {
            'location_format': self.location_format_uri,
            'segment': 'T{}01'.format(self.location_set_name.separator)
            }
        uri = reverse('location-code-list')
        response = self.client.post(
            uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        msg = "Avaliable keys are: {}".format(response.data.keys())
        self.assertTrue(self._has_error(response, error_key='segment'), msg)
        self._test_errors(response, tests={
            'segment': "does not conform to ",
            })
        # Test inconsistant format.
        data = {
            'location_format': self.location_format_uri,
            'segment': 'S01'
            }
        uri = reverse('location-code-list')
        response = self.client.post(
            uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        msg = "Avaliable keys are: {}".format(response.data.keys())
        self.assertTrue(self._has_error(response, error_key='segment'), msg)
        self._test_errors(response, tests={
            'segment': "does not conform to ",
            })

    def test_segment_not_parent_to_itself(self):
        """
        Test that a segment is not a parent to itself.
        """
        #self.skipTest("Temporarily skipped")
        # Create the first location code.
        uri = reverse('location-code-list')
        data = {
            'location_format': self.location_format_uri,
            'segment': 'A11'
            }
        response = self.client.post(
            uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Create a second location code.
        data = {
            'location_format': self.location_format_uri,
            'segment': 'A11',
            'parent': response.data.get('href')
            }
        response = self.client.post(
            uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        msg = "Avaliable items are: {}".format(response.data.items())
        self.assertTrue(self._has_error(response, error_key='parent'), msg)
        self._test_errors(response, tests={
            'parent': "You cannot have a segment as a child to itself.",
            })

    def test_segments_have_same_location_set_name(self):
        """
        Test that all the segments in a given tree have the same location
        set_name.
        """
        #self.skipTest("Temporarily skipped")
        # Create the location set_name and format objects.
        ld0 = self._create_location_set_name(
            self.project, name="This one is OK")
        lf0 = self._create_location_format(ld0, 'T\d\d')
        lf0_uri = reverse('location-format-detail',
                          kwargs={'public_id': lf0.public_id})
        # Create second set of location set_name and format objects.
        ld1 = self._create_location_set_name(
            self.project, name="This one causes it to break")
        lf1 = self._create_location_format(ld1, r'C\d\dR\d\d', segment_order=1)
        lf1_uri = reverse('location-format-detail',
                          kwargs={'public_id': lf1.public_id})
        # Create first location code.
        data = {
            'location_format': lf0_uri,
            'segment': 'T01',
            }
        uri = reverse('location-code-list')
        response = self.client.post(
            uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        self.assertTrue(response.data.get('parent'), msg)
        self.assertTrue(response.data.get('href'), msg)
        # Create second location code.
        data = {
            'location_format': lf1_uri,
            'segment': 'C01R01',
            'parent': response.data.get('href')
            }
        response = self.client.post(
            uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        msg = "Avaliable items are: {}".format(response.data.items())
        self.assertTrue(self._has_error(
            response, error_key='location_set_name'), msg)
        self._test_errors(response, tests={
            'location_set_name': "All segments must be derived",
            })

    def test_altering_root_code(self):
        """
        Test that altering the root code is disallowed.
        """
        #self.skipTest("Temporarily skipped")
        # Create a location code.
        location_code = self._create_location_code(
            self.location_format, "A01")
        uri = reverse('location-code-detail',
                      kwargs={'public_id': location_code.public_id})
        data = {
            'location_format': self.location_format_uri,
            'segment': LocationCode.ROOT_NAME
            }
        response = self.client.put(
            uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST, msg)
        self.assertTrue(self._has_error(response, error_key='segment'), msg)
        self._test_errors(response, tests={
            'segment': ("Segment is '{}', This is an unalterable root "
                        "location.").format(LocationCode.ROOT_NAME)
            })


class TestLocationSetNameCloneAPI(BaseTest, APITestCase):
    DEFAULT_USER = UserModel.ROLE_MAP[UserModel.DEFAULT_USER]

    def __init__(self, name):
        super().__init__(name)

    def setUp(self):
        super().setUp()
        # Create an InventoryType and Project.
        self.in_type = self._create_inventory_type()
        members = [
            {'user': self.user, 'role_text': self.PROJECT_USER}
            ]
        self.project = self._create_project(self.in_type, members=members)
        self.location_set_name = self._create_location_set_name(self.project)
        kwargs = {'public_id': self.location_set_name.public_id}
        self.location_set_name_uri = reverse('location-set-name-detail',
                                             kwargs=kwargs)
        self.location_format = self._create_location_format(
            self.location_set_name, 'A\d\d')

    def test_GET_location_clone_with_invalid_permissions(self):
        """
        Test the location_clone endpoint fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        location_code = self._create_location_code(self.location_format, "A01")
        uri = reverse('location-clone')
        data = {}
        su = data.setdefault('SU', {})
        su['location_set_name'] = self.location_set_name.public_id
        su['project'] = self.project.public_id
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            uri, method, request_data=data)
        data.setdefault('POW', su.copy())
        data.setdefault('PMA', su.copy())
        data.setdefault('PDU', su.copy())
        self._test_project_users_with_invalid_permissions(
            uri, method, request_data=data)
        loc_set_name = LocationSetName.objects.all()
        loc_fmts = LocationFormat.objects.all()

    def test_GET_location_clone_with_valid_permissions(self):
        """
        Test the location_clone endpoint passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        location_code = self._create_location_code(self.location_format, "A01")
        uri = reverse('location-clone')
        data = {}
        su = data.setdefault('SU', {})
        su['location_set_name'] = self.location_set_name.public_id
        su['project'] = self.project.public_id
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)
        data.setdefault('POW', su.copy())
        data.setdefault('PMA', su.copy())
        data.setdefault('PDU', su.copy())
        self._test_project_users_with_valid_permissions(
            uri, method, request_data=data)

    def test_GET_location_clone_with_parameters(self):
        """
        Test the location_clone endpoint with various parameters.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        location_code = self._create_location_code(self.location_format, "A01")
        uri = reverse('location-clone')
        data = {}
        data['location_set_name'] = self.location_set_name.public_id
        data['project'] = self.project.public_id
        # Test with default arguments.
        response = self.client.get(uri, data=data, format='json',
                                   **self._HEADERS)
        msg = ("data: {}, found '{}' records , should be 2 records"
               ).format(response.data, len(response.data))
        self.assertEqual(len(response.data), 2, msg)
        # Test with with_set_name=False
        data['with_set_name'] = False
        response = self.client.get(uri, data=data, format='json',
                                   **self._HEADERS)
        msg = ("data: {}, found '{}' records , should be 1 records"
               ).format(response.data, len(response.data))
        self.assertEqual(len(response.data), 1, msg)
        # Test with with_root=True and with_set_name=True
        data['with_set_name'] = True
        data['with_root'] = True
        response = self.client.get(uri, data=data, format='json',
                                   **self._HEADERS)
        msg = ("data: {}, found '{}' records , should be 3 records"
               ).format(response.data, len(response.data))
        self.assertEqual(len(response.data), 3, msg)

    def test_POST_location_clone_with_invalid_permissions(self):
        """
        Test the location_clone endpoint fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'post'
        project = self._create_project(self.in_type, name="Test Project_1")
        uri = reverse('location-clone')
        data = {}
        su = data.setdefault('SU', {})
        su['location_set_name'] = self.location_set_name.public_id
        su['project'] = project.public_id
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            uri, method, request_data=data)
        data.setdefault('POW', su.copy())
        data.setdefault('PMA', su.copy())
        data.setdefault('PDU', su.copy())
        self._test_project_users_with_invalid_permissions(
            uri, method, request_data=data)
        loc_set_name = LocationSetName.objects.filter(project=project)
        loc_fmts = LocationFormat.objects.filter(
            location_set_name__project=project)
        msg = ("Found '{}' LocationSetName, and '{}' LocationFormat records, "
               "should be 0 and 0 records").format(
                   loc_set_name.count(), loc_fmts.count())
        self.assertTrue(loc_set_name.count() == 0
                        and loc_fmts.count() == 0, msg)

    def test_POST_location_clone_with_valid_permissions_superuser(self):
        """
        Test the location_clone endpoint passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'post'
        project = self._create_project(self.in_type, name="Test Project_1")
        uri = reverse('location-clone')
        data = {}
        su = data.setdefault('SU', {})
        su['location_set_name'] = self.location_set_name.public_id
        su['project'] = project.public_id
        self._test_superuser_with_valid_permissions(
            uri, method, request_data=data)
        loc_set_name = LocationSetName.objects.filter(project=project)
        loc_fmts = LocationFormat.objects.filter(
            location_set_name__project=project)
        msg = ("Found '{}' LocationSetName, and '{}' LocationFormat "
               "records, should be 1 and 2 records").format(
                   loc_set_name.count(), loc_fmts.count())
        self.assertTrue(loc_set_name.count() == 1
                        and loc_fmts.count() == 2, msg)

    def test_POST_location_clone_with_valid_permissions_administrator(self):
        """
        Test the location_clone endpoint passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'post'
        project = self._create_project(self.in_type, name="Test Project_1")
        uri = reverse('location-clone')
        data = {}
        ad = data.setdefault('AD', {})
        ad['location_set_name'] = self.location_set_name.public_id
        ad['project'] = project.public_id
        self._test_administrator_with_valid_permissions(
            uri, method, request_data=data)
        loc_set_name = LocationSetName.objects.filter(project=project)
        loc_fmts = LocationFormat.objects.filter(
            location_set_name__project=project)
        msg = ("Found '{}' LocationSetName, and '{}' LocationFormat "
               "records, should be 1 and 2 records").format(
                   loc_set_name.count(), loc_fmts.count())
        self.assertTrue(loc_set_name.count() == 1
                        and loc_fmts.count() == 2, msg)

    def test_POST_location_clone_with_valid_permissions_project_owner(self):
        """
        Test the location_clone endpoint passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'post'
        # Create a new user and project
        kwargs = self._setup_user_credentials()
        user, client = self._create_user(**kwargs)
        project = self._create_project(self.in_type, name="Test Project_1")
        members = [
            {'user': user, 'role_text': self.PROJECT_USER}
            ]
        project.process_members(members)
        # Test project owner
        uri = reverse('location-clone')
        data = {}
        pow = data.setdefault('POW', {})
        pow['location_set_name'] = self.location_set_name.public_id
        pow['project'] = project.public_id
        self._test_project_owner_with_valid_permissions(
            uri, method, request_data=data)
        loc_set_name = LocationSetName.objects.filter(project=project)
        loc_fmts = LocationFormat.objects.filter(
            location_set_name__project=project)
        msg = ("Found '{}' LocationSetName, and '{}' LocationFormat "
               "records, should be 1 and 2 records").format(
                   loc_set_name.count(), loc_fmts.count())
        self.assertTrue(loc_set_name.count() == 1
                        and loc_fmts.count() == 2, msg)

    def test_POST_location_clone_with_valid_permissions_project_manager(self):
        """
        Test the location_clone endpoint passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'post'
        # Create a new user and project
        kwargs = self._setup_user_credentials()
        user, client = self._create_user(**kwargs)
        project = self._create_project(self.in_type, name="Test Project_1",
                                       user=user)
        # Test project owner
        uri = reverse('location-clone')
        data = {}
        pma = data.setdefault('PMA', {})
        pma['location_set_name'] = self.location_set_name.public_id
        pma['project'] = project.public_id
        self._test_project_manager_with_valid_permissions(
            uri, method, request_data=data)
        loc_set_name = LocationSetName.objects.filter(project=project)
        loc_fmts = LocationFormat.objects.filter(
            location_set_name__project=project)
        msg = ("Found '{}' LocationSetName, and '{}' LocationFormat "
               "records, should be 1 and 2 records").format(
                   loc_set_name.count(), loc_fmts.count())
        self.assertTrue(loc_set_name.count() == 1
                        and loc_fmts.count() == 2, msg)

    def test_DELETE_location_clone_with_invalid_permissions(self):
        """
        Test the location_clone endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'delete'
        location_code = self._create_location_code(self.location_format, "A01")
        uri = reverse('location-clone')
        data = {}
        su = data.setdefault('SU', {})
        su['location_set_name'] = self.location_set_name.public_id
        su['project'] = self.project.public_id
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            uri, method, request_data=data)
        data.setdefault('POW', su.copy())
        data.setdefault('PMA', su.copy())
        data.setdefault('PDU', su.copy())
        self._test_project_users_with_invalid_permissions(
            uri, method, request_data=data)
        loc_set_name = LocationSetName.objects.filter(project=self.project)
        loc_fmts = LocationFormat.objects.filter(
            location_set_name__project=self.project)
        msg = ("Found '{}' LocationSetName, and '{}' LocationFormat "
               "records, should be 1 and 2 records").format(
                   loc_set_name.count(), loc_fmts.count())
        self.assertTrue(loc_set_name.count() == 1
                        and loc_fmts.count() == 2, msg)

    def test_DELETE_location_clone_with_valid_permissions_superuser(self):
        """
        Test the location_clone endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'delete'
        location_code = self._create_location_code(self.location_format, "A01")
        uri = reverse('location-clone')
        data = {}
        su = data.setdefault('SU', {})
        su['location_set_name'] = self.location_set_name.public_id
        su['project'] = self.project.public_id
        self._test_superuser_with_valid_permissions(
            uri, method, request_data=data)
        loc_set_name = LocationSetName.objects.filter(project=self.project)
        loc_fmts = LocationFormat.objects.filter(
            location_set_name__project=self.project)
        msg = ("Found '{}' LocationSetName, and '{}' LocationFormat "
               "records, should be 0 and 0 records").format(
                   loc_set_name.count(), loc_fmts.count())
        self.assertTrue(loc_set_name.count() == 0
                        and loc_fmts.count() == 0, msg)

    def test_DELETE_location_clone_with_valid_permissions_administrator(self):
        """
        Test the location_clone endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'delete'
        location_code = self._create_location_code(self.location_format, "A01")
        uri = reverse('location-clone')
        data = {}
        ad = data.setdefault('AD', {})
        ad['location_set_name'] = self.location_set_name.public_id
        ad['project'] = self.project.public_id
        self._test_administrator_with_valid_permissions(
            uri, method, request_data=data)
        loc_set_name = LocationSetName.objects.filter(project=self.project)
        loc_fmts = LocationFormat.objects.filter(
            location_set_name__project=self.project)
        msg = ("Found '{}' LocationSetName, and '{}' LocationFormat "
               "records, should be 0 and 0 records").format(
                   loc_set_name.count(), loc_fmts.count())
        self.assertTrue(loc_set_name.count() == 0
                        and loc_fmts.count() == 0, msg)

    def test_DELETE_location_clone_with_valid_permissions_project_owner(self):
        """
        Test the location_clone endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'delete'
        location_code = self._create_location_code(self.location_format, "A01")
        uri = reverse('location-clone')
        data = {}
        pow = data.setdefault('POW', {})
        pow['location_set_name'] = self.location_set_name.public_id
        pow['project'] = self.project.public_id
        self._test_project_owner_with_valid_permissions(
            uri, method, request_data=data)
        loc_set_name = LocationSetName.objects.filter(project=self.project)
        loc_fmts = LocationFormat.objects.filter(
            location_set_name__project=self.project)
        msg = ("Found '{}' LocationSetName, and '{}' LocationFormat "
               "records, should be 0 and 0 records").format(
                   loc_set_name.count(), loc_fmts.count())
        self.assertTrue(loc_set_name.count() == 0
                        and loc_fmts.count() == 0, msg)

    def test_DELETE_location_clone_valid_permissions_project_manager(self):
        """
        Test the location_clone endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'delete'
        location_code = self._create_location_code(self.location_format, "A01")
        uri = reverse('location-clone')
        data = {}
        pma = data.setdefault('PMA', {})
        pma['location_set_name'] = self.location_set_name.public_id
        pma['project'] = self.project.public_id
        self._test_project_manager_with_valid_permissions(
            uri, method, request_data=data)
        loc_set_name = LocationSetName.objects.filter(project=self.project)
        loc_fmts = LocationFormat.objects.filter(
            location_set_name__project=self.project)
        msg = ("Found '{}' LocationSetName, and '{}' LocationFormat "
               "records, should be 0 and 0 records").format(
                   loc_set_name.count(), loc_fmts.count())
        self.assertTrue(loc_set_name.count() == 0
                        and loc_fmts.count() == 0, msg)

    def test_location_clone_serializer_validation_errors_on_project(self):
        """
        Test that invalid data causes validation errors.
        """
        #self.skipTest("Temporarily skipped")
        location_code = self._create_location_code(self.location_format, "A01")
        uri = reverse('location-clone')
        data = {}
        data['location_set_name'] = self.location_set_name.public_id
        data['project'] = 'junk'
        kwargs = self._setup_user_credentials()
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = self.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        members = [
            {'user': self.user, 'role_text': self.PROJECT_USER},
            {'user': user, 'role_text': self.PROJECT_USER}
            ]
        self.project.process_members(members)
        self.project.set_role(user, Membership.PROJECT_USER)
        response = client.get(uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        self.assertTrue(self._has_error(response, error_key='project'), msg)
        self._test_errors(response, tests={
            'project': "A project with the public_id 'junk' does not exist.",
            })

    def test_location_clone_serializer_validation_errors_on_location_set(self):
        """
        Test that invalid data causes validation errors.
        """
        #self.skipTest("Temporarily skipped")
        location_code = self._create_location_code(self.location_format, "A01")
        uri = reverse('location-clone')
        data = {}
        data['location_set_name'] = 'junk'
        data['project'] = self.project.public_id
        kwargs = self._setup_user_credentials()
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = self.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        members = [
            {'user': self.user, 'role_text': self.PROJECT_USER},
            {'user': user, 'role_text': self.PROJECT_USER}
            ]
        self.project.process_members(members)
        self.project.set_role(user, Membership.PROJECT_USER)
        response = client.get(uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        self.assertTrue(self._has_error(
            response, error_key='location_set_name'), msg)
        self._test_errors(response, tests={
            'location_set_name': "Location set name 'junk' could not be found."
            })
