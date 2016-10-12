# -*- coding: utf-8 -*-
#
# inventory/projects/api/tests/test_projects.py
#
# Run ./manage.py test -k # Keep the DB, don't rebuild.
#

import random

from rest_framework.reverse import reverse
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND)

from inventory.common.api.tests.base_test import BaseTest
from inventory.projects.models import Project, Membership


class TestProject(BaseTest):

    def __init__(self, name):
        super(TestProject, self).__init__(name)

    def setUp(self):
        super(TestProject, self).setUp()
        # Create an InventoryType.
        self.in_type = self._create_inventory_type()
        kwargs = {'public_id': self.in_type.public_id}
        self.in_type_uri = self._resolve('inventory-type-detail', **kwargs)
        self.project = self._create_project(self.in_type, members=[self.user])
        kwargs = {'public_id': self.project.public_id}
        self.project_uri = self._resolve('project-detail', **kwargs)

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
        pdu['role'] = {'user': user.username, 'role': Membership.OWNER}
        self._test_project_user_with_valid_permissions(
            uri, method, default_user=False, request_data=data)






    def test_update_put_project(self):
        self.skipTest("Temporarily skipped")
        # Create Project with POST.
        uri = reverse('project-list')
        new_data = {'name': 'Test Project', 'public': False, 'active': True,
                    'members': [self.user_uri,], 'managers': [self.user_uri,]}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        self.assertFalse(data.get('public'), msg)
        # Update record with PUT.
        pk = data.get('id')
        uri = reverse('project-detail', kwargs={'pk': pk})
        new_data['public'] = True
        response = self.client.put(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertTrue(data.get('public'), msg)
        # Read record with GET.
        pk = data.get('id')
        uri = reverse('project-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('name'), new_data.get('name'), msg)
        self.assertTrue(data.get('public'), msg)

    def test_update_patch_project(self):
        self.skipTest("Temporarily skipped")
        # Create Project with POST.
        uri = reverse('project-list')
        new_data = {'name': 'Test Project', 'public': False, 'active': True,
                    'members': [self.user_uri,], 'managers': [self.user_uri,]}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        self.assertFalse(data.get('public'), msg)
        # Update record with PATCH.
        pk = data.get('id')
        uri = reverse('project-detail', kwargs={'pk': pk})
        updated_data = {'public': True}
        response = self.client.patch(uri, updated_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertTrue(data.get('public'), msg)
        # Read record with GET.
        pk = data.get('id')
        uri = reverse('project-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('name'), new_data.get('name'), msg)
        self.assertEqual(data.get('public'), updated_data.get('public'), msg)

    def test_delete_project(self):
        self.skipTest("Temporarily skipped")
        # Create Project with POST.
        uri = reverse('project-list')
        new_data = {'name': 'Test Project', 'public': False, 'active': True,
                    'members': [self.user_uri,], 'managers': [self.user_uri,]}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Delete the User.
        pk = data.get('id')
        uri = reverse('project-detail', kwargs={'pk': pk})
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

    def test_options_project(self):
        self.skipTest("Temporarily skipped")
        # Create Project with POST.
        uri = reverse('project-list')
        new_data = {'name': 'Test Project', 'public': False, 'active': True,
                    'members': [self.user_uri,], 'managers': [self.user_uri,]}
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
        self.assertEqual(data.get('name'), 'Project List', msg)
        # Get the API detail OPTIONS.
        uri = reverse('project-detail', kwargs={'pk': pk})
        response = self.client.options(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('name'), 'Project Detail', msg)

    def test_adding_member_patch(self):
        self.skipTest("Temporarily skipped")
        # Create Project with POST.
        uri = reverse('project-list')
        new_data = {'name': 'Test Project', 'public': False, 'active': True,
                    'members': [self.user_uri,], 'managers': [self.user_uri,]}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        self.assertEqual(len(data.get('members')),
                         len(new_data.get('members')), msg)
        # Add member
        pk = data.get('id')
        uri = reverse('project-detail', kwargs={'pk': pk})
        new_user_uri = reverse('user-detail', kwargs={'pk': self.user.pk})
        updated_data = {'members': [self.user_uri, new_user_uri]}
        response = self.client.patch(uri, updated_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(len(data.get('members')),
                         len(updated_data.get('members')), msg)
        # Get the same record through the API.
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertTrue(any([uri for uri in data.get('members')
                             if self.user_uri in uri]), msg)
        self.assertTrue(any([uri for uri in data.get('members')
                             if new_user_uri in uri]), msg)
        self.assertEqual(len(data.get('members')),
                         len(updated_data.get('members')), msg)

    def test_removing_member_patch(self):
        self.skipTest("Temporarily skipped")
        # Create Project with POST.
        uri = reverse('project-list')
        new_user_uri = reverse('user-detail', kwargs={'pk': self.user.pk})
        new_data = {'name': 'Test Project', 'public': False, 'active': True,
                    'members': [self.user_uri, new_user_uri],
                    'managers': [self.user_uri]}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        self.assertEqual(len(data.get('members')),
                         len(new_data.get('members')), msg)
        # Remove member
        pk = data.get('id')
        uri = reverse('project-detail', kwargs={'pk': pk})
        updated_data = {'members': [self.user_uri]}
        response = self.client.patch(uri, updated_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(len(data.get('members')),
                         len(updated_data.get('members')), msg)
        # Get the same record through the API.
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertTrue(any([uri for uri in data.get('members')
                             if self.user_uri in uri]), msg)
        self.assertFalse(any([uri for uri in data.get('members')
                              if new_user_uri in uri]), msg)
        self.assertEqual(len(data.get('members')),
                         len(updated_data.get('members')), msg)

    def test_adding_manager_patch(self):
        self.skipTest("Temporarily skipped")
        # Create Project with POST.
        uri = reverse('project-list')
        new_data = {'name': 'Test Project', 'public': False, 'active': True,
                    'members': [self.user_uri,], 'managers': [self.user_uri,]}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        self.assertEqual(len(data.get('managers')),
                         len(new_data.get('managers')), msg)
        # Add manager
        pk = data.get('id')
        uri = reverse('project-detail', kwargs={'pk': pk})
        new_user_uri = reverse('user-detail', kwargs={'pk': self.user.pk})
        updated_data = {'managers': [self.user_uri, new_user_uri]}
        response = self.client.patch(uri, updated_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(len(data.get('managers')),
                         len(updated_data.get('managers')), msg)
        # Get the same record through the API.
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertTrue(any([uri for uri in data.get('managers')
                             if self.user_uri in uri]), msg)
        self.assertTrue(any([uri for uri in data.get('managers')
                             if new_user_uri in uri]), msg)
        self.assertEqual(len(data.get('managers')),
                         len(updated_data.get('managers')), msg)

    def test_removing_manager_patch(self):
        self.skipTest("Temporarily skipped")
        # Create Project with POST.
        uri = reverse('project-list')
        new_user_uri = reverse('user-detail', kwargs={'pk': self.user.pk})
        new_data = {'name': 'Test Project', 'public': False, 'active': True,
                    'members': [self.user_uri,],
                    'managers': [self.user_uri, new_user_uri]}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        self.assertEqual(len(data.get('managers')),
                         len(new_data.get('managers')), msg)
        # Remove manager
        pk = data.get('id')
        uri = reverse('project-detail', kwargs={'pk': pk})
        updated_data = {'managers': [self.user_uri]}
        response = self.client.patch(uri, updated_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(len(data.get('managers')),
                         len(updated_data.get('managers')), msg)
        # Get the same record through the API.
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertTrue(any([uri for uri in data.get('managers')
                             if self.user_uri in uri]), msg)
        self.assertFalse(any([uri for uri in data.get('managers')
                              if new_user_uri in uri]), msg)
        self.assertEqual(len(data.get('managers')),
                         len(updated_data.get('managers')), msg)
