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
from inventory.projects.models import Project


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
        self.user_uri = reverse('user-detail', kwargs={'pk': user_pk})

    def test_create_post_project(self):
        # Create Project with POST.
        #self.skipTest("Temporarily skipped")
        uri = reverse('project-list')
        new_data = {'name': 'Test Project', 'public': False, 'active': True,
                    'members': [self.user_uri,], 'managers': [self.user_uri,]}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Read record with GET.
        pk = data.get('id')
        uri = reverse('project-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEquals(data.get('name'), new_data.get('name'), msg)
        self.assertTrue(data.get('active'), msg)

    def test_get_project_with_no_permissions(self):
        """
        Test the project_list endpoint with no permissions. We don't use the
        self.client created in the setUp method from the base class.
        """
        #self.skipTest("Temporarily skipped")
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(username, password, login=False)
        project = self._create_project(user)
        # Use API to get user list with unauthenticated user.
        uri = reverse('project-list')
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue('detail' in data, msg)

    def test_create_project_post_token(self):
        """
        Test project with API with token. We don't use the self.client
        created in the setUp method from the base class.
        """
        #self.skipTest("Temporarily skipped")
        # Create a non-logged in user, but one that has a valid token.
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(username, password,
                                                email='test@example.com')
        app_name = 'Token Test'
        data = self._make_app_token(
            user, app_name, client, client_type='public',
            grant_type='client_credentials')
        # Use API to create a supplier.
        uri = reverse('project-list')
        new_data = {'name': 'Test Project', 'public': False, 'active': True,
                    'members': [self.user_uri,], 'managers': [self.user_uri,]}
        response = client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)

    def test_update_put_project(self):
        #self.skipTest("Temporarily skipped")
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
        self.assertEquals(data.get('name'), new_data.get('name'), msg)
        self.assertTrue(data.get('public'), msg)

    def test_update_patch_project(self):
        #self.skipTest("Temporarily skipped")
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
        self.assertEquals(data.get('name'), new_data.get('name'), msg)
        self.assertEqual(data.get('public'), updated_data.get('public'), msg)

    def test_delete_project(self):
        #self.skipTest("Temporarily skipped")
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
        #self.skipTest("Temporarily skipped")
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
        #self.skipTest("Temporarily skipped")
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
        #self.skipTest("Temporarily skipped")
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
        #self.skipTest("Temporarily skipped")
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
        #self.skipTest("Temporarily skipped")
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

    def _create_project(self, user):
        new_data = {'name': 'Project01', 'public': False, 'active': True,
                    'updater': self.user, 'creator': self.user}
        project = Project.objects.create(**new_data)
        project.process_managers([user,])
        project.process_members([user,])
        return project
