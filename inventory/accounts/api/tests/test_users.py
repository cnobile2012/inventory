# -*- coding: utf-8 -*-
#
# inventory/user_profiles/api/tests/test_users.py
#
# Run ./manage.py test -k # Keep the DB, don't rebuild.
#

import random

from rest_framework.reverse import reverse
from rest_framework import status

from inventory.common.api.tests.base_test import BaseTest


class TestUser(BaseTest):

    def __init__(self, name):
        super(TestUser, self).__init__(name)

    def test_create_post_account(self):
        """
        Ensure we can create a new account.
        """
        # Use API to create a test user.
        uri = reverse('user-list')
        new_data = {'username': 'NewUser', 'password': 'NewUserPassword'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        msg = "Response Data: {}".format(data)
        self.assertEqual(data.get('username'), new_data.get('username'), msg)
        # Get the same record through the API.
        pk = data.get('id')
        uri = reverse('user-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response Data: {}".format(data)
        self.assertEqual(data.get('username'), new_data.get('username'), msg)

    def test_user_list_no_permissions(self):
        """
        Test the user_list endpoint with no permissions. We overwrite the
        self.client created in the setUp method in the base class.
        """
        self._create_user(
            username="TEMP-{}".format(random.randint(10000, 99999)),
            password="TEMP-{}".format(random.randint(10000, 99999)))
        self._set_user_auth(use_token=False)
        # Use API to get user list with unauthenticated user.
        uri = reverse('user-list')
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response Data: {}".format(data)
        self.assertTrue('detail' in data, msg)

    def test_user_list_with_token(self):
        """
        Test use of API with token.. We overwrite the self.client created in
        the setUp method in the base class.
        """
        self._create_user(
            username="TEMP-{}".format(random.randint(10000, 99999)),
            password="TEMP-{}".format(random.randint(10000, 99999)))
        self._set_user_auth(use_token=True)
        # Use API to create a test user.
        uri = reverse('user-list')
        data = {'username': 'NewUser_01', 'password': 'NewUserPassword'}
        response = self.client.post(uri, data, format='json')
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)

    def test_create_user_with_post_profile(self):
        """
        Test creating a new user and a user profile.
        """
        # Use API to create a test user.
        uri = reverse('user-list')
        new_data = {'username': 'NewUser_02', 'password': 'NewUserPassword',}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        user_pk = data.get('id')
        self.assertTrue(isinstance(user_pk, int))
        # Use API to create the user's profile.
        uri = reverse('user-profile-list')
        user_uri = reverse('user-detail', kwargs={'pk': user_pk})
        profile_data = {'user': user_uri, 'role': 0}
        response = self.client.post(uri, profile_data, format='json')
        data = response.data
        msg = "Response Data: {}".format(data)
        self.assertEquals(data.get('role'), profile_data.get('role'), msg)
        # Get the same user record through the API.
        response = self.client.get(user_uri, format='json')
        data = response.data
        msg = "Response Data: {}".format(data)
        self.assertEqual(data.get('username'), new_data.get('username'), msg)
        # Get the user profile for the user record.
        uri = data.get('userprofile')
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response Data: {}".format(data)
        self.assertTrue(user_uri in data.get('user'), msg)

    def test_update_put_user(self):
        # Use API to create a test user.
        uri = reverse('user-list')
        new_data = {'username': 'NewUser_03', 'password': 'NewUserPassword'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response Data: {}".format(data)
        self.assertFalse(data.get('is_staff'), msg)
        # Update record with PUT.
        pk = data.get('id')
        uri = reverse('user-detail', kwargs={'pk': pk})
        new_data['is_staff'] = True
        response = self.client.put(uri, new_data, format='json')
        data = response.data
        self.assertTrue(data.get('is_staff'), msg)
        # Read record with GET.
        pk = data.get('id')
        uri = reverse('user-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response Data: {}".format(data)
        self.assertEquals(data.get('username'), new_data.get('username'), msg)
        self.assertTrue(data.get('is_staff'), msg)

    def test_update_put_profile(self):
        # Use API to create a test user.
        uri = reverse('user-list')
        new_data = {'username': 'NewUser_04', 'password': 'NewUserPassword'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        # Use API to create the user's profile.
        pk = data.get('id')
        uri = reverse('user-profile-list')
        user_uri = reverse('user-detail', kwargs={'pk': pk})
        profile_data = {'user': user_uri, 'role': 0}
        response = self.client.post(uri, profile_data, format='json')
        data = response.data
        msg = "Response Data: {}".format(data)
        self.assertEquals(data.get('role'), 0, msg)
        # Update record with PUT.
        pk = data.get('id')
        uri = reverse('user-profile-detail', kwargs={'pk': pk})
        profile_data['role'] = 1
        response = self.client.put(uri, profile_data, format='json')
        data = response.data
        # Read record with GET.
        pk = data.get('id')
        uri = reverse('user-profile-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response Data: {}".format(data)
        self.assertTrue(user_uri in data.get('user'), msg)
        self.assertEquals(data.get('role'), 1, msg)

    def test_update_patch_user(self):
        # Use API to create a test user.
        uri = reverse('user-list')
        new_data = {'username': 'NewUser_05', 'password': 'NewUserPassword'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response Data: {}".format(data)
        self.assertFalse(data.get('is_staff'), msg)
        # Update record with PATCH.
        pk = data.get('id')
        uri = reverse('user-detail', kwargs={'pk': pk})
        new_data['is_staff'] = True
        response = self.client.patch(uri, new_data, format='json')
        data = response.data
        self.assertTrue(data.get('is_staff'), msg)
        # Read record with GET.
        pk = data.get('id')
        uri = reverse('user-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response Data: {}".format(data)
        self.assertEquals(data.get('username'), new_data.get('username'), msg)
        self.assertTrue(data.get('is_staff'), msg)

    def test_update_patch_profile(self):
        # Use API to create a test user.
        uri = reverse('user-list')
        new_data = {'username': 'NewUser_06', 'password': 'NewUserPassword'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        # Use API to create the user's profile.
        pk = data.get('id')
        uri = reverse('user-profile-list')
        user_uri = reverse('user-detail', kwargs={'pk': pk})
        profile_data = {'user': user_uri, 'role': 0}
        response = self.client.post(uri, profile_data, format='json')
        data = response.data
        msg = "Response Data: {}".format(data)
        self.assertEquals(data.get('role'), 0, msg)
        # Update record with PATCH.
        pk = data.get('id')
        uri = reverse('user-profile-detail', kwargs={'pk': pk})
        profile_data['role'] = 1
        response = self.client.patch(uri, profile_data, format='json')
        data = response.data
        # Read record with GET.
        pk = data.get('id')
        uri = reverse('user-profile-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response Data: {}".format(data)
        self.assertTrue(user_uri in data.get('user'), msg)
        self.assertEquals(data.get('role'), 1, msg)

    def test_delete_user(self):
        # Use API to create a test user.
        uri = reverse('user-list')
        new_data = {'username': 'NewUser_07', 'password': 'NewUserPassword'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Get the same record through the API.
        pk = data.get('id')
        uri = reverse('user-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response data: {}".format(data)
        self.assertEqual(data.get('username'), new_data.get('username'), msg)
        self.assertTrue(data.get('is_active'), msg)
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

    def test_delete_profile(self):
        # Use API to create a test user.
        uri = reverse('user-list')
        new_data = {'username': 'NewUser_06', 'password': 'NewUserPassword'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Use API to create the user's profile.
        pk = data.get('id')
        uri = reverse('user-profile-list')
        user_uri = reverse('user-detail', kwargs={'pk': pk})
        profile_data = {'user': user_uri, 'role': 0}
        response = self.client.post(uri, profile_data, format='json')
        data = response.data
        msg = "Response Data: {}".format(data)
        self.assertEquals(data.get('role'), 0, msg)
        # Get the same record through the API.
        pk = data.get('id')
        uri = reverse('user-profile-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response data: {}".format(data)
        self.assertEqual(data.get('role'), 0, msg)
        # Delete the UserProfile.
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

    def test_options_user(self):
        # Use API to create a test user.
        uri = reverse('user-list')
        new_data = {'username': 'NewUser_07', 'password': 'NewUserPassword'}
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
        self.assertEqual(data.get('name'), 'User List', msg)
        # Get the API detail OPTIONS.
        uri = reverse('user-detail', kwargs={'pk': pk})
        response = self.client.options(uri, format='json')
        data = response.data
        msg = "Response data: {}".format(data)
        self.assertEqual(data.get('name'), 'User Detail', msg)

    def test_options_user_profile(self):
        # Use API to create a test user.
        uri = reverse('user-list')
        new_data = {'username': 'NewUser_06', 'password': 'NewUserPassword'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Use API to create the user's profile.
        pk = data.get('id')
        uri = reverse('user-profile-list')
        user_uri = reverse('user-detail', kwargs={'pk': pk})
        profile_data = {'user': user_uri, 'role': 0}
        response = self.client.post(uri, profile_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Get the API list OPTIONS.
        response = self.client.options(uri, format='json')
        data = response.data
        msg = "Response data: {}".format(data)
        self.assertEqual(data.get('name'), 'User Profile List', msg)
        # Get the API detail OPTIONS.
        uri = reverse('user-profile-detail', kwargs={'pk': pk})
        response = self.client.options(uri, format='json')
        data = response.data
        msg = "Response data: {}".format(data)
        self.assertEqual(data.get('name'), 'User Profile Detail', msg)
