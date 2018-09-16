# -*- coding: utf-8 -*-
#
# inventory/projects/api/tests/test_projects_api.py
#

import random

from django.contrib.auth import get_user_model

from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APIClient

from inventory.common.api.tests.base_test import BaseTest
from inventory.projects.models import Project, Membership

UserModel = get_user_model()


class TestInventoryType(BaseTest):

    def __init__(self, name):
        super().__init__(name)

    def setUp(self):
        super().setUp()
        # Create an InventoryType and a Project.
        self.in_type = self._create_inventory_type()
        kwargs = {'public_id': self.in_type.public_id}
        self.in_type_uri = reverse('inventory-type-detail', kwargs=kwargs)
        self.project = self._create_project(self.in_type, members=[self.user])

    def test_GET_inventory_type_list_with_invalid_permissions(self):
        """
        Test the inventory-type-list endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        kwargs = self._setup_user_credentials()
        # Test that an unauthenticated superuser has no permissions.
        kwargs['login'] = False
        kwargs['is_superuser'] = True
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        response = client.get(self.in_type_uri, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN, response.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })
        # Test that an unauthenticated ADMINISTRATOR has no permissions.
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.ADMINISTRATOR
        user, client = self._create_user(**kwargs)
        response = client.get(self.in_type_uri, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN, response.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })
        # Test that a DEFAULT_USER has no permissions.
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        response = client.get(self.in_type_uri, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN, response.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['permission'],
            })
        # Test that a project PROJECT_OWNER has no permissions.
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        self.project.process_members([self.user, user])
        self.project.set_role(user, Membership.PROJECT_OWNER)
        response = client.get(self.in_type_uri, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN, response.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })
        # Test that a PROJECT_MANAGER has no permissions.
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        self.project.set_role(user, Membership.PROJECT_MANAGER)
        response = client.get(self.in_type_uri, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN, response.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })
        # Test that a PROJECT_USER has no access.
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        self.project.set_role(user, Membership.PROJECT_USER)
        response = client.get(self.in_type_uri, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN, response.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })

    def test_GET_inventory_type_list_with_valid_permissions(self):
        """
        Test the inventory-type-list endpoint with various permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        uri = reverse('inventory-type-list')
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_POST_inventory_type_list_with_invalid_permissions(self):
        """
        Test that a POST to inventory-type-list fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        kwargs = self._setup_user_credentials()
        user, client = self._create_user(**kwargs)
        method = 'post'
        uri = reverse('inventory-type-list')
        data = {}
        su = data.setdefault('SU', {})
        su['name'] = 'My Test Inventory Type'
        su['description'] = 'Test inventory type description.'
        ad = data.setdefault('AD', su.copy())
        du = data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            uri, method, request_data=data)
        pow = data.setdefault('POW', su.copy())
        pma = data.setdefault('PMA', su.copy())
        pdu = data.setdefault('PDU', su.copy())
        self._test_project_users_with_invalid_permissions(
            uri, method, request_data=data)

    def test_POST_inventory_type_list_with_valid_permissions(self):
        """
        Test that a POST to inventory-type-list passes with valid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        kwargs = self._setup_user_credentials()
        user, client = self._create_user(**kwargs)
        method = 'post'
        uri = reverse('inventory-type-list')
        data = {}
        su = data.setdefault('SU', {})
        su['name'] = 'My Test Inventory Type 1'
        su['description'] = 'Test inventory type description.'
        ad = data.setdefault('AD', su.copy())
        ad['name'] = 'My Test Inventory Type 2'
        du = data.setdefault('DU', su.copy())
        du['name'] = 'My Test Inventory Type 3'
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)
        # All project users will fails as tested in the previous test.

    def test_OPTIONS_inventory_type_list_with_invalid_permissions(self):
        """
        Test that the method OPTIONS fails with invald permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'options'
        uri = reverse('inventory-type-list')
        self._test_users_with_invalid_permissions(
            uri, method, default_user=False)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_OPTIONS_inventory_type_list_with_valid_permissions(self):
        """
        Test that the method OPTIONS brings back the correct data.
        """
        #self.skipTest("Temporarily skipped")
        method = 'options'
        uri = reverse('inventory-type-list')
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_GET_inventory_type_detail_with_invalid_permissions(self):
        """
        Test that a GET on the inventory-type-detail fails with invalid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        self._test_users_with_invalid_permissions(self.in_type_uri, method)
        self._test_project_users_with_invalid_permissions(
            self.in_type_uri, method)

    def test_GET_inventory_type_detail_with_valid_permissions(self):
        """
        Test that a GET to inventory-type-detail passes with valid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        self._test_users_with_valid_permissions(self.in_type_uri, method)
        self._test_project_users_with_valid_permissions(
            self.in_type_uri, method)

    def test_PUT_inventory_type_detail_with_invalid_permissions(self):
        """
        Test that a PUT to inventory-type-detail fails with invalid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        kwargs = self._setup_user_credentials()
        user, client = self._create_user(**kwargs)
        method = 'put'
        data = {}
        su = data.setdefault('SU', {})
        su['name'] = 'My Test Inventory Type'
        su['description'] = 'Test inventory type description.'
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            self.in_type_uri, method, request_data=data)
        data.setdefault('POW', su.copy())
        data.setdefault('PMA', su.copy())
        data.setdefault('PDU', su.copy())
        self._test_project_users_with_invalid_permissions(
            self.in_type_uri, method, request_data=data)

    def test_PUT_inventory_type_detail_with_valid_permissions(self):
        """
        Test that a PUT to inventory-type-detail passes with valid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        kwargs = self._setup_user_credentials()
        user, client = self._create_user(**kwargs)
        method = 'put'
        data = {}
        su = data.setdefault('SU', {})
        su['name'] = 'My Test Inventory Type 01'
        ad = data.setdefault('AD', su.copy())
        ad['name'] = 'My Test Inventory Type 02'
        du = data.setdefault('DU', su.copy())
        du['name'] = 'My Test Inventory Type 03'
        self._test_users_with_valid_permissions(
            self.in_type_uri, method, request_data=data)
        # All project users will fails as tested in the previous test.

    def test_PATCH_inventory_type_detail_with_invalid_permissions(self):
        """
        Test that a PATCH to inventory-type-detail fails with invalid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        kwargs = self._setup_user_credentials()
        user, client = self._create_user(**kwargs)
        method = 'patch'
        data = {}
        su = data.setdefault('SU', {})
        su['name'] = 'My Test Inventory Type'
        su['description'] = 'Test inventory type description.'
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            self.in_type_uri, method, request_data=data)
        data.setdefault('POW', su.copy())
        data.setdefault('PMA', su.copy())
        data.setdefault('PDU', su.copy())
        self._test_project_users_with_invalid_permissions(
            self.in_type_uri, method, request_data=data)

    def test_PATCH_inventory_type_detail_with_valid_permissions(self):
        """
        Test that a PATCH to inventory-type-detail passes with valid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        kwargs = self._setup_user_credentials()
        user, client = self._create_user(**kwargs)
        method = 'patch'
        data = {}
        su = data.setdefault('SU', {})
        su['description'] = 'Test inventory type description.'
        su['name'] = 'My Test Inventory Type 01'
        ad = data.setdefault('AD', {})
        ad['name'] = 'My Test Inventory Type 02'
        du = data.setdefault('DU', {})
        du['name'] = 'My Test Inventory Type 03'
        self._test_users_with_valid_permissions(
            self.in_type_uri, method, request_data=data)
        # All project users will fails as tested in the previous test.

    def test_DELETE_inventory_type_detail_with_invalid_permissions(self):
        """
        Test that a DELETE to inventory-type-detail fails with invalid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'delete'
        self._test_users_with_invalid_permissions(self.in_type_uri, method)
        self._test_project_users_with_invalid_permissions(
            self.in_type_uri, method)

    def test_DELETE_inventory_type_detail_with_valid_permissions(self):
        """
        Test that a DELETE to inventory-type-detail pass' with valid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        # All users will fail as tested in the previous test.

    def test_OPTIONS_project_detail_with_invalid_permissions(self):
        """
        Test that the method OPTIONS fails with invald permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'options'
        self._test_users_with_invalid_permissions(self.in_type_uri, method)
        self._test_project_users_with_invalid_permissions(
            self.in_type_uri, method)

    def test_OPTIONS_project_detail_with_valid_permissions(self):
        """
        Test that the method OPTIONS brings back the correct data.
        """
        method = 'options'
        self._test_users_with_valid_permissions(self.in_type_uri, method)
        self._test_project_users_with_valid_permissions(
            self.in_type_uri, method)


class TestProject(BaseTest):

    def __init__(self, name):
        super().__init__(name)

    def setUp(self):
        super().setUp()
        # Create an InventoryType and a Project.
        self.in_type = self._create_inventory_type()
        kwargs = {'public_id': self.in_type.public_id}
        self.in_type_uri = reverse('inventory-type-detail', kwargs=kwargs)
        self.project = self._create_project(self.in_type, members=[self.user])
        kwargs = {'public_id': self.project.public_id}
        self.project_uri = reverse('project-detail', kwargs=kwargs)

    ## def test_GET_condition_errors(self):
    ##     self.skipTest("Temporarily skipped")
    ##     username = 'Normal_User'
    ##     password = '123456'
    ##     kwargs = {}
    ##     kwargs['username'] = username
    ##     kwargs['password'] = password
    ##     kwargs['is_superuser'] = True
    ##     kwargs['is_active'] = True
    ##     user = UserModel(**kwargs)
    ##     user.save()
    ##     client = APIClient()
    ##     client.force_authenticate(user=user)
    ##     response = client.get(
    ##         self.project_uri, format='json',
    ##         **{'HTTP_ACCEPT': 'application/json',})
    ##     msg = "Response: {} should be {}, content: {}".format(
    ##         response.status_code, status.HTTP_200_OK, response.data)
    ##     self.assertEqual(response.status_code, status.HTTP_200_OK, msg)

    def test_GET_project_list_with_invalid_permissions(self):
        """
        Test the project-list endpoint with no permissions. This is the
        one endpoint where a PROJECT_USER can create an object, so it will
        not fail, therefore we skip it.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        uri = reverse('project-list')
        self._test_users_with_invalid_permissions(
            uri, method, default_user=False)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_GET_project_list_with_valid_permissions(self):
        """
        Test the project-list endpoint with various permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        uri = reverse('project-list')
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_POST_project_list_with_invalid_permissions(self):
        """
        Test that a POST to project-list fails with invalid permissions.
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
        su['members'] = [
            reverse('user-detail', kwargs={'public_id': user.public_id})]
        su['role'] = {'user': user.username, 'role': Membership.PROJECT_USER}
        ad = data.setdefault('AD', su.copy())
        #du = data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            uri, method, request_data=data, default_user=False)
        pow = data.setdefault('POW', su.copy())
        pma = data.setdefault('PMA', su.copy())
        #pdu = data.setdefault('PDU', su.copy())
        self._test_project_users_with_invalid_permissions(
            uri, method, request_data=data, project_user=False)

    def test_POST_project_list_with_valid_permissions(self):
        """
        Test that a POST to project-list passes with valid permissions.
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
        su['members'] = [
            reverse('user-detail', kwargs={'public_id': user.public_id})]
        su['role'] = {'user': user.username, 'role': Membership.PROJECT_USER}
        ad = data.setdefault('AD', su.copy())
        ad['name'] = 'My Test Project 2'
        du = data.setdefault('DU', su.copy())
        du['name'] = 'My Test Project 3'
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)
        pow = data.setdefault('POW', su.copy())
        pow['name'] = 'My Test Project 4'
        pma = data.setdefault('PMA', su.copy())
        pma['name'] = 'My Test Project 5'
        pdu = data.setdefault('PDU', su.copy())
        pdu['name'] = 'My Test Project 6'
        pdu['role'] = {'user': user.username, 'role': Membership.PROJECT_USER}
        self._test_project_users_with_valid_permissions(
            uri, method, project_user=False, request_data=data)

    def test_OPTIONS_project_list_with_invalid_permissions(self):
        """
        Test that the method OPTIONS fails with invald permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'options'
        uri = reverse('project-list')
        self._test_users_with_invalid_permissions(
            uri, method, default_user=False)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_OPTIONS_project_list_with_valid_permissions(self):
        """
        Test that the method OPTIONS brings back the correct data.
        """
        #self.skipTest("Temporarily skipped")
        method = 'options'
        uri = reverse('project-list')
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_GET_project_detail_with_invalid_permissions(self):
        """
        Test that a GET on the project-detail fails with invalid
        permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        self._test_users_with_invalid_permissions(self.project_uri, method)
        self._test_project_users_with_invalid_permissions(
            self.project_uri, method)

    def test_GET_project_detail_with_valid_permissions(self):
        """
        Test that a GET to project-detail passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        self._test_users_with_valid_permissions(self.project_uri, method)
        self._test_project_users_with_valid_permissions(
            self.project_uri, method)

    def test_PUT_project_detail_with_invalid_permissions(self):
        """
        Test that a PUT to project-detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        kwargs = self._setup_user_credentials()
        user, client = self._create_user(**kwargs)
        method = 'put'
        data = {}
        su = data.setdefault('SU', {})
        su['name'] = 'Test Project 01'
        su['inventory_type'] = self.in_type_uri
        su['members'] = [
            reverse('user-detail', kwargs={'public_id': user.public_id})]
        su['role'] = {'user': user.username, 'role': Membership.PROJECT_USER}
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            self.project_uri, method, request_data=data)
        data.setdefault('POW', su.copy())
        data.setdefault('PMA', su.copy())
        data.setdefault('PDU', su.copy())
        self._test_project_users_with_invalid_permissions(
            self.project_uri, method, request_data=data)

    def test_PUT_project_detail_with_valid_permissions(self):
        """
        Test that a PUT to project-detail passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        kwargs = self._setup_user_credentials()
        user, client = self._create_user(**kwargs)
        method = 'put'
        data = {}
        su = data.setdefault('SU', {})
        su['name'] = 'Test Project 01'
        su['inventory_type'] = self.in_type_uri
        su['members'] = [
            reverse('user-detail', kwargs={'public_id': user.public_id})]
        su['role'] = {'user': user.username, 'role': Membership.PROJECT_USER}
        ad = data.setdefault('AD', su.copy())
        ad['name'] = 'Test Project 02'
        du = data.setdefault('DU', su.copy())
        du['name'] = 'Test Project 03'
        self._test_users_with_valid_permissions(
            self.project_uri, method, default_user=False, request_data=data)
        pow = data.setdefault('POW', su.copy())
        pow['name'] = 'Test Project 04'
        pma = data.setdefault('PMA', su.copy())
        pma['name'] = 'Test Project 05'
        pdu = data.setdefault('PDU', su.copy())
        pdu['name'] = 'Test Project 06'
        # The PROJECT_USER is read only.
        self._test_project_users_with_valid_permissions(
            self.project_uri, method, project_user=False, request_data=data)

    def test_PATCH_project_detail_with_invalid_permissions(self):
        """
        Test that a PATCH to project-detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        kwargs = self._setup_user_credentials()
        user, client = self._create_user(**kwargs)
        method = 'patch'
        data = {}
        su = data.setdefault('SU', {})
        su['name'] = 'Test Project 01'
        su['inventory_type'] = self.in_type_uri
        su['members'] = [
            reverse('user-detail', kwargs={'public_id': user.public_id})]
        su['role'] = {'user': user.username, 'role': Membership.PROJECT_USER}
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            self.project_uri, method, request_data=data)
        data.setdefault('POW', su.copy())
        data.setdefault('PMA', su.copy())
        data.setdefault('PDU', su.copy())
        self._test_project_users_with_invalid_permissions(
            self.project_uri, method, request_data=data)

    def test_PATCH_project_detail_with_valid_permissions(self):
        """
        Test that a PATCH to project-detail passes with valid permissions.
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
        self._test_users_with_valid_permissions(
            self.project_uri, method, request_data=data)
        pow = data.setdefault('POW', {})
        pow['name'] = 'Test Project 04'
        pma = data.setdefault('PMA', {})
        pma['name'] = 'Test Project 05'
        pdu = data.setdefault('PDU', {})
        pdu['name'] = 'Test Project 06'
        # The PROJECT_USER is read only.
        self._test_project_users_with_valid_permissions(
            self.project_uri, method, project_user=False, request_data=data)

    def test_DELETE_project_detail_with_invalid_permissions(self):
        """
        Test that a DELETE to project-detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'delete'
        self._test_users_with_invalid_permissions(self.project_uri, method)
        self._test_project_users_with_invalid_permissions(
            self.project_uri, method)

    def test_DELETE_project_detail_with_valid_permissions(self):
        """
        Test that a DELETE to project-detail pass' with valid permissions.
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
        # Test PROJECT_OWNER
        project = self._create_project(self.in_type, name="Test Project 03",
                                       members=[user,])
        uri = reverse('project-detail',
                      kwargs={'public_id': project.public_id})
        self._test_project_owner_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test project MANAGER
        ## This is an invalid test since the PROJECT_MANAGER cannot delete.
        # Test project PROJECT_USER
        ## This is an invalid test since the PROJECT_USER has no access.

    def test_OPTIONS_project_detail_with_invalid_permissions(self):
        """
        Test that the method OPTIONS fails with invald permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'options'
        self._test_users_with_invalid_permissions(self.project_uri, method)
        self._test_project_users_with_invalid_permissions(
            self.project_uri, method)

    def test_OPTIONS_project_detail_with_valid_permissions(self):
        """
        Test that the method OPTIONS brings back the correct data.
        """
        #self.skipTest("Temporarily skipped")
        method = 'options'
        self._test_users_with_valid_permissions(self.project_uri, method)
        self._test_project_users_with_valid_permissions(
            self.project_uri, method)

    def test_special_case_project_inventory_type(self):
        """
        Test the special case where either inventory_type (HREF) or
        inventory_type_public_id (public_id) must be used.
        """
        #self.skipTest("Temporarily skipped")
        kwargs = self._setup_user_credentials()
        method = 'put'
        # Test populating inventory_type with a URI.
        data = {}
        su = data.setdefault('SU', {})
        su['name'] = 'Test Project 01'
        su['inventory_type'] = self.in_type_uri
        self._test_superuser_with_valid_permissions(
            self.project_uri, method, request_data=data)
        # Test populating inventory_type_public_id with a public ID.
        data = {}
        su = data.setdefault('SU', {})
        su['name'] = 'Test Project 01'
        su['inventory_type_public_id'] = self.in_type.public_id
        self._test_superuser_with_valid_permissions(
            self.project_uri, method, request_data=data)
        # Test invalid inventory_type_public_id.
        data = {}
        data['name'] = 'Test Project 01'
        data['inventory_type_public_id'] = "qwertyuiop"
        response = getattr(self.client, method)(
            self.project_uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        error_key = 'inventory_type_public_id'
        msg = "Should have error with key '{}'".format(error_key)
        self.assertTrue(self._has_error(response, error_key=error_key), msg)
        self._test_errors(response, tests={
            error_key: "Could not find InventoryType with public_id"
            })
        # Test missing inventory_type or inventory_type_public_id.
        data = {}
        data['name'] = 'Test Project 01'
        response = getattr(self.client, method)(
            self.project_uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        error_key = 'non_field_errors'
        msg = "Should have error with key '{}'".format(error_key)
        #self.assertTrue(self._has_error(response, error_key=error_key), msg)
        self._test_errors(response, tests={
            error_key: "Must choose a valid "
            })

    def test_set_user(self):
        """
        Test that an invalid user raises an validation exception.
        """
        #self.skipTest("Temporarily skipped")
        # Setup user for valid POST test.
        kwargs = self._setup_user_credentials()
        user, client = self._create_user(**kwargs)
        method = 'post'
        uri = reverse('project-list')
        data = {}
        # Test valid POST
        su = data.setdefault('SU', {})
        su['name'] = 'Test Project 01'
        su['inventory_type'] = self.in_type_uri
        su['members'] = [
            reverse('user-detail', kwargs={'public_id': user.public_id})]
        su['role'] = {'user': user.username, 'role': Membership.PROJECT_USER}
        self._test_superuser_with_valid_permissions(
            uri, method, request_data=data)
        # Test invalid POST
        su['role'] = {'user': 'Garbage_Name', 'role': Membership.PROJECT_USER}
        response = client.post(uri, data=su, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        self.assertTrue(self._has_error(response, error_key='role'), msg)
        self._test_errors(response, tests={
            'role': "is not a valid user for setting a role."
            })
        # Test with a string numeric value.
        su['role'] = {
            'user': user.username, 'role': str(Membership.PROJECT_USER)
            }
        response = client.post(uri, data=su, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Test invalid numeric value for the role.
        su['role'] = {'user': user.username, 'role': 100}
        response = client.post(uri, data=su, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        self.assertTrue(self._has_error(response, error_key='role'), msg)
        self._test_errors(response, tests={
            'role': " is not a valid role."
            })
        # Test an invalid empty string or None value for the role.
        su['role'] = {'user': user.username, 'role': ''}
        response = client.post(uri, data=su, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        self.assertTrue(self._has_error(response, error_key='role'), msg)
        self._test_errors(response, tests={
            'role': "The user project role '' is not valid."
            })
        su['role'] = {'user': user.username, 'role': None}
        response = client.post(uri, data=su, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        self.assertTrue(self._has_error(response, error_key='role'), msg)
        self._test_errors(response, tests={
            'role': "The user project role 'None' is not valid."
            })
