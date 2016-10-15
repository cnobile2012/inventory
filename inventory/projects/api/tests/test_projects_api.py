# -*- coding: utf-8 -*-
#
# inventory/projects/api/tests/test_projects.py
#
# Run ./manage.py test -k # Keep the DB, don't rebuild.
#

import random

from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APIClient

from inventory.common.api.tests.base_test import BaseTest
from inventory.projects.models import Project, Membership


class TestProject(BaseTest):

    def __init__(self, name):
        super(TestProject, self).__init__(name)

    def setUp(self):
        super(TestProject, self).setUp()
        # Create an InventoryType and a Project.
        self.in_type = self._create_inventory_type()
        kwargs = {'public_id': self.in_type.public_id}
        self.in_type_uri = self._resolve('inventory-type-detail', **kwargs)
        self.project = self._create_project(self.in_type, members=[self.user])
        kwargs = {'public_id': self.project.public_id}
        self.project_uri = self._resolve('project-detail', **kwargs)

    def test_GET_condition_errors(self):
        self.skipTest("Temporarily skipped")
        from django.contrib.auth import get_user_model
        User = get_user_model()

        username = 'Normal_User'
        password = '123456'
        kwargs = {}
        kwargs['username'] = username
        kwargs['password'] = password
        kwargs['is_superuser'] = True
        kwargs['is_active'] = True
        user = User.objects.create(**kwargs)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(
            self.project_uri, format='json',
            **{'HTTP_ACCEPT': 'application/json',})
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)

    def test_GET_project_list_with_invalid_permissions(self):
        """
        Test the project_list endpoint with no permissions. This is the
        one endpoint where a DEFAULT_USER can create an object, so it will
        not fail, therefore we skip it.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        uri = reverse('project-list')
        self._test_user_with_invalid_permissions(
            uri, method, default_user=False)
        self._test_project_user_with_invalid_permissions(uri, method)

    def test_GET_project_list_with_valid_permissions(self):
        """
        Test the project_list endpoint with various permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        uri = reverse('project-list')
        self._test_user_with_valid_permissions(uri, method)
        self._test_project_user_with_valid_permissions(uri, method)

    def test_POST_project_list_with_invalid_permissions(self):
        """
        Test that a POST to project_list fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        kwargs = self._setup_user_credentials()
        user, client = self._create_user(**kwargs)
        method = 'post'
        uri = reverse('project-list')
        data = {}
        su = data.setdefault('SU', {})
        su['name'] = 'My Test Project'
        su['inventory_type'] = self.in_type_uri
        su['members'] = [self._resolve('user-detail',
                                       **{'public_id': user.public_id})]
        su['role'] = {'user': user.username, 'role': Membership.DEFAULT_USER}
        ad = data.setdefault('AD', su.copy())
        #du = data.setdefault('DU', su.copy())
        self._test_user_with_invalid_permissions(
            uri, method, request_data=data, default_user=False)
        pow = data.setdefault('POW', su.copy())
        pma = data.setdefault('PMA', su.copy())
        #pdu = data.setdefault('PDU', su.copy())
        self._test_project_user_with_invalid_permissions(
            uri, method, request_data=data, default_user=False)

    def test_POST_project_list_with_valid_permissions(self):
        """
        Test that a POST to project_list passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        kwargs = self._setup_user_credentials()
        user, client = self._create_user(**kwargs)
        method = 'post'
        uri = reverse('project-list')
        data = {}
        su = data.setdefault('SU', {})
        su['name'] = 'My Test Project 1'
        su['inventory_type'] = self.in_type_uri
        su['members'] = [self._resolve('user-detail',
                                       **{'public_id': user.public_id})]
        su['role'] = {'user': user.username, 'role': Membership.DEFAULT_USER}
        ad = data.setdefault('AD', su.copy())
        ad['name'] = 'My Test Project 2'
        du = data.setdefault('DU', su.copy())
        du['name'] = 'My Test Project 3'
        self._test_user_with_valid_permissions(
            uri, method, request_data=data)
        pow = data.setdefault('POW', su.copy())
        pow['name'] = 'My Test Project 4'
        pma = data.setdefault('PMA', su.copy())
        pma['name'] = 'My Test Project 5'
        pdu = data.setdefault('PDU', su.copy())
        pdu['name'] = 'My Test Project 6'
        pdu['role'] = {'user': user.username, 'role': Membership.DEFAULT_USER}
        self._test_project_user_with_valid_permissions(
            uri, method, default_user=False, request_data=data)

    def test_OPTIONS_project_list_with_invalid_permissions(self):
        """
        Test that the method OPTIONS fails with invald permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'options'
        uri = reverse('project-list')
        self._test_user_with_invalid_permissions(
            uri, method, default_user=False)
        self._test_project_user_with_invalid_permissions(uri, method)

    def test_OPTIONS_project_list_with_valid_permissions(self):
        """
        Test that the method OPTIONS brings back the correct data.
        """
        #self.skipTest("Temporarily skipped")
        method = 'options'
        uri = reverse('project-list')
        self._test_user_with_valid_permissions(uri, method)
        self._test_project_user_with_valid_permissions(uri, method)

    def test_GET_project_detail_with_invalid_permissions(self):
        """
        Test that a GET on the project_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        self._test_user_with_invalid_permissions(self.project_uri, method)
        self._test_project_user_with_invalid_permissions(
            self.project_uri, method)

    def test_GET_project_detail_with_valid_permissions(self):
        """
        Test that a GET to project_detail passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        self._test_user_with_valid_permissions(self.project_uri, method)
        self._test_project_user_with_valid_permissions(self.project_uri, method)

    def test_PUT_project_detail_with_invalid_permissions(self):
        """
        Test that a PUT to project_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        kwargs = self._setup_user_credentials()
        user, client = self._create_user(**kwargs)
        method = 'put'
        data = {}
        su = data.setdefault('SU', {})
        su['name'] = 'Test Project 01'
        su['inventory_type'] = self.in_type_uri
        su['members'] = [self._resolve('user-detail',
                                       **{'public_id': user.public_id})]
        su['role'] = {'user': user.username, 'role': Membership.DEFAULT_USER}
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_user_with_invalid_permissions(
            self.project_uri, method, request_data=data)
        data.setdefault('POW', su.copy())
        data.setdefault('PMA', su.copy())
        data.setdefault('PDU', su.copy())
        self._test_project_user_with_invalid_permissions(
            self.project_uri, method, request_data=data)

    def test_PUT_category_detail_with_valid_permissions(self):
        """
        Test that a PUT to category_detail passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        kwargs = self._setup_user_credentials()
        user, client = self._create_user(**kwargs)
        method = 'put'
        data = {}
        su = data.setdefault('SU', {})
        su['name'] = 'Test Project 01'
        su['inventory_type'] = self.in_type_uri
        su['members'] = [self._resolve('user-detail',
                                       **{'public_id': user.public_id})]
        su['role'] = {'user': user.username, 'role': Membership.DEFAULT_USER}
        ad = data.setdefault('AD', su.copy())
        ad['name'] = 'Test Project 02'
        du = data.setdefault('DU', su.copy())
        du['name'] = 'Test Project 03'
        self._test_user_with_valid_permissions(
            self.project_uri, method, request_data=data)
        pow = data.setdefault('POW', su.copy())
        pow['name'] = 'Test Project 04'
        pma = data.setdefault('PMA', su.copy())
        pma['name'] = 'Test Project 05'
        pdu = data.setdefault('PDU', su.copy())
        pdu['name'] = 'Test Project 06'
        # The project DEFAULT_USER is read only.
        self._test_project_user_with_valid_permissions(
            self.project_uri, method, default_user=False, request_data=data)

    def test_PATCH_project_detail_with_invalid_permissions(self):
        """
        Test that a PATCH to project_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        kwargs = self._setup_user_credentials()
        user, client = self._create_user(**kwargs)
        method = 'patch'
        data = {}
        su = data.setdefault('SU', {})
        su['name'] = 'Test Project 01'
        su['inventory_type'] = self.in_type_uri
        su['members'] = [self._resolve('user-detail',
                                       **{'public_id': user.public_id})]
        su['role'] = {'user': user.username, 'role': Membership.DEFAULT_USER}
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_user_with_invalid_permissions(
            self.project_uri, method, request_data=data)
        data.setdefault('POW', su.copy())
        data.setdefault('PMA', su.copy())
        data.setdefault('PDU', su.copy())
        self._test_project_user_with_invalid_permissions(
            self.project_uri, method, request_data=data)

    def test_PATCH_project_detail_with_valid_permissions(self):
        """
        Test that a PATCH to project_detail passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        kwargs = self._setup_user_credentials()
        user, client = self._create_user(**kwargs)
        method = 'patch'
        data = {}
        su = data.setdefault('SU', {})
        su['name'] = 'Test Project 01'
        ad = data.setdefault('AD', {})
        ad['name'] = 'Test Project 02'
        du = data.setdefault('DU', {})
        du['name'] = 'TestProject 03'
        self._test_user_with_valid_permissions(
            self.project_uri, method, request_data=data)
        pow = data.setdefault('POW', {})
        pow['name'] = 'Test Project 04'
        pma = data.setdefault('PMA', {})
        pma['name'] = 'Test Project 05'
        pdu = data.setdefault('PDU', {})
        pdu['name'] = 'Test Project 06'
        # The project DEFAULT_USER is read only.
        self._test_project_user_with_valid_permissions(
            self.project_uri, method, default_user=False, request_data=data)

    def test_DELETE_project_detail_with_invalid_permissions(self):
        """
        Test that a DELETE to project_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'delete'
        self._test_user_with_invalid_permissions(self.project_uri, method)
        self._test_project_user_with_invalid_permissions(
            self.project_uri, method)

    def test_DELETE_project_detail_with_valid_permissions(self):
        """
        Test that a DELETE to project_detail pass' with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        kwargs = self._setup_user_credentials()
        user, client = self._create_user(**kwargs)
        method = 'delete'
        # Test SUPERUSER
        project = self._create_project(self.in_type, name="Test Project 01",
                                       members=[user,])
        uri = reverse('project-detail',
                      kwargs={'public_id': project.public_id})
        self._test_superuser_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test ADMINISTRATOR
        project = self._create_project(self.in_type, name="Test Project 02",
                                       members=[user,])
        uri = reverse('project-detail',
                      kwargs={'public_id': project.public_id})
        self._test_administrator_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test DEFAULT_USER
        ## This is an invalid test since the DEFAULT_USER has no access.
        # Test project OWNER
        project = self._create_project(self.in_type, name="Test Project 03",
                                       members=[user,])
        uri = reverse('project-detail',
                      kwargs={'public_id': project.public_id})
        self._test_project_owner_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test project MANAGER
        project = self._create_project(self.in_type, name="Test Project 04",
                                       members=[user,])
        uri = reverse('project-detail',
                      kwargs={'public_id': project.public_id})
        self._test_project_manager_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test project DEFAULT_USER
        ## This is an invalid test since the project DEFAULT_USER has no access.

    def test_OPTIONS_project_detail_with_invalid_permissions(self):
        """
        Test that the method OPTIONS fails with invald permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'options'
        self._test_user_with_invalid_permissions(self.project_uri, method)
        self._test_project_user_with_invalid_permissions(
            self.project_uri, method)

    def test_OPTIONS_project_detail_with_valid_permissions(self):
        """
        Test that the method OPTIONS brings back the correct data.
        """
        method = 'options'
        self._test_user_with_valid_permissions(self.project_uri, method)
        self._test_project_user_with_valid_permissions(self.project_uri, method)
