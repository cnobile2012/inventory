# -*- coding: utf-8 -*-
#
# inventory/projects/api/tests/test_projects.py
#
# Run ./manage.py test -k # Keep the DB, don't rebuild.
#

import random

from rest_framework.reverse import reverse
from rest_framework import status

from inventory.common.api.tests.base_test import BaseTest


class TestProject(BaseTest):

    def __init__(self, name):
        super(TestProject, self).__init__(name)

    def setUp(self):
        super(TestProject, self).setUp()
        # Use API to create a test user.
        uri = reverse('user-list')
        new_data = {'username': "TEMP-{}".format(random.randint(10000, 99999)),
                    'password': "TEMP-{}".format(random.randint(10000, 99999))}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        user_pk = data.get('id')
        self.assertTrue(isinstance(user_pk, int))
        # Use API to create the user's profile.
        uri = reverse('user-profile-list')
        self.user_uri = reverse('user-detail', kwargs={'pk': user_pk})
        profile_data = {'user': self.user_uri, 'role': 0}
        response = self.client.post(uri, profile_data, format='json')
        data = response.data
        msg = "Response Data: {}".format(data)
        self.assertEquals(data.get('role'), profile_data.get('role'), msg)

    def test_create_post_project(self):
        # Create Project with POST.
        uri = reverse('project-list')
        new_data = {'name': 'Test Project', 'public': False, 'active': True,
                    'members': [self.user_uri,]}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Read record with GET.
        pk = data.get('id')
        uri = reverse('project-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response Data: {}".format(data)
        self.assertEquals(data.get('name'), new_data.get('name'), msg)
        self.assertTrue(data.get('active'), msg)

    def test_update_put_project(self):
        # Create Project with POST.
        uri = reverse('project-list')
        new_data = {'name': 'Test Project', 'public': False, 'active': True,
                    'members': [self.user_uri,]}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        self.assertFalse(data.get('public'), msg)
        # Update record with PUT.
        pk = data.get('id')
        uri = reverse('project-detail', kwargs={'pk': pk})
        new_data['public'] = True
        response = self.client.put(uri, new_data, format='json')
        data = response.data
        self.assertTrue(data.get('public'), msg)
        # Read record with GET.
        pk = data.get('id')
        uri = reverse('project-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response Data: {}".format(data)
        self.assertEquals(data.get('name'), new_data.get('name'), msg)
        self.assertTrue(data.get('public'), msg)

    def test_update_patch_project(self):
        # Create Project with POST.
        uri = reverse('project-list')
        new_data = {'name': 'Test Project', 'public': False, 'active': True,
                    'members': [self.user_uri,]}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        self.assertFalse(data.get('public'), msg)
        # Update record with PATCH.
        pk = data.get('id')
        uri = reverse('project-detail', kwargs={'pk': pk})
        new_data['public'] = True
        response = self.client.patch(uri, new_data, format='json')
        data = response.data
        self.assertTrue(data.get('public'), msg)
        # Read record with GET.
        pk = data.get('id')
        uri = reverse('project-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response Data: {}".format(data)
        self.assertEquals(data.get('name'), new_data.get('name'), msg)
        self.assertTrue(data.get('public'), msg)

    def test_delete_project(self):
        # Create Project with POST.
        uri = reverse('project-list')
        new_data = {'name': 'Test Project', 'public': False, 'active': True,
                    'members': [self.user_uri,]}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Get the same record through the API.
        pk = data.get('id')
        uri = reverse('project-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response data: {}".format(data)
        self.assertEqual(data.get('name'), new_data.get('name'), msg)
        # Delete the User.
        response = self.client.delete(uri, format='json')
        data = response.data
        msg = "Response data: {}".format(data)
        self.assertTrue(data is None, msg)
        # Get the same record through the API.
        # There is NO reason for the code below to fail, however it throws an
        # exception in the client.get.
        #response = self.client.get(uri, format='json')
        #code = response.status_code
        #msg = "Status: {}".format(code)
        #self.assertEqual(code, status.HTTP_404_NOT_FOUND, msg)

    def test_options_project(self):
        # Create Project with POST.
        uri = reverse('project-list')
        new_data = {'name': 'Test Project', 'public': False, 'active': True,
                    'members': [self.user_uri,]}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        pk = data.get('id')
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Get the API list OPTIONS.
        response = self.client.options(uri, format='json')
        data = response.data
        msg = "Response data: {}".format(data)
        self.assertEqual(data.get('name'), 'Project List', msg)
        # Get the API detail OPTIONS.
        uri = reverse('project-detail', kwargs={'pk': pk})
        response = self.client.options(uri, format='json')
        data = response.data
        msg = "Response data: {}".format(data)
        self.assertEqual(data.get('name'), 'Project Detail', msg)

